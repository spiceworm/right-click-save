# right-click-save
## Usage
### Package
```python
import right_click_save

for token in right_click_save.get('<ETH-address>', 'ENS-domain'):
    print(token.metadata)
    print(token.metadata['name'])
```
### Development Environments
#### virtualenv
Using a virtual environment is more convenient for development because dependencies
do not need to be re-installed each time the source code changes as is the case with
the docker environment.
```bash
$ virtualenv -p python3.10 ~/venv/right-click-save
$ . ~/venv/right-click-save/bin/activate
$ pip install -e /path/to/right-click-save
$ right-click-save --help
```
#### docker
Copy this to /usr/local/bin/right-click-save
```bash
#!/usr/bin/env bash

set -e

NAME=right-click-save
REPO_PATH=/<change-this-to-local-repo-root-directory>/

pushd $REPO_PATH > /dev/null

# Capture version defined in source code
VERSION=$(
python << SCRIPT
d = {}
with open('right_click_save/__version__.py') as f:
    exec(f.read(), d)
print(d['__version__'])
SCRIPT
)

# Build and tag image
docker build . -t $NAME:$VERSION &> /dev/null
docker tag $NAME:$VERSION $NAME:latest

# Run container
docker run --rm -it $NAME:$VERSION "$@"

popd > /dev/null
```
```bash
$ chown $USER:USER /usr/local/bin/right-click-save
$ chmod +x /usr/local/bin/right-click-save
```
#### Invoke executable to run package in docker container
```bash
$ right-click-save <ETH-address> [<ETH-address>] [<ENS-domain>]
```

## TODO
* Add interactive mode where you can choose which of the NFTs to actually save to disk
* Save NFT image/mp4/metadata to file
  * display image/mp4/metadata in terminal?
* Add tests