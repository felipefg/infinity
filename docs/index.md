# Infinity DApp

This document describes the operations supported by the Cartesi DApp for the
Infinity Beer Dispenser project.

## Recognize Face (Inspect)

Run the face extraction model and return information for the largest face in the image.

**Input**: The raw image file, as bytes, should be sent as a POST request. JPEG or PNG should be fine.

**Outputs**:

- Report 0: Description of the largest face in the image. Will be a JSON object with the following keys:
  - `pixels` (integer): Total number of pixels (width * height) of this face in the original image
  - `confidence` (float): Confidence of the model on the detection of this face
  - `embedding` (string): A base64 representation of the 512-dimensions embedding of the face
  - `match` (object or `null`): A match with an existing wallet, if found. The fields are:
    - `wallet`: Wallet address
    - `balance`: Wallet balance

## Register Face (Advance)

Create a new association between a face and a wallet.

**Input**: JSON object with the following fields:

- `op` (string): Literal `register_face`
- `embedding` (string): Base64 representation of the person's embedding. This should be exactly as the inspect request returned
- `wallet` (string): Wallet address
- `init_balance` (integer): Initial balance for this wallet.

Example:

```json
{
    "op": "register_face",
    "embedding": "fSybkwQs...Iw==",
    "wallet": "0xbee5001DDe65c627516D2Cf77e047E91C3861F0e",
    "init_balance": 10,
}
```

**Output**:

- Report 0:
  - If everything goes as expected: `{"status": "ok", "msg": "Success"}`
  - In case of error: `{"status": "error", "msg": "Error message"}`

## Dispense Beer (Advance)

Match the face with a known wallet, and subtract one for the balance

**Input**: JSON object with the following fields:

- `op` (string): Literal `dispense_beer`
- `embedding` (string): Base64 representation of the person's embedding. This should be exactly as the inspect request returned

Example:

```json
{
    "op": "dispense_beer",
    "embedding": "fSybkwQs...Iw==",
}
```

**Output**:

- Notice 0: JSON with the following fields:
  - `wallet` (string): Matched wallet address
  - `distance` (float): Distance of the matched vector
  - `balance` (int): New balance after this operation
  - `dispense` (bool): True or False if the beer should be dispensed.

- Report 0:
  - If everything goes as expected: `{"status": "ok", "msg": "Success"}`
  - In case of error: `{"status": "error", "msg": "Error message"}`

**Restriction**:
This endpoint should only be called by the operator. It will be restricted to his wallet's address.
