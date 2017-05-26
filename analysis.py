def opinions_clusters(model, threshold=.05):
    '''
    Returns a list length #of clusters of dictionaries.
    Each dictionary contains the value of the opinion centers as
    keys, with the number of agents at the opinion centers as values.
    
    Keyword arguments:
    model -- An instance of OpinionModel.
    threshold -- a float. For large alpha/learning rates, a larger
    threshold may be used within reasonable limits. Large learning
    rates cause unclear/unstable behavior.
    '''
    num_agents = model.num_agents
    num_opinions = len(model.initial_opinions[0])
    opinions_clusters_list = []
    for opinion in range(num_opinions):
        clusters = {}
        for agent in range(num_agents):
            agent_opinion = model.schedule.agents[agent].opinions[opinion]
            found_in_clusters = 0
            for key in clusters:
                if abs(agent_opinion - key) < threshold:
                    clusters[key] += 1
                    found_in_clusters = 1
                    break;
            if not found_in_clusters:
                clusters[agent_opinion] = 1
        opinions_clusters_list.append(clusters)
    return opinions_clusters_list

def num_clusters(model, threshold=.2):
    '''
    Returns a list, with the number of clusters occurring in each
    opinion as values on indices.

    Keyword arguments:
    model -- An instance of OpinionModel.
    threshold -- a float. For large alpha/learning rates, a larger
    threshold may be used within reasonable limits. Large learning
    rates cause unclear/unstable behavior.
    '''
    opinions_clusters_list = opinions_clusters(model, threshold)
    num_list = []
    for entries in opinions_clusters_list:
        num_list.append(len(entries))
    return num_list
