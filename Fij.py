import math

"""
Ferramenta de cálculo dos fatores de forma tabelados no formulário de Transferência de Calor. 
"""

# ==========================================
# GEOMETRIAS INFINITAS (Dimensão Z -> inf)
# ==========================================

def planos_paralelos(L, wi, wj):
    if L <= 0:
        raise ValueError("A distância entre os planos deve ser positiva.")
    if wi <= 0 or wj <= 0:
        raise ValueError("O comprimento dos planos deve ser positivo.")
    
    Wi = wi / L
    Wj = wj / L 

    F_planos_paralelos = (math.sqrt((Wi + Wj)**2 + 4) - math.sqrt((Wj - Wi)**2 + 4)) / (2 * Wi)
    return F_planos_paralelos


def planos_inclinados_de_igual_largura(w, alpha):
    if w <= 0:
        raise ValueError("A largura dos planos deve ser positiva.")
    if alpha <= 0 or alpha >= 180:
        raise ValueError("O ângulo de inclinação deve ser entre 0° e 180°.")
    
    alpha_rad = math.radians(alpha)
    F_planos_inclinados = 1 - math.sin(alpha_rad / 2)
    return F_planos_inclinados


def espaco_fechado_triangular(wi, wj, wk):
    if wi <= 0 or wj <= 0 or wk <= 0:
        raise ValueError("O comprimento dos planos deve ser positivo.")
    
    F_espaco_fechado_triangular = (wi + wj - wk) / (2 * wi)
    return F_espaco_fechado_triangular


def planos_perpendiculares_c_aresta_comum(wi, wj):
    if wi <= 0 or wj <= 0:
        raise ValueError("O comprimento dos planos deve ser positivo.")
    
    F_planos_perpendiculares = (1 + (wj / wi) - math.sqrt(1 + (wj / wi)**2)) / 2
    return F_planos_perpendiculares


def cilindros_paralelos_com_R_diferentes(ri, rj, s):
    if ri <= 0 or rj <= 0:
        raise ValueError("O raio dos cilindros deve ser positivo.")
    if s <= 0:
        raise ValueError("A distância s entre os cilindros deve ser positiva.")
    
    R = rj / ri
    S = s / ri
    C = 1 + R + S
    
    # Validação geométrica interna das raízes
    if (C**2 < (R + 1)**2) or (C**2 < (R - 1)**2):
        raise ValueError("Geometria impossível: os cilindros estão se sobrepondo.")

    # Cálculo dos termos da equação longa
    termo_raiz1 = math.sqrt(C**2 - (R + 1)**2)
    termo_raiz2 = math.sqrt(C**2 - (R - 1)**2)
    
    # math.acos já retorna o resultado em radianos
    termo_acos1 = (R - 1) * math.acos((R / C) - (1 / C))
    termo_acos2 = (R + 1) * math.acos((R / C) - (1 / C))
    
    # Isolar Fi-j dividindo toda a expressão do lado direito por 2*pi
    F_cilindros_paralelos = (math.pi + termo_raiz1 - termo_raiz2 + termo_acos1 - termo_acos2) / (2 * math.pi)
    return F_cilindros_paralelos


def cilindro_e_retangulo_paralelo(r, s1, s2, L):
    if r <= 0:
        raise ValueError("O raio do cilindro deve ser positivo.")
    if L <= 0:
        raise ValueError("A distância L entre os planos deve ser positiva.")

    # Removido math.radians(), pois math.atan() já devolve o valor em radianos
    p1 = math.atan(s1 / L)
    p2 = math.atan(s2 / L)

    F_colindro_retangulo = (r / (s1 - s2)) * (p1 - p2)
    return F_colindro_retangulo


def plano_fila_de_cilindros_paralelos(D, S):
    if D <= 0:
        raise ValueError("O diâmetro dos cilindros deve ser positivo.")
    if S <= 0:
        raise ValueError("A distância entre os eixos dos cilindros deve ser positiva.")
    if S < D:
        raise ValueError("A distância entre os eixos (S) não pode ser menor que o diâmetro (D).")
    
    p1 = math.atan(math.sqrt((S**2 - D**2) / D**2))
    F_fila_cilindros = 1 - math.sqrt(1 - (D / S)**2) + (D / S) * p1
    return F_fila_cilindros


# ==========================================
# GEOMETRIAS FINITAS (Tridimensionais)
# ==========================================

def planos_paralelos_alinhados(X, Y, L):
    if X <= 0 or Y <= 0 or L <= 0:
        raise ValueError("Todas as dimensões (X, Y, L) devem ser positivas.")
    
    x_barra = X / L
    y_barra = Y / L

    # Correção dos termos matemáticos conforme a Figura 5.9
    p1 = math.log(((1 + x_barra**2) * (1 + y_barra**2) / (1 + x_barra**2 + y_barra**2))) * 0.5
    p2 = x_barra * math.sqrt(1 + y_barra**2) * math.atan(x_barra / math.sqrt(1 + y_barra**2))
    p3 = y_barra * math.sqrt(1 + x_barra**2) * math.atan(y_barra / math.sqrt(1 + x_barra**2))
    p4 = x_barra * math.atan(x_barra)
    p5 = y_barra * math.atan(y_barra)
    
    F_planos_paralelos_alinhados = (2 / (math.pi * x_barra * y_barra)) * (p1 + p2 + p3 - p4 - p5)
    return F_planos_paralelos_alinhados


def planos_perpendiculares_com_aresta_comum_finitos(X, Y, Z):
    if X <= 0 or Y <= 0 or Z <= 0:
        raise ValueError("Todas as dimensões (X, Y, Z) devem ser positivas.")
    
    H = Z / X
    W = Y / X
    
    termo_tan1 = W * math.atan(1 / W)
    termo_tan2 = H * math.atan(1 / H)
    termo_tan3 = math.sqrt(H**2 + W**2) * math.atan(1 / math.sqrt(H**2 + W**2))

    frac1 = ((1 + W**2) * (1 + H**2)) / (1 + W**2 + H**2)
    frac2 = (W**2 * (1 + W**2 + H**2)) / ((1 + W**2) * (W**2 + H**2))
    frac3 = (H**2 * (1 + W**2 + H**2)) / ((1 + H**2) * (W**2 + H**2))

    termo_log = 0.25 * math.log(frac1 * (frac2**(W**2)) * (frac3**(H**2)))
    
    F_planos_perpendiculares_finitos = (1 / (math.pi * W)) * (termo_tan1 + termo_tan2 - termo_tan3 + termo_log)
    return F_planos_perpendiculares_finitos


def discos_paralelos_coaxiais(ri, rj, L):
    if ri <= 0 or rj <= 0 or L <= 0:
        raise ValueError("Todas as dimensões (ri, rj, L) devem ser positivas.")
    
    Ri = ri / L
    Rj = rj / L 
    S = 1 + (1 + Rj**2) / (Ri**2)

    F_discos_paralelos = 0.5 * (S - math.sqrt(S**2 - 4 * (rj / ri)**2)) 
    return F_discos_paralelos


# ==========================================
# MENUS E INTERFACE DE USUÁRIO
# ==========================================

def menu_infinitos():
    while True:
        print("\n--- [ Dimensão 'Z' infinita ] ---")
        print("1. Planos paralelos infinitos")
        print("2. Planos inclinados de igual largura")
        print("3. Planos perpendiculares com aresta comum infinitos")
        print("4. Cilindros paralelos com raios diferentes infinitos")
        print("5. Cilindro e retângulo paralelos infinitos")
        print("6. Plano e fila de cilindros paralelos infinitos")
        print("0. Voltar")
        opc = input("Escolha uma opção: ")
        if opc == '0': break

        try:
            if opc == '1':
                L = float(input("Distância entre os planos (L): "))
                wi = float(input("Comprimento do plano i (wi): "))
                wj = float(input("Comprimento do plano j (wj): "))
                resultado = planos_paralelos(L, wi, wj)
                print("Fator de forma F_ij: {resultado:.4f}".format(resultado=resultado))
            elif opc == '2':
                w = float(input("Largura dos planos (w): "))
                alpha = float(input("Ângulo de inclinação (alpha em graus): "))
                resultado = planos_inclinados_de_igual_largura(w, alpha)
                print("Fator de forma F_ij: {resultado:.4f}".format(resultado=resultado))
            elif opc == '3':
                wi = float(input("Comprimento do plano i (wi): "))
                wj = float(input("Comprimento do plano j (wj): "))
                resultado = planos_perpendiculares_c_aresta_comum(wi, wj)
                print("Fator de forma F_ij: {resultado:.4f}".format(resultado=resultado))
            elif opc == '4':
                ri = float(input("Raio do cilindro i (ri): "))
                rj = float(input("Raio do cilindro j (rj): "))
                s = float(input("Distância entre as superfícies dos cilindros (s): "))
                resultado = cilindros_paralelos_com_R_diferentes(ri, rj, s)
                print("Fator de forma F_ij: {resultado:.4f}".format(resultado=resultado))
            elif opc == '5':
                r = float(input("Raio do cilindro (r): "))
                s1 = float(input("Distância s1: "))
                s2 = float(input("Distância s2: "))
                L = float(input("Distância vertical L: "))
                resultado = cilindro_e_retangulo_paralelo(r, s1, s2, L)
                print("Fator de forma F_ij: {resultado:.4f}".format(resultado=resultado))
            elif opc == '6':
                D = float(input("Diâmetro dos cilindros (D): "))
                S = float(input("Distância entre eixos (S): "))
                resultado = plano_fila_de_cilindros_paralelos(D, S)
                print("Fator de forma F_ij: {resultado:.4f}".format(resultado=resultado))
        except ValueError as e:
            print("Erro: {e}".format(e=e))
        aguardar()


def menu_finitos():
    while True:
        print("\n--- [ Dimensão 'Z' finita ] ---")
        print("1. Planos paralelos alinhados")
        print("2. Planos perpendiculares com aresta comum finitos")
        print("3. Discos paralelos coaxiais")
        print("0. Voltar")
        opc = input("Escolha uma opção: ")
        if opc == '0': break

        try:
            if opc == '1':
                X = float(input("Largura X do plano: "))
                Y = float(input("Comprimento Y do plano: "))
                L = float(input("Distância de separação L: "))
                resultado = planos_paralelos_alinhados(X, Y, L)
                print("Fator de forma F_ij: {resultado:.4f}".format(resultado=resultado))
            elif opc == '2':
                X = float(input("Dimensão X (comprimento da base): "))
                Y = float(input("Dimensão Y (largura na aresta comum): "))
                Z = float(input("Dimensão Z (altura vertical): "))
                resultado = planos_perpendiculares_com_aresta_comum_finitos(X, Y, Z)
                print("Fator de forma F_ij: {resultado:.4f}".format(resultado=resultado))
            elif opc == '3':
                ri = float(input("Raio do disco i (ri): "))
                rj = float(input("Raio do disco j (rj): "))
                L = float(input("Distância entre os discos (L): "))
                resultado = discos_paralelos_coaxiais(ri, rj, L)
                print("Fator de forma F_ij: {resultado:.4f}".format(resultado=resultado))
        except ValueError as e:
            print("Erro: {e}".format(e=e))
        aguardar()


def aguardar():
    input("\n[Pressione Enter para continuar...]") 


def menu():
    while True:
        print("\n--- CALCULADORA DE FATORES DE FORMA ---")
        print("1. Dimensão 'Z' infinita (2D)")
        print("2. Dimensão 'Z' finita (3D)")
        print("0. Sair")
        opc = input("Escolha uma opção: ")
        if opc == '0': 
            print("Encerrando o programa.")
            break
        elif opc == '1':
            menu_infinitos()
        elif opc == '2':
            menu_finitos()
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()