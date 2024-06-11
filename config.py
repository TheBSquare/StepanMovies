
import os


# resources
RESOURCES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources")
HISTORY_PATH = os.path.join(RESOURCES_PATH, "history.json")


if not os.path.isdir(RESOURCES_PATH):
    os.mkdir(RESOURCES_PATH)

if not os.path.isfile(HISTORY_PATH):
    with open(HISTORY_PATH, "w") as f:
        f.write("[]")
