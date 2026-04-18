import logging
from typing import Tuple


class UserPrompter:
    def __init__ (self):
        self.logger = logging.getLogger(__name__)
    

    def ask_workspace_grid(self) -> Tuple[int, int]:
        self.logger.info('Workspace split configuration:')
        n_rows = self._prompt_positive_number('number of rows')
        n_cols = self._prompt_positive_number('number of columns')
        return n_rows, n_cols

    
    def _prompt_positive_number(self, label: str):
        while True:
            raw = input(f'Enter {label}: ').strip()
            
            try:
                value = int(raw)
            except ValueError as e:
                self.logger.error('Please enter a valid integer.')
                continue

            if value <= 0:
                self.logger('Value must be a positive integer')
                continue

            return value