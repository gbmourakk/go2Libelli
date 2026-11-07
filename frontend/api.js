const API_BASE_URL = "http://127.0.0.1:5000/api";

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    credentials: "include",
    headers: { "Content-Type": "application/json", "X-Libelli-Request": "1", ...(options.headers || {}) },
    ...options,
  });

  if (response.status === 204) return null;

  const dados = await response.json().catch(() => null);

  if (response.status === 401 && !["login.html", "cadastro.html"].includes(location.pathname.split("/").pop())) {
    location.replace("login.html");
  }

  if (!response.ok) {
    throw new Error((dados && dados.erro) || "Erro na requisição.");
  }

  return dados;
}

function querystring(params) {
  const entradas = Object.entries(params).filter(
    ([, valor]) => valor !== undefined && valor !== null && valor !== ""
  );
  const query = new URLSearchParams(entradas).toString();
  return query ? `?${query}` : "";
}

const api = {
  usuarios: {
    criar: (dados) =>
      apiRequest("/usuarios/", { method: "POST", body: JSON.stringify(dados) }),
    buscar: (id) => apiRequest(`/usuarios/${id}`),
    login: (dados) =>
      apiRequest("/usuarios/login", { method: "POST", body: JSON.stringify(dados) }),
    atual: () => apiRequest("/usuarios/me"),
    sair: () => apiRequest("/usuarios/logout", { method: "POST" }),
  },

  disciplinas: {
    listar: (usuarioId) =>
      apiRequest(`/disciplinas/${querystring({ usuario_id: usuarioId })}`),
    listarComContagem: (usuarioId) =>
      apiRequest(`/disciplinas/com-contagem${querystring({ usuario_id: usuarioId })}`),
    criar: (dados) =>
      apiRequest("/disciplinas/", { method: "POST", body: JSON.stringify(dados) }),
    buscar: (id) => apiRequest(`/disciplinas/${id}`),
    atualizar: (id, dados) =>
      apiRequest(`/disciplinas/${id}`, { method: "PUT", body: JSON.stringify(dados) }),
    deletar: (id) => apiRequest(`/disciplinas/${id}`, { method: "DELETE" }),
  },

  conteudos: {
    listar: (disciplinaId) =>
      apiRequest(`/conteudos/${querystring({ disciplina_id: disciplinaId })}`),
    criar: (dados) =>
      apiRequest("/conteudos/", { method: "POST", body: JSON.stringify(dados) }),
    buscar: (id) => apiRequest(`/conteudos/${id}`),
    atualizar: (id, dados) =>
      apiRequest(`/conteudos/${id}`, { method: "PUT", body: JSON.stringify(dados) }),
    deletar: (id) => apiRequest(`/conteudos/${id}`, { method: "DELETE" }),
    buscarEstudos: (filtros) =>
      apiRequest(`/conteudos/buscar-estudos${querystring(filtros)}`),
  },

  comentarios: {
    listar: (disciplinaId) =>
      apiRequest(`/comentarios/${querystring({ disciplina_id: disciplinaId })}`),
    criar: (dados) =>
      apiRequest("/comentarios/", { method: "POST", body: JSON.stringify(dados) }),
    atualizar: (id, dados) =>
      apiRequest(`/comentarios/${id}`, { method: "PUT", body: JSON.stringify(dados) }),
    buscar: (id) => apiRequest(`/comentarios/${id}`),
    deletar: (id) => apiRequest(`/comentarios/${id}`, { method: "DELETE" }),
  },

  quizzes: {
    listar: (disciplinaId) =>
      apiRequest(`/quizzes/${querystring({ disciplina_id: disciplinaId })}`),
    gerar: (conteudoId, titulo) =>
      apiRequest("/quizzes/gerar", {
        method: "POST",
        body: JSON.stringify({ conteudo_id: conteudoId, titulo }),
      }),
    buscar: (id) => apiRequest(`/quizzes/${id}`),
    atualizar: (id, dados) =>
      apiRequest(`/quizzes/${id}`, { method: "PUT", body: JSON.stringify(dados) }),
    deletar: (id) => apiRequest(`/quizzes/${id}`, { method: "DELETE" }),
  },

  resumos: {
    listar: (disciplinaId) =>
      apiRequest(`/resumos/${querystring({ disciplina_id: disciplinaId })}`),
    gerar: (conteudoId, titulo) =>
      apiRequest("/resumos/gerar", {
        method: "POST",
        body: JSON.stringify({ conteudo_id: conteudoId, titulo }),
      }),
    buscar: (id) => apiRequest(`/resumos/${id}`),
    atualizar: (id, dados) =>
      apiRequest(`/resumos/${id}`, { method: "PUT", body: JSON.stringify(dados) }),
    deletar: (id) => apiRequest(`/resumos/${id}`, { method: "DELETE" }),
  },

  revisoes: {
    listar: (disciplinaId) =>
      apiRequest(`/revisoes/${querystring({ disciplina_id: disciplinaId })}`),
    gerar: (conteudoId, dataRevisao) =>
      apiRequest("/revisoes/gerar", {
        method: "POST",
        body: JSON.stringify({ conteudo_id: conteudoId, data_revisao: dataRevisao }),
      }),
    buscar: (id) => apiRequest(`/revisoes/${id}`),
    atualizar: (id, dados) =>
      apiRequest(`/revisoes/${id}`, { method: "PUT", body: JSON.stringify(dados) }),
    deletar: (id) => apiRequest(`/revisoes/${id}`, { method: "DELETE" }),
  },

  planos: {
    listar: (usuarioId) =>
      apiRequest(`/planos/${querystring({ usuario_id: usuarioId })}`),
    gerar: (dados) =>
      apiRequest("/planos/gerar", { method: "POST", body: JSON.stringify(dados) }),
    buscar: (id) => apiRequest(`/planos/${id}`),
    deletar: (id) => apiRequest(`/planos/${id}`, { method: "DELETE" }),
  },

  conversas: {
    listar: () => apiRequest("/conversas/"),
    buscar: (id) => apiRequest(`/conversas/${id}`),
    enviar: (texto, modo, conversaId = null) =>
      apiRequest("/conversas/enviar", {
        method: "POST",
        body: JSON.stringify({ texto, modo, conversa_id: conversaId }),
      }),
    excluir: (id) => apiRequest(`/conversas/${id}`, { method: "DELETE" }),
  },

  motorIa: {
    gerar: (prompt, modo) =>
      apiRequest("/motor-ia/gerar", {
        method: "POST",
        body: JSON.stringify({ prompt, modo }),
      }),
  },
};

// apenas a sessão autenticada, nunca ids arbitrários do localStorage.
let usuarioAtual = null;
async function garantirUsuario() {
  if (!usuarioAtual) usuarioAtual = await api.usuarios.atual();
  return usuarioAtual.id;
}
