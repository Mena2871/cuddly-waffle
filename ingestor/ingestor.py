from apiclient.discovery import build


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class Ingestor(object):

    def start(self, args):
        '''
        params: args
        '''

        print("Ingesting Videos...")
        self.ingest_videolist(args)
        print("Complete!")

    def ingest_videolist(self, options):
        '''
        Retrieves list of videos from Youtube
        
        params: options
        '''
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey=DEVELOPER_KEY)

        # Call the search.list method to retrieve results matching the specified
        # query term.
        search_response = youtube.search().list(
            q=options.q,
            type="video",
            location=options.location,
            locationRadius=options.location_radius,
            part="id,snippet",
            maxResults=options.max_results
        ).execute()

        search_videos = []
        
        # Merge video ids
        for search_result in search_response.get("items", []):
            search_videos.append(search_result["id"]["videoId"])
            video_ids = ",".join(search_videos)

            # Call the videos.list method to retrieve location details for each video.
            video_response = youtube.videos().list(
                id=video_ids,
                part='snippet, recordingDetails'
            ).execute()

            videos = []

        # Add each result to the list, and then display the list of matching videos.
        for video_result in video_response.get("items", []):
            videos.append("%s, (%s,%s)" % (video_result["snippet"]["title"],
                                           video_result["recordingDetails"]["location"]["latitude"],
                                           video_result["recordingDetails"]["location"]["longitude"]))
            
        print("Videos:\n", "\n".join(videos), "\n")
