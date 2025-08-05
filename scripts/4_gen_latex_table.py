#!/usr/bin/env python3

from math import inf
import statistics as stats
import common.params as params
import common.funcs as funcs
import csv

scheds_print_order = ["OTAC_little", "OTAC_big", "FERTAC", "2CATAC", "HeRAD"]
real_node_names = { "m1u": "Mac Studio", "ai370": "AI370", "x7ti": "X7 Ti", "opi5": "Orange Pi 5+" }
frames_per_stream = { "m1u": 4, "ai370": 16, "x7ti": 8, "opi5": 4 }
real_sched_names = { "OTAC_little": "\\otac[L]", "OTAC_big": "\\otac[B]", "2CATAC": "\\twocatac", "FERTAC": "\\fertac", "HeRAD": "\\herad" }

def _get_real_mbps(node_name, sched, pinning, strat):
    in_filename = params.path_postpro + pinning + "/" + node_name + "_scheds_reduced.csv"
    thr_mean = 0;
    try:
        fr = open(in_filename, "r")
        reader = csv.reader(fr, delimiter=',')

        d = {}
        first_time = True
        for row in reader:
            if first_time:
                i = 0
                for c in row:
                    d[c] = i
                    i = i + 1
                first_time = False
            else:
                if row[d["sched"]] == sched and row[d["pinning"]] == pinning and row[d["strat"]] == strat:
                    thr_mean = float(row[d["thr_mean"]])
                    break
        fr.close()
    except IOError:
        print(f"'{in_filename}' does not appear to exist, skipped.")

    return thr_mean

def _get_power(node_name, sched, pinning, strat):
    in_filename = params.path_conso_postpro + node_name + "_scheds.csv"
    sck_w_mean = 0;
    sck_ene_per_fra = 0;
    try:
        fr = open(in_filename, "r")
        reader = csv.reader(fr, delimiter=',')

        d = {}
        first_time = True
        for row in reader:
            if first_time:
                i = 0
                for c in row:
                    d[c] = i
                    i = i + 1
                first_time = False
            else:
                if row[d["sched"]] == sched and row[d["pinning"]] == pinning and row[d["strat"]] == strat:
                    sck_w_mean = float(row[d["sck_w_mean"]])
                    sck_ene_per_fra = float(row[d["sck_ene_per_fra"]])
                    break
        fr.close()
    except IOError:
        print(f"'{in_filename}' does not appear to exist, skipped.")

    return sck_w_mean, sck_ene_per_fra

def _print_sched_row(node_name, tag, data, first, sid):
    if first:
        print("& \\multirow{5}{*}{$(" + str(data[tag]["max_big"]) + "_{\\mathcal{B}}," + str(data[tag]["max_little"]) + "_{\\mathcal{L}})$} & ", end='')
    else:
        print("& & ", end='')

    print("$\\mathcal{S}_{" + str(sid) + "}$ & ", end='')
    print(real_sched_names[data[tag]["sched"]] + " & ", end='')

    print("$", end='')
    for s in range(0, len(data[tag]["tasks_per_stage"])):
        if data[tag]["types_per_stage"][s] == "Little":
            sta = "\\StaL"
        else:
            sta = "\\StaB"
        if float(data[tag]["loads_per_stage"][s]) == data[tag]["period"]:
            sta = sta + "[h]"
        if s > 0:
            print(",", end='')
        print(sta + "{" + data[tag]["tasks_per_stage"][s] + "}{" + data[tag]["resources_per_stage"][s] + "}", end='')
    print("$ & ", end='')
    print("$" + str(len(data[tag]["tasks_per_stage"])) + "$ & ", end='')

    print("$" + str(data[tag]["n_big"]) + "$ & ", end='')
    print("$" + str(data[tag]["n_little"]) + "$ & ", end='')

    formatted_period = f"{float(data[tag]["period"])/100:.1f}"
    print("$" + formatted_period + "$ & ", end='')

    real_mbps = _get_real_mbps(node_name, data[tag]["sched"], "packed", data[tag]["strat"]);

    sim_FPS = (1.0 / (float(data[tag]["period"])*1e-8)) * frames_per_stream[node_name]
    # formatted_sim_FPS = f"{float(sim_FPS):.1f}"
    # print("$" + formatted_sim_FPS + "$ & ", end='')

    real_FPS = ((real_mbps * 1e6) / 14232)
    # formatted_real_FPS = f"{float(real_FPS):.1f}"
    # print("$" + formatted_real_FPS + "$ & ", end='')

    sim_mbps = (14232 / (float(data[tag]["period"])/100)) * frames_per_stream[node_name]
    formatted_sim_mbps = f"{float(sim_mbps):.1f}"
    print("$" + formatted_sim_mbps + "$ & ", end='')

    formatted_real_mbps = f"{float(real_mbps):.1f}"
    print("$" + formatted_real_mbps + "$ & ", end='')

    diff_mbps = sim_mbps - real_mbps
    formatted_diff_mbps = f"{float(diff_mbps):.1f}"
    if diff_mbps > 0:
        print("$+" + formatted_diff_mbps + "$ & ", end='')
    else:
        print("$" + formatted_diff_mbps + "$ & ", end='')

    if sim_FPS > real_FPS:
        ratio = int(((sim_FPS / real_FPS) - 1)*100)
        print("$+" + str(ratio) + "$\\% & ", end='')
    else:
        ratio = int(((real_FPS / sim_FPS) - 1)*100)
        print("$-" + str(ratio) + "$\\% & ", end='')

    sck_w_mean, sck_ene_per_fra = _get_power(node_name, data[tag]["sched"], "packed", data[tag]["strat"]);

    formatted_sck_pow = f"{float(sck_w_mean):.1f}"
    print("$" + formatted_sck_pow + "$ & ", end='')

    sck_ene_per_fra = sck_ene_per_fra * 1000
    formatted_sck_ene = f"{float(sck_ene_per_fra):.1f}"
    print("$" + formatted_sck_ene + "$ ", end='')

    print("\\\\")
    return 0

def print_schedulings(node_name, sid):
    csv_filename = params.path_schedulings + node_name + "_results.csv"
    # print(csv_filename)
    try:
        fr = open(csv_filename, "r")
        reader = csv.reader(fr, delimiter=',')
        data = {}
        d = {}
        first_time = True
        for row in reader:
            if first_time:
                i = 0
                for c in row:
                    d[c] = i
                    i = i + 1
                first_time = False
            else:
                sched = row[d["algorithm"]]
                max_big = int(row[d["big resources"]])
                max_little = int(row[d["little resources"]])
                n_tasks = int(row[d["number of tasks"]])
                n_big = int(row[d["big used"]])
                n_little = int(row[d["little used"]])
                period = float(row[d["period"]])
                tasks_per_stage = row[d["tasks per stage"]].split("|")
                resources_per_stage = row[d["resources per stage"]].split("|")
                types_per_stage = row[d["types of resources"]].split("|")
                loads_per_stage = row[d["load per stage"]].split("|")

                strat = "unknown"
                if max_little == params.resources[node_name][0] and max_big == params.resources[node_name][1]:
                    strat = "full"
                if max_little == params.resources[node_name][0] / 2 and max_big == params.resources[node_name][1] / 2:
                    strat = "half"

                tag = sched + "_" + strat
                data[tag] = {}
                data[tag]["sched"] = sched
                data[tag]["max_big"] = max_big
                data[tag]["max_little"] = max_little
                data[tag]["n_tasks"] = n_tasks
                data[tag]["n_big"] = n_big
                data[tag]["n_little"] = n_little
                data[tag]["period"] = period
                data[tag]["tasks_per_stage"] = tasks_per_stage
                data[tag]["resources_per_stage"] = resources_per_stage
                data[tag]["types_per_stage"] = types_per_stage
                data[tag]["loads_per_stage"] = loads_per_stage
                data[tag]["strat"] = strat

        print("\\midrule")
        print("\\multirow{11}{*}{\\rotatebox[origin=c]{90}{" + real_node_names[node_name] + "}}")
        first = True
        for sched in scheds_print_order:
            _print_sched_row(node_name, sched + "_half", data, first, sid)
            first = False
            sid = sid + 1
        print("\\addlinespace")
        first = True
        for sched in scheds_print_order:
            _print_sched_row(node_name, sched + "_full", data, first, sid)
            sid = sid + 1
            first = False

        fr.close()
    except IOError:
            print(f"'{csv_filename}' does not appear to exist, skipped.")

    return sid

print("\\begin{tabular}{l c r l l l r r r r r r r r r r}")
print("\\toprule")
print("& \\multicolumn{1}{c}{} & \\multicolumn{7}{c}{Solution} & \\multicolumn{4}{c}{Info. Throughput (Mb/s)} & \\multicolumn{2}{c}{Socket Cons.} \\\\")
print("\\cmidrule(lr){3-9} \\cmidrule(lr){10-13} \\cmidrule(lr){14-15}")
print("&             &    &          &                                                                                                          &                 &                  &                  &    Period &      &      &       &       & Power & $\\mathcal{E}$ / fra. \\\\")
print("& $R = (b,l)$ & Id & Strategy & Pipeline decomposition where a stage is $(n^{\\text{tasks}},r_{v \\in \\{\\mathcal{L},\\mathcal{B}\\}})$ & $|\\mathsf{s}|$ & $b_\\text{used}$ & $l_\\text{used}$ & ($\\mu$s) & Sim. & Real & Diff. & Ratio &   (W) &                  (mJ) \\\\")
sid = 1
sid = print_schedulings("opi5",  sid)
sid = print_schedulings("m1u",   sid)
sid = print_schedulings("ai370", sid)
sid = print_schedulings("x7ti",  sid)

print("\\bottomrule")
print("\\end{tabular}")
