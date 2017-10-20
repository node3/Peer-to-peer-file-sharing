import json
import os
import time
import records
import utils


def read_rfc_metadata():
    utils.Logging.debug("Entering peer.read_rfc_metadata")
    metadata_file = os.path.join(utils.get_rfc_dir(), "metadata.json")
    # Load metadata.json
    metadata = None
    try:
            try:
                f = open(metadata_file, "r")
                metadata = json.load(f)
                f.close()
            except ValueError as err:
                utils.Logging.info("Could not load %s. %s" % (metadata_file, err))
    except IOError:
        utils.Logging.debug("No %s found" % metadata_file)
    utils.Logging.debug("Exiting peer.read_rfc_metadata")
    return metadata


def update_rfc_metadata(number, title, rfc_format):
    utils.Logging.debug("Entering peer.update_rfc_metadata")
    new_data = {"number": str(number), "title": title, "format": rfc_format}
    metadata_file = os.path.join(utils.get_rfc_dir(), "metadata.json")
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
            rfc = records.RFC("localhost", obj["number"], obj["title"])
            if head:
                head.insert(rfc)
            else:
                head = records.Node(rfc)
    else:
        utils.Logging.info("Metadata empty, no records of local rfcs found")
    utils.Logging.debug("Exiting peer.build_rfc_index")
    return head


def update_rfc_index(rfc_index_head, rfc):
    utils.Logging.debug("Entering peer.build_rfc_index")
    rfc.hostname = "localhost"
    rfc.ttl = "7200"
    if rfc_index_head:
        rfc_index_head.find_and_update(rfc)
    else:
        rfc_index_head = records.Node(rfc)
    utils.Logging.debug("Exiting peer.build_rfc_index")
    return rfc_index_head


def create_data_field(cookie, port):
    return {"cookie": cookie, "port": port}


def periodic_ttl_reduction(head, last_time_updated):
    if head:
        current_time = int(time.time())
        decrement_value = current_time - last_time_updated
        utils.Logging.info("TTL reduction by %s" % decrement_value)
        ptr = head
        while ptr:
            ptr.rfc.decrement_ttl(decrement_value)
            ptr = ptr.nxt


def check_rfc_metadata(rfc_number):
    utils.Logging.debug("Entering peer.check_rfc_metadata")
    metadata = read_rfc_metadata()
    if metadata and metadata["rfcs"]:
        for rfc in metadata["rfcs"]:
            if rfc["number"] == rfc_number:
                return utils.get_rfc_path(rfc)
    utils.Logging.debug("Exiting peer.check_rfc_metadata")
    return None


# Query a peer for its RFC index
def get_rfc_index_from_peer(hostname, port):
    utils.Logging.debug("Entering peer.get_rfc_index_from_peer")
    peer_rfc_index_head = None
    try:
        sock = utils.send_request(hostname, port, "RFCQuery", {})
        response = utils.accept_response(sock)
        if response.status == "200":
            peer_rfc_index_head = records.decode_rfc_list(hostname, response.data)
    except BaseException as err:
        utils.Logging.info(err)
    utils.Logging.debug("Exiting peer.get_rfc_index_from_peer")
    return peer_rfc_index_head


# Get RFC from a peer
def get_rfc_from_peer(peer_ip, peer_port, rfc):
    utils.Logging.debug("Entering peer.get_rfc_from_peer")
    rfc_path = None
    try:
        sock = utils.send_request(peer_ip, peer_port, "GetRFC", {"rfc": rfc.number})
        rfc_path, rfc_format = utils.accept_rfc(sock, rfc.number)
        if rfc_path:
            update_rfc_metadata(rfc.number, rfc.title, rfc_format)
    except BaseException as err:
        utils.Logging.info(err)
    utils.Logging.debug("Exiting peer.get_rfc_from_peer")
    return rfc_path
