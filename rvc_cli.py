import argparse
import os
import sys
from functools import lru_cache
import pathlib

script_dir = pathlib.Path(os.path.realpath(__file__)).parent.absolute()
sys.path.append(str(script_dir))

python = sys.executable


@lru_cache(maxsize=None)
def import_voice_converter():
    from rvc.infer.infer import VoiceConverter

    return VoiceConverter()


@lru_cache(maxsize=1)
def get_config():
    from rvc.configs.config import Config

    return Config()


def strtobool(value):
    value = value.lower()
    if value in {"true", "t", "yes", "y", "1"}:
        return True
    elif value in {"false", "f", "no", "n", "0"}:
        return False
    else:
        raise ValueError(f"Invalid boolean value: '{value}'")


# Infer
def run_infer_script(
    pitch: int,
    filter_radius: int,
    index_rate: float,
    volume_envelope: int,
    protect: float,
    hop_length: int,
    f0_method: str,
    input_path: str,
    output_path: str,
    pth_path: str,
    index_path: str,
    split_audio: bool,
    f0_autotune: bool,
    f0_autotune_strength: float,
    clean_audio: bool,
    clean_strength: float,
    export_format: str,
    upscale_audio: bool,
    f0_file: str,
    embedder_model: str,
    embedder_model_custom: str = "",
    formant_shifting: bool = False,
    formant_qfrency: float = 1.0,
    formant_timbre: float = 1.0,
    post_process: bool = False,
    reverb: bool = False,
    pitch_shift: bool = False,
    limiter: bool = False,
    gain: bool = False,
    distortion: bool = False,
    chorus: bool = False,
    bitcrush: bool = False,
    clipping: bool = False,
    compressor: bool = False,
    delay: bool = False,
    reverb_room_size: float = 0.5,
    reverb_damping: float = 0.5,
    reverb_wet_gain: float = 0.5,
    reverb_dry_gain: float = 0.5,
    reverb_width: float = 0.5,
    reverb_freeze_mode: float = 0.5,
    pitch_shift_semitones: float = 0.0,
    limiter_threshold: float = -6,
    limiter_release_time: float = 0.01,
    gain_db: float = 0.0,
    distortion_gain: float = 25,
    chorus_rate: float = 1.0,
    chorus_depth: float = 0.25,
    chorus_center_delay: float = 7,
    chorus_feedback: float = 0.0,
    chorus_mix: float = 0.5,
    bitcrush_bit_depth: int = 8,
    clipping_threshold: float = -6,
    compressor_threshold: float = 0,
    compressor_ratio: float = 1,
    compressor_attack: float = 1.0,
    compressor_release: float = 100,
    delay_seconds: float = 0.5,
    delay_feedback: float = 0.0,
    delay_mix: float = 0.5,
    sid: int = 0,
):
    infer_pipeline = import_voice_converter()
    kwargs = {
        "audio_input_path": input_path,
        "audio_output_path": output_path,
        "model_path": pth_path,
        "index_path": index_path,
        "pitch": pitch,
        "filter_radius": filter_radius,
        "index_rate": index_rate,
        "volume_envelope": volume_envelope,
        "protect": protect,
        "hop_length": hop_length,
        "f0_method": f0_method,
        "pth_path": pth_path,
        "split_audio": split_audio,
        "f0_autotune": f0_autotune,
        "f0_autotune_strength": f0_autotune_strength,
        "clean_audio": clean_audio,
        "clean_strength": clean_strength,
        "export_format": export_format,
        "upscale_audio": upscale_audio,
        "f0_file": f0_file,
        "embedder_model": embedder_model,
        "embedder_model_custom": embedder_model_custom,
        "post_process": post_process,
        "formant_shifting": formant_shifting,
        "formant_qfrency": formant_qfrency,
        "formant_timbre": formant_timbre,
        "reverb": reverb,
        "pitch_shift": pitch_shift,
        "limiter": limiter,
        "gain": gain,
        "distortion": distortion,
        "chorus": chorus,
        "bitcrush": bitcrush,
        "clipping": clipping,
        "compressor": compressor,
        "delay": delay,
        "reverb_room_size": reverb_room_size,
        "reverb_damping": reverb_damping,
        "reverb_wet_level": reverb_wet_gain,
        "reverb_dry_level": reverb_dry_gain,
        "reverb_width": reverb_width,
        "reverb_freeze_mode": reverb_freeze_mode,
        "pitch_shift_semitones": pitch_shift_semitones,
        "limiter_threshold": limiter_threshold,
        "limiter_release": limiter_release_time,
        "gain_db": gain_db,
        "distortion_gain": distortion_gain,
        "chorus_rate": chorus_rate,
        "chorus_depth": chorus_depth,
        "chorus_delay": chorus_center_delay,
        "chorus_feedback": chorus_feedback,
        "chorus_mix": chorus_mix,
        "bitcrush_bit_depth": bitcrush_bit_depth,
        "clipping_threshold": clipping_threshold,
        "compressor_threshold": compressor_threshold,
        "compressor_ratio": compressor_ratio,
        "compressor_attack": compressor_attack,
        "compressor_release": compressor_release,
        "delay_seconds": delay_seconds,
        "delay_feedback": delay_feedback,
        "delay_mix": delay_mix,
        "sid": sid,
    }
    infer_pipeline.convert_audio(
        **kwargs,
    )
    return f"File {input_path} inferred successfully.", output_path.replace(
        ".wav", f".{export_format.lower()}"
    )


# Parse arguments
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run the main.py script with specific parameters."
    )
    subparsers = parser.add_subparsers(
        title="subcommands", dest="mode", help="Choose a mode"
    )

    # Parser for 'infer' mode
    infer_parser = subparsers.add_parser("infer", help="Run inference")
    pitch_description = (
        "Set the pitch of the audio. Higher values result in a higher pitch."
    )
    infer_parser.add_argument(
        "--pitch",
        type=int,
        help=pitch_description,
        choices=range(-24, 25),
        default=0,
    )
    filter_radius_description = "Apply median filtering to the extracted pitch values if this value is greater than or equal to three. This can help reduce breathiness in the output audio."
    infer_parser.add_argument(
        "--filter_radius",
        type=int,
        help=filter_radius_description,
        choices=range(11),
        default=3,
    )
    index_rate_description = "Control the influence of the index file on the output. Higher values mean stronger influence. Lower values can help reduce artifacts but may result in less accurate voice cloning."
    infer_parser.add_argument(
        "--index_rate",
        type=float,
        help=index_rate_description,
        choices=[i / 100.0 for i in range(0, 101)],
        default=0.3,
    )
    volume_envelope_description = "Control the blending of the output's volume envelope. A value of 1 means the output envelope is fully used."
    infer_parser.add_argument(
        "--volume_envelope",
        type=float,
        help=volume_envelope_description,
        choices=[i / 100.0 for i in range(0, 101)],
        default=1,
    )
    protect_description = "Protect consonants and breathing sounds from artifacts. A value of 0.5 offers the strongest protection, while lower values may reduce the protection level but potentially mitigate the indexing effect."
    infer_parser.add_argument(
        "--protect",
        type=float,
        help=protect_description,
        choices=[i / 1000.0 for i in range(0, 501)],
        default=0.33,
    )
    hop_length_description = "Only applicable for the Crepe pitch extraction method. Determines the time it takes for the system to react to a significant pitch change. Smaller values require more processing time but can lead to better pitch accuracy."
    infer_parser.add_argument(
        "--hop_length",
        type=int,
        help=hop_length_description,
        choices=range(1, 513),
        default=128,
    )
    f0_method_description = "Choose the pitch extraction algorithm for the conversion. 'rmvpe' is the default and generally recommended."
    infer_parser.add_argument(
        "--f0_method",
        type=str,
        help=f0_method_description,
        choices=[
            "crepe",
            "crepe-tiny",
            "rmvpe",
            "fcpe",
            "hybrid[crepe+rmvpe]",
            "hybrid[crepe+fcpe]",
            "hybrid[rmvpe+fcpe]",
            "hybrid[crepe+rmvpe+fcpe]",
        ],
        default="rmvpe",
    )
    infer_parser.add_argument(
        "--input_path",
        type=str,
        help="Full path to the input audio file.",
        required=True,
    )
    infer_parser.add_argument(
        "--output_path",
        type=str,
        help="Full path to the output audio file.",
        required=True,
    )
    pth_path_description = "Full path to the RVC model file (.pth)."
    infer_parser.add_argument(
        "--pth_path", type=str, help=pth_path_description, required=True
    )
    index_path_description = "Full path to the index file (.index)."
    infer_parser.add_argument(
        "--index_path", type=str, help=index_path_description, required=True
    )
    split_audio_description = "Split the audio into smaller segments before inference. This can improve the quality of the output for longer audio files."
    infer_parser.add_argument(
        "--split_audio",
        type=lambda x: bool(strtobool(x)),
        choices=[True, False],
        help=split_audio_description,
        default=False,
    )
    f0_autotune_description = "Apply a light autotune to the inferred audio. Particularly useful for singing voice conversions."
    infer_parser.add_argument(
        "--f0_autotune",
        type=lambda x: bool(strtobool(x)),
        choices=[True, False],
        help=f0_autotune_description,
        default=False,
    )
    f0_autotune_strength_description = "Set the autotune strength - the more you increase it the more it will snap to the chromatic grid."
    infer_parser.add_argument(
        "--f0_autotune_strength",
        type=float,
        help=f0_autotune_strength_description,
        choices=[(i / 10) for i in range(11)],
        default=1.0,
    )
    clean_audio_description = "Clean the output audio using noise reduction algorithms. Recommended for speech conversions."
    infer_parser.add_argument(
        "--clean_audio",
        type=lambda x: bool(strtobool(x)),
        choices=[True, False],
        help=clean_audio_description,
        default=False,
    )
    clean_strength_description = "Adjust the intensity of the audio cleaning process. Higher values result in stronger cleaning, but may lead to a more compressed sound."
    infer_parser.add_argument(
        "--clean_strength",
        type=float,
        help=clean_strength_description,
        choices=[(i / 10) for i in range(11)],
        default=0.7,
    )
    export_format_description = "Select the desired output audio format."
    infer_parser.add_argument(
        "--export_format",
        type=str,
        help=export_format_description,
        choices=["WAV", "MP3", "FLAC", "OGG", "M4A"],
        default="WAV",
    )
    embedder_model_description = (
        "Choose the model used for generating speaker embeddings."
    )
    infer_parser.add_argument(
        "--embedder_model",
        type=str,
        help=embedder_model_description,
        choices=[
            "contentvec",
            "chinese-hubert-base",
            "japanese-hubert-base",
            "korean-hubert-base",
            "custom",
        ],
        default="contentvec",
    )
    embedder_model_custom_description = "Specify the path to a custom model for speaker embedding. Only applicable if 'embedder_model' is set to 'custom'."
    infer_parser.add_argument(
        "--embedder_model_custom",
        type=str,
        help=embedder_model_custom_description,
        default=None,
    )
    upscale_audio_description = "Upscale the input audio to a higher quality before processing. This can improve the overall quality of the output, especially for low-quality input audio."
    infer_parser.add_argument(
        "--upscale_audio",
        type=lambda x: bool(strtobool(x)),
        choices=[True, False],
        help=upscale_audio_description,
        default=False,
    )
    f0_file_description = "Full path to an external F0 file (.f0). This allows you to use pre-computed pitch values for the input audio."
    infer_parser.add_argument(
        "--f0_file",
        type=str,
        help=f0_file_description,
        default=None,
    )
    formant_shifting_description = "Apply formant shifting to the input audio. This can help adjust the timbre of the voice."
    infer_parser.add_argument(
        "--formant_shifting",
        type=lambda x: bool(strtobool(x)),
        choices=[True, False],
        help=formant_shifting_description,
        default=False,
        required=False,
    )
    formant_qfrency_description = "Control the frequency of the formant shifting effect. Higher values result in a more pronounced effect."
    infer_parser.add_argument(
        "--formant_qfrency",
        type=float,
        help=formant_qfrency_description,
        default=1.0,
        required=False,
    )
    formant_timbre_description = "Control the timbre of the formant shifting effect. Higher values result in a more pronounced effect."
    infer_parser.add_argument(
        "--formant_timbre",
        type=float,
        help=formant_timbre_description,
        default=1.0,
        required=False,
    )
    sid_description = "Speaker ID for multi-speaker models."
    infer_parser.add_argument(
        "--sid",
        type=int,
        help=sid_description,
        default=0,
        required=False,
    )
    post_process_description = "Apply post-processing effects to the output audio."
    infer_parser.add_argument(
        "--post_process",
        type=lambda x: bool(strtobool(x)),
        choices=[True, False],
        help=post_process_description,
        default=False,
        required=False,
    )
    reverb_description = "Apply reverb effect to the output audio."
    infer_parser.add_argument(
        "--reverb",
        type=lambda x: bool(strtobool(x)),
        choices=[True, False],
        help=reverb_description,
        default=False,
        required=False,
    )

    pitch_shift_description = "Apply pitch shifting effect to the output audio."
    infer_parser.add_argument(
        "--pitch_shift",
        type=lambda x: bool(strtobool(x)),
        choices=[True, False],
        help=pitch_shift_description,
        default=False,
        required=False,
    )

    limiter_description = "Apply limiter effect to the output audio."
    infer_parser.add_argument(
        "--limiter",
        type=lambda x: bool(strtobool(x)),
        choices=[True, False],
        help=limiter_description,
        default=False,
        required=False,
    )

    gain_description = "Apply gain effect to the output audio."
    infer_parser.add_argument(
        "--gain",
        type=lambda x: bool(strtobool(x)),
        choices=[True, False],
        help=gain_description,
        default=False,
        required=False,
    )

    distortion_description = "Apply distortion effect to the output audio."
    infer_parser.add_argument(
        "--distortion",
        type=lambda x: bool(strtobool(x)),
        choices=[True, False],
        help=distortion_description,
        default=False,
        required=False,
    )

    chorus_description = "Apply chorus effect to the output audio."
    infer_parser.add_argument(
        "--chorus",
        type=lambda x: bool(strtobool(x)),
        choices=[True, False],
        help=chorus_description,
        default=False,
        required=False,
    )

    bitcrush_description = "Apply bitcrush effect to the output audio."
    infer_parser.add_argument(
        "--bitcrush",
        type=lambda x: bool(strtobool(x)),
        choices=[True, False],
        help=bitcrush_description,
        default=False,
        required=False,
    )

    clipping_description = "Apply clipping effect to the output audio."
    infer_parser.add_argument(
        "--clipping",
        type=lambda x: bool(strtobool(x)),
        choices=[True, False],
        help=clipping_description,
        default=False,
        required=False,
    )

    compressor_description = "Apply compressor effect to the output audio."
    infer_parser.add_argument(
        "--compressor",
        type=lambda x: bool(strtobool(x)),
        choices=[True, False],
        help=compressor_description,
        default=False,
        required=False,
    )

    delay_description = "Apply delay effect to the output audio."
    infer_parser.add_argument(
        "--delay",
        type=lambda x: bool(strtobool(x)),
        choices=[True, False],
        help=delay_description,
        default=False,
        required=False,
    )

    reverb_room_size_description = "Control the room size of the reverb effect. Higher values result in a larger room size."
    infer_parser.add_argument(
        "--reverb_room_size",
        type=float,
        help=reverb_room_size_description,
        default=0.5,
        required=False,
    )

    reverb_damping_description = "Control the damping of the reverb effect. Higher values result in a more damped sound."
    infer_parser.add_argument(
        "--reverb_damping",
        type=float,
        help=reverb_damping_description,
        default=0.5,
        required=False,
    )

    reverb_wet_gain_description = "Control the wet gain of the reverb effect. Higher values result in a stronger reverb effect."
    infer_parser.add_argument(
        "--reverb_wet_gain",
        type=float,
        help=reverb_wet_gain_description,
        default=0.5,
        required=False,
    )

    reverb_dry_gain_description = "Control the dry gain of the reverb effect. Higher values result in a stronger dry signal."
    infer_parser.add_argument(
        "--reverb_dry_gain",
        type=float,
        help=reverb_dry_gain_description,
        default=0.5,
        required=False,
    )

    reverb_width_description = "Control the stereo width of the reverb effect. Higher values result in a wider stereo image."
    infer_parser.add_argument(
        "--reverb_width",
        type=float,
        help=reverb_width_description,
        default=0.5,
        required=False,
    )

    reverb_freeze_mode_description = "Control the freeze mode of the reverb effect. Higher values result in a stronger freeze effect."
    infer_parser.add_argument(
        "--reverb_freeze_mode",
        type=float,
        help=reverb_freeze_mode_description,
        default=0.5,
        required=False,
    )

    pitch_shift_semitones_description = "Control the pitch shift in semitones. Positive values increase the pitch, while negative values decrease it."
    infer_parser.add_argument(
        "--pitch_shift_semitones",
        type=float,
        help=pitch_shift_semitones_description,
        default=0.0,
        required=False,
    )

    limiter_threshold_description = "Control the threshold of the limiter effect. Higher values result in a stronger limiting effect."
    infer_parser.add_argument(
        "--limiter_threshold",
        type=float,
        help=limiter_threshold_description,
        default=-6,
        required=False,
    )

    limiter_release_time_description = "Control the release time of the limiter effect. Higher values result in a longer release time."
    infer_parser.add_argument(
        "--limiter_release_time",
        type=float,
        help=limiter_release_time_description,
        default=0.01,
        required=False,
    )

    gain_db_description = "Control the gain in decibels. Positive values increase the gain, while negative values decrease it."
    infer_parser.add_argument(
        "--gain_db",
        type=float,
        help=gain_db_description,
        default=0.0,
        required=False,
    )

    distortion_gain_description = "Control the gain of the distortion effect. Higher values result in a stronger distortion effect."
    infer_parser.add_argument(
        "--distortion_gain",
        type=float,
        help=distortion_gain_description,
        default=25,
        required=False,
    )

    chorus_rate_description = "Control the rate of the chorus effect. Higher values result in a faster chorus effect."
    infer_parser.add_argument(
        "--chorus_rate",
        type=float,
        help=chorus_rate_description,
        default=1.0,
        required=False,
    )

    chorus_depth_description = "Control the depth of the chorus effect. Higher values result in a stronger chorus effect."
    infer_parser.add_argument(
        "--chorus_depth",
        type=float,
        help=chorus_depth_description,
        default=0.25,
        required=False,
    )

    chorus_center_delay_description = "Control the center delay of the chorus effect. Higher values result in a longer center delay."
    infer_parser.add_argument(
        "--chorus_center_delay",
        type=float,
        help=chorus_center_delay_description,
        default=7,
        required=False,
    )

    chorus_feedback_description = "Control the feedback of the chorus effect. Higher values result in a stronger feedback effect."
    infer_parser.add_argument(
        "--chorus_feedback",
        type=float,
        help=chorus_feedback_description,
        default=0.0,
        required=False,
    )

    chorus_mix_description = "Control the mix of the chorus effect. Higher values result in a stronger chorus effect."
    infer_parser.add_argument(
        "--chorus_mix",
        type=float,
        help=chorus_mix_description,
        default=0.5,
        required=False,
    )

    bitcrush_bit_depth_description = "Control the bit depth of the bitcrush effect. Higher values result in a stronger bitcrush effect."
    infer_parser.add_argument(
        "--bitcrush_bit_depth",
        type=int,
        help=bitcrush_bit_depth_description,
        default=8,
        required=False,
    )

    clipping_threshold_description = "Control the threshold of the clipping effect. Higher values result in a stronger clipping effect."
    infer_parser.add_argument(
        "--clipping_threshold",
        type=float,
        help=clipping_threshold_description,
        default=-6,
        required=False,
    )

    compressor_threshold_description = "Control the threshold of the compressor effect. Higher values result in a stronger compressor effect."
    infer_parser.add_argument(
        "--compressor_threshold",
        type=float,
        help=compressor_threshold_description,
        default=0,
        required=False,
    )

    compressor_ratio_description = "Control the ratio of the compressor effect. Higher values result in a stronger compressor effect."
    infer_parser.add_argument(
        "--compressor_ratio",
        type=float,
        help=compressor_ratio_description,
        default=1,
        required=False,
    )

    compressor_attack_description = "Control the attack of the compressor effect. Higher values result in a stronger compressor effect."
    infer_parser.add_argument(
        "--compressor_attack",
        type=float,
        help=compressor_attack_description,
        default=1.0,
        required=False,
    )

    compressor_release_description = "Control the release of the compressor effect. Higher values result in a stronger compressor effect."
    infer_parser.add_argument(
        "--compressor_release",
        type=float,
        help=compressor_release_description,
        default=100,
        required=False,
    )

    delay_seconds_description = "Control the delay time in seconds. Higher values result in a longer delay time."
    infer_parser.add_argument(
        "--delay_seconds",
        type=float,
        help=delay_seconds_description,
        default=0.5,
        required=False,
    )
    delay_feedback_description = "Control the feedback of the delay effect. Higher values result in a stronger feedback effect."
    infer_parser.add_argument(
        "--delay_feedback",
        type=float,
        help=delay_feedback_description,
        default=0.0,
        required=False,
    )
    delay_mix_description = "Control the mix of the delay effect. Higher values result in a stronger delay effect."
    infer_parser.add_argument(
        "--delay_mix",
        type=float,
        help=delay_mix_description,
        default=0.5,
        required=False,
    )

    return parser.parse_args()


def main():
    if len(sys.argv) == 1:
        print("Please run the script with '-h' for more information.")
        sys.exit(1)

    args = parse_arguments()

    try:
        if args.mode == "infer":
            run_infer_script(
                pitch=args.pitch,
                filter_radius=args.filter_radius,
                index_rate=args.index_rate,
                volume_envelope=args.volume_envelope,
                protect=args.protect,
                hop_length=args.hop_length,
                f0_method=args.f0_method,
                input_path=args.input_path,
                output_path=args.output_path,
                pth_path=args.pth_path,
                index_path=args.index_path,
                split_audio=args.split_audio,
                f0_autotune=args.f0_autotune,
                f0_autotune_strength=args.f0_autotune_strength,
                clean_audio=args.clean_audio,
                clean_strength=args.clean_strength,
                export_format=args.export_format,
                embedder_model=args.embedder_model,
                upscale_audio=args.upscale_audio,
                f0_file=args.f0_file,
                formant_shifting=args.formant_shifting,
                formant_qfrency=args.formant_qfrency,
                formant_timbre=args.formant_timbre,
                embedder_model_custom=args.embedder_model_custom,
                sid=args.sid,
                post_process=args.post_process,
                reverb=args.reverb,
                pitch_shift=args.pitch_shift,
                limiter=args.limiter,
                gain=args.gain,
                distortion=args.distortion,
                chorus=args.chorus,
                bitcrush=args.bitcrush,
                clipping=args.clipping,
                compressor=args.compressor,
                delay=args.delay,
                reverb_room_size=args.reverb_room_size,
                reverb_damping=args.reverb_damping,
                reverb_wet_gain=args.reverb_wet_gain,
                reverb_dry_gain=args.reverb_dry_gain,
                reverb_width=args.reverb_width,
                reverb_freeze_mode=args.reverb_freeze_mode,
                pitch_shift_semitones=args.pitch_shift_semitones,
                limiter_threshold=args.limiter_threshold,
                limiter_release_time=args.limiter_release_time,
                gain_db=args.gain_db,
                distortion_gain=args.distortion_gain,
                chorus_rate=args.chorus_rate,
                chorus_depth=args.chorus_depth,
                chorus_center_delay=args.chorus_center_delay,
                chorus_feedback=args.chorus_feedback,
                chorus_mix=args.chorus_mix,
                bitcrush_bit_depth=args.bitcrush_bit_depth,
                clipping_threshold=args.clipping_threshold,
                compressor_threshold=args.compressor_threshold,
                compressor_ratio=args.compressor_ratio,
                compressor_attack=args.compressor_attack,
                compressor_release=args.compressor_release,
                delay_seconds=args.delay_seconds,
                delay_feedback=args.delay_feedback,
                delay_mix=args.delay_mix,
            )
    except Exception as error:
        print(f"An error occurred during execution: {error}")

        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
