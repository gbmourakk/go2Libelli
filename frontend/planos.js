(async function iniciarPlanos() {
  const pagina = document.getElementById("plano-pagina");
  if (!pagina) return;

  const formulario = document.getElementById("plano-form");
  const seletor = document.getElementById("plano-disciplina");
  const lista = document.getElementById("planos-lista");
  const aviso = document.getElementById("plano-status");
  const botao = document.getElementById("plano-gerar");
  const quadro = document.getElementById("plano-atual");

  function mostrarPlano(plano) {
    quadro.hidden = false;
    quadro.dataset.id = String(plano.id);
    document.getElementById("plano-atual-titulo").textContent = plano.titulo;
    document.getElementById("plano-atual-meta").textContent =
      `${plano.disciplina_nome || "Matéria"} · ${plano.dias} dia(s) · ${plano.minutos_por_dia} minutos por dia · ${plano.dificuldade}`;
    formatarTextoIA(document.getElementById("plano-atual-texto"), plano.cronograma);
    quadro.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  async function listar() {
    const usuarioId = await garantirUsuario();
    const planos = await api.planos.listar(usuarioId);
    lista.replaceChildren();
    if (!planos.length) {
      const vazio = document.createElement("p");
      vazio.className = "sub";
      vazio.textContent = "Você ainda não gerou nenhum plano.";
      lista.appendChild(vazio);
      return;
    }
    for (const plano of planos) {
      const item = document.createElement("article");
      item.className = "item plano-item";
      const conteudo = document.createElement("div");
      conteudo.className = "grow";
      const titulo = document.createElement("strong");
      titulo.textContent = plano.titulo;
      const detalhes = document.createElement("small");
      detalhes.textContent = `${plano.disciplina_nome || "Matéria"} · ${plano.dias} dia(s) · ${plano.minutos_por_dia} min/dia`;
      conteudo.append(titulo, document.createElement("br"), detalhes);
      const abrir = document.createElement("button");
      abrir.type = "button";
      abrir.className = "btn secondary";
      abrir.textContent = "Abrir";
      abrir.onclick = async () => {
        try { mostrarPlano(await api.planos.buscar(plano.id)); }
        catch (erro) { alert(erro.message); }
      };
      const excluir = document.createElement("button");
      excluir.type = "button";
      excluir.className = "link-danger";
      excluir.textContent = "Excluir";
      excluir.onclick = async () => {
        if (!confirm(`Excluir o plano "${plano.titulo}"?`)) return;
        try {
          await api.planos.deletar(plano.id);
          if (quadro.dataset.id === String(plano.id)) quadro.hidden = true;
          await listar();
        } catch (erro) { alert(erro.message); }
      };
      item.append(conteudo, abrir, excluir);
      lista.appendChild(item);
    }
  }

  formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    aviso.textContent = "Gerando plano com a Libi IA...";
    botao.disabled = true;
    const dados = {
      disciplina_id: Number(seletor.value),
      tema: document.getElementById("plano-tema").value.trim(),
      dias: Number(document.getElementById("plano-dias").value),
      minutos_por_dia: Number(document.getElementById("plano-minutos").value),
      dificuldade: document.getElementById("plano-dificuldade").value,
    };
    try {
      const plano = await api.planos.gerar(dados);
      quadro.dataset.id = String(plano.id);
      mostrarPlano(plano);
      aviso.textContent = "Plano gerado e salvo no SQLite!";
      await listar();
    } catch (erro) {
      aviso.textContent = `Erro: ${erro.message}`;
    } finally {
      botao.disabled = false;
    }
  });

  document.getElementById("planos-atualizar").onclick = () =>
    listar().catch((erro) => { aviso.textContent = `Erro: ${erro.message}`; });

  try {
    const usuarioId = await garantirUsuario();
    const disciplinas = await api.disciplinas.listar(usuarioId);
    seletor.replaceChildren();
    const opcao = document.createElement("option");
    opcao.value = "";
    opcao.textContent = disciplinas.length ? "Selecione uma matéria" : "Cadastre uma matéria primeiro";
    seletor.appendChild(opcao);
    for (const disciplina of disciplinas) {
      const item = document.createElement("option");
      item.value = disciplina.id;
      item.textContent = disciplina.nome;
      seletor.appendChild(item);
    }
    botao.disabled = !disciplinas.length;
    await listar();
  } catch (erro) {
    aviso.textContent = `Erro ao carregar planos: ${erro.message}`;
  }
})();
