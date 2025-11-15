# Flappy Bird Genetic Algorithm AI

This project implements an AI that learns to play Flappy Bird using a genetic algorithm (GA) and a small neural network genome.

## Overview

The system trains a population of birds. Each bird has a simple neural network genome that decides when it should flap. Over generations, birds evolve better behaviors through:

* Fitness-based selection
* Single-point crossover using mask-based mixing
* Random mutation of weights

The project includes two modes:

1. **Interactive game** – a human-controlled bird.
2. **Training simulation** – AI-only environment where many birds train together.

---

## Project Structure

```
├── Bird.py              # Bird physics, rendering, genome usage
├── Pipe.py              # Pipe generation and movement
├── Genome.py            # Neural network and evolutionary operators
├── collision_detection.py# Collision utilities
├── Player_Run.py        # Human-playable game
├── AI_Run.py            # GA training loop
└── README.md
```

---

## Neural Network Genome

Each bird uses a fixed-size neural network with:

* **4 inputs**: bird y-position, vertical velocity, distance to top pipe, distance to bottom pipe
* **Hidden layer**: 6 neurons with ReLU
* **Output layer**: 1 neuron (sigmoid) → flap if output > 0.5

Weights and biases are stored in a **flat genome vector**.

---

## Genetic Algorithm

### Fitness

Bird fitness increases with:

* Survival time
* Passing pipes (+100)

Penalties:

* Wall collision (−100)
* Pipe collision (−50)

### Selection & Reproduction

* Top `elites` birds are kept.
* New birds are produced via masked crossover:

```
child = np.where(mask, parent1.weights, parent2.weights)
```

* Mutation adds Gaussian noise:

```
weights += mask * np.random.randn() * strength
```

---

## Training

Training is run by:

```
train_genome(screen, generations=50, pop_size=100, max_score=5)
```

The max score target increases over time to progressively challenge the population.

Output: The best genome weights.

---

## Running the Game

### Human-controlled

```
python Player_Run.py
```

Press space to flap.

### AI playback using trained weights

```
python AI_Run.py
```

The system loads best weights and runs them in a live simulation.

---

## Requirements

* Python 3.10+
* pygame
* numpy

Install:

```
pip install pygame numpy
```

---

## Notes

* The GA is simple but effective for this environment.
* Increasing population size and generations improves results at cost of speed.
* The genome system allows easy expansion to deeper networks.

---

## License

MIT License.
