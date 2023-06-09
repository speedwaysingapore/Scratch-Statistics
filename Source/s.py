import os
import requests
import scratchattach as scratch3
import scratchconnect
import json
import Logging as logging

s = os.environ['s']

session = scratch3.Session(s, username="YOURNAMEHERE")
conn = session.connect_cloud("Enter your project")

cookie = {"Username": "YOUR NAME HERE", "SessionID": s}

login = scratchconnect.ScratchConnect(online_ide_cookie=cookie)

client = scratch3.CloudRequests(conn)

@client.request
def seeifonline() -> str:
  print("Online!")
  return "Online"


@client.request
def statistics(user: str) -> list:
  print(f"Getting {user}")
  logging.log(f"Getting statistics for {user}")
  user = login.connect_user(user)
  appending = []
  appending.append(user.joined_date())
  appending.append(user.id())
  appending.append("following and follower count not provided") # Scratch API might provide them
  appending.append(user.bio())
  appending.append(user.work())
  appending.append(user.messages_count())
  print("Completed appending.")
  print(appending)
  return appending


@client.event
def on_ready() -> None:
  print("Handler is running currently!")


@client.request
def leaderboard(region: str, cat: str, page: str):
  data = []
  for i in range(50): 
    response = requests.get(f"https://scratchdb.lefty.one/v3/user/rank/{region}/{cat}/{page}").json()[i]['username']
    data.append(f"#{i+1}: {response}")
    print(f"{i}/50")
  return data

def run():
  client.run()
