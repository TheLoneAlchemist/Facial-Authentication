import face_recognition
def ImageAuthentication(image1,image2):
    print(image1,"+++++++++++")
    
    image1 = f'media/{image1}'
    image2 = f'media/{image2}'
    print(image2,"_____________")
    known = face_recognition.load_image_file(image1)
    unknown = face_recognition.load_image_file(image2)
    print(known)
    print("______________________")
    print(unknown)
    knownencod = face_recognition.face_encodings(known)[0]
    unknownencod = face_recognition.face_encodings(unknown)[0]
    # print(knownencod)
    # print(unknownencod)

    result = face_recognition.compare_faces([knownencod],unknownencod)

    print("Image Result: " ,result) 
    
    return result

from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent

# filepath = f'{BASE_DIR}\media\\faces\hello@admin.com.jpeg'
# filepath1 = f'{BASE_DIR}\media\\faces\hello@admin.com1.jpeg'

# i = ImageAuthentication(filepath,filepath)


def FindMatch(unknown,images : list):
    '''
    Funtion that allows to find matches from a list of images\n
    use:\n \tFindMatch(unknownImage, Images:list)
    '''
    result = None
    print(unknown)
    print(images)
    for image in images[1:]:
        print(image)
        result = ImageAuthentication(image,unknown)
        print("---------------->",type(result))
        if result[0] == True:
            return True
    
    return False

