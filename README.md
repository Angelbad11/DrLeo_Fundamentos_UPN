# Clínica Veterinaria Dr. Leo - Fundamentos de Programación

Sistema académico desarrollado en Python para la gestión de una clínica veterinaria.

El proyecto permite registrar propietarios, mascotas, citas, consultas, pagos, historial clínico, recordatorios y reportes.

## Funciones principales

- Registro, búsqueda y edición de propietarios.
- Protección visual de DNI y número de celular.
- Registro de mascotas con sexo y estado de esterilización.
- Búsqueda y ordenamiento de mascotas por nombre y edad.
- Gestión de citas veterinarias.
- Registro de consultas con diagnóstico, tratamiento y vacuna.
- Registro de pagos con concepto, monto, método y estado.
- Generación de historial clínico por mascota.
- Generación de recordatorios de citas.
- Generación de reportes diarios.
- Exportación de datos en CSV.
- Persistencia de datos en JSON y SQLite.

## Estructura del proyecto

| Archivo o carpeta | Descripción |
|---|---|
| `main.py` | Punto de entrada de la aplicación |
| `gui/app.py` | Interfaz gráfica desarrollada con Tkinter |
| `models/entidades.py` | Entidades principales del sistema |
| `services/clinica_service.py` | Reglas de negocio, persistencia y exportación |
| `services/algoritmos_fundamentos.py` | Búsqueda, ordenamiento y estructuras de datos |
| `tests/` | Pruebas automatizadas |
| `assets/fondo.png` | Recurso visual utilizado por el sistema |

## Ejecución

Desde Visual Studio Code o PowerShell ejecutar:

`py main.py`

## Flujo recomendado de uso

1. Registrar propietarios.
2. Registrar mascotas.
3. Buscar y ordenar registros.
4. Gestionar citas.
5. Registrar consultas.
6. Registrar pagos.
7. Revisar historial clínico.
8. Generar recordatorios.
9. Generar reportes.

## Tecnologías utilizadas

- Python
- Tkinter
- SQLite
- JSON
- CSV
- Pytest
- Git y GitHub

## Buenas prácticas aplicadas

- Separación del proyecto por carpetas.
- Uso de clases para representar entidades.
- Aplicación de funciones y programación modular.
- Uso de arreglos unidimensionales, bidimensionales y paralelos.
- Implementación de algoritmos de búsqueda y ordenamiento.
- Manejo de errores y validaciones.
- Pruebas automatizadas.
- Organización y persistencia de datos.
- Control de versiones mediante Git y GitHub.
- Interfaz gráfica ordenada por flujo de trabajo.

## Proyecto académico

Proyecto desarrollado para el curso **Fundamentos de Programación (CIIN1205P)** de la **Universidad Privada del Norte (UPN)**.
