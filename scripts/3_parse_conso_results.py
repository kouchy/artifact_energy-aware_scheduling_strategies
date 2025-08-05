#!/usr/bin/env python3

from math import inf
import statistics as stats
import common.params as params
import common.funcs as funcs

verbose = False
csv_header = "node_name,x_node_name,tag1,tag2,sched,pinning,x_pinning,max_little,max_big,n_little,n_big,strat,sck_v_mean,sck_v_min,sck_v_max,sck_v_std,sck_i_mean,sck_i_min,sck_i_max,sck_i_std,sck_w_mean,sck_w_min,sck_w_max,sck_w_minus,sck_w_plus,sck_w_std,sck_w_idle,sck_j_first,sck_j_last,sck_j_total,rapl_w_mean,rapl_w_min,rapl_w_max,rapl_w_std,rapl_w_idle,thr_mean,thr_min,thr_max,thr_minus,thr_plus,thr_error,thr_std,sck_ene_per_fra,rapl_ene_per_fra\n"
pinning_id = {"loose": 1, "guided": 2, "packed": 3, "distant": 4, "os": 5}

def basic_stats(values, prefix):
    vmean = stats.mean(values)
    vmin = min(values)
    vmax = max(values)
    vstd = stats.stdev(values)
    if verbose:
        print(f"{prefix}mean = {vmean}")
        print(f"{prefix}min = {vmin}")
        print(f"{prefix}max = {vmax}")
        print(f"{prefix}std = {vstd}")
    return vmean, vmin, vmax, vstd

def compute_ene_per_fra(instant_power, throughput_mbps, fra_size):
    throughput_bps = throughput_mbps * 1e6 # thr in bits per second
    throughput_fps = throughput_bps / fra_size # thr in frames per second
    time_of_one_frame = 1 / throughput_fps
    ene_per_fra = time_of_one_frame * instant_power
    return ene_per_fra

def _get_sck_idle_power(node_name, legacy):
    in_filename = params.path_conso_raw + node_name + "_idle.txt"
    sck_w_values = []
    try:
        fr = open(in_filename, "r")
        lines=fr.readlines()
        for line in lines:
            line = line.strip()
            cols = line.split(" ")
            if verbose:
                print(line)
            if legacy:
                w_cur = float(cols[3])
                sck_w_values.append(w_cur)
            else:
                v_cur = float(cols[4].rstrip(cols[4][-1]))
                i_cur = float(cols[5].rstrip(cols[5][-1]))
                w_cur = v_cur * i_cur
                sck_w_values.append(w_cur)
        fr.close()
    except IOError:
        print(f"'{in_filename}' does not appear to exist, skipped.")

    if len(sck_w_values):
        sck_w_mean, sck_w_min, sck_w_max, sck_w_std = basic_stats(sck_w_values, "w_")
        return sck_w_mean
    else:
        return 0

def _get_raple_idle_power(node_name, verbose):
    rapl_filename = params.path_conso_rapl_raw + node_name + "_idle.txt"
    rapl_w_mean, rapl_w_min, rapl_w_max, rapl_w_std = funcs.get_rapl_info(rapl_filename, verbose)
    return rapl_w_mean

def _produce_csv(fw_merged, fw, out_filename, pinning, sched, legacy, n_try):
    x_pinning = pinning_id[pinning]
    if n_try == 0:
        max_try = 1
    else:
        max_try = n_try
    sched_short, max_big, max_little, strat, node_name, n_big, n_little = funcs.get_sched_info(sched, pinning, verbose)
    thr_mean, thr_min, thr_max, thr_error, thr_std = funcs.get_thr_info(node_name, pinning, sched_short, strat, verbose)
    thr_minus = float(thr_mean) - float(thr_min)
    thr_plus = float(thr_max) - float(thr_mean)
    if node_name == "x7ti" or node_name == "ai370":
        rapl_filename = params.path_conso_rapl_raw + pinning + "/" + sched + ".txt"
        rapl_w_mean, rapl_w_min, rapl_w_max, rapl_w_std = funcs.get_rapl_info(rapl_filename, verbose)
    else:
        rapl_w_mean = 0
        rapl_w_min = 0
        rapl_w_max = 0
        rapl_w_std = 0

    tag1 = sched_short + "_" + pinning + "_" + strat
    tag2 = node_name + "_" + sched_short + "_" + strat

    sck_legacy = legacy
    # if node_name == "opi5":
    #     sck_legacy = True
    sck_w_idle = _get_sck_idle_power(node_name, sck_legacy)
    if node_name == "x7ti" or node_name == "ai370":
        rapl_w_idle = _get_raple_idle_power(node_name, verbose)
    else:
        rapl_w_idle = 0

    sck_v_values = []
    sck_i_values = []
    sck_w_values = []
    sck_j_firts = -inf
    sck_j_last = -inf
    for n in range(0, max_try):
        if n_try == 0:
            in_filename = params.path_conso_raw + pinning + "/" + sched + ".txt"
        else:
            in_filename = params.path_conso_raw + pinning + "/" + sched + "_" + str(n) + ".txt"
        try:
            fr = open(in_filename, "r")
            lines=fr.readlines()

            for line in lines:
                line = line.strip()
                cols = line.split(" ")
                if verbose:
                    print(line)

                if legacy:
                    v_cur = float(cols[1])
                    sck_v_values.append(v_cur)
                    i_cur = float(cols[2])
                    sck_i_values.append(i_cur)
                    w_cur = float(cols[3])
                    sck_w_values.append(w_cur)
                else:
                    v_cur = float(cols[4].rstrip(cols[4][-1]))
                    sck_v_values.append(v_cur)
                    i_cur = float(cols[5].rstrip(cols[5][-1]))
                    sck_i_values.append(i_cur)
                    w_cur = v_cur * i_cur
                    sck_w_values.append(w_cur)

                    j_cur = float(cols[6].rstrip(cols[6][-1]))
                    if (sck_j_firts == -inf):
                        sck_j_firts = j_cur

                    if j_cur < sck_j_last:
                        sck_j_last = inf
                    if sck_j_last != inf:
                        sck_j_last = j_cur
            fr.close()
            print(f"Wrote '{sched}' scheduler conso results in '{out_filename}' file.")
        except IOError:
            print(f"'{in_filename}' does not appear to exist, skipped.")

    if len(sck_w_values):
        sck_v_mean, sck_v_min, sck_v_max, sck_v_std = basic_stats(sck_v_values, "v_")
        sck_i_mean, sck_i_min, sck_i_max, sck_i_std = basic_stats(sck_i_values, "i_")
        sck_w_mean, sck_w_min, sck_w_max, sck_w_std = basic_stats(sck_w_values, "w_")
        sck_w_minus = sck_w_mean - sck_w_min
        sck_w_plus = sck_w_max - sck_w_mean
        if legacy:
            sck_j_firts = 0
            sck_j_last = 0
            sck_j_total = 0
        else:
            sck_j_total = sck_j_last - sck_j_firts
        if verbose:
            print(f"j_first = {sck_j_firts}, sck_j_last = {sck_j_last}")
            print(f"sck_j_total = {sck_j_total}")
    else:
        sck_v_mean = 0
        sck_v_min = 0
        sck_v_max = 0
        sck_v_std = 0
        sck_i_mean = 0
        sck_i_min = 0
        sck_i_max = 0
        sck_i_std = 0
        sck_w_mean = 0
        sck_w_min = 0
        sck_w_max = 0
        sck_w_minus = 0
        sck_w_plus = 0
        sck_w_std = 0
        sck_j_firts = 0
        sck_j_last = 0
        sck_j_total = 0

    sck_ene_per_fra = compute_ene_per_fra(float(sck_w_mean), float(thr_mean), 14232)
    rapl_ene_per_fra = compute_ene_per_fra(float(rapl_w_mean), float(thr_mean), 14232)
    x_node_name = params.x[node_name]

    row = node_name             + "," + \
          str(x_node_name)      + "," + \
          tag1                  + "," + \
          tag2                  + "," + \
          sched_short           + "," + \
          pinning               + "," + \
          str(x_pinning)        + "," + \
          str(max_little)       + "," + \
          str(max_big)          + "," + \
          str(n_little)         + "," + \
          str(n_big)            + "," + \
          str(strat)            + "," + \
          str(sck_v_mean)       + "," + \
          str(sck_v_min)        + "," + \
          str(sck_v_max)        + "," + \
          str(sck_v_std)        + "," + \
          str(sck_i_mean)       + "," + \
          str(sck_i_min)        + "," + \
          str(sck_i_max)        + "," + \
          str(sck_i_std)        + "," + \
          str(sck_w_mean)       + "," + \
          str(sck_w_min)        + "," + \
          str(sck_w_max)        + "," + \
          str(sck_w_minus)      + "," + \
          str(sck_w_plus)       + "," + \
          str(sck_w_std)        + "," + \
          str(sck_w_idle)       + "," + \
          str(sck_j_firts)      + "," + \
          str(sck_j_last)       + "," + \
          str(sck_j_total)      + "," + \
          str(rapl_w_mean)      + "," + \
          str(rapl_w_min)       + "," + \
          str(rapl_w_max)       + "," + \
          str(rapl_w_std)       + "," + \
          str(rapl_w_idle)      + "," + \
          str(thr_mean)         + "," + \
          str(thr_min)          + "," + \
          str(thr_max)          + "," + \
          str(thr_minus)        + "," + \
          str(thr_plus)         + "," + \
          str(thr_error)        + "," + \
          str(thr_std)          + "," + \
          str(sck_ene_per_fra)  + "," + \
          str(rapl_ene_per_fra) + "\n"

    fw.write(row);
    fw_merged.write(row);

def produce_csv(fw_merged, node_name, R_max, scheds, out_filename, legacy):
    fw = open(out_filename, "w")
    fw.write(csv_header)
    for pinning in params.pinning_strategies:
        if pinning == "os":
            for R in range (1, R_max + 1):
                sched = node_name + "_os_R" + str(R)
                if node_name == "m1u":
                    _produce_csv(fw_merged, fw, out_filename, pinning, sched, legacy, 5)
                else:
                    _produce_csv(fw_merged, fw, out_filename, pinning, sched, legacy, 0)
        else:
            for sched in scheds:
                _produce_csv(fw_merged, fw, out_filename, pinning, sched, legacy, 0)
    fw.close()

fw_merged = open(params.path_conso_postpro + "all_scheds.csv", "w")
fw_merged.write(csv_header)

produce_csv(fw_merged, "m1u",   6, params.scheds_m1u,   params.path_conso_postpro + "m1u_scheds.csv",   True )
produce_csv(fw_merged, "opi5",  3, params.scheds_opi5,  params.path_conso_postpro + "opi5_scheds.csv",  False)
produce_csv(fw_merged, "x7ti",  7, params.scheds_x7ti,  params.path_conso_postpro + "x7ti_scheds.csv",  False)
produce_csv(fw_merged, "ai370", 3, params.scheds_ai370, params.path_conso_postpro + "ai370_scheds.csv", False)

fw_merged.close()
