
import numpy as np
import matplotlib.pyplot as plt


def dft(x):
    Xsize = len(x)
    X = np.zeros(Xsize, dtype=complex)

    for m in range(Xsize):
        mysumm = 0
        for n in range(Xsize):
            mysumm += x[n] * (np.cos(2*np.pi*m*n/Xsize) -
                              1j*np.sin(2*np.pi*m*n/Xsize))
        X[m] = mysumm

    return X


x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)
X = dft(y)

fig, axs = plt.subplots(2)
axs[0].plot(x, y)
axs[0].set_title('Sinal original')
axs[1].plot(np.arange(len(X)), np.abs(X))
axs[1].set_title('Magnitude da Transformada de Fourier')
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
plt.show()



function[X] = dft(x)
Xsize = length(x);

for m=0:Xsize-1
    mysumm = 0;
    for n=0:Xsize-1
        mysumm = mysumm + x(n+1) * (cos(2*pi**m/Xsize)-j*sin(2*pi*n*m/Xsize));
    end
    X(m+1)=mysumm;
end'''
