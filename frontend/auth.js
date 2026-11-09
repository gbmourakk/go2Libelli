(async function iniciarSessao() {
  const pagina = location.pathname.split("/").pop() || "index.html";
  if (pagina === "login.html" || pagina === "cadastro.html") return;
  try {
    const usuario = await api.usuarios.atual();
    usuarioAtual = usuario;
    const barra = document.querySelector(".topbar .container");
    if (!barra) return;
    const sair = document.createElement("button");
    sair.className = "btn secondary";
    sair.type = "button";
    sair.textContent = "Sair";
    sair.style.marginLeft = "8px";
    sair.addEventListener("click", async () => {
      try { await api.usuarios.sair(); } finally {
        usuarioAtual = null;
        location.replace("login.html");
      }
    });
    barra.appendChild(sair);
  } catch (erro) {
    location.replace("login.html");
  }
})();
