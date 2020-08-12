from spotframework.net.network import Network as Spotnet, NetworkUser
from fmframework.net.network import Network as Fmnet
from spotfm.timer import time, seconds_to_time_str

import logging
import os

spotframework_logger = logging.getLogger('spotframework')
fmframework_logger = logging.getLogger('fmframework')
spotfm_logger = logging.getLogger('spotfm')

log_format = '%(levelname)s %(name)s:%(funcName)s - %(message)s'
formatter = logging.Formatter(log_format)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

spotframework_logger.addHandler(stream_handler)
fmframework_logger.addHandler(stream_handler)
spotfm_logger.addHandler(stream_handler)

spot_client = os.environ.get('SPOT_CLIENT')
spot_secret = os.environ.get('SPOT_SECRET')
spot_access = os.environ.get('SPOT_ACCESS_TOKEN')
spot_refresh = os.environ.get('SPOT_REFRESH_TOKEN')
fmclient = os.environ.get('FM_CLIENT')
fmuser = os.environ.get('FM_USER')

if spot_access is None and spot_refresh is None:
    print('no spotify credentials')
    exit(0)

if fmclient is None:
    print('no last.fm credentials')
    exit(0)

spotnet = Spotnet(NetworkUser(client_id=spot_client,
                              client_secret=spot_secret,
                              access_token=spot_access,
                              refresh_token=spot_refresh)).refresh_access_token()

while len(fmuser) == 0:
    fmuser = input('last.fm username >> ')

fmnet = Fmnet(username=fmuser, api_key=fmclient)

top_artists = fmnet.top_artists(period=Fmnet.Range.OVERALL, limit=10)

artist_counts = dict()
for artist in top_artists:
    artist_counts[artist.name] = time(spotnet=spotnet, fmnet=fmnet, artist=artist.name, username=fmnet.username)

for name, count in artist_counts.items():
    print(name, f'{count}ms,', f'{count/1000}s,', seconds_to_time_str(milliseconds=count))
