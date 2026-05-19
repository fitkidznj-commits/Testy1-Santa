#!/usr/bin/env python3
"""
Treasure Harbor Resort — 30-Second Commercial Audio Generator
Uses ElevenLabs API to produce an emotionally rich voiceover.

Requirements:
    pip install elevenlabs

Usage:
    export ELEVENLABS_API_KEY="your_api_key_here"
    python3 generate_commercial.py
"""

import os
import sys
from pathlib import Path

try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import VoiceSettings, save
except ImportError:
    print("ERROR: ElevenLabs SDK not installed.")
    print("Run: pip install elevenlabs")
    sys.exit(1)


SCRIPT = """\
Close your eyes.

Feel the warm salt air on your face.
Hear the gentle lap of crystal water... beneath you.

Welcome to Treasure Harbor Resort.
Islamorada... the Heart of the Florida Keys.

Your houseboat. Your private harbor.
A front-row seat... to paradise.

Coral reefs at your doorstep.
Dolphins in the distance.
Sunsets... that steal your breath.

Snorkel. Fish. Drift. Dream.

This is your escape.

This... is Treasure Harbor.\
"""

# Voice from ElevenLabs voice library — selected for this commercial
VOICE_ID = "TABZn6CDfjMNGrsnGzzD"

# Emotional voice settings:
#   stability low  → more expressive, varied delivery
#   similarity_boost high → stays true to the voice character
#   style high     → more performative, cinematic
VOICE_SETTINGS = VoiceSettings(
    stability=0.30,
    similarity_boost=0.85,
    style=0.55,
    use_speaker_boost=True,
)

OUTPUT_FILE = "treasure_harbor_commercial.mp3"


def main():
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY environment variable not set.")
        print("Export your key:  export ELEVENLABS_API_KEY='sk-...'")
        sys.exit(1)

    client = ElevenLabs(api_key=api_key)

    print("Generating Treasure Harbor 30-second commercial voiceover...")
    print(f"Voice: Rachel (ID: {VOICE_ID})")
    print(f"Model: eleven_multilingual_v2\n")

    audio = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=SCRIPT,
        model_id="eleven_multilingual_v2",
        voice_settings=VOICE_SETTINGS,
    )

    save(audio, OUTPUT_FILE)

    size_kb = Path(OUTPUT_FILE).stat().st_size / 1024
    print(f"Saved: {OUTPUT_FILE}  ({size_kb:.1f} KB)")
    print("\nScript delivered:")
    print("-" * 50)
    print(SCRIPT)
    print("-" * 50)
    print("\nDone. Open the MP3 to hear your commercial.")


if __name__ == "__main__":
    main()
