import re
import sys

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add question
    if "id: 999" not in content:
        q_insert_idx = content.find('id: 83')
        if q_insert_idx != -1:
            end_of_q83 = content.find('},', q_insert_idx) + 2
            
            question_json = """  {
    id: 999, text: "Empareje el material con el espacio que corresponde (según cable coaxial):",
    type: "grid",
    rows: ["Aislante", "hilo de acero galvanizado", "Núcleo solido de cobre", "funda de PVC semirrígido", "La malla de hilo trenzada", "recubrimiento de fibra sintética", "Una cubierta de esmalte de plastico"],
    columns: ["ESPACIO 1", "ESPACIO 2", "ESPACIO 3", "ESPACIO 4", "NO CORRESPONDE"],
    correct: [1, 4, 0, 4, 2, 4, 3]
  }"""
            content = content[:end_of_q83] + "\n" + question_json + "," + content[end_of_q83:]
            print(f"Added question to {filename}")
        else:
            print(f"Could not find id: 83 in {filename}")
    else:
        print(f"Question already in {filename}")

    # 2. badgeText
    if "badgeClass = 'badge-multi';\\n    badgeText = 'Emparejamiento (Grilla)';" not in content:
        # Let's search via regex or substring for the exact block
        search_badge = "badgeText = 'Selección múltiple';\n  }"
        if search_badge in content:
            grid_badge = "badgeText = 'Selección múltiple';\n  } else if (q.type === 'grid') {\n    badgeClass = 'badge-multi';\n    badgeText = 'Emparejamiento (Grilla)';\n  }"
            content = content.replace(search_badge, grid_badge)
            print("Added badgeText")
        else:
            print("Could not find badgeText to replace")

    # 3. render logic
    if "else if (q.type === 'grid')" not in content:
        search_render = "  } else {\n    const isMulti ="
        if search_render in content:
            grid_render = """  } else if (q.type === 'grid') {
    const selectedRows = userSelections[q.id] || [];
    html += `<div style="overflow-x:auto; margin-top:15px; border-radius: 8px; border: 1px solid var(--border);">
      <table style="width:100%; border-collapse: collapse; text-align:center; min-width: 600px;">
        <thead>
          <tr style="background: var(--bg-card-hover); border-bottom: 2px solid var(--border);">
            <th style="padding:12px; text-align:left; border-right: 1px solid var(--border);">Elemento</th>
            ${q.columns.map(c => `<th style="padding:12px; font-weight:600;">${c}</th>`).join('')}
          </tr>
        </thead>
        <tbody>
    `;
    q.rows.forEach((r, rIdx) => {
      let rowStyle = 'border-bottom: 1px solid var(--border);';
      let rowBg = '';
      if (isChecked) {
        const isCorrectChoice = selectedRows[rIdx] === q.correct[rIdx];
        if (selectedRows[rIdx] !== undefined) {
           rowBg = isCorrectChoice ? 'background: var(--success-bg);' : 'background: var(--danger-bg);';
        }
      }
      html += `<tr style="${rowStyle} ${rowBg}">
        <td style="padding:12px; text-align:left; border-right: 1px solid var(--border);">${r}</td>
        ${q.columns.map((c, cIdx) => {
          const isSel = selectedRows[rIdx] === cIdx;
          const isCorrectAns = q.correct[rIdx] === cIdx;
          let extra = '';
          if (isChecked && isCorrectAns) {
             extra = '<br><span style="color:var(--success); font-weight:bold; font-size:12px;">✓</span>';
          }
          return `<td style="padding:12px;">
            <input type="radio" name="q${q.id}_r${rIdx}" 
              ${isSel ? 'checked' : ''} 
              ${isChecked ? 'disabled' : ''} 
              onchange="onGridChange(${q.id}, ${rIdx}, ${cIdx})">
              ${extra}
          </td>`;
        }).join('')}
      </tr>`;
    });
    html += `</tbody></table></div>`;
  } else {
    const isMulti ="""
            content = content.replace(search_render, grid_render)
            print("Added render logic")
        else:
            print("Could not find render logic to replace")
            
    # 4. onGridChange
    if "function onGridChange(" not in content:
        search_on_option = "function onOptionChange(qId, optIdx) {"
        if search_on_option in content:
            grid_change = """
function onGridChange(qId, rowIdx, colIdx) {
  if (userChecked[qId]) return;
  if (!userSelections[qId]) {
    userSelections[qId] = [];
  }
  userSelections[qId][rowIdx] = colIdx;
  renderQuestion();
}

function onOptionChange(qId, optIdx) {"""
            content = content.replace(search_on_option, grid_change)
            print("Added onGridChange")
        else:
            print("Could not find onOptionChange to replace")

    # 5. checkCurrentQuestion
    if "if (answered < q.rows.length) {" not in content:
        search_check = "  } else {\n    const selected = userSelections[q.id]"
        if search_check in content:
            grid_check = """  } else if (q.type === 'grid') {
    const selected = userSelections[q.id] || [];
    let answered = 0;
    for (let i=0; i<q.rows.length; i++) {
        if (selected[i] !== undefined) answered++;
    }
    if (answered < q.rows.length) {
      alert('⚠️ Por favor responde a todas las filas antes de verificar.');
      return;
    }
    let correctCount = 0;
    q.correct.forEach((corrCol, rIdx) => {
      if (selected[rIdx] === corrCol) correctCount++;
    });
    score = correctCount / q.rows.length;
    isCorrect = score === 1.0;
    isPartial = score > 0 && score < 1.0;
    
    userChecked[q.id] = true;
    answers[q.id] = { selected, score, isCorrect, isPartial, correctSelectedCount: correctCount, totalCorrect: q.rows.length };
  } else {
    const selected = userSelections[q.id]"""
            content = content.replace(search_check, grid_check)
            print("Added checkCurrentQuestion logic")
        else:
            print("Could not find checkCurrentQuestion to replace")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updating index.html")
update_file('index.html')
print("Updating cuestionario_com.html")
update_file('cuestionario_com.html')
