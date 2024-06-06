A good chunk of my tangible work for CSC 429, a class based on running a real Debian Apache2 webserver and defending it against various real-time attacks.

Included are:
- Quite a few uptime checker scripts, both remote and local to the server.
- Some basic automatic fixes, in case of downtime.
- IDS in the form of monitoring directories with inotify, and custom canary executables. 
- An automated portscanner (Python nmap wrapper) to spot vulnerabilities in other groups' sites.
- Backups of the basic site functionality in the /site directory.

Basically anything that would be cause for alarm would alert both our Slack bot and PagerDuty on-call system.
(P.S., all of the "sensitive" webhooks, vulnerable URLs, etc. are already deleted before publishing. I'm not _that_ bad of a security professional :P)

Things I did but couldn't back up for various reasons:
- Set up cronjobs and an AWS EC-2 instance for all of the external checks.
- Patched countless vulnerabilities/downtimes/corruptions/etc. over the course of 10 weeks
- Breached an opposing team's Slack channel to social engineer their flags :^) (Sorry Group 9)
- Set up and renew TLS certs with Let's Encrypt (I <3 the EFF)
- And much more that I forgot to list...

This code was built solely with my own use in mind, so apologies for any jankiness.
It was a group project _on paper_, but I ended up doing everything aside from 1/2 of a script and 1/2 of a patch. You know how it goes.
