# app.py
# ------------------------------------------------------------
# API con Flask que ofrece:
#   - GET  /api/info            : información del servicio
#   - POST /api/sumar           : suma dos números (validación simple)
#   - POST /api/multiplicar     : multiplica dos números (validación simple)
#   - GET  /api/score?cvss=...  : clasificación de riesgo a partir de CVSS (0-10)
#   - GET  /api/cve/<cve_id>    : consulta de CVE en API pública (CIRCL)
#
# Decisiones de diseño para simplicidad:
#   - Validaciones básicas (que existan parámetros y que sean numéricos).
#   - Uso de urllib.request (librería estándar) para evitar dependencias extra.
#   - Logs simples con print() de una línea legible por petición.
#   - Sin autenticación (se retiró a pedido).
# ------------------------------------------------------------

from flask import Flask, jsonify, request
import json
import urllib.request

app = Flask(__name__)

# ------------------------------------------------------------
# Función auxiliar de logging simple (texto, una línea)
# ------------------------------------------------------------
def log_line(evento, endpoint, extra=None):
    # Imprime una línea con evento, endpoint y datos adicionales si existen.
    msg = f"[LOG] evento={evento} endpoint={endpoint}"
    if extra is not None:
        try:
            # Convierte 'extra' a JSON compacto si es posible.
            extra_json = json.dumps(extra, ensure_ascii=False)
            msg += f" extra={extra_json}"
        except Exception:
            msg += f" extra={extra}"
    print(msg)

# ------------------------------------------------------------
# Funciones auxiliares de validación y mapeo de riesgo
# ------------------------------------------------------------
def es_numero(valor):
    # Retorna True si 'valor' puede convertirse a float; caso contrario False.
    try:
        float(valor)
        return True
    except (TypeError, ValueError):
        return False

def categoria_cvss(v):
    # Retorna una categoría de riesgo a partir de un CVSS en [0,10].
    # Umbrales simples: <4 bajo, <7 medio, <9 alto, si no crítico.
    if v < 4.0:
        return "bajo"
    elif v < 7.0:
        return "medio"
    elif v < 9.0:
        return "alto"
    else:
        return "critico"

# ------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------
@app.route('/', methods=['GET'])
def home():
    # Devuelve un mensaje breve para confirmar que la API está activa.
    log_line("ok", "/")
    return jsonify({"message": "La API se encuentra activa: info, sumar, multiplicar, score, cve"}), 200

@app.route('/api/info', methods=['GET'])
def info():
    # Devuelve información básica de la API (nombre, versión, descripción, autor).
    log_line("ok", "/api/info")
    return jsonify({
        "nombre": "API para Operaciones Simples y CVE",
        "version": "2.1.0",
        "descripcion": "Suma, multiplicacion, clasificacion de CVSS y consulta CVE en API publica.",
        "autor": "Grupo 11"
    }), 200

@app.route('/api/sumar', methods=['POST'])
def sumar():
    # Lee el JSON enviado, obtiene 'a' y 'b', valida que existan y que sean numéricos.
    data = request.get_json(silent=True) or {}
    a = data.get("a")
    b = data.get("b")

    # Valida presencia de parámetros.
    if a is None or b is None:
        log_line("bad_request", "/api/sumar", {"razon": "faltan a/b"})
        return jsonify({"error": "Faltan parámetros 'a' y/o 'b'."}), 400

    # Valida que sean numéricos.
    if not es_numero(a) or not es_numero(b):
        log_line("bad_request", "/api/sumar", {"razon": "no_numericos"})
        return jsonify({"error": "Los parámetros 'a' y 'b' deben ser números."}), 400

    # Realiza la operación de suma.
    resultado = float(a) + float(b)
    log_line("ok", "/api/sumar", {"a": a, "b": b, "resultado": resultado})
    return jsonify({"resultado": resultado}), 200

@app.route('/api/multiplicar', methods=['POST'])
def multiplicar():
    # Lee el JSON enviado, obtiene 'a' y 'b', valida que existan y que sean numéricos.
    data = request.get_json(silent=True) or {}
    a = data.get("a")
    b = data.get("b")

    if a is None or b is None:
        log_line("bad_request", "/api/multiplicar", {"razon": "faltan a/b"})
        return jsonify({"error": "Faltan parámetros 'a' y/o 'b'."}), 400

    if not es_numero(a) or not es_numero(b):
        log_line("bad_request", "/api/multiplicar", {"razon": "no_numericos"})
        return jsonify({"error": "Los parámetros 'a' y 'b' deben ser números."}), 400

    # Realiza la operación de multiplicación.
    resultado = float(a) * float(b)
    log_line("ok", "/api/multiplicar", {"a": a, "b": b, "resultado": resultado})
    return jsonify({"resultado": resultado}), 200

@app.route('/api/score', methods=['GET'])
def score():
    # Lee el parámetro 'cvss' de la query, valida que sea numérico y esté en [0,10].
    cvss_raw = request.args.get("cvss")

    if not es_numero(cvss_raw):
        log_line("bad_request", "/api/score", {"razon": "cvss_no_numerico"})
        return jsonify({"error": "Proporcione 'cvss' numérico (0 a 10)."}), 400

    cvss = float(cvss_raw)
    if cvss < 0 or cvss > 10:
        log_line("bad_request", "/api/score", {"razon": "fuera_de_rango"})
        return jsonify({"error": "El 'cvss' debe estar entre 0 y 10."}), 400

    # Determina la categoría de riesgo a partir del CVSS.
    cat = categoria_cvss(cvss)
    log_line("ok", "/api/score", {"cvss": cvss, "categoria": cat})
    return jsonify({"cvss": cvss, "categoria": cat}), 200

@app.route('/api/cve/<cve_id>', methods=['GET'])

def cve(cve_id):

    # Consulta un CVE en la API pública de NIST NVD (Estándar oficial)

    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
 
    try:

        # Es crucial enviar un User-Agent, de lo contrario las APIs públicas bloquean a urllib

        req = urllib.request.Request(

            url, 

            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

        )

        with urllib.request.urlopen(req, timeout=8) as resp:

            data = json.loads(resp.read().decode("utf-8"))
 
            # Validar si NVD encontró resultados

            vulns = data.get("vulnerabilities", [])

            if not vulns:

                log_line("not_found", "/api/cve", {"cve": cve_id})

                return jsonify({"error": "CVE no encontrado en la base de datos."}), 404
 
            # Extraer los datos del primer resultado

            cve_data = vulns[0].get("cve", {})

            # 1. Buscar el resumen (descripción en inglés)

            descriptions = cve_data.get("descriptions", [])

            summary = "Sin resumen disponible."

            for desc in descriptions:

                if desc.get("lang") == "en":

                    summary = desc.get("value")

                    break

            # 2. Buscar el puntaje CVSS (Prioridad: V3.1 -> V3.0 -> V2)

            cvss = None

            metrics = cve_data.get("metrics", {})

            if "cvssMetricV31" in metrics:

                cvss = metrics["cvssMetricV31"][0]["cvssData"].get("baseScore")

            elif "cvssMetricV30" in metrics:

                cvss = metrics["cvssMetricV30"][0]["cvssData"].get("baseScore")

            elif "cvssMetricV2" in metrics:

                cvss = metrics["cvssMetricV2"][0]["cvssData"].get("baseScore")
 
            # 3. Armar la salida

            cve_out = {

                "id": cve_data.get("id"),

                "summary": summary,

                "cvss": cvss

            }
 
            # Si hay CVSS, asignarle la categoría

            if es_numero(cve_out["cvss"]):

                v = float(cve_out["cvss"])

                cve_out["categoria"] = categoria_cvss(v)
 
            log_line("ok", "/api/cve", {"cve": cve_id})

            return jsonify(cve_out), 200
 
    except urllib.error.HTTPError as e:

        log_line("upstream_error", "/api/cve", {"cve": cve_id, "status": e.code})

        return jsonify({"error": "La API externa rechazó la conexión (probablemente límite de tasa)."}), 502

    except Exception as e:

        log_line("error", "/api/cve", {"cve": cve_id, "error": str(e)})

        return jsonify({"error": "No se pudo obtener el CVE en este momento."}), 502
 

# Punto de entrada de la app (desarrollo local / Docker / Cloud Run).
if __name__ == "__main__":
    # host 0.0.0.0 permite recibir conexiones desde Docker/Cloud Run
    # puerto 8080 es el estándar que usamos en Docker y Cloud Run
    app.run(debug=True, host="0.0.0.0", port=8080)