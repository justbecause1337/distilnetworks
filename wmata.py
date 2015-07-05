########### Python 2.7 #############
import httplib, urllib, base64, json

headers = {
   # Basic Authorization Sample
   # 'Authorization': 'Basic %s' % base64.encodestring('{username}:{password}'),
}

params = urllib.urlencode({
   # Specify your subscription key
   'api_key': 'kfgpmgvfgacx98de9q3xazww',
})

try:
   conn = httplib.HTTPSConnection('api.wmata.com')
   conn.request("GET", "/StationPrediction.svc/json/GetPrediction/K04?%s" % params, "", headers)
   response = conn.getresponse()
   data = response.read()
   data = json.loads(data)

   fstTrain = None
   fstEBTrain = None
   fstWBTrain = None
   friends = []

   print "Raw Data from API."
   print data
   print "\n"

   for train in data["Trains"]:
      
       if train["Line"] == ("OR"):
          #ARR (arriving -2), BRD (boarding -1), or --- (None)
          #Reset Weights for Comparison
          if train["Min"] == ("ARR"):
             train["Min"] = "-1"
          elif train["Min"] == ("BRD"):
             train["Min"] = "-2"
          elif train["Min"] == ("--"): #Says this "---" in API I have actually seen this "--"
             train["Min"] = "+inf"

          #Init first Train
          if fstTrain is None:
             fstTrain = train
          #Compare Trains
          elif train["Min"] != None and float(fstTrain["Min"]) == float(train["Min"]):
             friends.append(train)
          elif train["Min"] != None and float(fstTrain["Min"]) > float(train["Min"]):
             fstTrain = train
             friends = []

   print "Results"
   if fstTrain != None:
      #Reset Weights for Output
      print "The following train(s) are the first Orange line trains arriving at Ballston Metro."
      friends.append(fstTrain)
      for friend in friends:
         if friend["Min"] == ("-1"):
            friend["Min"] = "ARR"
         elif friend["Min"] == ("-2"):
            friend["Min"] = "BRD"
         elif friend["Min"] == ("+inf"): #Says this "---" in API I have actually seen this "--"
            friend["Min"] = "--"
         print friend
   else:
      print "There are no Orange Line trains available!"
       
   conn.close()
except Exception as e:
   print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################
