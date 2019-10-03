from spotframework.net.network import Network as SpotifyNetwork
from spotframework.model.playlist import SpotifyPlaylist
from spotframework.model.track import SpotifyTrack
from spotframework.model.uri import Uri

from fmframework.net.network import Network as FMNetwork

import logging

logger = logging.getLogger(__name__)


class Counter:
    def __init__(self,
                 spotnet: SpotifyNetwork,
                 fmnet: FMNetwork):
        self.spotnet = spotnet
        self.fmnet = fmnet

    def count(self, uri: Uri):
        if uri.object_type == Uri.ObjectType.playlist:
            return self.count_playlist(uri=uri)
        else:
            logger.error('cannot process uri')

    def count_playlist(self, username: str = None, uri: Uri = None, playlist: SpotifyPlaylist = None):

        if uri is None and playlist is None:
            raise ValueError('no input playlist to count')

        if playlist is not None:
            if playlist.has_tracks() is False:
                playlist.tracks = self.spotnet.get_playlist_tracks(uri=playlist.uri)

        if uri is not None:
            playlist = self.spotnet.get_playlist(uri=uri)

        scrobble_count = 0

        tracks = []
        for song in playlist.tracks:
            if isinstance(song, SpotifyTrack):
                if song.uri not in [i.uri for i in tracks]:
                    tracks.append(song)

        for song in tracks:
            if username is not None:
                fm_track = self.fmnet.get_track(name=song.name,
                                                artist=song.artists[0].name,
                                                username=username)
            else:
                fm_track = self.fmnet.get_track(name=song.name,
                                                artist=song.artists[0].name,
                                                username=self.fmnet.username)

            if fm_track:
                scrobble_count += fm_track.user_scrobbles
            else:
                logger.error(f'no last.fm track returned for {song}')

        return scrobble_count
