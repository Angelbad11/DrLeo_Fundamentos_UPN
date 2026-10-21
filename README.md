# Datos de demostración

Este paquete incluye **10 propietarios ficticios**, **10 mascotas ficticias**,
**10 citas**, **10 atenciones** y **10 pagos** de ejemplo para practicar la interfaz.
Los DNI de ejemplo empiezan con `70` (8 cifras) y los celulares con `9` (9 cifras).
Estos números son **generados aleatoriamente para pruebas**, no son contactos
verificados ni deben usarse para llamar o enviar mensajes.

Para evitar reemplazar datos existentes, abre este proyecto en una carpeta nueva.
Para volver a los datos de ejemplo después de editarlos, extrae de nuevo el ZIP.

---

# Clínica Veterinaria Dr. Leo — Fundamentos de Programación

Sistema academico desarrollado en Python para la gestion de una clinica veterinaria.  
El proyecto permite registrar propietarios, mascotas, citas, consultas, pagos, historial clinico, recordatorios y reportes.

## Funciones principales

- Registro y edicion de propietarios.
- Proteccion de DNI y numero de celular.
- Registro de mascotas con sexo y estado de esterilizacion.
- Gestion de citas veterinarias.
- Registro de consultas con diagnostico, tratamiento y vacuna.
- Registro de pagos con concepto, monto, metodo y estado.
- Generacion de historial clinico por mascota.
- Generacion de recordatorios de citas.
- Generacion de reportes diarios.
- Exportacion de datos en CSV.
- Persistencia de datos en JSON y SQLite.

## Estructura del proyecto

| Archivo o carpeta | Descripcion |
| --- | --- |
| `main.py` | Punto de entrada de la aplicacion |
| `gui/app.py` | Interfaz grafica desarrollada con Tkinter |
| `models/entidades.py` | Entidades principales del sistema |
| `services/clinica_service.py` | Reglas de negocio, persistencia y exportacion |
| `tests/test_clinica_service.py` | Pruebas automatizadas |
| `assets/fondo.png` | Recurso visual usado como fondo |

## Ejecucion

Desde Visual Studio Code o PowerShell ejecutar:

```bash
python main.py
```

## Flujo recomendado de uso

1. Registrar propietarios.
2. Registrar mascotas.
3. Gestionar citas.
4. Registrar consultas.
5. Registrar pagos.
6. Revisar historial clinico.
7. Generar recordatorios.
8. Generar reportes.

## Tecnologias utilizadas

- Python
- Tkinter
- SQLite
- JSON
- CSV
- Pytest
- Git y GitHub

## Buenas practicas aplicadas

- Separacion del proyecto por carpetas.
- Uso de clases para representar entidades.
- Manejo de errores y validaciones.
- Pruebas automatizadas.
- Proteccion de datos personales.
- Commits descriptivos en español.
- Interfaz grafica ordenada por flujo de trabajo.

## Proyecto academico

Adaptación académica para el curso Fundamentos de Programación (CIIN1205P). El número de grupo del curso actual queda por definir.


## Adaptación al desafío Fundamentos de Programación (CIIN1205P)

Esta es una **copia adaptada** del proyecto original Dr. Leo, utilizada con autorización docente para aplicar lógica y algoritmos al caso de la clínica veterinaria.

- **Ver algoritmos dentro de la interfaz:** entrar a *Reportes* y pulsar **Ver algoritmos UPN (arreglos y matriz)**.
- **Ordenar pacientes:** en *Gestión de mascotas*, selector **Ordenar por** (A–Z, Z–A, edad asc/desc). La ordenación utiliza burbuja sobre pares que conservan su índice original.
- **Módulo didáctico:** `services/algoritmos_fundamentos.py` implementa arreglos paralelos, búsqueda secuencial, burbuja y matriz de atenciones.
- **Validación adicional:** edades, citas duplicadas, fechas y horas inválidas y montos no finitos.
- **Pruebas:** ejecutar `py -m pip install -r requirements.txt` y `py -m pytest -q`. Requiere `pytest` (puedes instalarlo con `py -m pip install pytest`).

Se conserva la interfaz de una sola ventana del proyecto de GitHub; no se usan nuevos dashboards ni ventanas principales independientes. El proyecto está diseñado para pruebas con datos ficticios.

**Seguridad:** en el código original hay un mecanismo reversible basado en XOR con una clave fija; no debe considerarse cifrado fuerte ni usarse para información clínica personal real. No publicar ni compartir la carpeta `data/`.


## Registro de ejemplo incluido

Al abrir **Gestión de propietarios** encontrarás un único registro ficticio de práctica:

- **Nombre:** Ana Torres (Demo)
- **DNI ficticio:** 00000000
- **Teléfono ficticio:** 900000000
- **Código:** P-0001

No se incluyen mascotas, citas, consultas ni pagos de ejemplo. Puedes buscar el nombre **Ana** o editar el propietario desde la misma interfaz. El registro está precargado en `data/datos_clinica.json` y también se genera en el primer inicio de una instalación nueva sin datos. Si ya tienes registros de otra copia, **no sobrescribas su carpeta `data/`**. Este contenido se proporciona solo para prácticas y no representa a una persona real.
