from hypothesis import given, strategies as st

def partition(a,v):
    """partitionne a en 3 (premiere partie: > v, deuxieme partie =v, troisieme partie > v)
    et renvoie (i,j) tq:
    si j=i:
        aucune occurence de v
        si =len(a): toutes plus petites
        si =0: toutes plus grandes
    si i<j:
        a[i] premiere occurence de v, a[j-1] derniere occurence v"""
    i=0 #avant i les valeurs sont plus petites
    j=0 #entre i et j, valent v, entre j et k inconnues
    l=len(a)-1
    k=l #au-dela de k, les valeurs sont plus grandes
    
    while j<=k: #tant qu'on n'a pas tout vu
        if a[j]<v:
            if i==j:
                i+=1
                j+=1
            else:
                stock=a[i]
                a[i]=a[j]
                a[j]=stock
                i+=1
                j+=1
        elif a[j]==v:
            j+=1
        else:
            stock=a[k]
            a[k]=a[j]
            a[j]=stock
            k-=1
    return (i,j)
    

def sorting(a):
    l=len(a)
    if l>1:
        r=a[0]
        (i,j)=partition(a,r)
        b=[0 for i in range (len(a))]
        b[0:i]=sorting(a[0:i])
        for k in range(i,j):
            b[k]=r
        b[j:l]=sorting(a[j:l])
    else:
        return a
    return b

#one test just to check out a basic situation    
def test_oneexample():
    a=[8,2,4,1,1,9,2,3,7]
    assert partition(a,3)==(4,5)
    
#test if v has no occurence in a
def test_noV():
    a=[4,2,9,1,8,3]
    assert partition(a,6) == (4,4)

#test on le function partition(a,v)
@given(st.lists(st.integers()),st.integers())
def test_random_part(a,v):
    s=sorted(a)
    i=0
    while i<len(a) and s[i]<v:
        i+=1
    j=i
    while j<len(a) and s[j] <= v:
        j+=1
    assert (i,j)==partition(a,v)

#test on the function sorting(a)
@given(st.lists(st.integers()))
def test_random_sort(a):
    assert sorting(a)==sorted(a)