# Mackenzie Brown and Michael Newell
# Project Deliverable 1

# Best Friend Chain: 
# Use a modified Dijkstra’s algorithm to compute the highest-cost (weighted) path from User A to B
	
# New Friend Recommendation:
# Look at a user’s top three friends
# Look at each of those friend’s top three friends
# Determine who occurs most frequently (majority vote)
# Recommend that friend to a user (if it couldn’t be narrowed to one person, select randomly off a list)

# Popularity Score:
# See the average score of people who have you in their friend list.
# Loops through entire graph and determines average score for each person on the graph.

def read_file(filename):
    data = []
    infile = open(filename, 'r')
    lines = infile.readlines()
    for line in lines:
        line = line.strip()
        line = line.split(",")
        data.append(line)
    infile.close()

    return data

def create_user_data(data):
    users = {}
    user_id = 0
    for line in data:
        user1 = line[0]
        user2 = line[1]
        if (user1 not in users):
            users[user1] = user_id
            user_id = user_id + 1
        if (user2 not in users):
            users[user2] = user_id
            user_id = user_id + 1

    user_relationships = [[0 for _ in range(len(users))] for _ in range(len(users))]
    for line in data:
        user1 = line[0]
        user2 = line[1]
        friendship_score = int(line[2])
        user1_index = users[user1]
        user2_index = users[user2]
        user_relationships[user1_index][user2_index] += friendship_score
    return users, user_relationships

def menu(all_users, user_relationships):
    print("What do you want to do?")
    print("1) Check if user exists")
    print("2) Check connection between users")
    print("3) Quit")
    selection = int(input("> "))
    if(selection == 1):
        user = input("what user? ")
        if user in all_users:
            print(user + " does exist.")
        else:
            print(user + " doesn't exist.")
        menu(all_users, user_relationships)
    if(selection == 2):
        users = input("what users (separated by spaces)? ")
        users = users.split()
        user1 = users[0]
        user2 = users[1]
        if(user1 not in all_users or user2 not in all_users):
            print("Error: one of these users does not exist.")
        else:
            user1_index = all_users[user1]
            user2_index = all_users[user2]
            score = user_relationships[user1_index][user2_index]
            print("The connection from "+user1+" to "+user2+" has weight "+str(score))
        menu(all_users, user_relationships)
    if(selection == 3):
        return



def main():
    data = read_file("friends.txt")
    all_users, user_relationships = create_user_data(data)
    menu(all_users, user_relationships)

if __name__ == "__main__":
    main()