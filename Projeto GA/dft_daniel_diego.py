#Alunos Daniel Klauck e Diego Arruda
import numpy as np
import matplotlib.pyplot as plt

def dft(x):
    
    Xsize = len(x)#eixo Xsize tem o tamanho do vetor de dados x

    X = np.zeros(Xsize, dtype=complex) #cria um array de zeros com o tipo de dados complexos
    
    for m in range(Xsize): #percorre os valores de m de 0 a Xsize-1

        mysumm = 0 #para cada valor de m, a soma deve ser reinicializada

        for n in range(Xsize):
                        
            # calcula a parte real da DFT
            re = np.cos(2 * np.pi * m * n / Xsize)

            # calcula a parte imaginária da DFT
            im = -1j * np.sin(2 * np.pi * m * n / Xsize)
            
            # soma o termo real e imaginário
            mysumm += x[n] * (re + im)

        X[m] = mysumm

    return X

x = np.linspace(0, 2*np.pi, 100) #x é o numero de amostras# retorna numeros uniformemente espaçados
y = np.sin(x) #calcula y para plotar no gráfico
X = dft(y)

fig, axs = plt.subplots(3, 1, figsize=(8, 8))

axs[0].plot(x, y)
axs[0].set_xlabel('Tempo')
axs[0].set_ylabel('Amplitude')
axs[0].set_title('Sinal original')

axs[1].plot(np.arange(len(X)), np.abs(X))
axs[1].set_xlabel('Frequência')
axs[1].set_ylabel('Magnitude')
axs[1].set_title('Magnitude da Transformada de Fourier')

axs[2].plot(np.arange(len(X)), np.angle(X))
axs[2].set_xlabel('Frequência')
axs[2].set_ylabel('Ângulo (radianos)')
axs[2].set_title('Fase')

plt.show()

'''
# Exemplo de uso
x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
X = dft(x)

# plot do resultado
plt.figure()
plt.subplot(2,1,1)
plt.plot(np.abs(X))
plt.title('Magnitude')
plt.xlabel('Frequência')
plt.ylabel('Amplitude')

plt.subplot(2,1,2)
plt.plot(np.angle(X))
plt.title('Fase')
plt.xlabel('Frequência')
plt.ylabel('Ângulo (radianos)')
plt.show()'''


'''
function[X] = dft(x)
Xsize = length(x);

for m=0:Xsize-1
    mysumm = 0;
    for n=0:Xsize-1
        mysumm = mysumm + x(n+1) * (cos(2*pi**m/Xsize)-j*sin(2*pi*n*m/Xsize));
    end
    X(m+1)=mysumm;
end'''
