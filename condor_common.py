CONDOR_GPU = """
+Group="GRAD"
+Project="ARCHITECTURE"
+ProjectDescription="Architectural Simulation"

universe=vanilla
getenv=true
Rank=Memory
notification=Error
notify_user=qduong@cs.utexas.edu
error={err_file}
output={out_file}
initial_dir={init_dir}
executable={exe}

requirements=Cuda8 && TARGET.GPUSlot 
request_GPUs=1
+GPUJob=true && NumJobStarts == 0

queue
"""

CONDOR_CPU = """
+Group="GRAD"
+Project="ARCHITECTURE"
+ProjectDescription="Architectural Simulation"

universe=vanilla
getenv=true
Rank=Memory
notification=Error
notify_user=qduong@cs.utexas.edu
error={err_file}
output={out_file}
initial_dir={init_dir}
executable={exe}

queue
"""

def generate(gpu=False, **params):
    base = CONDOR_GPU if gpu else CONDOR_CPU
    return base.format(**params)
