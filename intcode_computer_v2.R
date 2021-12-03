intcode_comp <- function(prog, idx, input = NULL, base) {
  # ABCDE
  # DE - OpCode
  # C  - Parameter 1
  # B  - Parameter 2
  # A  - Parameter 3
  #
  # Parameter: 0 == position mode, 1 == immediate mode (d.h. Wert auslesen)
  opcode <- prog[idx] %% 100
  para_c <- prog[idx] %% 1000 %/% 100
  para_b <- prog[idx] %% 10000 %/% 1000
  para_a <- prog[idx] %% 100000 %/% 10000

  # Parameter vorbereiten
  if (para_c == 0) {
    parameter_1 <- prog[prog[idx + 1] + 1]
  } else if (para_c == 1){
    parameter_1 <- prog[idx + 1]
  } else if (para_c == 2) {
    parameter_1 <- prog[prog[idx + 1] + 1 + base]
  }

  if (para_b == 0) {
    parameter_2 <- prog[prog[idx + 2] + 1]
  } else if (para_b == 1){
    parameter_2 <- prog[idx + 2]
  } else if (para_b == 2) {
    parameter_2 <- prog[prog[idx + 2] + 1 + base]
  }

  if (para_a == 0) {
    target <- prog[idx + 3] + 1
  } else if (para_a == 1) {
    target <- idx + 3
  } else if (para_a == 2) {
    target <- prog[idx + 3] + 1 + base
  }

  if (debug) print(paste0("OpCode: ", opcode))


  if (opcode == 1) {
    # Addition (drei Parameter)
    prog[target] <- parameter_1 + parameter_2

    return(list(prog = prog,
                index = idx + 4,
                input = input,
                breaker = FALSE,
                base = base))

  } else if (opcode == 2) {
    # Multiplikation (drei Parameter)
    prog[target] <- parameter_1 * parameter_2

    return(list(prog = prog,
                index = idx + 4,
                input = input,
                breaker = FALSE,
                base = base))

  } else if (opcode == 3) {
# Eingabe in Zelle schreiben (ein Parameter)
    prog[prog[idx + 1] + 1] <- input

    return(list(prog = prog,
                index = idx + 2,
                input = input,
                breaker = FALSE,
                base = base))

  } else if (opcode == 4) {
# Wert ausgeben (ein Parameter)
    print(paste0("Ausgabe: ", parameter_1))

    return(list(prog = prog,
                index = idx + 2,
                input = input,
                breaker = FALSE,
                base = base))

  } else if (opcode == 5) {
# Jump-if-True (zwei Parameter)
    if (parameter_1 != 0) {
      return(list(prog = prog,
                  index = parameter_2 + 1,
                  input = input,
                  breaker = FALSE,
                  base = base))

    } else {
      return(list(prog = prog,
                  index = idx + 3,
                  input = input,
                  breaker = FALSE,
                  base = base))
    }
  } else if (opcode == 6) {
# Jump-if-False (zwei Parameter)
    if (parameter_1 == 0) {
      return(list(prog = prog, index = parameter_2 + 1, input = input, breaker = FALSE, base = base))
    } else {
      return(list(prog = prog, index = idx + 3, input = input, breaker = FALSE, base = base))
    }
  } else if (opcode == 7) {
# Kleiner-als
    # print(paste0("Parameter 1: ", parameter_1))
    # print(paste0("Parameter 2: ", parameter_2))
    # print(paste0("Kleiner: ", parameter_1 < parameter_2))
    if (parameter_1 < parameter_2) {
        prog[target] <- 1
        } else {
          prog[target] <- 0
          }

    return(list(prog = prog, index = idx + 4, input = input, breaker = FALSE, base = base))
  } else if (opcode == 8) {
# Gleichheit
    # print(paste0("Parameter 1 ", parameter_1))
    # print(paste0("Parameter 2 ", parameter_2))
    # print(paste0("Gleichheit: ", parameter_1 == parameter_2))

    if (parameter_1 == parameter_2) {
      prog[target] <- 1
    } else {
      prog[target] <- 0
    }

    return(list(prog = prog,
                index = idx + 4,
                input = input,
                breaker = FALSE,
                base = base))

  } else if (opcode == 9){
    base <- base + parameter_1

    return(list(prog = prog,
                index = idx + 2,
                input = input,
                breaker = FALSE,
                base = base))

  } else if (opcode == 99) {
# Programm beenden

    message("Programm erfolgreich beendet.")

    return(list(prog = prog,
                index = idx,
                input = input,
                breaker = TRUE,
                base = base))

  } else {

    stop("Fehler!")
  }
}
