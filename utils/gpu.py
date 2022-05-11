import os
from typing import List
from dataclasses import dataclass, field
from subprocess import Popen, PIPE


@dataclass
# pylint: disable=line-too-long, too-many-instance-attributes
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
    For detailed explanation, see the site below or `nvidia-smi --help-query-gpu`
    https://nvidia.custhelp.com/app/answers/detail/a_id/3751/~/useful-nvidia-smi-queries
    Returns:
        List[GPUInformation]: List of Information of each GPU
    Example:
        >>> get_gpus()
        >>> [
            GPUInformation(
                index=0,
                gpu_name='NVIDIA TITAN V',
                gpu_bus_id='00000000:06:00.0',
                gpu_temperature=46,
                gpu_utilization=0,
                memory_temperature=41,
                memory_utilization=0,
                total_memory=12288,
                free_memory=11180,
                used_memory=883
            )
        ]
    """

    def string_to_int(value: str) -> int:
        """
        Convert string value to Integer value
        If string value is not intger, return -1
        Args:
            value (str): string value
        Returns:
            int: Integer Value
        Examples:
            >>> string_to_int("32")
            >>> 32
            >>> string_to_int("N/A")
            >>> -1
        """
        try:
            return int(value)
        except ValueError:
            return -1

    with Popen(
        [
            "nvidia-smi",
            "--query-gpu=index,gpu_name,gpu_bus_id,temperature.gpu,utilization.gpu,temperature.memory,utilization.memory,memory.total,memory.free,memory.used",
            "--format=csv,noheader,nounits",
        ],
        stdout=PIPE,
    ) as proc:
        stdout, _ = proc.communicate()
        lines = stdout.decode("utf-8").split(os.linesep)
        ret = []
        for line in lines[:-1]:
            gpu_information_list = [each.strip() for each in line.split(",")]
            ret.append(
                GPUInformation(
                    index=string_to_int(gpu_information_list[0]),
                    gpu_name=gpu_information_list[1],
                    gpu_bus_id=gpu_information_list[2],
                    gpu_temperature=string_to_int(gpu_information_list[3]),
                    gpu_utilization=string_to_int(gpu_information_list[4]),
                    memory_temperature=string_to_int(gpu_information_list[5]),
                    memory_utilization=string_to_int(gpu_information_list[6]),
                    total_memory=string_to_int(gpu_information_list[7]),
                    free_memory=string_to_int(gpu_information_list[8]),
                    used_memory=string_to_int(gpu_information_list[9]),
                )
            )
        return ret


def get_average_gpu_utilization(gpu_information_list: List[GPUInformation]) -> float:
    """
    Get the average of the GPU utilization

    Args:
        gpu_information_list (List[GPUInformation]): gpu information

    Returns:
        float: average of gpu utilization

    Example:
        >>> get_average_gpu_utilization(
            [
                GPUInformation(
                    index=0,
                    gpu_name='NVIDIA TITAN V',
                    gpu_bus_id='00000000:06:00.0',
                    gpu_temperature=46,
                    gpu_utilization=43,
                    memory_temperature=41,
                    memory_utilization=0,
                    total_memory=12288,
                    free_memory=11180,
                    used_memory=883
                )
            ]
        )
        >>> 43.0
    """
    total_gpu_utilization = sum([gpu_info.gpu_utilization for gpu_info in gpu_information_list])
    average_gpu_utilization = total_gpu_utilization / len(gpu_information_list)

    return average_gpu_utilization
