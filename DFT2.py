import numpy as np
def naive_IDFT(x):
    N = np.size(x)
    X = np.zeros((N,),dtype=np.complex128)
    for m in range(0,N):
        for n in range(0,N): 
            X[m] += x[n]*np.exp(np.pi*2j*m*n/N)
    return X/N
x = np.random.rand(1024,)
# compute FFT
X=np.fft.fft(x)
# compute IDFT using IDFT
x2 = naive_IDFT(X)
# now compare DFT with np fft
print('Is IDFT close to original?',np.allclose(x - x2,1e-12))