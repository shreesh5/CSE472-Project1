import pickle
import cPickle


with open('half_network/social_network_1.pkl', 'rb') as f:
    sn_1  = pickle.load(f)
with open('half_network/social_network_2.pkl', 'rb') as f:
    sn_2  = pickle.load(f)

key_1 = sn_1.keys()
key_2 = sn_2.keys()
len(key_1)
len(key_2)
set(key_1).intersection(key_2)

sn_1.update(sn_2)
len(sn_1)

with open('social_network.pkl', 'wb') as f:
    pickle.dump(sn_1, f)
