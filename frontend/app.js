(function tema() {
  const salvo = localStorage.getItem("libelli-theme") || "light";
  document.documentElement.dataset.theme = salvo;

  document.addEventListener("click", (event) => {
    if (!event.target.closest("#theme-toggle")) return;
    const proximo =
      document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = proximo;
    localStorage.setItem("libelli-theme", proximo);
  });
})();

(function navegacao() {
  const pagina = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("[data-nav]").forEach((link) => {
    if (link.getAttribute("href") === pagina) link.classList.add("active");
  });
})();

function formatarErro(erro) {
  return erro instanceof Error ? erro.message : String(erro);
}

const listaMaterias = document.getElementById("materias");
if (listaMaterias) {
  async function renderizar() {
    const usuarioId = await garantirUsuario();
    const disciplinas = await api.disciplinas.listarComContagem(usuarioId);

    document.getElementById("materias-count").textContent =
      `${disciplinas.length} disciplina(s) cadastrada(s)`;

    listaMaterias.innerHTML = "";
    if (!disciplinas.length) {
      listaMaterias.innerHTML =
        '<p class="sub">Nenhuma disciplina cadastrada ainda.</p>';
      return;
    }

    disciplinas.forEach((disciplina) => {
      const elemento = document.createElement("article");
      elemento.className = "card";
      elemento.innerHTML = `
        <div class="row">
          <span class="dot"></span>
          <div class="grow">
            <strong></strong><br>
            <small class="meta"></small>
          </div>
        </div>
        <p class="meta descricao"></p>
        <p class="meta contagem"></p>
        <div class="row">
          <button class="btn secondary editar">Editar</button>
          <button class="link-danger excluir">Remover</button>
        </div>`;

      elemento.querySelector("strong").textContent = disciplina.nome;
      elemento.querySelector(".descricao").textContent =
        disciplina.descricao || "Sem descrição";
      elemento.querySelector(".contagem").textContent =
        `${disciplina.materiais_count || 0} material(is) relacionado(s)`;

      elemento.querySelector(".editar").onclick = async () => {
        const nome = prompt("Novo nome:", disciplina.nome);
        if (nome === null || !nome.trim()) return;

        const descricao = prompt(
          "Descrição:",
          disciplina.descricao || ""
        );

        try {
          await api.disciplinas.atualizar(disciplina.id, {
            nome: nome.trim(),
            descricao,
          });
          await renderizar();
        } catch (erro) {
          alert(formatarErro(erro));
        }
      };

      elemento.querySelector(".excluir").onclick = async () => {
        if (!confirm(`Remover "${disciplina.nome}"?`)) return;

        try {
          await api.disciplinas.deletar(disciplina.id);
          await renderizar();
        } catch (erro) {
          alert(formatarErro(erro));
        }
      };

      listaMaterias.appendChild(elemento);
    });
  }

  document.getElementById("materia-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const nome = document.getElementById("materia-nome").value.trim();
    const topicos = Number(document.getElementById("materia-topicos").value) || 0;

    if (!nome) return;

    try {
      await api.disciplinas.criar({
        nome,
        descricao: topicos ? `${topicos} tópico(s) planejado(s)` : null,
        usuario_id: await garantirUsuario(),
      });
      event.target.reset();
      await renderizar();
    } catch (erro) {
      alert(formatarErro(erro));
    }
  });

  renderizar().catch((erro) => alert(formatarErro(erro)));
}

const estudos = document.getElementById("estudos");
if (estudos) {
  const selectDisciplina = document.getElementById("estudo-disciplina");
  const selectBuscaDisciplina = document.getElementById("busca-disciplina");
  const listaConteudos = document.getElementById("conteudos");
  const listaMateriais = document.getElementById("materiais-gerados");
  const listaComentarios = document.getElementById("comentarios-lista");
  const selectComentarioDisciplina = document.getElementById("comentario-disciplina");
  let disciplinasDisponiveis = [];

  // Sem filtro selecionado, consulta apenas as disciplinas da conta logada.
  // Evita pedir todos os registros do banco sem um disciplina_id.
  async function listarDaConta(funcaoListar, disciplinaId) {
    if (disciplinaId) return funcaoListar(disciplinaId);
    const resultados = await Promise.all(
      disciplinasDisponiveis.map((disciplina) => funcaoListar(disciplina.id))
    );
    return resultados.flat();
  }

  async function carregarDisciplinas() {
    const disciplinas = await api.disciplinas.listar(await garantirUsuario());
    disciplinasDisponiveis = disciplinas;

    [selectDisciplina, selectBuscaDisciplina, selectComentarioDisciplina].forEach((select) => {
      const primeira = select.id === "busca-disciplina"
        ? '<option value="">Todas as disciplinas</option>'
        : '<option value="">Selecione a disciplina</option>';
      select.innerHTML = primeira;
      disciplinas.forEach((disciplina) => {
        const option = document.createElement("option");
        option.value = disciplina.id;
        option.textContent = disciplina.nome;
        select.appendChild(option);
      });
    });

    return disciplinas;
  }

  async function carregarConteudos() {
    const disciplinaId = Number(selectDisciplina.value) || undefined;
    const itens = await listarDaConta(api.conteudos.listar, disciplinaId);

    listaConteudos.innerHTML = "";
    if (!itens.length) {
      listaConteudos.innerHTML = '<p class="sub">Nenhum conteúdo encontrado.</p>';
      return;
    }

    itens.forEach((item) => {
      const elemento = document.createElement("article");
      elemento.className = "card";
      elemento.innerHTML = `
        <strong></strong>
        <p class="meta"></p>
        <div class="row">
          <button class="btn secondary editar">Editar</button>
          <button class="btn secondary resumo">Gerar resumo</button>
          <button class="btn secondary quiz">Gerar quiz</button>
          <button class="btn secondary revisao">Agendar revisão</button>
          <button class="link-danger excluir">Excluir</button>
        </div>`;

      elemento.querySelector("strong").textContent = item.titulo || "Sem título";
      elemento.querySelector(".meta").textContent = item.conteudo || "";

      elemento.querySelector(".editar").onclick = async () => {
        const titulo = prompt("Título:", item.titulo || "");
        if (titulo === null) return;
        const texto = prompt("Conteúdo:", item.conteudo || "");
        if (texto === null) return;

        try {
          await api.conteudos.atualizar(item.id, { titulo, conteudo: texto });
          await carregarConteudos();
        } catch (erro) {
          alert(formatarErro(erro));
        }
      };

      elemento.querySelector(".excluir").onclick = async () => {
        if (!confirm("Excluir este conteúdo e os materiais vinculados?")) return;
        try {
          await api.conteudos.deletar(item.id);
          await carregarConteudos();
        } catch (erro) {
          alert(formatarErro(erro));
        }
      };

      elemento.querySelector(".resumo").onclick = async (evento) => {
        const botao = evento.currentTarget;
        const rotulo = botao.textContent;
        botao.disabled = true;
        botao.textContent = "Gerando com IA...";
        try {
          await api.resumos.gerar(item.id);
          await carregarMateriais();
          alert("Resumo gerado com IA e salvo.");
        } catch (erro) {
          alert(formatarErro(erro));
        } finally {
          botao.disabled = false;
          botao.textContent = rotulo;
        }
      };

      elemento.querySelector(".quiz").onclick = async (evento) => {
        const botao = evento.currentTarget;
        const rotulo = botao.textContent;
        botao.disabled = true;
        botao.textContent = "Gerando com IA...";
        try {
          await api.quizzes.gerar(item.id);
          await carregarMateriais();
          alert("Quiz gerado com IA e salvo.");
        } catch (erro) {
          alert(formatarErro(erro));
        } finally {
          botao.disabled = false;
          botao.textContent = rotulo;
        }
      };

      elemento.querySelector(".revisao").onclick = async () => {
        const data = prompt(
          "Data e hora da revisão (ex.: 2026-08-30T19:00):",
          "2026-08-30T19:00"
        );
        if (!data) return;

        try {
          await api.revisoes.gerar(item.id, data);
          await carregarMateriais();
          alert("Revisão agendada.");
        } catch (erro) {
          alert(formatarErro(erro));
        }
      };

      listaConteudos.appendChild(elemento);
    });
  }

  async function carregarMateriais() {
    const disciplinaId = Number(selectBuscaDisciplina.value) || undefined;
    const [resumos, quizzes, revisoes] = await Promise.all([
      listarDaConta(api.resumos.listar, disciplinaId),
      listarDaConta(api.quizzes.listar, disciplinaId),
      listarDaConta(api.revisoes.listar, disciplinaId),
    ]);

    listaMateriais.innerHTML = "";
    [...resumos, ...quizzes, ...revisoes]
      .sort((a, b) => new Date(b.criado_em || 0) - new Date(a.criado_em || 0))
      .forEach((item) => {
        const elemento = document.createElement("article");
        elemento.className = "item";
        elemento.innerHTML = `
          <div class="grow"><strong></strong><br><small></small><p class="meta"></p></div>
          <div class="row material-acoes"></div>`;
        elemento.querySelector("strong").textContent = item.titulo || "Sem título";
        elemento.querySelector("small").textContent = item.tipo;
        const conteudoMaterial = elemento.querySelector(".meta");
        if (item.tipo === "revisao") {
          conteudoMaterial.textContent = `Data: ${item.data_revisao || "não definida"} · Status: ${item.status || "pendente"}`;
        } else {
          formatarTextoIA(conteudoMaterial, item.conteudo || item.perguntas || "Sem conteúdo");
        }
        const acoes = elemento.querySelector(".material-acoes");
        const editar = document.createElement("button");
        editar.className = "btn secondary";
        editar.textContent = item.tipo === "revisao" ? "Editar revisão" : "Editar";
        editar.onclick = async () => {
          try {
            if (item.tipo === "resumo") {
              const titulo = prompt("Título do resumo:", item.titulo || "");
              if (titulo === null) return;
              const conteudo = prompt("Conteúdo do resumo:", item.conteudo || "");
              if (conteudo === null) return;
              await api.resumos.atualizar(item.id, { titulo: titulo.trim(), conteudo });
            } else if (item.tipo === "quiz") {
              const titulo = prompt("Título do quiz:", item.titulo || "");
              if (titulo === null) return;
              const perguntas = prompt("Perguntas do quiz:", item.perguntas || item.conteudo || "");
              if (perguntas === null) return;
              await api.quizzes.atualizar(item.id, { titulo: titulo.trim(), perguntas });
            } else {
              const data = prompt("Data e hora (AAAA-MM-DDTHH:MM):", (item.data_revisao || "").slice(0, 16));
              if (data === null) return;
              const status = prompt("Status: pendente ou concluida", item.status || "pendente");
              if (status === null) return;
              if (!["pendente", "concluida"].includes(status.trim())) {
                alert("Use o status 'pendente' ou 'concluida'.");
                return;
              }
              await api.revisoes.atualizar(item.id, { data_revisao: data, status: status.trim() });
            }
            await carregarMateriais();
          } catch (erro) { alert(formatarErro(erro)); }
        };
        const remover = document.createElement("button");
        remover.className = "link-danger";
        remover.textContent = "Excluir";
        remover.onclick = async () => {
          if (!confirm(`Excluir ${item.tipo} "${item.titulo || "Sem título"}"?`)) return;
          try {
            if (item.tipo === "resumo") await api.resumos.deletar(item.id);
            else if (item.tipo === "quiz") await api.quizzes.deletar(item.id);
            else await api.revisoes.deletar(item.id);
            await carregarMateriais();
          } catch (erro) { alert(formatarErro(erro)); }
        };
        acoes.append(editar, remover);
        listaMateriais.appendChild(elemento);
      });

    if (!listaMateriais.children.length) {
      listaMateriais.innerHTML = '<p class="sub">Nenhum material gerado.</p>';
    }
  }

  async function carregarComentarios() {
    const disciplinaId = Number(selectComentarioDisciplina.value) || undefined;
    const comentarios = await listarDaConta(api.comentarios.listar, disciplinaId);
    listaComentarios.innerHTML = "";
    comentarios.forEach((item) => {
      const elemento = document.createElement("article");
      elemento.className = "item";
      elemento.innerHTML = '<div class="grow"><strong></strong><p class="meta"></p></div><div class="row"><button class="btn secondary editar">Editar</button><button class="link-danger excluir">Excluir</button></div>';
      elemento.querySelector("strong").textContent = item.titulo || "Comentário";
      elemento.querySelector(".meta").textContent = item.conteudo || "";
      elemento.querySelector(".editar").onclick = async () => {
        const titulo = prompt("Título:", item.titulo || "");
        if (titulo === null) return;
        const texto = prompt("Comentário:", item.conteudo || "");
        if (texto === null) return;
        try {
          await api.comentarios.atualizar(item.id, { titulo: titulo.trim(), texto });
          await carregarComentarios();
        } catch (erro) { alert(formatarErro(erro)); }
      };
      elemento.querySelector(".excluir").onclick = async () => {
        if (!confirm("Excluir este comentário?")) return;
        try {
          await api.comentarios.deletar(item.id);
          await carregarComentarios();
        } catch (erro) { alert(formatarErro(erro)); }
      };
      listaComentarios.appendChild(elemento);
    });
    if (!listaComentarios.children.length) listaComentarios.innerHTML = '<p class="sub">Nenhum comentário cadastrado.</p>';
  }

  document.getElementById("comentario-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const titulo = document.getElementById("comentario-titulo").value.trim();
    const texto = document.getElementById("comentario-texto").value.trim();
    const disciplinaId = Number(selectComentarioDisciplina.value);
    if (!titulo || !texto || !disciplinaId) {
      alert("Preencha o título, o comentário e a disciplina.");
      return;
    }
    try {
      await api.comentarios.criar({ titulo, texto, disciplina_id: disciplinaId });
      event.target.reset();
      await carregarComentarios();
      alert("Comentário salvo.");
    } catch (erro) { alert(formatarErro(erro)); }
  });
  selectComentarioDisciplina.addEventListener("change", carregarComentarios);

  document.getElementById("conteudo-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const titulo = document.getElementById("conteudo-titulo").value.trim();
    const texto = document.getElementById("conteudo-texto").value.trim();
    const disciplinaId = Number(selectDisciplina.value);

    if (!titulo || !texto || !disciplinaId) {
      alert("Informe título, conteúdo e disciplina.");
      return;
    }

    try {
      await api.conteudos.criar({
        titulo,
        conteudo: texto,
        disciplina_id: disciplinaId,
      });
      event.target.reset();
      await carregarConteudos();
      alert("Conteúdo cadastrado.");
    } catch (erro) {
      alert(formatarErro(erro));
    }
  });

  document.getElementById("conteudo-carregar").onclick = carregarConteudos;
  document.getElementById("busca-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    try {
      const resultados = await api.conteudos.buscarEstudos({
        usuario_id: await garantirUsuario(),
        termo: document.getElementById("busca-termo").value.trim(),
        disciplina_id: Number(selectBuscaDisciplina.value) || undefined,
        tipo: document.getElementById("busca-tipo").value,
        ordenar_por: document.getElementById("busca-ordem").value,
        direcao: document.getElementById("busca-direcao").value,
      });

      const lista = document.getElementById("resultados-busca");
      lista.innerHTML = "";
      resultados.forEach((item) => {
        const elemento = document.createElement("div");
        elemento.className = "item";
        elemento.innerHTML =
          '<div class="grow"><strong></strong><br><small></small></div>';
        elemento.querySelector("strong").textContent =
          `${item.titulo || "Sem título"} — ${item.tipo}`;
        elemento.querySelector("small").textContent =
          item.disciplina_nome || "";
        lista.appendChild(elemento);
      });

      if (!lista.children.length) {
        lista.innerHTML = '<p class="sub">Nenhum resultado.</p>';
      }
    } catch (erro) {
      alert(formatarErro(erro));
    }
  });

  selectDisciplina.addEventListener("change", carregarConteudos);
  selectBuscaDisciplina.addEventListener("change", carregarMateriais);

  carregarDisciplinas()
    .then(() => Promise.all([carregarConteudos(), carregarMateriais(), carregarComentarios()]))
    .catch((erro) => alert(formatarErro(erro)));
}
