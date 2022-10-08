import pickle
from loguru import logger

from analyser.people import extract_people_from_report
from analyser.stats import calculate_hashtags_stats
from scrapper.config import FIRST_MESSAGE_WITH_LABEL_ID
from analyser.report import get_all_reports_from_messages
from scrapper.messages import get_messages_from_border_control
from database.postgres import insert_new_report, get_last_message_id, insert_or_increase_hashtag, insert_new_people


def fulfill_hashtag_stats_tables(hashtag_stats):
    for approved, stats in hashtag_stats.items():
        for tag, cnt in stats.items():
            insert_or_increase_hashtag(hashtag=tag, approved=approved, cnt=cnt)


def fulfill_reports_and_peoples_tables(reports, scrap_date):
    for report in reports:
        report_attributes_with_scrap_date = {**report.__dict__, **{'scrap_date': scrap_date}}
        report_returning = insert_new_report(**report_attributes_with_scrap_date)
        report_id = report_returning.fetchone()[0]
        peoples_from_report = extract_people_from_report(report, report_id)
        for people in peoples_from_report:
            insert_new_people(**people.__dict__)


def collect_reports_and_update_statistics(retro=False):
    # Get last message id
    if retro:
        last_saved_message_id = FIRST_MESSAGE_WITH_LABEL_ID
    else:
        last_saved_message_id = get_last_message_id()

    # Collect message
    messages, scrap_date = get_messages_from_border_control(min_id=last_saved_message_id)

    reports = get_all_reports_from_messages(messages)
    logger.info(f"# Prepare reports from messages: {len(reports)}")

    # Calculate stats and fullfill tables
    hashtag_stats = calculate_hashtags_stats(reports)

    # Fulfill raw report table
    fulfill_hashtag_stats_tables(hashtag_stats)

    # Fulfill raw reports table with peop
    fulfill_reports_and_peoples_tables(reports, scrap_date)


if __name__ == "__main__":
    collect_reports_and_update_statistics()
