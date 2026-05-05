import os
import json
import logging
from pp_assistant.workspace.workspace import Workspace
from pp_assistant.dataset.episode import Episode


META_FILE = "info.json"
EPISODES_FILE = 'episodes.json'


class Dataset:
    def __init__(self, name: str, workspace: Workspace, episodes: list[Episode] = None):
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.workspace = workspace
        self.episodes = episodes if episodes is not None else []

    
    def save(self, dir: str):
        self.logger.info(f'Saving "{self.name}" dataset to {dir}')
        os.makedirs(dir, exist_ok=True)

        # Save meta info
        meta_path = os.path.join(dir, META_FILE)

        data = {
            'version': 1,
            'dataset': self._to_dict()
        }

        with open(meta_path, 'w') as f:
            json.dump(data, f, indent = 2)
        
        # Save episode configs
        episodes_path = os.path.join(dir, EPISODES_FILE)
        self._save_episodes(path = episodes_path)

    
    @classmethod
    def from_json(cls, path: str) -> 'Dataset':
        # Check if path exists
        if not os.path.exists(path):
            raise ValueError(f'Path {path} doesn\'t exist')

        # Deserialize the dataset
        meta_path = os.path.join(path, META_FILE)
        with open(meta_path, 'r') as f:
            data = json.load(f)
        
        workspace = Dataset.from_dict(data.get('dataset'))

        # Deserialize the episodes

        # Instantiate the class and return it
        return workspace


    @classmethod
    def from_dict(cls, data) -> "Dataset":
        return cls(
            name = data.get('name'),
            workspace = Workspace.from_dict(data.get('workspace'))
        )

    
    def _save_episodes(self, path):
        if not self.episodes:
            self.logger.info('No episodes to save')
            return

        data = [e.__dict__ for e in self.episodes]

        with open(path, 'w') as f:
            json.dump(data, f)
        
        self.logger.info('Episodes saved')

    def _to_dict(self):
        return {
            'workspace': self.workspace.to_dict()
        }
    

