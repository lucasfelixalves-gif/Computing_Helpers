import math

EPS = 1e-9

# ==========================================
# VARIÁVEIS GLOBAIS DE ENTRADA
# ==========================================
z1 = 20.0       # Número de dentes do pinhão
z2 = 41.0       # Número de dentes da roda
mn = 2.0        # Módulo normal (mm)
alpha_n = 20.0  # Ângulo de pressão normal (graus)
beta = 0.0      # Ângulo de hélice (graus)
b = 20.0        # Largura da roda (mm)
x1 = 0.0        # Coeficiente de correção do pinhão
x2 = 0.0        # Coeficiente de correção da roda
n1 = 1000.0     # Rotação do pinhão (rpm)
aw_imposto = 0.0 # Entre-eixo forçado (0 = cálculo automático)
dR1 = 0.0       # Diâmetro do calibre pinhão (0 = ideal)
dR2 = 0.0       # Diâmetro do calibre roda (0 = ideal)

# ==========================================
# FUNÇÕES MATEMÁTICAS AUXILIARES
# ==========================================
def inv(angulo_rad):
    return math.tan(angulo_rad) - angulo_rad

def get_alpha_from_inv(inv_val):
    if inv_val <= 0: return 0.0
    ang = math.pow(3.0 * inv_val, 1.0 / 3.0)
    for _ in range(20):
        tan_ang = math.tan(ang)
        f = tan_ang - ang - inv_val
        df = tan_ang**2
        if df == 0: break
        ang -= f / df
        if abs(f) < 1e-8: break
    return ang

def ler_input(texto, var_atual):
    inp = input(texto.format(var_atual))
    if inp.strip():
        try:
            return float(inp)
        except ValueError:
            print("Valor inválido. Mantido o valor anterior.")
            return var_atual
    return var_atual

def clamp(v, lo, hi):
    if v < lo: return lo
    if v > hi: return hi
    return v

def calcular_k_wk(z, zv, x, m_n, alpha_n_rad, alpha_t_rad, beta_rad, cos_betab, sin_betab):
    # Fórmula universal para k (Eq. da sebenta: usa zv e alpha_n)
    k_float = (zv * alpha_n_rad / math.pi) + 0.5 + (2.0 * x * math.tan(alpha_n_rad) / math.pi)
    k = int(round(k_float))
    if k < 1: k = 1

    # Eq. 5.24 - Cota normal Wnk (Híbrida: usa z real e inv(alpha_t))
    wnk = m_n * math.cos(alpha_n_rad) * (((k - 0.5) * math.pi) + z * inv(alpha_t_rad))
    wnk += 2.0 * x * m_n * math.sin(alpha_n_rad)

    # Eq. 5.25 - Cota transversal Wtk
    wtk = wnk / cos_betab if cos_betab != 0 else wnk

    # Eq. 5.26 - Largura mínima b_min
    bmin = wnk * sin_betab

    return k, wnk, wtk, bmin

# ==========================================
# MÉTODOS DE CÁLCULO DE CORREÇÃO
# ==========================================
def calcular_correcoes_ideais():
    global x1, x2, aw_imposto
    alpha_n_rad = math.radians(alpha_n)
    beta_rad = math.radians(beta)
    cos_beta = math.cos(beta_rad)
    if abs(cos_beta) < EPS: return
    
    zv1 = z1 / (cos_beta**3)
    zv2 = z2 / (cos_beta**3)

    def obj_func(x_val, z1_virt, z2_virt, x1_fixed=None):
        xt1 = x_val if x1_fixed is None else x1_fixed
        xt2 = -x_val if x1_fixed is None else x_val
            
        r1, r2 = (z1_virt * mn) / 2.0, (z2_virt * mn) / 2.0
        a = r1 + r2
        inv_an = inv(alpha_n_rad)
        inv_aw = inv_an + 2 * math.tan(alpha_n_rad) * (xt1 + xt2) / (z1_virt + z2_virt)
        aw_rad = get_alpha_from_inv(inv_aw)
        
        if aw_rad == 0.0: return 999
        a_w = a * math.cos(alpha_n_rad) / math.cos(aw_rad)
        
        ra1, ra2 = r1 + mn * (1 + xt1), r2 + mn * (1 + xt2)
        rb1, rb2 = r1 * math.cos(alpha_n_rad), r2 * math.cos(alpha_n_rad)
        if ra1 < rb1 or ra2 < rb2: return 999
        
        delta1, delta2 = ra1**2 - rb1**2, ra2**2 - rb2**2
        if delta1 < 0 or delta2 < 0: return 999

        T1A = math.sqrt(delta1)
        T2A = a_w * math.sin(aw_rad) - T1A
        T2B = math.sqrt(delta2)
        T1B = a_w * math.sin(aw_rad) - T2B
        
        if T1B <= 0 or T2A <= 0: return 999
        
        gs1B = abs(1.0 - (z1_virt/z2_virt) * (T2B / T1B))
        gs2A = abs((z2_virt/z1_virt) * (T1A / T2A) - 1.0)
        return gs1B - gs2A

    def find_root(z1_cur, z2_cur, x1_fixed=None):
        best_x, min_diff = 0, 9999
        low, high = -1.5, 1.5
        for _ in range(4):
            step = (high - low) / 50.0
            for i in range(51):
                x_test = low + i * step
                diff = abs(obj_func(x_test, z1_cur, z2_cur, x1_fixed))
                if diff < min_diff:
                    min_diff, best_x = diff, x_test
            low, high = best_x - step, best_x + step
        return best_x

    if (zv1 + zv2) >= 60:
        print("\n=> zv1+zv2 >= 60. Aplicando Metodo Direto (Dentes Virtuais).")
        x_ideal = find_root(zv1, zv2)
        x1, x2 = x_ideal, -x_ideal
    else:
        print("\n=> zv1+zv2 < 60. Aplicando Metodo Henriot (Dentes Virtuais).")
        x1_ideal = find_root(zv1, 60 - zv1)
        x2_ideal = find_root(zv1, zv2, x1_fixed=x1_ideal)
        x1, x2 = x1_ideal, x2_ideal
    
    aw_imposto = 0.0
    print("Correcoes calculadas: x1 = {0:.4f}, x2 = {1:.4f}".format(x1, x2))

def calcular_correcoes_iso():
    global x1, x2, aw_imposto
    alpha_n_rad = math.radians(alpha_n)
    beta_rad = math.radians(beta)
    cos_beta = math.cos(beta_rad)
    if abs(cos_beta) < EPS: return
    mt = mn / cos_beta if beta != 0 else mn
    alpha_t_rad = math.atan(math.tan(alpha_n_rad)/math.cos(beta_rad)) if beta != 0 else alpha_n_rad
        
    a_corte = (z1 + z2) * mt / 2.0
    aw_imp = ler_input("Definir o Entre-eixo imposto [{0:.4f}]: ", a_corte)
    tipo = input("Tipo de transmissao (1: Redutora, 2: Multiplicadora) [1]: ")
    lmbda = 0.0 if tipo.strip() == '2' else 0.75

    if aw_imp < a_corte * math.cos(alpha_t_rad):
        print("Erro: O entre-eixo imposto e inferior ao limite base!")
        return

    cos_aw = clamp(a_corte * math.cos(alpha_t_rad) / aw_imp, -1.0, 1.0)
    aw_rad = math.acos(cos_aw)
    Px = (inv(aw_rad) - inv(alpha_t_rad)) * (z1 + z2) / (2.0 * math.tan(alpha_n_rad))
    u = z2 / z1
    
    x1 = lmbda * ((u - 1.0) / (u + 1.0)) + Px / (u + 1.0)
    x2 = Px - x1
    aw_imposto = 0.0
    
    print("\nResultados do Metodo ISO:")
    print("Soma das correcoes (Sigma x): {0:.4f}".format(Px))
    print("Correcoes aplicadas: x1 = {0:.4f} | x2 = {1:.4f}".format(x1, x2))

# ==========================================
# CÁLCULO GERAL E INTERFERÊNCIAS
# ==========================================
def calcular_propriedades():
    alpha_n_rad = math.radians(alpha_n)
    beta_rad = math.radians(beta)
    cos_beta = math.cos(beta_rad)
    if z1 <= 0 or z2 <= 0 or mn <= 0 or abs(cos_beta) < EPS: return None

    pn = math.pi * mn
    pbn = pn * math.cos(alpha_n_rad)
    mt = mn / cos_beta if beta != 0 else mn
    alpha_t_rad = math.atan(math.tan(alpha_n_rad)/math.cos(beta_rad)) if beta != 0 else alpha_n_rad
    alpha_t_deg = math.degrees(alpha_t_rad)
    pt = math.pi * mt
    pbt = pt * math.cos(alpha_t_rad)
    
    betab_rad = math.asin(math.sin(beta_rad) * math.cos(alpha_n_rad))
    betab_deg = math.degrees(betab_rad)
    cos_betab = math.cos(betab_rad)
    sin_betab = math.sin(betab_rad)
    
    zv1 = z1 / (cos_beta**3)
    zv2 = z2 / (cos_beta**3)

    r1, r2 = (z1 * mt) / 2.0, (z2 * mt) / 2.0
    rb1, rb2 = r1 * math.cos(alpha_t_rad), r2 * math.cos(alpha_t_rad)
    d1, d2 = r1 * 2.0, r2 * 2.0
    db1, db2 = rb1 * 2.0, rb2 * 2.0
    a = r1 + r2
    
    if aw_imposto > 0.0:
        a_w = aw_imposto
        aw_rad = math.acos(clamp(a * math.cos(alpha_t_rad) / a_w, -1.0, 1.0))
    else:
        inv_aw = inv(alpha_t_rad) + 2 * math.tan(alpha_n_rad) * (x1 + x2) / (z1 + z2)
        aw_rad = get_alpha_from_inv(inv_aw)
        if abs(math.cos(aw_rad)) < EPS: return None
        a_w = a * math.cos(alpha_t_rad) / math.cos(aw_rad)
        
    aw_deg = math.degrees(aw_rad)
    rw1, rw2 = a_w * (z1 / (z1 + z2)), a_w * (z2 / (z1 + z2))
    ra1, ra2 = r1 + mn * (1 + x1), r2 + mn * (1 + x2)
    rd1, rd2 = r1 - mn * (1.25 - x1), r2 - mn * (1.25 - x2)
    
    st1 = mt * (math.pi / 2.0 + 2.0 * x1 * math.tan(alpha_n_rad))
    st2 = mt * (math.pi / 2.0 + 2.0 * x2 * math.tan(alpha_n_rad))
    
    inv_at = inv(alpha_t_rad)
    inv_aw_val = inv(aw_rad)
    
    sb1 = rb1 * (st1 / r1 + 2.0 * inv_at)
    sb2 = rb2 * (st2 / r2 + 2.0 * inv_at)
    
    swt1 = rw1 * (st1 / r1 + 2.0 * (inv_at - inv_aw_val))
    swt2 = rw2 * (st2 / r2 + 2.0 * (inv_at - inv_aw_val))
    
    u = z2 / z1
    
    omega1 = 2.0 * math.pi * n1 / 60.0
    omega2 = omega1 / u
    
    delta1, delta2 = ra1**2 - rb1**2, ra2**2 - rb2**2
    if delta1 < 0 or delta2 < 0: return None

    T1T2 = a_w * math.sin(aw_rad)
    T1A, T2B = math.sqrt(delta1), math.sqrt(delta2)
    T2A, T1B = T1T2 - T1A, T1T2 - T2B

    if abs(T1B) < EPS or abs(T2A) < EPS: return None
    
    gs1B = abs(1.0 - (z1 / z2) * (T2B / T1B)) if T1B != 0 else 0
    gs2A = abs((z2 / z1) * (T1A / T2A) - 1.0) if T2A != 0 else 0
    
    vgA = abs(omega1 * T1A - omega2 * T2A)
    vgB = abs(omega1 * T1B - omega2 * T2B)
    
    eps_alpha = (T1A + T2B - T1T2) / pbt
    eps_beta = (b * math.sin(beta_rad)) / pn if beta != 0.0 else 0.0
    
    # Cotas Tangenciais e Larguras (agora totalmente unificadas e blindadas)
    k1, wnk1, wtk1, bmin1 = calcular_k_wk(z1, zv1, x1, mn, alpha_n_rad, alpha_t_rad, beta_rad, cos_betab, sin_betab)
    k2, wnk2, wtk2, bmin2 = calcular_k_wk(z2, zv2, x2, mn, alpha_n_rad, alpha_t_rad, beta_rad, cos_betab, sin_betab)
    
    # ----------------------------------------------------
    # CALIBRES CILÍNDRICOS (MR) E DIÂMETRO (dR)
    # ----------------------------------------------------
    et1 = pt - st1
    et2 = pt - st2
    
    # Eq. 5.34 / 5.35 - Diâmetro Ideal
    dR1_calc = dR1 if dR1 > 0 else et1 * math.cos(alpha_t_rad) * cos_betab
    dR2_calc = dR2 if dR2 > 0 else et2 * math.cos(alpha_t_rad) * cos_betab
    
    inv_aR1 = (st1 / d1) + inv_at + (dR1_calc / (db1 * cos_betab)) - (math.pi / z1)
    aR1 = get_alpha_from_inv(inv_aR1)
    if int(round(z1)) % 2 == 0:
        MR1 = (db1 / math.cos(aR1)) + dR1_calc
    else:
        MR1 = (db1 / math.cos(aR1)) * math.cos(math.pi / (2.0 * z1)) + dR1_calc
        
    inv_aR2 = (st2 / d2) + inv_at + (dR2_calc / (db2 * cos_betab)) - (math.pi / z2)
    aR2 = get_alpha_from_inv(inv_aR2)
    if int(round(z2)) % 2 == 0:
        MR2 = (db2 / math.cos(aR2)) + dR2_calc
    else:
        MR2 = (db2 / math.cos(aR2)) * math.cos(math.pi / (2.0 * z2)) + dR2_calc

    # ----------------------------------------------------
    # INTERFERÊNCIAS
    # ----------------------------------------------------
    zmin_v = 2.0 / (math.sin(alpha_n_rad)**2)
    xlim1, xlim2 = 1.0 - (zv1 / zmin_v), 1.0 - (zv2 / zmin_v)
    int_corte_1 = x1 < xlim1
    int_corte_2 = x2 < xlim2
    
    sin2_at = math.sin(alpha_t_rad)**2
    z1_min_eng = math.sqrt(z2**2 + 4.0*(z2 + 1.0)/sin2_at) - z2
    z2_min_eng = math.sqrt(z1**2 + 4.0*(z1 + 1.0)/sin2_at) - z1

    ramax1 = math.sqrt((a_w**2)*(math.sin(aw_rad)**2) + rb1**2)
    ramax2 = math.sqrt((a_w**2)*(math.sin(aw_rad)**2) + rb2**2)
    
    int_func_1 = ra1 > ramax1
    int_func_2 = ra2 > ramax2

    return {
        "pn": pn, "pt": pt, "pbn": pbn, "pbt": pbt, 
        "zv1": zv1, "zv2": zv2, "betab_deg": betab_deg,
        "a": a, "a_w": a_w, "alpha_t": alpha_t_deg, "aw_deg": aw_deg,
        "mt": mt, "r1": r1, "rw1": rw1, "ra1": ra1, "rd1": rd1, "rb1": rb1, 
        "st1": st1, "st2": st2, "sb1": sb1, "sb2": sb2, "swt1": swt1, "swt2": swt2,
        "r2": r2, "rw2": rw2, "ra2": ra2, "rd2": rd2, "rb2": rb2, 
        "u": u, "eps_alpha": eps_alpha, "eps_beta": eps_beta, "eps_gamma": eps_alpha + eps_beta,
        "gs1B": gs1B, "gs2A": gs2A, "vgA": vgA, "vgB": vgB,
        "T1T2": T1T2, "T1A": T1A, "T2B": T2B, "T2A": T2A, "T1B": T1B,
        "k1": k1, "wnk1": wnk1, "wtk1": wtk1, "bmin1": bmin1,
        "k2": k2, "wnk2": wnk2, "wtk2": wtk2, "bmin2": bmin2,
        "dR1": dR1_calc, "MR1": MR1, "dR2": dR2_calc, "MR2": MR2, "aR1": aR1, "aR2": aR2, "db1": db1, "db2": db2,
        "z_linha": zmin_v, "xlim1": xlim1, "xlim2": xlim2,
        "z1_min_eng": z1_min_eng, "z2_min_eng": z2_min_eng,
        "ramax1": ramax1, "ramax2": ramax2,
        "int_corte_1": int_corte_1, "int_corte_2": int_corte_2,
        "int_func_1": int_func_1, "int_func_2": int_func_2
    }

# ==========================================
# MENUS DESCRITIVOS
# ==========================================
def aguardar():
    input("\n[Pressione Enter para voltar...]")

def menu_inputs():
    global z1, z2, mn, alpha_n, beta, b, x1, x2, aw_imposto, n1
    print("\n--- [ INSERIR OU ALTERAR INPUTS ] ---")
    z1 = ler_input("Dentes do Pinhao (z1) [{0}]: ", z1)
    z2 = ler_input("Dentes da Roda (z2) [{0}]: ", z2)
    mn = ler_input("Modulo Normal (mn) [{0}]: ", mn)
    alpha_n = ler_input("Angulo de Pressao (alpha_n) [{0}]: ", alpha_n)
    beta = ler_input("Angulo de Helice (beta) [{0}]: ", beta)
    b = ler_input("Largura do Dentado (b) [{0}]: ", b)
    x1 = ler_input("Correcao do Pinhao (x1) [{0}]: ", x1)
    x2 = ler_input("Correcao da Roda (x2) [{0}]: ", x2)
    n1 = ler_input("Rotacao do Pinhao n1 (rpm) [{0}]: ", n1)
    aw_imposto = ler_input("Forcar Entre-eixo (0 para Calc. Auto) [{0}]: ", aw_imposto)

def menu_geometricos():
    global dR1, dR2, x1, x2
    while True:
        print("\n--- [ OUTPUTS GEOMETRICOS ] ---")
        print("1. Geometria Geral (Angulos, Eixos e Passos)")
        print("2. Geometria do Pinhao e da Roda (Raios e Espessuras)")
        print("3. Medicao (Wk e Rolos cilindricos)")
        print("4. Analise de Interferencia")
        print("0. Voltar ao Menu Principal")
        opc = input("Escolha uma opcao: ")
        if opc == '0': break
        
        if opc == '3':
            print("\n[ CONFIGURACAO DOS CALIBRES ]")
            dR1 = ler_input("Calibre Pinhao dR1 (0 para Ideal) [{0}]: ", dR1)
            dR2 = ler_input("Calibre Roda dR2 (0 para Ideal) [{0}]: ", dR2)
            
        res = calcular_propriedades()
        if not res: continue

        if opc == '1':
            print("\n[ GEOMETRIA GERAL ]")
            print("Mod. Norm/Apar (mn/mt)  : {0:.4f} / {1:.4f} mm".format(mn, res['mt']))
            print("Ang. Press. (at / aw)   : {0:.4f} / {1:.4f} deg".format(res['alpha_t'], res['aw_deg']))
            print("Ang. Helice (beta / bb) : {0:.4f} / {1:.4f} deg".format(beta, res['betab_deg']))
            print("Eixos Crt/Func (a/aw)   : {0:.4f} / {1:.4f} mm".format(res['a'], res['a_w']))
            print("Passo Norm/Apar (pn/pt) : {0:.4f} / {1:.4f} mm".format(res['pn'], res['pt']))
            print("Passo Base (pbn / pbt)  : {0:.4f} / {1:.4f} mm".format(res['pbn'], res['pbt']))
            print("Dentes Virtuais (zv)    : {0:.2f} e {1:.2f}".format(res['zv1'], res['zv2']))
            aguardar()
        elif opc == '2':
            print("\n[ PINHAO (1) / RODA (2) ]")
            print("Raio Prim. Ref (r) : {0:.4f} / {1:.4f} mm".format(res['r1'], res['r2']))
            print("Raio Prim. Func(rw): {0:.4f} / {1:.4f} mm".format(res['rw1'], res['rw2']))
            print("Raio de Cabeca (ra): {0:.4f} / {1:.4f} mm".format(res['ra1'], res['ra2']))
            print("Raio de Pe (rd)    : {0:.4f} / {1:.4f} mm".format(res['rd1'], res['rd2']))
            print("Raio de Base (rb)  : {0:.4f} / {1:.4f} mm".format(res['rb1'], res['rb2']))
            print("Esp. Corte (st)    : {0:.4f} / {1:.4f} mm".format(res['st1'], res['st2']))
            print("Esp. Func. (swt)   : {0:.4f} / {1:.4f} mm".format(res['swt1'], res['swt2']))
            print("Esp. Base (sb)     : {0:.4f} / {1:.4f} mm".format(res['sb1'], res['sb2']))
            aguardar()
        elif opc == '3':
            print("\n[ MEDICAO COTA TANGENCIAL ]")
            if beta == 0.0:
                print("Pinhao(Wk): {0:.4f} mm (k={1})".format(res['wnk1'], res['k1']))
                print("Roda  (Wk): {0:.4f} mm (k={1})".format(res['wnk2'], res['k2']))
            else:
                print("Pinhao(Wnk | Wtk): {0:.4f} | {1:.4f} mm (k={2})".format(res['wnk1'], res['wtk1'], res['k1']))
                print(" -> Largura min. (b_min1): {0:.4f} mm".format(res['bmin1']))
                print("\nRoda(Wnk | Wtk): {0:.4f} | {1:.4f} mm (k={2})".format(res['wnk2'], res['wtk2'], res['k2']))
                print(" -> Largura min. (b_min2): {0:.4f} mm".format(res['bmin2']))
                if b < res['bmin1'] or b < res['bmin2']:
                    print("  [!] AVISO: A largura b ({0}mm) e inferior ao b_min!".format(b))
            
            input("\n[Pressione Enter para ver Calibres...]")
            print("\n[ CALIBRES CILINDRICOS (MR) ]")
            print("Cal. Pinhao (Mdk1): {0:.4f} mm DM={1:.4f})".format(res['MR1'], res['dR1']))
            print("Ang. alfa_k1: {0:.4f} rad | dk: {1:.4f} ".format(res['aR1'], res['db1']))
            print("Cal. Roda   (Mdk2): {0:.4f} mm (DM={1:.4f})".format(res['MR2'], res['dR2']))
            print("Ang. alfa_k2: {0:.4f} rad | dk: {1:.4f} ".format(res['aR2'], res['db2']))
            print()
            aguardar()
        elif opc == '4':
            print("\n[ INTERFERENCIA DE CORTE ]")
            print("Z' Minimo Teorico: {0:.2f} dentes".format(res['z_linha']))
            print("x_min Pinhao     : {0:.4f} (atual x1={1:.3f})".format(res['xlim1'], x1))
            print("x_min Roda       : {0:.4f} (atual x2={1:.3f})".format(res['xlim2'], x2))
            print("Ocorre Corte?    : PINHAO:{0} | RODA:{1}".format("SIM!" if res['int_corte_1'] else "Nao", "SIM!" if res['int_corte_2'] else "Nao"))
            
            if res['int_corte_1'] or res['int_corte_2']:
                corrigir = input("\nAplicar correcao minima de corte p/ testar (S/N)? ")
                if corrigir.upper() == 'S':
                    if res['int_corte_1']: x1 = res['xlim1']
                    if res['int_corte_2']: x2 = res['xlim2']
                    print("--> Valores de x1 e/ou x2 atualizados!")
                    res = calcular_propriedades() 
                    
            input("\n[Pressione Enter para ver Interf. de Engrenamento...]")
            
            print("\n[ INTERFERENCIA ENGRENAMENTO (TEORICA x=0) ]")
            print("Para z2={0:.0f}, o z1 minimo seria: {1:.2f}".format(z2, res['z1_min_eng']))
            print("Para z1={0:.0f}, o z2 minimo seria: {1:.2f}".format(z1, res['z2_min_eng']))
            
            print("\n[ INTERFERENCIA ENGRENAMENTO (ATUAL com x) ]")
            print("P no Roda (ra1={0:.2f} vs ra_max={1:.2f}): {2}".format(res['ra1'], res['ramax1'], "SIM!" if res['int_func_1'] else "OK"))
            print("R no Pinhao (ra2={0:.2f} vs ra_max={1:.2f}): {2}".format(res['ra2'], res['ramax2'], "SIM!" if res['int_func_2'] else "OK"))
            aguardar()

def menu_cinematicos():
    res = calcular_propriedades()
    if not res: return
    while True:
        print("\n--- [ OUTPUTS CINEMATICOS ] ---")
        print("1. Razoes de Transmissao e Conducao")
        print("2. Escorregamentos Especificos e Velocidades")
        print("0. Voltar ao Menu Principal")
        opc = input("Escolha uma opcao: ")
        if opc == '0': break
        
        if opc == '1':
            print("\n[ RAZOES DE TRANSMISSAO E CONDUCAO ]")
            print("Razao de Multiplicacao (u)  : {0:.4f}".format(res['u']))
            print("Razao de Conducao Perfil    : {0:.4f}".format(res['eps_alpha']))
            print("Razao de Conducao Complem.  : {0:.4f}".format(res['eps_beta']))
            print("Razao de Conducao Total     : {0:.4f}".format(res['eps_gamma']))
            aguardar()
        elif opc == '2':
            print("\n[ ESCORREGAMENTOS MAXIMOS (A e B) ]")
            print("Ponto A (Inicio do Contacto):")
            print("  gs2A (Roda)  : {0:.5f}".format(res['gs2A']))
            print("  Vel. Escorr. : {0:.2f} mm/s".format(res['vgA']))
            print("Ponto B (Fim do Contacto):")
            print("  gs1B (Pinhao): {0:.5f}".format(res['gs1B']))
            print("  Vel. Escorr. : {0:.2f} mm/s".format(res['vgB']))
            aguardar()

def menu_ajuda_calculo():
    res = calcular_propriedades()
    if not res: return
    print("\n--- [ AJUDA DE CALCULO DE ENGRENAMENTO ] ---")
    print("Linha teorica de contacto (T1T2): {0:.4f} mm".format(res['T1T2']))
    print("Ponto A (Inicio, T1A)           : {0:.4f} mm".format(res['T1A']))
    print("Ponto B (Fim, T2B)              : {0:.4f} mm".format(res['T2B']))
    print("Complementar T2A                : {0:.4f} mm".format(res['T2A']))
    print("Complementar T1B                : {0:.4f} mm".format(res['T1B']))
    aguardar()

def menu_correcoes():
    while True:
        print("\n--- [ CALCULAR CORRECOES ] ---")
        print("1. Metodo de Henriot (Igualar gs)")
        print("2. Metodo ISO (Impor aw)")
        print("0. Voltar ao Menu Principal")
        opc = input("Escolha uma opcao: ")
        if opc == '0': break
        
        if opc == '1':
            calcular_correcoes_ideais()
            aguardar()
        elif opc == '2':
            calcular_correcoes_iso()
            aguardar()
        else:
            print("Opcao invalida.")
            aguardar()

def main():
    while True:
        print("\n" + "="*30)
        print("  CALCULADORA DE ENGRENAGENS")
        print("="*30)
        print("1. Inserir ou Alterar Inputs Manuais")
        print("2. Outputs Geometricos e Interferencias")
        print("3. Outputs Cinematicos (Conducao / Escorreg.)")
        print("4. Ajuda de Calculo (Cam. Engrenamento)")
        print("5. Calcular Correcoes (Henriot / ISO)")
        print("0. Sair do Programa")
        
        opc = input("Escolha a opcao: ")
        if opc == '1': menu_inputs()
        elif opc == '2': menu_geometricos()
        elif opc == '3': menu_cinematicos()
        elif opc == '4': menu_ajuda_calculo()
        elif opc == '5': menu_correcoes()
        elif opc == '0': break

if __name__ == "__main__":
    main()