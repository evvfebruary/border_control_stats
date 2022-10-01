import re
import datetime
from typing import List
from operator import itemgetter
from collections import defaultdict
from analyser.config import HASHTAGS_PATTERN, APPROVED_MARK, DECLINED_MARK,\
    PEOPLE_PATTERN, REPORTS_SEPARATORS, GENDER_MAPPING


class Report:

    def __init__(self, text: str, post_date: datetime.datetime, message_id: int):
        """
        Create instance of Report
        :param text: text, after split by separators from message
        :param post_date: datetime when post was pasted
        :param message_id: id of message ( from rg )
        """
        self.marks_sequence = None
        self.normalised_hashtags = None
        self.peoples = None
        self.approved = None
        self.hashtags = None
        self.approved_mark_cnt, self.declined_mark_cnt = None, None
        self.text = text
        self.post_date = post_date
        self.message_id = message_id

    def check_approved(self):
        self.approved_mark_cnt, self.declined_mark_cnt = self.text.count(APPROVED_MARK), self.text.count(DECLINED_MARK)
        self.marks_sequence = re.findall(r'[❌|✅]', self.text)
        # ToDo: Improve logic to handling few different cases in one report
        if APPROVED_MARK in self.text:
            self.approved = True
        elif DECLINED_MARK in self.text:
            self.approved = False

    def extract_people_data(self):
        final_peoples = []
        all_occurences = re.findall(PEOPLE_PATTERN, self.text)
        for occurence in all_occurences:
            formatted_occurence = re.sub('[^а-я0-9]+', '', occurence.lower())
            gender, age = re.findall('[а-я]', formatted_occurence), re.findall('\d{2}', formatted_occurence)
            if gender and age:
                final_peoples.append({'gender': GENDER_MAPPING.get(gender[0]), "age": age[0]})
        self.peoples = final_peoples

    def extract_hashtags(self):

        def normalise_hashtag(hashtag):
            # ToDo: Create more complex logic for some cases ( maybe )
            return hashtag.lower()

        self.hashtags = re.findall(HASHTAGS_PATTERN, self.text)
        self.normalised_hashtags = [normalise_hashtag(hashtag) for hashtag in self.hashtags]


def get_all_reports_from_messages(messages: List[dict]) -> List[Report]:
    """
    Handling messages and divide them into reports using separator
    :param messages: array of messages ( represented as a dicts )
    :return: array of reports instances
    """
    all_reports = []
    for message in messages:
        message_dd = defaultdict(lambda: None, message)
        post_date, message_id, text = itemgetter('date', 'id', 'message')(message_dd)

        # Work with different lengths of separators in report
        reports_splitted_len, splitted_text = -1, None
        for possible_separator in REPORTS_SEPARATORS:
            reports_text = text.split(possible_separator)
            new_len_splitted = len(reports_text)
            if new_len_splitted > reports_splitted_len:
                reports_splitted_len = new_len_splitted
                splitted_text = reports_text

        # Prepare each report
        for report_text in splitted_text:
            rep = Report(text=report_text,
                         post_date=post_date,
                         message_id=message_id)
            rep.check_approved()
            rep.extract_hashtags()
            rep.extract_people_data()
            all_reports.append(rep)
    return all_reports
