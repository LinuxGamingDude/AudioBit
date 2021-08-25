#!/usr/bin/python

import os
import subprocess
from tkinter import *

class Dat:
	def __init__(self):
		#eventually a .dat file will be implemented to preserve the last applied settings
		#so that the user does not have to reselect them redundently.
		pass


class DaemonInterface:
	"""
	Important Information - Please Review

	Author: LinuxGamerDude
	Idea Collaboration: SMGuy

	[1] This Class is intended as a set of tools to map & set Daemon.Conf options.
	The ultimate goal of this class will be to generate a Daemon.conf in the users-home
	directory that will apply the desired settings to Pulse Audio
	
	[2] ~/.config/pulse/daemon.conf will be overwritten, please backup to a safe location if you
		wish to save any custom daemon settings.
	
	[3] /etc/asound.conf will be overwritten, please backup to a safe location if you wish to save.

	[4] Systems should be using systemd and have pulseaudio implemented
	[5] May have undefined behavior if run outside of intended environment
	[6] Run at your own risk

	"""
	daemonExperimental = False
	daemonResampleMethod = "speex-float-10"
	daemonRate = "48000"
	daemonSize = "float32le"
	CPU_Type = 1
	resampleMethodOptions = ['soxr-vhq', 'src-sinc-best-quality', 'speex-float-10', 'speex-fixed-10', 'speex-float-5', 'src-sinc-medium-quality', 'src-sinc-fastest', 'src-zero-order-hold', 'src-linear', 'trivial', 'ffmpeg']
	sampleRateOptions = ['192000', '96000', '48000', '44100',]
	sampleSizeOptionsL = ['float32le', 's32le', 's24-32le', 's24le', 's24le', 's16le']
	sampleSizeOptionsB = ['float32be', 's32be', 's24-32be', 's24be', 's24be', 's16be']
	resampleMethodMenu = []
	sampleSizeMenu = []
	sampleRateMenu = []

	def __init__(self, root):

		#determine if CPU is Little Endian or Big Endian
		cmd = "echo I | tr -d [:space:] | od -to2 | head -n1 | awk \'{print $2}\' | cut -c6"
		CPU_Type = int(subprocess.check_output(cmd, shell=True))

		#Generate System Specific GUI Options
		for x in self.resampleMethodOptions:
			self.resampleMethodMenu.append(StringVar(root, x, x))

		for x in self.sampleRateOptions:
			self.sampleRateMenu.append(StringVar(root, x, x))

		if not CPU_Type:
			for x in self.sampleSizeOptionsB:
				self.sampleSizeMenu.append(StringVar(root, x, x))
		else:
			for x in self.sampleSizeOptionsL:
				self.sampleSizeMenu.append(StringVar(root, x, x))

	def resetPulse(self):
		os.system('systemctl --user restart pulseaudio')

	def writeConfig(self):
		#(1) remove old pulse config 
		os.system('rm -r ~/.config/pulse/')
		os.system('mkdir ~/.config/pulse')

		#(2) write new daemon.conf with desired settings
		os.system('echo \"default-sample-format = ' + self.daemonSize + '\" >> ~/.config/pulse/daemon.conf')
		os.system('echo \"default-sample-rate = ' + self.daemonRate + '\" >> ~/.config/pulse/daemon.conf')
		os.system('echo \"alternate-sample-rate = 48000\" >> ~/.config/pulse/daemon.conf')
		os.system('echo \"resample-method = ' + self.daemonResampleMethod + '\" >> ~/.config/pulse/daemon.conf')
		os.system('echo \"high-priority = yes\" >> ~/.config/pulse/daemon.conf')
		os.system('echo \"nice-level = -11\" >> ~/.config/pulse/daemon.conf')
		os.system('echo \"realtime-scheduling = yes\" >> ~/.config/pulse/daemon.conf')
		os.system('echo \"realtime-priority = 9\" >> ~/.config/pulse/daemon.conf')
		os.system('echo \"rlimit-rtprio = 9\" >> ~/.config/pulse/daemon.conf')
		os.system('echo \"daemonize = no\" >> ~/.config/pulse/daemon.conf')

		#(3) write asound.conf with direct pulseaudio <-> kernel communication
		if self.daemonExperimental:
			os.system('sudo echo "pcm.!default {" >> /etc/asound.conf')
			os.system('sudo echo "   type plug" >> /etc/asound.conf')
			os.system('sudo echo "   slave.pcm hw" >> /etc/asound.conf')
			os.system('sudo echo "}" >> /etc/asound.conf')

		#(4) reset pulse audio 
		'''You may have to refresh your webpage if audio-stream interrupted'''
		self.resetPulse()

	def getResampleOptions(self):
		return self.resampleMethodMenu

	def setResampleMethod(self, choice):
		self.daemonResampleMethod = choice.get()

	def getResampleMethod(self):
		return self.daemonResampleMethod

	def getRateOptions(self):
		return self.sampleRateMenu

	def setSampleRate(self, choice):
		self.daemonRate = choice.get()

	def getSampleRate(self):
		return self.daemonRate

	def getSizeOptions(self):
		return self.sampleSizeMenu

	def getSize(self):
		return self.daemonSize

	def setSize(self, choice):
		self.daemonSize = choice.get()

def main():
	#Create master widget & center it on-screen
	master = Tk()
	master.eval('tk::PlaceWindow . center')

	#Create instance of DaemonInterface
	dInterface = DaemonInterface(master)

	#Get the current working directory
	cwd = os.getcwd()


	#Set Window Icon
	AudioBitIconPath = cwd + "/assets/icon.png"
	AudioBitIcon = PhotoImage(file=AudioBitIconPath)
	master.iconphoto(False, AudioBitIcon)
	
	#Set window title
	master.title('AudioBit')

	#Structuring the GUI presentation

	'''Setting up initial OptionMenu Vars'''
	resampleMethodVar = StringVar()
	resampleMethodVar.set("None Selected") 
	
	sampleRateVar = StringVar()
	sampleRateVar.set("None Selected")

	sampleSizeVar = StringVar()
	sampleSizeVar.set("None Selected")


	'''Resample Method Options'''
	resampleMethodFrame = Frame(master)
	resampleMethodLabel = Label(resampleMethodFrame, text="Resample Method:")
	resampleMethodOptionMenu = OptionMenu(resampleMethodFrame, resampleMethodVar, *dInterface.getResampleOptions(), command=dInterface.setResampleMethod)

	#pack the components
	resampleMethodFrame.pack(side=TOP, pady=10, fill=X)
	resampleMethodLabel.pack(side=LEFT, padx=20)
	resampleMethodOptionMenu.pack(side=RIGHT, padx=20)

	'''Sample Rate Options'''
	sampleRateFrame = Frame(master)
	sampleRateLabel = Label(sampleRateFrame, text="Sample Rate (in kHz):")
	sampleRateMenu = OptionMenu(sampleRateFrame, sampleRateVar, *dInterface.getRateOptions(), command=dInterface.setSampleRate)

	#pack the components
	sampleRateFrame.pack(side=TOP, pady=10, fill=X)
	sampleRateLabel.pack(side=LEFT, padx=20)
	sampleRateMenu.pack(side=RIGHT, padx=20)

	'''Sample Size Options'''
	sampleSizeFrame = Frame(master)
	sampleSizeLabel = Label(sampleSizeFrame, text="Sample Size:")
	sampleSizeMenu = OptionMenu(sampleSizeFrame, sampleSizeVar, *dInterface.getSizeOptions(), command=dInterface.setSize)

	#pack the components
	sampleSizeFrame.pack(side=TOP, pady=10, fill=X)
	sampleSizeLabel.pack(side=LEFT, padx=20)
	sampleSizeMenu.pack(side=RIGHT, padx=20)


	'''TODO Experimental direct Pulseaudio/Kernel communication'''


	'''Application Buttons'''
	applicationButtonsFrame = Frame(master)
	applyButton = Button(applicationButtonsFrame, text="Apply", command=dInterface.writeConfig)

	#pack the components
	applicationButtonsFrame.pack(side=TOP, pady=10, fill=X)
	applyButton.pack(side=RIGHT, padx=20)

	#Start Tkinter event loop
	master.mainloop()

main()
