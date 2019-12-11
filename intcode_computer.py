

# run_opcode führt einen OpCode in einem bestehenden Programm aus
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
#   A, B, C         Diese Stellen entsprech den Handles für die Verarbeitung von Parametern. Einzelne Opcode können
#                   maximal drei Parameter besitzen. Die Ausprägungen von A = p_3, B = p_2, C = p_1 sind 0 und 1.
#       0           Position: Der Wert des Parameter an Stelle index ist die Position des Wertes
#       1           Wert: Der Wert des Parameters an Stelle index ist der Wert
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
#       99          Name: Halt
#                   Parameter: 0
#                   Beschreibung: Das Programm wird beendet
def run_opcode(programm, index, eingabe_index, eingabe):
    ausgabe = None
    wert = str(programm[index]).zfill(5)
    opcode = wert[3:]
    p_1_mode, p_2_mode, p_3_mode = wert[2], wert[1], wert[0]
    halt = False
    if opcode == '01':  # Addition
        programm[programm[index + 3]] = zugriff(programm, p_2_mode, (index + 2)) \
                                        + zugriff(programm, p_1_mode, (index + 1))
        return programm, (index + 4), ausgabe, eingabe_index, halt
    elif opcode == '02':  # Multiplikation
        programm[programm[index + 3]] = zugriff(programm, p_2_mode, (index + 2)) \
                                        * zugriff(programm, p_1_mode, (index + 1))
        return programm, (index + 4), ausgabe, eingabe_index, halt
    elif opcode == '03':  # Eingabe schreiben
        programm[programm[(index + 1)]] = eingabe[eingabe_index]
        return programm, (index + 2), ausgabe, 1 if eingabe_index == 0 else 1, halt
    elif opcode == '04':  # Ausgabe schreiben
        ausgabe = zugriff(programm, p_1_mode, index + 1)
        # print(f"Ausgabe: {ausgabe}")
        return programm, (index + 2), ausgabe, eingabe_index, halt
    elif opcode == '05':  # Springen wenn wahr
        if zugriff(programm, p_1_mode, index + 1) != 0:
            # print(f"05: {zugriff(programm, p_2_mode, index + 2)}")
            return programm, zugriff(programm, p_2_mode, index + 2), ausgabe, eingabe_index, halt
        else:
            return programm, index + 3, ausgabe, eingabe_index, halt
    elif opcode == '06':  # Springen wenn falsch
        if zugriff(programm, p_1_mode, index + 1) == 0:
            # print(f"06: {zugriff(programm, p_2_mode, index + 2)}")
            return programm, zugriff(programm, p_2_mode, index + 2), ausgabe, eingabe_index, halt
        else:
            return programm, index + 3, ausgabe, eingabe_index, halt
    elif opcode == '07':  # Kleiner als
        if zugriff(programm, p_1_mode, index + 1) < zugriff(programm, p_2_mode, index + 2):
            programm[programm[index + 3]] = 1
        else:
            programm[programm[index + 3]] = 0
        return programm, index + 4, ausgabe, eingabe_index, halt
    elif opcode == '08':  # Gleich
        if zugriff(programm, p_1_mode, index + 1) == zugriff(programm, p_2_mode, index + 2):
            programm[programm[index + 3]] = 1
        else:
            programm[programm[index + 3]] = 0
        return programm, index + 4, ausgabe, eingabe_index, halt
    elif opcode == '99':
        halt = True
        return programm, index, ausgabe, eingabe_index, halt
    else:
        # print('Kein gültiger Opcode.')
        raise Exception(f"Unknown opcode: {opcode}")


# zugriff liefert den Wert eines Parameters des OpCodes in Abhängigkeit von dem Switch
# Input
#   programm        Das Programm, das gerade bearbeitet wird
#   handle          Das Kennzeichen, wie der Parameter in dem Index behandelt werden soll (siehe oben)
#   index           Der Index des Parameters
# Output:           Die Funktion gibt den Wert des Parameters zurück
def zugriff(programm, handle, index):
    if handle == '0':
        return programm[programm[index]]
    else:
        return programm[index]


# run_prog führt das Programm aus
# Input
#   programm        Das Programm, das bearbeitet werden soll
#   eingabe         Die Eingabe-Parameter
#   startindex      Der Index, der verwendet werden soll
#   debug_mode      Gibt den aktuellen Durchlauf und den Status des Programms aus, wenn True
# Output
#   prog            Das modifizierte Programm
#   i               Der Index, an dem das Programm gestoppt hat
#   ausgabe         Der Ausgabewert des OpCode 04
#   halt            Der Zustand, ob das Programm angehalten hat oder nicht
def run_prog(programm, eingabe, startindex=0, debug_mode=False):
    # Initialisiere Programm
    i = startindex                  # Startindex des Programms
    eingabe_index = 0               # Erste Eingabe
    prog = programm.copy()          # Kopie des Programms, die in der Funktion verwendet wird
    if debug_mode:                  # Zähler für den Debug-Modus
        zaehler = 1
    while i < len(prog):
        prog, i, ausgabe, eingabe_index, halt = run_opcode(prog, i, eingabe_index, eingabe)
        if halt:
            print('Angehalten') if debug_mode else False
            return prog, 0, ausgabe, halt
            # break
        if ausgabe is not None:
            return prog, i, ausgabe, halt
            # return prog, ausgabe, halt
        if debug_mode:  # Durchlauf, Programmzustand, nächster Index
            print(f"{zaehler}:\t {prog} \t {i}")
            zaehler += 1
