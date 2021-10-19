import numpy as np

#ax + by = g
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
#inverse mod
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
 
def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def Deternminant(m):
    #2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]
    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*Deternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m, mod = 26):
    determinant = modinv(Deternminant(m) % mod, mod)
    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * Deternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = np.array(cofactors)
    cofactors = cofactors*determinant%26
    return cofactors.transpose()

if __name__ == '__main__':
    key_mat = [[17, 17, 5], [21, 18, 21],[ 2, 2, 19]] 
    #input code
    code = input()
    t = len(code)//3 
    code = np.array([ord(i) - ord('a') for i in code])
    code = code.reshape((t,3))
    poh = [[] for i in range(t)]
    #encription
    for i in range(t):
        m = key_mat*code[i]
        for r in m:
            poh[i].append(sum(r) %26)

    #render ciphertext
    ciphertext = ''
    for i in range(t):
        ct = map(chr, [i+ord('a') for i in poh[i]])
        ciphertext += ''.join(ct)
    print('ciphertext:', ciphertext)

    #decription
    inv_mat = getMatrixInverse(key_mat)
    poh = np.array(poh)
    ans = []
    for i in range(t):
        m = inv_mat*poh[i]
        for r in m:
            ans.append(sum(r)%26)


    ans = map(chr, [i+ord('a') for i in ans])
    ans = ''.join(ans)
    print(ans)
            
