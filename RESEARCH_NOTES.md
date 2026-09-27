
# Research notes

## Reference data

- IAPWS-IF97 is the industrial formulation for thermodynamic properties of water and steam and is particularly relevant to steam-power calculations.
- U.S. Department of Energy references use 120 MJ/kg as the lower heating value of hydrogen.
- NIST thermochemical data provide hydrogen/oxygen/water reference data.

## Scope

The current implementation is deliberately a first-order cycle-screening model. It demonstrates the modelling workflow that would precede a more detailed engineering model.

The model should not be presented as a validated Siemens Energy or plant-design calculation.

## Recommended next technical step

Replace the simplified oxygen-compression model with a more detailed oxygen-supply model and introduce:
- compressor staging
- intercooling
- pressure losses
- multi-stage turbine expansion
- reheat
- condenser-pressure sensitivity
- water purge/makeup balance
- exergy analysis
- uncertainty analysis
