import re

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 3. render logic
    if "else if (q.type === 'grid')" not in content:
        content = re.sub(r'(\} else \{\s*const isMulti = q\.type === \'multi\')', r'''  } else if (q.type === 'grid') {
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
\1''', content)
        print("Updated render logic")

    # 4. onGridChange
    if "function onGridChange(" not in content:
        content = re.sub(r'(function onOptionChange\(qId, optIdx\) \{)', r'''function onGridChange(qId, rowIdx, colIdx) {
  if (userChecked[qId]) return;
  if (!userSelections[qId]) {
    userSelections[qId] = [];
  }
  userSelections[qId][rowIdx] = colIdx;
  renderQuestion();
}

\1''', content)
        print("Updated onGridChange")

    # 5. checkCurrentQuestion
    if "if (answered < q.rows.length) {" not in content:
        content = re.sub(r'(\} else \{\s*const selected = userSelections\[q\.id\] \|\| \[\];\s*if \(selected\.length === 0\) \{)', r'''  } else if (q.type === 'grid') {
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
\1''', content)
        print("Updated checkCurrentQuestion")
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

update_file('index.html')
update_file('cuestionario_com.html')
