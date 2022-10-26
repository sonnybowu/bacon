#!/usr/bin/env python3

from cgitb import small
import pickle

# NO ADDITIONAL IMPORTS ALLOWED!

# This function mutates our data to have the correct bacon number
def bacon_number(data):
    kevin_bacon_id = 4724
    visited_actors = set()
    previous_set = []
    #We want to start by considering the actors who have been in a movie with Kevin Bacon or have Bacon number of 1
    #Add Bacon to visited_actors and his bacon number remains 0
    visited_actors.add(kevin_bacon_id)
    #Add all the actors that have acted with Bacon to visited_actors and give them a bacon number of 1
    for actor in data[kevin_bacon_id]['acted_with']:
        if actor == kevin_bacon_id:
            continue
        visited_actors.add(actor)
        previous_set.append(actor)
        data[actor]['bacon_number'] = 1
    while previous_set:
        l = []
        for actor in previous_set:
            for acted_with in data[actor]['acted_with']:
                if acted_with not in visited_actors:
                    data[acted_with]['bacon_number'] = data[actor]['bacon_number'] + 1
                    visited_actors.add(acted_with)
                    l.append(acted_with)
        previous_set = l
    return None
                
def transform_data(raw_data):
    '''Data representation will be a dictionary of the form {actor_id: {'acted_with': {actor...}, 'bacon_number': bacon number}}'''
    data = {}
    for actor1, actor2, movie_id in raw_data:
        # Check if actor 1 has been scanned already, if not add it to database and say they have acted with themselves and actor2
        if actor1 not in data:
            data[actor1] = {'acted_with': {actor1, actor2}, 'bacon_number': 0, 'acted_with_movies': {actor2: movie_id}, 'movies': {movie_id}}
        # Case where actor1 is already in data then just add actor 2 to acted_with set
        else:
            data[actor1]['acted_with'].add(actor2)
            data[actor1]['acted_with_movies'][actor2] = movie_id
            data[actor1]['movies'].add(movie_id)
        # Check if actor 2 has been scanned already, if not add it to database and say they have acted with themselves and actor1
        if actor2 not in data:
            data[actor2] = {'acted_with': {actor2, actor1}, 'bacon_number': 0, 'acted_with_movies': {actor1: movie_id}, 'movies': {movie_id}}
        # Case where actor2 is already in data then just add actor 1 to acted_with set
        else:
            data[actor2]['acted_with'].add(actor1)
            data[actor2]['acted_with_movies'][actor1] = movie_id
            data[actor2]['movies'].add(movie_id)
    bacon_number(data)
    return data

def acted_together(transformed_data, actor_id_1, actor_id_2):
    # if actor is the list of actors acted with then they have acted together
    if actor_id_1 in transformed_data[actor_id_2]['acted_with']:
        return True
    return False


def actors_with_bacon_number(transformed_data, n):
    s = set()
    for actor in transformed_data:
        if transformed_data[actor]['bacon_number'] == n:
            s.add(actor)
    return s


def bacon_path(transformed_data, actor_id):
    return actor_to_actor_path(transformed_data, 4724, actor_id)
    # if actor_id not in transformed_data:
    #     return None
    # l = []
    # #Add actor ID first so it becomes last element in list
    # l.append(actor_id)
    # kevin_bacons_id = 4724
    # current_actor = actor_id
    # #Terminate when we reach Kevin Bacon
    # while current_actor != kevin_bacons_id:
    #     #Get a set of actors that have n-1 bacon number than current one
    #     actors_closer_to_kevin = actors_with_bacon_number(transformed_data, transformed_data[current_actor]['bacon_number'] - 1)
    #     #Seach through the set to find a connecting actor and add it to the list
    #     for actor in actors_closer_to_kevin:
    #         if actor in transformed_data[current_actor]['acted_with']:
    #             l.insert(0, actor)
    #             #Move to the connecting actor and algorithm will repeat
    #             current_actor = actor
    #             break
    # return l

def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    #Perform BFS
    current_actor = actor_id_1
    target_actor = actor_id_2
    queue = [(current_actor, [current_actor])]
    visited_actors = set()

    while queue:
        current_actor, path = queue.pop(0)
        visited_actors.add(current_actor)
        for actor in transformed_data[current_actor]['acted_with']:
            if actor == target_actor:
                return path + [target_actor]
            elif actor not in visited_actors:
                visited_actors.add(actor)
                #Add the path with the next actor in it
                queue.append((actor, path + [actor]))

def actor_path(transformed_data, actor_id_1, goal_test_function):
    #Perform BFS
    current_actor = actor_id_1
    queue = [(current_actor, [current_actor])]
    visited_actors = set()

    while queue:
        current_actor, path = queue.pop(0)
        visited_actors.add(current_actor)
        for actor in transformed_data[current_actor]['acted_with']:
            if goal_test_function(actor):
                return path + [actor]
            elif actor not in visited_actors:
                visited_actors.add(actor)
                #Add the path with the next actor in it
                queue.append((actor, path + [actor]))

def actors_connecting_films(transformed_data, film1, film2):
    data = transformed_data.keys()
    actors_in_film2 = set()
    #Get all actors that are in film2 to be used for goal test function
    for actor_id in data:
        if film2 in transformed_data[actor_id]['movies']:
            actors_in_film2.add(actor_id)
    l = {}
    #Find the shortest chain of actors from film1 to film2
    for actor_id in data:
        if film1 in transformed_data[actor_id]['movies']:
            l[len(actor_path(transformed_data, actor_id, lambda p: p in actors_in_film2))] = actor_path(transformed_data, actor_id, lambda p: p in actors_in_film2)
    #If no path exists return none
    if not l:
        return None
    #Return the shortest out of all the valid paths
    return l[min(l)]

if __name__ == "__main__":
    with open("resources/large.pickle", "rb") as f:
        smalldb = pickle.load(f)

    with open("resources/names.pickle", "rb") as f:
        namedb = pickle.load(f)

    with open("resources/movies.pickle", "rb") as f:
        moviedb = pickle.load(f)

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    # print(list(smalldb.keys())[list(smalldb.values()).index(1357022)])
    # print(smalldb['Sydney Tafler'])
    test = transform_data(smalldb)
    print(namedb['Janne \'Loffe\' Carlsson'], namedb['Miko Hughes'])
    l = actor_to_actor_path(test, namedb['Josh Groban'], namedb['Anton Radacic'])
    s = []
    for i in range(len(l) - 1):
        s.append(test[l[i]]['acted_with_movies'][l[i + 1]])
    g = []
    for id in s:
        g.append(list(moviedb.keys())[list(moviedb.values()).index(id)])
    print(g)