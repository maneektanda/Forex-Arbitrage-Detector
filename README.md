                            Background Information and Inspiration

The Bellman-Ford algorithm can be used to find the shortest path from a starting node to all other nodes within
a weighted, directed graph. However, where a graph contains a negative edge cycle, the result is meaningless.
This algorithm can be modified to test for, and identify negative edge cycles. In a financial context such as
foreign exchange rates, negative edge cycles can be used to identify arbitrage oppotunites.

To detect an arbitrage opportunity amongst foreign exchange rates, the product of the rates must be greater than 1. 
The Bellman-Ford algorithm is not directly applicable here, as its logic is based off of the summation of edge
weights. A conversion of some sort needs to happen, so that the product relationship can be expressed as a sum
relationship. The solution for this problem is not my own and was learned from online materials.

Observe the following-

Let A and B be exchange rates, arbitrage exists when-
 
A * B > 1

Taking the natural logarithm of both sides gives-

ln(A * B) > ln(1)

ln(A) + ln(B) > 0

So if we take the natural log of the exchange rates, an arbitrage opportunity exists if the summation is greater
than 0. If we were to apply Bellman-Ford to the natural log of the exchange rates, the negative edge cycles found
would just represent transactions where money is lost. Therefore, taking the negative natural log of the exchange
rates will successfully detect an arbitrage oppotunity.



                         Custom algorithm for identifying arbitrage

While a method already exists to locate the path of a negative edge cycle found when using the Bellman-Ford
algorithm, I wanted to test a theory of my own. I have implemented this theory in a function called 'arbitrage_path'.

                                        The Theory

Suppose a negative edge cycle is detected in a graph. If one of the nodes in that cycle, as well as all edges
connected to that node, is excluded, then the cycle will no longer be present. The 'arbitrage_path' function
iteratively excludes a node and all of its associated edges from a graph to create a new 'excluded_graph'. It
then tests again for the negative edge cycle in the 'excluded_graph'. If the cycle is no longer detected, then
that node must have been in the negative edge cycle. Iteratively excluding all of the nodes allows for a list of
nodes to be made that form the negative edge cycle. This list represents the exchange rates that create the
arbitrage opportunity.

                                  Recognising Limitations

Before completing this function, I realised some limitations.

Firstly, this logic only works when only one cycle is present. Two individual negative edge cycles that do not
affect each other will clearly not be detected by this logic.

Secondly, the time complexity of this solution is very slow, as you have to run the Bellman_Ford algorithm for
however many nodes are in the graph.

Thirdly, I have made the assumption that finding the exact path in a forex setting is not necessarily that
important, because I don't expect there to be too many oppotunites of a long enough length, that the path can't
be found intuitively once the nodes have been identified.

Despite becoming aware of these limitations, I still thought this would be a great learning experience and
foundational project in the early stages of my career. I have been able to turn an intuitive thought, into
actual implemented code.
