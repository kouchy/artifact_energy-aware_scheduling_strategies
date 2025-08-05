#!/usr/bin/env python3

import statistics as stats
import common.params as params
import common.funcs as funcs

verbose = False

def _produce_csv(fw, sched, pinning, n_try):
    for i in range(0, n_try):
        in_filename = params.path_raw + pinning + "/" + sched + "_" + str(i) + ".txt"
        try:
            fr = open(in_filename, "r")
            lines=fr.readlines()
            lines_cnt = 0
            for line in lines:
                lines_cnt = lines_cnt + 1
                if "Signal Noise Ratio" in line:
                    break;
            cols = lines[lines_cnt + 6].split("|")
            thr = cols[9]
            fw.write(sched + "," + thr.strip() + "\n");
            fr.close()
        except IOError:
            print(f"'{in_filename}' does not appear to exist, skipped.")

def produce_csv(node_name, R_max, scheds, filename, pinning):
    fw = open(filename, "w")
    fw.write("sched_name,throughput_mbps\n")
    if pinning == "os":
        for R in range(1, R_max + 1):
            sched = node_name + "_os_R" + str(R)
            _produce_csv(fw, sched, pinning, 15)
    else:
        for sched in scheds:
            _produce_csv(fw, sched, pinning, 10)
    fw.close()

def _produce_csv_for_pgfplot(fw, sched, pinning, n_try):
    sched_short, max_big, max_little, strat, node_name, n_big, n_little = funcs.get_sched_info(sched, pinning, verbose)
    min_thr = 100000
    max_thr = 0
    sum_thr = 0
    thr_values = []
    for i in range(0, n_try):
        in_filename = params.path_raw + pinning + "/" + sched + "_" + str(i) + ".txt"
        try:
            fr = open(in_filename, "r")
            lines=fr.readlines()
            lines_cnt = 0
            for line in lines:
                lines_cnt = lines_cnt + 1
                if "Signal Noise Ratio" in line:
                    break;
            cols = lines[lines_cnt + 6].split("|")
            thr = cols[9]
            thr_values.append(float(thr))
            fr.close()
            thr_float = float(thr);
            sum_thr += thr_float
            max_thr = max([thr_float, max_thr])
            min_thr = min([thr_float, min_thr])
        except IOError:
            print(f"'{in_filename}' does not appear to exist, skipped.")
    mean_thr = sum_thr / n_try
    error_thr = max_thr - min_thr
    if len(thr_values) < 2:
        std = max_thr
    else:
        std = stats.stdev(thr_values)

    fw.write(node_name       + "," +
             sched_short     + "," +
             pinning         + "," +
             str(max_little) + "," +
             str(max_big)    + "," +
             str(n_little)   + "," +
             str(n_big)      + "," +
             str(strat)      + "," +
             str(mean_thr)   + "," +
             str(min_thr)    + "," +
             str(max_thr)    + "," +
             str(error_thr)  + "," +
             str(std)        + "\n");

def produce_csv_for_pgfplot(node_name, R_max, scheds, filename, pinning):
    fw = open(filename, "w")
    fw.write("node,sched,pinning,max_little,max_big,n_little,n_big,strat,thr_mean,thr_min,thr_max,thr_error,thr_std\n")
    if pinning == "os":
        for R in range(1, R_max + 1):
            sched = node_name + "_os_R" + str(R)
            _produce_csv_for_pgfplot(fw, sched, pinning, 15)
    else:
        for sched in scheds:
            _produce_csv_for_pgfplot(fw, sched, pinning, 10)
    fw.close()

for pinning in params.pinning_strategies:
    produce_csv("opi5",  3, params.scheds_opi5,  params.path_postpro + "/" + pinning + "/" + "opi5_scheds.csv",  pinning)
    produce_csv("m1u",   6, params.scheds_m1u,   params.path_postpro + "/" + pinning + "/" + "m1u_scheds.csv",   pinning)
    produce_csv("x7ti",  7, params.scheds_x7ti,  params.path_postpro + "/" + pinning + "/" + "x7ti_scheds.csv",  pinning)
    produce_csv("ai370", 3, params.scheds_ai370, params.path_postpro + "/" + pinning + "/" + "ai370_scheds.csv", pinning)

    produce_csv_for_pgfplot("opi5",  3, params.scheds_opi5,  params.path_postpro + "/" + pinning + "/" + "opi5_scheds_reduced.csv",  pinning)
    produce_csv_for_pgfplot("m1u",   6, params.scheds_m1u,   params.path_postpro + "/" + pinning + "/" + "m1u_scheds_reduced.csv",   pinning)
    produce_csv_for_pgfplot("x7ti",  7, params.scheds_x7ti,  params.path_postpro + "/" + pinning + "/" + "x7ti_scheds_reduced.csv",  pinning)
    produce_csv_for_pgfplot("ai370", 3, params.scheds_ai370, params.path_postpro + "/" + pinning + "/" + "ai370_scheds_reduced.csv", pinning)
