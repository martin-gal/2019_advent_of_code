# Der IntCodeComputer im Redesign als Klasse.


# Die Klasse *IntCodeComputer* verarbeitet das Programm und verschiedene Instanzen des IntCodeComputers
# Parameter
# Inputs
#   programm        Der Programm-Code, der ausgeführt werden soll, als Liste
#   eingabe         Die Eingaben als Liste
#   debug_mode      Der Schalter für den Debug-Mode. Default: False. Unklar, ob der hier verwendet wird.
# Gegeben
#   idx             Der Zustand des Computers, d.h. der Index, an dem als nächstes im Programm gearbeitet wird
#                   Start: 0        
#   ausgabe         Die Ausgaben des Computers als Liste 
#                   Start: leer
#   halt            Der Schalter, ob das Programm angehalten hat (OpCode 99) oder nicht.
#                   Start: False
#   base            Die relative Basis
#                   Start: 0
class IntCodeComputer:

    def __init__(self, programm, eingabe, debug_mode=False):
        self.prog = programm
        self.eingabe = eingabe
        self.debug_mode = debug_mode
        self.idx = 0
        self.ausgabe = []
        self.halt = False
        self.base = 0

    # *run_opcode* führt einen OpCode in einem bestehenden Programm aus
    # Input
    #   programm        Das Programm, das den OpCode enthält
    #   index           Der Index, an dem der OpCode startet, der ausgeführt werden soll (auch: Pointer)
    #   eingabe_index   Der Index der Eingabe, die gerade verarbeitet werden soll
    #   eingabe         Die Liste der Inputs (erster Eintrag: Phase_Setting, zweiter Eintrag: Inputparameter)
    # Output
    #   programm        Das Programm, das ggfs. durch die OpCode-Operation verändert wurde
    #   index           Den Index, der als nächstes angesteuert werden soll
    #   ausgabe         Die Ausgabe, wenn das Programm eine Ausgabe erzeugt hat
    #   eingabe_index   Den Index der Eingabe, die als nächstes verarbeitet werden (ggfs. identisch)
    #   halt            Den Schalter, ob das Programm auf den OpCode 99 gestoßen und damit beendet ist
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
    #                   Beschreibung: Der Wert an dem Ort von p_1 wird ausgegeben und in die Eingabe geschrieben
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
    def run_opcode(self):
        wert = str(self.prog[self.idx]).zfill(5)
        opcode = wert[3:]
        p_1_mode, p_2_mode, p_3_mode = wert[2], wert[1], wert[0]
        if opcode in ['01', '02', '07', '08']:  # Drei Parameter
            a = self.get_data(p_1_mode, 1)
            b = self.get_data(p_2_mode, 2)
            c = self.get_index(p_3_mode, 3)
            if opcode == '01':  # Addition
                self.prog[c] = a + b
            elif opcode == '02':  # Multiplikation
                self.prog[c] = a * b
            elif opcode == '07':  # kleiner als
                self.prog[c] = 1 if a < b else 0
            elif opcode == '08':  # gleich
                self.prog[c] = 1 if a == b else 0
            self.idx += 4
        elif opcode == '03':  # self.eingabe schreiben
            a = self.get_index(p_1_mode, 1)
            self.prog[a] = self.eingabe.pop(0)
            # self.prog[a] = self.eingabe[0]
            # self.eingabe.pop(0)
            self.idx += 2
        elif opcode in ['04', '09']:  # Ein Parameter
            a = self.get_data(p_1_mode, 1)
            if opcode == '04':  # Ausgabe schreiben
                self.ausgabe.append(a)
            elif opcode == '09':  # relative Basis ändern
                self.base += a
            self.idx += 2
        elif opcode in ['05', '06']:  # Zwei Parameter
            a = self.get_data(p_1_mode, 1)
            b = self.get_data(p_2_mode, 2)
            if opcode == '05':  # Springen wenn wahr
                self.idx = b if a != 0 else self.idx + 3
            elif opcode == '06':  # Springen wenn falsch
                self.idx = b if a == 0 else self.idx + 3
        elif opcode == '99':
            self.halt = True
            self.idx += 0
        else:
            # print('Kein gültiger Opcode.')
            raise Exception(f"Unknown opcode: {opcode}")

    # *get_data*        Liefert den Wert eines Parameters des OpCodes in Abhängigkeit Modus
    # Input
    #   modus           Das Kennzeichen, wie der Parameter in dem Index behandelt werden soll (siehe oben)
    #   inc             Der Wert, um den der aktuelle Index (OpCode, Zustand des Programms) erhöht werden muss
    # Output:           Die Funktion gibt den Wert des Parameters zurück
    def get_data(self, modus, inc):
        return self.prog[self.get_index(modus, inc)]

    # *get_index        Liefert den Index, der durch einen Parameter und seinen Modus beschrieben wird
    # Input
    #   modus           Das Kennzeichen, wie der Parameter in dem Index behandelt werden soll (siehe oben)
    #   inc             Der Wert, um den der aktuelle Index (OpCode, Zustand des Programms) erhöht werden muss
    # Output:           Der Index, den der Parameter beschreibt
    def get_index(self, modus, inc):
        if modus == '0':
            self.chkidx(self.prog[self.idx + inc])
            return self.prog[self.idx + inc]
        elif modus == '1':
            self.chkidx(self.idx + inc)
            return self.idx + inc
        elif modus == '2':
            self.chkidx(self.base + self.prog[self.idx + inc])
            return self.base + self.prog[self.idx + inc]
        else:
            raise Exception(f"Unbekannter Modus: {modus}")

    # *chkidx*          Prüft, ob das Programm genug speicher (d. h. ob die Liste lang genug ist) und verlängert diese
    #  Input
    #   idx             Der Index, für den geprüft werden muss, ob er noch im Programm liegt
    def chkidx(self, idx):
        # if len(self.prog) <= self.idx + inc:
        if len(self.prog) <= idx:
            for _ in range(len(self.prog), idx + 1):
                self.prog.append(0)

    # *read_output*     Gibt die Ausgabe des IntCodeComputers zurück
    def read_output(self):
        return self.ausgabe

    # *pop_output*      Entfernt das letzte Element der Ausgabe
    def pop_output(self):
        self.ausgabe.pop()

    # *write_input*     Schreibt den Wert in die Eingabe
    def write_input(self, ipt):
        self.eingabe.append(ipt)

    # *set_value*       Überschreibt einen Wert im Programm
    def set_value(self, idx, value):
        try:
            self.prog[idx] = value
        except IndexError:
            print(f"Index {idx} außerhalb des gültigen Bereichs.")

# ******************************************************************************************************************** #
