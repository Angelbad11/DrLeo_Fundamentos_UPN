def arreglos_paralelos_mascotas(mascotas):
    """Devuelve cinco arreglos cuyo índice i identifica a la MISMA mascota."""
    codigos, nombres, edades, especies, propietarios = [], [], [], [], []
    for mascota in mascotas:
        codigos.append(mascota.id_ponkis)
        nombres.append(mascota.nombre.strip())
        edades.append(int(mascota.edad))
        especies.append(mascota.especie.strip())
        propietarios.append(mascota.propietario.nombre.strip())
    return codigos, nombres, edades, especies, propietarios


def buscar_secuencial(codigos, codigo_buscado):
    """Busca el código; devuelve su posición, o -1 si no existe."""
    buscado = str(codigo_buscado).strip().casefold()
    for i in range(len(codigos)):
        if str(codigos[i]).strip().casefold() == buscado:
            return i
    return -1


def ordenar_pares_burbuja(pares, criterio="Registro original"):
    """Ordena una copia de (indice_original, mascota), sin perder relaciones.

    Complejidad máxima temporal O(n²); memoria adicional O(n).
    """
    resultado = list(pares)
    if criterio == "Registro original":
        return resultado
    criterios_validos = (
        "Nombre A-Z", "Nombre Z-A",
        "Edad: menor a mayor", "Edad: mayor a menor"
    )
    if criterio not in criterios_validos:
        raise ValueError("Criterio de ordenamiento desconocido.")
    por_edad = criterio.startswith("Edad:")
    descendente = criterio in ("Nombre Z-A", "Edad: mayor a menor")

    def clave(par):
        mascota = par[1]
        return int(mascota.edad) if por_edad else mascota.nombre.strip().casefold()

    n = len(resultado)
    for i in range(n - 1):
        intercambio = False
        for j in range(n - i - 1):
            a, b = clave(resultado[j]), clave(resultado[j + 1])
            if (a < b) if descendente else (a > b):
                resultado[j], resultado[j + 1] = resultado[j + 1], resultado[j]
                intercambio = True
        if not intercambio:
            break
    return resultado


def matriz_atenciones(atenciones):
    """Cada fila: [codigo_mascota, fecha, diagnostico, tratamiento, vacuna]."""
    matriz = []
    for atencion in atenciones:
        matriz.append([
            atencion.mascota.id_ponkis,
            atencion.fecha,
            atencion.diagnostico,
            atencion.tratamiento,
            atencion.vacuna,
        ])
    return matriz


def buscar_en_matriz(matriz, codigo_mascota):
    """Retorna las filas de atenciones del paciente consultado."""
    filas = []
    for fila in matriz:
        if fila[0].casefold() == codigo_mascota.strip().casefold():
            filas.append(fila.copy())
    return filas


def evidencia_en_texto(mascotas, atenciones):
    """Muestra la relación de los conceptos del curso con datos del sistema."""
    codigos, nombres, edades, especies, propietarios = arreglos_paralelos_mascotas(mascotas)
    matriz = matriz_atenciones(atenciones)
    ordenados = ordenar_pares_burbuja(list(enumerate(mascotas)), "Nombre A-Z")
    lineas = [
        "FUNDAMENTOS DE PROGRAMACIÓN - DR. LEO",
        "Evidencia técnica de arreglos, búsqueda y ordenamiento",
        "=" * 56,
        f"Arreglo unidimensional de códigos: {codigos}",
        f"Arreglo unidimensional de nombres: {nombres}",
        f"Arreglo unidimensional de edades: {edades}",
        "",
        "ARREGLOS PARALELOS",
        "Posición | Código | Mascota | Edad | Especie | Propietario",
    ]
    for i in range(len(codigos)):
        lineas.append(f"{i} | {codigos[i]} | {nombres[i]} | {edades[i]} | {especies[i]} | {propietarios[i]}")
    lineas += ["", "ORDENAMIENTO BURBUJA POR NOMBRE (A-Z)"]
    for indice_original, mascota in ordenados:
        lineas.append(f"Índice {indice_original}: {mascota.id_ponkis} - {mascota.nombre}")
    lineas += ["", "BÚSQUEDA SECUENCIAL"]
    if codigos:
        codigo = codigos[0]
        lineas.append(f"Código {codigo}: índice {buscar_secuencial(codigos, codigo)}")
    else:
        lineas.append("Todavía no hay pacientes para buscar.")
    lineas += ["", "MATRIZ BIDIMENSIONAL DE ATENCIONES", "[código, fecha, diagnóstico, tratamiento, vacuna]"]
    for fila in matriz:
        lineas.append(str(fila))
    if not matriz:
        lineas.append("Sin atenciones registradas.")
    lineas += ["", f"Total mascotas: {len(codigos)}", f"Total atenciones: {len(matriz)}"]
    return "\n".join(lineas)
