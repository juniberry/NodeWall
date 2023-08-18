#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
wall.py

Title: NodeWall
Description: 
Author: Daria Juniper -- juniberry@github
Created: March 2023
Version: 1.0


Changelog:
* readability improvements
* beta has been improved and cleaned up, config file added for usability
* datetime sorting bug with sqlite fix
"""

import sys
import os
import sqlite3
import datetime
import configparser

# get the directory path of the running script
script_path = os.path.dirname(os.path.abspath(__file__))

# build paths to required files
config_file_path = os.path.join(script_path, 'wall.ini')
db_file_path = os.path.join(script_path, 'wall.db')

# load config file
config = configparser.ConfigParser()
config.read(config_file_path)

# connect to the database
conn = sqlite3.connect(db_file_path)
c = conn.cursor()

# create a table for the wall messages
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              callsign TEXT,
              message TEXT,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

# get the user's callsign
callsign = input().strip()
print(config['wall']['banner'])

# show the latest entries on the wall
num_entries = config['posts'].getint('perpage')
max_message_length = config['posts'].getint('maxlen')

start_index = 0

while True:
    c.execute("SELECT COUNT(*) FROM messages")
    num_messages = c.fetchone()[0]

    if start_index <= 0:
        start_index = 0

    c.execute("SELECT * FROM messages ORDER BY timestamp DESC LIMIT ? OFFSET ?", (num_entries, start_index))
    rows = c.fetchall()
    if rows:
        print("\nPosts {0}-{1} of {2}:".format(start_index+1, start_index+len(rows), num_messages))
        for row in rows:
            date_string = datetime.datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S').strftime('(%d-%b %H:%M)')
            print(date_string, "<", row[1], ">", row[2])
    else:
        print("\nNo more posts to show.")

    # present options to the user
    print("\n[P]ost a message [B]ack [F]orward [D]elete E[x]it")
    choice = input().lower().strip()

    if choice == "p":
        # ask the user for a message
        message = input("Enter your post (limit {0} characters): ".format(max_message_length)).strip()[:max_message_length]

        if message:
            # Check if the message starts with "*** Disconnected from"
            if message.startswith("*** Disconnected from"):
                conn.close()
                sys.exit()
            # insert the message into the database
            c.execute("INSERT INTO messages (callsign, message) VALUES (?, ?)", (callsign, message))
            conn.commit()
            print("Posted to the wall.")
        else:
            print("Not posted as it was empty.")
    elif choice == "b":
        # move the start index back by num_entries
        start_index = max(0, start_index - num_entries)
    elif choice == "f":
        # move the start index forward by num_entries
        start_index = min(num_messages - num_entries, start_index + num_entries)
    elif choice == "d":
        # delete the user's latest message
        c.execute("SELECT * FROM messages WHERE callsign=? ORDER BY timestamp DESC LIMIT 1", (callsign,))
        row = c.fetchone()
        if row:
            confirm = input("Delete your latest post? (y/n): ").strip().lower()
            if confirm == "y":
                c.execute("DELETE FROM messages WHERE id=?", (row[0],))
                conn.commit()
                print("Post deleted.")
        else:
            print("You have not posted.")
    elif choice == "x":
        # cleanup and exit
        conn.close()
        print(config['wall']['exitmsg'])
        break
    else:
        print("Invalid choice.")
