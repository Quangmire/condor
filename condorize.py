#!/usr/bin/env python3

from argparse import ArgumentParser
import datetime as dt
import os
import sys

CONDOR_TEMPLATE = (
'''#!/bin/bash
# Automatically generated with {condorize_file}
# Created by {user} at {timestamp}
# With command {condorize_cmd}
# In directory: {pwd}

+Group="GRAD"
+Project="ARCHITECTURE"
+ProjectDescription="Architectural Simulation"

universe=vanilla
getenv=true
Rank=Memory
notification=Error
notify_user={user}@cs.utexas.edu
error={name}.CONDOR.ERR
output={name}.CONDOR.OUT
log={name}.CONDOR.LOG
initial_dir={directory}
executable={binary}

requirements={requirements}

queue
'''
)

def get_args():
    parser = ArgumentParser()
    parser.add_argument('--directory', required=True, help='Directory to store results / script files')
    parser.add_argument('--name', required=True, help='Job name')
    parser.add_argument('--binary', required=True, help='Binary / script to run')
    parser.add_argument('--gpu', action='store_true', help='Whether or not to require a GPU')
    parser.add_argument('--ram', type=int, default=None, help='Minimum RAM requirements in GB')
    parser.add_argument('--dry-run', action='store_true', help='Print output condor file only')
    return parser.parse_args()

def main(args=None):
    if args is None:
        return

    template_vars = {
        'condorize_file': os.path.abspath(sys.argv[0]),
        'condorize_cmd': ' '.join(sys.argv),
        'user': os.getlogin(),
        'timestamp': dt.datetime.now().strftime('%m/%d/%Y %H:%M:%S'),
        'pwd': os.path.abspath(os.getcwd()),
        'directory': args.directory,
        'binary': args.binary,
        'name': args.name,
    }

    # Note that GPU and RAM settings aren't used simultaneously
    if args.gpu:
        template_vars['requirements'] = 'Cuda8 && TARGET.GPUSlot \nrequest_GPUs=1\n+GPUJob=true && NumJobStarts == 0'
    elif args.ram is not None:
        template_vars['requirements'] = 'InMastodon\nrequest_memory=' + str(args.ram) + ' GB'
    else:
        template_vars['requirements'] = 'InMastodon'

    if args.dry_run:
        print(CONDOR_TEMPLATE.format(**template_vars))
    else:
        # Create output directory if it doesn't exist
        if not os.path.isdir(args.directory):
            os.mkdir(args.directory)

        # Create scripts directory for storing condor file (and possibly the script / binary)
        if not os.path.isdir(os.path.join(args.directory, 'scripts')):
            os.mkdir(os.path.join(args.directory, 'scripts'))

        # Create the condor file
        with open(os.path.join(args.directory, 'scripts', args.name + '.condor'), 'w') as f:
            f.write(CONDOR_TEMPLATE.format(**template_vars))

if __name__ == '__main__':
    main(args = get_args())
