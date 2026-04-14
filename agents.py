from mesa import Agent

class SchellingAgent(Agent):
    ## Initiate agent instance, inherit model trait from parent class
    def __init__(self, model, agent_type):
        super().__init__(model)
        ## Set agent type
        self.type = agent_type
    ## Define basic decision rule
    def move(self):
        ## Get list of neighbors within range of sight
        neighbors = self.model.grid.get_neighbors(self.pos, moore = True, include_center = False, radius = self.model.radius)
        ## Count neighbors of same type as self
        similar_neighbors = sum(1 for n in neighbors if n.type == self.type)
        ## If an agent has any neighbors (to avoid division by zero), calculate share of neighbors of same type
        if len(neighbors) > 0:
            share_happy = similar_neighbors / len(neighbors)
        else:
            share_happy = 0
        ## If unhappy with neighbors, move to random empty slot. Otherwise add one to model count of happy agents.
        if share_happy < self.model.desired_share_alike:
            self.model.grid.move_to_empty(self)
        else: 
            self.model.happy += 1
