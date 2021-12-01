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
