import os
import sys
import time
import argparse

from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler

from utils.slack import SlackWebhookBot
from utils.gpu import get_gpus, get_average_gpu_utilization
from constants import ExitStatusEnum, SlackMessageTypeEnum

low_utilization_start_time = None


def get_args() -> argparse.Namespace:
    """
    Get parameters for script execution.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server_name",
        type=str,
        default=os.getenv("SERVER_NAME", None),
        help="name that identifies the server",
    )
    parser.add_argument(
        "--webhook_url",
        type=str,
        default=os.getenv("WEBHOOK_URL", None),
        help="slack webhook url",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=int(os.getenv("INTERVAL", 60)),
        help="interval to check GPU usage (second)",
    )
    parser.add_argument(
        "--utilization_threshold",
        type=int,
        default=int(os.getenv("UTILIZATION_THRESHOLD", 40)),
        help="minimum GPU utilization",
    )
    parser.add_argument(
        "--time_threshold",
        type=int,
        default=int(os.getenv("TIME_THRESHOLD", 3600)),
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


def _gpu_check_job(
    utilization_threshold: int, server_name: str, time_threshold: int, slack_bot
) -> None:
    """
    Job to get GPU information every interval

    Args:
        utilization_threshold (int): minimum GPU utilization
        time_threshold (int): time to start sending danger alarms
    """
    global low_utilization_start_time
    now = time.time()
    logger.info("Check GPU")
    gpu_information_list = get_gpus()
    average_gpu_utilization = get_average_gpu_utilization(gpu_information_list)
    logger.info(f"GPU Utilization : {average_gpu_utilization}")
    if average_gpu_utilization <= utilization_threshold:
        if low_utilization_start_time is None:
            logger.warning("GPU Utilization is low")
            low_utilization_start_time = now
        elif now - low_utilization_start_time >= time_threshold:
            logger.error("GPU Utilization is low")
            low_utilization_start_time = None
            slack_bot.send_message(
                SlackMessageTypeEnum.ERROR_MESSAGE.value, server_name, average_gpu_utilization
            )
    else:
        low_utilization_start_time = None


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
    slack_bot = SlackWebhookBot(args.webhook_url)
    slack_bot.send_message(SlackMessageTypeEnum.INFO_MESSAGE.value, args.server_name)
    logger.info("Scheduler Start")
    scheduler = BlockingScheduler()
    scheduler.add_job(
        _gpu_check_job,
        "interval",
        args=[args.utilization_threshold, args.server_name, args.time_threshold, slack_bot],
        seconds=args.interval,
    )
    scheduler.start()


if __name__ == "__main__":
    main(get_args())
