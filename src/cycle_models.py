from .parameters import CycleParameters
from .thermodynamics import pump_state, turbine_states


def oxygen_compression_work_kj_per_kg_h2(params: CycleParameters) -> float:
    """First-order ideal-gas oxygen compressor estimate, per kg H2 basis."""
    cp = params.oxygen_cp_kj_per_kgk
    R = params.oxygen_gas_constant_kj_per_kgk
    gamma = cp / (cp - R)

    pressure_ratio = params.p_high_mpa / params.oxygen_inlet_pressure_mpa
    t1 = params.oxygen_inlet_temperature_k

    t2s = t1 * pressure_ratio ** ((gamma - 1.0) / gamma)
    w_is = cp * (t2s - t1)
    w_actual = w_is / params.oxygen_compressor_efficiency

    return params.oxygen_to_h2_mass_ratio * params.h2_mass_kg * w_actual


def _common_cycle_states(params: CycleParameters):
    state_1, state_2, h2s, h2 = pump_state(
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

    return state_1, state_2, state_3, state_4s, state_4, h2s, h2


def direct_fired_cycle(params: CycleParameters) -> dict:
    state_1, state_2, state_3, state_4s, state_4, h2s, h2 = _common_cycle_states(params)

    heat_available_kj = params.h2_lhv_kj * params.combustion_efficiency

    # Total circulating steam flow from the cycle energy balance.
    m_steam = heat_available_kj / (state_3.h - h2)

    turbine_work_kj = m_steam * (state_3.h - state_4.h)
    pump_work_kj = m_steam * (state_2.h - state_1.h)
    oxygen_work_kj = oxygen_compression_work_kj_per_kg_h2(params)
    condenser_heat_rejection_kj = m_steam * (state_4.h - state_1.h)
    net_work_kj = turbine_work_kj - pump_work_kj - oxygen_work_kj

    return {
        "cycle": "Hydrogen Direct-Fired Steam Cycle",
        "h2_mass_kg": params.h2_mass_kg,
        "oxygen_mass_kg": params.oxygen_to_h2_mass_ratio * params.h2_mass_kg,
        "combustion_water_mass_kg": params.water_to_h2_mass_ratio * params.h2_mass_kg,
        "working_fluid_mass_kg": m_steam,
        "combustion_water_fraction": (
            params.water_to_h2_mass_ratio * params.h2_mass_kg / m_steam
        ),
        "turbine_inlet_temperature_c": params.turbine_inlet_temperature_k - 273.15,
        "high_pressure_bar": params.p_high_mpa * 10.0,
        "low_pressure_bar": params.p_low_mpa * 10.0,
        "h1_kj_per_kg": state_1.h,
        "h2s_kj_per_kg": h2s,
        "h2_kj_per_kg": state_2.h,
        "h3_kj_per_kg": state_3.h,
        "h4s_kj_per_kg": state_4s.h,
        "h4_actual_kj_per_kg": state_4.h,
        "s1_kj_per_kgk": state_1.s,
        "s2_kj_per_kgk": state_2.s,
        "s3_kj_per_kgk": state_3.s,
        "s4s_kj_per_kgk": state_4s.s,
        "s4_actual_kj_per_kgk": state_4.s,
        "t1_c": state_1.T - 273.15,
        "t2_c": state_2.T - 273.15,
        "t3_c": state_3.T - 273.15,
        "t4s_c": state_4s.T - 273.15,
        "t4_actual_c": state_4.T - 273.15,
        "turbine_work_mj": turbine_work_kj / 1000.0,
        "pump_work_mj": pump_work_kj / 1000.0,
        "oxygen_compression_work_mj": oxygen_work_kj / 1000.0,
        "heat_input_mj": heat_available_kj / 1000.0,
        "condenser_heat_rejection_mj": condenser_heat_rejection_kj / 1000.0,
        "net_work_mj_per_kg_h2": net_work_kj / 1000.0,
        "net_efficiency_percent": net_work_kj / params.h2_lhv_kj * 100.0,
    }


def conventional_rankine_cycle(params: CycleParameters) -> dict:
    state_1, state_2, state_3, state_4s, state_4, h2s, h2 = _common_cycle_states(params)

    heat_available_kj = params.h2_lhv_kj * params.boiler_efficiency
    m_steam = heat_available_kj / (state_3.h - h2)

    turbine_work_kj = m_steam * (state_3.h - state_4.h)
    pump_work_kj = m_steam * (state_2.h - state_1.h)
    condenser_heat_rejection_kj = m_steam * (state_4.h - state_1.h)
    net_work_kj = turbine_work_kj - pump_work_kj

    return {
        "cycle": "Conventional Rankine Steam Cycle",
        "h2_mass_kg": params.h2_mass_kg,
        "oxygen_mass_kg": 0.0,
        "combustion_water_mass_kg": 0.0,
        "working_fluid_mass_kg": m_steam,
        "combustion_water_fraction": 0.0,
        "turbine_inlet_temperature_c": params.turbine_inlet_temperature_k - 273.15,
        "high_pressure_bar": params.p_high_mpa * 10.0,
        "low_pressure_bar": params.p_low_mpa * 10.0,
        "h1_kj_per_kg": state_1.h,
        "h2s_kj_per_kg": h2s,
        "h2_kj_per_kg": state_2.h,
        "h3_kj_per_kg": state_3.h,
        "h4s_kj_per_kg": state_4s.h,
        "h4_actual_kj_per_kg": state_4.h,
        "s1_kj_per_kgk": state_1.s,
        "s2_kj_per_kgk": state_2.s,
        "s3_kj_per_kgk": state_3.s,
        "s4s_kj_per_kgk": state_4s.s,
        "s4_actual_kj_per_kgk": state_4.s,
        "t1_c": state_1.T - 273.15,
        "t2_c": state_2.T - 273.15,
        "t3_c": state_3.T - 273.15,
        "t4s_c": state_4s.T - 273.15,
        "t4_actual_c": state_4.T - 273.15,
        "turbine_work_mj": turbine_work_kj / 1000.0,
        "pump_work_mj": pump_work_kj / 1000.0,
        "oxygen_compression_work_mj": 0.0,
        "heat_input_mj": heat_available_kj / 1000.0,
        "condenser_heat_rejection_mj": condenser_heat_rejection_kj / 1000.0,
        "net_work_mj_per_kg_h2": net_work_kj / 1000.0,
        "net_efficiency_percent": net_work_kj / params.h2_lhv_kj * 100.0,
    }
