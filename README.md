# bfe-upload
This action uploads a network snapshot to a Batfish Enterprise service

## Usage


See [action.yml](action.yml)


## Basic:
```yaml
    steps:

    - name: Checkout this repo
      uses: actions/checkout@v2
      with:
        path: main #to reference files from this repo, the filepath to use will be $GITHUB_WORKSPACE/main

    # Ensure your snapshot directory is organized in the way described at
    # https://batfish.readthedocs.io/en/latest/notebooks/interacting.html#Packaging-snapshot-data
    - name: Create snapshot directory required for Batfish
      run: |
        mkdir -p $GITHUB_WORKSPACE/tmp/configs
        mkdir -p $GITHUB_WORKSPACE/tmp/batfish
        cp $GITHUB_WORKSPACE/main/test-snapshot/configs/*.cfg $GITHUB_WORKSPACE/tmp/configs/
        cp $GITHUB_WORKSPACE/main/test-snapshot/configs/batfish/* $GITHUB_WORKSPACE/tmp/batfish/
        echo "::set-output name=snapshot_dir::$GITHUB_WORKSPACE/tmp/"
      id: prepare_snapshot

    - name: Upload new snapshot to Batfish Enterprise server
      uses: saparikh/bfe-upload@v1.0
      with:
        server_name: demo.intentionet.com
        server_ip: ${{ secrets.BFE_SERVER_IP }}
        snapshot_folder: ${{ steps.prepare_snapshot.outputs.snapshot_dir }}
        network_name: TEST
        snapshot_name: $GITHUB_SHA
        ssl_certificate: ${{ secrets.BFE_SSL_CERTIFICATE }}
      id: upload_snapshot

    - name: Retrieve outputs from BFE upload action
      run: |
        echo ${{ steps.upload_snapshot.outputs.status }}
        echo ${{ steps.upload_snapshot.outputs.url }}
```
## Inputs

### `server_name`

**Required** The name of the server running Batfish Enterprise service

### `server_ip`

The IP address of the server running Batfish Enterprise. This is required if a DNS entry does not exist for the server running Batfish Enterprise

### `server_port`
TCP port on which Batfish Enterprise service is listening. Default: `443`

### `snapshot_folder`
Directory where the new network snapshot is stored

### `network_name`
**Required**  Name of the network used by Batfish Enterprise

### `snapshot_name`
**Required** Name of the snapshot to be created

### `init_snapshot`
Boolean telling the Batfish Enterprise server to initialize (or not) a new snapshot. Default: `yes`

### `ssl_certificate`
**Required** base64 encoded contents of the CA file for SSL certificate installed on Batfish Enterprise server. Run `base64 -i yourCA.pem`. Copy the output into the Github secret `BFE_SSL_CERTIFICATE` of your repository 



# License
The scripts and documentation in this project are released under the [Apache 2.0 License](LICENSE)
