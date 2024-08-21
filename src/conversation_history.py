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
    current_message = []
    current_timestamp = None
    current_role = None

    for line in lines:
        if line.strip():
            try:
                timestamp, role, content = line.strip().split(",", 2)
                
                if current_message:
                    conversation.append({
                        "role": current_role,
                        "content": "\n".join(current_message)
                    })
                
                current_message = [content]
                current_timestamp = timestamp
                current_role = role
            except ValueError:
                current_message.append(line.strip())

    if current_message:
        conversation.append({
            "role": current_role,
            "content": "\n".join(current_message)
        })

    return conversation

def check_file_age(channel_id):
  filename = f"conversation_{channel_id}.txt"
  if os.path.exists(filename):
      file_age = time.time() - os.path.getmtime(filename)
      if file_age > 1 * 3600:
          os.remove(filename)