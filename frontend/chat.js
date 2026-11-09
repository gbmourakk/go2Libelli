(function iniciarChat() {
  const chat = document.getElementById("chat");
  if (!chat) return;

  const input = document.getElementById("chat-input");
  const enviarBotao = document.getElementById("chat-send");
  const novaBotao = document.getElementById("chat-new");
  const lista = document.getElementById("chat-conversations");
  const titulo = document.getElementById("chat-current-title");
  let conversaId = null;
  let modo = "resumo";
  let enviando = false;

  function adicionarMensagem(papel, texto) {
    const elemento = document.createElement("div");
    elemento.className = `msg ${papel === "user" ? "user" : "libi"}`;
    if (papel === "assistant") {
      formatarTextoIA(elemento, texto);
    } else {
      elemento.textContent = texto;
    }
    chat.appendChild(elemento);
    chat.scrollTop = chat.scrollHeight;
    return elemento;
  }

  function novaConversa() {
    if (enviando) return;
    conversaId = null;
    titulo.textContent = "Nova conversa";
    chat.innerHTML = "";
    adicionarMensagem("assistant", "Olá! O que você quer estudar hoje?");
    lista.querySelectorAll(".chat-conversation").forEach((item) => item.classList.remove("active"));
    input.focus();
  }

  function renderizarLista(conversas) {
    lista.innerHTML = "";
    if (!conversas.length) {
      const vazio = document.createElement("p");
      vazio.className = "sub";
      vazio.textContent = "Nenhuma conversa salva.";
      lista.appendChild(vazio);
      return;
    }

    conversas.forEach((conversa) => {
      const linha = document.createElement("div");
      linha.className = "chat-conversation";
      linha.dataset.conversaId = String(conversa.id);
      linha.classList.toggle("active", conversa.id === conversaId);

      const abrir = document.createElement("button");
      abrir.type = "button";
      abrir.className = "chat-conversation-open";
      abrir.textContent = conversa.titulo;
      abrir.title = conversa.titulo;
      abrir.onclick = () => {
        if (enviando) return;
        abrirConversa(conversa.id).catch((erro) => alert(formatarErro(erro)));
      };

      const excluir = document.createElement("button");
      excluir.type = "button";
      excluir.className = "chat-conversation-delete";
      excluir.textContent = "×";
      excluir.title = "Excluir conversa";
      excluir.setAttribute("aria-label", `Excluir conversa ${conversa.titulo}`);
      excluir.onclick = async () => {
        if (enviando || !confirm(`Excluir a conversa "${conversa.titulo}"?`)) return;
        try {
          await api.conversas.excluir(conversa.id);
          if (conversa.id === conversaId) novaConversa();
          await carregarLista();
        } catch (erro) {
          alert(formatarErro(erro));
        }
      };
      linha.append(abrir, excluir);
      lista.appendChild(linha);
    });
  }

  async function carregarLista() {
    const conversas = await api.conversas.listar();
    renderizarLista(conversas);
    return conversas;
  }

  async function abrirConversa(id) {
    const conversa = await api.conversas.buscar(id);
    conversaId = conversa.id;
    titulo.textContent = conversa.titulo;
    chat.innerHTML = "";
    conversa.mensagens.forEach((mensagem) => adicionarMensagem(mensagem.papel, mensagem.conteudo));
    lista.querySelectorAll(".chat-conversation").forEach((item) => {
      item.classList.toggle("active", item.dataset.conversaId === String(conversaId));
    });
  }

  async function enviar() {
    if (enviando) return;
    const texto = input.value.trim();
    if (!texto) return;

    enviando = true;
    enviarBotao.disabled = true;
    novaBotao.disabled = true;
    const perguntaVisivel = adicionarMensagem("user", texto);
    input.value = "";
    const carregando = adicionarMensagem("assistant", "Pensando...");

    try {
      const resultado = await api.conversas.enviar(texto, modo, conversaId);
      conversaId = resultado.conversa.id;
      titulo.textContent = resultado.conversa.titulo;
      formatarTextoIA(carregando, resultado.mensagem.conteudo);
      try {
        await carregarLista();
      } catch (erro) {
        lista.textContent = "Mensagem salva. Atualize a página para recarregar o histórico.";
      }
    } catch (erro) {
      carregando.remove();
      perguntaVisivel.remove();
      if (!input.value.trim()) input.value = texto;
      alert(formatarErro(erro));
    } finally {
      enviando = false;
      enviarBotao.disabled = false;
      novaBotao.disabled = false;
      input.focus();
    }
  }

  document.querySelectorAll("[data-modo]").forEach((botao) => {
    botao.onclick = () => {
      modo = botao.dataset.modo;
      document.querySelectorAll("[data-modo]").forEach((item) => {
        item.classList.toggle("active", item === botao);
      });
    };
  });
  document.querySelectorAll("[data-sugestao]").forEach((botao) => {
    botao.onclick = () => { input.value = botao.textContent.trim(); input.focus(); };
  });
  novaBotao.onclick = novaConversa;
  enviarBotao.onclick = enviar;
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      enviar();
    }
  });

  carregarLista().then((conversas) => {
    if (conversas.length) return abrirConversa(conversas[0].id);
    novaConversa();
  }).catch((erro) => {
    lista.textContent = `Não foi possível carregar as conversas: ${formatarErro(erro)}`;
    novaConversa();
  });
})();
