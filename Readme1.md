# SRH – SISTEMA DE RESERVAS DE HOTELES BACKEND – FASTAPI (SEGUNDA PARTE)
## Pruebas Unitarias (T02.04)

Backend del Sistema de Reservas de Hoteles (SRH)

UNIVERSIDAD POLITÉCNICA SALESIANA – UPS

Materia: Ingeniería de Software

Tarea: T02.04 – Pruebas Unitarias

Grupo: B

Integrantes:
- Andrea Murillo Medina
- Andy Arévalo Dueñas
- Keyla Sisalima Torres
- Gregory Morán Silva

Fecha: 09/01/2026

Docente: Darío Huilcapi

---

## Descripción de la Tarea T02.04

La Tarea T02.04 tiene como objetivo implementar pruebas unitarias automáticas
sobre el backend desarrollado en la Tarea T02.03, utilizando frameworks de testing
acordes al lenguaje Python.
Se valida el correcto funcionamiento de los endpoints del sistema y se garantiza
una cobertura mínima del 60% de los métodos, cumpliendo con la rúbrica de
evaluación establecida.

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
- Implementación de pruebas unitarias y cobertura: Andrea Murillo
- Elaboración del diagrama UML general (Controller, Service, Repository, Crud): Keyla Sisalima
- Apoyo en revisión, ajustes y mejoras del proyecto: Andy Arévalo
- Control de versiones y repositorio GitHub: Andrea Murillo y Andy Arévalo

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

Las pruebas unitarias se encuentran organizadas en la carpeta test/:

test/
├── test_root.py
├── test_usuarios.py
├── test_clientes.py
├── test_habitaciones.py
├── test_reservas.py
├── test_facturas.py
└── test_pagos.py

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

Para ejecutar pruebas con cobertura:

coverage run -m pytest
coverage report -m

La cobertura obtenida cumple con el mínimo del 60% requerido.

El trabajo colaborativo se realizó mediante GitHub, utilizando commits
progresivos. Se realizaron más de 10 commits, permitiendo evidenciar la
participación de los integrantes del grupo y el avance en la implementación de
pruebas unitarias.

La implementación de pruebas unitarias permitió validar el correcto
funcionamiento del backend del Sistema de Reservas de Hoteles, mejorar la calidad
del código y reducir errores en los servicios REST. El uso de Pytest y Coverage
facilitó la detección de fallos y el cumplimiento de la cobertura mínima exigida,
fortaleciendo la confiabilidad del sistema y preparándolo para futuras mejoras.
