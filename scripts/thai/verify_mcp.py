"""Verify the bundled CLI's actual MCP handshake and advertised tools, without file edits."""
import json,subprocess,sys,queue,threading,time,os,tempfile
from pathlib import Path
binary,out=sys.argv[1:]
args=[binary,'mcp','--demo']
profile=tempfile.TemporaryDirectory(prefix='lightcraft-th-mcp-')
p=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',bufsize=1,env=dict(os.environ,LIGHTCRAFT_CONFIG_DIR=profile.name))
responses=queue.Queue()
def read_stdout():
    for line in p.stdout:responses.put(line)
    responses.put(None)
threading.Thread(target=read_stdout,daemon=True).start()
def call(payload):
    p.stdin.write(json.dumps(payload)+'\n');p.stdin.flush()
    deadline=time.monotonic()+30
    while time.monotonic()<deadline:
        try:line=responses.get(timeout=1)
        except queue.Empty:
            if p.poll() is not None:raise RuntimeError('CLI MCP exited early')
            continue
        if not line:raise RuntimeError('MCP stdout closed')
        reply=json.loads(line)
        if reply.get('id')==payload.get('id'):
            if 'error' in reply:raise RuntimeError(reply['error'])
            return reply['result']
    raise TimeoutError('MCP response timeout')
try:
    init=call({'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'Thai-release-check','version':'1.0.0'}}})
    p.stdin.write(json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'})+'\n');p.stdin.flush()
    tools=call({'jsonrpc':'2.0','id':2,'method':'tools/list','params':{}})
    assert tools.get('tools'),'No MCP tools advertised'
    result={'cli':binary,'initialization':init,'toolCount':len(tools['tools']),'tools':[t['name'] for t in tools['tools']],'status':'passed'}
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    Path(out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('MCP handshake and tools/list passed:',result['toolCount'],'tools')
finally:
    p.terminate()
    try:p.wait(timeout=5)
    except subprocess.TimeoutExpired:p.kill();p.wait()

    profile.cleanup()
