import numpy as np


grid_row_amt = 9
grid_col_amt = 9
grid_cell_amt = grid_row_amt * grid_col_amt
states = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8}
symbols = dict(zip(states.values(), states.keys()))
states_amt = len(states)
grid_shape = (grid_row_amt, grid_col_amt)
grid_states_shape = (grid_row_amt, grid_col_amt, states_amt)


class Grid:
    def __init__(self, file_path=None):
        self.grid_states = np.full(grid_states_shape, 1, dtype=np.bool)
        self.grid_states_amt = np.full(grid_shape, 9, dtype=np.int8)
        self.grid_state = np.full(grid_shape, -1, dtype=np.int8)

        if type(file_path) == str:
            self.read_file(file_path)
        elif file_path is not None:
            raise Exception("File path must be a string.")

    def __repr__(self):
        return str(self)

    def __str__(self):
        group_grid = self.grid_state.reshape(3, 3, 3, 3)
        return "\n───┼───┼───\n".join([
            "\n".join([
                "│".join([
                    "".join([
                        symbols[state_id] if state_id > -1 else "▯"
                        for state_id in mini_col])
                    for mini_col in col])
                for col in mini_row])
            for mini_row in group_grid])

    def read_file(self, file_path):
        with open(file_path, "r") as file:
            raw_data = file.read()
        concise_raw_data = raw_data.replace("\n", "")

        if len(concise_raw_data) is not grid_cell_amt:
            raise Exception("File does not contain a valid grid state.")

        for index, symbol in enumerate(concise_raw_data):
            row = index // grid_row_amt
            col = index % grid_row_amt
            if symbol in states:
                state_id = states[symbol]
                self.set(row, col, state_id)
    
    def set(self, row, col, state_id):
        self.grid_states_amt[row, :] -= self.grid_states[row, :, state_id]
        self.grid_states[row, :, state_id] = 0
        self.grid_states_amt[:, col] -= self.grid_states[:, col, state_id]
        self.grid_states[:, col, state_id] = 0

        self.grid_states_amt[row, col] = 0
        self.grid_states[row, col] = 0
        self.grid_state[row, col] = state_id

    def collapse(self):
        collapsable_grid = self.grid_states_amt == 1
        collapsable = collapsable_grid.sum() > 0
        if not collapsable:
            return 0

        collapsable_grid_states = self.grid_states * collapsable_grid.reshape(9, 9, 1)
        rows, cols, state_ids = np.where(collapsable_grid_states)
        self.set(rows, cols, state_ids)
        return  1


if __name__ == "__main__":
    grid = Grid("../1.puz")
    print(f"Puzzle:\n{grid}\n")
    collapsable = 1
    collapses = 0
    while collapsable:
        collapsable = grid.collapse()
        collapses += 1
        print(f"Collapse {collapses}:\n{grid}\n")
    print("No longer collapsable, multiple possible states for all remaining cells.")
