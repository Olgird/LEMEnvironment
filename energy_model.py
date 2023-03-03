


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