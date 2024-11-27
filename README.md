Simplified version of https://github.com/blaisewf/rvc-cli
# Instructions
* Put this in `rvc/models/predictors/rmvpe.pt`
  * https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/rmvpe.pt?download=true
* Put this in `/rvc/models/embedders/contentvec/pytorch_model.bin`
  * https://huggingface.co/IAHispano/Applio/resolve/main/Resources/embedders/contentvec/pytorch_model.bin
* Put this in `/rvc/models/embedders/contentvec/config.json`
  * https://huggingface.co/IAHispano/Applio/resolve/main/Resources/embedders/contentvec/config.json

# Usage
```bash
python rvc_cli.py infer --pth_path custom.pth --index_path custom.index --input_path ./input.wav --output_path ./output.wav
```
