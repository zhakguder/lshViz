import os
from data_file import DatasetFile
from data_reader import DataReader
from label_reader import LabelReader
from raw_vector_reader import RawVectorReader

RAW_DATA_FILE = "../examples/mnist/mnist_train.csv"


class MnistReader(DataReader):
    def __init__(self, input_file=RAW_DATA_FILE, name="mnist"):
        super().__init__(input_file)
        self.name = name

    def _prepare_raw_data(self):
        dataset_file = DatasetFile(
            vector="mnist_train_feature", label="mnist_train_labels"
        )
        commands_ = [
            "mkdir -p",
            "wget https://pjreddie.com/media/files/mnist_train.csv -O",
            f"cut -d, -f2- {self.input_file} >",
            f"cut -d, -f1 {self.input_file} >",
        ]

        output_paths = [
            "../examples/mnist",
            self.input_file,
            f"{self.output_dir}/{dataset_file.vector}",
            f"{self.output_dir}/{dataset_file.label}",
        ]

        commands = []
        for i, val in enumerate(zip(commands_, output_paths)):
            command, output_path = val
            if not os.path.exists(output_path):
                commands.append(f"{command} {output_path}")

        for command in commands:
            os.system(command)

        self.raw_vector_reader = RawVectorReader(
            f"{self.output_dir}/{dataset_file.vector}"
        )
        self.label_reader = LabelReader(f"{self.output_dir}/{dataset_file.label}")


if __name__ == "__main__":
    from ipdb import set_trace

    reader = MnistReader()
