import os
import time

def write_to_file(channel_id, role, content):
  filename = f"conversation_{channel_id}.txt"
  with open(filename, "a") as f:
      timestamp = time.time()
      f.write(f"{timestamp},{role},{content}\n")
      
def read_from_file(channel_id):
  filename = f"conversation_{channel_id}.txt"
  if not os.path.exists(filename):
      return []

  with open(filename, "r") as f:
      lines = f.readlines()

  conversation = []
  for line in lines:
      timestamp, role, content = line.strip().split(",", 2)
      conversation.append({"role": role, "content": content})

  return conversation

def check_file_age(channel_id):
  filename = f"conversation_{channel_id}.txt"
  if os.path.exists(filename):
      file_age = time.time() - os.path.getmtime(filename)
      if file_age > 3 * 3600:
          os.remove(filename)