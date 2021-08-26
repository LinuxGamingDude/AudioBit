# AudioBit
A Graphical Interface for adjusting important Linux Audio Settings

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

[5] Use the following command if you would like a way to test Audio Latency:
pacmd list-sinks | grep 'latency: [1-9]'


[5] May have undefined behavior if run outside of intended environment

[6] Run at your own risk

