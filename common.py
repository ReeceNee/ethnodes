# coding:utf-8
#!/usr/bin/env python3

import logging
import logging.config
import pymongo
import configparser


class Common(object):

    cfg = None
    log = None
    db = None

    def __init__(self):

        # config handler
        self.cfg = configparser.ConfigParser()
        self.cfg.read("conf/config.ini")

        # logging handler
        self.log = logging
        self.log.config.fileConfig('conf/log_conf.ini')
        self.log.info("Init config and log success!")

        # mongoDB handler
        db_host = self.cfg.get('mongodb', 'host')
        db_port = self.cfg.get('mongodb', 'port')
        db_user = self.cfg.get('mongodb', 'user')
        db_passwd = self.cfg.get('mongodb', 'passwd')
        db_database = self.cfg.get('mongodb', 'database')
        mongo_uri = "mongodb://{0}:{1}@{2}:{3}/{4}".format(
            db_user, db_passwd, db_host, db_port, db_database)
        # print(mongo_uri)

        mongo_uri = "mongodb://{0}:{1}".format(db_host,db_port)
        self.db = pymongo.MongoClient(mongo_uri)
        # self.db = db_conn.get_database('node')
        # self.db.authenticate(db_user, db_passwd, mechanism='MONGODB-CR')
        self.log.info("Init MongoDB succeess!")


if __name__ == '__main__':
    c = Common()
    datadb = c.db['ethnodes']['ethernodes']
    # datadb.authenticate("reece","r33c3_mong0.THU",mechanism='MONGODB-CR')
    # datadb['ethernodes'].insert({"a":"1"})
    # print(datadb['system.users'].find_one())
