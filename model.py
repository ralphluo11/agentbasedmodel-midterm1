from mesa import Model
from mesa.space import SingleGrid
from agents import SchellingAgent
from mesa.datacollection import DataCollector

class SchellingModel(Model):
    ## CHANGE 1: Add parameters for racial group shares and Dissimilarity Index tracking
    def __init__(self, width=30, height=30, density=0.7, 
             desired_share_alike=0.5,
             white_share=0.25, black_share=0.25, 
             hispanic_share=0.25, asian_share=0.25,
             radius=1, seed=None):
        ## Inherit seed trait from parent class and ensure seed is integer
        if seed is not None:
            seed = int(seed)
        super().__init__(rng=seed)
        ## Define parameter values for model instance
        self.width = width
        self.height = height
        self.density = density
        self.desired_share_alike = desired_share_alike
        # CHANGE 2: Store racial group shares and normalize to sum to 1
        shares = [white_share, black_share, hispanic_share, asian_share]
        total = sum(shares)
        if total > 0:
              self.group_shares = [s / total for s in shares]
        else:
              self.group_shares = [0.25, 0.25, 0.25, 0.25] 
        self.radius = radius
        ## Create grid
        self.grid = SingleGrid(width, height, torus = True)
        ## Instantiate global happiness tracker
        self.happy = 0
        ## Place agents randomly around the grid, randomly assigning them to agent types.
        for cont, pos in self.grid.coord_iter():
            if self.random.random() < self.density:
                # CHANGE 3: Randomly assign agent type based on specified group shares
                chosen_type = self.random.choices( population=[0,1,2,3], weights=self.group_shares, k=1)[0]
                self.grid.place_agent(SchellingAgent(self, chosen_type), pos)

        ## Initialize datacollector
        self.datacollector = DataCollector(
            model_reporters = {
                "happy" : "happy",
                "share_happy" : lambda m : (m.happy / len(m.agents)) * 100
                if len(m.agents) > 0
                else 0,
                # CHANGE 4: Add Dissimilarity Index reporters for each racial group
                "D_white"   : lambda m: m.dissimilarity(0),
                "D_black"   : lambda m: m.dissimilarity(1),
                "D_hispanic": lambda m: m.dissimilarity(2),
                "D_asian"   : lambda m: m.dissimilarity(3),
            }
        )


    ## Define a step: reset global happiness tracker, agents move in random order, collect data
    def step(self):
        self.happy = 0
        self.agents.shuffle_do("move")
        self.datacollector.collect(self)
        ## Modification 99 percent happy condition: model runs until at least 99% of agents are happy
        self.running = (self.happy / len(self.agents)) < 0.99
    
    ## ============================================================
    ## MODIFICATION: Dissimilarity Index calculation
    ## ============================================================
    ## The Dissimilarity Index (Duncan & Duncan 1955; Massey & Denton 1988)
    ## measures residential segregation. For one group vs. all others:
    ##   D = 0.5 * sum over blocks of |a_i/A - b_i/B|
    ## where a_i = focal group count in block i, A = total focal group;
    ## b_i = other groups' count in block i, B = total other groups.
    ## D ranges from 0 (perfect integration) to 1 (complete segregation).
    
    def get_block_id(self, pos):
        """Map a (x, y) cell to a coarser block ID for D-index calculation.
        We divide the grid into a 5x5 grid of blocks (25 blocks total).
        Each block is roughly width/5 by height/5 cells. With default
        30x30 grid and 0.7 density, each block holds ~18 agents on average,
        which is large enough to give meaningful proportions."""
        n = 5  # number of blocks per side
        block_w = self.width // n
        block_h = self.height // n
        ## Use min() to handle non-divisible grid sizes:
        ## any leftover cells get folded into the last block.
        block_x = min(pos[0] // block_w, n - 1)
        block_y = min(pos[1] // block_h, n - 1)
        return (block_x, block_y)
    
    def dissimilarity(self, group_id):
        """Compute the Dissimilarity Index for one racial group vs. all others.
        Returns a value in [0, 1]: 0 = perfectly mixed, 1 = fully segregated."""
        ## Build a dict: block_id -> [count of focal group, count of others]
        block_counts = {}
        for agent in self.agents:
            block = self.get_block_id(agent.pos)
            ## Initialize this block's counter the first time we see it
            if block not in block_counts:
                block_counts[block] = [0, 0]
            ## Increment focal group count or "other" count
            if agent.type == group_id:
                block_counts[block][0] += 1
            else:
                block_counts[block][1] += 1
        
        ## Compute citywide totals: A = total focal group, B = total others
        A = sum(counts[0] for counts in block_counts.values())
        B = sum(counts[1] for counts in block_counts.values())
        
        ## Edge case: if either group has zero people, D is undefined.
        ## Return 0 (no segregation possible if a group doesn't exist).
        if A == 0 or B == 0:
            return 0
        
        ## Apply the D formula: sum the absolute differences across blocks
        D = 0.5 * sum(
            abs(counts[0] / A - counts[1] / B)
            for counts in block_counts.values()
        )
        return D
