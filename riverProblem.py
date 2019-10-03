"""
Solution stub for the River Problem.

Fill in the implementation of the `River_problem` class to match the
representation that you specified in problem XYZ.
"""
from searchProblem import Search_problem, Arc

class River_problem(Search_problem):
    def start_node(self):
        """returns start node"""
        
        return ('0000')
    
    def is_goal(self,node):
        """is True if node is a goal"""
        return (node == '1111')
        #return len(node) % 2 == 0 # dummy goal, state has two items in it

    def neighbors(self,node):
        """returns a list of the arcs for the neighbors of node"""
        chicken = node[0]
        fox = node[1]
        grain = node[2]
        raft = node[3]
        neighbours = []
        if chicken == raft:
            if chicken == '0':
                if self.isValidNode('1'+ fox + grain + '1'):
                    neighbours.append(Arc(node, '1' + fox + grain + '1', 1))
            else:
                if self.isValidNode('0' + fox + grain + '0'):
                    neighbours.append(Arc(node, '0' + fox + grain + '0', 1))
        if fox == raft:
            if fox == '0':
                if self.isValidNode(chicken + '1' + grain + '1'):
                    neighbours.append(Arc(node, chicken + '1' + grain + '1',1))
            else:
                if self.isValidNode(chicken + '0' + grain + '0'):
                    neighbours.append(Arc(node, chicken + '0' + grain + '0',1))
        if grain == raft:
            if grain == '0':
                if self.isValidNode(chicken + fox + '1' + '1'):
                    neighbours.append(Arc(node, chicken + fox + '1' + '1', 1))
            else:
                if self.isValidNode(chicken + fox + '0' + '0'):
                    neighbours.append(Arc(node, chicken + fox + '0' + '0', 1))
        if raft == '0':
            if self.isValidNode(chicken + fox + grain + '1'):
                neighbours.append(Arc(node, chicken + fox + grain + '1', 1))
        else:
            if self.isValidNode(chicken + fox + grain + '0'):
                neighbours.append(Arc(node, chicken + fox + grain + '0', 1))

        return neighbours

    def heuristic(self,n):
        """Gives the heuristic value of node n."""
        n = n[0:3]
        return n.count('0')

    def isValidNode(self,node):
        """Returns whether a node is valid or not"""
        chicken = node[0]
        fox = node[1]
        grain = node[2]
        raft = node[3]
        if ((chicken == fox) and (chicken !=raft)):
        #fox eats chicken
            return False
        if ((chicken == grain) and (chicken !=raft)):
        #chicken eats grain
            return False
        return True
    
    

