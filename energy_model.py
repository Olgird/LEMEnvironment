


class PV():
    def __init__(self,own_PV):
        self.own_PV = own_PV
        

    '''
    输入 产生的功率(W)(瓦)
    
    输出 产生功率 千瓦
    '''
    def get_generation(self,inverter_ac_power_per_w):
        inverter_ac_power_per_kw = inverter_ac_power_per_w / 1000
        # 乘了own 如果own为0 的话就代表不存在own
        return (-inverter_ac_power_per_kw) * self.own_PV
    
class ES():
    '''
    P_max 最大充放电功率
    E_ES_min 最小电量
    E_ES_max 最大电量
    E_ES_capcity 容量
    Charge_efficiency_ES 充电效率
    '''
    def __init__(self,own_ES,P_max,E_ES_min,E_ES_max,E_ES_capcity,Charge_efficiency_ES,E0_ES,delta_t):
        # 1表示拥有 ES，0 表示没有拥有ES
        self.own_ES = own_ES

        self.P_max = P_max
        self.E_ES_min = E_ES_min
        self.E_ES_max = E_ES_max
        self.E_ES_capcity = E_ES_capcity
        self.Charge_efficiency_ES = Charge_efficiency_ES
        self.E_ES = E0_ES
        self.delta_t = delta_t

        pass
    

    '''
    input: a_ES ES的动作
    output: P_ES_charge ES的充电功率
    '''
    def ES_Charge(self,a_ES):
        if a_ES >=0:
            P_ES_charge = min(a_ES*self.P_max ,(self.E_ES_max-self.E_ES)/(self.Charge_efficiency_ES * self.delta_t))
            # 充电改变电量
            self.E_ES = self.E_ES + self.delta_t * P_ES_charge * self.Charge_efficiency_ES

            return P_ES_charge * self.own_ES
        
        else:
            P_ES_discharge = max(a_ES*self.P_max ,(self.E_ES_min-self.E_ES)*self.Charge_efficiency_ES /( self.delta_t))

            # 放电改变电量
            self.E_ES = self.E_ES + self.delta_t * P_ES_discharge / self.Charge_efficiency_ES

            return P_ES_discharge * self.own_ES
        
    

class EV():
    '''
    EV_dep_arr 是一个list, list中包含(dep,arr,E_EV_com)时间
    E_EV_com 对应的是每次通勤消耗的电量
    delta_t 为时间间隔
    '''
    def __init__(self,own_EV,P_max,E_EV_min,E_EV_max,E_EV_capcity,Charge_efficiency_EV,E0_EV,delta_t,EV_dep_arr_Ecom,):
        # 0表示没有EV，1表示拥有EV
        self.own_EV = own_EV

        self.P_max = P_max
        
        self.E_EV_min = E_EV_min
        self.E_EV_max = E_EV_max
        self.E_EV_capcity = E_EV_capcity
        self.Charge_efficiency_EV = Charge_efficiency_EV
        self.E_EV = E0_EV
        self.delta_t = delta_t
        self.EV_dep_arr_Ecom = EV_dep_arr_Ecom
        
    def EV_charge(self,a_EV,t):

        A_EV = 1

        # 如果在外面的话A_EV 为 0 表示不能充放电
        for dep,arr,Ecom in self.EV_dep_arr_Ecom:
            if t>=dep and t<= arr:
                A_EV = 0 
        if a_EV >=0:
            P_EV_charge =A_EV * (min(a_EV*self.P_max ,(self.E_EV_max-self.E_EV)/(self.Charge_efficiency_EV * self.delta_t)))

            # 充电放电改变电量
            self.E_EV = self.E_EV + self.delta_t * P_EV_charge *self.Charge_efficiency_EV

            return P_EV_charge * self.own_EV
        else:
            P_EV_discharge =A_EV * max(a_EV*self.P_max ,(self.E_EV_min-self.E_EV)*self.Charge_efficiency_EV /( self.delta_t))
            # 放电改变电量
            self.E_EV = self.E_EV + self.delta_t * P_EV_discharge / self.Charge_efficiency_EV

            return P_EV_discharge * self.own_EV
    
    '''
    通勤 在回来的时候减少电量 并且返回min(self.E_EV - Ecom,0), 表示惩罚
    '''
    def EV_commuting(self,t):
        for dep,arr,Ecom in self.EV_dep_arr_Ecom:
            # 如果汽车开回来，电量减少, 如果低于0，电量设置成0
            if t == arr:
                self.E_EV = max(0,self.E_EV - Ecom)
            # 如果出勤不够电，那就返回惩罚
            if t == dep:
                return min(self.E_EV - Ecom,0) * self.own_EV
        
        return 0

        
        

        
class SA():
    def __init__(self,own_SA,P_SA_cyc,n_cyc,delta_t,SA_tin_tter):
        self.own_SA = own_SA
        
        self.P_SA_cyc = P_SA_cyc
        self.delta_t = delta_t

        # 最早开始时间和最晚结束时间 [9,14) 不包括14点
        self.SA_tin_tter = SA_tin_tter
        self.n_cyc = n_cyc

        # 记录激活的时间
        self.t_activate = -1

    def running_SA(self,t,a_SA):
        A_SA = 0

        tin = self.SA_tin_tter[0]
        tter = self.SA_tin_tter[1]

        if t>=tin and t<=(tter - self.n_cyc):
            A_SA = 1

        # 如果还没有激活，并且a_SA ==1
        if A_SA == 1 and a_SA == 1 and self.t_activate == -1:
            self.t_activate = t

        # 如果在截止时间到达还没激活，那就直接激活
        if t==(tter - self.n_cyc) and self.t_activate == -1:
            self.t_activate = t

        # 运行，返回cyc中没段的功率
        for i in range(self.n_cyc):
            if t == (self.t_activate + i):
                return self.P_SA_cyc[i] * self.own_SA
            
        return 0
            


    


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
                 heat_resistance, a_hvac, P_max_hvac,
                 delta_t
                 ):
        self.init_indoor_temerpature = init_indoor_temerpature
        self.min_comfort_temperature = min_comfort_temperature
        self.max_comfort_temperature = max_comfort_temperature
        self.heat_capacity = heat_capacity
        self.outtemp = outtemp
        self.heat_resistance = heat_resistance
        self.energy_efficiency = a_hvac * max_comfort_temperature
        self.P_max_hvac = P_max_hvac
        self.delta_t = delta_t
        self.now_temperature = self.init_indoor_temerpature
    
    def calculate(self, a_hvac):
        # ####################################################################
        self.energy_efficiency = a_hvac * self.max_comfort_temperature
        next_step_tempature = self.now_temperature - (self.now_temperature - self.outtemp + 
        self.energy_efficiency * self.heat_resistance * self.heat_capacity) * self.delta_t / (self.heat_capacity * self.heat_resistance)
        return next_step_tempature
    
    """
    thermal_cpmfort_weight is a const int
    hvac_reward = -thermal_cpmfort_weight * (abs(now_tempature - max_temperature) + abs(min_temperature - now_temperature))
    """
