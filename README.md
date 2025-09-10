# Print Shop Game

This repository contains a simple simulation of a print shop used for unit
exercise purposes.

## Assets

Game resources such as audio clips, images, and fonts live under the
[`assets/`](assets) directory.  Access to these resources should go through the
[`AssetLoader`](assets/loader.py) helper which resolves paths relative to this
folder:

```python
from assets.loader import AssetLoader

loader = AssetLoader()
print(loader.audio("bell.wav"))
```

The directory structure currently includes subfolders for `audio`, `images`
and `fonts` – additional categories can be added as needed.

## Running the demo

A minimal command-line interface is provided via `main.py`. Launch the script
with Python and then enter commands at the prompt:

```bash
python main.py
```

Available commands allow you to spawn machines, add customers and progress
active jobs. A short example session:

```text
> spawn printer
> add copy 5
> process printer
> progress 100
Completed copy
```
