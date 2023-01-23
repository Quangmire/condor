#!/usr/bin/env python3

import os
import shutil

# Used for template for condor submit scripts
from condor_common import generate

BENCHES = ['spec06']
TYPES = ['1', '2', '3']

# Template for bash script
sh_template='''#!/bin/bash
python3 -u {script_file} --benchmark {benchmark} --hist-len {hist_len} 2>&1
'''

# Iterate over different settings
for benchmark in BENCHES:
    for exp_type in TYPES:
        # Setup initial output directory per experiment
        parent_dir = '/scratch/cluster/qduong/data_prefetching/temporal_pc_predictor/{}/{}'.format(benchmark, exp_type)

        # Create a scripts directory
        scripts_dir = os.path.join(parent_dir, 'scripts')
        os.makedirs(scripts_dir, exist_ok=True)

        # Always good to copy over the version of the script used for the jobs
        shutil.copyfile('pc_predictor.py', os.path.join(scripts_dir, 'pc_predictor.py'))

        # Iterate over all traces in for each experiment
        traces_dir = '/scratch/cluster/qduong/ML-DPC/data/load_traces/' + benchmark
        for fn in os.listdir(traces_dir):
            # Create the bash script
            sh_path = os.path.join(scripts_dir, fn + '.sh')
            with open(sh_path, 'w') as f:
                print(sh_template.format(
                    script_file='scripts/pc_predictor.py',
                    benchmark=traces_dir + '/' + fn,
                    hist_len=exp_type,
                ), file=f)

            # Don't forget to make it executable
            os.chmod(sh_path, 0o777)

            # Generate the associated condor file for this job
            with open(os.path.join(scripts_dir, fn + '.condor'), 'w') as f:
                print(generate(gpu=False, init_dir=parent_dir, err_file=os.path.join(parent_dir, fn + '.ERR'), out_file=os.path.join(parent_dir, fn + '.OUT'), log_file=os.path.join(parent_dir, fn + '.LOG', exe=sh_path), file=f)
