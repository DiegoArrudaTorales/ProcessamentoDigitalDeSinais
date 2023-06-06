import numpy as np
def naive_DFT(x):
    N = np.size(x)
    X = np.zeros((N,),dtype=np.complex128)
    for m in range(0,N):    
        for n in range(0,N): 
            X[m] += x[n]*np.exp(-np.pi*2j*m*n/N)
    return X

x = np.random.rand(1024,)
# compute DFT
X=naive_DFT(x)
# compute FFT using np's fft function
X2 = np.fft.fft(x)
# now compare DFT with np fft
print('Is DFT close to fft?',np.allclose(X - X2,1e-12))