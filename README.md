# Hydrogen Direct-Fired Steam Cycle
## Thermodynamic Modelling and Performance Comparison

A Python-based conceptual thermodynamic study comparing a **hydrogen direct-fired steam cycle (DFSC)** with a **conventional Rankine steam cycle** under comparable turbine inlet conditions.

The project was developed as an engineering modelling exercise focused on:

- thermodynamic cycle modelling
- hydrogen energy systems
- heat and mass balances
- turbine and pump performance
- oxygen-compression parasitic losses
- sensitivity analysis
- quantitative comparison of competing power-generation concepts
- reproducible Python-based engineering analysis

> **Model scope:** conceptual thermodynamic screening model. The results are not intended to represent a detailed plant design or commercial performance prediction.

---

## 1. Engineering question

The study investigates:

> **How does a conceptual hydrogen direct-fired steam cycle compare with a conventional Rankine cycle when both are evaluated under comparable turbine inlet conditions?**

The analysis focuses on net work and efficiency while explicitly accounting for the oxygen-compression penalty associated with the direct-fired concept.

---

## 2. System concept

The direct-fired reaction is represented by:

\[
2H_2 + O_2 \rightarrow 2H_2O
\]

For a basis of 1 kg hydrogen:

\[
m_{O_2}=8\,m_{H_2}
\]

\[
m_{H_2O}=9\,m_{H_2}
\]

The model represents a recycle-dominated steam loop. The total circulating working-fluid mass is determined from the cycle heat balance, while the stoichiometric combustion-water production is tracked separately.

### Direct-fired steam cycle

1. Condensed water is pumped to the high-pressure level.
2. Hydrogen and oxygen are supplied to the direct-fired process.
3. The released hydrogen energy provides heat to the circulating steam/water working fluid.
4. High-temperature steam expands through the turbine.
5. The exhaust is condensed and recycled.
6. Oxygen-compression work is treated as a parasitic system load.

### Conventional Rankine reference

The reference cycle uses the same turbine inlet pressure and temperature and the same turbine/pump efficiencies, while representing heat addition through an external boiler with a configurable boiler efficiency.

---

## 3. Thermodynamic methodology

Water/steam properties are calculated using the `iapws` Python package based on IAPWS formulations, with **IAPWS-IF97** used for industrial steam-property calculations.

### Turbine

The isentropic outlet is obtained from:

\[
s_{4s}=s_3
\]

The actual turbine outlet is:

\[
h_4=h_3-\eta_t(h_3-h_{4s})
\]

Turbine work:

\[
W_t=m_s(h_3-h_4)
\]

### Pump

The ideal pump outlet is approximated using:

\[
h_{2s}=h_1+v_1(P_2-P_1)
\]

and the actual pump outlet is:

\[
h_2=h_1+\frac{h_{2s}-h_1}{\eta_p}
\]

### Direct-fired working-fluid flow

\[
m_s=
\frac{m_{H_2}LHV_{H_2}\eta_{comb}}
{h_3-h_2}
\]

### Direct-fired gross and net work

\[
W_{gross}=W_t-W_p
\]

\[
W_{net,DFSC}=W_{gross}-W_{O_2,comp}
\]

### Conventional Rankine

\[
m_s=
\frac{m_{H_2}LHV_{H_2}\eta_{boiler}}
{h_3-h_2}
\]

\[
W_{net,Rankine}=W_t-W_p
\]

### Net efficiency

\[
\eta_{net}=
\frac{W_{net}}
{m_{H_2}LHV_{H_2}}
\]

---

## 4. Baseline assumptions

| Parameter | Baseline |
|---|---:|
| Hydrogen LHV | 120 MJ/kg |
| Hydrogen basis | 1 kg |
| Turbine inlet pressure | 100 bar |
| Turbine inlet temperature | 800 °C |
| Condenser pressure | 0.1 bar |
| Turbine isentropic efficiency | 85% |
| Pump efficiency | 85% |
| O₂ compressor efficiency | 75% |
| Combustion efficiency | 99% |
| Conventional boiler efficiency | 90% |
| O₂/H₂ mass ratio | 8 kg/kg |
| H₂O/H₂ stoichiometric ratio | 9 kg/kg |

---

## 5. Baseline results

The validated baseline model produces:

| Metric | Hydrogen DFSC | Conventional Rankine |
|---|---:|---:|
| Working-fluid mass | 30.375 kg/kg H₂ | 27.614 kg/kg H₂ |
| Turbine work | 45.621 MJ/kg H₂ | 41.474 MJ/kg H₂ |
| Pump work | 0.361 MJ/kg H₂ | 0.328 MJ/kg H₂ |
| Gross cycle work | 45.260 MJ/kg H₂ | 41.146 MJ/kg H₂ |
| O₂ compression work | 7.828 MJ/kg H₂ | 0 |
| Net work | 37.432 MJ/kg H₂ | 41.146 MJ/kg H₂ |
| Net efficiency | **31.19%** | **34.29%** |

### Baseline interpretation

The direct-fired configuration produces more gross turbine-cycle work:

\[
45.260 > 41.146\ {\rm MJ/kg_{H_2}}
\]

but the modeled oxygen-compression penalty is:

\[
7.828\ {\rm MJ/kg_{H_2}}
\]

Consequently, the DFSC net work is:

\[
37.432\ {\rm MJ/kg_{H_2}}
\]

compared with:

\[
41.146\ {\rm MJ/kg_{H_2}}
\]

for the conventional reference.

Under the baseline assumptions, the modeled net-efficiency difference is:

\[
31.19-34.29
=
\boxed{-3.09\ {\rm percentage\ points}}
\]

This is a **model-specific result**, not a general statement about all hydrogen direct-fired steam-cycle configurations.

---

## 6. Model validation

The project includes explicit first-law and reaction-balance checks.

### Steam-cycle energy balance

For the steam-cycle boundary:

\[
Q_{in}=W_{gross}+Q_{out}
\]

The baseline DFSC residual is approximately:

\[
1.4\times10^{-14}\ {\rm MJ/kg_{H_2}}
\]

which is numerical round-off.

### Complete DFSC system boundary

Because oxygen-compression work is deducted when calculating net work, the complete system balance is evaluated as:

\[
Q_{in}
=
W_{net}
+
W_{O_2,comp}
+
Q_{out}
\]

The baseline residual is approximately:

\[
1.4\times10^{-14}\ {\rm MJ/kg_{H_2}}
\]

with a relative error of approximately:

\[
1.2\times10^{-14}\%
\]

### Stoichiometric mass balance

For:

\[
2H_2+O_2\rightarrow2H_2O
\]

the 1 kg H₂ basis gives:

\[
m_{H_2}=1\ {\rm kg}
\]

\[
m_{O_2}=8\ {\rm kg}
\]

\[
m_{H_2O}=9\ {\rm kg}
\]

and the modeled reaction mass-balance residual is:

\[
\boxed{0.0\ {\rm kg}}
\]

These checks validate the numerical consistency of the implemented cycle model; they do not constitute validation against experimental plant data.

---

## 7. Temperature and pressure sensitivity

The model was evaluated over:

- turbine inlet temperature: **600–1000 °C**
- turbine inlet pressure: **30–150 bar**

with 54 operating points.

The efficiency difference was defined as:

\[
\Delta\eta=
\eta_{DFSC}-\eta_{Rankine}
\]

### Observed trend

Across the modeled range, DFSC net efficiency remained below the conventional Rankine reference.

The gap was smallest at:

\[
1000^\circ C,\ 30\ {\rm bar}
\]

where:

\[
\Delta\eta\approx-0.56\ {\rm percentage\ points}
\]

The largest modeled gap occurred at:

\[
600^\circ C,\ 150\ {\rm bar}
\]

where:

\[
\Delta\eta\approx-4.33\ {\rm percentage\ points}
\]

At 100 bar, increasing turbine inlet temperature from 600 °C to 1000 °C increased modeled DFSC net efficiency from approximately 28.51% to 33.85%.

The sensitivity results therefore indicate that, within this simplified model:

- increasing turbine inlet temperature improves both cycles;
- the DFSC/Rankine efficiency gap becomes smaller at higher turbine inlet temperature;
- increasing pressure does not produce the same relative benefit for DFSC as for the conventional reference over the investigated range.

These trends should be interpreted within the model assumptions and not extrapolated outside the investigated operating range.

---

## 8. Oxygen-compression sensitivity

The model also evaluates the influence of O₂ compressor isentropic efficiency.

| O₂ compressor efficiency | O₂ compression work | DFSC net efficiency |
|---:|---:|---:|
| 50% | 11.742 MJ/kg H₂ | 27.93% |
| 60% | 9.785 MJ/kg H₂ | 29.56% |
| 70% | 8.387 MJ/kg H₂ | 30.73% |
| 75% | 7.828 MJ/kg H₂ | 31.19% |
| 80% | 7.339 MJ/kg H₂ | 31.60% |
| 85% | 6.907 MJ/kg H₂ | 31.96% |
| 90% | 6.524 MJ/kg H₂ | 32.28% |
| 95% | 6.180 MJ/kg H₂ | 32.57% |

At the baseline 75% compressor efficiency:

\[
\frac{W_{O_2}}{W_{gross}}
\approx17.3\%
\]

Thus, oxygen compression is a significant modeled parasitic load.

The sensitivity also shows diminishing incremental efficiency gains as compressor efficiency becomes higher.

---

## 9. Visualizations

The project generates:

- baseline cycle-state data
- efficiency versus turbine inlet temperature
- efficiency versus turbine inlet pressure
- DFSC-versus-Rankine efficiency-gap heatmap
- baseline T-s diagram
- O₂ compression work versus compressor efficiency
- DFSC net efficiency versus O₂ compressor efficiency

These figures are intended to make the thermodynamic trends and system-level trade-offs transparent.

---

## 10. Limitations

This is a **first-order conceptual model**. It does not represent a detailed industrial plant.

The model currently does not include:

- detailed H₂/O₂ combustion kinetics
- flame-temperature calculation
- detailed combustor geometry
- radiation and detailed heat-transfer losses
- oxygen production / air-separation energy
- hydrogen compression
- detailed pressure losses
- moisture separation
- detailed water inventory and purge control
- material-temperature limits
- NOx formation
- multi-stage turbine expansion
- reheat
- extraction/cooling systems
- detailed condenser design
- plant-level balance of plant
- experimental validation

The oxygen-compression model is a simplified ideal-gas compressor estimate. Consequently, the results should be presented as **conceptual screening results**.

---

## 11. Recommended future work

Potential extensions include:

1. Add multi-stage turbine expansion and reheat.
2. Include oxygen-production / air-separation energy.
3. Include hydrogen compression.
4. Add detailed water-management and purge calculations.
5. Compare concepts at equal net electrical output.
6. Add exergy analysis.
7. Add uncertainty analysis.
8. Compare assumptions against published direct-fired hydrogen/oxygen steam-cycle studies.
9. Add pressure-loss and component-level efficiency models.
10. Investigate optimized operating windows after the expanded system boundary is implemented.

---

## 12. Project structure

```text
hydrogen_direct_fired_steam_cycle/
├── README.md
├── RESEARCH_NOTES.md
├── requirements.txt
├── .gitignore
├── run_simulation.py
│
├── src/
│   ├── __init__.py
│   ├── parameters.py
│   ├── thermodynamics.py
│   └── cycle_models.py
│
├── tests/
│   └── test_cycle.py
│
└── results/
    ├── baseline_results.csv
    ├── cycle_states.csv
    ├── energy_balance.csv
    ├── mass_balance.csv
    ├── sensitivity_results.csv
    ├── oxygen_compression_sensitivity.csv
    ├── efficiency_vs_temperature.png
    ├── efficiency_vs_pressure.png
    ├── efficiency_gap_heatmap.png
    ├── efficiency_vs_o2_compressor_efficiency.png
    ├── o2_compression_work_vs_efficiency.png
    └── ts_diagram.png
```

---



## 14. References

- IAPWS, **IAPWS-IF97: Revised Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam**  
  https://www.iapws.org/relguide/IF97-Rev.html

- IAPWS, **Technical Guidance Documents / New Formulations**  
  https://iapws.org/technical-guidance/newform

- U.S. Department of Energy, **Hydrogen Storage**  
  https://www.energy.gov/cmei/fuels/hydrogen-storage

- NIST, **Thermochemical Reference / Hydrogen-Oxygen-Water Species Data**  
  https://www.nist.gov/

---


## Disclaimer

This repository demonstrates engineering modelling methodology and numerical analysis. Its results depend on the stated assumptions and simplified component models and should not be interpreted as validated industrial plant performance.
