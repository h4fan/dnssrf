#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

#db_str = '/root/dnssrf/dnssrf.db'
db_str = 'dnssrf.db'

import datetime,requests


from qqwry import QQwry
from config import API_DOMAIN_PREFIX, DNSLOG_Root_Domain


def gettime():
	timenow = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
	timetext = timenow.strftime('%Y/%m/%d %H:%M:%S') + " UTC+8"
	return timetext


def getiploc(ip):
	r = requests.get(url="http://ip-api.com/json/%s?lang=zh-CN" % ip)
	resp = r.json()
	#print(resp)
	iploc = resp["country"]+resp["regionName"]+resp['city']+resp["isp"]
	return iploc


def getlocfromqqwry(ip):
	q = QQwry()
	q.load_file('qqwry_lastest.dat')
	result = q.lookup(ip)
	return ",".join(result)

def getrecords():
	conn = sqlite3.connect(db_str)
	c = conn.cursor()
	#print(logtimestamp,src_ip,iplocation,datatype,hostname,fulldata,isshow)
	

	c.execute("select * from logmessage where hostname like ? and isshow=0",('%'+DNSLOG_Root_Domain,))

	values = c.fetchall()
	result_json = []
	for row in values:
		result_json.append({"timestamp":row[0],"ip":row[1],"iploc":row[2],"datatype":row[3],"hostname":row[4],"fulldata":row[5]})

	c.execute("update logmessage set isshow=1 where hostname like ? and isshow=0",('%'+DNSLOG_Root_Domain,))
	# may lost some data

	conn.commit()
	conn.close()
	return result_json


def log2db(src_ip,datatype,hostname,fulldata):
	hostname = str(hostname)
	if(API_DOMAIN_PREFIX in str(hostname).lower()):
		return
	if(hostname[-1] == "."):
		hostname = hostname[:-1]
	conn = sqlite3.connect(db_str)
#conn = sqlite3.connect('srcmon.db')

	c = conn.cursor()
	logtimestamp = gettime()
	#iplocation = getiploc(src_ip)
	iplocation = getlocfromqqwry(src_ip)
	isshow = 0
	#print(logtimestamp,src_ip,iplocation,datatype,hostname,fulldata,isshow)

	c.execute("insert into logmessage values(?,?,?,?,?,?,?)",(logtimestamp,str(src_ip),iplocation,datatype,str(hostname),fulldata,isshow))

	conn.commit()
	conn.close()
