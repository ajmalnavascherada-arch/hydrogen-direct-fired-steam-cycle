from iapws import IAPWS97


def state_pt(p_mpa: float, temperature_k: float) -> IAPWS97:
    return IAPWS97(P=p_mpa, T=temperature_k)


def state_ps(p_mpa: float, entropy_kj_per_kgk: float) -> IAPWS97:
    return IAPWS97(P=p_mpa, s=entropy_kj_per_kgk)


def state_ph(p_mpa: float, enthalpy_kj_per_kg: float) -> IAPWS97:
    """Return a water/steam state from pressure and specific enthalpy."""
    return IAPWS97(P=p_mpa, h=enthalpy_kj_per_kg)


def pump_state(p_low_mpa: float, p_high_mpa: float, pump_efficiency: float):
    # Condenser outlet: saturated liquid.
    state_1 = IAPWS97(P=p_low_mpa, x=0.0)

    delta_p = p_high_mpa - p_low_mpa
    h2s = state_1.h + state_1.v * delta_p * 1000.0
    h2 = state_1.h + (h2s - state_1.h) / pump_efficiency
    state_2 = state_ph(p_high_mpa, h2)

    return state_1, state_2, h2s, h2


def turbine_states(
    p_high_mpa: float,
    p_low_mpa: float,
    temperature_k: float,
    turbine_efficiency: float,
):
    state_3 = state_pt(p_high_mpa, temperature_k)
    state_4s = state_ps(p_low_mpa, state_3.s)

    h4 = state_3.h - turbine_efficiency * (state_3.h - state_4s.h)
    state_4 = state_ph(p_low_mpa, h4)

    return state_3, state_4s, state_4
