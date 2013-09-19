# Copyright (c) 2013, RTP Network Services, Inc.
# All Rights Reserved      (904-236-6993)
# Vinod Halaharvi / vinod.halaharvi@rtpnet.net
# 
# http://www.rtpnet.net / codesupport@rtpnet.net
#
# There is NO warranty for this software.  If this software is used by
# someone else and passed on, the recipients should know that what they
# have is not the original, so that any problems introduced by others will
# not reflect on the original authors' reputations. This is *not* authorization
# to copy or distribute this software to others!

from get import Get
import sys
import multiprocessing as mp
import xml.dom.minidom
import os

def runSQL(item):
	g = Get()
	host = "host"
	"""docstring for runSQL"""
	platformName, resourceId = item
	url = r"http://%s:7080/hqu/hqapi1/resource/get.hqu?id=%s&children=true&verbose=true" % (host, resourceId)
	filename = platformName + ".resource.xml"
	print " Now processing .. " 	
	print filename
	print url
	print resourceId
	file = open("data/" + filename, 'w')
	data = g.get(url)
	file.write(xml.dom.minidom.parseString(data).toprettyxml())
	print filename + " done .. " 


class GetResources(object):
	"""docstring for GetResources"""
	def __init__(self, ):
		self.tup = []

	def readTuple(self):
		"""docstring for getTuple"""
		for line in sys.stdin:
			line = line.strip()
			platformName, resourceId = line.split()
			self.tup.append((platformName, resourceId))

	def getTuple(self,):
		return self.tup


if __name__ == '__main__':
	assert os.environ["hyperic_username"]
	assert os.environ["hyperic_password"]
        if len(sys.argv) > 1 and sys.argv[1] == "-h":
                print
		print " This script has only been tested to work with Python version 2.7 " 
                print " Usage: python getResourcesParallel.py [Number of parallel jobs] < platformList.txt" 
                print " Example: python getResourcesParallel.py 10 < platformList.txt"
		print " Enter FQDN RESOURCE_ID pairs, one per line " 
		print " For example your input should look like this .. " 
		print
		print r""" 
		TJAX2723APP.csxt.ad.csx.com	15508
		TJAXD80157APP.csxt.ad.csx.com	32827
		TJAXV648PS.csxt.ad.csx.com	24227
		TJAXV707APP.csxt.ad.csx.com	15829
		"""
		print " You can get this input by running the following SQL in hyperic console .. " 
		print
		print " select fqdn, resource_id from eam_platform order by 1; " 
		print " save the output of this in a file say, platformList.txt "
		print " Now run .." 
		print
                print " python getResourcesParallel.py 10 < platformList.txt"
		print 
		print " For output look for ./data directory .." 
		print " Enjoy! " 
                sys.exit(0)

	if len(sys.argv) > 1:
		N = int(sys.argv[1])
	else:
		N = 4
	p = mp.Pool(N)
	ga = GetResources()
	ga.readTuple()
	t = ga.getTuple()
	p.map(runSQL, t)
	
