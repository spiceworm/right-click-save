# right-click-save
## Usage
### Package
```python
import right_click_save

for token in right_click_save.get('<ETH-address>', 'ENS-domain'):
    print(token.meta_data)
    print(token.meta_data['name'])
```
### Development Environment
#### Create executable
```bash
$ cat << EOF >> /usr/local/bin/right-click-save
#!/usr/bin/env bash

set -e

NAME=right-click-save

pushd /path/to/repo/$NAME/ > /dev/null

# Build image if any changes have been made to the source code
docker build . -t $NAME &> /dev/null

# Run container
docker run --rm -it $NAME "$@"

popd > /dev/null
EOF

$ chown $USER:USER /usr/local/bin/right-click-save
$ chmod +x /usr/local/bin/right-click-save
```
#### Invoke executable to run package in docker container
```bash
$ right-click-save <ETH-address> [<ETH-address>] [<ENS-domain>]
```

## TODO
* For some reason the erc721 subgraph is not including ENS NFTs
  * `right-click-save <ENS-domain>` does not retrieve tokens for ENS domain but DOES get other NFTs
* Add interactive mode where you can choose which of the NFTs to actually save to disk
* Save NFT image/mp4/metadata to file
  * display image/mp4/metadata in terminal?
* Add tests