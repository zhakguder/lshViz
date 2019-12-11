import pickle
import json
import pprint
from config import LshConfig
from ipdb import set_trace


def load_hashed_dataset():

    with open("config.json", "r") as f:
        options = json.load(f)
    options_tmp = {int(key): value for key, value in options.items()}
    options_str = pprint.pformat(options_tmp)
    model_choice = input(f"{options_str}\n 0: Skip load and create new hash\n")

    process_types = ["embedded_", "hashed_", ""]
    if int(model_choice):  # 0 creates a new hash dataset
        for process_type in process_types:
            try:
                config = options[model_choice]
                with open(process_type + config["_pickle_name"], "rb") as f:
                    ds = pickle.load(f)
                ds.config = LshConfig(config=config)
                print(f"OPENING {process_type[:-1]} DATASET")
                return ds
            except:
                pass
    else:
        return None


if __name__ == "__main__":
    load_hashed_dataset()
