from math import *
#import ti_draw as view
# ----------------
# NUMPY DOSPOBRES
# ----------------

def zeros(rows, cols):
    return [[0.0 for j in range(cols)] for i in range(rows)]

def transpose(A):
    rows = len(A)
    cols = len(A[0])
    return [[A[j][i] for j in range(rows)] for i in range(cols)]

def matrix_mul(A, B):
    rowsA = len(A)
    colsA = len(A[0])
    rowsB = len(B)
    colsB = len(B[0])

    if colsA != rowsB:
        print("Error: Incompatible dimensions")
        return None

    C = zeros(rowsA, colsB)
    for i in range(rowsA):
        for j in range(colsB):
            s = 0.0
            for k in range(colsA):
                s += A[i][k] * B[k][j]
            C[i][j] = s
    return C

def solve_linear_system(A, B):
  
    n = len(A)
    M = [row[:] + [B[i]] for i, row in enumerate(A)]

    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(M[k][i]) > abs(M[max_row][i]):
                max_row = k
        

        M[i], M[max_row] = M[max_row], M[i]

        if abs(M[i][i]) < 1e-12:
            return None # is singular
        pivot = M[i][i]
        for j in range(i, n + 1):
            M[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(i, n + 1):
                    M[k][j] -= factor * M[i][j]

    x = [M[i][n] for i in range(n)]
    return x

# -----------------------
# Formulacao estrutural
# -----------------------
def get_global_member_k(E, A, I, L, angle):
    c1 = E * A / L
    c2 = 12 * E * I / (L**3)
    c3 = 6 * E * I / (L**2)
    c4 = 4 * E * I / L
    c5 = 2 * E * I / L

    k_local = [
        [ c1,  0,   0,  -c1,  0,   0 ],
        [ 0,   c2,  c3,  0,  -c2,  c3],
        [ 0,   c3,  c4,  0,  -c3,  c5],
        [-c1,  0,   0,   c1,  0,   0 ],
        [ 0,  -c2, -c3,  0,   c2, -c3],
        [ 0,   c3,  c5,  0,  -c3,  c4]
    ]

    c = cos(angle)
    s = sin(angle)

    T = [
        [ c,  s,  0,  0,  0,  0],
        [-s,  c,  0,  0,  0,  0],
        [ 0,  0,  1,  0,  0,  0],
        [ 0,  0,  0,  c,  s,  0],
        [ 0,  0,  0, -s,  c,  0],
        [ 0,  0,  0,  0,  0,  1]
    ]

    return matrix_mul(transpose(T), matrix_mul(k_local, T))

def assemble_global_stiffness(nodes, members, dof_map, total_dofs):
    K = zeros(total_dofs, total_dofs)

    for mid in members:
        m = members[mid]
        n1, n2 = m['nodes']

        # Check for missing map
        if n1 not in dof_map or n2 not in dof_map:
            return None

        k = get_global_member_k(
            m['E'], m['A'], m['I'], m['L'], m['angle']
        )

        dofs = dof_map[n1] + dof_map[n2]

        for i in range(6):
            for j in range(6):
                gi = dofs[i]
                gj = dofs[j]
                if gi is not None and gj is not None:
                    K[gi][gj] += k[i][j]

    return K

def assemble_load_vector(members, member_loads, dof_map, total_dofs):
    F = [0.0] * total_dofs
    
    for mid, f_vec in member_loads.items():
        n1, n2 = members[mid]['nodes']
        dofs = dof_map[n1] + dof_map[n2]
        
        for i in range(6):
            g_idx = dofs[i]
            if g_idx is not None:
                F[g_idx] += f_vec[i]  #eralize that this is the reaction vector Qi,0 according to [K]*{d} = {Qi - Qi,0} and should be treating as such in a future global solver 
    return F

# ----------------
# Inputs e edits 
# ----------------

def collect_nodes(current_nodes):
    nodes = current_nodes
    i = 0
    print("\n--- Node Editor ---")
    print("Current: " + str(list(nodes.keys())))
    print("Type 'S' to return.")
   
    while True:
        nid = input("Node Name: ").strip()
        if nid.upper() == 'S':
            break

        if nid in nodes:
            print("Node exists. Overwrite? (y/n)")
            if input().lower() != 'y':
                dof_order = nodes[nid]['dof_order']
                continue


        try:
            x = float(input("  X: "))
            y = float(input("  Y: "))
            if nodes[nid]['dof_order'] == None:
                i +=1 
                dof_order = i
            else:
                continue               
            nodes[nid] = {'x': x, 'y': y, 'dof_order': dof_order}
        except ValueError:
            print("Invalid number.")

    return nodes

def collect_members(nodes, current_members):
    members = current_members
    print("\n--- Member Editor ---")
    print("Current: " + str(list(members.keys())))
    print("Type 'S' to return.")
    
    last_E = None
    last_I = None
    last_A = None

    while True:
        mid = input("Member ID: ").strip()
        if mid.upper() == 'S':
            break

        if mid in members:
            print("Member exists. Overwrite? (y/n)")
            if input().lower() != 'y':
                continue

        n1 = input("  Start Node: ").strip()
        n2 = input("  End Node: ").strip()

        if n1 not in nodes or n2 not in nodes:
            print("Error: Nodes not found.")
            continue

        x1 = nodes[n1]['x']
        y1 = nodes[n1]['y']
        x2 = nodes[n2]['x']
        y2 = nodes[n2]['y']
        
        L = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        if L == 0:
            print("Error: Length is zero.")
            continue
            
        angle = atan2(y2 - y1, x2 - x1)

        try:
            use_last = 'n'
            if last_E is not None:
                msg = "  Use E={:.2e}, I={:.2e}, A={:.2e}? (y/n): ".format(last_E, last_I, last_A)
                use_last = input(msg).strip().lower()

            if use_last == 'y':
                E, I, A = last_E, last_I, last_A
            else:
                E = float(input("  E: "))
                I = float(input("  I: "))
                A = float(input("  A: "))
                last_E, last_I, last_A = E, I, A

            members[mid] = {
                'nodes': (n1, n2),
                'E': E, 'I': I, 'A': A, 'L': L, 'angle': angle
            }
        except ValueError:
            print("Invalid number.")

    return members

def map_custom_dofs(nodes):
    print("\n--- DOF Mapping ---")
    print("Enter 'R' for Restricted, or Integer for DOF.")
    print("Use SAME integer to link nodes (Inextensible).")
    
    dof_map = {}
    max_dof = -1

    node_list = []
    for nid in nodes:
        node_list.append((nodes[nid]['dof_order'], nid))   
    node_list.sort() 

    for node in node_list:
        nid = node[1]
        print("\nNode " + str(nid))
        indices = []
        

        labels = ['u', 'v', 'th']
        for label in labels:
            val = input("  " + label + ": ").strip().upper()
            
            if val == 'R' or val == "":
                indices.append(None)
            else:
                try:
                    idx = int(val)
                    indices.append(idx)
                    if idx > max_dof:
                        max_dof = idx
                except ValueError:
                    indices.append(None)
        
        dof_map[nid] = indices

    return dof_map, max_dof + 1

def plot_structure(nodes, members, dof_map):
    # 1. Safety Checks
    if not nodes:
        print("No nodes to plot.")
        return

    # 2. Setup Screen (318x212 is standard Nspire resolution)
    # 0,0 is usually Top-Left. We will handle the math.
    view.clear()
    
    # 3. Calculate Scale
    # Get all X and Y coordinates
    xs = []
    ys = []
    for nid in nodes:
        xs.append(nodes[nid]['x'])
        ys.append(nodes[nid]['y'])
    
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    
    span_x = max_x - min_x
    span_y = max_y - min_y
    
    # Avoid division by zero
    if span_x == 0: span_x = 1.0
    if span_y == 0: span_y = 1.0
    
    # Margins (keep away from edges)
    margin_x = 20
    margin_y = 20
    screen_w = 318 - (2 * margin_x)
    screen_h = 212 - (2 * margin_y)
    
    # Determine scale (pixels per meter)
    scale_x = screen_w / span_x
    scale_y = screen_h / span_y
    scale = min(scale_x, scale_y) # Maintain aspect ratio
    
    # Centering offsets
    # We want to center the structure in the remaining whitespace
    struct_w_px = span_x * scale
    struct_h_px = span_y * scale
    
    offset_x = margin_x + (screen_w - struct_w_px) / 2
    offset_y = margin_y + (screen_h - struct_h_px) / 2

    # Coordinate Transformer Function
    # NOTE: Screen Y=0 is TOP. Structure Y+ is UP. We must invert Y.
    def to_scr(x, y):
        sx = offset_x + (x - min_x) * scale
        # Invert Y: Max Y structure -> Min Y screen (Top)
        sy = 212 - (offset_y + (y - min_y) * scale) 
        return int(sx), int(sy)

    # 4. Draw Members (Lines)
    view.set_color(0, 0, 255) # Blue
    view.set_pen(2, "solid")   # Thickness 2
    
    for mid in members:
        m = members[mid]
        n1 = m['nodes'][0]
        n2 = m['nodes'][1]
        
        x1, y1 = to_scr(nodes[n1]['x'], nodes[n1]['y'])
        x2, y2 = to_scr(nodes[n2]['x'], nodes[n2]['y'])
        
        view.draw_line(x1, y1, x2, y2)

    # 5. Draw Nodes (Circles + Text)
    view.set_color(0, 0, 0) # Black
    
    for nid in nodes:
        nx, ny = to_scr(nodes[nid]['x'], nodes[nid]['y'])
        
        # Draw Node Circle
        view.fill_circle(nx, ny, 3)
        
        # Prepare Label
        label = str(nid)
        if nid in dof_map:
            # Create short label [0,1,R]
            dofs = dof_map[nid]
            d_str = []
            for d in dofs:
                if d is None: d_str.append("R")
                else: d_str.append(str(d))
            # Join manually (no f-strings)
            label = label + "[" + ",".join(d_str) + "]"
        
        # Draw Text (slightly offset)
        view.draw_text(nx + 5, ny - 10, label)

    print(">> Plot generated.")
    print(">> Check the Python Drawing tab.")  #complety done in AI, do not blindy trust - DOES NOT WORK

# ---------------------
# Inspection funcitons
# ---------------------

def inspect_member(members):
    mid = input("Member ID: ").strip()
    if mid not in members:
        print("Not found.")
        return

    m = members[mid]
    k = get_global_member_k(m['E'], m['A'], m['I'], m['L'], m['angle'])

    print("\nGLOBAL Stiffness Matrix for " + mid)
    print("      u1       v1      th1       u2       v2      th2")
    for row in k:
        line = ""
        for val in row:
            line += "{:8.2e} ".format(val)
        print(line)
    input("Press Enter...")

def calculate_member_loads(members, member_loads):
    print("\n--- Fixed End Moments Calculator ---")
    mid = input("Member ID: ").strip()
    if mid not in members:
        print("Not found.")
        return

    m = members[mid]
    L = m['L']
    angle = m['angle']

    print("Length: {:.2f}m".format(L))
    
    # 1. Initialize an accumulator for the Total Reactions in this session
    r_total = [0.0] * 6 

    # 2. Start the Loop
    while True:
        print("\n--- New Load Case ---")
        print("1: Distributed (q) Down")
        print("2: Point (P) Down")
        typ = input("Type: ").strip()

        # Temporary vector for THIS specific load
        r_step = [0.0] * 6 

        valid_input = False # Flag to check if we should accumulate

        if typ == '1':
            try:
                q = float(input("  q: "))
                # Calculate for this specific q
                r_step[1] = (q*L)/2.0
                r_step[2] = (q*L**2)/12.0
                r_step[4] = (q*L)/2.0
                r_step[5] = -(q*L**2)/12.0
                valid_input = True
            except ValueError:
                print("Invalid number. Try again.")
        
        elif typ == '2':
            try:
                P = float(input("  P: "))
                a = float(input("  Dist 'a': "))
                b = L - a
                if a < 0 or a > L:
                    print("Distance out of range.")
                else:
                    r_step[1] = (P*(b**2)*(L+2*a))/(L**3)
                    r_step[2] = (P*a*(b**2))/(L**2)
                    r_step[4] = (P*(a**2)*(L+2*b))/(L**3)
                    r_step[5] = -(P*(a**2)*b)/(L**2)
                    valid_input = True
            except ValueError:
                print("Invalid number. Try again.")
        
        else:
            print("Invalid Type.")

        # 3. Accumulate (Superposition)
        if valid_input:
            for i in range(6):
                r_total[i] += r_step[i]
            print(">> Load added to stack.")

        # 4. Checkpoint
        cont = input("Wish to add more loads on this member? (y/n): ").strip().lower()
        if cont != 'y':
            break

    # Transform TOTAL Reactions to Global Coordinates
    equiv_local = [val for val in r_total] # Keeping positive (Reactions)
    
    c, s = cos(angle), sin(angle)
    T_T = [[c,-s,0,0,0,0],[s,c,0,0,0,0],[0,0,1,0,0,0],
           [0,0,0,c,-s,0],[0,0,0,s,c,0],[0,0,0,0,0,1]]
    
    f_global = [0.0]*6
    for i in range(6):
        val = 0.0
        for j in range(6):
            val += T_T[i][j] * equiv_local[j]
        f_global[i] = val

    # STORAGE (The overwriting feature works here, at the very end)
    if mid in member_loads:
        print("\nNote: Overwriting previous database entry for " + mid)
    
    member_loads[mid] = f_global
    print(">> Total Combined Loads Stored.")

    # OPTIONAL PRINT
    print("View Total? (L=Local, G=Global, N=No)")
    choice = input("Option: ").strip().upper()

    if choice == 'L':
        print("Total Local Reactions:")
        print(" Start: Fy={:.2f} Mz={:.2f}".format(r_total[1], r_total[2]))
        print(" End  : Fy={:.2f} Mz={:.2f}".format(r_total[4], r_total[5]))
    elif choice == 'G':
        print("Total Global Reactions:")
        print(" Start: {:.2e} {:.2e} {:.2e}".format(f_global[0], f_global[1], f_global[2]))
        print(" End  : {:.2e} {:.2e} {:.2e}".format(f_global[3], f_global[4], f_global[5]))
    
    input("Press Enter...")

# ---------------------
#      MAIN - MENUS
#----------------------

nodes = {}
members = {}
dof_map = {}
member_loads = {}
total_dofs = 0

while True:
    print("\n" + "="*30)
    print("      MAIN MENU")
    print("="*30)
    print("Nodes:{} Members:{} DOFs:{}".format(len(nodes), len(members), total_dofs)) #  no f strings in ti nspire - .format all the way ;) 
    print("-" * 30)
    print("1. Pre-Processing (Nodes/Members/DOFs)")
    print("2. Stiffness Analysis (Matrix K)")
    print("3. Load Calculation (Vector F)")
    print("4. Plot structure - don't use, in dev")
    print("5. Exit")

    main = input("\nOption: ").strip()

    # --- 1. PRE-PROCESSING ---
    if main == '1':
        while True:
            print("\n[PRE-PROCESSING]")
            print("1. Nodes")
            print("2. Members")
            print("3. Map DOFs")
            print("4. Return")
            sub = input("Opt: ").strip()
            
            if sub == '1': nodes = collect_nodes(nodes)
            elif sub == '2': members = collect_members(nodes, members)
            elif sub == '3': dof_map, total_dofs = map_custom_dofs(nodes)
            elif sub == '4': break

    # --- 2. STIFFNESS ---
    elif main == '2':
        while True:
            print("\n[STIFFNESS]")
            print("1. Assemble Global Matrix")
            print("2. Inspect Member")
            print("3. Return")
            sub = input("Opt: ").strip()

            if sub == '1':
                if not dof_map: print("Map DOFs first.")
                else:
                    K = assemble_global_stiffness(nodes, members, dof_map, total_dofs)
                    if K:
                        print("\nGLOBAL MATRIX K:")
                        for row in K:
                            l = ""
                            for v in row: l += "{:>9.2e} ".format(v)
                            print(l)
                        input("Enter...")
            elif sub == '2': inspect_member(members)
            elif sub == '3': break

    # --- 3. LOADS ---
    elif main == '3':
        while True:
            print("\n[LOADS]")
            print("1. Calc Member Loads")
            print("2. Assemble Load Vector")
            print("3. Return")
            sub = input("Opt: ").strip()

            if sub == '1': calculate_member_loads(members, member_loads)
            elif sub == '2':
                if not member_loads: print("Calc loads first.")
                else:
                    F = assemble_load_vector(members, member_loads, dof_map, total_dofs)
                    print("\nGLOBAL VECTOR F:")
                    for i in range(len(F)):
                        print(" DOF {:<2}: {:>10.2e}".format(i, F[i]))
                    input("Enter...")
            elif sub == '3': break
    elif main == '4':
        plot_structure(nodes, members, dof_map)
    # --- 5. EXIT ---
    elif main == '5':
        break