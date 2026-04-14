*Code adapted from Mesa Examples project*

# Multi-Group Schelling Segregation Model with Dissimilarity Index

*Code adapted from the Mesa Examples project. Extended as part of a course assignment on agent-based modeling.*

## Summary

This project extends the classic Schelling (1971) segregation model from its
original two-group formulation to a **four-group model calibrated to U.S.
racial and ethnic categories** (White, Black, Hispanic, Asian). The goal is
to examine how differences in **population composition across real U.S.
cities** shape emergent residential segregation, holding individual-level
tolerance preferences constant.

In the original Schelling model, agents of two colors live on a grid and
relocate whenever the share of same-type neighbors falls below a threshold.
Even mild in-group preferences produce striking macro-level segregation.
This modification asks: given the same preference rule, does a city's
demographic structure itself shape how severe segregation becomes, and
which groups bear the brunt of it?

## Modifications to the Base Model

1. **Four racial/ethnic groups instead of two.** Agent types 0–3 represent
   White, Black, Hispanic, and Asian residents. Group assignment at
   initialization is a weighted draw from user-specified shares.

2. **Share parameters replace `group_one_share`.** Four independent sliders
   (`white_share`, `black_share`, `hispanic_share`, `asian_share`) are
   automatically normalized to sum to 1, letting the user freely explore
   any composition.

3. **City presets based on U.S. Census 2020 data.** The GUI displays a
   reference table of demographic compositions for Chicago, New York, Los
   Angeles, Detroit, San Francisco, and a uniform benchmark. Users set
   sliders manually to match a city.

4. **Dissimilarity Index (D) as a segregation metric.** The model implements
   the Duncan & Duncan (1955) / Massey & Denton (1988) Dissimilarity Index
   by partitioning the grid into a 5×5 block structure and computing D for
   each group relative to all others. D is tracked via the `DataCollector`
   and plotted live during simulation.

5. **The agent decision rule is unchanged** (same-type neighbor share ≥
   tolerance threshold). This keeps the comparison with the original model
   clean: any differences in outcomes come from composition, not preferences.

## Installation

Dependencies are listed in `requirements.txt`:


## How to Run

To run the model interactively once you have a complete agents file, run the following code in this directory:

```
    $ solara run app.py
```

## Files

* ``agents.py``: Contains the agent class, currently incomplete
* ``model.py``: Contains the model class
* ``app.py``: Defines classes for visualizing the model in the browser via Solara, and instantiates a visualization server.