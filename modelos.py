class paquete(object):

    def __init__(self, type_alg, mensaje, ori, go):
        self.algorithm = type_alg
        self.msg = mensaje
        self.origin = ori
        self.goal = go
        self.path = None
        self.maxJumps = None
        self.pastNode = None
        self.jumps = None
        self.distance = 0
        self.nextNode = None
        self.sendingNode = None

    def get_algorithm(self):
        return self.algorithm

    def get_msg(self):
        return self.msg

    def get_orgigin(self):
        return self.origin

    def get_goal(self):
        return self.goal

    def get_path(self):
        return self.path

    def set_path(self,the_path):
        self.path = the_path

    def get_maxJumps(self):
        return self.maxJumps

    def set_maxJumps(self,total_jumps):
        self.maxJumps = total_jumps

    def get_pastNode(self):
        return self.pastNode

    def set_pastNode(self,pNode):
        self.pastNode = pNode

    def get_jumps(self):
        return self.jumps

    def set_jumps(self,nJumps):
        self.jumps = nJumps

    def get_distance(self):
        return self.distance

    def set_distance(self,dist):
        self.distance = dist

    def get_nextNode(self):
        return self.nextNode

    def set_nextNode(self,nNode):
        self.nextNode = nNode

    def get_sendingNode(self):
        return self.sendingNode

    def set_sendingNode(self,sNode):
        self.sendingNode = sNode
