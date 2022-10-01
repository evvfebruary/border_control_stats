from loguru import logger
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData, Boolean, DateTime, Integer, ARRAY, JSON, ForeignKey

from database.config import PG_USERNAME, PG_PASSWORD, PG_PORT, PG_DATABASE, PG_HOST, REPORTS_TABLE_NAME, \
    HASHTAGS_STATS_TABLE_NAME, PEOPLES_TABLE_NAME

db_string = f"postgresql://{PG_USERNAME}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
logger.info(f'DB STINRG {db_string}')
db = create_engine(db_string)

meta = MetaData(db)

# Reports table
reports_table = Table(REPORTS_TABLE_NAME, meta,
                      Column('id', Integer, primary_key=True),
                      Column('message_id', Integer),
                      Column('text', String),
                      Column('hashtags', ARRAY(String)),
                      Column('normalised_hashtags', ARRAY(String)),
                      Column('approved', Boolean),
                      Column('approved_mark_cnt', Integer),
                      Column('declined_mark_cnt', Integer),
                      Column('marks_sequence', ARRAY(String)),
                      Column('peoples', JSON),
                      Column('post_date', DateTime),
                      Column('scrap_date', DateTime))

hashtags_stats = Table(HASHTAGS_STATS_TABLE_NAME, meta,
                       Column('hashtag', String),
                       Column('approved', Boolean),
                       Column('cnt', Integer))


peoples_table = Table(PEOPLES_TABLE_NAME, meta,
                      Column('id', Integer, primary_key=True),
                      Column('report_id', Integer, ForeignKey('reports_new.id')),
                      Column('gender', String),
                      Column('age', Integer),
                      Column('approved', Boolean))


def insert_new_report(**kwargs):
    with db.connect() as conn:
        insert_statement = reports_table.insert().values(kwargs).returning(reports_table.c.id)
        report_id = conn.execute(insert_statement)
        return report_id


def insert_new_people(**kwargs):
    with db.connect() as conn:
        insert_statement = peoples_table.insert().values(kwargs)
        conn.execute(insert_statement)


def insert_new_hashtag_stats(hashtag, approved, cnt):
    with db.connect() as conn:
        insert_statement = hashtags_stats.insert().values(
            hashtag=hashtag,
            approved=approved,
            cnt=cnt
        )
        conn.execute(insert_statement)


def get_last_message_id():
    """ToDo: Handle none situation"""
    with Session(db) as session:
        max_id = session.query(func.max(reports_table.c.message_id)).scalar()
    return max_id


def insert_or_increase_hashtag(hashtag, approved, cnt):
    with Session(db) as session:
        hashtag_info = session.query(hashtags_stats.c.hashtag,
                                     hashtags_stats.c.cnt).filter_by(hashtag=hashtag, approved=approved).first()
        if not hashtag_info:
            logger.info(f"# Got new hashtag:{hashtag}")
            insert_new_hashtag_stats(hashtag=hashtag,
                                     approved=approved,
                                     cnt=cnt)
        else:
            hashtag, old_cnt = hashtag_info
            new_cnt = old_cnt + cnt
            update_statement = hashtags_stats.update().where(and_(hashtags_stats.c.hashtag == hashtag,
                                                                  hashtags_stats.c.approved == approved)).values(
                cnt=new_cnt)
            session.execute(update_statement)
            session.commit()
