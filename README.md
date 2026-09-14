# Computing Helpers

**Computing Helpers** is a collection of small computational tools for common problems in mechanical engineering courses. The scripts are intended to make repetitive calculations faster whitout hindering learning or understanding of the subjects. 

Most programs are interactive command-line applications. Run one from the repository folder with:

```text
python <script>.py
```

The `.tns` files are companion files for use on TI-Nspire calculators or software. The Python scripts are the most convenient versions to run on a regular computer.

## Python Scripts

1. **[dmi.py](dmi.py) - Direct stiffness method for plane frames**

   Builds a small structural-analysis model from nodes and members. It calculates element stiffness matrices, transforms them from local to global coordinates, assembles the global stiffness matrix, and creates global load vectors. The interactive menus also support custom degree-of-freedom mapping, inspection of an individual member matrix, and fixed-end reactions for distributed or point loads. The structure plotting option is not working. 

2. **[engrenagens.py](engrenagens.py) - Cylindrical gear geometry and measurements**

   Calculates geometric properties of a pair of spur or helical gears, including pitch and base dimensions, operating geometry, virtual tooth numbers, tooth thicknesses, tangential measurement dimensions, and cylindrical measurement gauges. It can estimate profile-shift corrections using direct/virtual-tooth and ISO methods, evaluate interference, and report whether the selected face width is adequate for the calculated minimum width.

3. **[Fij.py](Fij.py) - Heat-transfer view factors**

   Provides formulas for radiation view factors between standard geometries. It covers idealized infinite-depth cases such as parallel, inclined, perpendicular, and cylindrical surfaces, as well as finite three-dimensional cases such as aligned parallel planes, perpendicular planes, and coaxial disks. The interactive menus validate dimensions and return the corresponding $F_{ij}$ value.

4. **[interpol_OM.py](interpol_OM.py) - Tabulated machine-element calculations**

   Interpolates dimensionless tables used in machine-element and tribology problems. Its modules cover radial journal bearings and the Cheng theory for rolling bearings, cam-follower contacts, and gears. It supports both direct calculations of film thickness and $\Lambda$ values and inverse calculations for lubricant parameters, while retaining previously entered values during an interactive session.

5. **[TC_interpol.py](TC_interpol.py) - Thermophysical-property interpolation**

   Interpolates temperature-dependent properties for atmospheric air, liquid water, and saturated water vapor. Depending on the selected temperature and property, it returns values such as density, specific heat, thermal conductivity, viscosity, diffusivity, Prandtl number, saturation pressure, latent heat, and surface tension.

6. **[tribologia.py](tribologia.py) - Tribology calculator**

   Combines two tribology modules. The radial-journal-bearing module uses dimensionless bearing tables and a solver to infer quantities such as eccentricity, Sommerfeld number, friction, load capacity, power loss, lubricant flow, and temperature rise. The Cheng-theory module estimates lubricant-film thickness and specific film thickness for rolling bearings, cam-follower contacts, and several gear arrangements, including direct and inverse problem modes.

7. **[poker.py](poker.py) - Poker betting and chip tracker**

   Runs a simple command-line multiplayer poker helper. It records players, starting chips, and blinds; manages pre-flop, flop, turn, and river betting phases; accepts folds, checks, calls, and raises; tracks the pot and each player’s chips; distributes showdown winnings, handles ties, eliminates players with no chips, and increases the blind during the game. The program does not evaluate cards or determine a winner automatically, so the winner is entered manually after a showdown.

## Notes

- The programs use metric units unless an input prompt specifies otherwise.
- The calculations are intended as study and engineering-assistance tools. Check assumptions, units, interpolation ranges, and source tables.
