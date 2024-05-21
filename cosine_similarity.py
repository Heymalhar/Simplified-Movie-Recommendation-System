# Separate code file for cosine similarity to better understand the concept

import math

def cosine_similarity(A, B):

    l1 = len(A)
    l2 = len(B)

    if l1 != l2:
        print("The cosine similarity of two unequal vectors cannot be calculated. Please make sure that only two equal vectors are entered.")

    C = [0]*l1

    for i in range(l1):
        C[i] = A[i]*B[i]

    count = sum(C)

    s1 = sum(x*x for x in A)
    s2 = sum(x*x for x in B)

    num1 = math.sqrt(s1) * math.sqrt(s2)

    cs = count/num1

    return cs

if __name__ == "__main__":
    vector1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    vector2 = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    cs = cosine_similarity(vector1, vector2)
    print("The cosine similarity of vector1 and vector2 is: ", cs)