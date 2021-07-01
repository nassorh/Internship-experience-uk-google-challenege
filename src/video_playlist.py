"""A video playlist class."""


from array import array


class Playlist:
    def __init__(self, playListName):
        self._name = playListName
        self._videos = []
    """A class used to represent a Playlist."""

    @property
    def name(self) -> str:
        """Returns the naem of the platlist."""
        return self._name

    @property
    def videos(self) -> array:
        """Returns the array of a video."""
        return self._videos
    
    def addVideo(self,video):
        """
            Adds video the playlist
            Args:
                video: The video object
        """
        self._videos.append(video)

    def removeVideo(self,video):
        """
            Remove video from video list
            Args:
                video: The video object
        """
        self._videos.remove(video)

    def getVideo(self,video_id):
        """
            Fetches the video object
            Args:
                video_id: The id of the video object
            Returns:
                video: The video object, None if not found
        """
        for video in self._videos:
            if video.video_id== video_id:
                return video
        return None

    def clear(self):
        """
            Clears playlist
        """
        self._videos = []