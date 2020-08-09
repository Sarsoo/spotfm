import logging
from datetime import datetime

from spotframework.net.network import Network as SpotNet
from spotframework.model.uri import Uri
from spotframework.model.track import TrackFull
from fmframework.net.network import Network as FmNet
from fmframework.model import Track
from fmframework.net.scrape import LibraryScraper

logger = logging.getLogger(__name__)

def time_artist(spotnet: SpotNet, artist: str, username: str, fmnet: FmNet = None,
                from_date: datetime = None, to_date: datetime = None, date_preset: str = None) -> int:
    logger.info(f'timing {artist} for {username}')

    fmtracks = LibraryScraper.get_scrobbled_tracks(username=username, artist=artist, whole_track=False,
                                                   from_date=from_date, to_date=to_date, date_preset=date_preset)

    return time_track_collection(tracks=fmtracks, spotnet=spotnet, username=username, fmnet=fmnet)

def time_album(spotnet: SpotNet, artist: str, album: str, username: str, fmnet: FmNet = None,
               from_date: datetime = None, to_date: datetime = None, date_preset: str = None) -> int:
    logger.info(f'timing {album} / {artist} for {username}')

    fmtracks = LibraryScraper.get_albums_tracks(username=username, artist=artist, album=album, whole_track=False,
                                                from_date=from_date, to_date=to_date, date_preset=date_preset)

    return time_track_collection(tracks=fmtracks, spotnet=spotnet, username=username, fmnet=fmnet)

def time_track(spotnet: SpotNet, artist: str, track: str, username: str, fmnet: FmNet = None,
               from_date: datetime = None, to_date: datetime = None, date_preset: str = None) -> int:
    logger.info(f'timing {track} / {artist} for {username}')

    fmtracks = LibraryScraper.get_track_scrobbles(username=username, artist=artist, track=track, whole_track=False,
                                                  from_date=from_date, to_date=to_date, date_preset=date_preset)

    return time_track_collection(tracks=fmtracks, spotnet=spotnet, username=username, fmnet=fmnet)

def time_track_collection(tracks, spotnet: SpotNet, username: str, fmnet:FmNet = None):
    track_pairs = []
    if tracks is not None:
        for track in tracks:
            spottrack = spotnet.search(query_types=[Uri.ObjectType.track],
                                       track=track.name,
                                       artist=track.artist.name,
                                       response_limit=1).tracks

            if len(spottrack) == 1:
                track_pairs.append((track, spottrack[0]))
            else:
                if fmnet is not None:
                    logger.error(f'no track returned for search {track.name} / {track.artist.name} / {username}'
                                 f', pulling last.fm track')

                    fmtrack = fmnet.get_track(name=track.name, artist=track.artist.name, username=username)

                    if fmtrack is not None and fmtrack.duration is not None and fmtrack.duration > 0:
                        track_pairs.append((track, fmtrack))
                    else:
                        logger.error(f'no duration found on last.fm for {track.name} / {track.artist.name} / {username}')
                else:
                    logger.error(f'no track returned for search {track.name} / {track.artist.name} / {username}'
                                 f', no fmnet to use as fallback')

        total_ms = 0

        for track_pair in track_pairs:
            if isinstance(track_pair[1], TrackFull):
                duration = track_pair[1].duration_ms
            elif isinstance(track_pair[1], Track):
                duration = track_pair[1].duration
            else:
                logger.critical(f'invalid track type found {type(track_pair[1])}')
                duration = 0

            total_ms += duration * track_pair[0].user_scrobbles

        return total_ms
