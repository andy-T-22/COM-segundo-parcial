import re

def clean_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove duplicate badgeText
    dup_badge = """  } else if (q.type === 'grid') {
    badgeClass = 'badge-multi';
    badgeText = 'Emparejamiento (Grilla)';
  }
  } else if (q.type === 'grid') {
    badgeClass = 'badge-multi';
    badgeText = 'Emparejamiento (Grilla)';
  }"""
    clean_badge = """  } else if (q.type === 'grid') {
    badgeClass = 'badge-multi';
    badgeText = 'Emparejamiento (Grilla)';
  }"""
    content = content.replace(dup_badge, clean_badge)

    # 2. Remove duplicate question 999 (the one around line 1412)
    q_pattern = r'  \{\s*id: 999, text: "Empareje el material con el espacio que corresponde \(según cable coaxial\):",\s*type: "grid",\s*rows: \[.*?\],\s*columns: \[.*?\],\s*correct: \[.*?\]\s*\},'
    # we'll find all and just replace the first one with empty string if there are multiple
    matches = list(re.finditer(q_pattern, content, re.DOTALL))
    if len(matches) > 0:
        # Just replace the first occurrence
        content = content[:matches[0].start()] + content[matches[0].end():]
        print(f"Removed duplicate id 999 in {filename}")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

clean_file('index.html')
clean_file('cuestionario_com.html')
