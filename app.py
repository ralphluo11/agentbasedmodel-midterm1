import solara
from model import SchellingModel
from mesa.visualization import (  
    SolaraViz,
    make_space_component,
    make_plot_component,
)
from mesa.visualization.components import AgentPortrayalStyle

## Define agent portrayal: color, shape, and size
def agent_portrayal(agent):
    # CHANGE 5: Update colors to represent 4 racial groups instead of 2
    return AgentPortrayalStyle( color = ("blue" if agent.type == 0 
                    else "orange" if agent.type == 1 
                    else "green" if agent.type == 2 
                    else "red"))

## Enumerate variable parameters in model: seed, grid dimensions, population density, agent preferences, vision, and relative size of groups.
# CHANGE 6: Add sliders for racial group shares (white_share, black_share, hispanic_share, asian_share)
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "width": {
        "type": "SliderInt",
        "value": 30,
        "label": "Width",
        "min": 5,
        "max": 100,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 30,
        "label": "Height",
        "min": 5,
        "max": 100,
        "step": 1,
    },
    "density": {
        "type": "SliderFloat",
        "value": 0.7,
        "label": "Population Density",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
    "desired_share_alike": {
        "type": "SliderFloat",
        "value": 0.5,
        "label": "Desired Share Alike",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
    "white_share": {
        "type": "SliderFloat",
        "value": 0.25,
        "label": "Share White",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
    "black_share": {
        "type": "SliderFloat",
        "value": 0.25,
        "label": "Share Black",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
    "hispanic_share": {
        "type": "SliderFloat",
        "value": 0.25,
        "label": "Share Hispanic",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
    "asian_share": {
        "type": "SliderFloat",
        "value": 0.25,
        "label": "Share Asian",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },

    "radius": {
        "type": "SliderInt",
        "value": 1,
        "label": "Vision Radius",
        "min": 1,
        "max": 5,
        "step": 1,
    },
}

# CHANGE 7: Add components to explain legend, presets, and normalization note
@solara.component
def Legend(model):
    solara.Markdown("""
    ### Legend
    - 🟦 **Blue** = White
    - 🟧 **Orange** = Black
    - 🟩 **Green** = Hispanic
    - 🟥 **Red** = Asian
    """)

@solara.component
def CityPresets(model):
    solara.Markdown("""
    ### City Presets (set sliders manually)
    
    | City | White | Black | Hispanic | Asian |
    |------|-------|-------|----------|-------|
    | Chicago | 0.34 | 0.30 | 0.29 | 0.07 |
    | New York | 0.33 | 0.21 | 0.30 | 0.16 |
    | Los Angeles | 0.29 | 0.08 | 0.50 | 0.13 |
    | Detroit | 0.11 | 0.78 | 0.08 | 0.03 |
    | San Francisco | 0.41 | 0.05 | 0.15 | 0.39 |
    | Uniform | 0.25 | 0.25 | 0.25 | 0.25 |
    
    *Source: U.S. Census 2020, normalized to White/Black/Hispanic/Asian only.*
    """)
@solara.component
def NormalizationNote(model):
    ## Show that shares are auto-normalized to 1
    solara.Markdown(f"""
    ### Note on shares
    
    The four share sliders do **not** need to sum to 1.  
    The model automatically normalizes them to proportions.
    
    **Current normalized shares:**
    - White: {model.group_shares[0]:.1%}
    - Black: {model.group_shares[1]:.1%}
    - Hispanic: {model.group_shares[2]:.1%}
    - Asian: {model.group_shares[3]:.1%}
    """)
## Instantiate model
schelling_model = SchellingModel()

## Define happiness over time plot
HappyPlot = make_plot_component({"share_happy": "tab:green"})

## CHANGE 8: plot Dissimilarity Index over time for all 4 groups
DPlot = make_plot_component({
    "D_white": "tab:blue",
    "D_black": "tab:orange",
    "D_hispanic": "tab:green",
    "D_asian": "tab:red",
})

## Define space component
SpaceGraph = make_space_component(agent_portrayal, draw_grid=False)

## Instantiate page inclusing all components
page = SolaraViz(
    schelling_model,
    # change 9: add Dissimilarity Index plot and other explanatory components to page
    components=[SpaceGraph, HappyPlot, NormalizationNote, Legend, CityPresets, DPlot],
    model_params=model_params,
    name="Schelling Segregation Model",
)
## Return page
page
    
