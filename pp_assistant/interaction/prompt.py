import logging
from typing import Tuple


class UserPrompter:
    def __init__ (self):
        self.logger = logging.getLogger(__name__)
    

    def ask_workspace_grid(self) -> Tuple[int, int]:
        self.logger.info('Workspace split configuration:')
        n_rows = self._prompt_positive_number('number of rows', interruptable = False)
        n_cols = self._prompt_positive_number('number of columns', interruptable = False)
        return n_rows, n_cols

    def ask_evaluation_cells(self) -> list[int]:
        self.logger.info('Specify the cells you want to hold out for evaluation')
        self.logger.info('Press "Enter" when finished')

        cell_ids = []
        while True:
            cell_id = self._prompt_positive_number('cell ID', interruptable = True)

            if not cell_id:
                break
            
            cell_ids.append(cell_id)
        
        return cell_ids

    
    def _prompt_positive_number(self, label: str, interruptable: bool = False):
        while True:
            raw = input(f'Enter {label}: ').strip()

            if interruptable and raw == '':
                return
            
            try:
                value = int(raw)
            except ValueError as e:
                self.logger.error('Please enter a valid integer.')
                continue

            if value <= 0:
                self.logger('Value must be a positive integer')
                continue

            return value