# Royal Cut: grid defense as a minimum-cut problem in Python

Royal Cut computes the minimum troop cost needed to block every route from a map's boundary to its capital. A grid becomes a directed flow network, and a BFS-based augmenting-path algorithm computes the maximum flow corresponding to the minimum cut.

## 1. Project information

- **Institution:** Universidade Federal de Minas Gerais (UFMG)
- **Degree:** Ciência da Computação
- **Course:** Algoritmos 1
- **Assignment:** Trabalho Prático 2
- **Semester:** 2025-01

The assignment's central modeling challenge is charging for defending a location, rather than for blocking a road between locations. Each traversable grid cell is split into entry and exit vertices connected by an edge whose capacity is its troop requirement.

Mountain cells are excluded. Infinite-capacity edges connect neighboring cells, a super-source represents invasions from the boundary, and the capital connects to the sink. The delivered command-line solver prints the resulting minimum defense cost.

## 2. How to run

Prerequisite: Python 3.9 or newer, as specified by the assignment. The implementation uses built-in language facilities without external packages. From the repository root:

```sh
python3 main.py
```

Standard input contains the row and column counts, the integer-valued grid rows, and the capital's row and column. The entered capital coordinates are one-based; the program converts them to zero-based indexes. A grid value of zero represents an impassable mountain.

The solver prints one integer: the minimum troop cost. Input must follow the assignment's grid format and specify a traversable capital.

## 3. Usage example

Example 01 from the assignment supplies the complete input through standard input:

```sh
python3 main.py <<'EOF'
5 7
9 1 1 1 9 9 9
9 0 9 1 1 1 9
9 0 9 50 9 1 9
9 1 1 1 9 1 9
9 9 9 1 9 9 9
3 4
EOF
```

This describes a five-row, seven-column map with the capital at row 3, column 4. No separate input file is required for this example.

## 4. Implementation decisions

- **Vertex capacities through splitting:** the entry-to-exit edge makes cutting a location incur that cell's cost, while movement edges preserve adjacency without adding a competing finite cost.
- **Boundary and capital connections:** the super-source connects to each traversable boundary cell's entry vertex. The capital's exit vertex connects to the sink. Its finite entry-to-exit edge remains in the network, so defending the capital itself is a possible cut.
- **Sequential vertex identifiers:** a dictionary maps cell coordinates and entry/exit type to compact graph identifiers.
- **Residual capacities:** each added edge receives a reverse adjacency and an initially zero reverse capacity. Augmentation subtracts capacity along the selected path and adds it in reverse.
- **BFS augmenting paths:** parent pointers reconstruct each source-to-sink path, identify its bottleneck, and guide residual updates until the sink becomes unreachable.

## 5. Tests and evaluation

### Verified results

Reference output provided in the assignment for Example 01:

```text
13
```

The reference states that 13 soldiers suffice for the minimum-cost defense of this map.

The repository includes the implementation and its technical report, but no automated test suite or versioned input fixtures.

## 6. Learning and limitations

The project develops the connection between a problem reduction and the algorithm that solves the reduced problem. Splitting locations into two vertices is the key step that makes a standard flow calculation express a defense cost. Reverse edges then make it possible to revise earlier routing choices as new augmenting paths appear.

The implementation retains only the final cost in its public output; it does not print the defended cells forming a cut. Its BFS queue uses list removal from the front, which adds overhead compared with a queue supporting constant-time removal.
