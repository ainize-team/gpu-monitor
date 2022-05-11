import sys
import argparse

from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler

from utils.gpu import get_gpus, get_average_gpu_utilization
from constants import ExitStatusEnum


def get_args() -> argparse.Namespace:
    """
    Get parameters for script execution.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server_name",
        type=str,
        required=True,
        help="name that identifies the server",
    )
    parser.add_argument(
        "--webhook_url",
        type=str,
        required=True,
        help="slack webhook url",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="interval to check gpu usage (second)",
    )
    parser.add_argument(
        "--utilization_threshold", type=int, default=40, help="minimum GPU utilization"
    )
    parser.add_argument(
        "--time_threshold",
        type=int,
        default=60 * 60,  # 1 hour
        help="time to start sending danger alarms",
    )
    return parser.parse_args()


def check_args(args: argparse.Namespace) -> None:
    """
    Checks whether the input parameters are valid.
    If it is an invalid parameter, an error is raised.
    """
    if args.interval < 0:
        raise ValueError("The value of `interval` must be positive.")
    if args.interval > args.time_threshold:
        raise ValueError(
            "The value of `time_threshold` must be greater than the value of `interval`."
        )
    if args.utilization_threshold < 0 or args.utilization_threshold > 100:
        raise ValueError("The value of `utilization_threshold` must be between 0 and 100.")


def _gpu_check_job(utilization_threshold: int, time_threshold: int) -> None:
    """
    Job to get gpu information every interval

    Args:
        utilization_threshold (int): minimum GPU utilization
        time_threshold (int): time to start sending danger alarms
    """
    gpu_information_list = get_gpus()
    average_gpu_utilization = get_average_gpu_utilization(gpu_information_list)
    if average_gpu_utilization <= utilization_threshold:
        logger.error("gpu utilization is low")
    else:
        logger.info("gpu utilization is good")


def main(args: argparse.Namespace) -> None:
    """
    Main function
    """
    logger.info("Server Start")
    try:
        check_args(args)
    except ValueError as error:
        logger.error(error)
        sys.exit(ExitStatusEnum.PARAMETER_VALUE_ERROR.value)
    try:
        get_gpus()
    except FileNotFoundError as error:
        logger.error(error)
        sys.exit(ExitStatusEnum.NVIDIA_SMI_NOT_FOUND_ERROR.value)
    logger.info("Scheduler Start")
    scheduler = BlockingScheduler()
    scheduler.add_job(
        _gpu_check_job,
        "interval",
        args=[args.utilization_threshold, args.time_threshold],
        seconds=args.interval,
    )
    scheduler.start()


if __name__ == "__main__":
    main(get_args())
