"""Validate Thai catalog coverage, Rust format signatures and unchanged numeric values."""
from pathlib import Path
import collections,json,re,sys
ROOT=Path(__file__).resolve().parents[2]
LOCALES=ROOT/'crates/ui-egui/locales'
def signature(text):
 result=[];auto=0
 for m in re.finditer(r'(?<!\{)\{([^{}]*)\}(?!\})',text):
  name,_,spec=m[1].partition(':')
  if not name:name=str(auto);auto+=1
  result.append((name,spec))
 return tuple(sorted(result))
def digits(text):
 return collections.Counter(re.findall(r'\d+(?:[.,]\d+)*',re.sub(r'\{[^{}]*\}','',text)))
errors=[];report={}
for suffix in ['', '-formats']:
 name='th'+suffix+'.json';file=LOCALES/name
 def pairs(items):
  result={}
  for k,v in items:
   if k in result:errors.append([name,k,'duplicate key'])
   result[k]=v
  return result
 data=json.loads(file.read_text(encoding='utf-8'),object_pairs_hook=pairs);refs={}
 for other in LOCALES.glob('*.json'):
  if other.name.startswith('th') or other.name.endswith('-formats.json')!=bool(suffix):continue
  for k,v in json.loads(other.read_text(encoding='utf-8')).items():refs.setdefault(k,[]).append(v)
 for k in refs:
  if not data.get(k):errors.append([name,k,'missing reference translation'])
 for k,v in data.items():
  if not isinstance(v,str) or not v.strip():errors.append([name,k,'empty/non-string translation']);continue
  allowed={signature(k)}|{signature(s) for s in refs.get(k,[])}
  if signature(v) not in allowed:errors.append([name,k,'Rust format signature differs'])
  if digits(k)!=digits(v):errors.append([name,k,'fixed numeric values differ'])
  if collections.Counter(re.findall(r'`([^`]+)`',k))!=collections.Counter(re.findall(r'`([^`]+)`',v)):errors.append([name,k,'inline code identifier differs'])
  if any(c in v for c in '▸▾✕'):errors.append([name,k,'unpaintable menu character'])
 report[name]={'entries':len(data),'referenceKeys':len(refs),'thaiScriptValues':sum(bool(re.search(r'[\u0e00-\u0e7f]',v)) for v in data.values())}
result={'status':'passed' if not errors else 'failed','catalogs':report,'errors':errors,'scope':'Static catalog validation; compiled source scan and native UI checks are separate'}
print(json.dumps(result,ensure_ascii=False,indent=2))
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(bool(errors))
