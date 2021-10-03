"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self,playlist_name: str):
        self._playlist_name = playlist_name
        self._videos = dict()#Stores dictonary video_id:video Object

    @property
    def name(self) -> str:
        """Returns the title of a playlist."""
        return self._playlist_name
    
    @property
    def get_all_videos(self) -> dict:
        """Returns the dictonary of the videos."""
        return self._videos

    def get_video(self,video_id):
        """
            Returns the video object
            None if video does not exist
        """
        return self._videos.get(video_id)
    
    def add_video(self,video_id,video):
        """
            Adds video to playlist 
            Returns:
                True if video has been added
        """
        self._videos[video_id] = video
        return True