from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# Configura CORS só pra liberar o front (ajusta o origin pro que você usa)
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)


def pega_faltas(ra, digito, senha):
    driver = webdriver.Chrome()  # chromedriver no PATH, beleza?
    driver.get("https://saladofuturo.educacao.sp.gov.br/login-alunos")

    wait = WebDriverWait(driver, 15)

    ra_input = wait.until(EC.presence_of_element_located((By.ID, "input-usuario-sed")))
    ra_input.clear()
    ra_input.send_keys(ra)

    digito_input = driver.find_element(By.NAME, "digito-ra")
    digito_input.clear()
    digito_input.send_keys(digito)

    senha_input = driver.find_element(By.ID, "input-senha")
    senha_input.clear()
    senha_input.send_keys(senha)

    btn_login = driver.find_element(By.ID, "botao-login")
    btn_login.click()

    div_clicavel = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div[1]/div[2]/div/div/div/div[1]/div/div/div[2]/div/div[1]/div[1]/div/div[3]',
            )
        )
    )
    div_clicavel.click()

    faltas_element = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "p.MuiTypography-root.MuiTypography-body1.css-p9k9s9")
        )
    )
    faltas = faltas_element.text

    driver.quit()
    return faltas


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    ra = data.get("ra")
    digito = data.get("digito")
    senha = data.get("senha")

    try:
        faltas = pega_faltas(ra, digito, senha)
        return jsonify({"sucesso": True, "faltas": faltas})
    except Exception as e:
        print("Erro:", e)
        return jsonify({"sucesso": False, "erro": str(e)}), 500


if __name__ == "__main__":
    # roda com debug ligado só em dev
    app.run(port=3000, debug=True)
