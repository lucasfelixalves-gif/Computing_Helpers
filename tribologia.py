import math

# ==========================================
# FUNCOES AUXILIARES GLOBAIS
# ==========================================
def formatar_val(val):
    return "---" if val is None else "{0:.4g}".format(val)

def ler_input(texto, var_atual):
    display_val = "Vazio" if var_atual is None else "{0:.4g}".format(var_atual)
    inp = input(texto.format(display_val))
    if inp.strip():
        try:
            return float(inp)
        except ValueError:
            print("Invalido. Mantido.")
            return var_atual
    return var_atual

def aguardar():
    input("\n[Enter para voltar...]")

def interpolar_1d(x, lista_x, lista_y):
    if x <= lista_x[0]: return lista_y[0]
    if x >= lista_x[-1]: return lista_y[-1]
    
    for i in range(len(lista_x) - 1):
        x1, x2 = lista_x[i], lista_x[i+1]
        if x1 <= x <= x2:
            y1, y2 = lista_y[i], lista_y[i+1]
            return y1 + (x - x1) * (y2 - y1) / (x2 - x1)
    return None

# ==============================================================================
# ======================== MODULO A: CHUMACEIRAS RADIAIS =======================
# ==============================================================================

# BASE DE DADOS: TABELAS ADIMENSIONAIS
tabelas_chumaceira = {
    0.166: { # L/D < 1/6
        "epsilon": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95],
        "S_mod":   [0.99, 0.461, 0.272, 0.17, 0.106, 0.0625, 0.033, 0.0139, 0.00331, 0.000812],
        "phi":     [83, 75, 68, 61, 54, 47, 39, 31, 21, 15],
        "f_mod":   [18.75, 8.514, 4.98, 3.14, 2.016, 1.25, 0.722, 0.355, 0.114, 0.038],
        "Ca_adim": [18.94, 18.47, 18.31, 18.50, 19.02, 20.02, 21.89, 25.55, 34.58, 47.79]
    },
    0.25: { # L/D = 1/4
        "epsilon": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95],
        "S":       [16.2, 7.57, 4.49, 2.83, 1.78, 1.07, 0.58, 0.263, 0.0728, 0.0221],
        "phi":     [82.5, 75.5, 68.5, 61.5, 54, 47, 39.5, 31.5, 21.5, 15.5],
        "R_c_fa":  [307, 140, 82.5, 52.67, 34.26, 21.85, 13.19, 6.97, 2.70, 1.20],
        "Q_adim":  [0.0983, 0.196, 0.295, 0.393, 0.491, 0.590, 0.688, 0.787, 0.885, 0.933],
        "Ca_adim": [18.95, 18.49, 18.37, 18.61, 19.24, 20.42, 22.74, 26.50, 37.09, 54.30]
    },
    0.5: { # L/D = 1/2
        "epsilon": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95],
        "S":       [4.32, 2.03, 1.21, 0.784, 0.508, 0.318, 0.184, 0.0912, 0.0309, 0.0116],
        "phi":     [82, 75, 68.5, 61.53, 55, 48, 41, 33, 23.5, 17],
        "R_c_fa":  [82.10, 37.71, 22.55, 14.75, 9.94, 6.67, 4.33, 2.59, 1.27, 0.70],
        "Q_adim":  [0.0938, 0.187, 0.281, 0.374, 0.468, 0.562, 0.657, 0.751, 0.845, 0.890],
        "Ca_adim": [19, 18.57, 18.64, 18.81, 19.57, 20.97, 23.53, 28.40, 41.10, 60.34]
    },
    1.0: { # L/D = 1
        "epsilon": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95],
        "S":       [1.33, 0.631, 0.388, 0.260, 0.178, 0.120, 0.0776, 0.0443, 0.0185, 0.00831],
        "phi":     [79.5, 74.0, 68.0, 62.5, 56.5, 50.5, 44.0, 36.0, 26.0, 19.0],
        "R_c_fa":  [25.36, 11.87, 7.35, 5.07, 3.67, 2.70, 1.99, 1.40, 0.859, 0.563],
        "Q_adim":  [0.0801, 0.159, 0.237, 0.314, 0.390, 0.466, 0.542, 0.616, 0.688, 0.721],
        "Ca_adim": [19.06, 18.81, 18.94, 19.50, 20.62, 22.50, 25.64, 31.60, 46.43, 67.75]
    },
    2.0: { # L/D = 2
        "epsilon": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95],
        "S":       [0.559, 0.271, 0.173, 0.122, 0.0893, 0.0654, 0.0463, 0.0297, 0.0143, 0.00707],
        "phi":     [75, 71, 67, 62.5, 58, 52.5, 46.5, 39, 29, 21],
        "R_c_fa":  [10.76, 5.21, 3.40, 2.50, 1.96, 1.60, 1.31, 1.04, 0.730, 0.517],
        "Q_adim":  [0.0537, 0.104, 0.153, 0.199, 0.243, 0.285, 0.329, 0.369, 0.406, 0.422],
        "Ca_adim": [19.25, 19.22, 19.65, 20.49, 21.95, 24.46, 28.29, 35.01, 51.05, 73.12]
    },
    4.0: { # L/D > 4
        "epsilon": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95],
        "S":       [0.247, 0.123, 0.0823, 0.0628, 0.0483, 0.0389, 0.0297, 0.0211, 0.0114, 0.00605],
        "phi":     [69, 67, 64, 62, 58, 54, 49, 42, 32, 23],
        "R_c_fa":  [5.02, 2.61, 1.84, 1.47, 1.25, 1.10, 0.98, 0.852, 0.658, 0.494],
        "Ca_adim": [19.54, 19.85, 20.68, 22.03, 24.03, 26.89, 31.39, 38.80, 55.42, 78.42]
    }
}

# ESTADO GLOBAL DO MODULO A
estado_chumaceira = {
    'D': None, 'R': None, 'L': None, 'L_D': None,
    'c_R': None, 'c': None, 'e': None, 'epsilon': None, 'hmin': None,
    'N_rpm': None, 'omega': None, 'V': None, 'W': None,
    'eta': None, 'rho': None, 'cp': None, 'T0': None, 'alpha': None,
    'S': None, 'phi': None, 'fa': None, 'Ca': None, 'f_adim': None, 'Q_adim': None, 'Ca_adim': None,
    'Pa': None, 'Q': None, 'Qc': None, 'T2': None, 'Te': None, 'Ti': None
}

def resolver_chumaceira():
    global estado_chumaceira
    st = estado_chumaceira
    progresso = True
    
    while progresso:
        progresso = False
        
        # --- DEDUCOES GEOMETRICAS ---
        if st['D'] is not None and st['R'] is None:
            st['R'] = st['D'] / 2.0; progresso = True
        elif st['R'] is not None and st['D'] is None:
            st['D'] = st['R'] * 2.0; progresso = True
            
        if st['L'] is not None and st['D'] is not None and st['L_D'] is None:
            st['L_D'] = st['L'] / st['D']; progresso = True
            
        if st['c_R'] is not None and st['R'] is not None and st['c'] is None:
            st['c'] = st['c_R'] * st['R']; progresso = True
        if st['c'] is not None and st['R'] is not None and st['c_R'] is None:
            st['c_R'] = st['c'] / st['R']; progresso = True
            
        if st['e'] is not None and st['c'] is not None and st['epsilon'] is None:
            st['epsilon'] = st['e'] / st['c']; progresso = True
        elif st['epsilon'] is not None and st['c'] is not None and st['e'] is None:
            st['e'] = st['epsilon'] * st['c']; progresso = True
        
        if st['c'] is not None and st['epsilon'] is not None and st['hmin'] is None:
            st['hmin'] = st['c'] * (1.0 - st['epsilon']); progresso = True
        elif st['hmin'] is not None and st['c'] is not None and st['epsilon'] is None:
            st['epsilon'] = 1.0 - (st['hmin'] / st['c']); progresso = True

        # --- DEDUCOES CINEMATICAS ---
        if st['N_rpm'] is not None and st['omega'] is None:
            st['omega'] = 2.0 * math.pi * st['N_rpm'] / 60.0; progresso = True
            
        if st['omega'] is not None and st['R'] is not None and st['V'] is None:
            st['V'] = st['omega'] * st['R']; progresso = True
            
        # --- SOMMERFELD ---
        if all(st[k] is not None for k in ['c_R', 'eta', 'L', 'V', 'W']) and st['S'] is None:
            st['S'] = (1.0 / (st['c_R']**2)) * ((st['eta'] * st['L'] * st['V']) / (math.pi * st['W']))
            progresso = True
            
        # --- TABELAS ---
        if st['L_D'] is not None:
            ld_disponiveis = list(tabelas_chumaceira.keys())
            ld_key = min(ld_disponiveis, key=lambda k: abs(k - st['L_D']))
            tab = tabelas_chumaceira[ld_key]
            
            if st['S'] is not None and st['epsilon'] is None:
                if "S" in tab:
                    st['epsilon'] = interpolar_1d(st['S'], tab['S'][::-1], tab['epsilon'][::-1])
                elif "S_mod" in tab:
                    s_mod = st['S'] * (st['L_D']**2)
                    st['epsilon'] = interpolar_1d(s_mod, tab['S_mod'][::-1], tab['epsilon'][::-1])
                progresso = True
                
            if st['epsilon'] is not None:
                if st['phi'] is None:
                    st['phi'] = interpolar_1d(st['epsilon'], tab['epsilon'], tab['phi']); progresso = True
                if st['Ca_adim'] is None and "Ca_adim" in tab:
                    st['Ca_adim'] = interpolar_1d(st['epsilon'], tab['epsilon'], tab['Ca_adim']); progresso = True
                
                if st['f_adim'] is None:
                    if "R_c_fa" in tab:
                        st['f_adim'] = interpolar_1d(st['epsilon'], tab['epsilon'], tab['R_c_fa'])
                    elif "f_mod" in tab:
                        f_mod = interpolar_1d(st['epsilon'], tab['epsilon'], tab['f_mod'])
                        st['f_adim'] = f_mod / (st['L_D']**2)
                    progresso = True
                    
                if st['Q_adim'] is None:
                    if "Q_adim" in tab:
                        st['Q_adim'] = interpolar_1d(st['epsilon'], tab['epsilon'], tab['Q_adim'])
                    elif ld_key == 4.0:
                        st['Q_adim'] = 0.0
                    progresso = True

        # --- FISICA DE ATRITO E DEBITOS ---
        if st['Q_adim'] is not None and all(st[k] is not None for k in ['L', 'c', 'V']) and st['Q'] is None:
            st['Q'] = st['Q_adim'] * st['L'] * st['c'] * st['V']
            progresso = True
            
        if st['hmin'] is not None and st['L'] is not None and st['V'] is None and st['Qc'] is None:
            st['Qc'] = st['hmin'] * st['L'] * (st['V'] / 2.0)
            progresso = True
            
        if st['f_adim'] is not None and st['c_R'] is not None and st['fa'] is None:
            st['fa'] = st['f_adim'] * st['c_R']
            progresso = True
            
        if st['fa'] is not None and st['R'] is not None and st['W'] is not None and st['Ca'] is None:
            st['Ca'] = st['R'] * st['W'] * st['fa']
            progresso = True
            
        if st['Ca'] is not None and st['omega'] is not None and st['Pa'] is None:
            st['Pa'] = st['Ca'] * st['omega']
            progresso = True
            
        # --- BALANCO TERMICO ---
        if all(st[k] is not None for k in ['T0', 'alpha', 'Pa', 'Q', 'Qc', 'rho', 'cp']) and st['T2'] is None:
            numerador = st['alpha'] * st['Pa'] * (st['Q'] + st['Qc'])
            denominador = st['rho'] * st['cp'] * st['Q'] * ((st['Q'] / 2.0) + st['Qc'])
            if denominador != 0:
                st['T2'] = st['T0'] + (numerador / denominador)
                progresso = True
                
        if all(st[k] is not None for k in ['T0', 'Q', 'T2', 'Qc']) and st['Te'] is None:
            if (st['Q'] + st['Qc']) != 0:
                st['Te'] = (st['T0'] * st['Q'] + st['T2'] * st['Qc']) / (st['Q'] + st['Qc'])
                progresso = True
                
        if st['Te'] is not None and st['T2'] is not None and st['Ti'] is None:
            st['Ti'] = (st['Te'] + st['T2']) / 2.0
            progresso = True

def menu_geometria():
    print("\n--- 1. GEOMETRIA ---")
    print("D   = {0} m   | L = {1} m".format(formatar_val(estado_chumaceira['D']), formatar_val(estado_chumaceira['L'])))
    print("c/R = {0}     | c = {1} m".format(formatar_val(estado_chumaceira['c_R']), formatar_val(estado_chumaceira['c'])))
    print("e   = {0} m   | eps= {1}".format(formatar_val(estado_chumaceira['e']), formatar_val(estado_chumaceira['epsilon'])))
    print("hmin= {0} m".format(formatar_val(estado_chumaceira['hmin'])))
    
    if input("\nEditar valores? (s/n) [n]: ").lower() == 's':
        estado_chumaceira['D'] = ler_input("Diametro D (m) [{0}]: ", estado_chumaceira['D'])
        estado_chumaceira['L'] = ler_input("Comprimento L (m) [{0}]: ", estado_chumaceira['L'])
        estado_chumaceira['c_R'] = ler_input("Relacao c/R [{0}]: ", estado_chumaceira['c_R'])
        estado_chumaceira['c'] = ler_input("Folga radial c (m) [{0}]: ", estado_chumaceira['c'])
        estado_chumaceira['e'] = ler_input("Excentricidade e (m) [{0}]: ", estado_chumaceira['e'])
        estado_chumaceira['epsilon'] = ler_input("Excentricidade eps [{0}]: ", estado_chumaceira['epsilon'])

def menu_operacao():
    print("\n--- 2. OPERACAO ---")
    print("N = {0} rpm | W = {1} N".format(formatar_val(estado_chumaceira['N_rpm']), formatar_val(estado_chumaceira['W'])))
    print("V = {0} m/s".format(formatar_val(estado_chumaceira['V'])))
    
    if input("\nEditar valores? (s/n) [n]: ").lower() == 's':
        estado_chumaceira['N_rpm'] = ler_input("Rotacao N (rpm) [{0}]: ", estado_chumaceira['N_rpm'])
        estado_chumaceira['W'] = ler_input("Carga W (N) [{0}]: ", estado_chumaceira['W'])

def menu_lubrificante():
    print("\n--- 3. LUBRIFICANTE ---")
    print("eta = {0} Pa.s | rho = {1} kg/m3".format(formatar_val(estado_chumaceira['eta']), formatar_val(estado_chumaceira['rho'])))
    print("cp  = {0} J/kgK| T0  = {1} C".format(formatar_val(estado_chumaceira['cp']), formatar_val(estado_chumaceira['T0'])))
    print("alpha= {0}".format(formatar_val(estado_chumaceira['alpha'])))
    
    if input("\nEditar valores? (s/n) [n]: ").lower() == 's':
        estado_chumaceira['eta'] = ler_input("Viscosidade eta (Pa.s) [{0}]: ", estado_chumaceira['eta'])
        estado_chumaceira['rho'] = ler_input("Densidade rho (kg/m3) [{0}]: ", estado_chumaceira['rho'])
        estado_chumaceira['cp'] = ler_input("Calor especifico cp [{0}]: ", estado_chumaceira['cp'])
        estado_chumaceira['alpha'] = ler_input("Dissipacao alpha [{0}]: ", estado_chumaceira['alpha'])
        estado_chumaceira['T0'] = ler_input("Temp. Entrada T0 (C) [{0}]: ", estado_chumaceira['T0'])

def menu_resultados():
    print("\n--- 4. RESULTADOS ---")
    print("L/D Usado = {0}".format(formatar_val(estado_chumaceira['L_D'])))
    print("S  = {0} | phi = {1} deg".format(formatar_val(estado_chumaceira['S']), formatar_val(estado_chumaceira['phi'])))
    print("fa = {0} | Ca  = {1} N.m".format(formatar_val(estado_chumaceira['fa']), formatar_val(estado_chumaceira['Ca'])))
    print("Pa = {0} W".format(formatar_val(estado_chumaceira['Pa'])))
    print("Q  = {0} m3/s | Qc = {1} m3/s".format(formatar_val(estado_chumaceira['Q']), formatar_val(estado_chumaceira['Qc'])))
    print("T2 = {0} C   | Te = {1} C".format(formatar_val(estado_chumaceira['T2']), formatar_val(estado_chumaceira['Te'])))
    aguardar()

def menu_chumaceiras_principal():
    while True:
        print("\n" + "-"*30)
        print("  MODULO A: CHUMACEIRAS RADIAIS")
        print("-"*30)
        print("1. Geometria   (D, L, c/R...)")
        print("2. Operacao    (N, W...)")
        print("3. Lubrificante(eta, rho...)")
        print("4. Resultados  (S, T2, Pa...)")
        print("5. [EXECUTAR SOLVER]")
        print("6. Limpar Quadro Negro")
        print("0. Voltar ao Menu Principal")
        
        opc = input("Escolha a opcao: ")
        
        if opc == '1': menu_geometria()
        elif opc == '2': menu_operacao()
        elif opc == '3': menu_lubrificante()
        elif opc == '4': menu_resultados()
        elif opc == '5':
            print("\n[ A deduzir valores... ]")
            resolver_chumaceira()
            if estado_chumaceira['L_D'] is not None:
                ld_key = min(tabelas_chumaceira.keys(), key=lambda k: abs(k - estado_chumaceira['L_D']))
                if abs(ld_key - estado_chumaceira['L_D']) > 0.01:
                    print("AVISO: L/D real ({0:.3f}) foi aproximado para a tabela L/D = {1}".format(estado_chumaceira['L_D'], ld_key))
            print("[ Calculo concluido! Va a Resultados (4) ]")
            aguardar()
        elif opc == '6':
            for key in estado_chumaceira.keys():
                estado_chumaceira[key] = None
            print("\n[ Memoria limpa. ]")
            aguardar()
        elif opc == '0':
            break

# ==============================================================================
# ========================== MODULO B: TEORIA DE CHENG =========================
# ==============================================================================

def menu_cheng_rolamentos():
    print("\n--- CHENG: ROLAMENTOS ---")
    D = ler_input("Diametro exterior D (m) [{0}]: ", None)
    N = ler_input("Diferenca de velocidades N (rpm) [{0}]: ", None)
    LP = ler_input("Parametro lubrificante LP (s) [{0}]: ", None)
    
    print("\n1. Esferas (sigma = 0.178 um)")
    print("2. Rolos cilindricos/esfericos (sigma = 0.356 um)")
    print("3. Conicos/agulhas (sigma = 0.229 um)")
    tipo = input("Tipo de rolamento: ")
    
    print("\n1. Anel Interior\n2. Anel Exterior")
    anel = input("Anel a analisar: ")
    
    dados = {
        '1': {'int': 8.65e-4, 'ext': 9.43e-4, 'sigma': 0.178},
        '2': {'int': 8.37e-4, 'ext': 8.99e-4, 'sigma': 0.356},
        '3': {'int': 8.01e-4, 'ext': 8.48e-4, 'sigma': 0.229}
    }
    
    if tipo in dados and anel in ['1', '2'] and None not in (D, N, LP):
        C = dados[tipo]['int'] if anel == '1' else dados[tipo]['ext']
        sigma = dados[tipo]['sigma']
        
        h = C * D * math.pow((LP * N), 0.74)
        Lambda = h / sigma
        
        print("\n[ RESULTADOS ROLAMENTO ]")
        print("Espessura de filme (h): {0:.4g} um".format(h))
        print("Espessura especifica (Lambda): {0:.4g}".format(Lambda))
        if Lambda >= 1.5:
            print("Estado: SEGURO (Lambda >= 1.5)")
        else:
            print("Estado: RISCO DE AVARIA PRECOCE")
    else:
        print("\n[!] Falta de dados ou opcao invalida.")
    aguardar()

def menu_cheng_cames():
    print("\n--- CHENG: CAME-IMPULSOR ---")
    N = ler_input("Velocidade angular came N (rpm) [{0}]: ", None)
    LP = ler_input("Parametro lubrificante LP (s) [{0}]: ", None)
    rn = ler_input("Menor raio curvatura came rn (m) [{0}]: ", None)
    rf = ler_input("Raio do impulsor rf (m) [{0}]: ", None)
    l = ler_input("Dist. max contacto ao eixo l (m) [{0}]: ", None)
    sigma = ler_input("Rugosidade composta sigma (um) [{0}]: ", None)
    
    print("\n1. Com escorregamento\n2. Sem escorregamento")
    esc = input("Condicao: ")
    
    if None not in (N, LP, rn, rf, l, sigma) and esc in ['1', '2']:
        fN = abs(2.0 * rn - l) if esc == '1' else 2.0 * l
        R = 1.0 / ( (1.0 / rn) + (1.0 / rf) )
        
        h = 4.35e-3 * math.pow((fN * LP * N), 0.74) * math.pow(R, 0.26)
        Lambda = h / sigma
        
        print("\n[ RESULTADOS CAME-IMPULSOR ]")
        print("Raio equivalente (R): {0:.4g} m".format(R))
        print("Fator distancia (fN): {0:.4g} m".format(fN))
        print("Espessura de filme (h): {0:.4g} um".format(h))
        print("Espessura especifica (Lambda): {0:.4g}".format(Lambda))
        if Lambda < 1.0:
            print("Estado: Lubrificacao limite/mista (Normal)")
    else:
        print("\n[!] Falta de dados.")
    aguardar()

def menu_cheng_engrenagens():
    print("\n--- CHENG: ENGRENAGENS (PARALELAS EXT.) ---")
    n2 = ler_input("Vel. angular roda n2 (rpm) [{0}]: ", None)
    u = ler_input("Razao de multiplicacao u [{0}]: ", None)
    a = ler_input("Entre-eixo a (m) [{0}]: ", None)
    b = ler_input("Largura do dente b (m) [{0}]: ", None)
    alpha = ler_input("Angulo pressao alpha (deg) [{0}]: ", 20.0)
    beta = ler_input("Angulo helice beta (deg) [{0}]: ", 0.0)
    T2 = ler_input("Binario da roda T2 (Nm) [{0}]: ", None)
    LP = ler_input("Parametro lubrificante LP (s) [{0}]: ", None)
    
    print("\n[ RUGOSIDADE ]")
    print("1. Fresadas (1.78 um -> 1.02 um)")
    print("2. 'Shaved' (1.27 um -> 1.02 um)")
    print("3. Retificadas (0.89 um ou 0.51 um)")
    print("4. Inserir manualmente")
    op_sigma = input("Opcao: ")
    
    if op_sigma == '1': sigma = ler_input("1:Inicial(1.78) ou 2:Rodagem(1.02)? ", 1.78)
    elif op_sigma == '2': sigma = ler_input("1:Inicial(1.27) ou 2:Rodagem(1.02)? ", 1.27)
    elif op_sigma == '3': sigma = ler_input("1:Suave(0.89) ou 2:Forte(0.51)? ", 0.89)
    else: sigma = ler_input("Rugosidade composta sigma (um) [{0}]: ", None)

    if None not in (n2, u, a, b, alpha, beta, T2, LP, sigma):
        alpha_rad = math.radians(alpha)
        beta_rad = math.radians(beta)
        
        G = 3.4e-4 * math.pow((u * a * math.sin(alpha_rad)), -0.148) * math.pow((u + 1.0), 2)
        Wt_l = (T2 * (u + 1.0)) / (u * a * b * math.cos(alpha_rad) * math.pow(math.cos(beta_rad), 2))
        V = (2.0 * math.pi * u * a * n2) / (60.0 * (u + 1.0))
        
        termo_N = n2 / math.pow((u + 1.0), 2)
        h = math.pow((G * LP * termo_N * math.pow(Wt_l, -0.148)), 0.74)
        Lambda = h / sigma
        
        Lambda_5 = math.pow((2.68863 / V) + 0.47767, -1.0)
        
        print("\n[ RESULTADOS ENGRENAGENS ]")
        print("Vel. Tangencial (V): {0:.4g} m/s".format(V))
        print("Carga especifica (Wt/l): {0:.4g} N/m".format(Wt_l))
        print("Parametro Geom. (G): {0:.4g}".format(G))
        print("Espessura filme (h): {0:.4g} um".format(h))
        print("Espessura esp. (Lambda): {0:.4g}".format(Lambda))
        print("Lambda critico (5%): {0:.4g}".format(Lambda_5))
        
        if Lambda >= Lambda_5:
            print("Estado: SEGURO (Lambda > Critico)")
        else:
            print("Estado: RISCO ELEVADO DE AVARIA")
    else:
        print("\n[!] Falta de dados.")
    aguardar()

def menu_cheng_principal():
    while True:
        print("\n" + "-"*30)
        print("  MODULO B: TEORIA DE CHENG")
        print("-"*30)
        print("1. Rolamentos")
        print("2. Came-Impulsor")
        print("3. Engrenagens (Paralelas Ext.)")
        print("0. Voltar ao Menu Principal")
        
        opc = input("Escolha a opcao: ")
        
        if opc == '1': menu_cheng_rolamentos()
        elif opc == '2': menu_cheng_cames()
        elif opc == '3': menu_cheng_engrenagens()
        elif opc == '0': break

# ==============================================================================
# =============================== MENU PRINCIPAL ===============================
# ==============================================================================

def main():
    while True:
        print("\n" + "="*35)
        print("     CALCULADORA DE TRIBOLOGIA")
        print("="*35)
        print("1. Chumaceiras Radiais (Modulo A)")
        print("2. Teoria de Cheng (Modulo B)")
        print("0. Sair do Programa")
        
        opc = input("\nEscolha a opcao: ")
        
        if opc == '1':
            menu_chumaceiras_principal()
        elif opc == '2':
            menu_cheng_principal()
        elif opc == '0':
            print("\nA encerrar o programa...")
            break
        else:
            print("\n[!] Opcao invalida.")
            aguardar()

if __name__ == "__main__":
    main()