import pymysql
import passwords as pw

connection = pymysql.connect(host=pw.aws_mysql_scraping_db.host, user=pw.aws_mysql_scraping_db.username,
                password=pw.aws_mysql_scraping_db.password, database=pw.aws_mysql_scraping_db.db_name,
                port=pw.aws_mysql_scraping_db.port)

cursor = connection.cursor()

cursor.execute("SHOW TABLES")
outcome = cursor.fetchone()

print(outcome)