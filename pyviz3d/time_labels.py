"""Labels class e.g. to visualize the labels of instances."""
import numpy as np


class TimeLabels:
    """Set of labels."""

    def __init__(self, labels, positions, colors, visible, time):
        self.labels = labels
        self.positions = positions
        self.colors = colors
        self.visible = visible
        self.time = time

    def get_properties(self, binary_filename):
        """ Get arrow properties, they are written into json and interpreted by javascript.
        :return: A dict conteining object properties.
        """

        positions = np.array(self.positions)
        colors = np.array(self.colors)
        time = np.array(self.time)

        json_dict = {
            'type': 'timelabels',
            'labels': self.labels,
            'positions': positions.tolist(),
            'colors': colors.tolist(),
            'time': time.tolist(), 
            'visible': self.visible,
        }
        return json_dict

    def write_binary(self, path):
        """Write lines to binary file."""
        return

    def write_blender(self, path):
        print(type(self).__name__+'.write_blender() not yet implemented.' )
        return