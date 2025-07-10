const form = document.getElementById('form-login');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const ra = form.ra.value;
    const digito = form.digito.value;
    const senha = form.senha.value;

    try {
        const response = await fetch('http://localhost:3000/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ra, digito, senha }),
        });

        if (!response.ok) throw new Error('Erro na requisição');

        const data = await response.json();

        if (data.sucesso) {
            alert(`Você tem ${data.faltas} faltas.`);
        } else {
            alert(`Erro: ${data.erro || 'dados inválidos'}`);
        }
    } catch (err) {
        alert(`Falha na conexão: ${err.message}`);
    }
});
