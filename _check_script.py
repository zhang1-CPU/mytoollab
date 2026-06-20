# Now I'll write a completely clean replacement script for json-formatter.html
# Let me first verify the file structure around the script section

import re

with open('tools/text/json-formatter.html', 'r', encoding='utf-8', errors='replace') as fp:
    c = fp.read()

# Find the last <script> tag - this is the main tool script
positions = [(m.start(), m.end()) for m in re.finditer(r'<script\b[^>]*>', c)]
last_start = positions[-1][1]
last_end = c.rfind('</script>')

# Get everything before and after
before = c[:last_start]
after = c[last_end+9:]

print(f'Before script: {len(before)} chars')
print(f'Script content: {len(c[last_start:last_end])} chars')
print(f'After script: {len(after)} chars')

# Print last 100 chars of 'before'
print(f'\n--- End of "before": ---')
print(before[-200:])
print(f'\n--- Start of "after": ---')
print(after[:200])

# Now create the new script
new_script = """
(function() {
  'use strict';

  var inputEl = document.getElementById('inputText');
  var parseModeEl = document.getElementById('parseMode');
  var indentEl = document.getElementById('indentSize');
  var sortKeysEl = document.getElementById('sortKeys');
  var outputArea = document.getElementById('outputArea');
  var jsonpathInput = document.getElementById('jsonpathInput');
  var statusEl = document.getElementById('statusLabel');
  var treeRoot = document.getElementById('treeViewRoot');

  var lastData = null;

  function setStatus(msg, ok) {
    statusEl.textContent = msg;
    statusEl.style.color = (ok === true) ? '#047857' : (ok === false) ? '#b91c1c' : '#64748b';
  }

  // --- JSON5 tolerant parser ---
  function parseLoose(text) {
    var i = 0, len = text.length;

    function peek() {
      while (i < len) {
        var c = text.charAt(i);
        if (c === ' ' || c === '\t' || c === '\n' || c === '\r') { i++; continue; }
        if (c === '/' && text.charAt(i+1) === '/') { while (i < len && text.charAt(i) !== '\n') i++; continue; }
        if (c === '/' && text.charAt(i+1) === '*') {
          i += 2;
          while (i < len && !(text.charAt(i) === '*' && text.charAt(i+1) === '/')) i++;
          i += 2;
          continue;
        }
        break;
      }
      return i < len ? text.charAt(i) : '';
    }

    function parseValue() {
      peek();
      if (i >= len) throwError('Unexpected end of input');
      var c = text.charAt(i);
      if (c === '{') return parseObject();
      if (c === '[') return parseArray();
      if (c === '"' || c === "'") return parseString();
      if (c === '-' || (c >= '0' && c <= '9')) return parseNumber();
      if (c === 't' || c === 'f') return parseBoolean();
      if (c === 'n') return parseNull();
      // try identifier (unquoted key)
      if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c === '_' || c === '$') {
        return parseIdentOrKeyword();
      }
      throwError('Unexpected character: ' + c);
    }

    function parseObject() {
      i++; // skip {
      var obj = {};
      if (peek() === '}') { i++; return obj; }
      while (true) {
        peek();
        var key;
        var c = text.charAt(i);
        if (c === '"' || c === "'") {
          key = parseString();
        } else if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c === '_' || c === '$' || (c >= '0' && c <= '9')) {
          key = parseIdentifier();
        } else {
          throwError('Expected object key, got: ' + c);
        }
        peek();
        if (text.charAt(i) !== ':') throwError("Expected ':' after key");
        i++;
        obj[key] = parseValue();
        peek();
        c = text.charAt(i);
        if (c === ',') { i++; peek(); if (text.charAt(i) === '}') { i++; return obj; } continue; }
        if (c === '}') { i++; return obj; }
        throwError("Expected ',' or '}' in object, got: '" + c + "'");
      }
    }

    function parseArray() {
      i++; // skip [
      var arr = [];
      if (peek() === ']') { i++; return arr; }
      while (true) {
        arr.push(parseValue());
        peek();
        var c = text.charAt(i);
        if (c === ',') { i++; peek(); if (text.charAt(i) === ']') { i++; return arr; } continue; }
        if (c === ']') { i++; return arr; }
        throwError("Expected ',' or ']' in array, got: '" + c + "'");
      }
    }

    function parseString() {
      var quote = text.charAt(i);
      i++;
      var out = '';
      while (i < len && text.charAt(i) !== quote) {
        if (text.charAt(i) === '\\') {
          i++;
          var n = text.charAt(i);
          if (n === 'n') out += '\n';
          else if (n === 't') out += '\t';
          else if (n === 'r') out += '\r';
          else if (n === '\\') out += '\\';
          else if (n === '"') out += '"';
          else if (n === "'") out += "'";
          else if (n === '/') out += '/';
          else if (n === 'b') out += '\b';
          else if (n === 'f') out += '\f';
          else if (n === 'u') {
            out += String.fromCharCode(parseInt(text.substr(i+1, 4), 16));
            i += 4;
          }
          else out += n;
          i++;
        } else {
          out += text.charAt(i);
          i++;
        }
      }
      if (i >= len) throwError('Unterminated string');
      i++; // skip closing quote
      return out;
    }

    function parseNumber() {
      var start = i;
      if (text.charAt(i) === '-') i++;
      while (i < len && ((text.charAt(i) >= '0' && text.charAt(i) <= '9') || text.charAt(i) === '.' || text.charAt(i) === 'e' || text.charAt(i) === 'E' || text.charAt(i) === '+' || text.charAt(i) === '-')) i++;
      var num = text.substring(start, i);
      if (num === '-' || num === '' || num === '.' || num === '-.' || /e[-+]*$/i.test(num) || /\..*\./.test(num)) throwError('Invalid number: ' + num);
      if (/^-?(Infinity|NaN)$/.test(num)) return num === '-Infinity' ? -Infinity : (num === 'NaN' ? NaN : Infinity);
      return parseFloat(num);
    }

    function parseBoolean() {
      if (text.substr(i, 4) === 'true') { i += 4; return true; }
      if (text.substr(i, 5) === 'false') { i += 5; return false; }
      throwError('Invalid boolean at position ' + i);
    }

    function parseNull() {
      if (text.substr(i, 4) === 'null') { i += 4; return null; }
      throwError('Invalid value at position ' + i);
    }

    function parseIdentifier() {
      var start = i;
      while (i < len) {
        var c = text.charAt(i);
        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || c === '_' || c === '$') i++;
        else break;
      }
      return text.substring(start, i);
    }

    function parseIdentOrKeyword() {
      var ident = parseIdentifier();
      if (ident === 'true') return true;
      if (ident === 'false') return false;
      if (ident === 'null') return null;
      if (ident === 'Infinity') return Infinity;
      if (ident === 'NaN') return NaN;
      throwError('Unexpected identifier: ' + ident);
    }

    function throwError(msg) {
      var line = 1, col = 1;
      for (var k = 0; k < i && k < len; k++) {
        if (text.charAt(k) === '\n') { line++; col = 1; } else col++;
      }
      throw new Error(msg + ' at line ' + line + ', column ' + col);
    }

    var result = parseValue();
    peek();
    if (i < len) throwError('Unexpected trailing content');
    return result;
  }

  // --- Sort keys recursively ---
  function sortKeysDeep(v) {
    if (Array.isArray(v)) return v.map(sortKeysDeep);
    if (v && typeof v === 'object') {
      var sorted = {};
      Object.keys(v).sort().forEach(function(k) { sorted[k] = sortKeysDeep(v[k]); });
      return sorted;
    }
    return v;
  }

  function getIndent() {
    var val = indentEl.value;
    if (val === 'tab') return '\t';
    return parseInt(val, 10);
  }

  // --- JSONPath simple evaluator ---
  function jsonPathGet(obj, path) {
    if (!path || path === '$' || path === '') return obj;
    var parts = [];
    var i = 0;
    if (path.charAt(0) === '$') i = 1;
    while (i < path.length) {
      var c = path.charAt(i);
      if (c === '.') {
        i++;
        var start = i;
        while (i < path.length && path.charAt(i) !== '.' && path.charAt(i) !== '[') i++;
        parts.push({type: 'key', value: path.substring(start, i)});
      } else if (c === '[') {
        i++;
        if (path.charAt(i) === "'" || path.charAt(i) === '"') {
          var q = path.charAt(i); i++;
          var keyStart = i;
          while (i < path.length && path.charAt(i) !== q) i++;
          parts.push({type: 'key', value: path.substring(keyStart, i)});
          if (path.charAt(i) === q) i++;
          if (path.charAt(i) === ']') i++;
        } else {
          var numStart = i;
          while (i < path.length && path.charAt(i) !== ']') i++;
          parts.push({type: 'index', value: path.substring(numStart, i)});
          if (path.charAt(i) === ']') i++;
        }
      } else {
        // bare key
        var kStart = i;
        while (i < path.length && path.charAt(i) !== '.' && path.charAt(i) !== '[') i++;
        parts.push({type: 'key', value: path.substring(kStart, i)});
      }
    }
    var current = obj;
    for (var p = 0; p < parts.length; p++) {
      var part = parts[p];
      if (current === null || current === undefined) return undefined;
      if (part.type === 'index') {
        if (part.value === '*' || part.value === '') {
          // noop on arrays, return current (not fully supported)
          continue;
        }
        var idx = parseInt(part.value, 10);
        if (isNaN(idx)) return undefined;
        current = current[idx];
      } else {
        current = current[part.value];
      }
    }
    return current;
  }

  // --- Tree view generator ---
  function buildTree(data, parentId, level) {
    if (level === undefined) level = 0;
    if (level > 20) return '(nesting too deep)';
    var html = '';
    if (data === null) return '<span style="color:#64748b">null</span>';
    if (typeof data === 'boolean') return '<span style="color:#b45309">' + data + '</span>';
    if (typeof data === 'number') return '<span style="color:#7c3aed">' + data + '</span>';
    if (typeof data === 'string') return '<span style="color:#047857">"'+escapeHtml(data)+'"</span>';
    if (Array.isArray(data)) {
      if (data.length === 0) return '[ ]';
      html += '[ ';
      for (var i = 0; i < data.length; i++) {
        html += buildTree(data[i], parentId + '.' + i, level+1);
        if (i < data.length-1) html += ', ';
      }
      html += ' ]';
      return html;
    }
    if (typeof data === 'object') {
      var keys = Object.keys(data);
      if (keys.length === 0) return '{ }';
      html += '{ ';
      for (var k = 0; k < keys.length; k++) {
        html += '<span style="color:#b91c1c">"'+escapeHtml(keys[k])+'"</span>: ';
        html += buildTree(data[keys[k]], parentId + '.' + k, level+1);
        if (k < keys.length-1) html += ', ';
      }
      html += ' }';
      return html;
    }
    return String(data);
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>]/g, function(c) {
      return '&amp;<>&'.indexOf(c) === 0 ? '&amp;' : (c === '<' ? '&lt;' : '&gt;');
    });
  }

  // --- Syntax highlighting for formatted JSON ---
  function highlightJson(text) {
    var out = '';
    var i = 0;
    while (i < text.length) {
      var c = text.charAt(i);
      if (c === '"') {
        // string - determine if it's a key or value
        var start = i;
        i++;
        while (i < text.length && text.charAt(i) !== '"') {
          if (text.charAt(i) === '\\') i += 2;
          else i++;
        }
        i++;
        var str = text.substring(start, i);
        // look ahead for colon to detect key
        var j = i;
        while (j < text.length && (text.charAt(j) === ' ' || text.charAt(j) === '\t')) j++;
        if (text.charAt(j) === ':') out += '<span style="color:#b91c1c">' + escapeHtml(str) + '</span>';
        else out += '<span style="color:#047857">' + escapeHtml(str) + '</span>';
      } else if (c === '-' || (c >= '0' && c <= '9')) {
        var s = i;
        while (i < text.length && ((text.charAt(i) >= '0' && text.charAt(i) <= '9') || text.charAt(i) === '.' || text.charAt(i) === 'e' || text.charAt(i) === 'E' || text.charAt(i) === '+' || text.charAt(i) === '-')) i++;
        out += '<span style="color:#7c3aed">' + escapeHtml(text.substring(s, i)) + '</span>';
      } else if (c === 't' && text.substr(i, 4) === 'true') { out += '<span style="color:#b45309">true</span>'; i += 4; }
      else if (c === 'f' && text.substr(i, 5) === 'false') { out += '<span style="color:#b45309">false</span>'; i += 5; }
      else if (c === 'n' && text.substr(i, 4) === 'null') { out += '<span style="color:#64748b">null</span>'; i += 4; }
      else if (c === '{' || c === '[' || c === '}' || c === ']') { out += '<span style="color:#1e293b;font-weight:600">' + c + '</span>'; i++; }
      else { out += escapeHtml(c); i++; }
    }
    return out;
  }

  // --- Main render function ---
  function render(viewMode) {
    var input = inputEl.value;
    if (!input || !input.trim()) {
      outputArea.innerHTML = '';
      if (treeRoot) treeRoot.innerHTML = '';
      setStatus('Ready');
      lastData = null;
      return;
    }

    var data;
    try {
      if (parseModeEl.value === 'json5') data = parseLoose(input);
      else data = JSON.parse(input);
      lastData = data;
    } catch (e) {
      outputArea.innerHTML = '<div style="padding:12px;border:1px solid #fecaca;border-radius:6px;background:#fef2f2;color:#b91c1c"><strong>Parse error:</strong> ' + escapeHtml(e.message) + '</div>';
      if (treeRoot) treeRoot.innerHTML = '';
      setStatus('Parse error', false);
      return;
    }

    if (sortKeysEl && sortKeysEl.checked) data = sortKeysDeep(data);

    var mode = viewMode || (outputArea.dataset.viewMode || 'highlighted');
    outputArea.dataset.viewMode = mode;

    if (mode === 'minified') {
      outputArea.innerHTML = '<pre style="background:#0f172a;color:#e2e8f0;padding:12px;border-radius:6px;overflow:auto;white-space:pre-wrap;word-break:break-all">' + escapeHtml(JSON.stringify(data)) + '</pre>';
    } else {
      var formatted = JSON.stringify(data, null, getIndent());
      outputArea.innerHTML = '<pre style="background:#0f172a;color:#e2e8f0;padding:12px;border-radius:6px;overflow:auto;white-space:pre-wrap">' + highlightJson(formatted) + '</pre>';
    }

    // Tree view
    if (treeRoot) {
      treeRoot.innerHTML = '<div style="background:#f8fafc;padding:12px;border-radius:6px;border:1px solid #e2e8f0;overflow:auto;white-space:pre-wrap;max-height:400px">' + buildTree(data, '', 0) + '</div>';
    }

    // JSONPath
    var jpValue = jsonpathInput.value.trim();
    if (jpValue && lastData !== null) {
      try {
        var result = jsonPathGet(lastData, jpValue);
        var jpOut = document.getElementById('jsonpathOutput');
        if (jpOut) {
          var rendered = (result === undefined) ? '<em style="color:#64748b">No match</em>' : '<pre style="background:#f1f5f9;padding:8px;border-radius:6px;overflow:auto;white-space:pre-wrap;margin:4px 0">'+escapeHtml(JSON.stringify(result, null, 2))+'</pre>';
          jpOut.innerHTML = rendered;
        }
      } catch (err) {
        var jpOut = document.getElementById('jsonpathOutput');
        if (jpOut) jpOut.innerHTML = '<div style="color:#b91c1c">' + escapeHtml(err.message) + '</div>';
      }
    } else {
      var jpOut = document.getElementById('jsonpathOutput');
      if (jpOut) jpOut.innerHTML = '';
    }

    var bytes = (new Blob([JSON.stringify(data)])).size;
    setStatus('Parsed successfully (' + bytes + ' bytes)', true);
  }

  function getCurrentText() {
    if (!lastData) return '';
    var mode = outputArea.dataset.viewMode || 'highlighted';
    var d = sortKeysEl && sortKeysEl.checked ? sortKeysDeep(lastData) : lastData;
    return (mode === 'minified') ? JSON.stringify(d) : JSON.stringify(d, null, getIndent());
  }

  // --- Event handlers ---
  document.getElementById('sampleBtn').addEventListener('click', function() {
    inputEl.value = JSON.stringify({
      name: "zlbox Tools",
      version: 1.0,
      active: true,
      tags: ["text", "json", "formatter"],
      nested: { key1: "value1", key2: [1, 2, 3] }
    }, null, 2);
    render();
  });
  document.getElementById('clearBtn').addEventListener('click', function() {
    inputEl.value = '';
    if (treeRoot) treeRoot.innerHTML = '';
    outputArea.innerHTML = '';
    var jpOut = document.getElementById('jsonpathOutput');
    if (jpOut) jpOut.innerHTML = '';
    setStatus('Ready');
    lastData = null;
    inputEl.focus();
  });
  document.getElementById('formatBtn').addEventListener('click', function() { render('highlighted'); });
  document.getElementById('minifyBtn').addEventListener('click', function() { render('minified'); });
  document.getElementById('copyBtn').addEventListener('click', function() {
    var txt = getCurrentText();
    if (!txt) return;
    if (navigator.clipboard) {
      navigator.clipboard.writeText(txt).then(function() { setStatus('Copied to clipboard', true); });
    } else {
      var ta = document.createElement('textarea');
      ta.value = txt;
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); setStatus('Copied', true); }
      catch (e) { setStatus('Copy failed', false); }
      document.body.removeChild(ta);
    }
  });
  document.getElementById('downloadBtn').addEventListener('click', function() {
    var txt = getCurrentText();
    if (!txt) return;
    var blob = new Blob([txt], { type: 'application/json' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = (outputArea.dataset.viewMode === 'minified') ? 'data.min.json' : 'data.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function() { URL.revokeObjectURL(url); }, 1000);
  });

  parseModeEl.addEventListener('change', function() { render(); });
  indentEl.addEventListener('change', function() { render(); });
  if (sortKeysEl) sortKeysEl.addEventListener('change', function() { render(); });
  inputEl.addEventListener('input', function() { render(); });
  jsonpathInput.addEventListener('input', function() { render(); });

  // Set initial status
  setStatus('Ready');
})();
"""

# Write the new file
output = before + new_script + after
with open('tools/text/json-formatter.html', 'w', encoding='utf-8') as fp:
    fp.write(output)

print(f'File written, size: {len(output)} chars')

# Validate with node
import subprocess
with open('/tmp/_validate.js', 'w') as tf:
    tf.write(new_script)
result = subprocess.run(['node', '--check', '/tmp/_validate.js'], capture_output=True, timeout=10)
print(f'Node validation: {"OK" if result.returncode == 0 else "FAILED"}')
if result.returncode != 0:
    print(result.stderr.decode()[:500])
