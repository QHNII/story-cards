# -*- coding: utf-8 -*-
"""批量生成竖版图文卡片（千问 Token Plan 图像接口，适配任意账号/设备）。
用法: python3 generate_cards.py --cards cards.json --outdir <dir> [--keyfile ~/.story-cards/key] [--style healing]
cards.json: [{"name","scene","lines":[...],"pos":"top|center"}] 或 [{"name","prompt"}]
--style: healing|flat|film|ink|line|3d（场景+文字模式时注入画风）；prompt 模式忽略 style。
只读密钥、不打印。输出 OK/FAIL 与汇总；无密钥退出码 3。
"""
import argparse, json, os, sys, time, urllib.request, urllib.error

DEF_BASE = 'https://token-plan.maas.qianwenaiapi.com/api/v1'
DEF_MODEL = 'qwen-image-3.0-pro'
DEF_SIZE = '1104*1472'  # 3:4
STYLES = {
 'healing': '治愈系水彩插画，低饱和暖色调（米白、暖黄、浅咖、低饱和蓝灰），柔和笔触、安静温柔、大量留白。',
 'flat': '现代扁平插画，几何色块、低饱和莫兰迪配色、简洁构图、留白充足、温柔治愈。',
 'film': '胶片摄影风，柔和颗粒、暖调自然光、浅景深、生活纪实感、安静温柔。',
 'ink': '国风水墨插画，淡彩晕染、留白意境、宣纸质感、低饱和、温柔治愈。',
 'line': '手绘线条插画，暖米色底、细线勾勒、淡彩点缀、大量留白、安静治愈。',
 '3d': '3D 治愈渲染，黏土/盲盒质感、柔和全局光、低饱和暖色、圆润可爱、干净背景。',
}
FONT = '温柔宋体/手写感字体，深咖色文字，逐字准确无错字。不要水印，不要这些行以外的文字。'

def build_prompt(c, style):
    if c.get('prompt'):
        return c['prompt']
    lines = c.get('lines', [])
    txt = '「' + '」「'.join(lines) + '」'
    n = len(lines)
    place = ('画面居中排%d行中文，前两行稍大后两行稍小：' % n) if c.get('pos') == 'center' \
        else ('画面上方留白居中排%d行中文：' % n)
    return '竖版3:4。' + STYLES.get(style, STYLES['healing']) + c.get('scene', '') + place + txt + '。' + FONT

def gen(base, model, size, key, prompt, out):
    body = {"model": model, "input": {"messages": [{"role": "user", "content": [{"text": prompt}]}]},
            "parameters": {"size": size, "n": 1}}
    req = urllib.request.Request(base + '/services/aigc/multimodal-generation/generation',
        data=json.dumps(body).encode(), headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'},
        method='POST')
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    url = None
    for x in d['output']['choices'][0]['message']['content']:
        if isinstance(x, dict) and x.get('image'):
            url = x['image']
    if not url:
        raise RuntimeError('no image in response')
    urllib.request.urlretrieve(url, out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cards', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--keyfile', default=os.path.expanduser('~/.story-cards/key'))
    ap.add_argument('--base', default=DEF_BASE)
    ap.add_argument('--model', default=DEF_MODEL)
    ap.add_argument('--size', default=DEF_SIZE)
    ap.add_argument('--style', default='healing')
    ap.add_argument('--prefix', default='卡片')
    a = ap.parse_args()
    if not os.path.exists(a.keyfile):
        print('NO_KEY: 密钥文件不存在 %s，请先一次性配置' % a.keyfile); sys.exit(3)
    key = open(a.keyfile).read().strip()
    cards = json.load(open(a.cards))
    os.makedirs(a.outdir, exist_ok=True)
    ok, fail = [], []
    for c in cards:
        name = c['name']
        out = os.path.join(a.outdir, a.prefix + name + '.png')
        try:
            gen(a.base, a.model, a.size, key, build_prompt(c, a.style), out)
            ok.append(name); print('OK', name, flush=True)
        except urllib.error.HTTPError as e:
            fail.append(name); print('FAIL', name, e.code, e.read().decode()[:150], flush=True)
        except Exception as e:
            fail.append(name); print('ERR', name, str(e)[:150], flush=True)
        time.sleep(1)
    print('DONE ok=%d fail=%d' % (len(ok), len(fail)))
    if fail:
        print('FAILED:', ','.join(fail)); sys.exit(2)

if __name__ == '__main__':
    main()