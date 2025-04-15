from __future__ import annotations
from typing import NamedTuple, Callable
from collections.abc import ItemsView
import random, itertools, heapq, functools


class Transaction(NamedTuple):
    type: str
    amount: float


with open("input.txt", "r") as f:
    lst = f.readlines()
    register = [
        Transaction(type=x, amount=int(y))
        for x, y in (elem.strip().split() for elem in lst[1:])
    ]
    reg_size = lst[0]


def generate_binary_strings(string_size: int, num_of_strings: int) -> set[str]:
    s = set()
    while len(s) != num_of_strings:
        s.add(bin(random.randint(0, 2**string_size - 1))[2:].zfill(string_size))
    return s


class GA:
    def __init__(self, genotype: set[str], phenotype: list[Transaction]):
        self.genotype = genotype
        self.get_fitness = GA.normalized_fitness(phenotype, 0, 1)
        self.selection_per_generation: int = 0
        self.num_of_combination_for_crossover: int = 0
        self.crossover_point: int = 0
        self.mutation_factor: float = 0
        self.__sequence = ""
        
    def __str__(self):
        return ""

    @staticmethod
    def normalized_fitness(
        phenotypes: list[NamedTuple], fmin: float, fmax: float
    ) -> Callable[[str,], float]:
        normalization_constant: float = fmax - fmin
        offset: float = fmin / normalization_constant

        @functools.lru_cache(maxsize=None)
        def fitness(genotype: str) -> float:
            phenotype = [
                phenotypes[idx]
                for idx, allele in enumerate(genotype)
                if bool(int(allele))
            ]
            if not phenotype:
                return 0
            score = sum(
                elem.amount * (1 if elem.type == "d" else -1) for elem in phenotype
            )
            score = 1 / (1 + abs(score))
            return score / normalization_constant - offset

        return fitness

    def natural_selection(
        self, items: ItemsView[str, float]
    ) -> list[tuple[str, float]]:
        if self.selection_per_generation < 0 and self.selection_per_generation >= len(
            items
        ):
            raise ("Insert a valid number for extracting the n fittest items")
        top_genotypes = heapq.nlargest(
            self.selection_per_generation, items, key=lambda kv: kv[1]
        )
        return top_genotypes

    def crossover(
        self,
        genotype_1: str,
        genotype_2: str,
        crossover_point: int = None,
        move_after_split: bool = True,
    ) -> tuple[str, str]:
        crossover_point = crossover_point or self.crossover_point
        if self.crossover_point >= min(len(genotype_1), len(genotype_2)):
            raise ValueError("Enter valid crossover point")

        substr_to_move = (
            genotype_1[self.crossover_point :]
            if move_after_split
            else genotype_1[: self.crossover_point]
        )
        if not move_after_split:
            genotype_1 = (
                genotype_2[: self.crossover_point] + genotype_1[self.crossover_point :]
            )
            genotype_2 = substr_to_move + genotype_2[self.crossover_point :]
        else:
            genotype_1 = (
                genotype_1[: self.crossover_point] + genotype_2[self.crossover_point :]
            )
            genotype_2 = genotype_2[: self.crossover_point] + substr_to_move

        return genotype_1, genotype_2

    @staticmethod
    def mutation(genotype: str) -> str:
        rand_idx = random.randint(0, len(genotype) - 1)
        mutated_char = "0" if genotype[rand_idx] == "1" else "1"
        return genotype[:rand_idx] + mutated_char + genotype[rand_idx + 1 :]

    def evolution(
        self, generations: int, fitness_function: Callable[..., float] = None
    ) -> str | int:
        if not all(
            [
                self.selection_per_generation,
                self.num_of_combination_for_crossover,
                self.crossover_point,
                self.mutation_factor,
            ]
        ):
            message = (
                f"One or more parameters not initiliazed.\n"
                f"Current values of parameters:\n"
                f"{self.selection_per_generation=}\n"
                f"{self.num_of_combination_for_crossover=}\n"
                f"{self.crossover_point=}\n"
                f"{self.mutation_factor=}"
            )
            print(message)
            return
            
        population = self.genotype
        get_fitness = fitness_function or self.get_fitness
        for _ in range(generations):
            fitness_scores = {
                genotype: get_fitness(genotype) for genotype in population
            }
            top_genotypes = self.natural_selection(fitness_scores.items())
            genotype, max_score = top_genotypes[0]
            if max_score == 1:
                return genotype
            top_genotypes = [elem for elem, _ in top_genotypes]
            combinations = itertools.combinations(top_genotypes, 2)
            sampled_combination = random.sample(list(combinations), 3)

            crossed_over_population = [
                crossed_genotypes
                for args in sampled_combination
                for crossed_genotypes in self.crossover(
                    *args,
                    move_after_split=random.choice([True, False]),
                )
            ]

            next_population = set(top_genotypes).union(set(crossed_over_population))
            population = {
                GA.mutation(elem) if random.random() > self.mutation_factor else elem
                for elem in next_population
            }

        return -1


if __name__ == "__main__":
    initial_population = generate_binary_strings(int(reg_size), 10)
    ga = GA(initial_population, register)
    ga.selection_per_generation = 5
    ga.num_of_combination_for_crossover = 3
    ga.crossover_point = random.choice(range(1, int(reg_size)))
    ga.mutation_factor = 0.4
    print(ga.evolution(20))
