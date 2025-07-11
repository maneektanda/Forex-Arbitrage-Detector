





# #################################### Background Information and Inspiration ####################################

# The Bellman-Ford algorithm can be used to find the shortest path from a starting node to all other nodes within
# a weighted, directed graph. However, where a graph contains a negative edge cycle, the result is meaningless.
# This algorithm can be modified to test for, and identify negative edge cycles. In a financial context such as
# foreign exchange rates, negative edge cycles can be used to identify arbitrage oppotunites.

# To detect an arbitrage opportunity amongst foreign exchange rates, the product of the rates must be greater than
# 1. The Bellman-Ford algorithm is not directly applicable here, as its logic is based off of the summation of edge
# weights. A conversion of some sort, needs to happen, so that the product relationship can be expressed as a sum
# relationship.
# The solution for this problem is not my own and was learned from online materials.
#
# Observe the following-
#
# Let A and B be exchange rates, arbitrage exists when-
# 
# A * B > 1
#
# Taking the natural logarithm of both sides gives-
#
# ln(A * B) > ln(1)
#
# ln(A) + ln(B) > 0
#
# So if we take the natural log of the exchange rates, an arbitrage opportunity exists if the summation is greater
# than 0. If we were to apply Bellman-Ford to the natural log of the exchange rates, the negative edge cycles found
# would just represent transactions where money is lost. Therefore, taking the negative natural log of the exchange
# rates will successfully detect an arbitrage oppotunity.





# Importing required libraries
from tkinter import *
from math import log





# The function called 'Bellman_Ford' in this program was learned from online materials. Whilst the code is my own,
# and written from my gained understanding of the algorithm, the logic is not my own unique work.

def Bellman_Ford(graph):
    
    # Initialise a dictionary where the distance to all nodes will be stored.
    distances = {}

    # Set all distances to infinity.
    for node in graph:
        distances[node] = float('inf')

    # Then pick a starting node, and set the distance to itself as 0.
    # In this case, use the first node in the graph.
    starting_node = list(graph.keys())[0]
    distances[starting_node] = 0

    # Repeat this process one less time than the number of nodes in the graph.
    # The longest possible path cannot exceed this value without having revisited a node.
    for repeat in range(len(graph)-1):

        # For every node in the graph, or key in the dictionary.
        for node in graph:

            # For all of that nodes neighbouring nodes, and the edge weights to get to those neighbouring nodes.
            for neighbouring_node, associated_weight in graph[node]:

                # If the value already stored in the dictionary for that nodes distance from the starting node,
                # plus the edge weight to the neighbouring node, is less than the value already stored for the
                # distance from the starting node to the neighbouring node, then a shorter path has just been
                # found.
                if distances[node] + associated_weight < distances[neighbouring_node]:

                    # Update the distance in the dictionary accordingly.
                    distances[neighbouring_node] = distances[node] + associated_weight

    # Now that the process has been repeated one less time than the number of nodes,
    # the distances should have reached equilibrium if there is no negative edge cycle present.
    # To check this, repeat once more. If any of the distances are updated during this iteration, then a
    # negative edge cycle is present.

    # Create a Boolean variable and set to False
    negative_cycle = False

    # For every node in the graph.
    for node in graph:

        # For all of that nodes neighbouring nodes, and the edge weights to get to those neighbouring nodes.
        for neighbouring_node, associated_weight in graph[node]:

            # If a shorter path is able to be found than what is already stored in the dictionary, a
            # negative edge cycle is present.
            
            # When working with floating point numbers, rounding errors can
            # affect the calculation. In this case, a false arbitrage opportunity may be detected. To prevent
            # this, the distance being checked must be considerably less than the pre-existing distance in
            # the dictionary. This is done by reducing the pre-existing distance by some small amount.
            if distances[node] + associated_weight < distances[neighbouring_node] - 0.000000001:

                # Update the Boolean variable if shorter path found.
                negative_cycle = True

    return negative_cycle





# As previously mentioned, the logic for the 'Bellman_Ford' function was not my own, and was learned from online
# materials. While a method already exists to locate the path of a negative edge cycle found when using the
# Bellman-Ford algorithm, I wanted to test a theory of my own. I have implemented this theory below in the function
# called 'arbitrage_path'.


# ################################################# The Theory ###################################################

# Suppose a negative edge cycle is detected in a graph. If one of the nodes in that cycle, as well as all edges
# connected to that node, is excluded, then the cycle will no longer be present. The 'arbitrage_path' function
# iteratively excludes a node and all of its associated edges from a graph to create a new 'excluded_graph'. It
# then tests again for the negative edge cycle in the 'excluded_graph'. If the cycle is no longer detected, then
# that node must have been in the negative edge cycle. Iteratively excluding all of the nodes allows for a list of
# nodes to be made that form the negative edge cycle.


# ########################################### Recognising Limitations ############################################

# Before completing this function, I realised some limitations.
#
# Firstly, this logic only works when only one cycle is present. Two individual negative edge cycles that do not
# affect each other will clearly not be detected by this logic.
#
# Secondly, the time complexity of this solution is very slow, as you have to run the Bellman_Ford algorithm for
# however many nodes are in the graph.
#
# Thirdly, I have made the assumption that finding the exact path in a forex setting is not necessarily that
# important, because I don't expect there to be too many oppotunites of a long enough length, that the path can't
# be found intuitively once the nodes have been identified.
#
# Despite becoming aware of these limitations, I still thought this would be a great learning experience and
# foundational project in the early stages of my career. I have been able to turn an intuitive thought, into
# actual implemented code.

def arbitrage_path(graph):

    # Create a list to add the nodes that are in a negative cycle to.
    nodes_in_cycle = []

    # For the excluded node in the graph.
    for excluded_node in graph:

        # Create a new graph for that node.
        excluded_graph = {}

        # For each node and value in the entire graph (hence using graph.items() instead of graph[excluded_node])
        for node, value in graph.items():

            # Create a list of edges that will be added to the excluded_graph.
            updated_edges = []

            # Skip over the node that we want to exclude.
            if node == excluded_node:
                continue

            # Otherwise, for every neighbouring_node and weight in the entire graph.
            else:
                for neighbouring_node, weight in value:

                    # Skip over the neighbouring node if its connected to the excluded_node.
                    if neighbouring_node == excluded_node:
                        continue

                    # Otherwise, add it to the list of edges.
                    else:
                        updated_edges.append((neighbouring_node, weight))

                # Update the excluded_graph with the new edges.
                excluded_graph[node] = updated_edges

        # Now check if a negative edge cycle is present with that node and associated edges removed.
        if Bellman_Ford(excluded_graph) == False:

            # If there's no longer a negative cycle, then add that node to the list.
            nodes_in_cycle.append(excluded_node)

    return nodes_in_cycle





# This function is called when the 'Detect' button is clicked. 

def button_click():

    # Taking the negative natural logarithm of each inserted value, and create a graph in the form of a dictionary.
    try:
        exchange_rates = {
            'USD': [('EUR', -log(float(USD_to_EUR.get()))), ('JPY', -log(float(USD_to_JPY.get()))), ('GBP', -log(float(USD_to_GBP.get())))],
            'EUR': [('USD', -log(float(EUR_to_USD.get()))), ('JPY', -log(float(EUR_to_JPY.get()))), ('GBP', -log(float(EUR_to_GBP.get())))],
            'JPY': [('USD', -log(float(JPY_to_USD.get()))), ('EUR', -log(float(JPY_to_EUR.get()))), ('GBP', -log(float(JPY_to_GBP.get())))],
            'GBP': [('USD', -log(float(GBP_to_USD.get()))), ('EUR', -log(float(GBP_to_EUR.get()))), ('JPY', -log(float(GBP_to_JPY.get())))]
            }

    # If any of the values haven't been entered, or are not of floating point type, then prompt the user accordingly.   
    except ValueError:
        result['text'] = 'Ensure all values have been entered in floating point format.'

    # Otherwise check for an arbitrage opportunity.
    else:
        if Bellman_Ford(exchange_rates) == True:

            # If an arbitrage opportunity exists, then find the relevant currencies involved.
            countries = arbitrage_path(exchange_rates)

            # Display the result to the user.
            result['text'] = f"An arbitrage opportunity exists between {', '.join(countries)}"

        # If no arbitrage opportunity exists, tell the user.
        else:
            result['text'] = 'No arbitrage opportunity detected.'





# Window

main_window = Tk()
main_window.title('Forex Arbitrage Detector')
main_window.minsize(640,300)





# Widgets

# Title label.
title = Label(main_window, text = 'Forex Arbitrage Detector', font = ('Arial', 20))

# Instruct the user how to use the program.
instructions = Label(main_window, text = "Enter the exchange rates for the countries below, then click 'Detect' to find an arbitrage opportunity.")

# A blank result label, this will be updated with the results after the user clicks 'Detect'.
result = Label(main_window)

# The detect button allows the user to commence the calculation.
detect_button = Button(main_window, text = 'Detect', command = button_click)

##################################################################################################################

# Labels for the entry boxes

from_to = Label(main_window, text = r'From\To', font = ('Arial', 12))

USD_to = Label(main_window, text = 'USD')

EUR_to = Label(main_window, text = 'EUR')

JPY_to = Label(main_window, text = 'JPY')

GBP_to = Label(main_window, text = 'GBP')


USD_from = Label(main_window, text = 'USD')

EUR_from = Label(main_window, text = 'EUR')

JPY_from = Label(main_window, text = 'JPY')

GBP_from = Label(main_window, text = 'GBP')

##################################################################################################################

##################################################################################################################

# Creating the entry box for each currency. The exchange rate of a currency to itself is just a placeholder to
# help with the grid layout, and is therefore disabled.

USD_to_USD = Entry(main_window, width = 10, bg = 'white', fg = 'black', state = 'disabled')

USD_to_EUR = Entry(main_window, width = 10, bg = 'white', fg = 'black')

USD_to_JPY = Entry(main_window, width = 10, bg = 'white', fg = 'black')

USD_to_GBP = Entry(main_window, width = 10, bg = 'white', fg = 'black')


EUR_to_USD = Entry(main_window, width = 10, bg = 'white', fg = 'black')

EUR_to_EUR = Entry(main_window, width = 10, bg = 'white', fg = 'black', state = 'disabled')

EUR_to_JPY = Entry(main_window, width = 10, bg = 'white', fg = 'black')

EUR_to_GBP = Entry(main_window, width = 10, bg = 'white', fg = 'black')


JPY_to_USD = Entry(main_window, width = 10, bg = 'white', fg = 'black')

JPY_to_EUR = Entry(main_window, width = 10, bg = 'white', fg = 'black')

JPY_to_JPY = Entry(main_window, width = 10, bg = 'white', fg = 'black', state = 'disabled')

JPY_to_GBP = Entry(main_window, width = 10, bg = 'white', fg = 'black')


GBP_to_USD = Entry(main_window, width = 10, bg = 'white', fg = 'black')

GBP_to_EUR = Entry(main_window, width = 10, bg = 'white', fg = 'black')

GBP_to_JPY = Entry(main_window, width = 10, bg = 'white', fg = 'black')

GBP_to_GBP = Entry(main_window, width = 10, bg = 'white', fg = 'black', state = 'disabled')

##################################################################################################################





# Grid locations

# Placing the title label.
title.grid(row = 0, column = 1, columnspan = 5, padx = 5, pady = 5)

# Placing the instructions label.
instructions.grid(row = 1, column = 1, columnspan = 5, padx = 15, pady = 5)

# Placing the result label.
result.grid(row = 7, column = 1, columnspan = 5, padx = 5, pady = 5)

# Placing the button.
detect_button.grid(row = 7, column = 5, padx = 5, pady = 5)

##################################################################################################################

# Placing the labels for the entry boxes.

from_to.grid(row = 2, column = 1, padx = 5, pady = 5)


USD_to.grid(row = 2, column = 2, padx = 5, pady = 5)

EUR_to.grid(row = 2, column = 3, padx = 5, pady = 5)

JPY_to.grid(row = 2, column = 4, padx = 5, pady = 5)

GBP_to.grid(row = 2, column = 5, padx = 5, pady = 5)


USD_from.grid(row = 3, column = 1, padx = 5, pady = 5)

EUR_from.grid(row = 4, column = 1, padx = 5, pady = 5)

JPY_from.grid(row = 5, column = 1, padx = 5, pady = 5)

GBP_from.grid(row = 6, column = 1, padx = 5, pady = 5)

##################################################################################################################

##################################################################################################################

# Placing the entry boxes.

USD_to_USD.grid(row = 3, column = 2, padx = 5, pady = 5)

USD_to_EUR.grid(row = 3, column = 3, padx = 5, pady = 5)

USD_to_JPY.grid(row = 3, column = 4, padx = 5, pady = 5)

USD_to_GBP.grid(row = 3, column = 5, padx = 5, pady = 5)


EUR_to_USD.grid(row = 4, column = 2, padx = 5, pady = 5)

EUR_to_EUR.grid(row = 4, column = 3, padx = 5, pady = 5)

EUR_to_JPY.grid(row = 4, column = 4, padx = 5, pady = 5)

EUR_to_GBP.grid(row = 4, column = 5, padx = 5, pady = 5)


JPY_to_USD.grid(row = 5, column = 2, padx = 5, pady = 5)

JPY_to_EUR.grid(row = 5, column = 3, padx = 5, pady = 5)

JPY_to_JPY.grid(row = 5, column = 4, padx = 5, pady = 5)

JPY_to_GBP.grid(row = 5, column = 5, padx = 5, pady = 5)


GBP_to_USD.grid(row = 6, column = 2, padx = 5, pady = 5)

GBP_to_EUR.grid(row = 6, column = 3, padx = 5, pady = 5)

GBP_to_JPY.grid(row = 6, column = 4, padx = 5, pady = 5)

GBP_to_GBP.grid(row = 6, column = 5, padx = 5, pady = 5)

##################################################################################################################





#################################### Prefilled values for demonstration purposes ##################################

# Uncomment out either one of these scenarios to prefil the entry boxes to show how the program works.


# No arbitrage opportunity present-

##USD_to_EUR.insert(0, 0.74)
##
##USD_to_JPY.insert(0, 1.32)
##
##USD_to_GBP.insert(0, 0.67)
##
##
##EUR_to_USD.insert(0, 1.3513513514)
##
##EUR_to_JPY.insert(0, 1.7837837838)
##
##EUR_to_GBP.insert(0, 0.9054054054)
##
##
##JPY_to_USD.insert(0, 0.7575757576)
##
##JPY_to_EUR.insert(0, 0.5606060606)
##
##JPY_to_GBP.insert(0, 0.5075757576)
##
##
##GBP_to_USD.insert(0, 1.4925373134)
##
##GBP_to_EUR.insert(0, 1.1044776119)
##
##GBP_to_JPY.insert(0, 1.9701492537)



# Arbitrage opportunity present USD -> EUR -> JPY -> USD, currently my code only finds the sub-arbitrage opporunity
# between EUR -> JPY.


##USD_to_EUR.insert(0, 0.9)
##
##USD_to_JPY.insert(0, 0.75)
##
##USD_to_GBP.insert(0, 110)
##
##
##EUR_to_USD.insert(0, 1.11)
##
##EUR_to_JPY.insert(0, 0.85)
##
##EUR_to_GBP.insert(0, 122)
##
##
##JPY_to_USD.insert(0, 1.33)
##
##JPY_to_EUR.insert(0, 1.2)
##
##JPY_to_GBP.insert(0, 147)
##
##
##GBP_to_USD.insert(0, 0.009)
##
##GBP_to_EUR.insert(0, 0.008)
##
##GBP_to_JPY.insert(0, 0.0068)

##################################################################################################################

main_window.mainloop()
