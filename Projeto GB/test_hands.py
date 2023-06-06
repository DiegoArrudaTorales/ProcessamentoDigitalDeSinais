import cv2
import mediapipe as mp

video = cv2.VideoCapture(0)

hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=2)  # faz a detecção da mão dentro do vídeo

mpDraw = mp.solutions.drawing_utils # desenha as ligações entre os pontos na mão

while True:
    check, img = video.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # converte a imagem para RGB
    results = Hand.process(imgRGB)  # processa a imagem
    
    handsPoints = results.multi_hand_landmarks # extrai os pontos de dentro do desenho da mão
    h, w, _ = img.shape  # fornece as dimensoes da imagem
    pontos = []

    if handsPoints:
        for points in handsPoints:  # percorre os handsPoints
            print(points) #printa os pontos de coordenadas do desenho da mão
            # desenha os pontos dentro da imagem
            mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS)
            # para enumerar os pontos no desenho
            for id, cord in enumerate(points.landmark):
                cx = int(cord.x*w)
                cy = int(cord.y*h)
                cv2.putText(img, str(id), (cx, cy+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                pontos.append((cx, cy))# retorna um array com a coordenada dos pontos a cada frame

    cv2.imshow("Imagem", img)
    cv2.waitKey(100)

    

video.release()
cv2.destroyAllWindows()
