import src.api.wca_api as wca_api
import json

def generate_delegates_list():
    """This writes a local file containing basic delegates info."""

    file_name = "temp/delegates.json"
    delegates_json = wca_api.get_delegates()
    with open(file_name, "w", encoding="utf8") as fout:
        json.dump(delegates_json, fout, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generate_delegates_list()