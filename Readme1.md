# SRH – SISTEMA DE RESERVAS DE HOTELES BACKEND – FASTAPI (SEGUNDA PARTE) 
## T02.04 – Pruebas Unitarias y Cobertura

Backend del Sistema de Reservas de Hoteles (SRH) desarrollado con FastAPI, ampliado con pruebas unitarias automáticas y medición de cobertura de código.

**Universidad Politécnica Salesiana – UPS**  
**Materia:** Ingeniería de Software  
**Tarea:** T02.04 – Pruebas Unitarias  
**Grupo:** B  
**Docente:** Darío Huilcapi  
**Fecha:** 13/01/2026  

### Integrantes
- Andrea Murillo Medina  
- Andy Arévalo Dueñas  
- Keyla Sisalima Torres  
- Gregory Morán Silva  
- Kevin Ramírez Villón 

---
## 1. Objetivo de la Tarea (T02.04)

Implementar pruebas unitarias sobre el backend desarrollado en la T02.03 para verificar el correcto funcionamiento de los endpoints REST.  
Además, se ejecuta análisis de cobertura para garantizar una cobertura mínima del 60% según la rúbrica.

---

## Descripción de la Tarea T02.04

La Tarea T02.04 tiene como objetivo implementar pruebas unitarias automáticas
sobre el backend desarrollado en la Tarea T02.03, utilizando frameworks de testing
acordes al lenguaje Python.
Se valida el correcto funcionamiento de los endpoints del sistema y se garantiza
una cobertura mínima del 60% de los métodos, cumpliendo con la rúbrica de
evaluación establecida.

---

## 2. Tecnologías y herramientas utilizadas

- **FastAPI** (API REST)
- **Uvicorn** (servidor ASGI)
- **Pytest** (ejecución de pruebas)
- **FastAPI TestClient** (pruebas de endpoints)
- **Coverage.py** (cobertura de código)
- **Git y GitHub** (control de versiones y trabajo colaborativo)

---

## Gestión del Proyecto

El repositorio del proyecto fue creado en GitHub para el control de versiones y
seguimiento del desarrollo. El backend fue implementado inicialmente en la Tarea
T02.03 y posteriormente ampliado en la T02.04 con la incorporación de pruebas
unitarias y análisis de cobertura.

El control de versiones se gestionó mediante commits progresivos, permitiendo
evidenciar la participación de los integrantes del grupo y el avance del proyecto.

---

## Asignación de Tareas

- Diseño e implementación del backend (FastAPI): Andrea Murillo
- Gestión de clientes, habitaciones, reservas, facturas y pagos: Andrea Murillo
- Implementación y actualización de pruebas unitarias en carpeta test/: Andrea Murillo, Keyla Sisalima , Andy Arevalo y Kevin Ramirez
- Actualización de documentación README1.md y bitácora comandos_t02_04.txt: Andrea Murillo , Gregory Morán
- Apoyo en revisión, ajustes y mejoras del proyecto: Andy Arévalo
- Control de versiones y repositorio GitHub: Andrea Murillo , Andy Arévalo y Keyla Sisalima

---

## Backend y Framework

El backend del sistema SRH corresponde a una API REST desarrollada con FastAPI,
permitiendo la creación de servicios eficientes y la documentación automática
mediante Swagger (OpenAPI).

---

## Pruebas Unitarias – Frameworks Utilizados

Para la implementación de pruebas unitarias se utilizaron los siguientes
frameworks y herramientas:

- Pytest – Ejecución de pruebas unitarias
- FastAPI TestClient – Pruebas de endpoints REST
- Coverage.py – Medición de cobertura de código

---

## Estructura de Pruebas

Las pruebas unitarias se encuentran organizadas en la carpeta 'app/test/':

app/test/
├── test_root.py
├── test_usuarios.py
├── test_clientes.py
├── test_habitaciones.py
├── test_reservas.py
├── test_facturas.py
├── test_pagos.py
└── test_reportes.py


Cada archivo contiene pruebas orientadas a validar la creación, consulta y
funcionamiento de los endpoints correspondientes, asegurando la correcta
respuesta del sistema ante distintas solicitudes.

Para la ejecución del backend se utilizó el servidor ASGI Uvicorn:

uvicorn app.main:app --reload

Una vez en ejecución, el sistema permite el acceso a la documentación interactiva
y a la definición formal de la API a través de los siguientes enlaces:

Swagger UI: http://127.0.0.1:8000/docs
OpenAPI JSON: http://127.0.0.1:8000/openapi.json

Para ejecutar todas las pruebas unitarias:

pytest

Ejecutar pruebas con detalle:

python -m pytest app/test -v


Para ejecutar pruebas con cobertura (Coverage):

python -m coverage run -m pytest app/test -v

python -m coverage report -m

Generar reporte HTML:

python -m coverage html

Abrir reporte HTML (Windows):

start htmlcov/index.html

La cobertura obtenida cumple con el mínimo del 60% requerido.

El trabajo colaborativo se realizó mediante GitHub, utilizando commits
progresivos. Se realizaron más de 10 commits, permitiendo evidenciar la
participación de los integrantes del grupo y el avance en la implementación de
pruebas unitarias.


Conclusión:

La implementación de pruebas unitarias permitió validar el correcto
funcionamiento del backend del Sistema de Reservas de Hoteles, mejorar la calidad
del código y reducir errores en los servicios REST. El uso de Pytest y Coverage
facilitó la detección de fallos y el cumplimiento de la cobertura mínima exigida,
fortaleciendo la confiabilidad del sistema y preparándolo para futuras mejoras.
