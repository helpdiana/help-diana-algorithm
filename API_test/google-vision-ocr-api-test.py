import os, io
from google.cloud.bigquery.client import Client
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ''
bq_client = Client()

def detect_text(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)


    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    
    

    for text in texts:
        print('\n"{}"'.format(text.description))
    
    

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
        
    


detect_text("test1.png")