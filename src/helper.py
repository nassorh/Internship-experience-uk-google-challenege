from typing import Sequence


class Helper():
    def merge_sort(array: Sequence[str]):
        """merge sort implementation  

            Base Case: return if the array len is 1 since we can assume this is a sorted array
            Recursion: breaks the array down to one

        Args:
            Array: array that needs sorting .

        Returns:
            Sorted array
        """
        if len(array) == 1:
            return array
        mid = len(array)//2
        L = Helper.merge_sort(array[:mid])
        R = Helper.merge_sort(array[mid:])
        return Helper.merge(L,R)
    
    def merge(left: Sequence[str],right: Sequence[str]):
        """merge implementation  

        loop through each array
        if the position in one array is smaller than the over
            append to the merge array        

        Args:
            Array: array that needs merging 

        Returns:
            Left and right merged
        """
        output = []
        i = j = 0 #Defines the pointer
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                output.append(left[i])
                i+=1
            else:
                output.append(right[j])
                j+=1
        output.extend(left[i:])
        output.extend(right[j:])
        return output
    
    def searchOutput(foundVideo,search_term):
        """Search videos output  

        If any videos exist in foundVideo
            print the video in the format of x) Title (video_id) [#tags]
            return the index of the video they want to play     

        Args:
            Array: foundVideo is the array of video objecst found 
            String: search_term is the string of the term that was used to search

        Returns:
            Index of video to play
        """
        foundVideo = Helper.videoClean(foundVideo)
        if len(foundVideo) == 0:
            print("No search results for {}".format(search_term))
            return ""
        else:
            print("Here are the results for {}:".format(search_term))
            for x in range(len(foundVideo)):
                print(" {}) {}".format(x+1,foundVideo[x]))
            print("Would you like to play any of the above? If yes, specify the number of the video.\nIf your answer is not a valid number, we will assume it's a no.")
            index = input()
            return index
    
    def indexValidaton(index,foundVideo):
        """Validates the index input   

        Checks if the index is a numeric value and that the index is within range of the array

        Args:
            Array: foundVideo is the array of video objecst found 
            Int: index is the index of the array

        Returns:
            Index of video to play
        """
        if index.isnumeric() and int(index)-1 <= len(foundVideo) and int(index) > 0:
            return True

    def videoClean(videos):
        if len(videos) == 0:
            return None
        videoClean = []

        #Remove all videos with flag
        for video in videos:
            if video.flag == None:
                videoClean.append(video)
        return videoClean