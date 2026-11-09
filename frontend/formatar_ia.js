(function () {
  "use strict";

  const escapar = (valor) => String(valor).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[c]);

  function matematica(codigo) {
    let s = escapar(codigo.trim());
    const comandos = {
      Delta: "Δ", delta: "δ", alpha: "α", beta: "β", gamma: "γ", pi: "π",
      theta: "θ", times: "×", cdot: "·", div: "÷", neq: "≠", ne: "≠",
      leq: "≤", geq: "≥", le: "≤", ge: "≥", pm: "±", infty: "∞",
      rightarrow: "→", sqrt: "√", approx: "≈"
    };
    s = s.replace(/\\([a-zA-Z]+)/g, (t, nome) => comandos[nome] || t);
    s = s.replace(/\^\{([^{}]+)\}/g, "<sup>$1</sup>")
      .replace(/\^([\w\d+-])/g, "<sup>$1</sup>")
      .replace(/_\{([^{}]+)\}/g, "<sub>$1</sub>")
      .replace(/_([\w\d+-])/g, "<sub>$1</sub>");
    return '<span class="ia-matematica">' + s + '</span>';
  }

  function linha(texto) {
    const partes = [];
    const guardar = (html) => {
      const indice = partes.push(html) - 1;
      return `\u0001${indice}\u0002`;
    };
    let s = String(texto);
    s = s.replace(/`([^`\n]+)`/g, (_, codigo) => guardar('<code>' + escapar(codigo) + '</code>'));
    s = s.replace(/\\\((.+?)\\\)|\$([^$\n]+)\$/g,
      (_, par, dolar) => guardar(matematica(par ?? dolar)));
    s = escapar(s);
    s = s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/__(.+?)__/g, '<strong>$1</strong>')
      .replace(/\*([^*\n]+)\*/g, '<em>$1</em>');
    return s.replace(/\u0001(\d+)\u0002/g, (_, i) => partes[Number(i)]);
  }

  function formatar(texto) {
    const linhas = String(texto ?? "").replace(/\r\n?/g, "\n").split("\n");
    const html = [];
    let lista = "";
    let paragrafo = [];
    let codigo = false;
    let codigoLinhas = [];
    function fecharLista() {
      if (lista) { html.push(`</${lista}>`); lista = ""; }
    }
    function fecharParagrafo() {
      if (paragrafo.length) { html.push('<p>' + paragrafo.map(linha).join('<br>') + '</p>'); paragrafo = []; }
    }
    for (const original of linhas) {
      const t = original.trim();
      if (t.startsWith('```')) {
        fecharParagrafo(); fecharLista();
        if (codigo) { html.push('<pre><code>' + escapar(codigoLinhas.join('\n')) + '</code></pre>'); codigoLinhas = []; }
        codigo = !codigo;
        continue;
      }
      if (codigo) { codigoLinhas.push(original); continue; }
      if (!t) { fecharParagrafo(); fecharLista(); continue; }
      const titulo = t.match(/^(#{1,4})\s+(.+)$/);
      if (titulo) {
        fecharParagrafo(); fecharLista();
        const nivel = Math.min(4, titulo[1].length + 1);
        html.push(`<h${nivel}>${linha(titulo[2])}</h${nivel}>`);
        continue;
      }
      const bullet = t.match(/^[-*•]\s+(.+)$/);
      const numero = t.match(/^\d+[.)]\s+(.+)$/);
      if (bullet || numero) {
        fecharParagrafo();
        const tipo = bullet ? 'ul' : 'ol';
        if (lista !== tipo) { fecharLista(); html.push(`<${tipo}>`); lista = tipo; }
        html.push('<li>' + linha((bullet || numero)[1]) + '</li>');
        continue;
      }
      if (lista) fecharLista();
      paragrafo.push(original);
    }
    if (codigo) html.push('<pre><code>' + escapar(codigoLinhas.join('\n')) + '</code></pre>');
    fecharParagrafo(); fecharLista();
    return html.join('\n');
  }

  window.formatarTextoIA = function (elemento, texto) {
    elemento.classList.add('conteudo-ia');
    elemento.innerHTML = formatar(texto);
  };
  window.gerarHtmlIA = formatar;
})();
