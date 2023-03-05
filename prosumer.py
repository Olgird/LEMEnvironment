from energy_model import *

class Prosumer():
    def __init__(self,id_prosumer,delta_t,
                 own_PV,
                 own_ES,ES_P_max,E_ES_min,E_ES_max,E_ES_capcity,Charge_efficiency_ES,E0_ES,
                 own_EV,EV_P_max,E_EV_min,E_EV_max,E_EV_capcity,Charge_efficiency_EV,E0_EV,EV_dep_arr_Ecom,
                 own_SA,P_SA_cyc,n_cyc,SA_tin_tter,
                 init_indoor_temerpature, outtemp, min_comfort_temperature, max_comfort_temperature, heat_capacity,
                 heat_resistance, energy_efficiency, max_hvac_voltage,
                 timestep):
        # 为了方便找到对应数据的地址，设置一个id
        self.id_prosumer = id_prosumer

        # 初始化 自己的部件
        self.myPV = PV(own_PV)
        self.myES = ES(own_ES,ES_P_max,E_ES_min,E_ES_max,E_ES_capcity,Charge_efficiency_ES,E0_ES,delta_t)

        self.myEV = EV(own_EV,EV_P_max,E_EV_min,E_EV_max,E_EV_capcity,Charge_efficiency_EV,E0_EV,delta_t,EV_dep_arr_Ecom)

        self.mySA = SA(own_SA,P_SA_cyc,n_cyc,delta_t,SA_tin_tter)

        self.myHVAC = HVAC(init_indoor_temerpature, outtemp, min_comfort_temperature, max_comfort_temperature, heat_capacity,
                 heat_resistance, energy_efficiency, max_hvac_voltage,
                 timestep)
        
    def do_actions(self,t,a_ES,a_EV,a_SA):
        
        p_ES = 0
        p_EV = 0
        p_SA = 0


        p_ES = self.myES.ES_Charge(a_ES)
        p_EV = self.myEV.EV_charge(a_EV,t)
        p_SA = self.mySA.running_SA(t,a_SA)
        # 惩罚
        commuting_error = self.myEV.EV_commuting(t)


        all_p = p_ES + p_EV + p_SA

        return all_p,commuting_error



        


        