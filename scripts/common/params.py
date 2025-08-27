user                = "cassagnea"
path_conf_file      = "../conf/src/K_14232.src"
nodes               = ["m1u", "opi5", "x7ti", "ai370"]
pinning_strategies  = ["packed", "loose", "distant", "guided", "os"]
path_schedulings    = "./inputs/schedulings/"
path_raw            = "./inputs/throughput/"
path_conso_raw      = "./inputs/conso_socket/"
path_conso_rapl_raw = "./inputs/conso_rapl/"
path_postpro        = "./outputs/1_postpro/"
path_conso_postpro  = "./outputs/2_postpro_with_conso/"
resources           = {"m1u": [4,16], "opi5": [4,4], "x7ti": [8,6], "ai370": [8,4] }
x                   = {"opi5": 1, "ai370": 3, "m1u": 2, "x7ti": 4 }
scheds_m1u          = ['m1u_2CATAC_16big_4little',
                       'm1u_2CATAC_8big_2little',
                       'm1u_FERTAC_16big_4little',
                       'm1u_FERTAC_8big_2little',
                       'm1u_HeRAD_16big_4little',
                       'm1u_HeRAD_8big_2little',
                       'm1u_OTAC_big_16big_4little',
                       'm1u_OTAC_big_8big_2little',
                       'm1u_OTAC_little_16big_4little',
                       'm1u_OTAC_little_8big_2little']
scheds_opi5         = ['opi5_2CATAC_2big_2little',
                       'opi5_2CATAC_4big_4little',
                       'opi5_FERTAC_2big_2little',
                       'opi5_FERTAC_4big_4little',
                       'opi5_HeRAD_2big_2little',
                       'opi5_HeRAD_4big_4little',
                       'opi5_OTAC_big_2big_2little',
                       'opi5_OTAC_big_4big_4little',
                       'opi5_OTAC_little_2big_2little',
                       'opi5_OTAC_little_4big_4little']
scheds_x7ti         = ['x7ti_2CATAC_3big_4little',
                       'x7ti_2CATAC_6big_8little',
                       'x7ti_FERTAC_3big_4little',
                       'x7ti_FERTAC_6big_8little',
                       'x7ti_HeRAD_3big_4little',
                       'x7ti_HeRAD_6big_8little',
                       'x7ti_OTAC_big_3big_4little',
                       'x7ti_OTAC_big_6big_8little',
                       'x7ti_OTAC_little_3big_4little',
                       'x7ti_OTAC_little_6big_8little']
scheds_ai370        = ['ai370_2CATAC_2big_4little',
                       'ai370_2CATAC_4big_8little',
                       'ai370_FERTAC_2big_4little',
                       'ai370_FERTAC_4big_8little',
                       'ai370_HeRAD_2big_4little',
                       'ai370_HeRAD_4big_8little',
                       'ai370_OTAC_big_2big_4little',
                       'ai370_OTAC_big_4big_8little',
                       'ai370_OTAC_little_2big_4little',
                       'ai370_OTAC_little_4big_8little']