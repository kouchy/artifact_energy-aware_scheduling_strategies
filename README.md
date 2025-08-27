# Dataset and Scripts used for Energy-Aware Scheduling Strategies Article

This repository contains the dataset used for the “Energy-Aware Scheduling 
Strategies for Partially-Replicable Task Chains on Heterogeneous Processors”
article, submitted to the Elsevier Parallel Computing journal. It concerns 
throughput and energy consumption measurements over the open source [SDR DVB-S2 
receiver v1.0.0](https://doi.org/10.5281/zenodo.16966824).

> [!NOTE]
> This repository uses schedules as inputs. If you seek for generating schedules
> you may have a look into the following dedicated repository: [AMP scheduling 
> v2.0](https://doi.org/10.5281/zenodo.16964647).

## 1. Artifact Identification

- **Article's title**: Energy-Aware Scheduling Strategies for 
  Partially-Replicable Task Chains on Heterogeneous Processors
- **Authors' names and affiliations**: 
    * Yacine Idouar - *LIP6, Sorbonne University, CNRS, UMR7606, Paris, France*
    * Adrien Cassagne - *LIP6, Sorbonne University, CNRS, UMR7606, Paris, 
      France*
    * Laércio L. Pilla - *University of Bordeaux, CNRS, Inria, LaBRI, UMR5800, 
      Talence, France*
    * Julien Sopena - *LIP6, Sorbonne University, CNRS, UMR7606, Paris, France*
    * Manuel Bouyer - *LIP6, Sorbonne University, CNRS, UMR7606, Paris, France*
    * Diane Orhan - *University of Bordeaux, CNRS, Inria, LaBRI, UMR5800, 
      Talence, France*
    * Lionel Lacassagne - *LIP6, Sorbonne University, CNRS, UMR7606, Paris, 
      France*
    * Dimitri Galayko - *LIP6, Sorbonne University, CNRS, UMR7606, Paris, 
      France*
    * Denis Barthou - *Bordeaux INP, Talence, France*
    * Christophe Jégo - *University Bordeaux, CNRS, Bordeaux INP, IMS, UMR5218, 
      Talence, France*
- **Abstract**: The arrival of heterogeneous (or hybrid) multicore architectures 
  has brought new performance trade-offs for applications, and efficiency 
  opportunities to systems. They have also increased the challenges related to 
  thread scheduling, as tasks' execution times will vary depending if they are 
  placed on big (performance) cores or little (efficient) ones. In this paper, 
  we focus on the challenges heterogeneous multicore processors bring to 
  partially-replicable task chains, such as the ones that implement digital 
  communication standards in Software-Defined Radio (SDR). Our objective is to 
  maximize the throughput of these task chains while also minimizing their power 
  consumption. We model this problem as a pipelined workflow scheduling problem 
  using pipelined and replicated parallelism on two types of resources whose 
  objectives are to minimize the period and to use as many little cores as 
  necessary. We propose two greedy heuristics (FERTAC and 2CATAC) and one 
  optimal dynamic programming (HeRAD) solution to the problem. We evaluate our 
  solutions and compare the quality of their schedules (in period and resource 
  utilization) and their execution times using synthetic task chains. We also 
  study an open source implementation of the DVB-S2 communication standard based 
  on the StreamPU runtime. Leading processor vendors are covered with ARM, 
  Apple, AMD, and Intel platforms. Both the achieved throughput and the energy 
  consumption are evaluated. Our results demonstrate the benefits and drawbacks 
  of the different proposed solutions. On average, FERTAC and 2CATAC achieve 
  near-optimal solutions, with periods that are less than 10% worse than the 
  optimal (HeRAD) using fewer than 2 extra cores. These three scheduling 
  strategies now enable programmers and users of StreamPU to transparently make 
  use of heterogeneous multicore processors and achieve a throughput that 
  differs from its theoretical maximum by less than 6% on average. On the DVB-S2 
  receiver, it is also shown that the heterogeneous solutions outperform the 
  best homogeneous ones in terms of energy efficiency by 8% on average.

## 2. Artifact Dependencies and Requirements

This code has been tested on systems with the following basic characteristics:

- **Hardware resources**: an ARM or x86_64 processor, few GB of RAM and few MB 
  of storage.
- **Operating systems**: Linux Ubuntu 24.04 LTS and macOS 14.6.1 has been 
  tested.
- **Software libraries needed**: Python 3 with `subprocess`, `argparse`, `sys`,
  `statistics`, and `math` packages.
- **Input datasets**: All the measurements files are already available in the
  artifact. The script to reproduce them is also available in the repository.
- **Output datasets**: All the preprocessed data is also already available in 
  the artifact.

## 3. Artifact Installation and Deployment Process

### Installation

If you download this artifact from Zenodo (directly from the website or using 
`wget`), you will have to decompress the `.zip` file (for instance, using 
`unzip [file]`). You can skip this step if you are downloading this artifact 
from GitHub using `git clone`. You will find the following organization in the 
base folder:

```
├── inputs
│   ├── conso_rapl
│   │   ├── distant
│   │   │   └── [ai370|x7ti]_[2CATAC|FERTAC|HeRAD|OTAC]_*.txt
│   │   ├── guided
│   │   │   └── [ai370|x7ti]_[2CATAC|FERTAC|HeRAD|OTAC]_*.txt
│   │   ├── os
│   │   │   └── [ai370|x7ti]_os_R*.txt
│   │   ├── packed
│   │   │   └── [ai370|x7ti]_[2CATAC|FERTAC|HeRAD|OTAC]_*.txt
│   │   └── [ai370|x7ti]_idle.txt
│   ├── conso_socket
│   │   ├── distant
│   │   │   └── [ai370|m1u|opi5|x7ti]_[2CATAC|FERTAC|HeRAD|OTAC]_*.txt
│   │   ├── guided
│   │   │   └── [ai370|m1u|opi5|x7ti]_[2CATAC|FERTAC|HeRAD|OTAC]_*.txt
│   │   ├── os
│   │   │   └── [ai370|m1u|opi5|x7ti]_os_R*.txt
│   │   ├── packed
│   │   │   └── [ai370|m1u|opi5|x7ti]_[2CATAC|FERTAC|HeRAD|OTAC]_*.txt
│   │   └── [ai370|m1u|opi5|x7ti]_idle.txt
│   ├── schedulings
│   │   ├── distant
│   │   │   └── [ai370|m1u|opi5|x7ti]_[2CATAC|FERTAC|HeRAD|OTAC]_*.json
│   │   ├── guided
│   │   │   └── [ai370|m1u|opi5|x7ti]_[2CATAC|FERTAC|HeRAD|OTAC]_*.json
│   │   ├── loose
│   │   │   └── [ai370|m1u|opi5|x7ti]_[2CATAC|FERTAC|HeRAD|OTAC]_*.json
│   │   ├── packed
│   │   │   └── [ai370|m1u|opi5|x7ti]_[2CATAC|FERTAC|HeRAD|OTAC]_*.json
│   │   └── [ai370|m1u|opi5|x7ti]_results.csv
│   └── throughput
│       ├── distant
│       │   └── [ai370|m1u|opi5|x7ti]_[2CATAC|FERTAC|HeRAD|OTAC]_*.txt
│       ├── guided
│       │   └── [ai370|m1u|opi5|x7ti]_[2CATAC|FERTAC|HeRAD|OTAC]_*.txt
│       ├── loose
│       │   └── [ai370|m1u|opi5|x7ti]_[2CATAC|FERTAC|HeRAD|OTAC]_*.txt
│       ├── os
│       │   └── [ai370|m1u|opi5|x7ti]_os_R*.txt
│       └── packed
│           └── [ai370|m1u|opi5|x7ti]_[2CATAC|FERTAC|HeRAD|OTAC]_*.txt
├── misc
│   ├── frequencies
│   │   └── [ai370|x7ti]_freqs.txt
│   └── profilings
│       └── [ai370|m1u|opi5|x7ti]_dvbs2_profiling.txt
├── outputs
│   ├── 1_postpro
│   │   ├── distant
│   │   │   ├── [ai370|m1u|opi5|x7ti]_scheds.csv
│   │   │   └── [ai370|m1u|opi5|x7ti]_scheds_reduced.csv
│   │   ├── guided
│   │   │   ├── [ai370|m1u|opi5|x7ti]_scheds.csv
│   │   │   └── [ai370|m1u|opi5|x7ti]_scheds_reduced.csv
│   │   ├── loose
│   │   │   ├── [ai370|m1u|opi5|x7ti]_scheds.csv
│   │   │   └── [ai370|m1u|opi5|x7ti]_scheds_reduced.csv
│   │   ├── os
│   │   │   ├── [ai370|m1u|opi5|x7ti]_scheds.csv
│   │   │   └── [ai370|m1u|opi5|x7ti]_scheds_reduced.csv
│   │   └── packed
│   │       ├── [ai370|m1u|opi5|x7ti]_scheds.csv
│   │       └── [ai370|m1u|opi5|x7ti]_scheds_reduced.csv
│   └── 2_postpro_with_conso
│       ├── [ai370|m1u|opi5|x7ti]_scheds.csv
│       └── all_scheds.csv
├── scripts
│   ├── common
│   │   ├── funcs.py
│   │   └── params.py
│   ├── 1_generic_run_scheds.py
│   ├── 2_parse_results.py
│   ├── 3_parse_conso_results.py
│   └── 4_gen_latex_table.py
├── .gitignore
└──  README.md
```

Here is a description of the main folders:
- `inputs`: Schedules and the raw measurements.
- `misc`: Miscellaneous additional data, unused by the scripts, like profilings 
  and frequencies.
- `outputs`: Post processed data from `inputs` and `scripts`.
- `scripts`: Python scripts used to run the code and to transform the raw data 
  (from the `inputs` folder) into post processed data (`outputs` folder).

Sub-folders are used for the different scheduling strategies and pinning 
policies:
- `distant`: Contains OTAC, FERTAC, 2CATAC and HeRAD results for `distant` 
  policy.
- `packed`: Contains OTAC, FERTAC, 2CATAC and HeRAD results for `packed` policy.
- `loose`: Contains OTAC, FERTAC, 2CATAC and HeRAD results for `loose` policy.
- `guided`: Contains OTAC, FERTAC, 2CATAC and HeRAD results for `guided` policy.
- `os`: Contains the OS scheduling results with different values of R (the 
  number of replications).

Scripts are expected to be run from the base folder, and in the lexicographic
order. For instance, to post-process the raw data again, one may do:
```bash
./scripts/2_parse_results.py # will produce the contents of 'outputs/1_postpro'
./scripts/3_parse_conso_results.py # will produce the contents of 'outputs/2_postpro_with_conso'
```

## 4. Reproducibility of Experiments

A detailed description of the experiments and their results is available in the 
article “Energy-Aware Scheduling Strategies for Partially-Replicable Task Chains 
on Heterogeneous Processors”.

Experiments are conducted in two parts: 10 runs of 1 minute to gather the 
throughput, and one run of 1 min 30 seconds to gather the power measurements.

### 4.1 Compiling the DVB-S2 Transceiver

The DVB-S2 has been compiled independently (Ubuntu 24.04) on each platform as 
follow (`[platform_tag]` is a placeholder, see Section 4.3):
```bash
sudo apt install git cmake hwloc libhwloc-dev
git clone https://github.com/aff3ct/dvbs2.git
cd dvbs2/
git checkout v1.0.0
git submodule update --init --recursive
mkdir build_[platform_tag]
cd build_[platform_tag]
cmake .. -G"Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS="-Wall -funroll-loops -march=native" -DSPU_LINK_HWLOC=ON -DDVBS2_LINK_UHD=OFF
make -j16
```
And, this artifact has been unzipped and copied inside the previously cloned 
`dvbs2` folder like as follow:
```bash
cp -r artifact_energy-aware_scheduling_strategies $SOMEWHERE/dvbs2/
```

### 4.2 Generating DVB-S2 Rx Input IQs

To re-run the experiments, the `out_tx.bin` file is missing. It has not been 
added to this repository as it is an heavy binary file containing IQ samples 
(500 MB to 1 GB). To regenerate this file, one may run the following command:
```bash
./bin/dvbs2_tx --sim-stats --rad-type USER_BIN --rad-tx-file-path out_tx.bin -F 8 --src-type USER --src-path ../conf/src/K_14232.src --mod-cod QPSK-S_8/9 --tx-time-limit 1000
```
This is detailed in the 
[README file](https://github.com/aff3ct/dvbs2/tree/v1.0.0?tab=readme-ov-file#testing-tx-and-rx-separately) 
of the DVB-S2 transceiver.

### 4.3 Experimental Platforms

Four different platforms have been tested, identified by a tag:
- `opi5`: Orange Pi 5 Plus with 4 ARM Cortex-A76 cores (big) @ 2.4 GHz and 4 ARM 
  Cortex-A55 cores (little).
- `m1u`: Apple Mac Studio 2022 with 16 Apple Firestorm cores (big) @ 3.2 GHz and 
  4 Apple Icestorm cores (little) @ 2 GHz.
- `ai370`: Minisforum EliteMini AI370 with 4 AMD Zen 5 cores (big) @ 2 GHz and 8 
  AMD Zen 5c cores (little) @ 2 GHz.
- `x7ti`: Minisforum AtomMan X7 Ti with 6 Intel Redwood Cove p-cores (big) @ 
  2.3 GHz, 8 Intel Crestmont e-cores (little) @ 1.8 GHz, and 2 Intel Crestmont 
  LPe-cores @ 1.0 GHz left unused.

### 4.4 Python Script Configuration

Paths and options are defined in the `scripts/common/params/py` file. One may
want to change the `user`. Normally, other paths should be the same and left 
unmodified.

In the `scripts/1_generic_run_scheds.py` file, the path of the IQs should be
updated (line 44-46) according to the real location of this file (see 
Section 4.2). In our experiments, we ran the DVB-S2 on a cluster environment 
and, to avoid extra network traffic, we moved the `out_tx.bin` file on the 
local SSD (`/scratch/[user]/dvbs2` folder).

The Python script comes with the two following command line parameters:
```
usage: run_scheds [-h] [-N NODE] [-S STRATEGY]

options:
  -h, --help            show this help message and exit
  -N, --node NODE       targeted node in ['m1u', 'opi5', 'x7ti', 'ai370'] (default: None)
  -S, --strategy STRATEGY
                        selected strategy in ['packed', 'loose', 'distant', 'guided', 'os'] (default: None)
```

For instance, to run the experiments on the Orange Pi 5 Plus platform and for
the `distant` pinning policy, one may do (from the base DVB-S2 folder):
```bash
cd artifact_energy-aware_scheduling_strategies
./scripts/1_generic_run_scheds.py -N opi5 -S distant
```

### 4.5 Running the DVB-S2 Rx

### 4.5.1 Throughput

For the throughput measurements, on each platform, one may do:
```bash
cd artifact_energy-aware_scheduling_strategies
./scripts/1_generic_run_scheds.py -N [platform_tag] -S distant
./scripts/1_generic_run_scheds.py -N [platform_tag] -S guided
./scripts/1_generic_run_scheds.py -N [platform_tag] -S packed
./scripts/1_generic_run_scheds.py -N [platform_tag] -S loose

# this requires a small modification in the code, explained bellow
./scripts/1_generic_run_scheds.py -N [platform_tag] -S os
```

The previous scripts are saving the raw files in the `inputs/throughput` folder.

`os` scheduling strategy does not expect any pinning from the application. To 
achieve this, you need to modify the DVB-S2 receiver code. Open the 
`dvbs2_root/src/mains/RX/main_sched.cpp` file and at line 20 do:
```cpp
// constexpr bool thread_pinning = true; // <- comment this line
constexpr bool thread_pinning = false; // <- add this line below
```
Then, you need to recompile the code:
```bash
cd build_[platform_tag]
make -j4
```

### 4.5.2 Energy Consumption

For the socket energy consumption, we used a preliminary version of the Dalek's 
measurement platform detailed in the following article: [Dalek 
DOI](https://doi.org/10.48550/arXiv.2508.10481). 
We plan to fully open this hardware in the future. For now, we are still working 
on it and it is not fully ready.

For the SoC energy consumption we used the `powerstat` command line tool. It
is itself based on Intel RAPL technology. We generated the samples with the 
following command line:
```bash
powerstat -cDHRf 2 30
```
The previous command was run directly on the platforms that were executing the
DVB-S2 receiver. In order to limit the probe effect, only one sample every 2 
seconds is generated. This is done 30 times so it takes 1 minutes in total.

For both type of measurements, we manually saved the energy files into the 
`inputs/conso_socket` and `inputs/conso_rapl` folders.
