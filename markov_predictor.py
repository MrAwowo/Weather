import numpy as np
from collections import defaultdict
import random

class WeatherMarkovChain:
    """
    Markov Chain model for weather prediction
    Uses temperature ranges and weather conditions to predict future weather
    """

    def __init__(self, order=2):
        """
        Initialize Markov Chain
        order: the number of previous states to consider (default: 2 for second-order)
        """
        self.order = order
        self.temp_transitions = defaultdict(lambda: defaultdict(int))
        self.condition_transitions = defaultdict(lambda: defaultdict(int))
        self.trained = False

    def _discretize_temperature(self, temp):
        """Convert continuous temperature to discrete state"""
        if temp < 0:
            return "freezing"
        elif temp < 10:
            return "cold"
        elif temp < 20:
            return "mild"
        elif temp < 30:
            return "warm"
        else:
            return "hot"

    def train(self, historical_data):
        """
        Train the Markov chain on historical data
        historical_data: list of dicts with 'temp' and 'condition' keys
        """
        if len(historical_data) < self.order + 1:
            raise ValueError(f"Need at least {self.order + 1} data points to train")

        # Extract temperature states and conditions
        temp_states = [self._discretize_temperature(d["temp"]) for d in historical_data]
        conditions = [d["condition"] for d in historical_data]

        # Build transition matrices
        for i in range(len(temp_states) - self.order):
            # Create state tuple from previous states
            current_state = tuple(temp_states[i:i + self.order])
            next_state = temp_states[i + self.order]

            self.temp_transitions[current_state][next_state] += 1

        for i in range(len(conditions) - self.order):
            current_state = tuple(conditions[i:i + self.order])
            next_state = conditions[i + self.order]

            self.condition_transitions[current_state][next_state] += 1

        self.trained = True

    def _get_next_state(self, current_state, transition_matrix):
        """Get next state based on current state and transition probabilities"""
        if current_state not in transition_matrix:
            # If we haven't seen this state, return a random common state
            all_states = [state for states in transition_matrix.values() for state in states.keys()]
            if all_states:
                return random.choice(all_states)
            return None

        # Get transition counts
        next_states = transition_matrix[current_state]
        total = sum(next_states.values())

        # Convert to probabilities
        probabilities = {state: count / total for state, count in next_states.items()}

        # Sample next state based on probabilities
        states = list(probabilities.keys())
        probs = list(probabilities.values())

        return random.choices(states, weights=probs)[0]

    def predict(self, recent_data, days=7):
        """
        Predict future weather based on recent data
        recent_data: list of recent weather observations (at least 'order' days)
        days: number of days to predict
        """
        if not self.trained:
            raise ValueError("Model must be trained before prediction")

        if len(recent_data) < self.order:
            raise ValueError(f"Need at least {self.order} recent observations")

        # Initialize with recent states
        recent_temps = [self._discretize_temperature(d["temp"]) for d in recent_data[-self.order:]]
        recent_conditions = [d["condition"] for d in recent_data[-self.order:]]

        predictions = []

        for _ in range(days):
            # Predict temperature state
            temp_state = tuple(recent_temps[-self.order:])
            next_temp_state = self._get_next_state(temp_state, self.temp_transitions)

            # Predict condition
            condition_state = tuple(recent_conditions[-self.order:])
            next_condition = self._get_next_state(condition_state, self.condition_transitions)

            # Convert temperature state back to numeric value
            temp_map = {
                "freezing": -5,
                "cold": 5,
                "mild": 15,
                "warm": 25,
                "hot": 35
            }
            predicted_temp = temp_map.get(next_temp_state, 15) + random.uniform(-3, 3)

            predictions.append({
                "temp_state": next_temp_state,
                "temp": round(predicted_temp, 1),
                "condition": next_condition if next_condition else "Clear"
            })

            # Update recent states for next iteration
            recent_temps.append(next_temp_state)
            recent_conditions.append(next_condition if next_condition else "Clear")

        return predictions

    def get_transition_probabilities(self, state_type="temp"):
        """Get transition probability matrix for visualization"""
        transitions = self.temp_transitions if state_type == "temp" else self.condition_transitions

        prob_matrix = {}
        for current_state, next_states in transitions.items():
            total = sum(next_states.values())
            prob_matrix[current_state] = {
                state: count / total for state, count in next_states.items()
            }

        return prob_matrix
