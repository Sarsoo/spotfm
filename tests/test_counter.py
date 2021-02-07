import unittest
from unittest.mock import Mock, MagicMock, create_autospec, patch

from dataclasses import fields

from spotfm.maths.counter import Counter
from spotframework.model.uri import Uri
from spotframework.net.network import SpotifyNetworkException
from fmframework.net.network import LastFMNetworkException

class TestCounter(unittest.TestCase):

    ### ARTIST ###

    def test_artist_no_input(self):
        spotnet = Mock()
        fmnet = Mock()
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        with self.assertRaises(ValueError):
            counter.count_artist()

    def test_artist_with_artist_obj(self):
        spotnet = Mock()
        fmnet = Mock()
        
        return_mock = Mock()
        return_mock.user_scrobbles = 10
        fmnet.artist.return_value = return_mock
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        artist_mock = Mock()
        artist_mock.name = 'artist'

        answer = counter.count_artist(artist=artist_mock)

        fmnet.artist.assert_called_once()
        self.assertEqual(answer, 10)

    def test_artist_with_artist_obj_no_response(self):
        spotnet = Mock()
        fmnet = Mock()
        
        fmnet.artist.return_value = None
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        artist_mock = Mock()
        artist_mock.name = 'artist'

        answer = counter.count_artist(artist=artist_mock)

        fmnet.artist.assert_called_once()
        self.assertEqual(answer, 0)

    def test_artist_network_error(self):
        spotnet = Mock()
        fmnet = Mock()
        
        return_mock = Mock()
        return_mock.user_scrobbles = 10
        fmnet.artist.side_effect = LastFMNetworkException(500, 5)
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        artist_mock = Mock()
        artist_mock.name = 'artist'

        answer = counter.count_artist(artist=artist_mock)

        fmnet.artist.assert_called_once()
        self.assertEqual(answer, 0)

    def test_artist_with_uri(self):
        spotnet = Mock()
        fmnet = Mock()
        
        return_mock = Mock()
        return_mock.user_scrobbles = 10
        fmnet.artist.return_value = return_mock

        spot_return_mock = Mock()
        spot_return_mock.name = 'artist'
        spotnet.artist.return_value = spot_return_mock
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        uri_mock = Mock()
        uri_mock.object_type = Uri.ObjectType.artist

        answer = counter.count_artist(uri=uri_mock)

        fmnet.artist.assert_called_once()
        self.assertEqual(answer, 10)

    def test_artist_with_uri_wrong_type(self):
        spotnet = Mock()
        fmnet = Mock()
        
        return_mock = Mock()
        return_mock.user_scrobbles = 10
        fmnet.artist.return_value = return_mock

        spot_return_mock = Mock()
        spot_return_mock.name = 'artist'
        spotnet.artist.return_value = spot_return_mock
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        uri_mock = Mock()
        uri_mock.object_type = Uri.ObjectType.track

        with self.assertRaises(ValueError):
            answer = counter.count_artist(uri=uri_mock)

            fmnet.artist.assert_called_once()
            self.assertEqual(answer, 10)

    def test_artist_with_uri_network_error(self):
        spotnet = Mock()
        fmnet = Mock()
        
        return_mock = Mock()
        return_mock.user_scrobbles = 10
        fmnet.artist.return_value = return_mock

        spot_return_mock = Mock()
        spot_return_mock.name = 'artist'
        spotnet.artist.return_value = spot_return_mock
        spotnet.artist.side_effect = SpotifyNetworkException(500)
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        uri_mock = Mock()
        uri_mock.object_type = Uri.ObjectType.artist

        answer = counter.count_artist(uri=uri_mock)

        spotnet.artist.assert_called_once()
        fmnet.artist.assert_not_called()
        self.assertEqual(answer, 0)

    ### ALBUM ###

    def test_album_no_input(self):
        spotnet = Mock()
        fmnet = Mock()
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        with self.assertRaises(ValueError):
            counter.count_album()

    def test_album_with_artist_obj(self):
        spotnet = Mock()
        fmnet = Mock()
        
        return_mock = Mock()
        return_mock.user_scrobbles = 10
        fmnet.album.return_value = return_mock
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        album_mock = Mock()
        album_mock.name = 'album'
        album_mock.artists = [Mock()]

        answer = counter.count_album(album=album_mock)

        fmnet.album.assert_called_once()
        self.assertEqual(answer, 10)

    def test_album_with_album_obj_no_response(self):
        spotnet = Mock()
        fmnet = Mock()
        
        fmnet.album.return_value = None
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        album_mock = Mock()
        album_mock.name = 'album'
        album_mock.artists = [Mock()]

        answer = counter.count_album(album=album_mock)

        fmnet.album.assert_called_once()
        self.assertEqual(answer, 0)

    def test_album_network_error(self):
        spotnet = Mock()
        fmnet = Mock()
        
        return_mock = Mock()
        return_mock.user_scrobbles = 10
        fmnet.album.side_effect = LastFMNetworkException(500, 5)
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        album_mock = Mock()
        album_mock.name = 'album'
        album_mock.artists = [Mock()]

        answer = counter.count_album(album=album_mock)

        fmnet.album.assert_called_once()
        self.assertEqual(answer, 0)

    def test_album_with_uri(self):
        spotnet = Mock()
        fmnet = Mock()
        
        return_mock = Mock()
        return_mock.user_scrobbles = 10
        fmnet.album.return_value = return_mock

        spot_return_mock = Mock()
        spot_return_mock.name = 'album'
        spot_return_mock.artists = [Mock()]
        spotnet.album.return_value = spot_return_mock
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        uri_mock = Mock()
        uri_mock.object_type = Uri.ObjectType.album

        answer = counter.count_album(uri=uri_mock)

        fmnet.album.assert_called_once()
        self.assertEqual(answer, 10)

    def test_album_with_uri_wrong_type(self):
        spotnet = Mock()
        fmnet = Mock()
        
        return_mock = Mock()
        return_mock.user_scrobbles = 10
        fmnet.album.return_value = return_mock

        spot_return_mock = Mock()
        spot_return_mock.name = 'album'
        spotnet.album.return_value = spot_return_mock
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        uri_mock = Mock()
        uri_mock.object_type = Uri.ObjectType.track

        with self.assertRaises(ValueError):
            answer = counter.count_album(uri=uri_mock)

            fmnet.album.assert_called_once()
            self.assertEqual(answer, 10)

    def test_album_with_uri_network_error(self):
        spotnet = Mock()
        fmnet = Mock()
        
        return_mock = Mock()
        return_mock.user_scrobbles = 10
        fmnet.album.return_value = return_mock

        spot_return_mock = Mock()
        spot_return_mock.name = 'album'
        spotnet.album.return_value = spot_return_mock
        spotnet.album.side_effect = SpotifyNetworkException(500)
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        uri_mock = Mock()
        uri_mock.object_type = Uri.ObjectType.album

        answer = counter.count_album(uri=uri_mock)

        spotnet.album.assert_called_once()
        fmnet.album.assert_not_called()
        self.assertEqual(answer, 0)

    ### TRACK ###

    def test_track_no_input(self):
        spotnet = Mock()
        fmnet = Mock()
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        with self.assertRaises(ValueError):
            counter.count_track()

    def test_track_with_artist_obj(self):
        spotnet = Mock()
        fmnet = Mock()
        
        return_mock = Mock()
        return_mock.user_scrobbles = 10
        fmnet.track.return_value = return_mock
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        track_mock = Mock()
        track_mock.name = 'track'
        track_mock.artists = [Mock()]

        answer = counter.count_track(track=track_mock)

        fmnet.track.assert_called_once()
        self.assertEqual(answer, 10)

    def test_track_with_album_obj_no_response(self):
        spotnet = Mock()
        fmnet = Mock()
        
        fmnet.track.return_value = None
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        track_mock = Mock()
        track_mock.name = 'track'
        track_mock.artists = [Mock()]

        answer = counter.count_track(track=track_mock)

        fmnet.track.assert_called_once()
        self.assertEqual(answer, 0)

    def test_track_network_error(self):
        spotnet = Mock()
        fmnet = Mock()
        
        return_mock = Mock()
        return_mock.user_scrobbles = 10
        fmnet.track.side_effect = LastFMNetworkException(500, 5)
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        track_mock = Mock()
        track_mock.name = 'track'
        track_mock.artists = [Mock()]

        answer = counter.count_track(track=track_mock)

        fmnet.track.assert_called_once()
        self.assertEqual(answer, 0)

    def test_track_with_uri(self):
        spotnet = Mock()
        fmnet = Mock()
        
        return_mock = Mock()
        return_mock.user_scrobbles = 10
        fmnet.track.return_value = return_mock

        spot_return_mock = Mock()
        spot_return_mock.name = 'track'
        spot_return_mock.artists = [Mock()]
        spotnet.track.return_value = spot_return_mock
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        uri_mock = Mock()
        uri_mock.object_type = Uri.ObjectType.track

        answer = counter.count_track(uri=uri_mock)

        fmnet.track.assert_called_once()
        self.assertEqual(answer, 10)

    def test_track_with_uri_wrong_type(self):
        spotnet = Mock()
        fmnet = Mock()
        
        return_mock = Mock()
        return_mock.user_scrobbles = 10
        fmnet.track.return_value = return_mock

        spot_return_mock = Mock()
        spot_return_mock.name = 'track'
        spotnet.track.return_value = spot_return_mock
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        uri_mock = Mock()
        uri_mock.object_type = Uri.ObjectType.album

        with self.assertRaises(ValueError):
            answer = counter.count_track(uri=uri_mock)

            fmnet.track.assert_called_once()
            self.assertEqual(answer, 10)

    def test_track_with_uri_network_error(self):
        spotnet = Mock()
        fmnet = Mock()
        
        return_mock = Mock()
        return_mock.user_scrobbles = 10
        fmnet.track.return_value = return_mock

        spot_return_mock = Mock()
        spot_return_mock.name = 'track'
        spotnet.track.return_value = spot_return_mock
        spotnet.track.side_effect = SpotifyNetworkException(500)
        
        counter = Counter(spotnet=spotnet, fmnet=fmnet)

        uri_mock = Mock()
        uri_mock.object_type = Uri.ObjectType.track

        answer = counter.count_track(uri=uri_mock)

        spotnet.track.assert_called_once()
        fmnet.track.assert_not_called()
        self.assertEqual(answer, 0)

    #TODO: count_playlist method
    #TODO: count method

if __name__ == '__main__':
    unittest.main()