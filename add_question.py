import sys

def insert_question(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    question_json = """  ,{
    id: 999, text: "Empareje el material con el espacio que corresponde (según cable coaxial):",
    type: "grid",
    rows: ["Aislante", "hilo de acero galvanizado", "Núcleo solido de cobre", "funda de PVC semirrígido", "La malla de hilo trenzada", "recubrimiento de fibra sintética", "Una cubierta de esmalte de plastico"],
    columns: ["ESPACIO 1", "ESPACIO 2", "ESPACIO 3", "ESPACIO 4", "NO CORRESPONDE"],
    correct: [1, 4, 0, 4, 2, 4, 3]
  }"""
    
    # insert right before the first occurrence of `];`
    idx = content.find('\n];')
    if idx != -1:
        content = content[:idx] + question_json + content[idx:]
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added question to {filename}")
    else:
        print(f"Could not find end of array in {filename}")

insert_question('index.html')
insert_question('cuestionario_com.html')
