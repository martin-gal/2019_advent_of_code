# Advent of Code 2019
# Day 9

library(tidyverse)

input <- read_csv("aoc_data/day_9.csv",
                  col_names = FALSE)

# Teil 1
vec <- input %>%
  slice(1) %>%
  as.numeric()

source("intcode_computer_v2.R")

debug <- TRUE


output <- list(prog = vec, index = 1, input = 1, base = 0)

# Schleife starten
while(TRUE) {
  output <- intcode_comp(
    output[["prog"]],
    output[["index"]],
    output[["input"]],
    output[["base"]]
    )

  output[["prog"]][is.na(output[["prog"]])] <- 0

  if (output[["breaker"]]) { break }
}
