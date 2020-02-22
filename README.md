spotfm
=============

Utility functions sitting on top of [spotframework](https://github.com/Sarsoo/spotframework) and [fmframework](https://github.com/Sarsoo/pyspotframework).

## Track Chart Source

Spotframework playlist engine source pulling from track charts for a given standard Last.fm range.

## Counter

Interface class across Spotify and Last.fm to count scrobbles of Spotify objects (Tracks, Albums, Artists, Playlists).

#### Stats

Simple CMD interface to wrap around Counter including basic reading from file for frequently used.

## Chart

`get_chart_of_spotify_tracks()` function to return Last.fm track chart for given range as Spotify tracks. Used Spotify search API to retrieve Spotify tracks.