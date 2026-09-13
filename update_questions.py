import re

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add grid question to the end of the questions array
    question_json = """  {
    id: 999, text: "Empareje el material con el espacio que corresponde (según cable coaxial):",
    type: "grid",
    rows: ["Aislante", "hilo de acero galvanizado", "Núcleo solido de cobre", "funda de PVC semirrígido", "La malla de hilo trenzada", "recubrimiento de fibra sintética", "Una cubierta de esmalte de plastico"],
    columns: ["ESPACIO 1", "ESPACIO 2", "ESPACIO 3", "ESPACIO 4", "NO CORRESPONDE"],
    correct: [1, 4, 0, 4, 2, 4, 3]
  }"""
    
    # Insert before the last bracket of the array (we assume it's right before "// === MEDIOS DE TRANSMISIÓN ===" or just find a good place.
    # Actually, better to append right before the end of the `const questions = [...]` block.
    # Wait, the array name is `const questions = [`. I'll search for `];\n\n//` or `];\nlet currentQuestions`
    
    # We can just insert it after the question 83
    q_insert_idx = content.find('id: 83')
    if q_insert_idx != -1:
        end_of_q83 = content.find('},', q_insert_idx) + 2
        content = content[:end_of_q83] + "\n" + question_json + "," + content[end_of_q83:]

    # 2. Add badgeText for grid
    grid_badge = """  } else if (q.type === 'grid') {
    badgeClass = 'badge-multi';
    badgeText = 'Emparejamiento (Grilla)';
  }"""
    content = content.replace("badgeText = 'Selección múltiple';\n  }", "badgeText = 'Selección múltiple';\n  }\n" + grid_badge)

    # 3. Add render logic for grid
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
"""
    content = content.replace("  } else {\n    const isMulti =", grid_render + "  } else {\n    const isMulti =")

    # 4. Add onGridChange
    grid_change = """
function onGridChange(qId, rowIdx, colIdx) {
  if (userChecked[qId]) return;
  if (!userSelections[qId]) {
    userSelections[qId] = [];
  }
  userSelections[qId][rowIdx] = colIdx;
  renderQuestion();
}
"""
    content = content.replace("function onOptionChange(qId, optIdx) {", grid_change + "\nfunction onOptionChange(qId, optIdx) {")

    # 5. Add checkCurrentQuestion logic
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
"""
    content = content.replace("  } else {\n    const selected = userSelections[q.id]", grid_check + "  } else {\n    const selected = userSelections[q.id]")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

update_file('index.html')
update_file('cuestionario_com.html')
print("Done")
