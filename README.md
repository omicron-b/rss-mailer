# rss-mailer
Get your RSS feeds via email.  
This is a small personal project, so may not work for everyone.  
`rss-mailer.py` reads RSS feed urls from `feeds.txt`, saves timestamps from last posts, and emails you (or someone else) if there are updates.  

# prerequisites
- Python 3  
- `python3-feedparser`  
- being okay with some email account login and password being stored in plaintext in $HOME  

# warning
This software needs your email login and password in plain text in home folder. Please, do not use an important email account.  

# installation
`git clone https://github.com/omicron-b/reminder.git`  
- edit `feeds.txt`  
- edit `config.txt`, put your email credentials  
- `sudo mkdir /var/log/rss-mailer && sudo chown $USER:$USER /var/log/rss-mailer`  
- do not forget to setup a cron job. `rss-mailer.py` can be executed directly, no need to specify `python3` executable if Python 3 is correctly installed. Example:  
```
10,40 * * * * <your-path-to-script>/rss-mailer/rss-mailer.py 1> /dev/null 2>> /var/log/rss-mailer/log
```
This will execute twice every hour, at 10 and 40 minutes and append errors, if any, to `/var/log/rss-mailer/log`  
No need to set cron job as root, log file should be owned by `$USER`  
