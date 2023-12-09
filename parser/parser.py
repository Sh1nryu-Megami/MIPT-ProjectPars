import urllib.request
from bs4 import BeautifulSoup
import psycopg2
import p_const
import quaries
from time import sleep

def connect_to_database():
    connection = psycopg2.connect(dbname=p_const.dbname,
                                  user=p_const.user,
                                  password=p_const.password,
                                  host=p_const.host)
    return connection


def update(cur, upd_dtype, upd_name, upd_details, upd_grams, upd_price, upd_image):
    cur.execute("""SELECT * FROM food_positions WHERE dish_name = %s""", (upd_name,))
    update_sql = quaries.SQL_UPDATE
    update_values = (upd_dtype, upd_details, upd_grams, upd_price, upd_image, upd_name)
    cur.execute(update_sql, update_values)
    cur.connection.commit()


def insert(cur, ins_dtype, ins_name, ins_details, ins_grams, ins_price, ins_image):
    insert_sql = quaries.SQL_INSERT
    insert_values = (ins_dtype, ins_name, ins_details, ins_grams, ins_price, ins_image)
    cur.execute(insert_sql, insert_values)
    cur.connection.commit()


def scrape_and_update_db(conn, cur, url, sections):
    
    response = urllib.request.urlopen(url)
    html_content = response.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    for section_number in sections:
        dishes = soup.find_all('div', {'class': f'tag-{section_number}'})
        for dish in dishes:
            dtype = dish.find('div', {'class': 'product__meta'}).find('span').text
            name = dish.find('a', {'class': 'js-item_title'}).text
            details = dish.find('p', {'class': 'js-item_desc'}).text.strip().replace('\n', ' ').replace('\xa0','')
            try:
                grams = dish.find('span', {'class': 'js-item_weight'}).text.strip().replace('::before', '').replace('"',
                                                                                                                    '')
            except:
                grams = ""
            price = dish.find('span', {'class': 'js-item_price'}).text
            image = url + dish.find('div', {'class': 'js-item_picture product__image uk-margin-bottom'}).find(
                'img').get('src')
            cur.execute("SELECT * FROM food_positions WHERE dish_name = %s", (name,))
            existing_record = cur.fetchone()
            if existing_record:
                update(cur, dtype, name, details, grams, price, image)
            else:
                insert(cur, dtype, name, details, grams, price, image)
         
                


def main():
    while True:
        try:
        	conn = connect_to_database()
        except psycopg2.OperationalError:
        	sleep(1)
        	continue
        with conn.cursor() as cur:
        	scrape_and_update_db(conn, cur, p_const.url, p_const.sections)
        	print("111111111111111111111111111111111111111111111111111111")
        	cur.execute('SELECT DISTINCT dish_type FROM food_positions')
        	result = [row[0] for row in cur.fetchall()]
        	print(result[0])
        	sleep(3600)
        	
        



if __name__ == '__main__':
    main()
