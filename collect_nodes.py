# coding:utf-8
#!/usr/bin/env python3

from common import Common
import urllib3
import json

ether_api = '''https://ethernodes.org/network/1/data?draw=3&\
columns%5B0%5D%5Bdata%5D=id&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&\
columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=host&\
columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5B\
search%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=port&columns%5B2%5D%5B\
name%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&\
columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=country&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5B\
searchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5B\
regex%5D=false&columns%5B4%5D%5Bdata%5D=clientId&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&\
columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&\
columns%5B5%5D%5Bdata%5D=client&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&\
columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=clientVersion&\
columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5B\
search%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=os&columns%5B7%5D%5Bname%5D=&\
columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5B\
search%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=lastUpdate&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&\
columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5B\
column%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length={0}&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1528539370439'''


class collectNodes(object):
    # global common info handler
    g = Common()
    http = urllib3.PoolManager()
    items_onece = 2000
    logger = g.log.getLogger("collect")

    def __init__(self):
        pass

    def crawler(self):
        '''
        crawl in ethernodes.org to collect nodes
        '''
        # get count
        try:
            r = self.http.request('GET', ether_api.format(0))
            result = json.loads(r.data.decode('utf-8'))
            node_count = result["recordsTotal"]
            self.logger.info(
                "The latest count for ethernodes is : {0}".format(node_count))
                
        except Exception as e:
            self.logger.error("Get count error!")
            self.logger.error(repr(e))
            exit(-1)

        # get node info
        try:
            r = self.http.request('GET', ether_api.format(node_count))
            result = json.loads(r.data.decode('utf-8'))
            db_database = self.g.cfg.get('mongodb', 'database')
            db_datapage = self.g.cfg.get('database', 'datapage')
            db_col = self.g.db[db_database][db_datapage]
            for node in result['data']:
                db_col.insert(node)
                self.logger.info(str(node))
        except Exception as e:
            self.logger.error("Get data error!")
            self.logger.error(repr(e))
            exit(-1)

    def store_node(self, node_json):
        '''
        store node into database
        '''
        pass


def main():
    cn = collectNodes()
    cn.crawler()


if __name__ == '__main__':
    main()
