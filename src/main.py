import numpy as np
from time import time, sleep


states = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8}
symbols = dict(zip(states.values(), states.keys()))

def check(grid_state):
    ids = set(range(9))
    for i in range(3):
        for j in range(3):
            if not (set(grid_state[i, j, :, :].reshape(9)) == set(grid_state[:, :, i, j].reshape(9)) == set(grid_state[i, :, j, :].reshape(9)) == ids):
                return 1
    return 0

def ani_solve(grid, delay=0.25):
    status = 0
    print(grid)
    while status == 0:
        sleep(delay)
        status = grid.collapse()
        print(f"\033[11A{grid}")

class Grid:
    def __init__(self, file_path=None):
        self.grid_states=np.full((3, 3, 3, 3, 9), 1, dtype=np.bool)
        self.grid_state = np.full((3, 3, 3, 3), -1, dtype=np.int8)

        if type(file_path) == str:
            self.read_file(file_path)
        elif file_path != None:
            raise Exception("File path must be a string.")

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "\n───┼───┼───\n".join([
            "\n".join([
                "│".join([
                    "".join([
                        symbols[state_id] if state_id > -1 else "▯"
                        for state_id in mini_col])
                    for mini_col in col])
                for col in mini_row])
            for mini_row in self.grid_state])

    def read_file(self, file_path):
        with open(file_path, "r") as file:
            raw_data = file.read()
        concise_raw_data = raw_data.replace("\n", "")

        if len(concise_raw_data) != 81:
            raise Exception("File does not contain a valid grid state.")

        for index, symbol in enumerate(concise_raw_data):
            m_row = index // 27
            row = index // 9 % 3
            m_col = index % 9 // 3
            col = index % 3
            if symbol in states:
                state_id = states[symbol]
                self.set(m_row, row, m_col, col, state_id)
    
    def set(self, m_row, row, m_col, col, state_id):
        self.grid_states[m_row, row, :, :, state_id] = 0
        self.grid_states[:, :, m_col, col, state_id] = 0
        self.grid_states[m_row, :, m_col, :, state_id] = 0
        self.grid_states[m_row, row, m_col, col] = 0
        self.grid_state[m_row, row, m_col, col] = state_id

    def collapse(self):
        grid_states_amt = self.grid_states.sum(axis=-1)
        collapsable_grid = grid_states_amt == 1
        collapsable = collapsable_grid.sum() > 0
        solved = (grid_states_amt == 0).all()
        if solved:
            return 1
        if not collapsable:
            return 2

        collapsable_grid_states = self.grid_states * collapsable_grid.reshape(3, 3, 3, 3, 1)
        m_rows, rows, m_cols, cols, state_ids = np.where(collapsable_grid_states)
        self.set(m_rows, rows, m_cols, cols, state_ids)
        return  0

    def solve(self, branch=1):
        status = 0
        while status == 0:
            status = self.collapse()
        if status == 1:
            print(f"\n\n\nSolved:\n{self}\n\n\n")
        if status == 2 and branch:
            grid_states_amt = self.grid_states.sum(axis=-1)
            max_state_amt = grid_states_amt.max()
            rows, cols = np.where(grid_states_amt == max_state_amt)
            row, col = rows[0], cols[0]

if __name__ == "__main__":
    grid = Grid("../puzzles/1.puz")
    print(f"Puzzle:\n{grid}\n")
    start = time()
    grid.solve()
    duration = time() - start
    correct = "INCORRECT" if check(grid.grid_state) else "CORRECT"
    print(f"It took {duration} seconds to solve. Evaluated: {correct}")
