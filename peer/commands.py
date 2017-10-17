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
    utils.Logging.debug("Entering peer.read_rfc_metadata")
    metadata_file = os.path.join(get_rfc_dir(), "metadata.json")
    # Load metadata.json
    data = None
    try:
        with open(metadata_file) as f:
            try:
                data = json.load(f)
            except ValueError as err:
                utils.Logging.info("Could not load %s. %s" % (metadata_file, err))
    except OSError:
        utils.Logging.info("No %s found" % metadata_file)
    utils.Logging.debug("Exiting peer.read_rfc_metadata")
    return data


def update_rfc_metadata(number, title):
    utils.Logging.debug("Entering peer.update_rfc_metadata")
    new_data = {"number".encode('utf-8'): str(number), "title".encode('utf-8'): title}
    metadata_file = os.path.join(get_rfc_dir(), "metadata.json")
    try:
        metadata = read_rfc_metadata()
        if metadata and isinstance(metadata, dict):
            metadata["rfcs"].append(new_data)
        else:
            metadata = {"rfcs": []}
            metadata["rfcs"].append(new_data)
        f = open(metadata_file, "w")
        json.dump(metadata, f)
        f.close()
        updated = True
    except BaseException as err:
        updated = False
        utils.Logging.debug(err)
    utils.Logging.debug("Exiting peer.update_rfc_metadata")
    return updated


def build_rfc_index():
    utils.Logging.debug("Entering peer.build_rfc_index")
    metadata = read_rfc_metadata()
    head = None
    if metadata:
        for obj in metadata["rfcs"]:
            rfc = records.RFC(obj["number"], obj["title"], "localhost")
            rfc_node = records.Node(rfc)
            head = rfc_node.insert(head)
    else:
        utils.Logging.info("Metadata empty, no records of local rfcs found")
    utils.Logging.debug("Exiting peer.build_rfc_index")
    return head


def create_data_field(cookie, port):
    return {"cookie": cookie, "port": port}

