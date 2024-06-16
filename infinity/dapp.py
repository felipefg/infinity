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


BALANCES = {}


def str2hex(str):
    """Encodes a string as a hex string"""
    return "0x" + str.encode("utf-8").hex()

######################################################################
# Register Face
######################################################################


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

    logging.info('Associating face to wallet %s', wallet)
    vdb.add_vector(key=wallet, vector=vec)

    if wallet in BALANCES:
        logging.info('Wallet %s already has a balance of %d. Not modifying.',
                     wallet, BALANCES[wallet])
    else:
        logging.info('Registering balance of %d to wallet %s.',
                     payload.init_balance, wallet)
        BALANCES[wallet] = payload.init_balance

    result = {"status": "ok", "msg": "Success"}
    rollup.report(str2hex(json.dumps(result)))

######################################################################
# Dispense Beer
######################################################################


class DispenseBeerInput(BaseModel):
    op: str
    embedding: str


@json_router.advance({"op": "dispense_beer"})
def handle_dispense_beer(rollup: Rollup, data: RollupData):
    payload = DispenseBeerInput.parse_obj(data.json_payload())
    vec = parse_embedding(payload.embedding)
    match = vdb.get_nearest_key(vec)

    if match is None:
        logging.warning('No matches found for given embedding.')
        rollup.notice(str2hex(json.dumps({})))
        status = {"status": "error", "msg": "No matches found."}
        rollup.report(str2hex(json.dumps(status)))
        return True

    status = {"status": "ok", "msg": "Success"}
    dispense = True

    wallet, distance = match

    if BALANCES[wallet] >= 1:
        balance = BALANCES[wallet] - 1
        BALANCES[wallet] = balance
    else:
        status = {"status": "error", "msg": "Insufficient funds."}
        dispense = False

    resp = {
        "wallet": wallet,
        "distance": distance,
        "balance": balance,
        "dispense": dispense,
    }
    rollup.notice(str2hex(json.dumps(resp)))
    rollup.report(str2hex(json.dumps(status)))
    return True


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
            'balance': BALANCES.get(match[0], -1),
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
