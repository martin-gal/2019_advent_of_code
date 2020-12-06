# Advent of Code 2019: Day 14
library(tidyverse)
library(magrittr)
library(data.table)
library(lubridate)
library(glue)

test <- read_lines("10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL")

# Part 1
# Given the list of reactions in your puzzle input, what is the minimum amount
# of ORE required to produce exactly 1 FUEL?


incred <- str_extract_all(test, "(?<=\\d{1,2}\\s)\\w{1,4}", simplify = TRUE) %>%
  as.vector() %>%
  unique()
incred <- incred[incred != '']

test %>%
  as.data.frame() %>%
  separate(., col=`.`, into=c('input', 'output'), sep='=>')

