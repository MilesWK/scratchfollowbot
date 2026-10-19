# Get Griffpatch, find top projects, get comments, follow from there
import scratchattach as sa
import time
import ast
import os
from dotenv import load_dotenv

load_dotenv()

BOT_USERNAME = os.getenv("USERNAME")
BOT_PASSWORD = os.getenv("PASSWORD")

##########################
#      GET USER LIST     #
##########################

def get_list_to_follow(): # gets users.
    start_time = time.perf_counter()

    users_to_follow = []

    griffpatch = sa.get_user("griffpatch")                       # the biggest scratcher, so the projects are guaranteed to have many commenters.
    griffpatch_project = griffpatch.projects(limit=1, offset=0)[0]  # we just need a project. Not 40 (for now)
    comment_offset = 0
    for x in range(0, 50):
        for item in griffpatch_project.comments(limit=100, offset=comment_offset): # get the comments in batches of 100, as less load all around (probably)
            users_to_follow.append(item.author_name)
        comment_offset+=100
        print(f"COMPLETED BATCH {x}/50  ")

    #print(users_to_follow)
    with open("userlist.txt", "a") as file:
        file.write(str(users_to_follow))

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print(f"Fetched {len(users_to_follow)} users in {elapsed_time:.6f} seconds.")


##########################
#      FOLLOW VIA LIST   #
##########################

def follow_by_file():
    with open("userlist.txt", "r") as file:
        user_list_as_file = file.read()
        

    user_list = ast.literal_eval(user_list_as_file)  
    user_list = list(set(user_list))
    x = 0
    session = sa.login(BOT_USERNAME, BOT_PASSWORD) 
    while x < len(user_list):
        user_to_follow = session.connect_user(user_list[x])
        try:
            user_to_follow.follow()
            print(f"FOLLOWED {user_to_follow.name}")
            x += 1
        except Exception as e:
            print(e)
            if "rate" in str(e):
                time.sleep(15)


follow_by_file()