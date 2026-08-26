const API_BASE_URL = "http://127.0.0.1:5000/api";

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  if (response.status === 204) return null;

  const dados = await response.json().catch(() => null);

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
  },

  resumos: {
    listar: (disciplinaId) =>
      apiRequest(`/resumos/${querystring({ disciplina_id: disciplinaId })}`),
    gerar: (conteudoId, titulo) =>
      apiRequest("/resumos/gerar", {
        method: "POST",
        body: JSON.stringify({ conteudo_id: conteudoId, titulo }),
      }),
  },

  revisoes: {
    listar: (disciplinaId) =>
      apiRequest(`/revisoes/${querystring({ disciplina_id: disciplinaId })}`),
    gerar: (conteudoId, dataRevisao) =>
      apiRequest("/revisoes/gerar", {
        method: "POST",
        body: JSON.stringify({ conteudo_id: conteudoId, data_revisao: dataRevisao }),
      }),
  },

  motorIa: {
    gerar: (prompt, modo) =>
      apiRequest("/motor-ia/gerar", {
        method: "POST",
        body: JSON.stringify({ prompt, modo }),
      }),
  },
};

async function garantirUsuario() {
  const salvo = localStorage.getItem("libelli-usuario-id");
  if (salvo) return Number(salvo);

  const sufixo = Date.now();
  const usuario = await api.usuarios.criar({
    nome: "Estudante",
    email: `estudante-${sufixo}@libelli.local`,
    senha: "libelli-demo-123",
  });

  localStorage.setItem("libelli-usuario-id", usuario.id);
  return usuario.id;
}
