import os
import utils
import records
import json


def get_rfc_dir():
    rfc_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rfc")
    if not os.path.exists(rfc_dir):
        os.makedirs(rfc_dir)
    return rfc_dir


def read_rfc_metadata():
    metadata_file = os.path.join(get_rfc_dir(), "metadata.json")
    # Load metadata.json
    try:
        with open(metadata_file) as f:
            try:
                return json.load(f)
            except ValueError as err:
                utils.Logging.info("Could not load %s. %s" % (metadata_file, err))
                return None
    except OSError:
        utils.Logging.info("No %s found" % metadata_file)
        return None


def build_rfc_index():
    metadata = read_rfc_metadata()
    if metadata:
        head = None
        for obj in metadata["rfcs"]:
            rfc = records.RFC(obj["number"], obj["title"], "localhost")
            rfc_node = records.RFCs(rfc)
            head = rfc_node.prepend(head)
        return head
    else:
        utils.Logging.info("Metadata empty, no records of local rfcs found")
