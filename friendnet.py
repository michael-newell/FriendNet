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
import math
import operator
import random

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
	print("3) Find best friend chain")
	print("4) Get a user reccomendation")
	print("5) Calculate a popularity score")
	print("6) Quit")
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
		users = input("what users (separated by spaces)?")
		users = users.split()
		user1 = users[0]
		user2 = users[1]
		if(user1 not in all_users or user2 not in all_users):
			print("Error: one of these users does not exist.")
		else:
			user1_index = all_users[user1]
			user2_index = all_users[user2]
			chain = best_friend(user1_index, user2_index, all_users, user_relationships)
			for i in chain:
				for name, value in all_users.items():
					if i == value:
						print(" -> " + str(name))

			menu(all_users, user_relationships)
	if(selection == 4):
		user = input("Find reccomendation for what user? ")
		if(user not in all_users):
			print("Error: this user does not exist.")
		else:
			user_index = all_users[user]
			friend_recommendation(all_users, user_relationships, user_index, 3, [])
			print()
			menu(all_users, user_relationships)

	if(selection == 5):
		user = input("Calculate popularity score for what user? ")
		if(user not in all_users):
			print("Error: this user does not exist.")
		else:
			user_index = all_users[user]
			popularity_score(all_users, user_relationships, user_index)
			print()
			menu(all_users, user_relationships)
	if(selection == 6):
		return

def invert_relationships(user_relationships):
	inverted_user_relationships = []
	for row in user_relationships:
		new_row = []
		for relationship in row:
			if (relationship == 0):
				new_row.append(0)
			else:
				new_relationship = 11 - relationship
				new_row.append(new_relationship)
		inverted_user_relationships.append(new_row)
	return inverted_user_relationships

def friend_recommendation(all_users, user_relationship, user, iterations, total):
	index = user
	relationships= user_relationship[index]
	relationships_dict = {}
	for index, x in enumerate(relationships):
		relationships_dict[index] = x
	sorted_friends = sorted(relationships_dict.items(), key=operator.itemgetter(1))
	top_3_friends = []
	i = -1
	for _ in range(3):
		friend = sorted_friends[i]
		if friend[1] == 0:
			continue
		else:
			top_3_friends.append(sorted_friends[i])
		i-=1
	
	top_friends_tally = {}
	for friend in top_3_friends:
		if friend[0] in top_friends_tally:
			top_friends_tally[friend[0]] += 1
		else:
			top_friends_tally[friend[0]] = 1
	total.append(top_friends_tally)
	
	if(iterations == 1):
		recommendation(all_users, user_relationship, user, total)
		return total
	else:
		for key in top_friends_tally:
			val = iterations - 1
			friend_recommendation(all_users, user_relationship, key, val, total)
def recommendation(all_users, user_relationships, user, total):
	options = total[1:]
	recommendations = []
	for option in options:
		for friend in option:
			# Add it to the list even if it is already in there. This will act as a weight. If a friend
			# recommendation appears in multiple lists, it is a stronger recommendation and should have 
			# a higher liklihood of being randomly selected
			recommendations.append(friend)
	if(len(recommendations) == 0):
		print("Sorry, we don't have any recommendations for you!")
	else:
		selection = random.randrange(0, len(recommendations))
		user_index = recommendations[selection]
		selected_user = list(all_users.keys())[list(all_users.values()).index(user_index)]
		print("We recommend adding "+selected_user+" as a user!")

def popularity_score(all_users, user_relationships, user):
	user_index = user
	score = 0
	friend_count = 0
	for index, row in enumerate(user_relationships):
		if(index == user_index):
			continue
		else:
			if(row[user_index] != 0):
				friend_count += 1
			score += row[user_index]
	score = score/friend_count
	user_name = list(all_users.keys())[list(all_users.values()).index(user_index)]
	print(user_name+" has a popularity score of "+str(score))

def best_friend(user_index1, user_index2, all_users, user_relationships):
	relationships = invert_relationships(user_relationships)
	path = []
	distances = {}
	prevUsers = {}
	visited = [user_index1]
	user = user_index1
	minimum = math.inf
	count = 0

	for i in range(len(relationships[user_index1])):
		distances[i] = relationships[user_index1][i]
		prevUsers[i] = user_index1
		if relationships[user_index1][i] > 0:
			count += 1
		if relationships[user_index1][i] <= 0:
			distances.pop(i, None) #only contains direct links
			#prevUsers.pop(i, None)

	if count == 0:
		print("Path does not exist")
		return path
	elif count == 1:
		for i in distances:
			if list(distances.keys()).index(i) > 0:
				if list(distances.keys()).index(i) == user_index2:
					return [user_index2]


	if relationships[user_index1][user_index2] > 0:
		distances[user_index2] = relationships[user_index1][user_index2]
	else:
		distances[user_index2] = math.inf
	distances[user_index1] = 0
	while len(visited) != len(distances):
		if len(visited) == len(distances) - 1:
			if distances[user_index2] == math.inf and user_index2 not in visited:
				print("Path does not exist")
				return path
		for i in range(len(relationships[user])):
			if relationships[user][i] != 0 and (i not in visited):
				if relationships[user][i] <= minimum:
					minimum = relationships[user][i]
					index = i

		if user not in visited:
			visited.append(user)
		if minimum == math.inf:
			user = prevUsers[user]
		else:
			if index not in distances:
				distances[index] = relationships[user][index] + distances[user]
				prevUsers[index] = user
			else:
				distances[index] = min(relationships[user][index] + distances[user], distances[index])
				if distances[index] == relationships[user][index] + distances[user]:
					prevUsers[index] = user
			user = index
		minimum = math.inf

	# print(prevUsers)
	if distances[user_index2] == math.inf:
		print("Path does not exist")
	else:
		user = user_index2
		while (user != user_index1):
			path = [user] + path
			user = prevUsers[user]
	# print("Total best-friend chain score: ")
	return path


def main():
	data = read_file("friends.txt")
	all_users, user_relationships = create_user_data(data)
	invert = invert_relationships(user_relationships)
	menu(all_users, user_relationships)

if __name__ == "__main__":
	main()
