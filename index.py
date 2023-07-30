from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from random import randint
from innertube import InnerTube
from ytmusicapi import YTMusic

app = Flask(__name__)
CORS(app)
api = Api(app)

# Client for YouTube on iOS
client = InnerTube("IOS")

ytmusic = YTMusic()

cat = {
    "chill" : "ggMPOg1uX1JOQWZFeDByc2Jm",
    "commute" : "ggMPOg1uX044Z2o5WERLckpU",
    "energy booster" : "ggMPOg1uX2lRZUZiMnNrQnJW",
    "feel good" : "ggMPOg1uXzZQbDB5eThLRTQ3",
    "focus" : "ggMPOg1uX0NvNGNhWThMYWRh",
    "party" : "ggMPOg1uX0pmQ0s2V0JRclZs",
    "romance" : "ggMPOg1uX0FzQ2FhZWtUY211",
    "sleep" : "ggMPOg1uX1MxaFQ3Z0JMZkN4",
    "workout" : "ggMPOg1uX09LWkhnTjRGRUJh", 
}
'''
class Search(Resource):
    def get(self):
        client = InnerTube("IOS_MUSIC")
        if(not request.args.get("search")):
            return {"error": "No search query provided"}
        data = client.search(query=request.args.get("search"))
        video_id = []
        for k in range(0,len(data["contents"]["tabbedSearchResultsRenderer"]["tabs"])):
        
            for i in range(0,len(data["contents"]["tabbedSearchResultsRenderer"]["tabs"][k]["tabRenderer"]["content"]["sectionListRenderer"]["contents"])):
                    try:
                        for j in range(len(data["contents"]["tabbedSearchResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][i]["musicShelfRenderer"]["contents"])):
                            try:
                                video_id.append(data["contents"]["tabbedSearchResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][i]["musicShelfRenderer"]["contents"][j]["musicTwoColumnItemRenderer"]["navigationEndpoint"]["watchEndpoint"]["videoId"])
                            except:
                                pass
                    except:
                        pass
        streamobj = []
        key = 1
        client = InnerTube("ANDROID_MUSIC")
        for vid in video_id:
            data = InnerTube("ANDROID_MUSIC").player(vid)
            if "streamingData" in data:
                streams = data["streamingData"]["adaptiveFormats"]
                title = data["videoDetails"]["title"]
                author = data["videoDetails"]["author"]
                viewcount = data["videoDetails"]["viewCount"]
                videoid = data["videoDetails"]["videoId"]
                data = InnerTube("IOS").player(vid)
                thumbnail = data["videoDetails"]["thumbnail"]["thumbnails"][2]["url"] if len(data["videoDetails"]["thumbnail"]["thumbnails"])>2 else data["videoDetails"]["thumbnail"]["thumbnails"][1]["url"]
                li=[]
                for i in streams:
                    if i["itag"]==251:
                        li.append({"url":i["url"],"mimeType":i["mimeType"].split(";")[0]}) 
                streamobj.append({"id":key,"title":title,"author":author,"thumbnail":thumbnail,"streamlinks":li,"viewcount":viewcount,"videoid":videoid})
                key+=1  
        return jsonify(streamobj)
'''
class Search(Resource):
    def get(self):
        if(not request.args.get("search")):
            return {"error": "No search query provided"}
        search_results = []
        for i in ytmusic.search(query=request.args.get("search"),filter="videos"):
            search_results.append({"title": i["title"],"videoId": i["videoId"],"duration": i["duration"],"artists":i["artists"][0]["name"],"thumbnails":i["thumbnails"][0]["url"]})
        for i in ytmusic.search(query=request.args.get("search"),filter="songs"):
            search_results.append({"title": i["title"],"videoId": i["videoId"],"duration": i["duration"],"artists":i["artists"][0]["name"],"thumbnails":i["thumbnails"][len(i["thumbnails"])-1]["url"]})
        return search_results

class SearchSuggestion(Resource):
    def __init__(self):
        self.client = InnerTube("IOS_MUSIC")

    def get(self):
        if len(request.args.get("query"))==0:
            return {"suggestions": [""]}
        data = self.client.music_get_search_suggestions(request.args.get("query"))
        suggestions = []
        for i in range(len(data["contents"][0]["searchSuggestionsSectionRenderer"]["contents"])):
            suggestions.append(data["contents"][0]["searchSuggestionsSectionRenderer"]["contents"][i]["searchSuggestionRenderer"]["navigationEndpoint"]["searchEndpoint"]["query"])
        return {"suggestions": suggestions}
    
class NextSongResource(Resource):
    def get(self, vid):
        client = InnerTube("WEB_MUSIC")
        data = client.next(vid)
        i = randint(1,len(data["contents"]["singleColumnMusicWatchNextResultsRenderer"]["playlist"]["playlistPanelRenderer"]["contents"])-1)
        print(i)
        videoid = data["contents"]["singleColumnMusicWatchNextResultsRenderer"]["playlist"]["playlistPanelRenderer"]["contents"][i]["playlistPanelVideoRenderer"]["videoId"]
        if vid == videoid:
            data = client.next(vid)
            i = randint(0,len(data["contents"]["singleColumnMusicWatchNextResultsRenderer"]["playlist"]["playlistPanelRenderer"]["contents"])-1)
            videoid = data["contents"]["singleColumnMusicWatchNextResultsRenderer"]["playlist"]["playlistPanelRenderer"]["contents"][i]["playlistPanelVideoRenderer"]["videoId"]
        streamobj = []
        data = InnerTube("ANDROID_MUSIC").player(videoid)
        streams = data["streamingData"]["adaptiveFormats"]
        title = data["videoDetails"]["title"]
        author = data["videoDetails"]["author"]
        viewcount = data["videoDetails"]["viewCount"]
        thumbnail = data["videoDetails"]["thumbnail"]["thumbnails"][len(data["videoDetails"]["thumbnail"]["thumbnails"])-1]["url"]
        videoid = data["videoDetails"]["videoId"]
        li=[]
        for i in streams:
            if i["itag"]==251:
                li.append({"url":i["url"],"mimeType":i["mimeType"].split(";")[0]}) 
        streamobj.append({"id":1,"title":title,"author":author,"thumbnail":thumbnail,"streamlinks":li,"viewcount":viewcount,"videoid":videoid})
        return jsonify(streamobj)
    
class Playlists(Resource):
    def get(self):
        return ytmusic.get_mood_playlists(cat[request.args.get("cat")])

class PlaylistSong(Resource):
    def get(self,pid):
        return ytmusic.get_playlist(pid)
    
class SongDetails(Resource):
    def get(self,vid):
        streamobj = []
        data = InnerTube("ANDROID_MUSIC").player(vid)
        if "streamingData" in data:
            streams = data["streamingData"]["adaptiveFormats"]
            title = data["videoDetails"]["title"]
            author = data["videoDetails"]["author"]
            viewcount = data["videoDetails"]["viewCount"]
            videoid = data["videoDetails"]["videoId"]
            thumbnail = data["videoDetails"]["thumbnail"]["thumbnails"][len(data["videoDetails"]["thumbnail"]["thumbnails"])-1]["url"]
            li=[]
            for i in streams:
                if i["itag"]==251:
                    li.append({"url":i["url"],"mimeType":i["mimeType"].split(";")[0]}) 
            streamobj.append({"id":1,"title":title,"author":author,"thumbnail":thumbnail,"streamlinks":li,"viewcount":viewcount,"videoid":videoid})
        return jsonify(streamobj)

api.add_resource(Search, '/')
api.add_resource(SearchSuggestion, "/search_suggestion")
api.add_resource(NextSongResource, '/next/<string:vid>')
api.add_resource(Playlists, '/playlist')
api.add_resource(PlaylistSong, '/playlist/song/<string:pid>')
api.add_resource(SongDetails, '/songdetails/<string:vid>')

if __name__ == '__main__':
    app.run(debug=True)
