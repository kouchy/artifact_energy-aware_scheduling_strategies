# Dataset and Scripts

This repository contains the dataset used for the "*Energy-Aware Scheduling 
Strategies for Partially-Replicable Task Chains on Heterogeneous Processors*"
article, submitted to the Elsevier Parallel Computing journal. It concerns 
throughput and energy consumption measurements over the open source SDR DVB-S2 
receiver ([https://github.com/aff3ct/dvbs2](https://github.com/aff3ct/dvbs2), 
commit xxxxxxx).

It contains the following folders:
- `input`: Schedules and the raw measurements
- `output`: Post processed data from `input` and `scripts`
- `scripts`: Python scripts used to run the code and to transform the raw data 
  (from the `input` folder) into post processed data (`output` folder)
- `data`: Small additional data, unused by the scripts, like profilings and 
  frequencies

Scripts are expected to be run from the root folder, and in the lexicographic
order. For instance, to post-process the raw data again, one may do:
```bash
./scripts/2_parse_results.py
./scripts/3_parse_conso_results.py
```

File names have different prefixes depending on the platform where they have
been run:
- `opi5`: Orange Pi 5 Plus
- `m1u`: Apple Mac Studio 2022 with M1 Ultra CPU
- `ai370`: Minisforum EliteMini AI370
- `x7ti`: Minisforum AtomMan X7 Ti

Sub-folders are used for the different scheduling strategies and pinning 
policies:
- `distant`: Contains OTAC, FERTAC, 2CATAC and HeRAD results for `distant` 
  policy
- `packed`: Contains OTAC, FERTAC, 2CATAC and HeRAD results for `packed` policy
- `loose`: Contains OTAC, FERTAC, 2CATAC and HeRAD results for `loose` policy
- `guided`: Contains OTAC, FERTAC, 2CATAC and HeRAD results for `guided` policy
- `os`: Contains the OS scheduling results with different values of R (the 
  number of replications)

To re-run the experiments, the `out_tx.bin` file will be missing. It has not 
been added to this repository as it is an heavy binary file containing IQ
samples. To regenerate this file, one may run the following command:
```bash
./bin/dvbs2_tx --sim-stats --rad-type USER_BIN --rad-tx-file-path out_tx.bin -F 8 --src-type USER --src-path ../conf/src/K_14232.src --mod-cod QPSK-S_8/9 --tx-time-limit 1000
```
This is detailed in the 
[README file](https://github.com/aff3ct/dvbs2?tab=readme-ov-file#testing-tx-and-rx-separately) 
of the DVB-S2 transceiver.