import os
from subprocess import Popen, PIPE
from typing import Dict


def string_to_int(string_number: str) -> int:
    try:
        number = int(string_number)
    except ValueError:
        number = 0
    return number


def get_gpus() -> Dict[int, Dict]:
    """
    Function to get gpu information using nvidia-smi. To use this function, `nvidia-smi` must be installed in advance.
    Using this function, you can get the GPU utilization, memory utilization, total memory, used memory and temperature information.
    For detailed explanation, see the site below
    https://nvidia.custhelp.com/app/answers/detail/a_id/3751/~/useful-nvidia-smi-queries
    This function returns information in the form below.
    {
        0: {
            'utilization': 65,
            'memory_utilization': 47,
            'total_memory': 40537,
            'used_memory': 19543
            'temperature': 48,
        },
        1: {
            'utilization': 52,
            'memory_utilization': 36,
            'total_memory': 40537,
            'used_memory': 17080
            'temperature': 46,
        },
        ...
    }
    """
    ret: Dict[int, Dict] = {}
    try:
        p = Popen([
            "nvidia-smi",
            "--query-gpu=index,utilization.gpu,utilization.memory,memory.total,memory.used,temperature.gpu",
            "--format=csv,noheader,nounits"], stdout=PIPE)
        stdout, stderr = p.communicate()
    except Exception as e:
        return {-1: f'{e}'}
    try:
        lines = stdout.decode('utf-8').split(os.linesep)
        number_of_gpus = len(lines) - 1
        for i in range(number_of_gpus):
            [index, utilization, memory_utilization, total_memory, used_memory, temperature] = lines[i].split(', ')
            ret[int(index)] = {
                'utilization': string_to_int(utilization),
                'memory_utilization': string_to_int(memory_utilization),
                'total_memory': string_to_int(total_memory),
                'used_memory': string_to_int(used_memory),
                'temperature': string_to_int(temperature)
            }
        return ret
    except UnicodeDecodeError as e:
        return {-1: f'{e}'}
