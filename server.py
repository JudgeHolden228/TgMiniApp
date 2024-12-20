from flask import Flask, request, jsonify

app = Flask(__name__)

# Список формул
FORMULAS = {
    "speed": {
        "name": "Скорость (v = s / t)",
        "description": "Скорость вычисляется по формуле v = s / t, где s — путь, t — время.",
        "parameters": ["s", "t"],
        "calculate": lambda s, t: s / t
    },
    "kinetic_energy": {
        "name": "Кинетическая энергия (E_k = 0.5 * m * v^2)",
        "description": "Кинетическая энергия вычисляется по формуле E_k = 0.5 * m * v^2, где m — масса, v — скорость.",
        "parameters": ["m", "v"],
        "calculate": lambda m, v: 0.5 * m * v**2
    },
    "ohms_law": {
        "name": "Закон Ома (I = U / R)",
        "description": "Сила тока вычисляется по формуле I = U / R, где U — напряжение, R — сопротивление.",
        "parameters": ["U", "R"],
        "calculate": lambda U, R: U / R
    }
}

@app.route('/formulas', methods=['GET'])
def get_formulas():
    """Возвращает список доступных формул."""
    return jsonify([
        {"key": key, "name": value["name"], "description": value["description"]}
        for key, value in FORMULAS.items()
    ])

@app.route('/calculate', methods=['POST'])
def calculate():
    """Выполняет расчёт выбранной формулы."""
    data = request.json
    formula_key = data.get('formula_key')
    parameters = data.get('parameters', {})

    formula = FORMULAS.get(formula_key)
    if not formula:
        return jsonify({"error": "Formula not found"}), 404

    try:
        # Выполняем расчёт
        result = formula["calculate"](**{param: float(parameters[param]) for param in formula["parameters"]})
        return jsonify({
            "formula": formula["name"],
            "description": formula["description"],
            "result": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
