#!/usr/bin/env python3
"""
Generate TTS audio for all 40 articles using MiniMax API directly via curl.
Saves MP3 files to audio/ directory.
"""

import json
import os
import subprocess
from pathlib import Path
import time
import concurrent.futures

BASE = Path('/Users/rick/.openclaw/workspace/zhesi')
DATA_DIR = BASE / 'data'
AUDIO_DIR = BASE / 'audio'

API_HOST = 'https://api.minimaxi.com'
API_KEY = 'sk-cp-15ryfXJOLxUtIunuVzO01q6GGH_FftpVryoGJ8HClVMforzeOUvsPmOh2PIl3HlvI9Y_fQDn1eBJF5jca9FSUnKM8fx5PNeFoV93Ck5oqzzvreUz1kHf-u8'
VOICE = 'female-tianmei'
MODEL = 'speech-2.8-hd'

AUDIO_DIR.mkdir(exist_ok=True)

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}',
}

def generate_tts(text: str, output_path: Path) -> bool:
    """Generate TTS audio for given text, save to output_path. Returns True on success."""
    import urllib.request
    import urllib.error

    if not text.strip():
        return False

    payload = {
        'model': MODEL,
        'text': text,
        'stream': False,
        'voice_setting': {
            'voice_id': VOICE,
            'speed': 1.0,
            'vol': 1,
            'pitch': 0,
        },
        'audio_setting': {
            'format': 'mp3',
            'sample_rate': 32000,
            'bitrate': 128000,
            'channel': 1,
        },
    }

    req = urllib.request.Request(
        f'{API_HOST}/v1/t2a_v2',
        data=json.dumps(payload).encode('utf-8'),
        headers=HEADERS,
        method='POST',
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f'    API error: {e}')
        return False

    if data.get('base_resp', {}).get('status_code') != 0:
        print(f"    API error: {data.get('base_resp', {}).get('status_msg')}")
        return False

    audio_hex = data.get('data', {}).get('audio')
    if not audio_hex:
        print(f'    No audio in response')
        return False

    # Decode hex to binary and save
    audio_bytes = bytes.fromhex(audio_hex)
    output_path.write_bytes(audio_bytes)
    return True


def process_article(json_path: Path) -> tuple:
    article_id = json_path.stem
    mp3_path = AUDIO_DIR / f'{article_id}.mp3'

    if mp3_path.exists():
        size = mp3_path.stat().st_size
        return article_id, 'skip', size

    data = json.loads(json_path.read_text(encoding='utf-8'))
    text = '。'.join([b['orig'] for b in data['blocks']])

    if not text.strip():
        return article_id, 'empty', 0

    print(f'  >> {article_id}.mp3 ({len(text)} chars)...', flush=True)

    ok = generate_tts(text, mp3_path)
    if ok:
        size = mp3_path.stat().st_size
        print(f'  ✓ {article_id}.mp3 ({size//1024}KB)')
        time.sleep(2)  # Rate limit avoidance
        return article_id, 'ok', size
    else:
        print(f'  ✗ {article_id} FAILED, retry in 5s')
        time.sleep(5)
        # retry once
        ok2 = generate_tts(text, mp3_path)
        if ok2:
            size = mp3_path.stat().st_size
            print(f'  ✓ {article_id}.mp3 (retry OK, {size//1024}KB)')
            time.sleep(2)
            return article_id, 'ok', size
        print(f'  ✗ {article_id} FAILED after retry')
        return article_id, 'error', 0


def main():
    json_files = sorted(DATA_DIR.glob('*.json'))
    total = len(json_files)

    print(f'Generating TTS for {total} articles...')
    print(f'Voice: {VOICE} | Model: {MODEL}')
    print()

    results = []
    for json_path in json_files:
        article_id, status, size = process_article(json_path)
        results.append((article_id, status, size))

    ok = sum(1 for r in results if r[1] == 'ok')
    skip = sum(1 for r in results if r[1] == 'skip')
    errors = [r[0] for r in results if r[1] == 'error']

    print(f'\nResults: {ok} generated, {skip} skipped, {len(errors)} errors')
    if errors:
        print(f'Failed articles: {errors}')


if __name__ == '__main__':
    main()
