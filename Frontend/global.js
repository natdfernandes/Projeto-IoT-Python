function extrairServidorUrl() {
  const servidorUrlLocalStorage = localStorage.getItem("servidorUrl");
  return servidorUrlLocalStorage ? servidorUrlLocalStorage : 'http://localhost:8000';
}