# *run_prog* führt das Programm aus
# Input
#   programm        Das Programm, das bearbeitet werden soll
#   eingabe         Die Eingabe-Parameter
#   base            Die Basis, die im Modus 2 verwendet wird
#   startindex      Der Index, der verwendet werden soll
#   debug_mode      Gibt den aktuellen Durchlauf und den Status des Programms aus, wenn True
# Output
#   prog            Das modifizierte Programm
#   i               Der Index, an dem das Programm gestoppt hat
#   ausgabe         Der Ausgabewert des OpCode 04
#   halt            Der Zustand, ob das Programm angehalten hat oder nicht


def run_prog(prog, eingabe, startindex=0, debug=False, base=0):
    # *run_opcode* führt einen OpCode in einem bestehenden Programm aus
    # Input
    #   programm        Das Programm, das den OpCode enthält
    #   index           Der Index, an dem der OpCode startet, der ausgeführt werden soll (auch: Pointer)
    #   eingabe_index   Der Index der Eingabe, die gerade verarbeitet werden soll
    #   eingabe         Die Liste der Inputs (erster Eintrag: Phase_Setting, zweiter Eintrag: Inputparameter)
    #
    # Output
    #   programm        Das Programm, das ggfs. durch die OpCode-Operation verändert wurde
    #   index           Den Index, der als nächstes angesteuert werden soll
    #   ausgabe         Die Ausgabe, wenn das Programm eine Ausgabe erzeugt hat
    #   eingabe_index   Den Index der Eingabe, die als nächstes verarbeitet werden (ggfs. identisch)
    #   halt            Den Schalter, ob das Programm auf den OpCode 99 gestoßen und damit beendet ist
    #
    # OpCodes haben die Form ABCDE, wobei sie von rechts nach links gelesen werden. Fehlende Stellen entsprechen 0.
    #   A, B, C         Diese Stellen entsprech den Modi für die Verarbeitung von Parametern. Einzelne Opcode können
    #                   maximal drei Parameter besitzen. Die Ausprägungen von A = p_3, B = p_2, C = p_1 sind 0 und 1.
    #       0           Position: Der Wert des Parameter an Stelle index ist die Position des Wertes
    #       1           Wert: Der Wert des Parameters an Stelle index ist der Wert
    #       2           relativer Wert: die relative Basis wird mit dem Wert des Parameters addiert und gibt den neuen
    #                   Index
    #   DE              Der OpCode mit Parametern p_n, n in {1, 2, 3}
    #       01          Name: Addition
    #                   Parameter: 3
    #                   Beschreibung: p_1 + p_2 wird geschrieben an Ort von p_3.
    #       02          Name: Multiplikation
    #                   Parameter: 3
    #                   Beschreibung: p_1 * p_ wird geschrieben an Ort von p_3.
    #       03          Name: Schreibe Eingabe
    #                   Parameter: 1
    #                   Beschreibung: Die Eingabe (aus dem Programm-Input) wird an den Ort von p_1 geschrieben
    #       04          Name: Schreibe Ausgabe
    #                   Parameter: 1
    #                   Beschreibung: Der Wert an dem Ort von p_1 wird ausgegeben
    #       05          Name: Springen (wenn wahr)
    #                   Parameter: 2
    #                   Beschreibung: WENN p_1 != 0, DANN springe zu dem Index gegeben durch p_2
    #       06          Name: Springen (wenn falsch)
    #                   Parameter: 2
    #                   Beschreibung: WENN p_1 == 0, DANN springe zu dem Index gegeben durch p_2
    #       07          Name: Kleiner als
    #                   Parameter: 3
    #                   Beschreibung: WENN p_1 < p_2, DANN schreibe 1 an die Stelle gegeben durch p_3. SONST 0.
    #       08          Name: Gleich
    #                   Parameter: 3
    #                   Beschreibung: WENN p_1 == p_2, DANN schreibe 1 an die Stelle gegeben durch p_3. SONST 0.
    #       09          Name: Basis anpassen
    #                   Parameter: 1
    #                   Beschreibung: Passt die Basis (für Parameter-Modus 2) auf den Wert im Parameter an.
    #       99          Name: Halt
    #                   Parameter: 0
    #                   Beschreibung: Das Programm wird beendet
    def run_opcode(idx):
        loc_base, loc_ausgabe, loc_halt = base, None, False
        wert = str(prog[idx]).zfill(5)
        opcode = wert[3:]
        p_1_mode, p_2_mode, p_3_mode = wert[2], wert[1], wert[0]
        if opcode in ['01', '02', '07', '08']:  # Drei Parameter
            a = get_data(p_1_mode, idx + 1)
            b = get_data(p_2_mode, idx + 2)
            c = get_index(p_3_mode, idx + 3)
            if opcode == '01':      # Addition
                prog[c] = a + b
            elif opcode == '02':    # Multiplikation
                prog[c] = a * b
            elif opcode == '07':    # kleiner als
                prog[c] = 1 if a < b else 0
            elif opcode == '08':    # gleich
                prog[c] = 1 if a == b else 0
            idx += 4
        elif opcode == '03':  # Eingabe schreiben
            a = get_index(p_1_mode, idx + 1)
            prog[a] = eingabe[0]
            eingabe.pop(0)
            idx += 2
        elif opcode in ['04', '09']:    # Ein Parameter
            a = get_data(p_1_mode, idx + 1)
            if opcode == '04':      # Ausgabe schreiben
                loc_ausgabe = a
            elif opcode == '09':    # relative Basis ändern
                loc_base += a
            idx += 2
        elif opcode in ['05', '06']:  # Zwei Parameter
            a = get_data(p_1_mode, idx + 1)
            b = get_data(p_2_mode, idx + 2)
            if opcode == '05':      # Springen wenn wahr
                idx = b if a != 0 else idx + 3
            elif opcode == '06':    # Springen wenn falsch
                idx = b if a == 0 else idx + 3
        elif opcode == '99':
            loc_halt = True
            idx += 0
        else:
            # print('Kein gültiger Opcode.')
            raise Exception(f"Unknown opcode: {opcode}")
        return idx, loc_ausgabe, loc_halt, loc_base

    # *get_data*        Liefert den Wert eines Parameters des OpCodes in Abhängigkeit Modus
    # Input
    #   modus           Das Kennzeichen, wie der Parameter in dem Index behandelt werden soll (siehe oben)
    #   g_idx           Der Index des Parameters
    # Output:           Die Funktion gibt den Wert des Parameters zurück
    def get_data(modus, g_idx):
        return prog[get_index(modus, g_idx)]

    # *get_index        Liefert den Index, der durch einen Parameter und seinen Modus beschrieben wird
    # Input
    #   modus           Das Kennzeichen, wie der Parameter in dem Index behandelt werden soll (siehe oben)
    #   g_idx           Der Index des Parameters
    # Output:           Der Index, den der Parameter beschreibt
    def get_index(modus, g_idx):
        if modus == '0':
            chkidx(prog[g_idx])
            return prog[g_idx]
        elif modus == '1':
            chkidx(g_idx)
            return g_idx
        elif modus == '2':
            chkidx(base + prog[g_idx])
            return base + prog[g_idx]
        else:
            raise Exception(f"Unbekannter Modus: {modus}")

    # *chkidx*          Prüft, ob das Programm genug speicher (d. h. ob die Liste lang genug ist) und verlängert diese
    #  Input
    #   c_inx           Der Index, der angesteuert werden soll und ggfs. nicht in der Liste ist
    def chkidx(c_idx):
        if len(prog) <= c_idx:
            for _ in range(len(prog), c_idx + 1):
                prog.append(0)

    # Initialisiere Programm
    index = startindex  # Startindex des Programms
    if debug:  # Zähler für den Debug-Modus
        zaehler = 1
        print(f"0:\t {prog} \t {index}")
    while index < len(prog):
        index, ausgabe, halt, base = run_opcode(index)
        if halt:
            print('Angehalten') if debug else False
            return prog, index, ausgabe, halt
            # break
        if ausgabe is not None:
            print(f"Ausgabe: {ausgabe}")
        if debug:  # Durchlauf, Programmzustand, nächster Index
            print(f"{zaehler}:\t {prog} \t {index}")
            zaehler += 1
