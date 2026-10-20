import hashlib,json,sys,time
from pathlib import Path
root=Path(__file__).resolve().parent
p=(root/'official-skills'/sys.argv[1]).resolve()
assert p.is_relative_to((root/'official-skills').resolve()) and p.is_file()
b=p.read_bytes()
with (root/'.skill-reads.jsonl').open('a') as f:
 f.write(json.dumps({'path':p.relative_to(root/'official-skills').as_posix(),'sha256':hashlib.sha256(b).hexdigest(),'read_at':time.time()})+'\n')
sys.stdout.buffer.write(b)
