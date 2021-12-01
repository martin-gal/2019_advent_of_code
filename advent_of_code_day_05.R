# Advent of Code 2019
# Day 5

library(tidyverse)

input <- read_csv("aoc_data/day_5.csv",
                  col_names = FALSE)

# Teil 1
vec <- input %>%
  slice(1) %>%
  as.numeric()

source("intcode_computer_v2.R")

output <- list(prog = vec, index = 1, input = 1)
debug <- FALSE


# Schleife starten
while(TRUE) {
  output <- intcode_comp(output[["prog"]], output[["index"]], output[["input"]])
  # print(output[["index"]])
  if (output[["breaker"]]) { break }
}

# Ausgabe anschauen
output[["index"]]

# Teil 2
source("intcode_computer_v2.R")
vec <- c(3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
         1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
         999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99)
debug <- FALSE

output <- list(prog = vec, index = 1, input = 5)

# Schleife starten
while(TRUE) {
  output <- intcode_comp(output[["prog"]], output[["index"]], output[["input"]])
  if (output[["breaker"]]) { break }
}

