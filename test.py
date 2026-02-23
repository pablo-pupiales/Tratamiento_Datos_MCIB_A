# test.py
# ------------------------------------------------------------
# Script de prueba simple para el API que corre en localhost:8080
# ------------------------------------------------------------
import requests

def get_info():
    # Realiza una consulta GET al endpoint /api/info y devuelve el JSON de respuesta.
    return requests.get("http://localhost:8080/api/info").json()

def post_sumar(a, b):
    # Envía un JSON con 'a' y 'b' al endpoint /api/sumar y devuelve el JSON de respuesta.
    return requests.post("http://localhost:8080/api/sumar",
                         json={"a": a, "b": b}).json()

def post_multiplicar(a, b):
    # Envía un JSON con 'a' y 'b' al endpoint /api/multiplicar y devuelve el JSON de respuesta.
    return requests.post("http://localhost:8080/api/multiplicar",
                         json={"a": a, "b": b}).json()

def get_cve(cve_id):
    # Consulta un CVE específico en /api/cve/<cve_id> y devuelve el JSON de respuesta.
    return requests.get(f"http://localhost:8080/api/cve/{cve_id}").json()

def get_score(cvss):
    # Consulta la categoría de riesgo a partir de un CVSS en /api/score.
    return requests.get("http://localhost:8080/api/score",
                        params={"cvss": cvss}).json()

if __name__ == "__main__":
    print("INFO:", get_info())
    print("SUMAR 7 + 20:", post_sumar(7, 20))
    print("MULTIPLICAR 7 * 20:", post_multiplicar(7, 20))
    print("CVE (CVE-2021-44228):", get_cve("CVE-2021-44228"))
    print("SCORE CVSS=9.8:", get_score(9.8))