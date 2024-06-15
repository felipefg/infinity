import json
import logging

from cartesi import DApp, Rollup, RollupData, JSONRouter

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
dapp = DApp()
json_router = JSONRouter()
dapp.add_router(json_router)


def str2hex(str):
    """Encodes a string as a hex string"""
    return "0x" + str.encode("utf-8").hex()


@json_router.advance({"op": "register_face"})
def handle_register_face(rollup: Rollup, data: RollupData):
    # TODO: Add face to DB
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
    dapp.run()
