import pytesseract as pt
import cv2 as cv
import numpy as np
import os

pt.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def resize_image(img):
    ''' Recebe uma imagem e a retorna no tamanho adequado para leitura.'''

    h, w, c = img.shape
    if h > 1000 or w > 1000:
        image_rszd = cv.resize(img, (1000,600))
        return (image_rszd)
    elif h < 400 or w < 400:
        image_rszd = cv.resize(img, (800,800))
        return (image_rszd)
    else: return img

def gray_scale(img):
    ''' Transforma uma imagem e a retorna na escala de cinza'''
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)

def binarize_image(img):
    ''' Transforma uma imagem em binária - preto e branco e a retorna.'''
    gray_img = gray_scale(img)
    thresh, bw_img = cv.threshold(gray_img, 200, 255, cv.THRESH_BINARY)
    return bw_img

def noise_removal(img):
    ''' Recebe a imagem e a retorna sem o ruido'''
    kernel = np.ones((1, 1), np.uint8)
    img = cv.dilate(img, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    img = cv.erode(img, kernel, iterations=1)
    img = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)
    img = cv.medianBlur(img, 3)
    return (img)

def thin_font(img): 
    img = cv.bitwise_not(img)
    kernel = np.ones((2,2),np.uint8)
    img = cv.erode(img, kernel, iterations=1)
    img = cv.bitwise_not(img)
    return (img)

def select_rgb_image(img, color):
    ''' Recebe uma imagem e uma cor - ('b' = blue // 'r' = red // 'g' = green)
    
        A partir da cor recebida, focaliza a cor escolhida na imagem e a retorna.   
    '''
    b,g,r = cv.split(img)
    if color == 'r':
        return r
    elif color == 'b':
        return b 
    elif color == 'g':
        return g
    else: 
        return img
    
def image_to_txt(file):
    ''' Recebe o arquivo de uma imagem .png ou .jpg e retorna o nome do arquivo com o tipo .txt
    
        Se o arquivo enviado não for .png ou .jpg - retorna erro.
    '''

    if file.endswith('jpg'): #se a imagem for jpg, cria um caminho para o arquivo da imagem no formato de texto
        image_txt = file.replace('jpg','txt')
        image_txt = 'images_txt/' + image_txt
        return image_txt
    elif file.endswith('png'):
        image_txt = file.replace('png','txt')
        image_txt = 'images_txt/' + image_txt
        return image_txt
    else:
        return ValueError('Imagem recebida não é do tipo .png ou .jpg')

def write_image_txt(image_txt, image_cv, myconfig = r"--psm 3 --oem 3"):
    ''' Recebe o caminho para um arquivo .txt - '''
    extractedInformation = pt.image_to_string(image_cv, lang= 'por', config= myconfig) #cria uma variável que armazena a imagem em forma de texto
    with open(image_txt,'w') as f: #abre/cria o arquivo de imagem em forma de texto no modo de escrita e escreve a 'extractedInformation' dentro do arquivo
        f.write(extractedInformation)

def test_img(img):
    ''' Recebe uma imagem - faz o tratamento e mostra na tela'''
    image_cv = cv.imread(img)
    image_cv = resize_image(image_cv)
    image_cv = binarize_image(image_cv)
    cv.imshow(img,image_cv)
    cv.waitKey(0)
    

def folder_img_to_text(folder):
    '''  Recebe uma o caminho de uma pasta de imagens (folder)

        Converte todas o texto de todas as em 'folder' para um arquivo .txt  e armazena 
        na pasta 'images_ txt' com o nome do arquivo da imagem.
    
        Retorna null
    '''

    files = os.listdir(folder)

    for file in files:
        path_to_image = folder + file #implementa o nome do arquivo para o caminho da imagem
        image_cv = cv.imread(path_to_image)
        config = r"--psm 3 --oem 3"

        image_cv = resize_image(image_cv)
        image_path_txt = image_to_txt(file)

        if 'photo_29_2022-11-22_10-32-53' in file:
            image_cv = select_rgb_image(image_cv,'r')
            write_image_txt(image_path_txt, image_cv)

        else:
            image_cv = binarize_image(image_cv)
            write_image_txt(image_path_txt, image_cv)


'''files = os.listdir('images/') # mostra todas as imagens tratadas
for i in files:
    test_img('images/' + i)
'''
folder_img_to_text('images/') #executa o código chamando como parametro a pasta de imagens






