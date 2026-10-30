"""아키텍처의 화살표 도착점과 카드 강조를 표준 라이브러리로 확인한다."""
from pathlib import Path
from decimal import Decimal
import re
import xml.etree.ElementTree as ET

source = Path(__file__).resolve().parents[1] / 'assets/diagrams/architecture.svg'
root = ET.parse(source).getroot()
ns = {'s': 'http://www.w3.org/2000/svg'}
nodes = root.findall('.//*[@data-node]')
flows = root.findall('.//*[@data-step]')
pulses = root.findall('.//s:rect[@class="node-pulse"]', ns)
assert len(nodes) == 8 and len(flows) == len(pulses) == 23
assert len({flow.get('style') for flow in flows}) == len(flows)
starts = [Decimal(re.search(r'--at:([\d.]+)s', flow.get('style'))[1]) for flow in flows]
assert starts == [Decimal('1.2') * index for index in range(23)]

for flow in flows:
    tip = flow.find('s:path[@class="tip"]', ns)
    # 화살촉의 가운데 꼭짓점이 실제 도착점이다.
    x, y = map(float, re.findall(r'-?\d+(?:\.\d+)?', tip.get('d'))[2:4])
    targets = []
    for node in nodes:
        card = node.find('s:rect[@class="card"]', ns)
        left, top, width, height = (float(card.get(k)) for k in ('x', 'y', 'width', 'height'))
        dx = max(left - x, 0, x - left - width)
        dy = max(top - y, 0, y - top - height)
        if dx * dx + dy * dy == 12 * 12:
            targets.append(node)
    assert len(targets) == 1, flow.get('data-step')
    matches = [p for p in pulses if p.get('style') == flow.get('style')]
    assert len(matches) == 1 and matches[0] in list(targets[0]), flow.get('data-step')
    card = targets[0].find('s:rect[@class="card"]', ns)
    for attr in ('x', 'y', 'width', 'height', 'rx'):
        assert matches[0].get(attr) == card.get(attr), (flow.get('data-step'), attr)
    assert matches[0].get('aria-hidden') == 'true'

ids = [element.get('id') for element in root.iter() if element.get('id')]
assert len(ids) == len(set(ids))
for element in root.iter():
    assert element.tag.split('}')[-1] not in ('script', 'foreignObject')
    for name, value in element.attrib.items():
        assert not name.lower().startswith('on')
        if name.split('}')[-1] == 'href':
            assert value.startswith('#')
for target in re.findall(r'url\(#([^)]*)\)', source.read_text()):
    assert target in ids
assert 'prefers-reduced-motion:reduce' in source.read_text()
print('PASS: SVG XML, 8 cards, 23 arrival targets, matching outlines, accessibility, internal references')
