import math

from src.parameters import CycleParameters
from src.cycle_models import direct_fired_cycle, conventional_rankine_cycle
from src.thermodynamics import pump_state, turbine_states


def test_direct_fired_cycle_returns_positive_work():
    result = direct_fired_cycle(CycleParameters())
    assert result["net_work_mj_per_kg_h2"] > 0
    assert result["net_efficiency_percent"] > 0


def test_rankine_cycle_returns_positive_work():
    result = conventional_rankine_cycle(CycleParameters())
    assert result["net_work_mj_per_kg_h2"] > 0
    assert result["net_efficiency_percent"] > 0


def test_stoichiometric_mass_ratios():
    params = CycleParameters()
    result = direct_fired_cycle(params)

    assert math.isclose(result["oxygen_mass_kg"], 8.0)
    assert math.isclose(result["combustion_water_mass_kg"], 9.0)


def test_cycle_energy_balance():
    params = CycleParameters()
    dfsc = direct_fired_cycle(params)
    rankine = conventional_rankine_cycle(params)

    for result in (dfsc, rankine):
        total_input = (
            result["heat_input_mj"]
            + result["oxygen_compression_work_mj"]
        )
        total_output = (
            result["net_work_mj_per_kg_h2"]
            + result["condenser_heat_rejection_mj"]
        )
        assert math.isclose(total_input, total_output, rel_tol=1e-10, abs_tol=1e-10)


def test_state_order_and_pressures():
    params = CycleParameters()
    state_1, state_2, _, _ = pump_state(
        params.p_low_mpa, params.p_high_mpa, params.pump_efficiency
    )
    state_3, state_4s, state_4 = turbine_states(
        params.p_high_mpa,
        params.p_low_mpa,
        params.turbine_inlet_temperature_k,
        params.turbine_isentropic_efficiency,
    )

    assert math.isclose(state_1.P, params.p_low_mpa)
    assert math.isclose(state_2.P, params.p_high_mpa)
    assert math.isclose(state_3.P, params.p_high_mpa)
    assert math.isclose(state_4s.P, params.p_low_mpa)
    assert math.isclose(state_4.P, params.p_low_mpa)
    assert state_3.T > state_4.T
