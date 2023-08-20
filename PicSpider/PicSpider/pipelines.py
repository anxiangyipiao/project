# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from scrapy.utils.project import get_project_settings
from .items import ImageItem, NovelItem


class PicspiderPipeline(object):

    def open_spider(self, spider):
        settings = get_project_settings()
        self.connection = pymysql.connect(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            charset='utf8mb4'
        )
        # self.create_table()
        self.cursor = self.connection.cursor()


    def process_item(self, item, spider):
       
        if isinstance(item, ImageItem):
            self.insert_image(item)
        elif isinstance(item, NovelItem):
            self.insert_novel(item)

        return item

 
    def create_table(self):
        
        with self.connection.cursor() as cursor:
            cursor.execute("SHOW TABLES LIKE 'novel_table'")
            if not cursor.fetchone():
                create_novel_table_query = """
            CREATE TABLE novel_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                url VARCHAR(255),
                size VARCHAR(255),
                des TEXT,
                content TEXT,
                author VARCHAR(100),
                category VARCHAR(50),
                is_public BOOLEAN DEFAULT TRUE,
                crawl_time DATETIME
            )
                """
                cursor.execute(create_novel_table_query)
                print("novel_table created")

            cursor.execute("SHOW TABLES LIKE 'image_table'")
            if not cursor.fetchone():
                create_image_table_query = """
            CREATE TABLE image_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                url VARCHAR(255),
                title VARCHAR(255),
                source MEDIUMBLOB,
                is_public BOOLEAN DEFAULT TRUE,
                category VARCHAR(50),
                crawl_time DATETIME
            )
                """
                cursor.execute(create_image_table_query)
                print("image_table created")

        self.connection.commit()


    def insert_image(self, item):

        insert_query = """
        INSERT INTO image_table (url, title, source, is_public, category, crawl_time)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        self.cursor.execute(insert_query, (item['url'], item['title'], item['source'], 
                                     item['is_public'], item['category'], item['crawl_time']))

        self.connection.commit()
   
   
    def insert_novel(self, item):
        insert_query = """
        INSERT INTO novel_table (size,url,des,title, content, author, category, is_public, crawl_time)
        VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_query, (item['size'],item['url'],item['des'],item['title'], item['content'], item['author'], 
                                     item['category'], item['is_public'], item['crawl_time']))
        
        self.connection.commit()
