from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.parameters import CycleParameters
from src.cycle_models import direct_fired_cycle, conventional_rankine_cycle
from src.thermodynamics import pump_state, turbine_states


RESULTS = Path("results")
RESULTS.mkdir(exist_ok=True)


def _state_rows(params: CycleParameters, cycle_name: str):
    state_1, state_2, h2s, _ = pump_state(
        params.p_low_mpa,
        params.p_high_mpa,
        params.pump_efficiency,
    )
    state_3, state_4s, state_4 = turbine_states(
        params.p_high_mpa,
        params.p_low_mpa,
        params.turbine_inlet_temperature_k,
        params.turbine_isentropic_efficiency,
    )

    states = [
        ("1", "Condenser outlet / pump inlet", state_1, "actual"),
        ("2s", "Ideal pump outlet", None, "isentropic"),
        ("2", "Actual pump outlet", state_2, "actual"),
        ("3", "Turbine inlet", state_3, "actual"),
        ("4s", "Ideal turbine outlet", state_4s, "isentropic"),
        ("4", "Actual turbine outlet", state_4, "actual"),
    ]

    rows = []
    for state_id, description, state, state_type in states:
        if state_id == "2s":
            rows.append(
                {
                    "cycle": cycle_name,
                    "state": state_id,
                    "description": description,
                    "state_type": state_type,
                    "pressure_mpa": params.p_high_mpa,
                    "pressure_bar": params.p_high_mpa * 10.0,
                    "temperature_c": np.nan,
                    "enthalpy_kj_per_kg": h2s,
                    "entropy_kj_per_kgk": np.nan,
                    "specific_volume_m3_per_kg": np.nan,
                    "quality": np.nan,
                }
            )
            continue

        rows.append(
            {
                "cycle": cycle_name,
                "state": state_id,
                "description": description,
                "state_type": state_type,
                "pressure_mpa": state.P,
                "pressure_bar": state.P * 10.0,
                "temperature_c": state.T - 273.15,
                "enthalpy_kj_per_kg": state.h,
                "entropy_kj_per_kgk": state.s,
                "specific_volume_m3_per_kg": state.v,
                "quality": getattr(state, "x", np.nan),
            }
        )

    return rows


def _balance_rows(params: CycleParameters, cycle_name: str, result: dict):
    heat_input = result["heat_input_mj"]
    oxygen = result["oxygen_compression_work_mj"]
    net = result["net_work_mj_per_kg_h2"]
    condenser = result["condenser_heat_rejection_mj"]

    # Overall first-law check for the model boundary:
    # chemical heat + external O2-compression work = net work + condenser rejection.
    total_input = heat_input + oxygen
    total_output = net + condenser
    energy_residual = total_input - total_output

    return {
        "cycle": cycle_name,
        "heat_input_mj_per_kg_h2": heat_input,
        "oxygen_compression_work_mj_per_kg_h2": oxygen,
        "net_work_mj_per_kg_h2": net,
        "condenser_heat_rejection_mj_per_kg_h2": condenser,
        "total_energy_input_mj_per_kg_h2": total_input,
        "total_energy_output_mj_per_kg_h2": total_output,
        "energy_balance_residual_mj_per_kg_h2": energy_residual,
        "energy_balance_relative_error_percent": (
            energy_residual / total_input * 100.0 if total_input else np.nan
        ),
    }


def _mass_balance_rows(params: CycleParameters, cycle_name: str):
    h2_in = params.h2_mass_kg
    o2_in = params.oxygen_to_h2_mass_ratio * h2_in
    h2o_out = params.water_to_h2_mass_ratio * h2_in

    return {
        "cycle": cycle_name,
        "h2_in_kg": h2_in,
        "o2_in_kg": o2_in,
        "combustion_water_out_kg": h2o_out,
        "reactant_mass_kg": h2_in + o2_in,
        "product_mass_kg": h2o_out,
        "mass_balance_residual_kg": h2_in + o2_in - h2o_out,
    }


def baseline():
    params = CycleParameters()

    dfsc = direct_fired_cycle(params)
    rankine = conventional_rankine_cycle(params)

    result = pd.DataFrame([dfsc, rankine])
    result.to_csv(RESULTS / "baseline_results.csv", index=False)

    state_rows = _state_rows(params, "Hydrogen Direct-Fired Steam Cycle")
    state_rows += _state_rows(params, "Conventional Rankine Steam Cycle")
    pd.DataFrame(state_rows).to_csv(RESULTS / "cycle_states.csv", index=False)

    balance_rows = [
        _balance_rows(params, dfsc["cycle"], dfsc),
        _balance_rows(params, rankine["cycle"], rankine),
    ]
    pd.DataFrame(balance_rows).to_csv(RESULTS / "energy_balance.csv", index=False)

    mass_rows = [_mass_balance_rows(params, dfsc["cycle"])]
    pd.DataFrame(mass_rows).to_csv(RESULTS / "mass_balance.csv", index=False)

    print("\n=== BASELINE COMPARISON ===")
    print(
        result[
            [
                "cycle",
                "working_fluid_mass_kg",
                "turbine_work_mj",
                "pump_work_mj",
                "oxygen_compression_work_mj",
                "net_work_mj_per_kg_h2",
                "net_efficiency_percent",
            ]
        ].to_string(index=False)
    )

    print("\n=== ENERGY BALANCE ===")
    print(
        pd.DataFrame(balance_rows)[
            [
                "cycle",
                "heat_input_mj_per_kg_h2",
                "oxygen_compression_work_mj_per_kg_h2",
                "condenser_heat_rejection_mj_per_kg_h2",
                "net_work_mj_per_kg_h2",
                "total_energy_input_mj_per_kg_h2",
                "total_energy_output_mj_per_kg_h2",
                "energy_balance_residual_mj_per_kg_h2",
                "energy_balance_relative_error_percent",
            ]
        ].to_string(index=False)
    )

    print("\n=== STOICHIOMETRIC MASS BALANCE ===")
    print(pd.DataFrame(mass_rows).to_string(index=False))


def sensitivity():
    rows = []

    temperatures_c = np.arange(600.0, 1001.0, 50.0)
    pressures_bar = [30.0, 50.0, 75.0, 100.0, 125.0, 150.0]

    for temperature_c in temperatures_c:
        for pressure_bar in pressures_bar:
            params = CycleParameters(
                turbine_inlet_temperature_k=temperature_c + 273.15,
                p_high_mpa=pressure_bar / 10.0,
            )

            dfsc = direct_fired_cycle(params)
            rankine = conventional_rankine_cycle(params)

            rows.append(
                {
                    "temperature_c": temperature_c,
                    "pressure_bar": pressure_bar,
                    "dfsc_efficiency_percent": dfsc["net_efficiency_percent"],
                    "rankine_efficiency_percent": rankine["net_efficiency_percent"],
                    "efficiency_difference_percentage_points": (
                        dfsc["net_efficiency_percent"]
                        - rankine["net_efficiency_percent"]
                    ),
                    "dfsc_net_work_mj_per_kg_h2": dfsc["net_work_mj_per_kg_h2"],
                    "rankine_net_work_mj_per_kg_h2": rankine["net_work_mj_per_kg_h2"],
                }
            )

    sensitivity_df = pd.DataFrame(rows)
    sensitivity_df.to_csv(RESULTS / "sensitivity_results.csv", index=False)

    temp_df = sensitivity_df[sensitivity_df["pressure_bar"] == 100.0]

    plt.figure(figsize=(8, 5))
    plt.plot(
        temp_df["temperature_c"],
        temp_df["dfsc_efficiency_percent"],
        marker="o",
        label="Hydrogen direct-fired steam cycle",
    )
    plt.plot(
        temp_df["temperature_c"],
        temp_df["rankine_efficiency_percent"],
        marker="s",
        label="Conventional Rankine cycle",
    )
    plt.xlabel("Turbine inlet temperature (°C)")
    plt.ylabel("Net efficiency (%)")
    plt.title("Cycle efficiency vs. turbine inlet temperature")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS / "efficiency_vs_temperature.png", dpi=200)
    plt.close()

    pressure_df = sensitivity_df[sensitivity_df["temperature_c"] == 800.0]

    plt.figure(figsize=(8, 5))
    plt.plot(
        pressure_df["pressure_bar"],
        pressure_df["dfsc_efficiency_percent"],
        marker="o",
        label="Hydrogen direct-fired steam cycle",
    )
    plt.plot(
        pressure_df["pressure_bar"],
        pressure_df["rankine_efficiency_percent"],
        marker="s",
        label="Conventional Rankine cycle",
    )
    plt.xlabel("Turbine inlet pressure (bar)")
    plt.ylabel("Net efficiency (%)")
    plt.title("Cycle efficiency vs. turbine inlet pressure")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS / "efficiency_vs_pressure.png", dpi=200)
    plt.close()


def ts_diagram():
    params = CycleParameters()
    state_1, state_2, _, _ = pump_state(
        params.p_low_mpa,
        params.p_high_mpa,
        params.pump_efficiency,
    )
    state_3, state_4s, state_4 = turbine_states(
        params.p_high_mpa,
        params.p_low_mpa,
        params.turbine_inlet_temperature_k,
        params.turbine_isentropic_efficiency,
    )

    actual_s = [state_1.s, state_2.s, state_3.s, state_4.s, state_1.s]
    actual_T = [state_1.T - 273.15, state_2.T - 273.15, state_3.T - 273.15, state_4.T - 273.15, state_1.T - 273.15]
    ideal_s = [state_3.s, state_4s.s]
    ideal_T = [state_3.T - 273.15, state_4s.T - 273.15]

    plt.figure(figsize=(8, 5.5))
    plt.plot(actual_s, actual_T, marker="o", label="Actual Rankine path")
    plt.plot(ideal_s, ideal_T, linestyle="--", marker="x", label="Isentropic turbine reference")
    plt.annotate("1: condenser outlet", (state_1.s, state_1.T - 273.15), xytext=(8, 8), textcoords="offset points")
    plt.annotate("2: pump outlet", (state_2.s, state_2.T - 273.15), xytext=(8, 8), textcoords="offset points")
    plt.annotate("3: turbine inlet", (state_3.s, state_3.T - 273.15), xytext=(8, 8), textcoords="offset points")
    plt.annotate("4: turbine outlet", (state_4.s, state_4.T - 273.15), xytext=(8, -16), textcoords="offset points")
    plt.xlabel("Specific entropy (kJ/kg·K)")
    plt.ylabel("Temperature (°C)")
    plt.title("Baseline steam-cycle T-s diagram")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS / "ts_diagram.png", dpi=200)
    plt.close()


if __name__ == "__main__":
    baseline()
    sensitivity()
    ts_diagram()
    print("\nAll validation outputs and figures saved to results/")
