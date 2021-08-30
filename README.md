# UT Austin CS HTCondor Scripts and Notes

More info on the cluster [https://www.cs.utexas.edu/facilities/documentation/condor](https://www.cs.utexas.edu/facilities/documentation/condor)

# Important Notes

There are two dedicated submit nodes: darmok.cs.utexas.edu and
jalad.cs.utexas.edu. Either are fine for submitting jobs to the cluster.

The GPU-equipped machines on the cluster are the eldar machines. They are
numbered from 1 to 50 (eldar-1.cs.utexas.edu ... eldar-50.cs.utexas.edu). Both
eldar-1 and eldar-11 are for testing your scripts before submitting to the
cluster and you can SSH to them as a result.

Each of the eldar machines have two available GPUs. All of the scripts in this
repository only request 1 GPU (and I have never needed / tried to request the
second, so I don't know if that works). As a result, you will generally be
running on a machine that could be running someone else's GPU job. Make sure
that you don't exceed the RAM / overwhelm the CPU of the eldar machines or you
could crash the machine and possibly kill someone else's job. To prevent this,
just test it on eldar-1 and eldar-11 first and be wary of RAM and CPU usage.

In the interest of fairness, I recommend using 20 GPU jobs at most at a time
during the year unless absolutely no one else has been using the GPUs for
awhile. Other students / faculty may become disgruntled otherwise.

In addition, always make sure to check how many GPUs are available using the
`gpu_idle` alias provided in `condor.sh` to make sure that you do not submit
more jobs than there are available GPUs (which could idle the jobs of other
students / faculty if you have lower priority) out of courtesy.

# Included Convenience Scripts

## `condor.sh`

Source in your `.bashrc` for some convenient commands. See the file for more
information on each of the commands / aliases.

It also contains set-up necessary for running TensorFlow 2 which requires
`libcudnn.so.8` which isn't available on these machines by default. I installed
it in my scratch directory from
[https://developer.nvidia.com/rdp/cudnn-download](https://developer.nvidia.com/rdp/cudnn-download).

## `condor_submit_batch.py`

Submits a batch of jobs from a file that contains condor submit files, one per
line. It sets the batch name (or job name effectively) to be the name of the
condor submit file sans the extension. You can also differentiate different
experiments that have the same condor submit file names using `--exp-name`.

Example:

```
python3 condor_submit_batch.py my_jobs 20 15
```

The above command will submit 15 jobs starting on line 20 (namely lines 20 - 34)

## `condorize.py`

Sets up a basic condor output directory / condor submit script for a given
binary or executable. I prefer a more programmatic approach as seen in
`condor_pc.py` as an example, since it generates all of the jobs given a certain
template.

## `condor_pc.py` and `condor_common.py`

Example code for how I normally create all the files necessary to submit a bunch
of jobs on condor.

The workflow comes out to be:

1. Create a file like `condor_pc.py` for the current experiment
2. Run it to generate all of the necessary condor job files
3. Extract all of that into a job file:

    ```
    find exp_directory -name '*condor' > job_files
    ```

4. Submit them via `condor_submit_batch`:

    ```
    condor_submit_batch job_files 0 27
    ```

# Basic Condor Commands

## `condor_q`

Shows the current status of your jobs (or other people's jobs if `-g -allusers`
is provided.

More information can be required using `-long` or `-xml` or `-json` in
conjunction with using `-attributes A,B,C,...` where you can get a slightly
outdated attribute list from
[https://research.cs.wisc.edu/htcondor/manual/v7.8/11_Appendix_A.html](https://research.cs.wisc.edu/htcondor/manual/v7.8/11_Appendix_A.html)

## `condor_submit`

Submits the given condor submit file. You can name the batch / job using the
`-batch-name` argument to help you discern which is which.

## `condor_rm`

Removes job(s) from the condor job queue. You can either specify the `JOB_ID` as
shown in `condor_q` or you can remove all of your jobs with `-all`.

## `condor_userprio`

Displays the current user priorities of users who recently submitted / are
currently running jobs. Note that anyone who has lower priority has the
possibility of preempting your jobs back into being idle (where they will
remain and as far as I can tell cannot be resumed using condor).

Furthermore, GPU jobs increase your priority 6 times as much as regular CPU
jobs.
