import logging
from typing import Tuple


class UserPrompter:
    def __init__ (self, n_rows: int = 2, n_cols: int = 3):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.logger = logging.getLogger(__name__)
    

    def ask_workspace_grid(self) -> Tuple[int, int]:
        self.logger.info('Workspace splig configuration:')
        n_rows = self._prompt_positive_number('number of rows', self.n_rows)
        n_cols = self._prompt_positive_number('number of columns', self.n_cols)
        return n_rows, n_cols

    
    def _prompt_positive_number(self, label: str, default: str):
        while True:
            raw = input(f'Enter {label} [{default}]: ').strip()

            if raw == '':
                return default
            
            try:
                value = int(raw)
            except ValueError as e:
                self.logger.error('Please enter a valid integer.')
                continue

            if value <= 0:
                self.logger('Value must be a positive integer')
                continue

            return value