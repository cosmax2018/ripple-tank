
# matrici.py libreria sulle matrici

from copy import copy,deepcopy

def deepCopyMatrix(m):	return deepcopy(m)	# copia ma crea due entità distinte

def copyMatrix(m):		return copy(m)		# copia ma crea due entità interdipendenti (se cambio il valore a una cambia anche l'altra)
	
def newArray(n,v=0):
	# crea un nuovo array lungo n e lo inizializza a v
	x = []
	for i in range(n):
		x.append(v)
	return x
			
def printIntArray(arr,f=3):
	# stampa un array di lunghezza n
	# arr : array
	# f   : numero di cifre da visualizzare
	# s   : stringa da mettere in caso il valore sia nullo
	fs = "%"+str(f)+"d"  # the format string..
	for i in range(len(arr)):
		v = arr[i]
		print(fs%v,end=" ")
	print()
	
def newMatrix(n,m,v=0):
	# crea una nuova matrice 2D (n=d[0] x m=d[1]) e la inizializza ai valori v
	# n  : numero di righe
	# m  : numero di colonne
	# v  : valore iniziale degli elementi dela matrice
	# la matrice sara' indirizzabile cosi':  v = mat[x][y]
	mat = []
	for y in range(n):
		row = []
		for x in range(m):
			row.append(v)
		mat.append(row)
	return mat

def newMatrix3D(xn,yn,zn,v=0):
	# crea una nuova matrice 3D (xn=d[0] x yn=d[1] x zn=d[2]) e la inizializza ai valori v
	# xn  : numero di righe
	# yn  : numero di colonne
	# zn  : numero di spessore
	# v  : valore iniziale degli elementi dela matrice
	# la matrice sara' indirizzabile cosi':  v = mat[x][y][z]
	mat3d = []
	for z in range(xn):
		mat3d.append(newMatrix(yn,zn,v))
	return mat3d
	
def resetMatrix(mat,v=0):
	# resetta una matrice 2D (n x m)
	# mat : matrice
	# v   : valore di reset
	for j in range(len(mat)):
		row = mat[j]
		for i in range(len(row)):
			row[i] = v
			
def resetValue(mat,i,j,v=0):
	# resetta una matrice 2D (n x m)
	# mat : matrice
	# j,i : indici
	# v   : valore di reset
	row = mat[j]
	row[i] = v
            
def fillRandom(mat, range_limit, m=0):
    # riempie la matrice 2D (n x m) di valori interi casuali (positivi e negativi) attorno a una media m.
	# mat           : matrice
    # range_limit   : limite al range di valori
	# m             : valore medio
	from random import randint
	for j in range(len(mat)):
		row = mat[j]
		for i in range(len(row)):
			row[i] = randint(m - range_limit, m + range_limit)

def sumRandom(mat, range_limit, m=0):
    # somma alla matrice 2D (n x m) dei valori interi casuali (positivi e negativi) attorno a una media m.
	# mat           : matrice
    # range_limit   : limite al range di valori
	# m             : valore medio
	from random import randint
	for j in range(len(mat)):
		row = mat[j]
		for i in range(len(row)):
			row[i] = row[i] + randint(m - range_limit, m + range_limit)
            
def swapMatrix(mat_a,mat_b):
	# scambia i valori delle matrici
	for j in range(len(mat_a)):
		row_a = mat_a[j]
		row_b = mat_b[j]
		for i in range(len(row_a)):
			row_a[i],row_b[i] = row_b[i],row_a[i]

def sumMatrix(mat_a,mat_b):
	# somma le matrici mat_a, mat_b della stessa dimensione
	if len(mat_a) != len(mat_b): 
		return [] # errore: colonne di dimensione diversa!
	mat_C = []
	for y in range(len(mat_a)):
		row_a = mat_a[y]
		row_b = mat_b[y]
		row_c = []
		if len(row_a) != len(row_b):
			return [] # errore:righe di dimensione diversa!
		for x in range(len(row_a)):
			row_c.append(row_a[x]+row_b[x])
		mat_C.append(row_c)
	return mat_C
	
def printIntMatrix(mat,f=1):
	# stampa una matrice 2D (n x m)
	# mat : matrice
	# f   : numero di cifre da visualizzare
	fs = "%0"+str(f)+"i"  # the format string..
	print()
	for y in range(len(mat)):
		row = mat[y]
		for x in range(len(row)):
			v = row[x]
			print(fs%v,end=' ')
		print()

def printStrMatrix(mat,f=3,s='   '):
	# stampa una matrice 2D (n x m)
	# mat : matrice
	# f   : numero di caratteri da visualizzare
	# s   : stringa da mettere in caso il valore sia nullo
	fs = "%"+str(f)+"s"  # the format string..
	for y in range(len(mat)):
		row = mat[y]
		for x in range(len(row)):
			v = row[x]
			if v != 0:
				print(fs%v,end=" ")
			else:
				print(s,end=" ")
		print("",end="")
	print()

def findValue(mat,v):
	# ritorna le coordinate (x,y) del valore v.
	if v != None:
		for y in range(len(mat)):
			row = mat[y]
			for x in range(len(row)):
				if v == row[x]:
					return (x,y)
	return (None,None)
	
def getMaximum(mat):
	# ritorna il valore massimo e le sue coordinate (x,y).
	maximum = 0
	for y in range(len(mat)):
		row = mat[y]
		for x in range(len(row)):
			v = row[x]
			if v > maximum:
				maximum = v
				coordinates = (x,y)
	return maximum,coordinates

def getMaximumValue(mat):    
	# ritorna il valore massimo.
	return max([valore for row in mat for valore in row])
    
def getMedia(mat,dim):
	# ritorna il valore medio intero.
	return int(sum([valore for row in mat for valore in row])/dim)
    
def matrixProduct(A, X):
    # Funzione per calcolare il prodotto di due matrici
    # Otteniamo le dimensioni delle matrici
    n = len(A)         # Numero di righe di A
    m = len(A[0])      # Numero di colonne di A (e numero di righe di X)
    p = len(X[0])      # Numero di colonne di X

    # Verifica che il numero di colonne di A sia uguale al numero di righe di X
    if m != len(X):
        raise ValueError("Il numero di colonne di A deve essere uguale al numero di righe di X per eseguire il prodotto.")

    # Inizializziamo la matrice risultato C con zeri (di dimensione n x p)
    C = [[0 for _ in range(p)] for _ in range(n)]

    # Calcoliamo il prodotto
    for i in range(n):
        for j in range(p):
            # Calcoliamo ogni elemento c_ij come somma dei prodotti degli elementi di riga e colonna
            for k in range(m):
                C[i][j] += A[i][k] * X[k][j]

    return C
    
def matrixSum(matrix):
    # Funzione per calcolare la somma di tutti gli elementi di una matrice
    S = 0
    for row in matrix:
        for element in row:
            S += element
    return S
    
def findMatrix_X(A, C):
    # prendiamo in considerazione il prodotto matriciale C = AX
    # Questa e' la funzione per trovare la matrice delle incognite X date A e C
    # Calcolo della pseudo-inversa di A
    import numpy as np
    A_pseudo_inverse = np.linalg.pinv(A)
    
    # Calcolo della matrice X usando la pseudo-inversa
    X = np.dot(A_pseudo_inverse, C)
    return X
    
def solve_via_qr(A, C):
    # Funzione per risolvere A * X = C usando la decomposizione QR
    import numpy as np
    # Decomposizione QR:
    Q, R = np.linalg.qr(A)
    
    # Calcolo X risolvendo R * X = Q^T * C
    X = np.dot(np.linalg.inv(R), np.dot(Q.T, C))
    return X
    
def pseudoInverse(A,C):
    # Calcolo della pseudo-inversa di A per trovare X
    import numpy as np
    A_pseudo_inverse = np.linalg.pinv(A)

    # Calcolo della matrice X
    X = np.dot(A_pseudo_inverse, C)

    # print("Matrice delle incognite X (5x3):\n", X)

    # Verifica del risultato
    # Se il residuo è molto vicino a zero, significa che X
    # è una buona approssimazione della soluzione.
    residuo = np.dot(A, X) - C
    # print("\nResiduo (A * X - C):\n", residuo)    
    return X,residuo