"""A video class."""

from enum import Flag
from typing import Sequence


class Video:
    """A class used to represent a Video."""

    def __init__(self, video_title: str, video_id: str, video_tags: Sequence[str], flag=None):
        """Video constructor."""
        self._title = video_title
        self._video_id = video_id
        self._flag = flag
        # Turn the tags into a tuple here so it's unmodifiable,
        # in case the caller changes the 'video_tags' they passed to us
        self._tags = tuple(video_tags)

    @property
    def title(self) -> str:
        """Returns the title of a video."""
        return self._title

    @property
    def video_id(self) -> str:
        """Returns the video id of a video."""
        return self._video_id

    @property
    def tags(self) -> Sequence[str]:
        """Returns the list of tags of a video."""
        return self._tags
    
    @property
    def flag(self):
        """Returns the reason why the video is flagged, None if the video is not flagged"""
        return self._flag
    
    #Setter
    def set_flag(self,flag_reason):
        """Sets the flag reason"""
        self._flag = flag_reason
        return True
    
    def remove_flag(self):
        self._flag = None
    
    def __str__(self):
        """Outputs video in the format "title(video_id)[tags]"

            Args:
                video: The video obeject.

            Returns:
                String: "title (video_id) [tags]"
        """
        if self.flag != None:
            return "{} ({}) [{}] - FLAGGED (reason: {})".format(self.title,self.video_id," ".join(self.tags),self.flag)
        else:
            return "{} ({}) [{}]".format(self.title,self.video_id," ".join(self.tags))
