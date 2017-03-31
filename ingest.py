from ingestor.ingestor import Ingestor
from apiclient.errors import HttpError
from oauth2client.tools import argparser


if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--location", help="Location", default="37.42307,-122.08427")
  argparser.add_argument("--location-radius", help="Location radius", default="5km")
  argparser.add_argument("--max-results", help="Max results", default=25)
  args = argparser.parse_args()

  try:
      ingestor = Ingestor()
      ingestor.start(args)
  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
    
