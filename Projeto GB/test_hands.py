import cv2
import mediapipe as mp

video = cv2.VideoCapture(0)

hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=1)  # faz a detecção da mão dentro do vídeo

mpDraw = mp.solutions.drawing_utils # desenha as ligações entre os pontos na mão
contadorGeral = 10 # Usado para o tempo de exibicao das mensagens na tela
contadorGeralSenha = 0 # Usado para definir o tempo que o usuário deve repetir a mesma leitura para considerar valida 
ultimosNumeros = [0,0,0,10] # valores iniciais do loop, realimentamos o loop com os valores gerado da última execução
senha=[0,0,0,0] # senha inicial
senhacorreta=[1,2,3,4] # senha esperada

while True:
    check, img = video.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # converte a imagem para RGB
    results = Hand.process(imgRGB)  # processa a imagem
    
    handsPoints = results.multi_hand_landmarks # extrai os pontos de dentro do desenho da mão
    h, w, _ = img.shape  # fornece as dimensoes da imagem
    pontos = []

    def detectador(ultimaLeitura = 0, contadorGeralSenha=0, posicaoSenha=0, contadorGeral=10): # Função principal
        
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
                dedao=0 # usado para não gerar duplicidade na leitura do dedão
                dedaoUp = (pontos[2][1] - pontos[4][1]>40) and (pontos[5][1]<pontos[17][1]) and (pontos[5][1]<pontos[14][1]) 
                palmadaMao = pontos[8][0] < pontos[20][0]
                trasdaMao = pontos[8][0] > pontos[20][0]
                distanciapontabase1 = 17
                distanciapontabase2 = 45
                analisePontaBase1 = (abs(pontos[8][1]-pontos[8-2][1])>distanciapontabase1 or abs(pontos[8][0]-pontos[8-2][0])>distanciapontabase1 or abs(pontos[12][1]-pontos[12-2][1])>distanciapontabase1 or abs(pontos[12][0]-pontos[12-2][0])>distanciapontabase1 or abs(pontos[16][1]-pontos[16-2][1])>distanciapontabase1 or abs(pontos[16][0]-pontos[16-2][0])>distanciapontabase1 or abs(pontos[20][1]-pontos[20-2][1])>distanciapontabase1 or abs(pontos[20][0]-pontos[20-2][0])>distanciapontabase1) 
                analisePontaBase2 = (abs(pontos[8][1]-pontos[8-3][1])>distanciapontabase2 or abs(pontos[8][0]-pontos[8-3][0])>distanciapontabase2 or abs(pontos[12][1]-pontos[12-3][1])>distanciapontabase2 or abs(pontos[12][0]-pontos[12-3][0])>distanciapontabase2 or abs(pontos[16][1]-pontos[16-3][1])>distanciapontabase2 or abs(pontos[16][0]-pontos[16-3][0])>distanciapontabase2 or abs(pontos[20][1]-pontos[20-3][1])>distanciapontabase2 or abs(pontos[20][0]-pontos[20-3][0])>distanciapontabase2)
                analiseSentidoPontaBase1 = ((pontos[8][1]<pontos[8-3][1]) or (pontos[12][1]<pontos[12-3][1]) or (pontos[16][1]<pontos[16-3][1]) or (pontos[20][1]<pontos[20-3][1]))
                analiseSentidoPontaBase2 = ((pontos[8][1]<pontos[8-1][1]) or (pontos[12][1]<pontos[12-1][1]) or (pontos[16][1]<pontos[16-1][1]) or (pontos[20][1]<pontos[20-1][1]))
                maoAberta = analisePontaBase1 and analisePontaBase2 and analiseSentidoPontaBase1 and analiseSentidoPontaBase2
                                                
                for x in dedos:
                    if(maoAberta):# Mitigando erros quando a mão está fechada, reconhecendo apenas contagem quando algum dedo estiver aberto(exceto dedão)
                        
                        if pontos [x-2][1] - pontos[x][1]>distanciapontabase1: # reconhecendo dedos levantados
                            contador += 1    
                        if(((pontos[4][0] - pontos[3][0])<-9) and (palmadaMao) and dedao==0): # dedão com palma da mão para frente
                            contador += 1
                            dedao=1
                        if(((pontos[4][0] - pontos[3][0])>9) and (trasdaMao) and dedao==0): # dedão com palma da mão para trás 
                            contador += 1
                            dedao=1
              
                     
                        print("doze menos dezeseis:",str(pontos[12][0] - pontos[16][0]))
                      
                        pardeDedosJuntos = (pontos[8][0] - pontos[12][0]<33 and (pontos[16][0]- pontos[20][0])<33)
                        pardeDedosSeparados = (pontos[12][0] - pontos[16][0]>55)
                        Vulcano = (contador == 5 and pardeDedosJuntos and pardeDedosSeparados)
                        print(pardeDedosJuntos)
                        print(pardeDedosSeparados)
                        
                        if (Vulcano): # DETECTOU MÃO ABERTA E SINAL Vulcano 
                            
                            if senha == senhacorreta:
                                 print("senha correta")
                                 cv2.putText(img,str('Senha correta!!'),(40,270),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),5)
                                 print("ACESSO LIBERADO")
                                 cv2.putText(img,str('Vulcado Detectado!'),(39,320),cv2.FONT_HERSHEY_SIMPLEX,2,(80, 200, 120),5)
                                 cv2.putText(img,str('Acesso Admin'),(40,370),cv2.FONT_HERSHEY_SIMPLEX,2,(80, 200, 120),5)
                                 cv2.putText(img,str('concedido!!'),(40,420),cv2.FONT_HERSHEY_SIMPLEX,2,(80, 200, 120),5)
                                 contadorGeralSenha=0
                        
                    else:#Mao Fechada
                        contador=0                 
                        if (dedaoUp): # DETECTOU MÃO FECHADA E POLEGAR PARA CIMA = JOINHA
                            
                            if senha == senhacorreta:
                                 print("senha correta")
                                 cv2.putText(img,str('Senha correta'),(45,270),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),5)
                                 print("ACESSO LIBERADO")
                                 cv2.putText(img,str('ACESSO LIBERADO'),(45,320),cv2.FONT_HERSHEY_SIMPLEX,2,(80, 200, 120),5)
                                 contadorGeralSenha=0
                            else:  
                                print("JOINHA DETECTADO")
                                cv2.putText(img,str('Joinha detectado'),(45,270),cv2.FONT_HERSHEY_SIMPLEX,2,(124, 252, 0),5)
                                contadorGeralSenha=0   
            Vulcano = (contador == 5 )
            contadorGeral+=1
            if contador == ultimaLeitura:
                contadorGeralSenha += 1        
            else:
                contadorGeralSenha=0

            if contadorGeralSenha>17:
                print('Digito registrado') 
                print('posicao senha:',posicaoSenha)
                senha[posicaoSenha] = contador
                    
                if posicaoSenha<3:
                    posicaoSenha+= 1
                else:
                    if senha != senhacorreta: 
                        print('Reiniciando leitura')
                        
                        senha[0]=0
                        senha[1]=0
                        senha[2]=0
                        senha[3]=0

                        posicaoSenha=0
                        contadorGeral=0

                    else:
                        if contadorGeral>25 and (dedaoUp)==False:#senha correta seta contador geral para zero, será resetado ao chegar em 20
                            contadorGeral=0
                          
                contadorGeralSenha=0

            if contadorGeral<10 and senha==[0,0,0,0]: #Tempo de exibicao na tela
                cv2.putText(img,str('Reiniciando leitura'),(50,470),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),5)

            senhacorretaejoinhaoff = senha==[1,2,3,4] and (dedaoUp)==False and Vulcano==False     
            
            if contadorGeral>18 and senhacorretaejoinhaoff: #Tempo para reset após senha correta
                print('Reiniciando leitura')
                cv2.putText(img,str('Reiniciando leitura'),(50,470),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),5)
                if contadorGeral>30:
                    posicaoSenha=0
                    senha[0]=0
                    senha[1]=0
                    senha[2]=0
                    senha[3]=0

            #Logs de controle:
            print('Contador geral Senha',contadorGeralSenha)
            print('Contador geral',contadorGeral)
            print('Contador atual',contador)
            print('senha atual : ', str(senha))
            cv2.rectangle(img,(80,10),(200,110),(255,0,0),-1)
            cv2.putText(img,str(contador),(100,100),cv2.FONT_HERSHEY_SIMPLEX,4,(255,255,255),5)

            match posicaoSenha: # exibição da posição atual ao usuário 
                case 0: posicaodot = 280
                case 1: posicaodot = 327            
                case 2: posicaodot = 373            
                case 3: posicaodot = 420                        
            cv2.rectangle(img,(250,7),(500,90),(255,0,0),-1)
            cv2.putText(img,str(senha),(260,45),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),5)
            cv2.putText(img,str("."),(posicaodot,15),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
            cv2.putText(img,str("Lendo senha..."),(300,75),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),5)
            
            return contador, contadorGeralSenha, posicaoSenha, contadorGeral # retorna ultimo status

    if handsPoints:    
        ultimosNumeros = detectador(ultimosNumeros[0],ultimosNumeros[1],ultimosNumeros[2],ultimosNumeros[3]) # funcao alimenta ela mesma com ultima leitura

    cv2.imshow("Imagem", img)
    cv2.waitKey(100)


video.release()
cv2.destroyAllWindows()
