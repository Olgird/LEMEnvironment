


class PV():
    def __init__(self):
        pass

    '''
    输入 产生的功率(W)(瓦)
    
    输出 产生功率 千瓦
    '''
    def get_generation(self,inverter_ac_power_per_w):
        inverter_ac_power_per_kw = inverter_ac_power_per_w / 1000
        return inverter_ac_power_per_kw
    
class ES():
    '''
    P_max 最大充放电功率
    E_ES_min 最小电量
    E_ES_max 最大电量
    E_ES_capcity 容量
    Charge_efficiency_ES 充电效率
    '''
    def __init__(self,P_max,E_ES_min,E_ES_max,E_ES_capcity,Charge_efficiency_ES,E0_ES):

        self.P_max = P_max
        self.E_ES_min = E_ES_min
        self.E_ES_max = E_ES_max
        self.E_ES_capcity = E_ES_capcity
        self.Charge_efficiency_ES = Charge_efficiency_ES
        self.E_ES = E0_ES

        pass

class HVAC():
    """
        init_indoor_temperature
        outdoor_temperature
        min_comfort_temperature
        max_comfort_temperature
        heat_capacity
        heat_resistance
        energy_efficiency
        hvac_voltage
        max_hvac_voltage
    """
    def __init__(self, init_indoor_temerpature, outtemp, min_comfort_temperature, max_comfort_temperature, heat_capacity,
                 heat_resistance, energy_efficiency, max_hvac_voltage,
                 timestep
                 ):
        self.init_indoor_temerpature = init_indoor_temerpature
        self.min_comfort_temperature = min_comfort_temperature
        self.max_comfort_temperature = max_comfort_temperature
        self.heat_capacity = heat_capacity
        self.outtemp = outtemp
        self.heat_resistance = heat_resistance
        self.energy_efficiency = energy_efficiency
        self.max_hvac_voltage = max_hvac_voltage
        self.timestep = timestep
        self.now_temperature = self.init_indoor_tempature
    
    def calculate(self):
        next_step_tempature = self.now_temperature - (self.now_temperature - self.outtemp + 
        self.energy_efficiency * self.heat_resistance * self.heat_capacity) * self.timestep / (self.heat_capacity * self.heat_resistance)
        return next_step_tempature
    
    """
    thermal_cpmfort_weight is a const int
    hvac_reward = -thermal_cpmfort_weight * (abs(now_tempature - max_temperature) + abs(min_temperature - now_temperature))
    """