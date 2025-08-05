import re
import json
import csv

import common.params as params

def get_rapl_info(txt_filename, verbose):
    rapl_mean = 0
    rapl_min = 0
    rapl_max = 0
    rapl_std = 0
    try:
        raplfile = open(txt_filename, "r")
        rapllines = raplfile.readlines()
        for line in rapllines:
            if "Average" in line or "Minimum" in line or "Maximum" in line or "StdDev" in line:
                line = line.strip()
                cols = line.split(" ")
                cols = list(filter(None, cols))
                # print(cols)
                if "Average" in line:
                    rapl_mean = cols[9]
                if "Minimum" in line:
                    rapl_min = cols[9]
                if "Maximum" in line:
                    rapl_max = cols[9]
                if "StdDev" in line:
                    rapl_std = cols[9]

    except IOError:
            print(f"'{txt_filename}' does not appear to exist, skipped.")

    return rapl_mean, rapl_min, rapl_max, rapl_std

def get_thr_info(node_name, pinning, sched_short, strat, verbose):
    csv_filename = params.path_postpro + pinning + "/" + node_name + "_scheds_reduced.csv"
    thr_mean = 0
    thr_min = 0
    thr_max = 0
    thr_error = 0
    thr_std = 0
    try:
        reader = csv.reader(open(csv_filename, 'r'), delimiter=',')
        d = {}
        first_time = True
        for row in reader:
            if first_time:
                i = 0
                for c in row:
                    d[c] = i
                    i = i + 1
            else:
                if row[d["sched"]] == sched_short and row[d["strat"]] == strat:
                    thr_mean = row[d["thr_mean"]]
                    thr_min = row[d["thr_min"]]
                    thr_max = row[d["thr_max"]]
                    thr_error = row[d["thr_error"]]
                    thr_std = row[d["thr_std"]]
                    break;
            first_time = False
    except IOError:
            print(f"'{csv_filename}' does not appear to exist, skipped.")

    return thr_mean, thr_min, thr_max, thr_error, thr_std

def get_sched_info(sched, pinning, verbose):
    if pinning == "os":
        max_big = 0
        max_little = 0
    else:
        search = re.search('_([1-9]+)big', sched, re.IGNORECASE)
        if search:
            max_big = int(search.group(1))
            if verbose:
                print(f"max_big = {max_big}")
        else:
            print(f"This should not happen, exiting (sched = {sched}).")
            sys.exit(-1)
        search = re.search('_([1-9]+)little', sched, re.IGNORECASE)
        if search:
            max_little = int(search.group(1))
            if verbose:
                print(f"max_little = {max_little}")
        else:
            print(f"This should not happen, exiting (sched = {sched}).")
            sys.exit(-1)

    if pinning == "os":
        sched_short = "OS"
        search = re.search('_os_R([0-9])', sched, re.IGNORECASE)
        if search:
            sched_short = sched_short + "_R" + search.group(1)
        else:
            print(f"This should not happen, exiting (sched = {sched}).")
    else:
        search = re.search('_([a-zA-Z0-9]+_little)_[1-9]', sched, re.IGNORECASE)
        if search:
            sched_short = search.group(1)
        else:
            search = re.search('_([a-zA-Z0-9]+_big)_[1-9]', sched, re.IGNORECASE)
            if search:
                sched_short = search.group(1)
            else:
                search = re.search('_([a-zA-Z0-9]+)_[1-9]', sched, re.IGNORECASE)
                if search:
                    sched_short = search.group(1)
                else:
                    print(f"This should not happen, exiting (sched = {sched}).")
                    sys.exit(-1)
        if verbose:
            print(f"sched_short = {sched_short}")

    search = re.search(f'^([a-zA-Z0-9]+)_', sched, re.IGNORECASE)
    if search:
        node_name = search.group(1)
    else:
        search = re.search(f'^([a-zA-Z0-9]+\-[a-zA-Z0-9]+)_', sched, re.IGNORECASE)
        if search:
            node_name = search.group(1)
        else:
            print(f"This should not happen, exiting (sched = {sched}).")
            sys.exit(-1)
    if verbose:
        print(f"node_name = {node_name}")

    strat = "unknown"
    if max_little == params.resources[node_name][0] and max_big == params.resources[node_name][1]:
        strat = "full"
    if max_little == params.resources[node_name][0] / 2 and max_big == params.resources[node_name][1] / 2:
        strat = "half"
    if verbose:
        print(f"strat = {strat}")

    if (pinning == "os"):
        n_big = 0
        n_little = 0
    else:
        n_big = 0
        n_little = 0
        jsonfilename = f"{params.path_schedulings}{pinning}/{sched}.json"
        try:
            with open(jsonfilename) as jsched:
                d = json.load(jsched)
                # print(d)
                for s in d["schedule"]:
                    if "core-type" in s:
                        if s["core-type"] == "e-core":
                            n_little = n_little + int(s["threads"])
                        if s["core-type"] == "p-core":
                            n_big = n_big + int(s["threads"])
        except IOError:
            print(f"'{jsonfilename}' does not appear to exist, skipped.")

    return sched_short, max_big, max_little, strat, node_name, n_big, n_little