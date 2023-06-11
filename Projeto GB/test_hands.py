import cv2
import mediapipe as mp
import os
import time

video = cv2.VideoCapture(0)

hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=1)  # faz a detecção da mão dentro do vídeo

mpDraw = mp.solutions.drawing_utils # desenha as ligações entre os pontos na mão
contadorGeral = 0
ultimosNumeros = [0,0,0] 
senha=[0,0,0,0]
senhacorreta=[1,2,3,4]

while True:
    check, img = video.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # converte a imagem para RGB
    results = Hand.process(imgRGB)  # processa a imagem
    
    handsPoints = results.multi_hand_landmarks # extrai os pontos de dentro do desenho da mão
    h, w, _ = img.shape  # fornece as dimensoes da imagem
    pontos = []
    

    def detectador(ultimaLeitura = 0, contadorGeral=0, posicaoSenha=0):
        
        if handsPoints:
            for points in handsPoints:  # percorre os handsPoints
                #print(points) #printa os pontos de coordenadas do desenho da mão
                # desenha os pontos dentro da imagem
                mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS)
                # para enumerar os pontos no desenho
                for id, cord in enumerate(points.landmark):
                    cx = int(cord.x*w)
                    cy = int(cord.y*h)
                    cv2.putText(img, str(id), (cx, cy+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    pontos.append((cx, cy))# retorna um array com a coordenada dos pontos a cada frame
                    #print(id,pontos)
            dedos=[8,12,16,20] 
            contador = 0
            
            if points:
                dedao=0
                distanciapontabase1 = 17
                distanciapontabase2 = 45
                for x in dedos:
                    if((abs(pontos[8][1]-pontos[8-2][1])>distanciapontabase1 or abs(pontos[8][0]-pontos[8-2][0])>distanciapontabase1 or abs(pontos[12][1]-pontos[12-2][1])>distanciapontabase1 or abs(pontos[12][0]-pontos[12-2][0])>distanciapontabase1 or abs(pontos[16][1]-pontos[16-2][1])>distanciapontabase1 or abs(pontos[16][0]-pontos[16-2][0])>distanciapontabase1 or abs(pontos[20][1]-pontos[20-2][1])>distanciapontabase1 or abs(pontos[20][0]-pontos[20-2][0])>distanciapontabase1)\
                    and (abs(pontos[8][1]-pontos[8-3][1])>distanciapontabase2 or abs(pontos[8][0]-pontos[8-3][0])>distanciapontabase2 or abs(pontos[12][1]-pontos[12-3][1])>distanciapontabase2 or abs(pontos[12][0]-pontos[12-3][0])>distanciapontabase2 or abs(pontos[16][1]-pontos[16-3][1])>distanciapontabase2 or abs(pontos[16][0]-pontos[16-3][0])>distanciapontabase2 or abs(pontos[20][1]-pontos[20-3][1])>distanciapontabase2 or abs(pontos[20][0]-pontos[20-3][0])>distanciapontabase2)
                    and ((pontos[8][1]<pontos[8-3][1]) or (pontos[12][1]<pontos[12-3][1]) or (pontos[16][1]<pontos[16-3][1]) or (pontos[20][1]<pontos[20-3][1]))
                    and ((pontos[8][1]<pontos[8-1][1]) or (pontos[12][1]<pontos[12-1][1]) or (pontos[16][1]<pontos[16-1][1]) or (pontos[20][1]<pontos[20-1][1]))):# Mitigando erros quando a mão está fechada, reconhecendo dedos fechados):# Mitigando erros quando a mão está fechada, reconhecendo dedos fechados
                        #if pontos[x][1] < :
                        if pontos [x-2][1] - pontos[x][1]>distanciapontabase1:
                            contador += 1    
                        if((pontos[4][0] < pontos[3][0]) and (pontos[8][0] < pontos[20][0]) and dedao==0): # dedão com palma da mão para frente
                            contador += 1
                            dedao=1
                        if((pontos[4][0] > pontos[3][0]) and (pontos[8][0] > pontos[20][0]) and dedao==0): # dedão com palma da mão para trás 
                            contador += 1
                            dedao=1
                    else:
                        contador=0                 
                        if ((pontos[2][1] - pontos[4][1]>60) and (pontos[5][1]<pontos[17][1]) and (pontos[5][1]<pontos[14][1])): # DETECTOU MÃO FECHADA E POLEGAR PARA CIMA = JOINHA
                            print("JOINHA DETECTADO")
                            cv2.putText(img,str('Joinha detectado'),(50,270),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),5)
            

            if contador == ultimaLeitura:
                contadorGeral += 1        
            else:
                contadorGeral=0

            if contadorGeral>22:
                print('Digito registrado') 
                print('posicao senha:',posicaoSenha)
                senha[posicaoSenha] = contador
              
                    
                if posicaoSenha<3:
                    posicaoSenha+= 1
                else:
                    posicaoSenha=0                    
                print('senha atual : ', str(senha))
                contadorGeral=0
            #print(('2 - '))
            #print(pontos[4][1])
            #print('4 - ')
            #print(pontos[2][1])
            print('Contador geral',contadorGeral)
            print('Contador atual',contador)
            cv2.rectangle(img,(80,10),(200,110),(255,0,0),-1)
            cv2.putText(img,str(contador),(100,100),cv2.FONT_HERSHEY_SIMPLEX,4,(255,255,255),5)

            cv2.rectangle(img,(250,10),(500,90),(255,0,0),-1)
            cv2.putText(img,str(senha),(260,45),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),5)
            cv2.putText(img,str("Lendo senha..."),(300,75),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),5)

            if senha == senhacorreta:
                print("senha correta")
                cv2.putText(img,str('Senha correta'),(50,270),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),5)
            
            return contador, contadorGeral, posicaoSenha

    if handsPoints:    
        ultimosNumeros = detectador(ultimosNumeros[0],ultimosNumeros[1],ultimosNumeros[2])

    cv2.imshow("Imagem", img)
    cv2.waitKey(100)

    

video.release()
cv2.destroyAllWindows()
