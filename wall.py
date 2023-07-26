#!/usr/bin/python3

# wall.py
# Packet Node Graffiti Wall
# digitaljackalope@github Mar-2023
# ...nothing fancy...

import sys
import sqlite3
import datetime

# connect to the database
conn = sqlite3.connect('/home/bpquser/wall.db')
c = conn.cursor()

# create a table for the wall messages
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              callsign TEXT,
              message TEXT,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

# get the user's callsign
callsign = input().strip()
print("-=- Node Wall -=-")

# show the latest entries on the wall
num_entries = 10  # change this to control the number of entries shown
max_message_length = 140  #change this to the maxium wall entry size you allow

start_index = 0

while True:
    c.execute("SELECT COUNT(*) FROM messages")
    num_messages = c.fetchone()[0]

    c.execute("SELECT * FROM messages ORDER BY timestamp ASC LIMIT ? OFFSET ?", (num_entries, start_index))
    rows = c.fetchall()
    if rows:
        print("\nShowing entries {0}-{1} of {2}:".format(start_index+1, start_index+len(rows), num_messages))
        for row in rows:
            date_string = datetime.datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M')
            print(date_string, "-", row[1], ":", row[2])
    else:
        print("\nNo more entries to show.")

    # present options to the user
    print("\n[P]ost a message [B]ack [F]orward [D]elete E[x]it")
    choice = input().lower().strip()

    if choice == "p":
        # ask the user for a message
        message = input("Enter your message (limit {0} characters): ".format(max_message_length)).strip()[:max_message_length]

        if message:
            # Check if the message starts with "*** Disconnected from"
            if message.startswith("*** Disconnected from"):
                print("Disconnect detected, ignoring post.")
                conn.close()
                sys.exit()

            # insert the message into the database
            c.execute("INSERT INTO messages (callsign, message) VALUES (?, ?)", (callsign, message))
            conn.commit()
            print("Message posted to the wall.")
        else:
            print("Message was not posted as it was empty or null.")
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
            confirm = input("Are you sure you want to delete your latest message? (y/n): ").strip().lower()
            if confirm == "y":
                c.execute("DELETE FROM messages WHERE id=?", (row[0],))
                conn.commit()
                print("Message deleted.")
        else:
            print("You have not posted any messages.")
    elif choice == "x":
        # exit the program
        conn.close()
        print("Returning to Node.")
        break
    else:
        print("Invalid choice. Please try again.")
