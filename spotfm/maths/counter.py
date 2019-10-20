from spotframework.net.network import Network as SpotifyNetwork
from spotframework.model.playlist import SpotifyPlaylist
from spotframework.model.track import SpotifyTrack
from spotframework.model.album import SpotifyAlbum
from spotframework.model.artist import SpotifyArtist
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
                       playlist: SpotifyPlaylist = None,
                       query_album=False,
                       query_artist=False) -> int:

        if uri is None and playlist is None:
            raise ValueError('no input playlist to count')

        if playlist is not None:
            if playlist.has_tracks() is False:
                playlist.tracks = self.spotnet.get_playlist_tracks(uri=playlist.uri)

        if uri is not None:
            if uri.object_type != Uri.ObjectType.playlist:
                raise ValueError('uri not a playlist')
            playlist = self.spotnet.get_playlist(uri=uri)

        scrobble_count = 0

        tracks = []
        for song in playlist.tracks:
            if isinstance(song, SpotifyTrack):
                if song.uri not in [i.uri for i in tracks]:
                    if query_album:
                        if song.album.uri not in [i.album.uri for i in tracks]:
                            tracks.append(song)
                    elif query_artist:
                        if song.artists[0].uri not in [song.artists[0].uri for i in tracks]:
                            tracks.append(song)
                    else:
                        tracks.append(song)

        for song in tracks:
            if query_album:
                scrobble_count += self.count_album(username=username, album=song.album)
            elif query_artist:
                scrobble_count += self.count_artist(username=username, artist=song.artists[0])
            else:
                scrobble_count += self.count_track(username=username, track=song)

        return scrobble_count

    def count_track(self, username: str = None, uri: Uri = None, track: SpotifyTrack = None) -> int:

        if uri is None and track is None:
            raise ValueError('no track to count')

        if uri is not None:
            if uri.object_type != Uri.ObjectType.track:
                raise ValueError('uri not a track')
            track = self.spotnet.get_track(uri=uri)

        if username is not None:
            fmtrack = self.fmnet.get_track(name=track.name, artist=track.artists[0].name, username=username)
        else:
            fmtrack = self.fmnet.get_track(name=track.name, artist=track.artists[0].name, username=self.fmnet.username)

        if fmtrack is not None:
            return fmtrack.user_scrobbles
        else:
            logger.error(f'no album returned for {track}')
            return 0

    def count_album(self, username: str = None, uri: Uri = None, album: SpotifyAlbum = None) -> int:

        if uri is None and album is None:
            raise ValueError('no album to count')

        if uri is not None:
            if uri.object_type != Uri.ObjectType.album:
                raise ValueError('uri not an album')
            album = self.spotnet.get_album(uri=uri)

        if username is not None:
            fmalbum = self.fmnet.get_album(name=album.name, artist=album.artists[0].name, username=username)
        else:
            fmalbum = self.fmnet.get_album(name=album.name, artist=album.artists[0].name, username=self.fmnet.username)

        if fmalbum is not None:
            return fmalbum.user_scrobbles
        else:
            logger.error(f'no album returned for {album}')
            return 0

    def count_artist(self, username: str = None, uri: Uri = None, artist: SpotifyArtist = None) -> int:

        if uri is None and artist is None:
            raise ValueError('no artist to count')

        if uri is not None:
            if uri.object_type != Uri.ObjectType.artist:
                raise ValueError('uri not an artist')
            artist = self.spotnet.get_artist(uri=uri)

        if username is not None:
            fmartist = self.fmnet.get_artist(name=artist.name, username=username)
        else:
            fmartist = self.fmnet.get_artist(name=artist.name, username=self.fmnet.username)

        if fmartist is not None:
            return fmartist.user_scrobbles
        else:
            logger.error(f'no artist returned for {artist}')
            return 0
