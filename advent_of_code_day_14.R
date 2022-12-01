# Advent of Code 2019
# Day 14: Space Stoichiometry ----
library(tidyverse)


test <- read_lines("10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL")

# Part 1
# Given the list of reactions in your puzzle input, what is the minimum amount
# of ORE required to produce exactly 1 FUEL?


incred <-
  test %>%
  str_extract_all("(?<=\\d{1,2}\\s)\\w{1,4}", simplify = TRUE) %>%
  as.vector() %>%
  unique()

incred <- incred[incred != ""]

test %>%
  as.data.frame() %>%
  separate(., col = ".", into = c("input", "output"), sep = "=>")


liste <- list("FUEL" = c("A" = 7, "E" = 1))

incred
