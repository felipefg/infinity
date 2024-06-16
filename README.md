# Infinity

See the frontend and device parts at https://github.com/MarcosGaius/infinitylock

## Running on Host Mode

After you have set up a virtual environment with all the packages in requirements.txt installed, you can run the project in host mode by opening two terminal windows and following the procedure below:

In the first terminal window, instruct the Cartesi CLI to run everything without the backend:

```shell
cartesi run --no-backend
```

In the second window, execute the application by running the following command from the repository root:

```shell
ROLLUP_HTTP_SERVER_URL="http://localhost:8080/host-runner" python -m infinity.dapp
```

In Host Mode, the DApp code will run in your native machine, allowing you to quickly iterate over the development. It is however unsuitable to deploy to a real blockchain.

> [!NOTE]
> There is no need to run `cartesi build` if you are executing the application in Host Mode via `cartesi run --no-backend`.

## Building

To build the DApp, run:

```shell
cartesi build
```

To test the DApp in production mode, in a local test chain, run:

```shell
cartesi run
```
