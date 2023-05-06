import pytesseract as pt
import cv2 as cv
import numpy as np
import os

pt.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def folder_img_to_text(folder):
    '''  Recebe uma o caminho de uma pasta de imagens (folder)

        Converte todas o texto de todas as em 'folder' para um arquivo .txt  e armazena 
        na pasta 'images_ txt' com o nome do arquivo da imagem.
    
        Retorna null
    '''

    files = os.listdir(folder)

    for file in files:
        path_to_image = 'images/' + file #implementa o nome do arquivo para o caminho da imagem
        image_cv = cv.imread(path_to_image)
        
        if file.endswith('jpg'): #se a imagem for jpg, cria um caminho para o arquivo da imagem no formato de texto
            image_txt = file.replace('jpg','txt')
            image_txt = 'images_txt/' + image_txt
        else:
            image_txt = file.replace('png','txt')
            image_txt = 'images_txt/' + image_txt

        if 'photo_29_2022-11-22_10-32-53' in file:
            image_cv = select_rgb_image(image_cv,'r')
            extractedInformation = pt.image_to_string(image_cv, lang='por')
            with open(image_txt,'w') as f: #abre/cria o arquivo de imagem em forma de texto no modo de escrita e escreve a 'extractedInformation' dentro do arquivo
                f.write(extractedInformation)

        else:
            image_cv = binarize_image(image_cv)
            extractedInformation = pt.image_to_string(image_cv, lang='por') #cria uma variável que armazena a imagem em forma de texto
            with open(image_txt,'w') as f: #abre/cria o arquivo de imagem em forma de texto no modo de escrita e escreve a 'extractedInformation' dentro do arquivo
                f.write(extractedInformation)


def gray_scale(img):
    ''' Transforma uma imagem e a retorna na escala de cinza'''
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)

def binarize_image(img):
    ''' Transforma uma imagem em binária - preto e branco e a retorna.'''
    gray_img = gray_scale(img)
    thresh, bw_img = cv.threshold(gray_img, 200, 230, cv.THRESH_BINARY)
    return bw_img

'''def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv.erode(image, kernel, iterations=1)
    image = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)
    image = cv.medianBlur(image, 3)
    return (image)

def thin_font(image):
    import numpy as np
    image = cv.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv.erode(image, kernel, iterations=1)
    image = cv.bitwise_not(image)
    return (image)'''

def select_rgb_image(img, color):
    b,g,r = cv.split(img)
    if color == 'r':
        return r
    elif color == 'b':
        return b 
    elif color == 'g':
        return g
    else: 
        return

folder_img_to_text('images')
