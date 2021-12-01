# Advent of Code 2019
# Day 9

library(tidyverse)

input <- read_csv("aoc_data/day_9_test_1.csv.csv",
                  col_names = FALSE)

# Teil 1
vec <- input %>%
  slice(1) %>%
  as.numeric()

source("intcode_computer_v2.R")
