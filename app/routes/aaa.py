import sqlite3


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

def fetch_login_data(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = generate_select_query_aaa_login()
    cursor.execute(query)
    login_info = cursor.fetchall()
    conn.close()
    return login_info