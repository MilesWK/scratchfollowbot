# Get Griffpatch, find top projects, get comments, follow from there
import scratchattach as sa
import time

def get_list_to_follow():
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
    
get_list_to_follow()