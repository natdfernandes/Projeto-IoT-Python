    // Barra de pesquisa mobile
    const searchToggle = document.getElementById('searchToggle');
    const mobileSearch = document.getElementById('mobileSearch');
    
    if (searchToggle && mobileSearch) {
        searchToggle.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Fecha o menu hamburguer se estiver aberto
            const navbarCollapse = document.querySelector('.navbar-collapse.show');
            if (navbarCollapse) {
                const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
                if (bsCollapse) {
                    bsCollapse.hide();
                }
            }
            
            // Alterna a barra de pesquisa
            mobileSearch.style.display = mobileSearch.style.display === 'block' ? 'none' : 'block';
            
            // Foca no input quando expandir
            if (mobileSearch.style.display === 'block') {
                setTimeout(() => {
                    mobileSearch.querySelector('input').focus();
                }, 100);
            }
        });
        
        // Fecha a barra de pesquisa ao clicar fora
        document.addEventListener('click', function(e) {
            if (!mobileSearch.contains(e.target) && e.target !== searchToggle && !searchToggle.contains(e.target)) {
                mobileSearch.style.display = 'none';
            }
        });
    }
    
    // Fecha a barra de pesquisa ao submeter
    const mobileSearchForm = document.querySelector('.mobile-search-form');
    if (mobileSearchForm) {
        mobileSearchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            mobileSearch.style.display = 'none';
            // Aqui você pode adicionar a lógica de busca
        });
    }

    // Melhoria de acessibilidade para navegação
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('focus', function() {
            this.parentElement.style.backgroundColor = 'rgba(255,255,255,0.1)';
        });
        
        link.addEventListener('blur', function() {
            this.parentElement.style.backgroundColor = 'transparent';
        });
    });