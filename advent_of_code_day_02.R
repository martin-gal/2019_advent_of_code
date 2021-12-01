# Advent of Code 2019
# Day 2

library(tidyverse)

input <- read_csv("aoc_data/day_2_1.csv",
                  col_names = FALSE)

# Teil 1
vec <- input %>%
  slice(1) %>%
  as.numeric()

vec_test <- c(1,9,10,3,2,3,11,0,99,30,40,50)

opcode <- function(prog, idx) {
# Addition
  if (prog[idx] == 1) {
    prog[prog[idx + 3] + 1] <- prog[prog[idx + 1] + 1] + prog[prog[idx + 2] + 1]
    return(list(prog, idx + 4))
  } else if (prog[idx] == 2) {
# Multiplikation
    prog[prog[idx + 3] + 1] <- prog[prog[idx + 1] + 1] * prog[prog[idx + 2] + 1]
    return(list(prog, idx + 4))
  } else if (prog[idx] == 99) {
# Programm beenden
    return(list(prog, idx))
  } else {
    message("Fehler")
  }
}

# Startwerte setzen
vec[2] <- 12
vec[3] <- 2
output <- list(vec, 1)

# Schleife starten
while(TRUE) {
  output <- opcode(output[[1]], output[[2]])
  if (output[[1]][[output[[2]]]] == 99) { break }
}

# Ausgabe anschauen
output[[1]][[1]]

# Teil 2
# Welche Inputs erzeugen 19690720?

memory <- vec

for (i in 0:99) {
  # Speicher wiederherstellen
  vec <- memory
  for (k in 0:99) {
    # Startwerte setzen
    vec[2] <- i
    vec[3] <- k

    # Programm initialisieren
    output <- list(vec, 1)

    # Schleife starten
    while(TRUE) {
      output <- opcode(output[[1]], output[[2]])
      if (output[[1]][[output[[2]]]] == 99) { break }
    }

    # Schleifen unterbrechen
    if (output[[1]][[1]] == 19690720) { break }
  }
  # Schleifen unterbrechen
  if (output[[1]][[1]] == 19690720) { break }
}

# Ausgabe schreiben
print(100 * i + k)

