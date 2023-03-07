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

        self.discount = 0.2

        self.prosumer_setting = []

        self.prosumer = []

        self.data_prosumer = []
        self.data_weather = []
        self.data_price = []

        for i in range(Prosumer1['number']):
            t = copy.deepcopy(Prosumer1)
            self.prosumer_setting.append(t)
        
        
        



        pass



    def reset(self):
        self.prosumer = []
           
        for i in range(self.n_prosumer):
            
            id_prosumer = i+1

            E0_ES = randGauss(E0ES[0],E0ES[1],E0ES[2],1)
            E0_EV = randGauss(E0EV[0],E0EV[1],E0EV[2],1)

            dep = randGauss(TDEP[0],TDEP[1],TDEP[2],0)
            arr = randGauss(TARR[0],TARR[1],TARR[2],0)
            Ecom = randGauss(ECOM[0],ECOM[1],ECOM[2],2)
            # 时间是整数
            EV_dep_arr_Ecom = [int(dep),int(arr),Ecom]

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



            self.prosumer.append(prosumer(id_prosumer,DELTA_T,
                                            own_PV,
                 own_ES,ES_P_max,E_ES_min,E_ES_max,E_ES_capcity,Charge_efficiency_ES,E0_ES,
                 own_EV,EV_P_max,E_EV_min,E_EV_max,E_EV_capcity,Charge_efficiency_EV,E0_EV,EV_dep_arr_Ecom,
                 own_SA,P_SA_cyc,n_cyc,SA_tin_tter,
                 inT0, outT0, T_min, T_max, C, R, E, p_max))


        return 0
    
    def step(self):

        return 0
    

    def init_data_prosumer(self):
        for i in range(self.n_prosumer):
            file = 'data\citylearn_challenge_2022_phase_all\Building_'+ str(i+1)+'.csv'
            df = pd.read_csv(file)
            df = df.values.tolist()

            for j in range(len(df)):
                df[j][7] = df[j][7] * self.discount

            self.data_prosumer.append(df)


            



        
    
    def init_data_weather(self):
        

        
        return 0
    
    def init_data_price(self):

        return 0 
    

    def MMR(self,price_buy,price_sell,P_list):

        price_buy_list = []
        price_sell_list = []
        return price_buy_list,price_sell_list

    

