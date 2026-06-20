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

  function escapeHtml(s) {
    return String(s).replace(/[&<>]/g, function(c) {
      return c === '&' ? '&amp;' : c === '<' ? '&lt;' : '&gt;';
    });
  }

  function parseLoose(text) {
    var i = 0, len = text.length;

    function peek() {
      while (i < len) {
        var ch = text.charAt(i);
        if (ch === ' ' || ch === '\t' || ch === '\n' || ch === '\r') { i++; continue; }
        if (ch === '/' && text.charAt(i+1) === '/') { while (i < len && text.charAt(i) !== '\n') i++; continue; }
        if (ch === '/' && text.charAt(i+1) === '*') {
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
      if (i >= len) throw new Error('Unexpected end of input');
      var c = text.charAt(i);
      if (c === '{') return parseObject();
      if (c === '[') return parseArray();
      if (c === '"' || c === "'") return parseString();
      if (c === '-' || (c >= '0' && c <= '9')) return parseNumber();
      if (c === 't' || c === 'f') return parseBoolean();
      if (c === 'n') return parseNull();
      if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c === '_' || c === '$') return parseIdent();
      throw new Error('Unexpected character at position ' + i + ': ' + c);
    }

    function parseObject() {
      i++;
      var obj = {};
      if (peek() === '}') { i++; return obj; }
      while (true) {
        peek();
        var key, c = text.charAt(i);
        if (c === '"' || c === "'") key = parseString();
        else if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c === '_' || c === '$' || (c >= '0' && c <= '9')) key = parseIdentifier();
        else throw new Error('Expected object key at position ' + i);
        peek();
        if (text.charAt(i) !== ':') throw new Error('Expected : at position ' + i);
        i++;
        obj[key] = parseValue();
        peek();
        c = text.charAt(i);
        if (c === ',') { i++; peek(); if (text.charAt(i) === '}') { i++; return obj; } continue; }
        if (c === '}') { i++; return obj; }
        throw new Error('Expected comma or closing brace at position ' + i);
      }
    }

    function parseArray() {
      i++;
      var arr = [];
      if (peek() === ']') { i++; return arr; }
      while (true) {
        arr.push(parseValue());
        peek();
        var c = text.charAt(i);
        if (c === ',') { i++; peek(); if (text.charAt(i) === ']') { i++; return arr; } continue; }
        if (c === ']') { i++; return arr; }
        throw new Error('Expected comma or closing bracket at position ' + i);
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
          else if (n === 'u') { out += String.fromCharCode(parseInt(text.substr(i+1, 4), 16)); i += 4; }
          else out += n;
          i++;
        } else {
          out += text.charAt(i);
          i++;
        }
      }
      if (i >= len) throw new Error('Unterminated string');
      i++;
      return out;
    }

    function parseNumber() {
      var start = i;
      if (text.charAt(i) === '-') i++;
      while (i < len) {
        var ch = text.charAt(i);
        if ((ch >= '0' && ch <= '9') || ch === '.' || ch === 'e' || ch === 'E' || ch === '+' || ch === '-') i++;
        else break;
      }
      var num = text.substring(start, i);
      if (num === '-' || num === '' || /e[-+]*$/i.test(num) || /\..*\./.test(num)) throw new Error('Invalid number: ' + num);
      if (/^-?(Infinity|NaN)$/.test(num)) return num.charAt(0) === '-' ? -Infinity : (num === 'NaN' ? NaN : Infinity);
      return parseFloat(num);
    }

    function parseBoolean() {
      if (text.substr(i, 4) === 'true') { i += 4; return true; }
      if (text.substr(i, 5) === 'false') { i += 5; return false; }
      throw new Error('Invalid boolean at position ' + i);
    }

    function parseNull() {
      if (text.substr(i, 4) === 'null') { i += 4; return null; }
      throw new Error('Invalid value at position ' + i);
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

    function parseIdent() {
      var ident = parseIdentifier();
      if (ident === 'true') return true;
      if (ident === 'false') return false;
      if (ident === 'null') return null;
      if (ident === 'Infinity') return Infinity;
      if (ident === 'NaN') return NaN;
      throw new Error('Unexpected identifier: ' + ident);
    }

    return parseValue();
  }

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

  function jsonPathGet(obj, path) {
    if (!path || path === '$' || path === '') return obj;
    var parts = [];
    var p = 0;
    if (path.charAt(0) === '$') p = 1;
    while (p < path.length) {
      var c = path.charAt(p);
      if (c === '.') {
        p++;
        var start = p;
        while (p < path.length && path.charAt(p) !== '.' && path.charAt(p) !== '[') p++;
        parts.push({type: 'key', value: path.substring(start, p)});
      } else if (c === '[') {
        p++;
        if (path.charAt(p) === "'" || path.charAt(p) === '"') {
          var q = path.charAt(p); p++;
          var kStart = p;
          while (p < path.length && path.charAt(p) !== q) p++;
          parts.push({type: 'key', value: path.substring(kStart, p)});
          if (p < path.length && path.charAt(p) === q) p++;
          if (p < path.length && path.charAt(p) === ']') p++;
        } else {
          var nStart = p;
          while (p < path.length && path.charAt(p) !== ']') p++;
          parts.push({type: 'index', value: path.substring(nStart, p)});
          if (p < path.length && path.charAt(p) === ']') p++;
        }
      } else {
        var kS = p;
        while (p < path.length && path.charAt(p) !== '.' && path.charAt(p) !== '[') p++;
        parts.push({type: 'key', value: path.substring(kS, p)});
      }
    }
    var current = obj;
    for (var idx = 0; idx < parts.length; idx++) {
      var part = parts[idx];
      if (current === null || current === undefined) return undefined;
      if (part.type === 'index') {
        if (part.value === '*' || part.value === '') continue;
        var n = parseInt(part.value, 10);
        if (isNaN(n)) return undefined;
        current = current[n];
      } else {
        current = current[part.value];
      }
    }
    return current;
  }

  function highlightJson(text) {
    var out = '';
    var p = 0;
    while (p < text.length) {
      var c = text.charAt(p);
      if (c === '"') {
        var strStart = p;
        p++;
        while (p < text.length && text.charAt(p) !== '"') {
          if (text.charAt(p) === '\\') p += 2;
          else p++;
        }
        p++;
        var str = text.substring(strStart, p);
        var q = p;
        while (q < text.length && (text.charAt(q) === ' ' || text.charAt(q) === '\t')) q++;
        if (text.charAt(q) === ':') out += '<span style="color:#b91c1c">' + escapeHtml(str) + '</span>';
        else out += '<span style="color:#047857">' + escapeHtml(str) + '</span>';
      } else if (c === '-' || (c >= '0' && c <= '9')) {
        var numStart = p;
        while (p < text.length) {
          var cc = text.charAt(p);
          if ((cc >= '0' && cc <= '9') || cc === '.' || cc === 'e' || cc === 'E' || cc === '+' || cc === '-') p++;
          else break;
        }
        out += '<span style="color:#7c3aed">' + escapeHtml(text.substring(numStart, p)) + '</span>';
      } else if (c === 't' && text.substr(p, 4) === 'true') { out += '<span style="color:#b45309">true</span>'; p += 4; }
      else if (c === 'f' && text.substr(p, 5) === 'false') { out += '<span style="color:#b45309">false</span>'; p += 5; }
      else if (c === 'n' && text.substr(p, 4) === 'null') { out += '<span style="color:#64748b">null</span>'; p += 4; }
      else if (c === '{' || c === '[' || c === '}' || c === ']') { out += '<span style="color:#1e293b;font-weight:600">' + c + '</span>'; p++; }
      else { out += escapeHtml(c); p++; }
    }
    return out;
  }

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
    if (treeRoot) {
      treeRoot.innerHTML = '<div style="background:#f8fafc;padding:12px;border-radius:6px;border:1px solid #e2e8f0;overflow:auto;white-space:pre-wrap;max-height:400px">' + highlightJson(JSON.stringify(data, null, 2)) + '</div>';
    }
    var jpValue = jsonpathInput.value.trim();
    var jpOut = document.getElementById('jsonpathOutput');
    if (jpValue && lastData !== null && jpOut) {
      try {
        var result = jsonPathGet(lastData, jpValue);
        jpOut.innerHTML = (result === undefined) ? '<em style="color:#64748b">No match</em>' : '<pre style="background:#f1f5f9;padding:8px;border-radius:6px;overflow:auto;white-space:pre-wrap;margin:4px 0">' + escapeHtml(JSON.stringify(result, null, 2)) + '</pre>';
      } catch (err) {
        jpOut.innerHTML = '<div style="color:#b91c1c">' + escapeHtml(err.message) + '</div>';
      }
    } else if (jpOut) {
      jpOut.innerHTML = '';
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

  document.getElementById('sampleBtn').addEventListener('click', function() {
    inputEl.value = JSON.stringify({name: "zlbox Tools", version: 1.0, active: true, tags: ["text", "json", "formatter"], nested: {key1: "value1", key2: [1, 2, 3]}}, null, 2);
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
    if (navigator.clipboard) navigator.clipboard.writeText(txt).then(function() { setStatus('Copied to clipboard', true); });
    else {
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
    var blob = new Blob([txt], {type: 'application/json'});
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
  setStatus('Ready');
})();
