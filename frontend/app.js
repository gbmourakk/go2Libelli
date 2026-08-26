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

// ---------- Libi IA ----------
const chat = document.getElementById("chat");
if (chat) {
  let modo = "resumo";
  const input = document.getElementById("chat-input");

  document.querySelectorAll("[data-modo]").forEach((botao) => {
    botao.onclick = () => {
      modo = botao.dataset.modo;
      document.querySelectorAll("[data-modo]").forEach((item) => {
        item.classList.toggle("active", item === botao);
      });
    };
  });

  function adicionarMensagem(tipo, texto) {
    const elemento = document.createElement("div");
    elemento.className = `msg ${tipo}`;
    elemento.textContent = texto;
    chat.appendChild(elemento);
    chat.scrollTop = chat.scrollHeight;
    return elemento;
  }

  async function enviar() {
    const texto = input.value.trim();
    if (!texto) return;

    adicionarMensagem("user", texto);
    input.value = "";
    const carregando = adicionarMensagem("libi", "Pensando...");

    try {
      const resposta = await api.motorIa.gerar(texto, modo);
      carregando.textContent = resposta.texto;
    } catch (erro) {
      carregando.textContent = `Erro: ${formatarErro(erro)}`;
    }
  }

  document.querySelectorAll("[data-sugestao]").forEach((botao) => {
    botao.onclick = () => {
      input.value = botao.textContent.trim();
      input.focus();
    };
  });

  document.getElementById("chat-send").onclick = enviar;
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      enviar();
    }
  });
}

// ---------- Capturar conteúdo ----------
const capturas = document.getElementById("capturas");
if (capturas) {
  const file = document.getElementById("file");
  const preview = document.getElementById("preview");
  const selectDisciplina = document.getElementById("materia-captura");
  const texto = document.getElementById("captura-texto");
  const salvar = document.getElementById("captura-salvar");

  async function carregar() {
    const usuarioId = await garantirUsuario();
    const disciplinas = await api.disciplinas.listar(usuarioId);

    selectDisciplina.innerHTML = '<option value="">Selecione a disciplina</option>';
    disciplinas.forEach((disciplina) => {
      const option = document.createElement("option");
      option.value = disciplina.id;
      option.textContent = disciplina.nome;
      selectDisciplina.appendChild(option);
    });

    const resultados = await Promise.all(
      disciplinas.map((disciplina) => api.conteudos.listar(disciplina.id))
    );
    const itens = resultados.flat().sort((a, b) => b.id - a.id);

    capturas.innerHTML = "";
    if (!itens.length) {
      capturas.innerHTML = '<p class="sub">Nenhum conteúdo cadastrado.</p>';
      return;
    }

    itens.forEach((item) => {
      const disciplina = disciplinas.find((d) => d.id === item.disciplina_id);
      const elemento = document.createElement("div");
      elemento.className = "item";
      elemento.innerHTML =
        '<div class="grow"><strong></strong><br><small></small></div>' +
        '<button class="link-danger">Remover</button>';
      elemento.querySelector("strong").textContent = item.titulo || "Sem título";
      elemento.querySelector("small").textContent =
        disciplina?.nome || "Disciplina removida";
      elemento.querySelector("button").onclick = async () => {
        try {
          await api.conteudos.deletar(item.id);
          await carregar();
        } catch (erro) {
          alert(formatarErro(erro));
        }
      };
      capturas.appendChild(elemento);
    });
  }

  file.addEventListener("change", () => {
    const arquivo = file.files[0];
    if (arquivo) {
      preview.innerHTML = `<img alt="Pré-visualização" src="${URL.createObjectURL(arquivo)}">`;
    }
  });

  salvar.onclick = async () => {
    const disciplinaId = Number(selectDisciplina.value);
    const conteudo = texto.value.trim();

    if (!disciplinaId || !conteudo) {
      alert("Selecione uma disciplina e informe o conteúdo.");
      return;
    }

    try {
      await api.conteudos.criar({
        titulo: file.files[0]?.name || "Conteúdo capturado",
        conteudo,
        disciplina_id: disciplinaId,
      });
      texto.value = "";
      file.value = "";
      preview.textContent = "Enquadre a página e tire a foto";
      await carregar();
      alert("Conteúdo cadastrado com sucesso.");
    } catch (erro) {
      alert(formatarErro(erro));
    }
  };

  carregar().catch((erro) => alert(formatarErro(erro)));
}

// ---------- Matérias ----------
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

// ---------- Estudos: CRUD, busca e geração de materiais ----------
const estudos = document.getElementById("estudos");
if (estudos) {
  const selectDisciplina = document.getElementById("estudo-disciplina");
  const selectBuscaDisciplina = document.getElementById("busca-disciplina");
  const listaConteudos = document.getElementById("conteudos");
  const listaMateriais = document.getElementById("materiais-gerados");

  async function carregarDisciplinas() {
    const disciplinas = await api.disciplinas.listar(await garantirUsuario());

    [selectDisciplina, selectBuscaDisciplina].forEach((select) => {
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
    const itens = await api.conteudos.listar(disciplinaId);

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

      elemento.querySelector(".resumo").onclick = async () => {
        try {
          await api.resumos.gerar(item.id);
          await carregarMateriais();
          alert("Resumo gerado e salvo.");
        } catch (erro) {
          alert(formatarErro(erro));
        }
      };

      elemento.querySelector(".quiz").onclick = async () => {
        try {
          await api.quizzes.gerar(item.id);
          await carregarMateriais();
          alert("Quiz gerado e salvo.");
        } catch (erro) {
          alert(formatarErro(erro));
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
      api.resumos.listar(disciplinaId),
      api.quizzes.listar(disciplinaId),
      api.revisoes.listar(disciplinaId),
    ]);

    listaMateriais.innerHTML = "";

    [...resumos, ...quizzes, ...revisoes]
      .sort((a, b) => b.id - a.id)
      .forEach((item) => {
        const elemento = document.createElement("article");
        elemento.className = "item";
        elemento.innerHTML = `
          <div class="grow">
            <strong></strong>
            <br><small></small>
            <p class="meta"></p>
          </div>`;
        elemento.querySelector("strong").textContent = item.titulo || "Sem título";
        elemento.querySelector("small").textContent = item.tipo;
        elemento.querySelector(".meta").textContent =
          item.conteudo || item.perguntas || item.data_revisao || "";
        listaMateriais.appendChild(elemento);
      });

    if (!listaMateriais.children.length) {
      listaMateriais.innerHTML = '<p class="sub">Nenhum material gerado.</p>';
    }
  }

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

  Promise.all([carregarDisciplinas(), carregarMateriais()])
    .then(carregarConteudos)
    .catch((erro) => alert(formatarErro(erro)));
}
