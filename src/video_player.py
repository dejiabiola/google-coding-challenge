"""A video player class."""
import operator
import random
from .video_library import VideoLibrary
from .video_playlist import Playlist

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playlist = Playlist()
        self.playing = []

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        videos = self._video_library.get_all_videos()
        print("Here's a list of all available videos:")
        videos.sort(key=operator.attrgetter('title'))
        for v in videos:
            if v.flagged == False:
                print(f"{self.format_video(v)}")
            else:
                print(f"{self.format_video(v)} - FLAGGED (reason: {v.flagged_reason})")


    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot play video: Video does not exist")
        elif video.flagged == True:
            print(f"Cannot play video: Video is currently flagged (reason: {video.flagged_reason})") 
            return
        elif video != None and len(self.playing) > 0:
            print(f"Stopping video: {self.playing[0]['title']}")
            self.playing.pop()
            print(f"Playing video: {video.title}")
            self.playing.append({'title': video.title, 'is_playing': True, 'id': video_id})
        else:
            self.playing.append({'title': video.title, 'is_playing': True, 'id': video_id})
            print(f"Playing video: {video.title}")

    def stop_video(self):
        """Stops the current video."""
        if (len(self.playing) > 0):
            print(f"Stopping video: {self.playing[0]['title']}")
            self.playing.pop()
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        videos = self._video_library.get_all_videos()
        
        unflagged_videos = []
        for v in videos:
            if v.flagged != True:
                unflagged_videos.append(v) 

        if len(unflagged_videos) < 1:
            print("No videos available")
            return
       
        random_int = random.randint(0, len(unflagged_videos) - 1)
        video = unflagged_videos[random_int]
        
        if (len(self.playing) > 0):
            print(f"Stopping video: {self.playing[0]['title']}")
            self.playing.pop()
            print(f"Playing video: {video.title}")
            self.playing.append({'title': video.title, 'is_playing': True, 'id': video.video_id})
        else:
            print(f"Playing video: {video.title}")
            self.playing.append({'title': video.title, 'is_playing': True, 'id': video.video_id})

        

    def pause_video(self):
        """Pauses the current video."""
        if (len(self.playing) > 0):
            if self.playing[0]['is_playing'] == True:
              print(f"Pausing video: {self.playing[0]['title']}")
              self.playing[0]['is_playing'] = False
            else:
              print(f"Video already paused: {self.playing[0]['title']}")
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""
        if (len(self.playing) > 0):
            if self.playing[0]['is_playing'] == False:
              print(f"Continuing video: {self.playing[0]['title']}")
              self.playing[0]['is_playing'] = True
            else:
              print(f"Cannot continue video: Video is not paused")
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        if (len(self.playing) > 0):
            video = self._video_library.get_video(self.playing[0]['id'])
            tags = ''
            for t in video.tags:
              if len(tags) < 1:
                tags += t
              else:
                tags += f" {t}"
            string = f"Currently playing: {video.title} ({video.video_id}) [{tags}]"
            if self.playing[0]['is_playing'] == True:
              print(string)
            else:
              print(f"{string} - PAUSED")
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        all_playlists = self._playlist.get_all_playlists()
        if self._playlist.check_playlist_exists(playlist_name) != False:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            all_playlists[playlist_name] = []
            print(f"Successfully created new playlist: {playlist_name}")


    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        video = self._video_library.get_video(video_id)
        all_playlists = self._playlist.get_all_playlists()
        playlist = self._playlist.check_playlist_exists(playlist_name)

        if video != None and video.flagged == True:
            print(f"Cannot add video to my_playlist: Video is currently flagged (reason: {video.flagged_reason})") 
            return
        if playlist != False and video != None:
            if video_id in all_playlists[playlist]:
                print(f"Cannot add video to {playlist_name}: Video already added")
            else:
                all_playlists[playlist].append(video_id)
                print(f"Added video to {playlist_name}: Amazing Cats")
        elif video == None and playlist != False:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
        elif playlist == False:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
        


    def show_all_playlists(self):
        """Display all playlists."""

        all_playlists = self._playlist.get_all_playlists()
        if len(all_playlists) < 1:
            print("No playlists exist yet")
        else:
          print("Showing all playlists:")
          for p in sorted(all_playlists.keys()):
            print(p)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        all_playlists = self._playlist.get_all_playlists()
        playlist = self._playlist.check_playlist_exists(playlist_name)

        if playlist == False:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
        else:
            print(f"Showing playlist: {playlist_name}")
            playlist_data = all_playlists[playlist]
            if (len(playlist_data) < 1):
                print("No videos here yet")
            else:
                for video_id in playlist_data:
                    video = self._video_library.get_video(video_id)
                    if video != None:
                        result = self.format_video(video)
                        if video.flagged == False:    
                            print(result)
                        else:
                          print(f"{result} - FLAGGED (reason: dont_like_cats)")
                
    def format_video(self, video):
        tags = ''
        for t in video.tags:
            if len(tags) < 1:
                tags += t
            else:
                tags += f" {t}"
        return f"{video.title} ({video.video_id}) [{tags}]" 


    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        all_playlists = self._playlist.get_all_playlists()
        playlist = self._playlist.check_playlist_exists(playlist_name)

        if playlist == False:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            return
        video = self._video_library.get_video(video_id)
        if video == None:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
            return
        if playlist != False and video != None:
            playlist_data = all_playlists[playlist]
            if video_id not in playlist_data:
                print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            else:
                playlist_data.remove(video_id)
                print(f"Removed video from {playlist_name}: {video.title}")
        
        

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        all_playlists = self._playlist.get_all_playlists()
        playlist = self._playlist.check_playlist_exists(playlist_name)

        if playlist == False:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            all_playlists[playlist] = []
            print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        all_playlists = self._playlist.get_all_playlists()
        playlist = self._playlist.check_playlist_exists(playlist_name)

        if playlist == False:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:
            all_playlists.pop(playlist)
            print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = self._video_library.get_all_videos()

        result = []
        for video in videos:
            if video.flagged != True:
                if search_term.lower() in video.title.lower():
                    result.append(video) 
        if len(result) < 1:
            print(f"No search results for {search_term}")
        else:
            print(f"Here are the results for {search_term}:")
            result.sort(key=operator.attrgetter('title'))
            for index, video in enumerate(result):
                print(f"{index + 1}) {self.format_video(video)}")
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            try:
              userInput = int(input())
              if userInput >= 1 and userInput <= len(result):
                  user_selection = result[userInput - 1]
                  self.play_video(user_selection.video_id)
            except:
              pass



    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        if video_tag.startswith("#") == False:
            print(f"No search results for {video_tag}")
            return

        videos = self._video_library.get_all_videos()
        result = []
        unflagged_videos = []
        for v in videos:
            if v.flagged != True:
                unflagged_videos.append(v)

        for video in unflagged_videos:
            for tag in video.tags:
                if video_tag.lower() == tag.lower():
                    result.append(video) 
        if len(result) < 1:
            print(f"No search results for {video_tag}")
        else:
            print(f"Here are the results for {video_tag}:")
            result.sort(key=operator.attrgetter('title'))
            for index, video in enumerate(result):
                print(f"{index + 1}) {self.format_video(video)}")
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            try:
              userInput = int(input())
              if userInput >= 1 and userInput <= len(result):
                  user_selection = result[userInput - 1]
                  self.play_video(user_selection.video_id)
            except:
              pass

    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print(f"Cannot flag video: Video does not exist")
            return
        if video.flagged == True:
            print(f"Cannot flag video: Video is already flagged")
        else:
            if len(self.playing) > 0 and self.playing[0]['id'] == video_id:
                self.stop_video()
            video.flagged = True
            video.flagged_reason = flag_reason
            print(f"Successfully flagged video: {video.title} (reason: {flag_reason})")
            
    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print(f"Cannot remove flag from video: Video does not exist")
            return
        if video.flagged != True:
            print(f"Cannot remove flag from video: Video is not flagged")
        else:
            video.flagged = False
            video.flagged_reason = None
            print(f"Successfully removed flag from video: {video.title}")


