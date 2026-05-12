document.addEventListener('DOMContentLoaded', function() {
    console.log('My Tool Lab loaded');
});

function copyToClipboard(text, element) {
    navigator.clipboard.writeText(text).then(function() {
        element.textContent = '已复制!';
        setTimeout(function() {
            element.textContent = '复制结果';
        }, 2000);
    }).catch(function(err) {
        console.error('复制失败:', err);
    });
}

function downloadText(text, filename) {
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}