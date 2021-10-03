"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
from .helper import Helper
import random
import re

class VideoPlayer:
    """A class used to represent a Video Player.
    
    Attributes:
        _video_library (VideoLibrary): Stores the video library
        current (Video): Stores the current video playing
        pause(Boolean): Stores whether the video is paused or not
        playlists(dict): Stores all the playlists created playlist_name.lower():Playlist()
    """

    def __init__(self):
        self._video_library = VideoLibrary()
        self.current = None 
        self.pause = False 
        self.playlists = dict()

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """
            List all available videos in the format "title(video_id)[tags]" 
            all in lexicographical order by title
        """
        videoDict = dict() #Used to fetch video object video.title:videoObject
        videos = [] #Array to sort video.titles

        #Populates dictonary and array
        for video in self._video_library.get_all_videos(): 
            videoDict[video.title] = video
            videos.append(video.title)

        sortedArray = Helper.merge_sort(videos)
        print("Here's a list of all available videos:")
        for video in sortedArray:
            print(" ",videoDict.get(video))

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        #Fetches video to play
        video = self._video_library.get_video(video_id)
        #Checks if video exist and nothing is playing
        if video != None and self.current == None and video.flag == None:
            print("Playing video: {}".format(video.title))
            self.current = video
            self.pause = False
        #Checks if video exist and if something is playing stop current and play new video
        elif video != None and self.current != None:
            print("Stopping video: {}\nPlaying video: {}".format(self.current.title,video.title))
            self.current = video
            self.pause = False
        #Video exists but is flagged
        elif video != None and video.flag != None:
            print("Cannot play video: Video is currently flagged (reason: {})".format(video.flag))
        #Video does not exist 
        else:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""

        if self.current != None:
            print("Stopping video: {}".format(self.current.title))
            self.current = None
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""

        videos = self._video_library.get_all_videos()
        videoClean = Helper.videoClean(videos)
        
        if len(videoClean) == 0:
            print("No videos available")
        else:
            videoIndex = random.randint(0,len(videoClean)-1)
            self.play_video(video[videoIndex].video_id)

    def pause_video(self):
        """Pauses the current video."""

        #Checks if no video is currently playing if not error cant pause video
        if self.current == None:
            print("Cannot pause video: No video is currently playing")
        #If video is currently playing and paused print already paused
        elif self.pause == True and self.current != None:
            print("Video already paused: {}".format(self.current.title))
        #Pausing video assuming video is playing and pause is false
        else:
            print("Pausing video: {}".format(self.current.title))
            self.pause = True


    def continue_video(self):
        """Resumes playing the current video."""

        #Checks if video is playing if not error message that no video is playing
        if self.current == None:
            print("Cannot continue video: No video is currently playing")
        #Checks if video is playing and video is not paused error message that we can't continue 
        elif self.current!=None and self.pause==False:
            print("Cannot continue video: Video is not paused")
        #Continue pause video
        else:
            print("Continuing video: {}".format(self.current.title))
            self.pause = False
        

    def show_playing(self):
        """Displays video currently playing."""

        #Video if no vide is playing
        if self.current == None:
            print("No video is currently playing")
        #If a video is playing and is paused 
        elif self.pause == True and self.current!=None:
            print("Currently playing:",self.current,"- PAUSED")
        #If a video is just playing
        else:
            print("Currently playing:",self.current)


    def fetch_playlist(self,playlist_name):
        """Fetch playlist object
        
            Args:
                playlist_name(string): Playlist name

            Returns:
                Playlist(Playlist): The playlist object
        """
        return self.playlists.get(playlist_name.lower())

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        #Checks if the playlist name is in the right format
        if len(re.findall("\d",playlist_name)) > 0:
            print("Playlist name should not contain numbers")

        #Checks if the playlist does not exist
        playlist = self.fetch_playlist(playlist_name)
        if playlist == None:
            self.playlists[playlist_name.lower()] = Playlist(playlist_name)
            print("Successfully created new playlist: {}".format(self.fetch_playlist(playlist_name).name))
        #If the playlist exists don't create
        else:
            print("Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        video = self._video_library.get_video(video_id)
        playlist = self.fetch_playlist(playlist_name)

        #If the video does not exist show error
        if playlist == None:
            print("Cannot add video to {}: Playlist does not exist".format(playlist_name))
        #If the playlist does not exist show error
        elif video == None:
            print("Cannot add video to {}: Video does not exist".format(playlist_name))
        #If video exist in playlist show error
        elif playlist.get_video(video_id) != None:
            print("Cannot add video to {}: Video already added".format(playlist_name))
        #Flagged
        elif video.flag != None:
            print("Cannot add video to {}: Video is currently flagged (reason: {})".format(playlist_name,video.flag))
        #Add video to playlist
        else:
            playlist.add_video(video_id,video)
            print("Added video to {}: {}".format(playlist_name,video.title))

    def show_all_playlists(self):
        """Display all playlists."""
        if len(self.playlists) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            playlist = [x for x in self.playlists.keys()]
            playlistOrder = Helper.merge_sort(playlist)
            for x in playlistOrder:
                print(" ",self.playlists[x].name)
            

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.fetch_playlist(playlist_name)
        if playlist == None:
            print("Cannot show playlist {}: Playlist does not exist".format(playlist_name))
            return

        print("Showing playlist: {}".format(playlist_name))
        videos = playlist.get_all_videos#Stores the video_id
        if len(videos) == 0:
            print(" No videos here yet")
        else:
            for video in videos:
                print(" ",self._video_library.get_video(video))

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        video = self._video_library.get_video(video_id)
        playlist = self.fetch_playlist(playlist_name)

        #Check if playlist exist if not show error message
        if playlist == None:
            print("Cannot remove video from {}: Playlist does not exist".format(playlist_name))
        #Check if the video exists if not show error message
        elif video == None:
            print("Cannot remove video from {}: Video does not exist".format(playlist_name))
        #If video is not in playlist show error message
        elif playlist.get_video(video_id) == None:
            print("Cannot remove video from {}: Video is not in playlist".format(playlist_name))
        #Remove the video
        else:
            del playlist._videos[video_id]
            print("Removed video from {}: {}".format(playlist_name,video.title))

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.fetch_playlist(playlist_name)
        #playlist doesnt exist show error
        if playlist == None:
            print("Cannot clear playlist {}: Playlist does not exist".format(playlist_name))
        #clear playlist 
        else:
            playlist._videos = dict()
            print("Successfully removed all videos from {}".format(playlist_name))

        

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.fetch_playlist(playlist_name)
        if playlist == None:
            print("Cannot delete playlist {}: Playlist does not exist".format(playlist_name))
        else:
            del self.playlists[playlist.name.lower()]
            print("Deleted playlist: {}".format(playlist_name))

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """

        videos = self._video_library.get_all_videos()
        #Linear search for videos
        foundVideo = []
        for video in videos:
            if search_term.lower() in video.title.lower() and video.flag == None:
                foundVideo.append(video)

        #Final Output
        index = Helper.searchOutput(foundVideo,search_term)
        if Helper.indexValidaton(index,foundVideo):
            self.play_video(foundVideo[int(index)-1].video_id)

    
    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        #When no hashtag is found assume it can't be found
        if video_tag[0] != "#":
            print("No search results for {}".format(video_tag))
            return
        
        videos = self._video_library.get_all_videos()
        #Linear search for videos
        foundVideo = []
        for video in videos:
            if video_tag.lower() in " ".join(video.tags).lower() and video.flag == None:
                foundVideo.append(video)

        #Final Output
        index = Helper.searchOutput(foundVideo,video_tag)
        if Helper.indexValidaton(index,foundVideo):
            self.play_video(foundVideo[int(index)-1].video_id)

    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)

        if video == None:
            print("Cannot flag video: Video does not exist")
        elif video.flag == None and self.current != None:
            if video == self.current:
                print("Stopping video: {}".format(self.current))
                self.current = None
            print("Successfully flagged video: {} (reason: {})".format(video.title,flag_reason))
            video.set_flag(flag_reason)
        elif video.flag == None:
            video.set_flag(flag_reason)
            print("Successfully flagged video: {} (reason: {})".format(video.title,flag_reason))
        elif video.flag != None:
            print("Cannot flag video: Video is already flagged")
        
    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot remove flag from video: Video does not exist")
        elif video.flag == None:
            print("Cannot remove flag from video: Video is not flagged")
        elif video.flag != None:
            print("Successfully removed flag from video: {}".format(video.title))
            video.remove_flag()
        

