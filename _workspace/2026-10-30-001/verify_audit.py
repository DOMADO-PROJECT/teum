"""공개 문서의 형식·집계·도식 정합성을 읽기 전용으로 확인한다."""
import hashlib
import json
import math
import re
import subprocess
import xml.etree.ElementTree as ET
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from urllib.parse import unquote, urlsplit

WORK = Path(__file__).resolve().parent
PUBLIC = WORK.parents[1]
PRIVATE = PUBLIC.parent / 'teum'
DOCS = [PUBLIC / 'README.md', *sorted((PUBLIC / 'docs').glob('*.md'))]
NS = {'s': 'http://www.w3.org/2000/svg'}
results = {}

def check(condition, message):
    if not condition:
        raise AssertionError(message)

def mask_markup(line):
    return re.sub(r'`[^`]+`|!?\[[^\]]*\]\([^)]*\)', '', line)

def missing_breaks(text):
    return [i for i, line in enumerate(text.splitlines(), 1)
            if not line.lstrip().startswith(('#', '<', '!['))
            and re.search(r'[가-힣][.!?](?:\*{1,2})?(?!\*|<br>)', mask_markup(line))]

# 검사기가 실제 누락은 잡고 코드·제목은 제외하는지 확인한다.
check(missing_breaks('문장입니다. 다음입니다.<br>') == [1], '줄바꿈 검사의 양성 대조')
check(not missing_breaks('## 제목입니다.\n문장입니다.<br>\n`v1.2.3`'), '줄바꿈 검사의 음성 대조')
check(not missing_breaks('**문장입니다.**<br>'), '강조 종결 처리')

links = 0
for doc in DOCS:
    text = doc.read_text()
    check(not missing_breaks(text), f'{doc.name}: 줄바꿈 누락 {missing_breaks(text)}')
    check(not re.search(r'<br>(?:\s*<br>){2}', text), f'{doc.name}: 줄바꿈 3회 이상 중복')
    for match in re.finditer(r'^## ', text, re.M):
        before = text[:match.start()].rstrip()
        check(re.search(r'<br>\s*<br>$', before) is not None, f'{doc.name}: 큰 절 앞의 두 줄 간격')
    targets = re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', text)
    targets += re.findall(r'(?:src|srcset)="([^"]+)"', text)
    for target in targets:
        parsed = urlsplit(target)
        if not parsed.scheme and parsed.path:
            check((doc.parent / unquote(parsed.path)).exists(), f'{doc.name}: 없는 링크 {target}')
            links += 1
results['markdown'] = {'documents': len(DOCS), 'local_link_occurrences': links, 'missing_sentence_breaks': 0}

summary = json.loads((PRIVATE / 'docs/verification/sdk-r1-r15-summary-20261024.json').read_text())
sdk_doc = (PUBLIC / 'docs/AI_SDK_R1_R15.md').read_text()
def decimal(value):
    return Decimal(str(value))
def clock_ms(value):
    value = int(decimal(value).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    return f'{value // 60000:02}:{value // 1000 % 60:02}.{value % 1000:03}'

quality_hashes = 0
for run in summary['runs']:
    raw_path = PRIVATE / run['source']
    check(hashlib.sha256(raw_path.read_bytes()).hexdigest() == run['source_sha256'], f'r{run["run"]}: 원본 해시')
    raw = json.loads(raw_path.read_text())
    check(raw['status'] == run['status'] and raw['elapsed_ms'] == run['elapsed_ms'], '실행 상태·시간')
    check(raw['accounting']['requests'] == run['requests'], '원본 요청 수')
    check(decimal(raw['accounting']['known_usd']) == decimal(run['known_usage_cost_usd']), '원본 usage 추정 비용')
    usages = [call['usage'] for phase in raw['phases'] for call in phase['calls'] if call.get('usage')]
    for key in ['input_tokens', 'output_tokens', 'total_tokens']:
        check((sum(u[key] for u in usages) if usages else None) == run[key], f'r{run["run"]}: {key} usage 합계')
    if run.get('quality_sha256'):
        check(hashlib.sha256((PRIVATE / run['quality_source']).read_bytes()).hexdigest() == run['quality_sha256'], '품질 기록 해시')
        quality_hashes += 1
    token_values = [f'{run[k]:,}' if run[k] is not None else '미수신' for k in ['input_tokens', 'output_tokens', 'total_tokens']]
    expected = f'| r{run["run"]} | {run["requests"]} | ' + ' | '.join(token_values) + ' |'
    check(expected in sdk_doc, f'r{run["run"]}: 공개 토큰 표')
    cost = f'${run["known_usage_cost_usd"]:.4f}' if usages else '미확정'
    check(f'| r{run["run"]} | {clock_ms(run["elapsed_ms"])} | {cost} |' in sdk_doc, '공개 시간·비용 표')
check(sum(r['requests'] for r in summary['runs']) == 250, '요청 합계')
check(sum(r['total_tokens'] or 0 for r in summary['runs']) == 14182881, '토큰 합계')
check(sum(decimal(r['known_usage_cost_usd']) for r in summary['runs']) == Decimal('14.7371835'), '비용 합계')
check(sum(r['status'] == 'completed' for r in summary['runs']) == 11, '완료 보고서 수')
check(sum(r['status'] == 'completed' and r['core_complete'] == 4 for r in summary['runs']) == 8, '핵심 4/4 완료 수')
for key, value in summary['final_pair_mean'].items():
    mean = sum(decimal(summary['runs'][i-1][key]) for i in [14,15]) / 2
    check(math.isclose(float(mean), value), f'{key}: 최종 두 회차 평균')
    baseline = decimal(summary['runs'][4][key])
    previous = sum(decimal(summary['runs'][i-1][key]) for i in [11,12]) / 2
    for group, start in [('baseline_comparison', baseline), ('previous_success_pair_comparison', previous)]:
        change = float((mean/start-1)*100)
        check(math.isclose(change, summary[group][key]['change_percent'], abs_tol=1e-10), f'{key}: 변화율')
        if group == 'baseline_comparison' or key != 'input_tokens':
            check(f'{abs(change):.1f}% {"감소" if change < 0 else "증가"}' in sdk_doc, '공개 비교 표의 변화율')
results['sdk'] = {'raw_results': 15, 'quality_hashes': quality_hashes, 'token_table_cells': 60, 'time_cost_table_cells': 30, 'comparisons_recomputed': 12}

svg_files = sorted((PUBLIC / 'assets').rglob('*.svg'))
for path in svg_files:
    root = ET.parse(path).getroot()
    ids = [e.get('id') for e in root.iter() if e.get('id')]
    check(len(ids) == len(set(ids)), f'{path.name}: 중복 SVG id')
    for elem in root.iter():
        check(elem.tag.split('}')[-1] not in ['script', 'foreignObject'], 'SVG 실행 요소')
        for key, value in elem.attrib.items():
            if key.split('}')[-1] == 'href':
                check(value.startswith(('#','data:')), f'{path.name}: 외부 리소스')
    if path.parent.name == 'diagrams' and path.stem != 'database':
        check('prefers-reduced-motion' in path.read_text(), f'{path.name}: 모션 감소 설정')
    if path.stem.startswith('sdk-optimization'):
        metrics = json.loads(root.find('s:metadata',NS).text)['metrics']
        for metric in metrics:
            source = summary['baseline_comparison'][metric['id']]
            check(math.isclose(float(metric['baseline']),source['baseline']), 'SDK SVG 기준값')
            check(math.isclose(float(metric['final_mean']),source['final_pair_mean']), 'SDK SVG 평균')
            check(math.isclose(float(metric['reduction_percent']),-source['change_percent']), 'SDK SVG 감소율')
results['svg'] = {'files': len(svg_files), 'sdk_graph_metrics': 8}

catalog = {t['table_name']:t for t in json.loads((WORK / 'schema-catalog.json').read_text())}
root = ET.parse(PUBLIC / 'assets/diagrams/database.svg').getroot()
def columns(definition):
    return set(re.search(r'\(([^)]+)\)',definition)[1].split(', '))
edges = root.findall('.//*[@data-fk]')
identifying = 0
for edge in edges:
    table = catalog[edge.get('data-child').split('.')[1]]
    foreign = next(c for c in table['constraints'] if c['name'] == edge.get('data-fk'))
    key = columns(foreign['definition'])
    primary = columns(next(c['definition'] for c in table['constraints'] if c['kind']=='p'))
    is_identifying = key <= primary
    identifying += is_identifying
    check(edge.get('data-relationship') == ('identifying' if is_identifying else 'non-identifying'), 'ERD 식별 관계')
    target = re.search(r'REFERENCES ([\w.]+)',foreign['definition'])[1]
    check(edge.get('data-parent') == (target if '.' in target else 'public.'+target), 'ERD 부모')
    parent = edge.find("s:g[@data-end='parent']",NS)
    child = edge.find("s:g[@data-end='child']",NS)
    nullable = any(c['nullable'] for c in table['columns'] if c['name'] in key)
    unique = any(columns(c['definition']) <= key for c in table['constraints'] if c['kind'] in ['p','u'])
    check(parent.get('data-min') == ('0' if nullable else '1') and parent.get('data-max') == 'one', 'ERD 부모 선택성')
    check(child.get('data-min') == '0' and child.get('data-max') == ('one' if unique else 'many'), 'ERD 자식 카디널리티')
cards = root.findall('.//*[@data-table]')
for card in cards:
    name = card.get('data-table').split('.')[1]
    if name == 'users':
        continue
    table = catalog[name]
    primary = columns(next(c['definition'] for c in table['constraints'] if c['kind']=='p'))
    foreign = set().union(*(columns(c['definition']) for c in table['constraints'] if c['kind']=='f'))
    fields = [e.text for e in card.findall('.//s:text[@class="field"]',NS)]
    types = [e.text for e in card.findall('.//s:text[@class="type"]',NS)]
    keys = [e.text for e in card.findall('.//s:text[@class="key"]',NS)]
    check(len(fields) == len(types) == len(keys), 'ERD 필드/키 표시 수')
    for name, kind, key in zip(fields,types,keys):
        check(next(c['type'] for c in table['columns'] if c['name']==name) == kind, 'ERD 자료형')
        check(key == '/'.join(k for k,s in [('PK',primary),('FK',foreign)] if name in s), 'ERD 키 표시')
metadata = json.loads(root.find('s:metadata',NS).text)
check(len(catalog) == metadata['total_public_tables'] == 16, 'DB 전체 테이블 수')
check(len(cards)-1 == metadata['displayed_public_tables'] == 15, '표시 테이블 수')
check(len(edges) == metadata['displayed_foreign_keys'] == 19 and identifying == 5, '표시 관계 수')
check(sum(c['kind']=='f' for t in catalog.values() for c in t['constraints']) - len(edges) == metadata['omitted_foreign_keys'] == 13, '생략 관계 수')
results['database'] = {'public_tables': 16, 'displayed_tables':15, 'verified_relations':19, 'identifying':5, 'non_identifying':14, 'omitted_relations':13}

package = json.loads((PRIVATE/'apps/web/package.json').read_text())
engineering = (PUBLIC/'docs/ENGINEERING.md').read_text()
for name in ['next','react','zod','@supabase/supabase-js','@supabase/ssr','workflow','@vercel/sandbox','openai','shiki','gsap']:
    check(package['dependencies'][name] in engineering, f'기술 버전 {name}')
check(package['devDependencies']['typescript'] in engineering, 'TypeScript 버전')
check(subprocess.run(['git','diff','--quiet','HEAD','FETCH_HEAD'],cwd=PRIVATE).returncode==0, '비공개 원격 main과 로컬 tree 일치')
check(not subprocess.check_output(['git','status','--porcelain'],cwd=PRIVATE,text=True), '비공개 작업 트리 보존')
check(subprocess.run(['git','diff','--check'],cwd=PUBLIC).returncode==0, 'diff 공백 검사')
results['source'] = {'package_versions':11, 'private_worktree_unchanged':True, 'private_remote_tree_matches':True}
(WORK/'verification.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
