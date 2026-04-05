#!/usr/bin/env python3
"""
Generate all article images using MiniMax image API via skill script.
"""
import subprocess
import os
import time
import json
from pathlib import Path

BASE = Path('/Users/rick/.openclaw/workspace/zhesi')
IMAGE_DIR = BASE / 'images'
IMAGE_DIR.mkdir(exist_ok=True)

SKILL_SCRIPT = '/Users/rick/.claude/skills/minimax-multimodal-toolkit/scripts/image/generate_image.sh'

os.environ['MINIMAX_API_HOST'] = 'https://api.minimaxi.com'
os.environ['MINIMAX_API_KEY'] = 'sk-cp-15ryfXJOLxUtIunuVzO01q6GGH_FftpVryoGJ8HClVMforzeOUvsPmOh2PIl3HlvI9Y_fQDn1eBJF5jca9FSUnKM8fx5PNeFoV93Ck5oqzzvreUz1kHf-u8'

PROMPTS = {
    'xiaoyao-you': 'A mythical giant fish leaping from a dark ocean at night, transforming into a massive celestial bird with wings spanning like clouds. Classical Chinese ink wash painting, ethereal mist, traditional East Asian landscape, black ink on aged parchment, wandering spirit, freedom, dramatic diagonal composition',
    'qi-wu-lun': 'Ancient Chinese philosopher sitting under a withered tree, mist rising from a valley. Classical Chinese ink wash painting, mountain silhouettes dissolving into each other, Taoist solitude, contemplative mood, monochrome with grey washes',
    'yang-sheng-zhu': 'A sage cooking by a woodland fire, silhouette against warm flames, bamboo grove. Classical Chinese ink wash style, flickering firelight, peaceful woodland hermitage, Taoist longevity symbolism, warm amber tones',
    'ren-jian-shi': 'Scholar navigating a narrow mountain path between ancient cliff walls, misty peaks above. Classical ink wash painting, steep rocks, narrow corridor path, dramatic vertical composition',
    'de-chong-fu': 'Serene ancient sage seated under a plum tree in snow, one sleeve empty. Classical Chinese ink wash painting, plum blossoms, winter stillness, spiritual completeness despite physical loss, minimalist',
    'da-zong-shi': 'Two fish swimming in shallow clear water among reeds, morning mist rising. Classical Chinese ink wash painting, Daoist transcendence, serene blue-grey tones, peaceful ripples',
    'ying-di-wang': 'Ancient ruler seated on simple throne receiving a barefoot sage, vast empty palace hall. Classical Chinese ink wash painting, minimal figures in expansive space, echoes of emptiness',
    'pian-mu': 'Conjoined twin birds perched on a withered branch, facing opposite directions yet connected. Classical Chinese ink wash painting, surreal Taoist paradox of unity and difference',
    'ma-ti': 'Wild horses galloping free on open steppe grassland under dramatic clouds, no bridle. Classical Chinese ink wash painting, dynamic movement, freedom and nature, sweeping brushstrokes',
    'qu-qie': 'Ancient chest with broken lock hanging open, treasures inside turning to dust. Classical Chinese ink still life, decay and transience, open lacquer box, muted sepia palette',
    'zai-you': 'Sage floating freely in vast cosmic space between heaven and earth. Classical Chinese ink wash painting, solitary figure suspended in misty void, ethereal atmosphere',
    'tian-di': 'Vast cosmic landscape with rivers flowing upward into heaven, mountains forming human faces. Classical Chinese ink wash painting, rivers defying gravity, Taoist cosmology, surreal nature',
    'tian-dao': 'Ancient figure reading a giant book under a pagoda, dust motes floating in sunlight beam. Classical Chinese ink wash painting, scholar with celestial book, contemplative stillness',
    'tian-yun': 'The sun and moon racing across the sky in opposite arcs, clouds parting. Classical Chinese ink wash painting, celestial motion, cosmic rhythm, dramatic sky',
    'ke-yi': 'Hermit scholar on mountain peak practicing sword forms, sword glinting in sunset light. Classical Chinese ink wash painting, solitary warrior-monk, dramatic silhouette against glowing sky',
    'shan-xing': 'Person polishing a rough jade stone by candlelight, revealing inner brilliance. Classical Chinese ink wash painting, figure at night with single candle, warm candlelight against dark ink',
    'qiu-shui': 'Autumn flood waters surging through a mountain gorge, huge waves crashing. Classical Chinese ink wash painting, torrential river, power of water, dynamic black strokes',
    'zhi-le': 'Skeleton seated cross-legged laughing at the sky, wine cup in hand. Classical Chinese ink wash painting, Taoist joy about death, bone-white against deep black ink',
    'da-sheng': 'Ancient craftsman shaping wood into a musical instrument, sawdust swirling. Classical Chinese ink wash painting, master woodworker, natural forms revealed, warm wood tones',
    'shan-mu': 'Solitary tree on mountain edge with one crow, dramatic sky, autumn foliage. Classical Chinese ink wash painting, gnarled tree on cliff, dramatic sunset sky',
    'tian-zi-fang': 'Ancient court official in flowing robes crossing a bridge toward a temple, morning mist. Classical Chinese ink wash painting, stone bridge, distant temple, Confucian pursuit of Dao',
    'zhi-bei-you': 'Knowledge as a lost traveler in dark forest, fireflies illuminating ancient trees. Classical Chinese ink wash painting, tiny glowing lights among massive dark trunks, luminescent particles',
    'geng-sang-chu': 'Elderly hermit in simple robe tending a remote mountain farm, terraced rice fields. Classical Chinese ink wash painting, misty mountain farm, green and grey',
    'xu-wu-gui': 'Sage and dog traveling together along mountain path, both seemingly invisible. Classical Chinese ink wash painting, autumn mountain path, muted browns and greys',
    'ze-yang': 'Two scholars debating beneath a canopy of stars, moonlight on stone. Classical Chinese ink wash painting, philosophical argument under open sky, cool blue night tones',
    'wai-wu': 'Fisherman returning home with empty net on shoulder, setting sun behind mountains. Classical Chinese ink wash painting, solitary fisherman, warm sunset palette',
    'yu-yan': 'Ancient storyteller narrating to a circle of listeners, each with different reacting faces. Classical Chinese ink wash painting, bamboo grove, communal storytelling tradition',
    'rang-wang': 'Ancient king abdicating throne, walking away into mountains, crown left on empty seat. Classical Chinese ink wash painting, ruler departing palace, dramatic exit',
    'dao-zhi': 'Confucian moralist confronted by laughing Taoist sage. Classical Chinese ink wash painting, formal pose versus carefree sprawl, dramatic tension',
    'shuo-jian': 'Two swordsmen facing each other on a misty cliff, swords drawn, lightning in background. Classical Chinese ink wash painting, duel on mountain peak, high contrast',
    'yu-fu': 'Old fisherman and woodsman sharing wine under a willow tree by a river. Classical Chinese ink wash painting, two elderly men drinking together, serene green and amber tones',
    'lie-yu-kou': 'Arrow shooter on cliff edge aiming at moving target, multiple arrows in flight. Classical Chinese ink wash painting, Lie Yu showing archery mastery, dynamic diagonal',
    'tian-xia': 'Ancient gathering of philosophers under a great tree, various postures of debate. Classical Chinese ink wash painting, Hundred Schools of Thought, numerous small figures',
    'qing-jing-jing': 'Daoist immortal seated in cosmic meditation, universe expanding from the heart. Classical Chinese ink wash painting, meditating sage surrounded by swirling galaxies, mystical',
    'taiyi-jinhua': 'Golden flower blooming in darkness, light radiating from a single petal. Classical Chinese ink wash painting, luminous bloom emerging from shadow, amber and deep black',
    'dao-de-jing': 'Ancient sage writing with one brush, ten thousand characters flowing from the brush. Classical Chinese ink wash painting, Laozi writing Dao De Jing, monumental composition',
    'wen-zi': 'Ancient minister consulting ancient scrolls by candlelight, shadows dancing on bamboo walls. Classical Chinese ink wash painting, candle casting long shadows, warm lamp glow',
    'lie-zi': 'Rider floating through clouds on the wind, robes streaming, crossing mountain peaks. Classical Chinese ink wash painting, Liezi riding the wind, ethereal white clouds against dark sky',
    'huainan-zi': 'Court scholars debating around a cosmological diagram, mountains and rivers in mist. Classical Chinese ink wash painting, intellectual gathering, scholarly debate',
    'bao-pu-zi': 'Alchemist working at furnace in mountain cave, green and gold flames. Classical Chinese ink wash painting, Ge Hong at inner alchemy furnace, mystical flames',
}


def main():
    data_dir = BASE / 'data'
    json_files = sorted(data_dir.glob('*.json'))

    results = []
    for json_path in json_files:
        article_id = json_path.stem
        png_path = IMAGE_DIR / f'{article_id}.png'

        if png_path.exists():
            print(f'  ─ {article_id}.png (exists, skip)')
            results.append((article_id, 'skip'))
            continue

        prompt = PROMPTS.get(article_id, PROMPTS['tian-di'])
        print(f'  >> {article_id}.png ...', flush=True)

        cmd = [
            'bash', SKILL_SCRIPT,
            '--prompt', prompt,
            '--aspect-ratio', '16:9',
            '-o', str(png_path),
        ]

        env = os.environ.copy()

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(BASE),
            env=env,
        )

        if result.returncode == 0 and png_path.exists():
            size = png_path.stat().st_size
            print(f'  ✓ {article_id}.png ({size//1024}KB)')
            results.append((article_id, 'ok'))
            time.sleep(5)  # rate limit
        else:
            print(f'  ✗ {article_id}.png FAILED: {result.stderr[:100]}')
            results.append((article_id, 'error'))
            time.sleep(8)

    ok = sum(1 for r in results if r[1] == 'ok')
    skip = sum(1 for r in results if r[1] == 'skip')
    errors = [r[0] for r in results if r[1] == 'error']
    print(f'\nResults: {ok} generated, {skip} skipped, {len(errors)} errors')
    if errors:
        print(f'Failed: {errors}')


if __name__ == '__main__':
    main()
