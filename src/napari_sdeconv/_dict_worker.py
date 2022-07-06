import inspect
from ._framework import SNapariWorker


class SDictWorker(SNapariWorker):
    """Create a napari worker from a dictionary

    Parameters
    ----------
    metadata: dict
        Dictionary describing the plugin metadata
    """
    def __init__(self, metadata):
        super().__init__()
        self.metadata = metadata

    def run(self):
        # run
        params = self._state['inputs'].copy()
        fnc_args = inspect.getfullargspec(self.metadata['fnc'])
        if 'observers' in fnc_args.args:
            params['observers'] = self._observers
        outputs_values = self.metadata['fnc'](**params)

        # copy outputs references to the dictionary
        if len(self._state['outputs'].keys()) == 1:
            outputs_values = [outputs_values]

        for i, key in enumerate(self._state['outputs'].keys()):
            self._state['outputs'][key]['data'] = outputs_values[i].detach().cpu().numpy()

        print('outputs dict = ', self._state['outputs'])

        self.finished.emit()
