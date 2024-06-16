import json
import logging

from pydantic import BaseModel
from cartesi import DApp, Rollup, RollupData, JSONRouter

from .model import model, format_embedding
from .vector_db import vdb, parse_embedding

LOGGER = logging.getLogger(__name__)
dapp = DApp()
json_router = JSONRouter()
dapp.add_router(json_router)


def str2hex(str):
    """Encodes a string as a hex string"""
    return "0x" + str.encode("utf-8").hex()


class RegisterFaceInput(BaseModel):
    op: str
    wallet: str
    embedding: str
    init_balance: int = 10


@json_router.advance({"op": "register_face"})
def handle_register_face(rollup: Rollup, data: RollupData):
    payload = RegisterFaceInput.parse_obj(data.json_payload())

    wallet = payload.wallet.lower()
    vec = parse_embedding(payload.embedding)

    vdb.add_vector(key=wallet, vector=vec)

    # TODO register balance

    result = {"status": "ok", "msg": "Mock Implementation Successful"}
    rollup.report(str2hex(json.dumps(result)))


@json_router.advance({"op": "dispense_beer"})
def handle_dispense_beer(rollup: Rollup, data: RollupData):
    # TODO: Match face and dispense beer

    match = {
        "wallet": "0xdeadbeef9d603c29af07a9b54b13f3e2deadbeef",
        "distance": 0.35,
        "balance": 9,
        "dispense": True
    }
    rollup.notice(str2hex(json.dumps(match)))

    result = {"status": "ok", "msg": "Mock Implementation Successful"}
    rollup.report(str2hex(json.dumps(result)))


class DetectFaceInput(BaseModel):
    op: str
    image: str


@json_router.inspect({"op": "detectface"})
def handle_detectface(rollup: Rollup, data: RollupData) -> bool:

    payload = DetectFaceInput.parse_obj(data.json_payload())

    face = model.transform(payload.image)
    embedding = format_embedding(face['embedding'])

    match = vdb.get_nearest_key(face['embedding'])

    resp_match = None

    if match is not None:
        resp_match = {
            'wallet': match[0],
            'distance': match[1],
            'balance': 123
        }

    response = {
        "pixels": face['box'][-1] * face['box'][-2],
        "confidence": face['confidence'],
        "embedding": embedding,
        "match": resp_match
    }
    rollup.report(str2hex(json.dumps(response)))
    return True


# Default routes, in case any of the above match
@dapp.advance()
def handle_advance(rollup: Rollup, data: RollupData) -> bool:
    payload = data.str_payload()
    LOGGER.debug("Echoing '%s'", payload)
    rollup.notice(str2hex(payload))
    rollup.notice(str2hex("Voce disse: " + payload))
    return True


@dapp.inspect()
def handle_inspect(rollup: Rollup, data: RollupData) -> bool:
    payload = data.str_payload()
    LOGGER.debug("Echoing '%s'", payload)
    rollup.report(str2hex(payload))
    return True


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-22s %(levelname)-8s %(message)s',
    )
    dapp.run()
