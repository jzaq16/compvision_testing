from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time



'''
Authenticate
Authenticates your credentials and creates a client.
'''
# <snippet_vars>
subscription_key = "c064f610e7274dcf96c613cefa50435a"
endpoint = "https://pcs-compvision-test-001.cognitiveservices.azure.com/"

# </snippet_vars>

# <snippet_client>
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
# </snippet_client>
'''
END - Authenticate
'''

# local_image_url = "C:\Users\Derek.Johanson\Documents\development\OCR\id.jpg"


'''
Batch Read File, recognize handwritten text - remote
This example will extract handwritten text in an image, then print results, line by line.
This API call can also recognize handwriting (not shown).
'''
print("===== Batch Read File - remote =====")
# Get an image with handwritten text
remote_image_handw_text_url = r"https://i.pinimg.com/236x/76/6b/be/766bbeed4408251e73c52a1b8ab74ca9.jpg"

# Call API with URL and raw response (allows you to get the operation location)
recognize_handw_results = computervision_client.read(remote_image_handw_text_url,  raw=True)

# Get the operation location (URL with an ID at the end) from the response
operation_location_remote = recognize_handw_results.headers["Operation-Location"]
# Grab the ID from the URL
operation_id = operation_location_remote.split("/")[-1]

# Call the "GET" API and wait for it to retrieve the results 
while True:
    get_handw_text_results = computervision_client.get_read_result(operation_id)
    if get_handw_text_results.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Print the detected text, line by line
if get_handw_text_results.status == OperationStatusCodes.succeeded:
    for text_result in get_handw_text_results.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
print()