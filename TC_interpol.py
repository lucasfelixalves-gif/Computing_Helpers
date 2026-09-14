import math

"""
Ferramenta de determinacao de propriedades
"""
# ==========================================
# Tabelas ar; agua ; vapor saturado
# ==========================================

T_AR = [-50, 0, 10, 20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200]
DADOS_AR = {
    "1": {"nome": "rho (kg/m3)", "valores": [1.5340, 1.2930, 1.2488, 1.2045, 1.1656, 1.1267, 1.0931, 1.0595, 1.0297, 0.9998, 0.9458, 0.8968, 0.8535, 0.8170, 0.7785, 0.7457]},
    "2": {"nome": "cp (kJ/kgK)", "valores": [1.005, 1.005, 1.005, 1.005, 1.005, 1.005, 1.005, 1.009, 1.009, 1.009, 1.009, 1.013, 1.013, 1.017, 1.022, 1.026]},
    "3": {"nome": "k (W/mK)", "valores": [0.0204, 0.0243, 0.0250, 0.0257, 0.0264, 0.0271, 0.0278, 0.0285, 0.0292, 0.0299, 0.0314, 0.0328, 0.0343, 0.0358, 0.0372, 0.0386]},
    "4": {"nome": "mu x 10^6 (N.s/m2)", "valores": [14.641, 17.189, 17.684, 18.179, 18.645, 19.110, 19.561, 20.012, 20.463, 20.913, 21.795, 22.648, 23.491, 24.314, 25.127, 25.823]},
    "5": {"nome": "nu x 10^6 (m2/s)", "valores": [9.55, 13.30, 14.21, 15.11, 16.04, 16.97, 17.94, 18.90, 19.92, 20.94, 23.06, 25.23, 27.55, 29.85, 32.29, 34.63]},
    "6": {"nome": "beta x 10^3 (K-1)", "valores": [4.51, 3.67, 3.55, 3.43, 3.32, 3.20, 3.10, 3.00, 2.92, 2.83, 2.68, 2.55, 2.43, 2.32, 2.21, 2.11]},
    "7": {"nome": "D (m2/h)", "valores": [0.048, 0.067, 0.072, 0.076, 0.081, 0.086, 0.091, 0.096, 0.101, 0.107, 0.118, 0.130, 0.143, 0.155, 0.168, 0.182]},
    "8": {"nome": "Pr", "valores": [0.725, 0.715, 0.714, 0.713, 0.712, 0.711, 0.710, 0.709, 0.709, 0.708, 0.703, 0.700, 0.695, 0.690, 0.690, 0.685]}
}

T_AGUA = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200]
DADOS_AGUA = {
    "1": {"nome": "P (atm)", "valores": [1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.03, 2.02, 3.68, 6.30, 10.23, 15.86]},
    "2": {"nome": "rho (kg/m3)", "valores": [999.8, 999.7, 998.2, 995.65, 992.2, 988.0, 983.2, 977.8, 971.8, 965.3, 958.4, 943.1, 928.1, 907.4, 886.8, 864.7]},
    "3": {"nome": "cp (kJ/kgK)", "valores": [4.218, 4.192, 4.182, 4.179, 4.179, 4.181, 4.184, 4.190, 4.197, 4.205, 4.216, 4.246, 4.287, 4.342, 4.409, 4.497]},
    "4": {"nome": "k (W/mK)", "valores": [0.552, 0.578, 0.598, 0.614, 0.628, 0.641, 0.651, 0.661, 0.669, 0.676, 0.682, 0.685, 0.684, 0.682, 0.678, 0.665]},
    "5": {"nome": "mu x 10^6 (N.s/m2)", "valores": [1790.5, 1306.3, 1001.6, 796.7, 651.7, 545.9, 465.5, 403.8, 354.8, 314.6, 277.3, 234.2, 198.9, 171.5, 150.4, 136.4]},
    "6": {"nome": "nu x 10^6 (m2/s)", "valores": [1.792, 1.304, 1.004, 0.801, 0.658, 0.553, 0.474, 0.413, 0.365, 0.326, 0.295, 0.249, 0.215, 0.189, 0.170, 0.158]},
    "7": {"nome": "beta x 10^3 (K-1)", "valores": [-0.070, 0.088, 0.207, 0.303, 0.385, 0.457, 0.523, 0.585, 0.643, 0.698, 0.752, 0.860, 0.975, 1.098, 1.233, 1.392]},
    "8": {"nome": "Pr", "valores": [13.67, 9.47, 7.01, 5.43, 4.34, 3.56, 2.99, 2.56, 2.23, 1.96, 1.75, 1.45, 1.25, 1.09, 0.98, 0.92]},
    "9": {"nome": "qlv (kJ/kg)", "valores": [2501, 2477, 2454, 2430, 2406, 2382, 2358, 2333, 2308, 2283, 2257, 2203, 2145, 2083, 2015, 1941]},
    "10": {"nome": "sigma x 10^3 (N/m)", "valores": [75.64, 74.23, 72.75, 71.20, 69.60, 67.94, 66.24, 64.47, 62.67, 60.82, 58.91, 54.96, 50.85, 46.58, 42.19, 37.69]}
}

T_VAPOR = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200]
DADOS_VAPOR = {
    "1": {"nome": "p (kPa)", "valores": [0.6112, 1.228, 2.339, 4.247, 7.384, 12.351, 19.946, 31.200, 47.415, 70.018, 101.318, 198.665, 361.501, 618.139, 1002.635, 1554.671]},
    "2": {"nome": "rho (kg/m3)", "valores": [0.0049, 0.0094, 0.0173, 0.0304, 0.0512, 0.0831, 0.1304, 0.1984, 0.2934, 0.4239, 0.598, 1.121, 1.966, 3.258, 5.156, 7.857]},
    "3": {"nome": "cp (kJ/kg.K)", "valores": [1.888, 1.896, 1.906, 1.918, 1.932, 1.948, 1.966, 1.987, 2.011, 2.039, 2.073, 2.156, 2.269, 2.417, 2.618, 2.886]},
    "4": {"nome": "k (W/mK)", "valores": [0.016, 0.017, 0.018, 0.019, 0.019, 0.020, 0.021, 0.022, 0.023, 0.024, 0.0248, 0.0270, 0.0294, 0.0322, 0.0354, 0.0391]},
    "5": {"nome": "mu x 10^6 (N.s/m2)", "valores": [9.216, 9.461, 9.727, 10.010, 10.308, 10.616, 10.935, 11.260, 11.592, 11.929, 12.269, 12.956, 13.647, 14.337, 15.026, 15.715]}
}


# ==========================================
# Funcoes de interpolacao
# ==========================================

def interpolar(x, list_x, list_y):
    # Se estiver fora dos limites, retorna o valor extremo correspondente
    if x <= list_x[0]: return list_y[0]
    if x >= list_x[-1]: return list_y[-1]
    
    # Interpolação linear padrão: y = y0 + (y1 - y0) * ((x - x0) / (x1 - x0))
    for i in range(len(list_x) - 1):
        if list_x[i] <= x <= list_x[i+1]:
            x0 = list_x[i]
            x1 = list_x[i+1]
            y0 = list_y[i]
            y1 = list_y[i+1]
            if x0 == x1: return y0
            return y0 + (y1 - y0) * ((x - x0) / (x1 - x0))

def aguardar():
    input("\n[Pressione Enter para continuar...]")

# ==========================================
#                 Menus
# ==========================================

def menu_propriedades(nome_tabela, lista_T, dic_dados):
    while True:
        print("\n--- [ {tabela} ] ---".format(tabela=nome_tabela))
        try:
            t_ref = float(input("Introduz Tref (°C) ou '0' para voltar: "))
            if t_ref == 0: break 
            
            while True:
                # Título ligeiramente mais curto para poupar espaço
                print("\n--- Interpolar a {t:.2f}°C ---".format(t=t_ref))
                for chave in sorted(dic_dados.keys(), key=int):
                    print("{k}. {prop}".format(k=chave, prop=dic_dados[chave]["nome"]))
                
                # A linha do 'print("0. Voltar...")' foi removida.
                # A indicação de voltar está agora embutida no próprio input.
                opc = input("Opção (0 volta): ")
                
                if opc == '0':
                    break
                elif opc in dic_dados:
                    resultado = interpolar(t_ref, lista_T, dic_dados[opc]["valores"])
                    unidade = dic_dados[opc]["nome"]
                    print("\n>> RESULTADO: {res:.4f}  [{u}]".format(res=resultado, u=unidade))
                    aguardar()
                else:
                    print("Opção inválida.")
        except ValueError:
            print("Erro: Introduza um valor numérico válido.")
            aguardar()

def menu():
    while True:
        print("\n--- INTERPOLAÇÃO DE PROPRIEDADES TERMODINÂMICAS ---")
        print("1. Ar (Pressão Atmosférica)")
        print("2. Água Líquida")
        print("3. Água (Vapor Saturado)")
        print("0. Sair")
        opc = input("Escolha a tabela: ")
        
        if opc == '0': 
            print("Encerrando o programa.")
            break
        elif opc == '1':
            menu_propriedades("Ar", T_AR, DADOS_AR)
        elif opc == '2':
            menu_propriedades("Água Líquida", T_AGUA, DADOS_AGUA)
        elif opc == '3':
            menu_propriedades("Água (Vapor Saturado)", T_VAPOR, DADOS_VAPOR)
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()