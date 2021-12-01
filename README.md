# right-click-save
## Usage
### Package
```python
import right_click_save

for token in right_click_save.get('<ETH-address>', 'ENS-domain'):
    print(token.meta_data)
    print(token.meta_data['name'])
```
### CLI
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