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
    ret: Dict[int, Dict] = {}
    try:
        p = Popen([
            "nvidia-smi",
            "--query-gpu=index,utilization.gpu,utilization.memory,memory.total,memory.used,temperature.gpu",
            "--format=csv,noheader,nounits"], stdout=PIPE)
        stdout, stderror = p.communicate()
    except Exception as e:
        # TODO(YoungJae Kim) : Exception Handling
        return ret
    try:
        lines = stdout.decode('utf-8').split(os.linesep)
        number_of_gpus = len(lines) - 1
        for i in range(number_of_gpus):
            [index, utilization, memory_utilization, total_memory, used_memory, temperature] = lines[i].split(', ')
            ret[int(index)] = {
                'utilization': string_to_int(utilization),
                'memory_utilization': string_to_int(memory_utilization),
                'total_memory': total_memory,
                'used_memory': used_memory,
                'temperature': string_to_int(temperature)
            }
        return ret
    except UnicodeDecodeError as e:
        # TODO(YoungJae Kim) : Exception Handling
        return ret
