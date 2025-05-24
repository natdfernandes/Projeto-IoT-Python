fetch('http://localhost:8080/livro')
    .then(Response => Response.json())
    .then(livros => {
        criar_cards_livros(livros)
    })

function criar_cards_livros(livros) {
    const container = document.getElementById("livros");

    livros.forEach((livro) => {
        const disponibilidadeClasse = livro.disponivel ? "bg-success" : "bg-danger";
        const disponibilidadeTexto = livro.disponivel ? "Disponível" : "Indisponível";
        const imagemDisponivel = livro.link_capa !== null ? "block" : "none";

        const col = document.createElement("div");
        col.className = "col";
        col.innerHTML = `
                  <div class="card border-success mb-3" style="max-width: 18rem;">
                    <img src="${livro.link_capa}" class="card-img-top" alt="Capa: ${livro.titulo}" style="display: ${imagemDisponivel}">
                    <div class="card-body">
                      <h5 class="card-title">${livro.titulo}</h5>
                      <p class="card-text">
                        Detalhes:
                        <ul>
                          <li><strong>Autores: </strong>${livro.autores}</li>
                          <li><strong>Publicação: </strong>${livro.data_publicacao}</li>
                        </ul>
                      </p>
                    </div>
                    <div class="align-items-center card-footer d-flex">
                      <div class="d-block h-100 me-3 position-relative">
                        <span class="position-absolute translate-middle p-2 ${disponibilidadeClasse} border border-light rounded-circle">
                          <span class="visually-hidden">${disponibilidadeTexto}</span>
                        </span>
                      </div>
                      <small class="text-body-secondary">${disponibilidadeTexto}</small>
                    </div>
                  </div>
                `;
        container.appendChild(col);
    });
}
