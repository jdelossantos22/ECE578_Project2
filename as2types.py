import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np


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
        plot = astypes.plot.pie(y=0, title="AS Classification - " + date, ylabel="(%) distribution of ASes", figsize=(5, 5))
    plt.show()
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
    deg_bins = [0,1,2,5,100,200,1000]
    print(peers_deg)
    
    plot_histogram(global_deg, deg_bins, 'deg')
    plot_histogram(customers_deg, deg_bins, 'deg')
    plot_histogram(providers_deg, deg_bins, 'deg')
    plot_histogram(peers_deg, deg_bins, 'deg')


    #print(global_deg[0])
    #test = global_deg["deg"].tolist()
    #test = [x for x in test if x > 1000]
    #print(global_deg["deg"])
    #print(global_deg.groupby("deg").count())
    #print(np.clip(global_deg["deg"], deg_bins[0], deg_bins[-1]))
    #plt.hist(global_deg["deg"], bins=deg_bins)
    #global_hist = global_deg.hist(column="deg",bins=[0,1,2,5,100,200,1000])
    #print(global_deg)
    
    #global_hist = global_deg.hist(column="deg", bins=deg_bins)
    #print(global_hist)
    #plt.hist(global_deg["deg"])
    
    
    #global_ip_space = ip_join_as(global_deg,ip_map)
    #customers_ip_space = ip_join_as(customers_deg,ip_map)
    #providers_ip_space = ip_join_as(providers_deg,ip_map)


    #histograms
    
    #test_ip = global_ip_space[1].tolist()
    #test_ip = [x for x in test_ip if x == 32]
    #print(len(test_ip))
    #test = global_ip_space.groupby("Num_IPs").count()
    #print(test)
    #bins = [0,1,2,5,100,200,1000]
    #print(global_ip_space.groupby("Num_IPs").count())
    
    #global_hist = global_ip_space.hist(column="Num_IPs", bins=[0,1,2,5,100,200,1000, np.Inf])
    #customers_hist = customers_ip_space.hist(column="Num_IPs", bins=[0,1,2,5,100,200,1000, np.Inf])
    #providers_hist = providers_ip_space.hist(column="Num_IPs", bins=[0,1,2,5,100,200,1000, np.Inf])
    #plt.hist(np.clip(global_ip_space["Num_IPs"], bins[0], bins[-1]), bins=bins)
    #section 2.2 Graph 4
    #print(non_peers)
    plt.show()
    

    '''
    providers_as = non_peers[[0]].values.ravel('K')
    print(providers_as)
    customer_as = non_peers[[1]].values.ravel('K')
    enterprise_as = [id for id in ids if(id in providers_as and id not in customer_as)]
    print(enterprise_as)
    peers_as = peers_deg.values.ravel('K')
    '''
def plot_histogram(data, org_bins, column):
    data_list = data[column].tolist()
    data_list.sort()
    bins = org_bins.copy()
    max_deg = data_list[-1]
    
    #print(global_deg_list[-1])
    #print(max_deg)
    if max_deg > bins[-1]:
        bins.append(max_deg)
    print(bins)
    #print(global_deg_list)
    #fig, ax = plt.subplots(figsize=(16, 10))
    #ax.hist(data_list, density=False, bins=bins)
    hist, bin_edges = np.histogram(data_list, bins)
    fig, ax = plt.subplots(figsize=(16, 10))
    # Plot the histogram heights against integers on the x axis
    ax.bar(range(len(hist)), hist, width=1)
    # Set the ticks to the middle of the bars
    ax.set_xticks([0.5+i for i,j in enumerate(hist)])
    # Set the xticklabels to a string that tells us what the bin edges were
    ax.set_xticklabels(['{} - {}'.format(bins[i],bins[i+1]) for i,j in enumerate(hist)])
    
    for rect in ax.patches:
        height = rect.get_height()
        ax.annotate(f'{int(height)}', xy=(rect.get_x()+rect.get_width()/2, height), 
                    xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')
    
    return

def ip_join_as(data, ip_prefix_as):
    #data is the types of degrees dataframe
    #Drop all rows with multiple AS separted by , or _
    ip_prefix_as = ip_prefix_as.drop(ip_prefix_as.loc[ip_prefix_as[2].str.contains("_")].index)
    ip_prefix_as = ip_prefix_as.drop(ip_prefix_as.loc[ip_prefix_as[2].str.contains(",")].index)
    
    #change type from Object to int
    ip_prefix_as[2] = ip_prefix_as[2].astype('int64')
    
    #getting all rows in ip_prefix that exists in data
    ip_as_exists = ip_prefix_as[ip_prefix_as[2].isin(data.index)]
    #print(data)
    
    ip_as_exists = ip_as_exists.assign(Num_IPs = lambda x: 2**(32 - x[1]))
    #ip_as_exists = ip_as_exists.assign(Num_AS = lambda x: data.loc[data[0] == x[2]])
    #ip_as_exists[3] =
    print(ip_as_exists)
    return ip_as_exists
    

    

def ip_prefix_as():
    #2.2 graph 3
    file = "routeviews-rv2-20211029-1800.pfx2as"
    data = read_file(file, "\t")
    print(data)
    ip_space = data.groupby(2).count().reset_index().drop(1, axis=1)
    print(ip_space)
    

    #for id in ids:
        #peers
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
    #as_classify()
    as_links()
    #ip_prefix_as()

if __name__ == "__main__":
    main() 