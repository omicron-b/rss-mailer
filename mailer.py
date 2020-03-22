#!/usr/bin/env python3

try:
    from feedparser import parse as fparse
except ModuleNotFoundError:
    print('Error importing module.\n', \
    'Please, install python3-feedparser', sep='')
    exit()
import smtplib
from email.message import EmailMessage
from pathlib import Path
from configparser import ConfigParser

config_file = ''.join((str(Path(__file__).parent), '/config.txt'))
url_file = ''.join((str(Path(__file__).parent), '/feeds.txt'))
config = ConfigParser()
config.read(config_file)

def get_urls(file):
    """Gets URLs from feeds.txt"""
    with open(file, 'r') as f:
        urls = list()
        for row in f:
            urls.append(row.strip('\n'))
    return urls

def get_rss_data(urls_list):
    """Gets RSS data and returns only relevant fields."""
    feeds_in = {}
    feeds_out = {}
    try:
        for line in urls_list:
            feeds_in[line] = fparse(line)
            feeds_out[line] = {'published': feeds_in[line].entries[0].published}
            feeds_out[line]['title'] = feeds_in[line].feed.title
            feeds_out[line]['post'] = feeds_in[line].entries[0].title
            feeds_out[line]['link'] = feeds_in[line].entries[0].link
    except IndexError:
        print('Not able to get any feeds. Are there valid URLs in feeds.txt?')
    return feeds_out

def send_mail(title, published, post, link):
    """Prepares and sends emails, one for each feed."""
    host = config.get('smtp', 'server')
    port = config.get('smtp', 'port')
    address = config.get('smtp', 'to')
    sender = config.get('smtp', 'from')

    text = '''
Feed updated, latest post: {}\n
Link: {}\n
Published: {}\n
'''.format(post, link, published)

    body = '\n'.join((
        'From: %s' % sender,
        'To: %s' % address,
        'Subject: %s' % title,
        '',
        text
    ))

    server = smtplib.SMTP(host, port)
    server.starttls()
    server.ehlo()
    server.login(config.get('smtp', 'login'), config.get('smtp', 'password'))
    server.sendmail(sender, [address], body.encode('utf-8'))
    server.quit()

def check_updates(feeds_dict):
    """Checks for updates and calls relevant functions."""
    count = 0  # Used for saving state files

    def state_update(file):
        """Updates state file."""
        try:
            with open(file, 'w') as write_file:
                write_file.write(feeds_dict[key]['published'])
        except IOError as e:
            print('Could not write feed states. Please, check write permission for "state/"')
            raise e

    for key in feeds_dict:
        updates_detected = False
        first_run = False
        state_file = ''.join((str(Path(__file__).parent), '/state/feed{}.state'.format(count)))
        # Detecting first run for each feed
        if Path(state_file).is_file() == False:
            state_update(state_file)
            first_run = True
        # Main loop
        try:
            with open(state_file, 'r') as read_file:
                for line in read_file:
                    # Detecting updates for each feed
                    if line != feeds_dict[key]['published']:
                        updates_detected = True
            if updates_detected and first_run != True:
                # Calling state_update and send_mail as normal operation
                state_update(state_file)
                send_mail(feeds_dict[key]['title'], feeds_dict[key]['published'], feeds_dict[key]['post'], feeds_dict[key]['link'])
        except IOError as e:
            print('Could not read feed states. Please, check read permission for "state/"')
            raise e
        count += 1

check_updates((get_rss_data(get_urls(url_file))))
