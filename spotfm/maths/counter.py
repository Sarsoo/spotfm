from spotframework.net.network import Network as SpotifyNetwork, SpotifyNetworkException
from spotframework.model.playlist import FullPlaylist
from spotframework.model.track import SimplifiedTrack
from spotframework.model.album import SimplifiedAlbum
from spotframework.model.artist import SimplifiedArtist
from spotframework.model.uri import Uri

from fmframework.net.network import Network as FMNetwork, LastFMNetworkException

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
        elif uri.object_type == Uri.ObjectType.track:
            return self.count_track(uri=uri)
        elif uri.object_type == Uri.ObjectType.album:
            return self.count_album(uri=uri)
        elif uri.object_type == Uri.ObjectType.artist:
            return self.count_artist(uri=uri)
        else:
            logger.error('cannot process uri')

    def count_playlist(self,
                       username: str = None,
                       uri: Uri = None,
                       playlist: FullPlaylist = None,
                       query_album=False,
                       query_artist=False) -> int:

        if uri is None and playlist is None:
            raise ValueError('no input playlist to count')

        if playlist is not None:
            if playlist.has_tracks() is False:
                try:
                    playlist.tracks = self.spotnet.playlist_tracks(uri=playlist.uri)
                except SpotifyNetworkException:
                    logger.exception(f'error occured during playlist track retrieval')
                    return 0

        if uri is not None:
            if uri.object_type != Uri.ObjectType.playlist:
                raise ValueError('uri not a playlist')
            try:
                playlist = self.spotnet.playlist(uri=uri, tracks=True)
            except SpotifyNetworkException:
                logger.exception(f'error occured during playlist retrieval')
                return 0

        scrobble_count = 0

        tracks = []
        for song in playlist.tracks:
            if song.track.uri not in [i.track.uri for i in tracks]:
                if query_album:
                    if song.track.album.uri not in [i.track.album.uri for i in tracks]:
                        tracks.append(song)
                elif query_artist:
                    if song.track.artists[0].uri not in [i.track.artists[0].uri for i in tracks]:
                        tracks.append(song)
                else:
                    tracks.append(song)

        for song in tracks:
            if query_album:
                scrobble_count += self.count_album(username=username, album=song.track.album)
            elif query_artist:
                scrobble_count += self.count_artist(username=username, artist=song.track.artists[0])
            else:
                scrobble_count += self.count_track(username=username, track=song.track)

        return scrobble_count

    def count_track(self, username: str = None, uri: Uri = None, track: SimplifiedTrack = None) -> int:

        if uri is None and track is None:
            raise ValueError('no track to count')

        if uri is not None:
            if uri.object_type != Uri.ObjectType.track:
                raise ValueError('uri not a track')
            try:
                track = self.spotnet.track(uri=uri)
            except SpotifyNetworkException:
                logger.exception(f'error occured during track retrieval')
                return 0

        try:
            fmtrack = self.fmnet.track(name=track.name,
                                       artist=track.artists[0].name,
                                       username=username or self.fmnet.username)
            if fmtrack is not None:
                return fmtrack.user_scrobbles
            else:
                logger.error(f'no track returned for {track}')
                return 0
        except LastFMNetworkException:
            logger.exception(f'error occured during track retrieval')
            return 0

    def count_album(self, username: str = None, uri: Uri = None, album: SimplifiedAlbum = None) -> int:

        if uri is None and album is None:
            raise ValueError('no album to count')

        if uri is not None:
            if uri.object_type != Uri.ObjectType.album:
                raise ValueError('uri not an album')
            try:
                album = self.spotnet.album(uri=uri)
            except SpotifyNetworkException:
                logger.exception(f'error occured during album retrieval')
                return 0

        try:
            fmalbum = self.fmnet.album(name=album.name,
                                       artist=album.artists[0].name,
                                       username=username or self.fmnet.username)
            if fmalbum is not None:
                return fmalbum.user_scrobbles
            else:
                logger.error(f'no track returned for {album}')
                return 0
        except LastFMNetworkException:
            logger.exception(f'error occured during album retrieval')
            return 0

    def count_artist(self, username: str = None, uri: Uri = None, artist: SimplifiedArtist = None) -> int:

        if uri is None and artist is None:
            raise ValueError('no artist to count')

        if uri is not None:
            if uri.object_type != Uri.ObjectType.artist:
                raise ValueError('uri not an artist')
            try:
                artist = self.spotnet.artist(uri=uri)
            except SpotifyNetworkException:
                logger.exception(f'error occured during artist retrieval')
                return 0

        try:
            fmartist = self.fmnet.artist(name=artist.name, username=username or self.fmnet.username)
            if fmartist is not None:
                return fmartist.user_scrobbles
            else:
                logger.error(f'no track returned for {artist}')
                return 0
        except LastFMNetworkException:
            logger.exception(f'error occured during artist retrieval')
            return 0
