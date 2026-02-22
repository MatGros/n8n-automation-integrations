from pathlib import Path
p = Path('workflows/inbox/smart-gmail-labeler-reply-draft_PUB_20260221.json')
print('stem ->', p.stem)
print('metadata path ->', p.with_name(p.stem + '.metadata.json'))
