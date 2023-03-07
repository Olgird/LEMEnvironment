
# SA 的参数
N_CYC_SA = 2
P_CYC_SA = [0.56,0.63]

# ES 的参数

E_ES_CAPACITY = 10
E_ES_MAX = 10
E_ES_MIN = 2
CHARGE_EFFICIENCY_ES = 0.95
P_ES_MAX = 4

# EV 的参数

E_EV_CAPACITY = 15
E_EV_MAX = 15
E_EV_MIN = 12
CHARGE_EFFICIENCY_EV = 0.93
P_EV_MAX = 6

# prosumer 的参数
TIN = [10 , 1 , [8,12]]
TTER = [18 , 1 , [16,20]]
T0IN = [21 , 1 , [19,24]]
E0ES = [6 , 1 , [4,8]]
TDEP = [9 , 1 , [7,11]]
TARR = [18 , 1 , [16,20]]
E0EV = [9 , 1 , [6,12]]
ECOM = [7.12 , 0.712 , [5.696 ,8.544]]

# HVAC 的参数 注意已经将摄氏度转换为华氏度
T_MIN = 66.2
T_MAX = 75.2
HVAC_C = 0.33
HVAC_R = 13.5
HVAC_E = 2.2
HVAC_P_MAX = 1.75


# 每个prosumer 的参数

N_PROSUMER = 1

PROSUMER_INFORMATION = [

    ]

    # def __init__(self,id_prosumer,delta_t,
    #              own_PV,
    #              own_ES,ES_P_max,E_ES_min,E_ES_max,E_ES_capcity,Charge_efficiency_ES,E0_ES,
    #              own_EV,EV_P_max,E_EV_min,E_EV_max,E_EV_capcity,Charge_efficiency_EV,E0_EV,EV_dep_arr_Ecom,
    #              own_SA,P_SA_cyc,n_cyc,SA_tin_tter,
    #              inT0, outT0, T_min, T_max, C, R, p_max):

Prosumer1 = {
    'number' : 1,
    'own_PV' : 1,
    'own_E' : 1,
    'own_EV' : 1,
    'own_SA' : 1,
    'ES_P_max':P_ES_MAX,
    'E_ES_min':E_ES_MIN,
    'E_ES_max' : E_ES_MAX,
    'E_ES_capcity':E_ES_CAPACITY,
    'Charge_efficiency_ES':CHARGE_EFFICIENCY_ES,
    'EV_P_max' : P_EV_MAX,
    'E_EV_min' :E_EV_MIN,
    'E_EV_max' : E_EV_MAX,
    'E_EV_capcity' : E_EV_CAPACITY,
    'Charge_efficiency_EV' :CHARGE_EFFICIENCY_EV,
    'P_SA_cyc' : P_CYC_SA,
    'n_cyc' : N_CYC_SA,
    'T_min' : T_MIN,
    'T_max' : T_MAX,
    'C':HVAC_C,
    'R':HVAC_R,
    'p_max':HVAC_P_MAX
    }


