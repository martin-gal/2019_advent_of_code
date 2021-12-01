intcode_comp <- function(prog, idx, input = NULL) {
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
  }

  if (para_b == 0) {
    parameter_2 <- prog[prog[idx + 2] + 1]
  } else if (para_b == 1){
    parameter_2 <- prog[idx + 2]
  }

  if (debug) print(paste0("OpCode: ", opcode))

# Addition (drei Parameter)
  if (opcode == 1) {
    if (para_a == 0) {
      prog[prog[idx + 3] + 1] <- parameter_1 + parameter_2
    } else if (para_a == 1){
      prog[idx + 3] <- parameter_1 + parameter_2
    }

    return(list(prog = prog, index = idx + 4, breaker = FALSE))
  } else if (opcode == 2) {
# Multiplikation (drei Parameter)
    if (para_a == 0) {
      prog[prog[idx + 3] + 1] <- parameter_1 * parameter_2
    } else if (para_a == 1){
      prog[idx + 3] <- parameter_1 * parameter_2
    }

    return(list(prog = prog, index = idx + 4, breaker = FALSE))
  } else if (opcode == 3) {
# Eingabe in Zelle schreiben (ein Parameter)
    prog[prog[idx + 1] + 1] <- input
    return(list(prog = prog, index = idx + 2, breaker = FALSE))
  } else if (opcode == 4) {
# Wert ausgeben (ein Parameter)
    print(paste0("Ausgabe: ", parameter_1))

    return(list(prog = prog, index = idx + 2, breaker = FALSE))
  } else if (opcode == 5) {
# Jump-if-True (zwei Parameter)
    if (parameter_1 != 0) {
      return(list(prog = prog, index = parameter_2 + 1, breaker = FALSE))
    } else {
      return(list(prog = prog, index = idx + 3, breaker = FALSE))
    }
  } else if (opcode == 6) {
# Jump-if-False (zwei Parameter)
    if (parameter_1 == 0) {
      return(list(prog = prog, index = parameter_2 + 1, breaker = FALSE))
    } else {
      return(list(prog = prog, index = idx + 3, breaker = FALSE))
    }
  } else if (opcode == 7) {
# Kleiner-als
    # print(paste0("Parameter 1: ", parameter_1))
    # print(paste0("Parameter 2: ", parameter_2))
    # print(paste0("Kleiner: ", parameter_1 < parameter_2))

    if (para_a == 0) {
      if (parameter_1 < parameter_2) {
        prog[prog[idx + 3] + 1] <- 1
      } else {
        prog[prog[idx + 3] + 1] <- 0
      }
    } else if (para_a == 1){
      if (parameter_1 < parameter_2) {
        prog[idx + 3] <- 1
      } else {
        prog[idx + 3] <- 0
      }
    }

    return(list(prog = prog, index = idx + 4, breaker = FALSE))
  } else if (opcode == 8) {
# Gleichheit
    # print(paste0("Parameter 1 ", parameter_1))
    # print(paste0("Parameter 2 ", parameter_2))
    # print(paste0("Gleichheit: ", parameter_1 == parameter_2))

    if (para_a == 0) {
      if (parameter_1 == parameter_2) {
        prog[prog[idx + 3] + 1] <- 1
      } else {
        prog[prog[idx + 3] + 1] <- 0
      }
    } else if (para_a == 1){
      if (parameter_1 == parameter_2) {
        prog[idx + 3] <- 1
      } else {
        prog[idx + 3] <- 0
      }
    }

    return(list(prog = prog, index = idx + 4, breaker = FALSE))
  } else if (opcode == 99) {
# Programm beenden
    message("Programm erfolgreich beendet.")
    return(list(prog = prog, index = idx, breaker = TRUE))
  } else {
    stop("Fehler!")
  }
}
