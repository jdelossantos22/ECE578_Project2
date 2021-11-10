import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx



def as_classify():
    files = ["20150801.as2types.txt", "20210401.as2types.txt"]
    for file in files:
        date = parse_date(file)
        data = read_file(file, "|")
        print(data)
        astypes = data.groupby(2).count()
        print(astypes)
        astypes = astypes.drop(1,axis=1)
        #astypes = as
        #print(astypes)
        plot = astypes.plot.pie(y=0, title="AS Classification - " + date, autopct='%1.1f%%', ylabel="(%) distribution of ASes", figsize=(5, 5))
    #plt.show()
    return

def as_links():
    file = "20211001.as-rel2.txt"
    data = read_file(file,"|")
    #print(data)
    #print(data)
    ids = pd.unique(data[[0,1]].values.ravel('K'))
    #print(ids)
    #2.2 graph 2

    peers_deg = get_peers(data)
    #print(peers_deg)
    non_peers = get_nonpeers(data)
    #<provider-AS>j<customer-AS>j -1 j<source>
    #group by provider-AS
    file = "routeviews-rv2-20211029-1800.pfx2as"
    ip_map = read_file(file, "\t")
    
    #print(ip_map)
    global_deg = get_global(data)
    customers_deg = get_customers(non_peers)
    providers_deg = get_providers(non_peers)
    #bins
    deg_bins = [0,1,2,6,101,201,1000]
    #print(peers_deg)
    
    #Section 2.2 graph 2
    plot_histogram(global_deg, deg_bins, 'deg', "Global Degree vs Number of AS")
    plot_histogram(customers_deg, deg_bins, 'deg', "Customer Degree vs Number of AS")
    plot_histogram(providers_deg, deg_bins, 'deg', "Provider Degree vs Number of AS")
    plot_histogram(peers_deg, deg_bins, 'deg', "Peer Degree vs Number of AS")
    
    #global_ip_space = ip_join_as(global_deg,ip_map)
    #customers_ip_space = ip_join_as(customers_deg,ip_map)
    #providers_ip_space = ip_join_as(providers_deg,ip_map)
    #peers_ip_space = ip_join_as(peers_deg,ip_map)

    ip_space = ip_join_as(data,ip_map)
    
    ip_bins = ip_space.groupby("Num_IPs").count()
    #print(ip_bins)
    ip_bins = ip_bins.index.tolist()
    #ip_bins = [16,256,512,2048,65536,1048576,4294967296]
    #section 2.2 graph 3
    plot_histogram(ip_space, ip_bins, 'Num_IPs', "IP Space of AS")
    

    #section 2.2 Graph 4
    #print(global_deg)
    #customers_deg = customers_deg.reset_index()
    #providers_deg = providers_deg.reset_index()
    #print(customers_deg)
    #print(providers_deg)
    #print(peers_deg)
    enterprise_as = global_deg[~global_deg.index.isin(customers_deg.index)]
    enterprise_as = enterprise_as[~enterprise_as.index.isin(peers_deg.index)]
    #print(enterprise_as)
    content_as = global_deg[~global_deg.index.isin(customers_deg.index)]
    content_as = content_as[content_as.index.isin(peers_deg.index)]
    #print(content_as)
    transit_as = global_deg[global_deg.index.isin(customers_deg.index)]
    #print(transit_as)
    size = [len(enterprise_as),len(content_as),len(transit_as)]
    labels = ["Enterprise AS", "Content AS", "Transit AS"]
    fig, ax = plt.subplots()
    ax.set_title("AS Classification")
    ax.pie(size,autopct='%1.1f%%',labels=labels)
    #ax.legend(this.patches, labels, loc="best")
    ax.axis('equal')
    #plt.show()
    
    print(non_peers)
    edges = non_peers.copy()
    edges = edges.drop([2,3], axis=1)
    print(edges)
    G = nx.DiGraph()
    G = nx.from_pandas_edgelist(edges, 0, 1)
    #plt.figure(figsize=(10, 8))
    #nx.draw_shell(G, with_labels=True)
    #plt.show()
    leaderboard = {}
    for x in G.nodes:
        leaderboard[x] = len(G[x])
    s = pd.Series(leaderboard, name='connections')
    conn_df = s.to_frame().sort_values('connections', ascending=False)
    print(conn_df)
    max_conn = conn_df.index.tolist()[0]
    #print(conn_df.index.tolist()[0])

    #section 2.3
    global_ranked = global_deg.sort_values(by = 'deg', ascending = False)
    #print(global_ranked)
    T1Clique = np.array([global_ranked['index'].iloc[0]])
    for i in range(1,50):
        NextAS = global_ranked['index'].iloc[i]
        NextLinks0 = data.loc[data[0] == NextAS]
        NextLinks1 = data.loc[data[1] == NextAS]
        count = 0
        for AS in T1Clique:
            if not AS in NextLinks0[1].values and not AS in NextLinks1[0]:
                break
            count = count + 1

        if count == T1Clique.size:
            T1Clique = np.append(T1Clique,NextAS)

        if  T1Clique.size >= 10 and not NextAS in T1Clique:
            break
    print (T1Clique)

    orgASData = read_file("20211001.as-org2info1.txt","|")
    orgOrgData = read_file("20211001.as-org2info.txt","|")
    print(orgASData)
    for AS in T1Clique:
        #print(orgASData.loc[orgASData[0] == AS,2].iloc[0])
        org_id = orgASData.loc[orgASData[0] == AS,3]
        #print(orgOrgData.loc[orgOrgData[0] == org_id.iloc[0],2].iloc[0])
        #print(global_ranked.loc[global_ranked['index'] == AS, 0].iloc[0])
        #print(global_ranked.loc[global_ranked['index'] == AS, 'deg'].iloc[0])

    #2.4 customer cone
    '''
    CustomerConeRanks = global_deg.copy()
    CustomerConeRanks["CustomerCone"] = list()
    CustomerConeRanks["visited"] = False
    for AS in non_peers:
        if not AS in CustomerConeRanks or CustomerConeRanks.empty:
            CustomerConeRanks, customerSubConeDegree, customerSubCone = immed_customers(CustomerConeRanks, non_peers, customers_deg, AS, list())
    '''
    
def find_all_paths(graph, start, path=[]):
    path = path + [start]
    paths = [path]
    if len(graph[start]) == 0:  # No neighbors
        print(path)
    for node in graph[start]:
        newpaths = find_all_paths(graph, node, path)
        for newpath in newpaths:
            paths.append(newpath)
    return paths
    

def immed_customers(CustomerConeRanks, non_peers, customers_deg, AS, CustomerCone):

    currentASdegree = customers_deg.loc[AS,0]        

    if currentASdegree == 0:
        newASrank = pd.DataFrame([AS, 0, list(), True])
        CustomerConeRanks.append(newASrank)
        return (CustomerConeRanks, 1, list(AS))

    for customer in non_peers.loc[AS].iloc[:,1]:
        if not customer in CustomerCone:
            CustomerConeRanks,customerSubConeDegree, customerSubCone = immed_customers(CustomerConeRanks, non_peers, customers_deg, customer, CustomerCone)
        else:
            continue
        currentASdegree += customerSubConeDegree
        CustomerCone.append(customerSubCone)

    if not AS in CustomerConeRanks:
        newASrank = pd.DataFrame([AS, customerSubConeDegree, customerSubCone, True])
        CustomerConeRanks.append(newASrank)

    return (CustomerConeRanks, currentASdegree, CustomerCone)
        
    
    
def plot_histogram(data, org_bins, column, title):
    data_list = data[column].tolist()
    data_list.sort()
    bins = org_bins.copy()
    max_deg = data_list[-1]
    
    #print(global_deg_list[-1])
    #print(max_deg)
    if max_deg > bins[-1]:
        bins.append(max_deg)
    #print(bins)
    #print(global_deg_list)
    #fig, ax = plt.subplots(figsize=(16, 10))
    #ax.hist(data_list, density=False, bins=bins)
    #print(data_list)
    #data_pct = data_list.div(data_list.sum(1),axis=0)
    hist, bin_edges = np.histogram(data_list, bins)#,weights=np.ones(len(data_list)) / len(data_list)
    fig, ax = plt.subplots(figsize=(16, 10))
    # Plot the histogram heights against integers on the x axis
    ax.bar(range(len(hist)), hist, width=1)
    # Set the ticks to the middle of the bars
    ax.set_xticks([0.5+i for i,j in enumerate(hist)])
    #ax.set_xlabel(bins)
    ax.set_title(title)
    # Set the xticklabels to a string that tells us what the bin edges were
    ax.set_xticklabels(['{} - {}'.format(bins[i],bins[i+1]) for i,j in enumerate(hist)])
    
    for rect in ax.patches:
        height = rect.get_height()
        ax.annotate(f'{int(height)}', xy=(rect.get_x()+rect.get_width()/2, height), 
                    xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')
    
    '''
    # Add this loop to add the annotations
    for p in ax.patches:
        width = p.get_width()
        height = p.get_height()
        print(height)
        x, y = p.get_xy() 
        ax.annotate(f'{height:.2%}', (x + width/2, y + height*1.0200), ha='center')
    '''
    
    
    return

def duplicate_rows(master_df, delimiter):
    multipl_as = master_df.loc[master_df[2].str.contains(delimiter)]
    #print(multipl_as)
    #print(multipl_as[2].str.split('_'))
    underscore = multipl_as[2].str.split(delimiter).apply(pd.Series,1).stack()
    #print(underscore)
    underscore.index = underscore.index.droplevel(-1)
    #print(underscore)
    underscore.name = 2
    #print(underscore)
    del multipl_as[2]
    #print(multipl_as)
    multipl_as = multipl_as.join(underscore)
    #print(multipl_as)
    master_df = master_df.drop(master_df.loc[master_df[2].str.contains(delimiter)].index)
    master_df = pd.concat([master_df, multipl_as])#, ignore_index=True
    master_df = master_df.reset_index()
    #print(master_df)
    return master_df

def ip_join_as(data, ip_prefix_as):
    #data is the types of degrees dataframe
    #Drop all rows with multiple AS separted by , or _
    #print(ip_prefix_as.loc[ip_prefix_as[2].str.contains("_")])3
    
    #ip_prefix_as = ip_prefix_as.reset_index
    ip_prefix_as = duplicate_rows(ip_prefix_as,'_')
    ip_prefix_as = duplicate_rows(ip_prefix_as,',')
    
    #change type from Object to int
    ip_prefix_as[2] = ip_prefix_as[2].astype('int64')
    
    #getting all rows in ip_prefix that exists in data
    #ip_as_exists = ip_prefix_as[ip_prefix_as[2].isin(data.index)]
    #print(data)
    ip_as_exists = ip_prefix_as
    
    ip_as_exists = ip_as_exists.assign(Num_IPs = lambda x: 2**(32 - x[1]))
    #ip_as_exists = ip_as_exists.assign(Num_AS = lambda x: data.loc[data[0] == x[2]])
    #ip_as_exists[3] =
    #print(ip_as_exists)
    return ip_as_exists
    

    

def ip_prefix_as(data=None):
    #2.2 graph 3
    #print(len(None))
    if (len(data) == 0):
        file = "routeviews-rv2-20211029-1800.pfx2as"
        data = read_file(file, "\t")
    
    #print(data)
    #ip_space = data.groupby(2).count().reset_index().drop(1, axis=1)
    #print(ip_space)
    

    
def get_global(data):
    as1 = data.groupby(0).count().drop([2,3], axis=1).rename(columns={1:0})
    as2 = data.groupby(1).count().drop([2,3], axis=1).rename(columns={1:0})
    as_sum = pd.concat([as1, as2])
    as_sum = as_sum.groupby(as_sum.index).sum()
    as_sum = as_sum.reset_index()
    as_sum = as_sum.rename(columns={0:"deg"})
    #print(as_sum)
    return as_sum

def get_providers(data):
    providers_deg = data.groupby(1).count().drop([2,3], axis=1).rename(columns={1:0})
    providers_deg = providers_deg.rename(columns={0:"deg"})
    return providers_deg

def get_customers(data):
    #group by provider-AS
    customer_deg = data.groupby(0).count().drop([2,3], axis=1).rename(columns={1:0})
    #customer_deg = customer_deg.reset_index()
    customer_deg = customer_deg.rename(columns={0:"deg"})
    #print(customer_deg)
    return customer_deg

def get_nonpeers(data):
    return data.loc[(data[2] == -1)]

def get_peers(data):
    peers = data.loc[(data[2] == 0)]
    #print(len(peers))
    peer1 = peers.groupby(0).count().drop([2,3], axis=1).rename(columns={1:0})
    peer2 = peers.groupby(1).count().drop([2,3], axis=1)
    #peers_sum = pd.concat([peer1, peer2]).groupby()
    #peer1.rename(columns={0:"id"},inplace=True)
    #print(peer1)
    #print(peer2)
    peers_sum = pd.concat([peer1, peer2])
    peers_sum = peers_sum.groupby(peers_sum.index).sum().reset_index()
    peers_sum = peers_sum.rename(columns={0:"deg"})
    #print(peers_sum)
    return peers_sum    
    
    

def read_file(filename, delimeter):
    data = pd.read_csv(filename, sep=delimeter,comment='#', header=None)
    return data

def parse_date(filename):
    date = filename[:4] + "-"+ filename[4:6] + "-" + filename[6:8]
    #print(date)
    return date
    

def main():
    '''
    data = pd.read_csv("20150801.as2types.txt", sep="|",comment='#', header=None)
    astypes = data.groupby(2).count()
    print(astypes)
    print(astypes.loc['Content',0])
    print(data)
    '''
    #2.1 graph 1a - 1b
    as_classify()
    #2.2 graph 2/3/4
    as_links()
    #ip_prefix_as()

if __name__ == "__main__":
    main() 