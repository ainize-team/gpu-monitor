import os
from typing import List
from dataclasses import dataclass, field
from subprocess import Popen, PIPE


@dataclass
# pylint: disable=line-too-long
class GPUInformation:
    """
    Information About GPU
    """

    index: int = field(metadata={"help": "Zero based index of the GPU. Can change at each boot."})
    gpu_name: str = field(
        metadata={
            "help": "The official product name of the GPU. This is an alphanumeric string. For all products."
        }
    )
    gpu_bus_id: str = field(
        metadata={"help": 'PCI bus id as "domain:bus:device.function", in hex.'}
    )
    gpu_temperature: int = field(metadata={"help": "Core GPU temperature. in degrees C."})
    gpu_utilization: int = field(
        metadata={
            "help": "Percent of time over the past sample period during which one or more kernels was executing on the GPU. The sample period may be between 1 second and 1/6 second depending on the product."
        }
    )
    memory_temperature: int = field(metadata={"help": "HBM memory temperature. in degrees C."})
    memory_utilization: int = field(
        metadata={
            "help": "Percent of time over the past sample period during which global (device) memory was being read or written. The sample period may be between 1 second and 1/6 second depending on the product."
        }
    )
    total_memory: int = field(metadata={"help": "Total installed GPU memory."})
    free_memory: int = field(metadata={"help": "Total free memory."})
    used_memory: int = field(metadata={"help": "Total memory allocated by active contexts."})


def get_gpus() -> List[GPUInformation]:
    """
    Function to get gpu information using nvidia-smi. To use this function, `nvidia-smi` must be installed in advance.
    Using this function, you can get the information of GPUs.
    For detailed explanation, see the site below
    https://nvidia.custhelp.com/app/answers/detail/a_id/3751/~/useful-nvidia-smi-queries
    Returns:
        List[GPUInformation]: List of Information of each GPU
    """
    p = Popen(
        [
            "nvidia-smi",
            "--query-gpu=index,gpu_name,gpu_bus_id,temperature.gpu,utilization.gpu,temperature.memory,utilization.memory,memory.total,memory.free,memory.used",
            "--format=csv,noheader,nounits",
        ],
        stdout=PIPE,
    )
    stdout, _ = p.communicate()
    lines = stdout.decode("utf-8").split(os.linesep)
    ret = []
    for line in lines[:-1]:
        [
            index,
            gpu_name,
            gpu_bus_id,
            gpu_temperature,
            gpu_utilization,
            memory_temperature,
            memory_utilization,
            total_memory,
            free_memory,
            used_memory,
        ] = [each.strip() for each in line.split(",")]
        ret.append(
            GPUInformation(
                index=index,
                gpu_name=gpu_name,
                gpu_bus_id=gpu_bus_id,
                gpu_temperature=gpu_temperature,
                gpu_utilization=gpu_utilization,
                memory_temperature=memory_temperature,
                memory_utilization=memory_utilization,
                total_memory=total_memory,
                free_memory=free_memory,
                used_memory=used_memory,
            )
        )
    return ret
