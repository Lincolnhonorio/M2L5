from flask import Flask, render_template, request

app = Flask(__name__)


def result_calculate(size, lights, device):
    """
    Calcula o consumo estimado de energia.
    Fórmula: (Área * 100) + (Lâmpadas * 0.04) + (Aparelhos * 5)
    """
    home_coef = 100
    light_coef = 0.04
    devices_coef = 5
    return size * home_coef + lights * light_coef + device * devices_coef

# --- ROTAS DA CALCULADORA ---


@app.route('/')
def index():
    """Página inicial: Seleção do tamanho da casa."""
    return render_template('index.html')


@app.route('/<size>')
def lights(size):
    """Segunda página: Seleção da quantidade de luzes."""
    return render_template('lights.html', size=size)


@app.route('/<size>/<lights>')
def electronics(size, lights):
    """Terceira página: Seleção da quantidade de aparelhos."""
    return render_template('electronics.html', size=size, lights=lights)


@app.route('/<size>/<lights>/<device>')
def end(size, lights, device):
    """
    Página final: Exibe o resultado do cálculo e o formulário de contato.
    Incluímos um try/except para garantir que valores inválidos não quebrem o site.
    """
    try:
        # Converte os parâmetros da URL para inteiros antes do cálculo
        res = result_calculate(int(size), int(lights), int(device))
        return render_template('end.html', result=res)
    except (ValueError, TypeError):
        # Se houver erro na conversão (ex: alguém digitar texto na URL), volta para o início
        return render_template('index.html')


# --- ROTAS DO FORMULÁRIO ---

@app.route('/form')
def form_page():
    """Rota alternativa para acessar o formulário diretamente."""
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    """
    Processa os dados enviados pelo formulário no end.html ou form.html.
    Captura: Nome, E-mail, Endereço e Data.
    """
    # Coleta os dados usando o atributo 'name' das tags <input> do HTML
    form_data = {
        "name": request.form.get('name'),
        "email": request.form.get('email'),
        "address": request.form.get('address'),
        "date": request.form.get('date')
    }

    # Renderiza a página de agradecimento com os dados recebidos
    return render_template('form_result.html', **form_data)


# --- INICIALIZAÇÃO ---

if __name__ == "__main__":
    # O debug=True permite ver as mudanças sem precisar reiniciar o servidor manualmente
    app.run(debug=True)
