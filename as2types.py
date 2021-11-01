import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np

def as_classify():
    files = ["20150801.as2types.txt", "20210401.as2types.txt"]
    for file in files:
        date = parse_date(file)
        data = read_file(file, "|")
        astypes = data.groupby(2).count()
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
    ids = pd.unique(data[[0,1]].values.ravel('K'))
    #print(ids)
    #2.2 graph 2
    global_deg = get_global(data)
    peers_deg = get_peers(data)
    non_peers = get_nonpeers(data)
    #<provider-AS>j<customer-AS>j -1 j<source>
    #group by provider-AS
    customers_deg = get_customers(non_peers)
    providers_deg = get_providers(non_peers)


    

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
    as_sum = as_sum.groupby(as_sum.index).sum().reset_index()
    return

def get_providers(data):
    providers_deg = data.groupby(1).count().drop([2,3], axis=1).rename(columns={1:0})
    return providers_deg

def get_customers(data):
    #group by provider-AS
    customer_deg = data.groupby(0).count().drop([2,3], axis=1).rename(columns={1:0})
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
    #as_links()
    ip_prefix_as()

if __name__ == "__main__":
    main() 