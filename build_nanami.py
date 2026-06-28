# -*- coding: utf-8 -*-
"""お手元のWindows/Mac PCで実行する用。
edge-tts で Nanami 音声(cover/r8/r9/summary.mp3)を生成し、
gen_html3.py を通して HTML に自動埋め込みします（全端末で同じNanami音声で再生）。
"""
import asyncio, subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

# gen_html3.py から最終ナレーション本文(NARR)を取得（HTML書き込み前まで実行）
src = open('gen_html3.py', encoding='utf-8').read()
ns = {}
exec(src.split('C={')[0], ns)
NARR = ns['NARR']

async def synth(text, out):
    import edge_tts
    c = edge_tts.Communicate(text, 'ja-JP-NanamiNeural')
    await c.save(out)

async def main():
    for _id, text in NARR:
        out = _id + '.mp3'
        print('  音声生成中:', out)
        await synth(text, out)
        print('    OK', os.path.getsize(out), 'bytes')

if __name__ == '__main__':
    try:
        import edge_tts  # noqa
    except ImportError:
        print('edge-tts をインストールします...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', 'edge-tts'])
    print('Nanami音声を生成します（ネット接続が必要）...')
    asyncio.run(main())
    print('HTMLにNanami音声を埋め込みます...')
    subprocess.check_call([sys.executable, 'gen_html3.py'])
    print('')
    print('===== 完成しました =====')
    print('ファイル: 新生社様_2段階プラン_24h自家消費シミュレーション.html')
    print('→ どの端末でも「自動再生」でNanami音声が流れます。Netlifyに公開してください。')
