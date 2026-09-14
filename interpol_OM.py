import math

# ==========================================
# Memoria Global para armazenar inputs
# ==========================================
MEMORIA = {}

def pedir_valor(mensagem, chave):
    """Pede um numero. Se existir na memoria, mostra em [ ] e assume com Enter."""
    while True:
        msg_limpa = mensagem.replace(":", "").strip()
        if chave in MEMORIA:
            prompt = "{msg} [{val}]: ".format(msg=msg_limpa, val=MEMORIA[chave])
        else:
            prompt = "{msg}: ".format(msg=msg_limpa)
            
        entrada = input(prompt).strip()
        
        if entrada == "":
            if chave in MEMORIA:
                return MEMORIA[chave]
            else:
                print("Valor obrigatorio.")
                continue
        try:
            valor = float(entrada)
            MEMORIA[chave] = valor
            return valor
        except ValueError:
            print("Erro: Digite um numero.")

def pedir_texto(mensagem, chave):
    """Igual ao pedir_valor, mas para strings (texto)."""
    while True:
        msg_limpa = mensagem.replace(":", "").strip()
        if chave in MEMORIA:
            prompt = "{msg} [{val}]: ".format(msg=msg_limpa, val=MEMORIA[chave])
        else:
            prompt = "{msg}: ".format(msg=msg_limpa)
            
        entrada = input(prompt).strip()
        
        if entrada == "":
            if chave in MEMORIA:
                return MEMORIA[chave]
            else:
                print("Valor obrigatorio.")
                continue
        MEMORIA[chave] = entrada
        return entrada

# ==========================================
# 1. Dados - Chumaceiras Radiais
# ==========================================
tabelas_chumaceira = {
    0.166: {
        "epsilon": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95],
        "S_mod":   [0.99, 0.461, 0.272, 0.17, 0.106, 0.0625, 0.033, 0.0139, 0.00331, 0.000812],
        "phi":     [83, 75, 68, 61, 54, 47, 39, 31, 21, 15],
        "f_mod":   [18.75, 8.514, 4.98, 3.14, 2.016, 1.25, 0.722, 0.355, 0.114, 0.038],
        "Ca_adim": [18.94, 18.47, 18.31, 18.50, 19.02, 20.02, 21.89, 25.55, 34.58, 47.79]
    },
    0.25: {
        "epsilon": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95],
        "S":       [16.2, 7.57, 4.49, 2.83, 1.78, 1.07, 0.58, 0.263, 0.0728, 0.0221],
        "phi":     [82.5, 75.5, 68.5, 61.5, 54, 47, 39.5, 31.5, 21.5, 15.5],
        "R_c_fa":  [307, 140, 82.5, 52.67, 34.26, 21.85, 13.19, 6.97, 2.70, 1.20],
        "Q_adim":  [0.0983, 0.196, 0.295, 0.393, 0.491, 0.590, 0.688, 0.787, 0.885, 0.933],
        "Ca_adim": [18.95, 18.49, 18.37, 18.61, 19.24, 20.42, 22.74, 26.50, 37.09, 54.30]
    },
    0.5: {
        "epsilon": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95],
        "S":       [4.32, 2.03, 1.21, 0.784, 0.508, 0.318, 0.184, 0.0912, 0.0309, 0.0116],
        "phi":     [82, 75, 68.5, 61.53, 55, 48, 41, 33, 23.5, 17],
        "R_c_fa":  [82.10, 37.71, 22.55, 14.75, 9.94, 6.67, 4.33, 2.59, 1.27, 0.70],
        "Q_adim":  [0.0938, 0.187, 0.281, 0.374, 0.468, 0.562, 0.657, 0.751, 0.845, 0.890],
        "Ca_adim": [19, 18.57, 18.64, 18.81, 19.57, 20.97, 23.53, 28.40, 41.10, 60.34]
    },
    1.0: {
        "epsilon": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95],
        "S":       [1.33, 0.631, 0.388, 0.260, 0.178, 0.120, 0.0776, 0.0443, 0.0185, 0.00831],
        "phi":     [79.5, 74.0, 68.0, 62.5, 56.5, 50.5, 44.0, 36.0, 26.0, 19.0],
        "R_c_fa":  [25.36, 11.87, 7.35, 5.07, 3.67, 2.70, 1.99, 1.40, 0.859, 0.563],
        "Q_adim":  [0.0801, 0.159, 0.237, 0.314, 0.390, 0.466, 0.542, 0.616, 0.688, 0.721],
        "Ca_adim": [19.06, 18.81, 18.94, 19.50, 20.62, 22.50, 25.64, 31.60, 46.43, 67.75]
    },
    2.0: {
        "epsilon": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95],
        "S":       [0.559, 0.271, 0.173, 0.122, 0.0893, 0.0654, 0.0463, 0.0297, 0.0143, 0.00707],
        "phi":     [75, 71, 67, 62.5, 58, 52.5, 46.5, 39, 29, 21],
        "R_c_fa":  [10.76, 5.21, 3.40, 2.50, 1.96, 1.60, 1.31, 1.04, 0.730, 0.517],
        "Q_adim":  [0.0537, 0.104, 0.153, 0.199, 0.243, 0.285, 0.329, 0.369, 0.406, 0.422],
        "Ca_adim": [19.25, 19.22, 19.65, 20.49, 21.95, 24.46, 28.29, 35.01, 51.05, 73.12]
    },
    4.0: {
        "epsilon": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95],
        "S":       [0.247, 0.123, 0.0823, 0.0628, 0.0483, 0.0389, 0.0297, 0.0211, 0.0114, 0.00605],
        "phi":     [69, 67, 64, 62, 58, 54, 49, 42, 32, 23],
        "R_c_fa":  [5.02, 2.61, 1.84, 1.47, 1.25, 1.10, 0.98, 0.852, 0.658, 0.494],
        "Ca_adim": [19.54, 19.85, 20.68, 22.03, 24.03, 26.89, 31.39, 38.80, 55.42, 78.42]
    }
}

# ==========================================
# 2. Dados - Teoria de Cheng
# ==========================================
DADOS_CHENG = {
    "1": {"nome": "Esferas", "C_int": 8.65e-4, "C_ext": 9.43e-4, "sigma": 0.178},
    "2": {"nome": "Rolos cil/esf", "C_int": 8.37e-4, "C_ext": 8.99e-4, "sigma": 0.356},
    "3": {"nome": "Conicos/agulhas", "C_int": 8.01e-4, "C_ext": 8.48e-4, "sigma": 0.229}
}

def interpolar(x, list_x, list_y):
    for i in range(len(list_x) - 1):
        x0, x1 = list_x[i], list_x[i+1]
        if (x0 <= x <= x1) or (x1 <= x <= x0):
            y0, y1 = list_y[i], list_y[i+1]
            if x0 == x1: return y0
            return y0 + (y1 - y0) * ((x - x0) / (x1 - x0))
    distancias = [abs(x - val) for val in list_x]
    idx_mais_proximo = distancias.index(min(distancias))
    return list_y[idx_mais_proximo]

def aguardar():
    input("\n[Enter p/ continuar]")

# ==========================================
# Modulo 1: Chumaceiras Radiais
# ==========================================
def menu_variavel(ld_val, tabela_dados):
    chaves = list(tabela_dados.keys())
    while True:
        print("\n--- L/D = {v} ---".format(v=ld_val))
        print("Variaveis conhecidas:")
        for i in range(len(chaves)):
            print("{idx}. {nome}".format(idx=i+1, nome=chaves[i]))
            
        opc = input("Opcao (0 volta): ")
        if opc == "0" or opc == "": break
        
        try:
            idx = int(opc) - 1
            if 0 <= idx < len(chaves):
                var_conhecida = chaves[idx]
                chave_mem = "chum_" + var_conhecida
                val = pedir_valor("Valor de " + var_conhecida, chave_mem)
                
                print("\n>> RESULTADOS PARA {k} = {v}".format(k=var_conhecida, v=val))
                lista_x = tabela_dados[var_conhecida]
                
                for var_alvo in chaves:
                    if var_alvo == var_conhecida: continue
                    lista_y = tabela_dados[var_alvo]
                    resultado = interpolar(val, lista_x, lista_y)
                    print("{k}: {r:.4f}".format(k=var_alvo, r=resultado))
                aguardar()
            else:
                print("Opcao invalida.")
        except ValueError:
            print("Erro: Introduza um numero.")
            aguardar()

def menu_chumaceiras():
    ld_opcoes = {
        "1": ("1/6 (0.166)", 0.166), "2": ("1/4 (0.25)", 0.25),
        "3": ("1/2 (0.5)", 0.5), "4": ("1.0", 1.0),
        "5": ("2.0", 2.0), "6": ("4.0 (Infinito)", 4.0)
    }
    
    while True:
        print("\n-- CHUMACEIRAS RADIAIS --")
        for k in sorted(ld_opcoes.keys()):
            print("{k}. L/D = {nome}".format(k=k, nome=ld_opcoes[k][0]))
        print("0. Sair")
        
        opc = input("Escolha a proporcao: ")
        if opc == "0" or opc == "": break
        elif opc in ld_opcoes:
            ld_val = ld_opcoes[opc][1]
            menu_variavel(ld_val, tabelas_chumaceira[ld_val])
        else: print("Opcao invalida.")

# ==========================================
# Modulo 2.1: Teoria de Cheng - Rolamentos
# ==========================================
def menu_cheng_rolamentos():
    while True:
        print("\n--- CHENG: ROLAMENTOS ---")
        print("1. Esferas")
        print("2. Rolos cil. ou esfericos")
        print("3. Conicos ou agulhas")
        opc_tipo = input("Tipo (0 volta): ")
        if opc_tipo == "0" or opc_tipo == "": break
            
        if opc_tipo in DADOS_CHENG:
            tipo = DADOS_CHENG[opc_tipo]
            print("\nQual o anel movel?")
            print("1. Interior\n2. Exterior")
            opc_anel = input("Anel (0 cancela): ")
            
            if opc_anel == "1": C = tipo["C_int"]
            elif opc_anel == "2": C = tipo["C_ext"]
            elif opc_anel == "0": continue
            else: continue
                
            sigma = tipo["sigma"]
            
            print("\n[Variaveis Base]")
            D = pedir_valor("Diametro D (m)", "rol_D")
            N = pedir_valor("Rotacao N (rpm)", "rol_N")

            print("\nO que deseja calcular?")
            print("1. h e Lambda (Prob. Direto)")
            print("2. LP (Prob. Inverso)")
            opc_prob = input("Opcao: ")
            
            if opc_prob == "1":
                LP = pedir_valor("Param. lubrif. LP (s)", "rol_LP")
                h = C * D * ((LP * N) ** 0.74)
                Lambda = h / sigma
                print("\n>> RESULTADOS (Direto):")
                print("C = {0:.4e} | sigma = {1:.3f}".format(C, sigma))
                print("h = {0:.4f} um".format(h))
                print("Lambda = {0:.4f}".format(Lambda))
                aguardar()
            elif opc_prob == "2":
                Lambda = 1.5
                h = Lambda * sigma
                base = h / (C * D)
                LP = (1.0 / N) * (base ** (1.0/0.74))
                print("\n>> RESULTADOS (Inverso):")
                print("C = {0:.4e} | sigma = {1:.3f}".format(C, sigma))
                print("Assumindo Lambda = 1.5")
                print("h calculado = {0:.4f} um".format(h))
                print("LP = {0:.4f} s".format(LP))
                print("Para uma temperatura de, geralmente, 60C")
                aguardar()

# ==========================================
# Modulo 2.2: Teoria de Cheng - Cames
# ==========================================
def menu_cheng_came():
    while True:
        print("\n--- CHENG: CAME-IMPULSOR ---")
        opc = input("Pressione Enter para sair ou '1' para iniciar: ")
        if opc != "1": break
        
        print("\n[Geometria e Cinematica]")
        rn = pedir_valor("Raio came rn (m)", "came_rn")
        rf = pedir_valor("Raio imp. rf (m, 0 p/ plano)", "came_rf")
        l  = pedir_valor("Dist. l (m)", "came_l")
        N  = pedir_valor("Rotacao N (rpm)", "came_N")
        sigma = pedir_valor("Rugosidade sigma (um)", "came_sigma")
        esc = pedir_texto("Tem escorregamento? (s/n)", "came_esc").lower()
        
        fn = abs(2.0 * rn - l) if esc == 's' else 2.0 * l
        R = rn if rf == 0 else 1.0 / (1.0/rn + 1.0/rf)
            
        print("\nO que deseja calcular?")
        print("1. h e Lambda (Prob. Direto)")
        print("2. LP (Prob. Inverso)")
        opc_prob = input("Opcao: ")
        
        if opc_prob == "1":
            LP = pedir_valor("Param. LP (s)", "came_LP")
            h = 4.35e-3 * ((fn * LP * N) ** 0.74) * (R ** 0.26)
            Lambda = h / sigma
            print("\n>> RESULTADOS (Direto):")
            print("fn = {0:.4f} m | R = {1:.4f} m".format(fn, R))
            print("h = {0:.4f} um".format(h))
            print("Lambda = {0:.4f}".format(Lambda))
            aguardar()
        elif opc_prob == "2":
            if "came_lambda" not in MEMORIA: MEMORIA["came_lambda"] = 1.0
            Lambda = pedir_valor("Lambda", "came_lambda")
            
            h = Lambda * sigma
            base = h / (4.35e-3 * (R ** 0.26))
            LP = (1.0 / (fn * N)) * (base ** (1.0/0.74))
            
            print("\n>> RESULTADOS (Inverso):")
            print("fn = {0:.4f} m | R = {1:.4f} m".format(fn, R))
            print("h calculado = {0:.4f} um".format(h))
            print("LP = {0:.4f} s".format(LP))
            print("Para uma temperatura de, geralmente, 60C")
            aguardar()

# ==========================================
# Modulo 2.3: Teoria de Cheng - Engrenagens
# ==========================================
def obter_sigma_engrenagem():
    print("\nAcabamento:")
    print("1. Fresadas")
    print("2. Shaved")
    print("3. Retificadas (suave) [0.89]")
    print("4. Retificadas (forte) [0.51]")
    print("5. Polidas [0.18]")
    opc = input("Opcao: ")
    
    if opc == "1":
        rod = pedir_texto("Apos rodagem? (s/n)", "engr_rodagem").lower()
        return 1.02 if rod == 's' else 1.78
    elif opc == "2":
        rod = pedir_texto("Apos rodagem? (s/n)", "engr_rodagem").lower()
        return 1.02 if rod == 's' else 1.27
    elif opc == "3": return 0.89
    elif opc == "4": return 0.51
    elif opc == "5": return 0.18
    return 1.0

def menu_cheng_engrenagens():
    while True:
        print("\n--- CHENG: ENGRENAGENS ---")
        opc_tipo = input("Pressione Enter para sair ou '1' para iniciar: ")
        if opc_tipo != "1": break
        
        print("\n[1] Constante Elastica E")
        E1_gpa = pedir_valor("E1 (GPa)", "engr_E1")
        v1 = pedir_valor("Poisson v1", "engr_v1")
        E2_gpa = pedir_valor("E2 (GPa)", "engr_E2")
        v2 = pedir_valor("Poisson v2", "engr_v2")
        
        # Multiplicar por 10^9 para converter para Pa
        E1 = E1_gpa * 1e9
        E2 = E2_gpa * 1e9
        E = 2.0 / ((1.0 - v1**2)/E1 + (1.0 - v2**2)/E2)
        
        sigma = obter_sigma_engrenagem()
        
        print("\n[2] Tipo de Engrenagem")
        print("1. Paralelos externos")
        print("2. Paralelos internos")
        print("3. Conicas (Sigma=90)")
        print("4. Conicas (Sigma!=90)")
        print("5. Sol-Planeta")
        print("6. Anel-Planeta")
        tipo = input("Tipo: ")
        
        if tipo in ['1', '2']:
            u = pedir_valor("Relacao u", "engr_u")
            a = pedir_valor("Dist. eixos a (m)", "engr_a")
            alfa = math.radians(pedir_valor("Alfa (graus)", "engr_alfa"))
            beta = math.radians(pedir_valor("Beta (graus, 0 se reto)", "engr_beta"))
            b = pedir_valor("Largura b (m)", "engr_b")
            
            if tipo == '1':
                n2 = pedir_valor("Rotacao n2 (rpm)", "engr_n2")
                T2 = pedir_valor("Binario T2 (Nm)", "engr_T2")
                N_rpm = n2
                G = (3.4e-4 * (u*a*math.sin(alfa))**1.5 * E**0.148) / ((u+1)**2)
                Wtl = (T2*(u+1)) / (u*a*b*math.cos(alfa)*(math.cos(beta)**2))
                V = (2*math.pi*u*a*n2) / (60*(u+1))
            else:
                na = pedir_valor("Rotacao na (rpm)", "engr_na")
                Ta = pedir_valor("Binario Ta (Nm)", "engr_Ta")
                N_rpm = na
                G = (3.4e-4 * (u*a*math.sin(alfa))**1.5 * E**0.148) / ((u-1)**2)
                Wtl = (Ta*(u-1)) / (u*a*b*math.cos(alfa)*(math.cos(beta)**2))
                V = (2*math.pi*u*a*na) / (60*(u-1))
                
        elif tipo in ['3', '4']:
            u = pedir_valor("Relacao u", "engr_u")
            alfa = math.radians(pedir_valor("Alfa (graus)", "engr_alfa"))
            beta_m = math.radians(pedir_valor("Beta_m (graus, 0 se zerol)", "engr_betam"))
            rm2 = pedir_valor("Raio rm2 (m)", "engr_rm2")
            b = pedir_valor("Largura b (m)", "engr_b")
            n2 = pedir_valor("Rotacao n2 (rpm)", "engr_n2")
            T2 = pedir_valor("Binario T2 (Nm)", "engr_T2")
            
            N_rpm = n2
            Wtl = T2 / (rm2*b*math.cos(alfa)*(math.cos(beta_m)**2))
            V = (2*math.pi*rm2*n2) / 60
            
            if tipo == '3':
                G = (3.4e-4 * (rm2*math.sin(alfa))**1.5 * E**0.148) / ((u**2 + 1)**0.25)
            else:
                g1 = math.radians(pedir_valor("Gamma 1 (graus)", "engr_g1"))
                g2 = math.radians(pedir_valor("Gamma 2 (graus)", "engr_g2"))
                G = (3.4e-4 * (rm2*math.sin(alfa))**1.5 * E**0.148) / ((math.cos(g2) + u*math.cos(g1))**0.5)
                
        elif tipo in ['5', '6']:
            rs = pedir_valor("Raio sol rs (m)", "engr_rs")
            ra = pedir_valor("Raio anel ra (m)", "engr_ra")
            alfa = math.radians(pedir_valor("Alfa (graus)", "engr_alfa"))
            beta = math.radians(pedir_valor("Beta (graus)", "engr_beta"))
            b = pedir_valor("Largura b (m)", "engr_b")
            nc = pedir_valor("Rotacao braco nc (rpm)", "engr_nc")
            np = pedir_valor("Num. planetas np", "engr_np")
            
            if tipo == '5':
                ns = pedir_valor("Rotacao sol ns (rpm)", "engr_ns")
                Ts = pedir_valor("Binario sol Ts (Nm)", "engr_Ts")
                N_rpm = abs(ns - nc)
                G = ((rs*math.sin(alfa))**1.5 * E**0.148 / 3.4e4) * (((ra-rs)/(ra+rs))**0.5)
                Wtl = Ts / (np*rs*b*math.cos(alfa)*(math.cos(beta)**2))
                V = (2*math.pi*rs*abs(ns - nc)) / 60
            else:
                na = pedir_valor("Rotacao anel na (rpm)", "engr_na")
                Ta = pedir_valor("Binario anel Ta (Nm)", "engr_Ta")
                N_rpm = abs(na - nc)
                G = ((ra*math.sin(alfa))**1.5 * E**0.148 / 3.4e4) * (((ra-rs)/(ra+rs))**0.5)
                Wtl = Ta / (np*ra*b*math.cos(alfa)*(math.cos(beta)**2))
                V = (2*math.pi*ra*abs(na - nc)) / 60
        else:
            print("Tipo invalido.")
            continue
        
        print("\n[3] Calcular o que?")
        print("1. h e Lambda (Prob. Direto)")
        print("2. LP e Lambda 5% (Prob. Inverso)")
        opc_prob = input("Opcao: ")
        
        if opc_prob == "1":
            LP = pedir_valor("Param. LP (s)", "engr_LP")
            h = ((G * LP * N_rpm * (Wtl**-0.148)) ** 0.74)
            Lambda = h / sigma
            print("\n>> RESULTADOS (Direto):")
            print("E = {0:.2e} | G = {1:.4e}".format(E, G))
            print("Wt/l = {0:.2f} | V = {1:.4f} | N = {2:.2f}".format(Wtl, V, N_rpm))
            print("h = {0:.4f} um".format(h))
            print("Lambda = {0:.4f}".format(Lambda))
            aguardar()
            
        elif opc_prob == "2":
            if V == 0:
                print("Erro: V=0, divisao por zero no Delta.")
                aguardar()
                continue
                
            Lam_5 = 1.0 / (2.68863 / V + 0.47767)
            h = Lam_5 * sigma
            base = h ** (1.0 / 0.74)
            denominador = G * N_rpm * (Wtl ** -0.148)
            LP = base / denominador
            
            print("\n>> RESULTADOS (Inverso):")
            print("E = {0:.2e} | G = {1:.4e}".format(E, G))
            print("Wt/l = {0:.2f} | V = {1:.4f} | N = {2:.2f}".format(Wtl, V, N_rpm))
            print("Lambda 5% (Delta) = {0:.4f}".format(Lam_5))
            print("h calculado = {0:.4f} um".format(h))
            print("LP = {0:.4f} s".format(LP))
            print("Para uma temperatura de, geralmente, 60C")
            aguardar()

# ==========================================
# Menu Teoria de Cheng
# ==========================================
def menu_cheng():
    while True:
        print("\n--- TEORIA DE CHENG ---")
        print("1. Rolamentos")
        print("2. Came-impulsor")
        print("3. Engrenagens")
        print("0. Voltar")
        opc = input("Escolha: ")
        
        if opc == "0" or opc == "": break
        elif opc == "1": menu_cheng_rolamentos()
        elif opc == "2": menu_cheng_came()
        elif opc == "3": menu_cheng_engrenagens()
        else: print("Opcao invalida.")

# ==========================================
# Gestor Principal
# ==========================================
def main():
    while True:
        print("\n===== ORGAOS DE MAQUINAS =====")
        print("1. Chumaceiras Radiais")
        print("2. Teoria de Cheng")
        print("0. Sair")
        opc = input("Escolha o Modulo: ")
        
        if opc == "0" or opc == "":
            print("Programa encerrado.")
            break
        elif opc == "1": menu_chumaceiras() 
        elif opc == "2": menu_cheng()
        else: print("Opcao invalida.")

if __name__ == "__main__":
    main()