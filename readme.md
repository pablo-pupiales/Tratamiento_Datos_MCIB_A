


# Proyecto: Tratamiento de Datos MCIB-A (Grupo 11)

El informe del proyecto se encuentra en la siguiente ubicación: docs/Informe_Clase1_Grupo11.docx

Este repositorio contiene el proyecto desarrollado en Visual Studio Code, utilizando Git y GitHub para control de versiones y colaboración.  
El sistema expone endpoints para operaciones matemáticas, cálculo de CVSS y consultas a una API externa sobre vulnerabilidades CVE.  
Las pruebas se ejecutaron en ambiente local y en Google Cloud mediante test.py, Docker y curl.



## Endpoints implementados

- **GET /info** → Información general del servicio.  
- **POST /sumar** → Suma dos valores enviados por el cliente.  
- **POST /multiplicar** → Multiplica dos valores enviados por el cliente.  
- **POST /cvss** → Calcula o devuelve un puntaje CVSS.  
- **GET /cves** → Consulta una API externa para obtener datos de CVE.


## Pruebas

**Herramientas usadas:** 
tests/test.py, curl, Docker, ejecución local y despliegue en Google Cloud.

**Ejemplos con curl:**
# Información del servicio
curl http://localhost:8000/info

# Suma
curl -X POST http://localhost:8000/sumar -H "Content-Type: application/json" -d "{\"a\": 7, \"b\": 20}"

# Multiplicación
curl -X POST http://localhost:8000/multiplicar -H "Content-Type: application/json" -d "{\"a\": 7, \"b\": 20}"

# Consulta de un CVE concreto
curl "http://localhost:8000/cves?cve_id=CVE-2021-44228"


