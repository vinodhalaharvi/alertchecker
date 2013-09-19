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


class GetAlertDefinitions(object):
	"""docstring for GetAlertDefinitions"""
	def __init__(self, host):
		super(GetAlertDefinitions, self).__init__()
		self.getTuple()
		self.g = Get()
		assert host
		self.host = host

	def getTuple(self):
		"""docstring for getTuple"""
		for line in sys.stdin:
			line = line.strip()
			platformName, resourceId = line.split()
			yield (platformName, resourceId)
	

	def runSQL(self):
		"""docstring for runSQL"""
		for platformName, resourceId in self.getTuple():
			url = r"http://%s:7080/hqu/hqapi1/alertdefinition/listDefinitions.hqu?resourceId=%s&children=true&verbose=true" % (self.host, resourceId)
			filename = platformName + ".xml"

			print " Now processing .. " 	
			print filename
			print url
			print resourceId

			file = open("data/" + filename, 'w')
			data = self.g.get(url)
			file.write(xml.dom.minidom.parseString(data).toprettyxml())
			print " filename done .. " 
			print "==========================="


if __name__ == '__main__':
        if len(sys.argv) > 1 or sys.argv[1] == "-h":
                print
                print " This script has only been tested to work with Python version 2.7 "
                print " Usage: python getAlertDefinitionsSerial.py [Number of parallel jobs] "
                print " Example: python getAlertDefinitionsSerial.py 10 "
                print " Enter FQDN RESOURCE_ID pairs, one per line "
                print " For example your input should look like this .. "
                print
                print r"""
                TJAX2723APP.csxt.ad.csx.com     15508
                TJAXD80157APP.csxt.ad.csx.com   32827
                TJAXV648PS.csxt.ad.csx.com      24227
                TJAXV707APP.csxt.ad.csx.com     15829
                """
                print " You can get this input by running the following SQL in hyperic console .. "
                print " select fqdn, resource_id from eam_platform order by 1; "
                print
                print " After you enter your input press two Control D's i.e., Ctrl-D, Ctrl-D "
                print
                print " For output look for ./data directory .."
                print " Enjoy! "
                sys.exit(0)

	ga = GetAlertDefinitions("host")
	ga.runSQL()
