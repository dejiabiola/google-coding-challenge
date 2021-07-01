"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self):
        self._all_playlist = {}

    def get_all_playlists(self):
        """Returns all the users playlists"""
        return self._all_playlist

    def check_playlist_exists(self, playlist):
        """Returns the element if element is in playlist otherwise returns false"""
        for element in self._all_playlist.keys():
            if playlist.lower() == element.lower():
                return element
        return False