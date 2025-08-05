#!/usr/bin/env python3

import subprocess
import argparse
import sys

import common.params as params

parser = argparse.ArgumentParser(prog='run_scheds',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-N', '--node',
                    action='store',
                    dest='node',
                    type=str,
                    required=False,
                    help=f'targeted node in {params.nodes}')

parser.add_argument('-S', '--strategy',
                    action='store',
                    dest='strategy',
                    type=str,
                    required=False,
                    help=f'selected strategy in {params.pinning_strategies}')

args = parser.parse_args()

if args.node not in params.nodes:
  print(f"(EE) Unsupported node type ({args.node})")
  parser.print_help()
  sys.exit(1)

if args.strategy not in params.pinning_strategies:
  print(f"(EE) Unsupported strategy ({args.strategy})")
  parser.print_help()
  sys.exit(1)

# CONFIG ######################################################################
n_exe_per_sched     = 10
n_exe_per_sched_os  = 15
path_dvbs2_exe      = f"../build_{args.node}/bin/dvbs2_rx_sched"
path_scheds_pinning = f"{params.path_schedulings}{args.strategy}/"
path_raw_pinning    = f"{params.path_raw}{args.strategy}/"
path_input_iqs      = f"/scratch/{params.user}-nfs/dvbs2/out_tx.bin"
if (args.node in ["iml-ia770", "ai370"]):
    path_input_iqs  = f"/scratch/{params.user}/dvbs2/out_tx.bin"
###############################################################################

def run_schedulings(scheds, n_frames):
    for sched in scheds:
        run_cmd = [path_dvbs2_exe,
               '--sim-stats',
               '--src-type', 'USER',
               '--src-path', params.path_conf_file,
               '--rad-type', 'USER_BIN',
               '--rad-rx-file-path', path_input_iqs,
               '-F', str(n_frames),
               '--mod-cod', 'QPSK-S_8/9',
               '--dec-implem', 'NMS',
               '--dec-ite', '10',
               '--dec-simd', 'INTER',
               '--snk-path', '/dev/null',
               '-T', 'FILE',
               '-J', path_scheds_pinning + sched + '.json',
               '-P', '100',
               '--rx-time-limit', '60000']

        print("Current sched is: " + sched);
        print("Command line is:", end=" ")
        for p in run_cmd:
            print(p, end=" ")
        print("")

        for i in range(0, n_exe_per_sched):
            print(" - running exe n°" + str(i) + "...", end=" ", flush=True)

            process = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            output = str(process.communicate()[0])

            lines = output.split("\\n");
            f = open(path_raw_pinning + sched + "_" + str(i) + ".txt", "w")
            for line in lines:
                f.write(line + "\n")
            f.close()
            print("Done!")

def run_os(R_max, n_frames):
    for R in range(1,R_max+1):
        run_cmd = [path_dvbs2_exe,
               '--sim-stats',
               '--src-type', 'USER',
               '--src-path', path_conf_file,
               '--rad-type', 'USER_BIN',
               '--rad-rx-file-path', path_input_iqs,
               '-F', str(n_frames),
               '--mod-cod', 'QPSK-S_8/9',
               '--dec-implem', 'NMS',
               '--dec-ite', '10',
               '--dec-simd', 'INTER',
               '--snk-path', '/dev/null',
               '-T', 'GR',
               '-R', str(R),
               '-P', '100',
               '--rx-time-limit', '60000']

        print("Current sched is: OS");
        print("Command line is:", end=" ")
        for p in run_cmd:
            print(p, end=" ")
        print("")

        for i in range(0, n_exe_per_sched_os):
            print(" - running exe n°" + str(i) + "...", end=" ", flush=True)

            process = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            output = str(process.communicate()[0])

            lines = output.split("\\n");
            f = open(path_raw_pinning + args.node + "_os_R" + str(R) + "_" + str(i) + ".txt", "w")
            for line in lines:
                f.write(line + "\n")
            f.close()
            print("Done!")

if (args.node == "m1u"):
    n_frames = 4
if (args.node == "opi5"):
    n_frames = 4
if (args.node == "x7ti"):
    n_frames = 8
if (args.node == "ai370"):
    n_frames = 16

if args.strategy == "os":
    if (args.node == "m1u"):
        R_max = 6
        run_os(R_max, n_frames)
    if (args.node == "opi5"):
        R_max = 3
        run_os(R_max, n_frames)
    if (args.node == "x7ti"):
        R_max = 7
        run_os(R_max, n_frames)
    if (args.node == "ai370"):
        R_max = 3
        run_os(R_max, n_frames)
else:
    if (args.node == "m1u"):
        run_schedulings(params.scheds_m1u, n_frames)
    if (args.node == "opi5"):
        run_schedulings(params.scheds_opi5, n_frames)
    if (args.node == "x7ti"):
        run_schedulings(params.scheds_x7ti, n_frames)
    if (args.node == "ai370"):
        run_schedulings(params.scheds_ai370, n_frames)
