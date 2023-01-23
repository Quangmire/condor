################################################################################
#                                                                              #
#                          CONVENIENT CONDOR COMMANDS                          #
#                                                                              #
################################################################################

# Note that this won't always work outside of BASH
CONDOR_SCRIPTS_DIR=`dirname $(realpath $0)`
alias cpu_idle="condor_status | grep -v -E 'eldar|nandor' | grep Idle | wc -l"

# Prints the number of idle GPU machines
alias gpu_idle="condor_status | grep -E 'eldar|nandor' | grep Idle | wc -l"

# Prints who is using the GPUs and how many
alias gpu_who="condor_q -g -allusers -long -attribute RemoteHost,Owner | grep -B 1 -E 'eldar|nandor' | grep Owner | awk '{print \$3}' | sed -e 's:\"::g' | sort | uniq -c"

# Get the executables for the idle GPU jobs
# Useful for restarting jobs that have been idled due to another user (with a
# lower priority) submitting more jobs than there are available GPUs
alias gpu_idle_cmd="condor_q -long -attribute Cmd,JobStatus | grep -B 1 'JobStatus = 1' | grep Cmd | awk '{print \$3}' | sed -e 's:\"::g'"

# I tend to name the shell script associated with the condor submit file the
# same, so getting the condor scripts would be easy as one replace
alias gpu_idle_condor="gpu_idle_cmd | sed -e 's:.sh$:.condor:'"

# Takes a text file containing one condor submit file per line, the start index,
# and the number of jobs to send up
#
# Example: condor_submit_batch my_jobs 20 15
#          This will submit the jobs on lines 20 - 34
#
# You can also differentiate different experiments that have condor submit files
# with the same name using --exp-name
alias condor_submit_batch="python3 $CONDOR_SCRIPTS_DIR/condor_submit_batch.py"

alias condorize="python3 $CONDOR_SCRIPTS_DIR/condorize.py"

alias prio="condor_userprio -g -allusers | awk -v user=\$USER '{if (\$1 ~ user || (\$2 != \"500.00\" && \$2 != \"1.00\")) {print \$0}}'"

alias chkquota-scratch="$CONDOR_SCRIPTS_DIR/chkquota-scratch $USER"

get_improve() {
    grep improved $1 | tail -n1 | awk '{print $2 " " $8}' | sed -e 's/://g' -e 's/,//g'
}

get_epoch() {
    grep '\[test\] Epoch' $1 | tail -n1 | awk '{print $3}'
}

################################################################################
#                                                                              #
#                                  GPU SETUP                                   #
#                                                                              #
################################################################################

# Needed for using GPUs with TensorFlow 2
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/scratch/cluster/qduong/cuda/lib64
export CUDA_HOME=/scratch/cluster/qduong/cuda
