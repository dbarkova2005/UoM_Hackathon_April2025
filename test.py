import PIL.Image

from google import genai
from google.genai import types
from os import listdir

def get_output_of_panel():
	client = genai.Client(api_key="AIzaSyAXhTlzcjOer55cngHl2awrRxwVxLRoJ3c")
	FACES_PATH = "faces/"

	# client.models.generate_content(
	#         model="gemini-2.0-flash",
	#         contents=[""])
		
	for imageName in listdir(FACES_PATH):
		name = imageName.split(".")[0]
		image = PIL.Image.open(FACES_PATH + imageName)

		client.models.generate_content(
			model="gemini-2.0-flash",
			contents=[f"This is {name}", image])
		

	image = PIL.Image.open("./lesson.webp")
	response = client.models.generate_content(
			model="gemini-2.0-flash",
			contents=[f"This is how you read a manga panel;", image])

	image = PIL.Image.open("manga_panel\love_is_war8.png")
	response = client.models.generate_content(
			model="gemini-2.0-flash",
			contents=[f"Give me the dialogue in the manga panel and format it with: NAME: <SPEECH>", image])

	#print(response.text)

	ray = response.text.split('\n')
	#print(ray)
	del ray[0]
	ray.remove('')
	for tup in range(0, len(ray)):
		ray[tup] = ray[tup].split(":")
		ray[tup][1] = ray[tup][1].lower()
	print(ray)
	return ray

get_output_of_panel()