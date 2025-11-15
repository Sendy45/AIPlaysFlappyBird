from __future__ import annotations
import numpy as np

class Genome:
    def __init__(self, input_len: int, hidden_len: int, output_len: int):
        # NN dimensions
        self.input_len = input_len
        self.hidden_len = hidden_len
        self.output_len = output_len

        # Weights and biases
        # -1 -> 1
        w1 = np.random.uniform(low=-1, high=1, size=(input_len, hidden_len))
        b1 = np.random.uniform(low=-1, high=1, size=hidden_len)
        w2 = np.random.uniform(low=-1, high=1, size=(hidden_len, output_len))
        b2 = np.random.uniform(low=-1, high=1, size=output_len)

        # flatten everything → one array
        self.weights = np.concatenate([
            w1.flatten(),
            b1,
            w2.flatten(),
            b2
        ])

    # Split the flat array to weights and biases
    def to_network(self):
        i = self.input_len
        h = self.hidden_len
        o = self.output_len

        w1 = self.weights[:i*h].reshape(i, h)
        b1 = self.weights[i*h:i*h+h]
        w2 = self.weights[i*h+h:i*h+h*2].reshape(h, o)
        b2 = self.weights[i*h+h*2:]

        return w1, b1, w2, b2

    # Put inputs into the NN and get output
    def forward(self, x: "np.array"):
        w1, b1, w2, b2 = self.to_network()

        # hidden layer activation
        hidden = np.maximum(0, np.dot(x, w1) + b1) # Relu
        # Output layer activation
        output = 1 / (1 + np.exp(-np.maximum(0, np.dot(hidden, w2) + b2))) # Sigmoid

        return output[0] # 0 - 1

    # Mutate genomes weights
    def mutate(self, mutation_rate=0.05, mutation_strength=0.05):
        weights = self.weights
        mask = np.random.rand(len(weights)) < mutation_rate # Boolean array - for weights in True -> mutate
        noise = np.random.randn(len(weights)) * mutation_strength # Float array (0-1) - the added noise to weights
        self.weights = weights + mask * noise # Add the noise for weights in True

    # Create child from 2 genomes by crossover
    @staticmethod
    def crossover(parent1: Genome, parent2: Genome):
        mask = np.random.rand(len(parent1.weights)) < 0.5 # Boolean array, half true half false
        # True - picks parent1 weights
        # False - picks parent1 weights
        child = np.where(mask, parent1.weights, parent2.weights)
        return child


