
from dataclasses import dataclass


@dataclass
class CycleParameters:
    h2_mass_kg: float = 1.0
    h2_lhv_mj_per_kg: float = 120.0

    p_high_mpa: float = 10.0
    p_low_mpa: float = 0.01

    turbine_inlet_temperature_k: float = 1073.15

    turbine_isentropic_efficiency: float = 0.85
    pump_efficiency: float = 0.85
    oxygen_compressor_efficiency: float = 0.75

    combustion_efficiency: float = 0.99
    boiler_efficiency: float = 0.90

    oxygen_inlet_pressure_mpa: float = 0.1
    oxygen_inlet_temperature_k: float = 298.15

    oxygen_to_h2_mass_ratio: float = 8.0
    water_to_h2_mass_ratio: float = 9.0

    oxygen_cp_kj_per_kgk: float = 0.918
    oxygen_gas_constant_kj_per_kgk: float = 0.2598

    @property
    def h2_lhv_kj(self) -> float:
        return self.h2_mass_kg * self.h2_lhv_mj_per_kg * 1000.0
