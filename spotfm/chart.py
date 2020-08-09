from spotframework.net.network import Network as SpotNetwork, SpotifyNetworkException
from spotframework.model.uri import Uri
from fmframework.net.network import Network as FmNetwork, LastFMNetworkException
import logging

logger = logging.getLogger(__name__)


def get_chart_of_spotify_tracks(spotnet: SpotNetwork,
                                fmnet: FmNetwork,
                                period: FmNetwork.Range,
                                limit: int,
                                username: str = None):
    logger.info(f'pulling {period.name} chart')

    try:
        chart = fmnet.get_top_tracks(period=period, username=username, limit=limit)

        spotify_chart = []
        for track in chart:
            try:
                spotify_search = spotnet.search(query_types=[Uri.ObjectType.track],
                                                track=track.name,
                                                artist=track.artist.name,
                                                response_limit=5).tracks
                if len(spotify_search) > 0:
                    spotify_chart.append(spotify_search[0])
                else:
                    logger.debug('no search tracks returned')
            except SpotifyNetworkException:
                logger.exception(f'error during search function')

        return spotify_chart
    except LastFMNetworkException:
        logger.exception(f'error during chart retrieval function')
        return []
