"""A video player class."""

from math import trunc
from src.video_playlist import Playlist
from .video_library import VideoLibrary
from random import randint
import re
from random import shuffle

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playlist = []
        self._current = None
        self._pause = False

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        
        videos = [[video.title,video.video_id," ".join(video.tags),video.flagReason,video.flagged] for video in self._video_library.get_all_videos()]

        #Insertion Sort on video
        for i in range(1,len(videos)):
            key = videos[i]
            j = i - 1
            while j >= 0 and videos[j] > key:
                videos[j+1] = videos[j]
                j-=1
            videos[j+1] = key

        print("Here's a list of all available videos:")
        for video in videos:
            if video[4] == True:
                print("  {title} ({ID}) [{tags}] - FLAGGED (reason: {flagReason})".format(title= video[0], ID=video[1], tags=video[2],flagReason = video[3]))
            else:
                print("  {title} ({ID}) [{tags}]".format(title= video[0], ID=video[1], tags=video[2]))

    def play_video(self, video_id):
        """
        Args:
            video_id: The video_id to be played.
        """
        
        video = self._video_library.get_video(video_id)
        if self._current != None and video != None:
            print("Stopping video: {}".format(self._current.title))
            print("Playing video: {}".format(video.title))
            self._current = video
            self._pause = False
        elif video != None and video.flagged == False:
            print("Playing video: {}".format(video.title))
            self._current = video
            self._pause = False
        elif video.flagged == True:
            print("Cannot play video: Video is currently flagged (reason: {})".format(video.flagReason))
        else:
            print("Cannot play video: Video does not exist")
        

    def stop_video(self):
        """Stops the current video."""
        if self._current != None:
            print("Stopping video: {video}".format(video = self._current.title))
            self._current = None
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""

        #Creates an array of Int num up to the length of array and shuffles the number
        randInt = [x for x in range(len(self._video_library.get_all_videos())-1)]
        shuffle(randInt)
        songNum = randInt.pop()
        randVid = self._video_library.get_all_videos()[songNum]
        while randVid.flagged == True and len(randInt) > 0:
            randVid = self._video_library.get_all_videos()[songNum]
            songNum = randInt.pop()
        
        if len(randInt) == 0:
            print("No videos available")
        else:
            if self._current == None:
                print("Playing video: {}".format(randVid.title))
                self._current = randVid
                self._pause = False
            else:
                print("Stopping video: {}".format(self._current.title))
                print("Playing video: {}".format(randVid.title))
                self._current = randVid
                self._pause = False

    def pause_video(self):
        """Pauses the current video."""
        if self._current == None:
            print("Cannot pause video: No video is currently playing")
        elif self._pause == False:
            print("Pausing video: {}".format(self._current.title))
            self._pause = True
        else:
            print("Video already paused: {}".format(self._current.title))

    def continue_video(self):
        """Resumes playing the current video."""
        if self._current == None:
            print("Cannot continue video: No video is currently playing")
        elif self._pause == False:
            print("Cannot continue video: Video is not paused")
        else:
            print("Continuing video: {}".format(self._current.title))
            self._pause = False

    def show_playing(self):
        """Displays video currently playing."""
        if self._current == None:
            print("No video is currently playing")
        elif self._pause == True:
            print("Currently playing: {} ({}) [{}] - PAUSED".format(self._current.title,self._current.video_id," ".join(self._current.tags)))
        else:
            print("Currently playing: {} ({}) [{}]".format(self._current.title,self._current.video_id," ".join(self._current.tags)))

    def search_playlist(self,playlist_name):
        """
            Searches playlist
            Args:
                playlist_name: The playlist name.
            Returns:
                playlist: The playlist object found, if not found None
        """
        for playlist in self._playlist:
            if playlist.name.lower() == playlist_name.lower() :
                return playlist
        return None
    
    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.search_playlist(playlist_name)
        if playlist == None:
            self._playlist.append(Playlist(playlist_name))
            print("Successfully created new playlist: {}".format(self._playlist[len(self._playlist)-1].name))
        else:
            print("Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        playlist = self.search_playlist(playlist_name)
        video = self._video_library.get_video(video_id)
        if playlist == None:
            print("Cannot add video to {}: Playlist does not exist".format(playlist_name))
        elif video == None:
            print("Cannot add video to {}: Video does not exist".format(playlist_name))
        elif video.flagged == True:
            print("Cannot add video to {}: Video is currently flagged (reason: {})".format(playlist_name,video.flagReason))
        elif playlist.getVideo(video_id) != None:
            print("Cannot add video to {}: Video already added".format(playlist_name))
        elif playlist != None and video != None :
            playlist.addVideo(video)
            print("Added video to {}: {}".format(playlist_name,video.title))
        
        


    def show_all_playlists(self):
        """Display all playlists."""

        if len(self._playlist) == 0:
            print("No playlists exist yet")
        else:
            #Insertion Sort
            for i in range(1,len(self._playlist)):
                key = self._playlist[i]
                j = i - 1
                while j >= 0 and self._playlist[j].name > key.name:
                    self._playlist[j+1] = self._playlist[j]
                    j-=1
                self._playlist[j+1] = key
            
            print("Showing all playlists:")
            for playlist in self._playlist:
                print("  "+playlist.name)


    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.search_playlist(playlist_name)
        if playlist == None:
            print("Cannot show playlist {}: Playlist does not exist".format(playlist_name))
        else:
            print("Showing playlist: {}".format(playlist_name))
            if len(playlist.videos) == 0:
                print("No videos here yet")
            else:
                for video in playlist.videos:
                    if video.flagged == True:
                        print("  {} ({}) [{}] - FLAGGED (reason: {})".format(video.title,video.video_id," ".join(video.tags), video.flagReason))
                    else:
                        print("  {} ({}) [{}]".format(video.title,video.video_id," ".join(video.tags)))

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist = self.search_playlist(playlist_name)
        video = self._video_library.get_video(video_id)
        if playlist == None:
            print("Cannot remove video from {}: Playlist does not exist".format(playlist_name))
        elif video == None:
            print("Cannot remove video from {}: Video does not exist".format(playlist_name))
        elif playlist.getVideo(video_id) == None:
            print("Cannot remove video from {}: Video is not in playlist".format(playlist_name))
        else:
            print("Removed video from {}: {}".format(playlist_name,video.title))
            playlist.removeVideo(video)


    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.search_playlist(playlist_name)
        if playlist == None:
            print("Cannot clear playlist {}: Playlist does not exist".format(playlist_name))
        else:
            print("Successfully removed all videos from {}".format(playlist_name))
            playlist.clear()

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.search_playlist(playlist_name)
        if playlist == None:
            print("Cannot delete playlist {}: Playlist does not exist".format(playlist_name))
        else:
            print("Deleted playlist: {}".format(playlist.name))
            self._playlist.remove(playlist)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videosList = []
        videos = self._video_library.get_all_videos()
        for video in videos:
            videoFound = re.search(search_term,video.title,re.IGNORECASE)
            if videoFound != None and video.flagged == False:
                videosList.append(video)
        if len(videosList) == 0:
            print("No search results for {}".format(search_term))
        else:
            #Insertion Sort
            for i in range(1,len(videosList)):
                key = videosList[i]
                j = i - 1
                while j >= 0 and videosList[j].title > key.title:
                    videosList[j+1] = videosList[j]
                    j-=1
                videosList[j+1] = key
            
            #Results
            print("Here are the results for {}:".format(search_term))
            for x in range(len(videosList)):
                print("  {}) {} ({}) [{}]".format(x+1,videosList[x].title,videosList[x].video_id," ".join(videosList[x].tags)))
            #Play
            try:
                print("Would you like to play any of the above? If yes, specify the number of the video.")
                print("If your answer is not a valid number, we will assume it's a no.")
                num = int(input())
            except ValueError:
                return
            if num <= len(videosList) and num > 0:
                self.play_video(videosList[num-1].video_id)



    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        if video_tag[0] == "#":
            videosList = []
            videos = self._video_library.get_all_videos()

            #Search for videos with the tags
            for video in videos:
                videoFound = re.search(video_tag," ".join(video.tags),re.IGNORECASE)
                if videoFound != None and video.flagged == False:
                    videosList.append(video)

            
            if len(videosList) == 0:
                print("No search results for {}".format(video_tag))
            else:
                #Insertion Sort to sort lexographical 
                for i in range(1,len(videosList)):
                    key = videosList[i]
                    j = i - 1
                    while j >= 0 and videosList[j].title > key.title:
                        videosList[j+1] = videosList[j]
                        j-=1
                    videosList[j+1] = key
                
                #Results
                print("Here are the results for {}:".format(video_tag))
                for x in range(len(videosList)):
                    print("  {}) {} ({}) [{}]".format(x+1,videosList[x].title,videosList[x].video_id," ".join(videosList[x].tags)))
                #Play
                try:
                    print("Would you like to play any of the above? If yes, specify the number of the video.")
                    print("If your answer is not a valid number, we will assume it's a no.")
                    num = int(input())
                except ValueError:
                    return
                if num <= len(videosList) and num > 0:
                    self.play_video(videosList[num-1].video_id)
        else:
            print("No search results for {}".format(video_tag))

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot flag video: Video does not exist")
        elif video.flagged == True:
            print("Cannot flag video: Video is already flagged")
        else:
            video._flagged = True
            if len(flag_reason) == 0:
                video._flagReason = "Not supplied"
            else:
                video._flagReason = flag_reason
            if self._current == None:
                print("Successfully flagged video: {} (reason: {})".format(video.title,video.flagReason))
            elif self._current.video_id == video.video_id:
                print("Stopping video: {}".format(self._current.title))
                self._current = None
                print("Successfully flagged video: {} (reason: {})".format(video.title,video.flagReason))
            else:
                print("Successfully flagged video: {} (reason: {})".format(video.title,video.flagReason))
                

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot remove flag from video: Video does not exist")
        elif video.flagged == False:
            print("Cannot remove flag from video: Video is not flagged")
        elif video.flagged == True:
            print("Successfully removed flag from video: {} (reason: {})".format(video.title,video.flagReason))
