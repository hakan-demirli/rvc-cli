{
  inputs = {
    nixpkgs.url = "nixpkgs/nixpkgs-unstable";
  };

  outputs =
    {
      self,
      nixpkgs,
      ...
    }@inputs:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
        #Didn't test this to spare my poor CPU
        #config.cudaSupport = true;
      };
      pedalboard = pkgs.callPackage ./nix/pedalboard.nix { };
      noisereduce = pkgs.callPackage ./nix/noisereduce.nix { };
      local-attention = pkgs.callPackage ./nix/local-attention.nix { };
    in
    {
      devShells.${system}.default =
        let
          pythonEnv = pkgs.python3.withPackages (
            ps: with ps; [
              pip

              # Core dependencies
              numpy
              requests
              tqdm
              wget
              pydantic
              fastapi
              starlette

              # Audio processing
              ffmpeg-python
              faiss
              librosa
              pyworld
              scipy
              soundfile
              # praat-parselmouth
              parselmouth
              noisereduce
              pedalboard
              # stftpitchshift

              # Machine learning and deep learning
              numba
              torch
              torchaudio
              torchvision
              torchcrepe
              einops
              # libf0
              transformers

              # Visualization and UI
              matplotlib
              tensorboard
              gradio

              # Miscellaneous utilities
              certifi
              antlr4-python3-runtime
              ffmpy
              tensorboardx
              # edge-tts
              pypresence
              beautifulsoup4
              flask
              local-attention

              # UVR
              samplerate
              six
              pydub
              onnx
              # onnx2torch
              onnxruntime
              julius
              # diffq
              # ml_collections
              resampy
              beartype
              rotary-embedding-torch
            ]
          );
        in
        pkgs.mkShell {
          packages = [ pythonEnv ];
        };
    };
}
