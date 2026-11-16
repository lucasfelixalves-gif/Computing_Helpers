

def bonfim_barreiros(row, col, p):
    L, a1, b1, a2, b2, beta, alfa, a, b =( p["L"], p["a1"], p["b1"], p["a2"], p["b2"], p["beta"], p["alfa"], p["a"], p["b"]) 
    
    # row 1
    if row == 1 and col == 1:
        return (2*a1*b1+2*a2*b2+a2*b1+a1*b2) * L / 6
    elif row ==1 and col == 2:
        return ((1+beta)*a1 + (1+alfa)*a2) * L / 6
     #row 2
    elif row ==2 and col ==1:
        return a * L * ( (1+beta)*b1 + (1+alfa)*b2) / 6
    elif row ==2 and col ==2:
        return a * b* L /3
    #row 3
    elif row == 3 and col == 1:
        return a* L * (b1+b2)/3
    elif row == 3 and col == 2:
        return a * b * L * (1+ alfa*beta) / 3
    #row 4
    elif row == 4  and col == 1:
        return a * L * (b1 + 3* b2) /12
    elif row ==4 and col ==2:
        return a * b * L * ( 1 + alfa + alfa*alfa) / 12
    #row 5
    elif row == 5 and col ==1:
        return a * L *(3*b1 + 5*b2) /12
    elif row ==5 and col ==2:
        return a * b * L * (5 - beta - beta*beta) / 12
    #combinacao nao definida
    else:
        print("a combinacao de row e col nao esta na tabela")
        return None


   
print("=======================================")
print("   METODO DE BONFIM–BARREIROS          ")
print("=======================================\n")
row = int(input("linha pretendida: "))
col = int(input("coluna pretendida: "))
L = float(input("comprimento da seccao: "))
# definir p - dicionario
p = {"L": L}


#pede os parametros utilizados em determinado combinacao
if row == 1 and col == 1:
    print("Trap-row: a1 e a2; trap-col: b1 e b2")
    p["a1"] = float(input("a1: "))
    p["a2"] = float(input("a2: "))
    p["b1"] = float(input("b1: "))
    p["b2"] = float(input("b2: "))

elif row == 1 and col == 2:
    print("Trap-row: a1, a2; trig-col: b, alfa, beta")
    p["a1"] = float(input("a1: "))
    p["a2"] = float(input("a2: "))
    p["b"] = float(input("b: "))
    p["alfa"] = float(input("alfa: "))
    p["beta"] = float(input("beta: "))

elif row == 2 and col == 1:
    print("Trig-row: a, alfa, beta; trap-col: b1, b2")
    p["a"] = float(input("a: "))
    p["alfa"] = float(input("alfa: "))
    p["beta"] = float(input("beta: "))
    p["b1"] = float(input("b1: "))
    p["b2"] = float(input("b2: "))

elif row == 2 and col == 2:
    print("Trig-row: a; trig-col: b")
    p["a"] = float(input("a: "))
    p["b"] = float(input("b: "))

elif row == 3 and col == 1:
    print("Parab.simetrica-row: a; trap-col: b1, b2")
    p["a"] = float(input("a: "))
    p["b1"] = float(input("b1: "))
    p["b2"] = float(input("b2: "))

elif row == 3 and col == 2:
    print("Parab.simetrica-row: a; trig-col: b, alfa, beta")
    p["a"] = float(input("a: "))
    p["b"] = float(input("b: "))
    p["alfa"] = float(input("alfa: "))
    p["beta"] = float(input("beta: "))

elif row == 4 and col == 1:
    print("Parab.negativa-row: a; trap-col: b1, b2")
    p["a"] = float(input("a: "))
    p["b1"] = float(input("b1: "))
    p["b2"] = float(input("b2: "))

elif row == 4 and col == 2:
    print("Parab.negativa-row: a; trig-col: b, alfa")
    p["a"] = float(input("a: "))
    p["b"] = float(input("b: "))
    p["alfa"] = float(input("alfa: "))

elif row == 5 and col == 1:
    print("Parab-row: a; trap-col: b1, b2")
    p["a"] = float(input("a: "))
    p["b1"] = float(input("b1: "))
    p["b2"] = float(input("b2: "))

elif row == 5 and col == 2:
    print("Parab-row: a; trig-col: b, beta")
    p["a"] = float(input("a: "))
    p["b"] = float(input("b: "))
    p["beta"] = float(input("beta: "))

else:
    print("combinacao não implementada")   #para impedir macacos de escolher uma combinacao que nao esta na tablea
    quit()


#para eveitar o erri "KeyError"
for k in ["a1","a2","b1","b2","a","b","alfa","beta"]: 
    if k not in p:
        p[k] = 0.0


MrowMcol = bonfim_barreiros(row,col,p)

print(f"\nO resultado do integral M*M dL é: {MrowMcol:.6g}")
