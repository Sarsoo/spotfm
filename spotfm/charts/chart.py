from spotframework.net.network import Network as SpotNetwork
from spotframework.model.uri import Uri
from fmframework.net.network import Network as FmNetwork
import logging

logger = logging.getLogger(__name__)


def get_chart_of_spotify_tracks(spotnet: SpotNetwork,
                                fmnet: FmNetwork,
                                period: FmNetwork.Range,
                                limit: int,
                                username: str = None):
    logger.info(f'pulling {period.name} chart')

    chart = fmnet.get_top_tracks(period=period, username=username, limit=limit)

    spotify_chart = []
    for track in chart:
        spotify_search = spotnet.search(query_types=[Uri.ObjectType.track],
                                        track=track.name,
                                        artist=track.artist.name,
                                        response_limit=5).tracks
        if len(spotify_search) > 0:
            spotify_chart.append(spotify_search[0])
        else:
            logger.warning('no search tracks returned')

    return spotify_chart
