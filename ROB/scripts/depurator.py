#!/usr/bin/env python

import roslib; 
roslib.load_manifest('ROB')
import rospy
import os,sys,itertools,traceback,time
import grasp_functions
from numpy import *
from openravepy import *



##################################################################################	
class SCRIPT():###################################################################
##################################################################################	

	# ------------------------------------------------------------------------------------
	# ------------------------------------------------------------------------------------
	def __init__(self):
		print "---------------------------------------------"
		print "To run this script you must be in his folder." 
		print "---------------------------------------------"

		self.robotName = 'robots/schunk-sdh.zae'
		if (len(sys.argv)<=1):
			self.targetName = 'mug'
			self.object_path = '../DB/obj/'+self.targetName+'.kinbody.xml'
			print "Loaded default values: (%s, %s)" %(self.robotName, self.object_path)
		else:
			self.targetName = sys.argv[1]

			if self.targetName[len(self.targetName)-3:len(self.targetName)] == ".iv":
				self.object_path = '../DB/obj/'+self.targetName;
			else:
				self.object_path = '../DB/obj/'+self.targetName+'.kinbody.xml'

			print "Loaded values: (%s, %s)" %(self.robotName, self.targetName)

	# ------------------------------------------------------------------------------------
	# ------------------------------------------------------------------------------------
	def run(self):	
		

		env = Environment()
 		robot = env.ReadRobotXMLFile(self.robotName)
		target = env.ReadKinBodyXMLFile(self.object_path)
		env.AddRobot(robot)
		env.AddKinBody(target)


		env.SetViewer('qtcoin')
		time.sleep(1.0)


		repetir=True
		while repetir==True:
			GRASPS_D = []
			try:
				GRASPS = grasp_functions.getGrasps(self.targetName+"_all_grasps.xml")
			except:
				print "There are not generated file."
				sys.exit()
	
			print "There are "+str(len(GRASPS))+" configurations for the object "+self.targetName

			try:
				GRASPS_D = grasp_functions.getGrasps(self.targetName+"_D.xml")
			except:
				print "Any configurations has been depurated."



			if len(GRASPS_D) < len(GRASPS):
				print "The configuration "+str(len(GRASPS_D))+" will be depurated.";
				g = grasp_functions.showOR(env=env, grasps=GRASPS[len(GRASPS_D)], depurador=True)
				if len(g)>0:
					grasp_functions.generaFicheroDepurado(targetName=self.targetName, grasps=g)
					res = raw_input("Do you want to show another configuration? (y/n): ")
					if res=="n":
						repetir = False
			else:
				print "All the configurations has been depurated."
				repetir = False;

	
						
		
		raw_input("Press ENTER to finish.")



##########################################################################
if __name__ == "__main__":################################################
##########################################################################
	s = SCRIPT()
    	s.run()
