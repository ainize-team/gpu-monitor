import argparse
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.blocking import BlockingScheduler

from utils.gpu import get_gpus
from utils import SlackWebhookBot

KST = timezone(timedelta(hours=9))

history = None


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--server_name',
        type=str,
        required=True,
        help='name that identifies the server',
    )
    parser.add_argument(
        '--webhook_url',
        type=str,
        required=True,
        help='slack webhook url',
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=60,
        help='interval to check gpu usage (second)',
    )
    parser.add_argument(
        '--utilization_threshold',
        type=int,
        default=40,
        help='minimum GPU utilization'
    )
    parser.add_argument(
        '--time_threshold',
        type=int,
        default=60 * 60,  # 1 hour
        help='time to start sending danger alarms'
    )
    return parser.parse_args()


def check_status(args: argparse.Namespace, slack_bot: SlackWebhookBot) -> None:
    global history
    gpus = get_gpus()
    now = datetime.now(tz=KST)
    if -1 in gpus:
        slack_bot.send_error(args.server_name, gpus[-1])
    else:
        average_utilization = sum([gpu['utilization'] for gpu in gpus.values()]) / len(gpus)
        if average_utilization <= args.utilization_threshold:
            if history is None:
                history = now
                for _ in range(3):
                    result = slack_bot.send_message('warning', args.server_name, now.strftime('%Y-%m-%d %H:%M:%S'),
                                                    average_utilization)
                    if not result['error']:
                        break
            elif (now - history).total_seconds() >= args.time_threshold:
                for _ in range(3):
                    result = slack_bot.send_message('danger', args.server_name, history.strftime('%Y-%m-%d %H:%M:%S'),
                                                    average_utilization)
                    if not result['error']:
                        break
        else:
            if history is not None:
                history = None
                for _ in range(3):
                    result = slack_bot.send_message('success', args.server_name, now.strftime('%Y-%m-%d %H:%M:%S'),
                                                    average_utilization)
                    if not result['error']:
                        break


def main(args: argparse.Namespace) -> None:
    slack_bot = SlackWebhookBot(args.webhook_url)
    scheduler = BlockingScheduler()
    scheduler.add_job(check_status, 'interval', args=[args, slack_bot], seconds=args.interval)
    scheduler.start()


if __name__ == '__main__':
    main(get_args())
