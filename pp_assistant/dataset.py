import os
import json
import logging
from pp_assistant.workspace import Workspace
from pp_assistant.episode import Episode


class Dataset:
    def __init__(self, name: str, workspace: Workspace, episodes: list[Episode] = None):
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.workspace = workspace
        self.episodes = episodes if episodes is not None else []
    
    def save(self, dir: str):
        os.makedirs(dir, exist_ok=True)

        # Save meta info
        meta_path = os.path.join(dir, 'info.json')

        data = {
            'version': 1,
            'dataset': self._to_dict()
        }

        with open(meta_path, 'w') as f:
            json.dump(data, f, indent = 2)
        
        # Save episode configs
        episodes_path = os.path.join(dir, 'episodes.json')
        self._save_episodes(path = episodes_path)

    
    def _save_episodes(self, path):
        if self.episodes:
            self.logger.warning('No episodes to save')

        data = [e.__dict__ for e in self.episodes]

        with open(path, 'w') as f:
            json.dump(data, f)
        
        self.logger.info('Episodes saved')

    def _to_dict(self):
        return {
            'workspace': self.workspace.to_dict()
        }
    

