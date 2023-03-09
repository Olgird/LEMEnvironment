from configs import *
import copy
import random
import pandas as pd
import prosumer


def randGauss(mu,sigma,scope,dot):
    a = random.gauss(mu,sigma)
    a = round(a,dot) 
    if a <scope[0]:
        a = scope[0]

    if a > scope[1]:
        a = scope[1]

    return a

def C_to_F(C):
    F = C * 1.8 + 32
    return F

class LEME():
    def __init__(self) -> None:
        self.n_prosumer = N_PROSUMER

        # 对应数据data的第多少行
        self.index = 1

        self.rate_inflexible_load = 0.2

        self.rate_sell_pricing = 0.3

        self.prosumer_setting = []

        self.prosumer = []

        # 
        self.data_prosumer = []
        # 
        self.data_weather = []
        # Electricity Pricing	6h Prediction Electricity Pricing 	12h Prediction Electricity Pricing 	
        # 24h Prediction Electricity Pricing   Sell Pricing
        self.data_price = []

        self.training_set = []
        self.validation_set =[]
        self.n_validation_set = 50

        self.t = 0

        # rate
        self.penalty_commuting = PENALTY_COMMUTING
        self.penalty_thermal = PENALTY_THERMAL

        for i in range(Prosumer1['number']):
            t = copy.deepcopy(Prosumer1)
            self.prosumer_setting.append(t)
        
        # 初始化
        self.init_data_price()
        self.init_data_prosumer()
        self.init_data_weather()
        self.init_trainning_set()

        



    def reset(self):
        # 清空prosumer 和 时间
        self.prosumer = []
        self.t = 0

        # 初始化文件位置
        # print(self.training_set)
        self.index = int(random.choice(self.training_set) * 24 + 1)
        
        # 初始化每个prosumer
        for i in range(self.n_prosumer):
            
            id_prosumer = i

            E0_ES = randGauss(E0ES[0],E0ES[1],E0ES[2],1)
            E0_EV = randGauss(E0EV[0],E0EV[1],E0EV[2],1)

            dep = randGauss(TDEP[0],TDEP[1],TDEP[2],0)
            arr = randGauss(TARR[0],TARR[1],TARR[2],0)
            Ecom = randGauss(ECOM[0],ECOM[1],ECOM[2],2)
            # 时间是整数
            EV_dep_arr_Ecom = [[int(dep),int(arr),Ecom]]

            # 时间是整数
            tter = randGauss(TTER[0],TTER[1],TTER[2],0)
            tin = randGauss(TIN[0],TIN[1],TIN[2],0)

            SA_tin_tter = [int(tin),int(tter)]

            inT0 = randGauss(T0IN[0],T0IN[1],T0IN[2],1)

            # 摄氏度 转 华氏度
            inT0 = C_to_F(inT0)





            own_PV = self.prosumer_setting[i]['own_PV']
            own_ES = self.prosumer_setting[i]['own_ES'] 
            ES_P_max = self.prosumer_setting[i]['ES_P_max'] 
            E_ES_min = self.prosumer_setting[i]['E_ES_min'] 
            E_ES_max = self.prosumer_setting[i]['E_ES_max'] 
            E_ES_capcity = self.prosumer_setting[i]['E_ES_capcity'] 
            Charge_efficiency_ES = self.prosumer_setting[i]['Charge_efficiency_ES'] 

            own_EV = self.prosumer_setting[i]['own_EV'] 
            EV_P_max = self.prosumer_setting[i]['EV_P_max'] 
            E_EV_min = self.prosumer_setting[i]['E_EV_min'] 
            E_EV_max = self.prosumer_setting[i]['E_EV_max'] 
            E_EV_capcity = self.prosumer_setting[i]['E_EV_capcity'] 
            Charge_efficiency_EV = self.prosumer_setting[i]['Charge_efficiency_EV'] 

            own_SA = self.prosumer_setting[i]['own_SA'] 
            P_SA_cyc = self.prosumer_setting[i]['P_SA_cyc'] 
            n_cyc = self.prosumer_setting[i]['n_cyc'] 


            T_min = self.prosumer_setting[i]['T_min'] 
            T_max = self.prosumer_setting[i]['T_max']
            C = self.prosumer_setting[i]['C'] 
            R = self.prosumer_setting[i]['R'] 
            p_max = self.prosumer_setting[i]['p_max'] 
            E = self.prosumer_setting[i]['E']

            # 读取当前的 室外温度
            outT0 = self.data_weather[self.index][0]

            p = prosumer.Prosumer(id_prosumer,DELTA_T,
                                            own_PV,
                 own_ES,ES_P_max,E_ES_min,E_ES_max,E_ES_capcity,Charge_efficiency_ES,E0_ES,
                 own_EV,EV_P_max,E_EV_min,E_EV_max,E_EV_capcity,Charge_efficiency_EV,E0_EV,EV_dep_arr_Ecom,
                 own_SA,P_SA_cyc,n_cyc,SA_tin_tter,
                 inT0, outT0, T_min, T_max, C, R, E, p_max)
            self.prosumer.append(p)
            
        # 提取每个prosumer的状态
        state = self.get_state()

            
        
        return state
    
    def step(self,action):

        # 保存结果
        L_all_p = []
        L_commuting_error = []
        L_thermal_error = []

        # 每个prosumer do action 并且把结果保存
        # action a_hvac [-1,1] a_ES [-1,1] a_EV [-1,1] a_SA {0,1}
        for i in range(self.n_prosumer):
            a_hvac,a_ES,a_EV,a_SA = action[i]
            inverter_ac_power_per_w = self.data_prosumer[i][self.index + self.t][11]
            outT = self.data_weather[self.index + self.t][0]
            # def do_actions(self,t,inverter_ac_power_per_w,outT,a_ES,a_EV,a_SA,a_HVAC):
            all_p,commuting_error,thermal_error =self.prosumer[i].do_actions(self.t,inverter_ac_power_per_w,outT,a_ES,a_EV,a_SA,a_hvac)
            
            # 
            L_all_p.append(all_p + self.data_prosumer[i][self.index + self.t][7])
            L_commuting_error.append(commuting_error)
            L_thermal_error.append(thermal_error)
    
        done = False
        # 时间 ++ 
        self.t = self.t + 1
        if self.t == 24:
            done = True

        # 返回下个时刻的状态
        _state = self.get_state()

        # 计算 reward 
        L_reward = []
        L_penalty_commuting = []
        L_penalty_thermal = []
        L_cost = []

        price_buy ,price_sell = self.MMR(L_all_p)
        
        
        for i in range(self.n_prosumer):
            L_penalty_commuting.append(L_commuting_error[i] * self.penalty_commuting)

            L_penalty_thermal.append(L_thermal_error[i] * self.penalty_thermal)
            
            if L_all_p[i] >= 0:
                L_cost.append(L_all_p[i] * price_buy * DELTA_T)
            else:
                L_cost.append(L_all_p[i] * price_sell * DELTA_T)

        for i in range(self.n_prosumer):
            L_reward.append(-(L_cost[i] + L_penalty_commuting[i] + L_penalty_thermal[i]))
        

        # 返回 下一个状态 ，reward，done，cost，
        return _state ,L_reward, done , L_cost,L_penalty_commuting,L_penalty_thermal
    

    def init_data_prosumer(self):
        for i in range(self.n_prosumer):
            file = 'data\citylearn_challenge_2022_phase_all\Building_'+ str(i+1)+'.csv'
            df = pd.read_csv(file)
            df = df.values.tolist()

            for j in range(len(df)):
                df[j][7] = df[j][7] * self.rate_inflexible_load

            self.data_prosumer.append(df)


            
    
    def init_data_weather(self):
        file = 'data\citylearn_challenge_2022_phase_all\weather.csv'

        df = pd.read_csv(file)
        df = df.values.tolist()
        self.data_weather = df
        

        
    def init_data_price(self):

        file = 'data\citylearn_challenge_2022_phase_all\pricing.csv'

        df = pd.read_csv(file)
        df = df.values.tolist()

        for i in range(len(df)):
            df[i].append(df[i][0]*self.rate_sell_pricing)

        self.data_price = df

    
    def init_trainning_set(self):
        L = list(range(1,365))
        random.shuffle(L)
        self.validation_set = L[:self.n_validation_set]
        self.training_set = L[self.n_validation_set:]


    def get_state(self):
        state =[]
        for i in range(self.n_prosumer):
            p_state = []

            

            # 月
            p_state.append(self.data_prosumer[i][self.index + self.t][0])

            # 小时
            p_state.append(self.data_prosumer[i][self.index + self.t][1])

            # 星期
            p_state.append(self.data_prosumer[i][self.index + self.t][2])

            # 7 inflexible 电量消费
            for j in range(1,24):
                p_state.append(self.data_prosumer[i][self.index + self.t - j][7])

            # 价格
            p_state.append(self.data_price[self.index + self.t][0])
            p_state.append(self.data_price[self.index + self.t][1])
            p_state.append(self.data_price[self.index + self.t][4])

            # 温度
            p_state.append(C_to_F(self.data_weather[self.index + self.t][0]))
            p_state.append(self.prosumer[i].myHVAC.now_temperature)

            # SA
            p_state.append(self.prosumer[i].mySA.own_SA)
            p_state.append(self.prosumer[i].mySA.SA_tin_tter[0])
            p_state.append(self.prosumer[i].mySA.SA_tin_tter[1])

            # EV
            p_state.append(self.prosumer[i].myEV.own_EV)
            p_state.append(self.prosumer[i].myEV.A_EV)

            p_state.append(self.prosumer[i].myEV.E_EV)

            # PV 我觉得应该是t-1的
            p_state.append(self.prosumer[i].myPV.own_PV)
            p_state.append(self.data_prosumer[i][self.index + self.t - 1][11])

            # ES
            p_state.append(self.prosumer[i].myES.own_ES)
            p_state.append(self.prosumer[i].myES.E_ES)


            state.append(p_state)

        return state


    def MMR(self,P_list):
        
        n_P = sum(P_list)
        buy = self.data_price[self.index + self.t][0]
        sell = self.data_price[self.index + self.t][4]
        mid_price = (buy + sell) / 2

        nc_P = 0
        ng_P = 0
        # 计算nc_P ng_P
        for i in range(self.n_prosumer):
            if P_list[i] > 0 :
                nc_P += P_list[i]
            else:
                ng_P +=P_list[i]
                



        if n_P == 0:
            price_buy = mid_price
            price_sell = mid_price
        elif n_P > 0:
            price_buy = (mid_price * abs(ng_P) + buy * n_P)/nc_P 
            price_sell = mid_price
        elif n_P < 0:
            price_buy = mid_price
            price_sell = (mid_price * nc_P + sell * abs(n_P)) / abs(ng_P)

        print('price:')
        print(price_buy ,price_sell)

        return price_buy ,price_sell

    

