const formulario = document.getElementById("form-auth");
const cadastro = location.pathname.endsWith("cadastro.html");
const erro = document.getElementById("erro-auth");
formulario.addEventListener("submit", async (event) => {
  event.preventDefault();
  erro.textContent = "";
  const botao = document.getElementById("botao-auth");
  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value;
  if (cadastro && senha !== document.getElementById("confirmar").value) {
    erro.textContent = "As senhas não coincidem.";
    return;
  }
  botao.disabled = true;
  try {
    if (cadastro) {
      await api.usuarios.criar({nome: document.getElementById("nome").value.trim(), email, senha});
    }
    await api.usuarios.login({email, senha});
    location.replace("index.html");
  } catch (falha) {
    erro.textContent = falha.message || "Não foi possível continuar.";
  } finally {
    botao.disabled = false;
  }
});
