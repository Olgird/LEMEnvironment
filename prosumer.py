from energy_model import *

class Prosumer():
    def __init__(self,id_prosumer,delta_t,
                 own_PV,
                 own_ES,ES_P_max,E_ES_min,E_ES_max,E_ES_capcity,Charge_efficiency_ES,E0_ES,
                 own_EV,EV_P_max,E_EV_min,E_EV_max,E_EV_capcity,Charge_efficiency_EV,E0_EV,EV_dep_arr_Ecom,
                 own_SA,P_SA_cyc,n_cyc,SA_tin_tter,
                 inT0, outT0, T_min, T_max, C, R, E, p_max):
        # 为了方便找到对应数据的地址，设置一个id
        self.id_prosumer = id_prosumer

        # 初始化 自己的部件
        self.myPV = PV(own_PV)
        self.myES = ES(own_ES,ES_P_max,E_ES_min,E_ES_max,E_ES_capcity,Charge_efficiency_ES,E0_ES,delta_t)

        self.myEV = EV(own_EV,EV_P_max,E_EV_min,E_EV_max,E_EV_capcity,Charge_efficiency_EV,E0_EV,delta_t,EV_dep_arr_Ecom)

        self.mySA = SA(own_SA,P_SA_cyc,n_cyc,delta_t,SA_tin_tter)

        self.myHVAC = HVAC(inT0, outT0, T_min, T_max, C, R, p_max, E, delta_t)
        

        # 初始化 EMS
        
        
    def do_actions(self,t,inverter_ac_power_per_w,outT,a_ES,a_EV,a_SA,a_HVAC):
        
        # 定义多个功率
        p_PV = 0
        p_ES = 0
        p_EV = 0
        p_SA = 0
        p_HVAC = 0

        # print(a_ES,a_EV,a_SA,a_HVAC)

        # 做动作，得到每个部件的功率
        p_PV = self.myPV.get_generation(inverter_ac_power_per_w)
        
        p_ES = self.myES.ES_Charge(a_ES)
        p_EV = self.myEV.EV_charge(a_EV,t)
        p_SA = self.mySA.running_SA(t,a_SA)
        p_HVAC = self.myHVAC.running_HVAC(a_HVAC, outT)

        # print(p_PV , p_ES , p_EV , p_SA , p_HVAC)

        # 惩罚
        commuting_error = self.myEV.EV_commuting(t)

        thermal_error = self.myHVAC.get_difference()

        # 计算单个prosumer的全部功率之和
        all_p = p_PV + p_ES + p_EV + p_SA + p_HVAC

        

        return all_p,commuting_error,thermal_error



        


        