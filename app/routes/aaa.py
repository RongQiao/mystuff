from dataclasses import dataclass, astuple
from typing import Optional
from datetime import date
import sqlite3

from config import db_config
DB_PATH = db_config.DB_PATH

def generate_select_query_aaa_login():
  return """
    SELECT
      aaa_login.id,
      aaa_login.name_short,
      aaa_login.website,
      aaa_login.category,
      aaa_login.note,
      aaa_login.has_sub_plan,
      aaa_login.has_point_plan,
      aaa_username.username_short,
      aaa_cipher.cipher_shortname,
      CONCAT(people_individual.first_name, ' ', people_individual.last_name) as owner
    FROM aaa_login
    JOIN aaa_username ON aaa_login.username_id = aaa_username.id
    JOIN aaa_cipher ON aaa_login.cipher_id = aaa_cipher.id
    JOIN people_individual ON aaa_login.primary_people_id = people_individual.id;
  """

def fetch_login_data():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  query = generate_select_query_aaa_login()
  cursor.execute(query)
  login_info = cursor.fetchall()
  conn.close()
  return login_info


@dataclass
class LoginFormData:
  name_short: str
  website: str
  category: Optional[str]
  note: Optional[str]
  username_short: str
  cipher_shortname: str
  owner: Optional[str]
  has_sub_plan: bool = False
  has_point_plan: bool = False

@dataclass
class LoginInsertData:
  name_short: str
  website: str
  category: str
  username_id: int
  cipher_id: int
  primary_people_id: int
  register_date: date
  tier: int
  note: str
  has_sub_plan: bool
  has_point_plan: bool

@dataclass
class LoginInsertInfo:
  query: str
  data: tuple

def get_single_id(table: str, where_condition: str) -> int:
  query = f"""
    SELECT id
    FROM {table}
    WHERE {where_condition}
  """
  print(query)
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute(query)
  result = cursor.fetchone()
  conn.close()
  return result[0] if result else 1


def generate_insert_query_aaa_login(input_data: LoginFormData) -> LoginInsertInfo:
  query = """
    INSERT INTO aaa_login
     (name_short, website, category, username_id, cipher_id, primary_people_id, register_date, tier, note, has_sub_plan, has_point_plan)
     VALUES
     (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  """
  # get the id from text input
  username_id = get_single_id('aaa_username', f'username_short = "{input_data.username_short}"')
  cipher_id = get_single_id('aaa_cipher', f'cipher_shortname = "{input_data.cipher_shortname}"')
  owner_name_l = input_data.owner.split(' ')
  primary_people_id = get_single_id('people_individual', f'first_name = "{owner_name_l[0]}" and last_name = "{owner_name_l[1]}"')
  data = LoginInsertData(
    name_short = input_data.name_short,
    website = input_data.website,
    category = input_data.category,
    username_id = 1,
    cipher_id = 1,
    primary_people_id = 1,
    register_date = date.today().isoformat(),
    tier = 1,
    note = input_data.note,
    has_sub_plan = False,
    has_point_plan = False
  )
  return LoginInsertInfo(query = query, data = astuple(data))

def inser_new_login_data(input_data):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  insert_info = generate_insert_query_aaa_login(input_data)
  print(insert_info.query)
  print(insert_info.data)
  cursor.execute(
    insert_info.query,
    insert_info.data
  )
  conn.commit()
  conn.close()
