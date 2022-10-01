from typing import List
from analyser.report import Report
from analyser.config import APPROVED_MARK


class People:

    def __init__(self, report_id: int, gender: str, age: int, approved: bool):
        """
        Create instance with information about people who crossed the borders
        :param report_id: Report ID used as foreign key
        :param gender: m or f ( according to mapping )
        :param age: integer value for age
        :param approved: True if passed, else False
        """
        self.report_id = report_id
        self.gender = gender
        self.age = age
        self.approved = approved

    def __str__(self):
        return f"{self.gender} {self.age} from report {self.report_id} passed {self.approved}"


def extract_people_from_report(report: Report, report_id: int) -> List[People]:
    """
    Extrac all participants from report
    :param report: Report instance
    :param report_id: report id returning after insert
    :return: list of peoples from report
    """
    peoples = []
    is_people_count_matched = (report.approved_mark_cnt + report.declined_mark_cnt) == len(report.peoples)
    if report.marks_sequence and report.peoples:
        for mark, people in zip(report.marks_sequence, report.peoples):
            if is_people_count_matched:
                approved = mark == APPROVED_MARK
            else:
                marks_set = list(set(report.marks_sequence))
                approved = None if len(marks_set) != 1 else marks_set[0] == APPROVED_MARK

            people_instance = People(report_id=report_id,
                                     gender=people.get('gender'),
                                     age=people.get('age'),
                                     approved=approved)
            peoples.append(people_instance)
    return peoples
