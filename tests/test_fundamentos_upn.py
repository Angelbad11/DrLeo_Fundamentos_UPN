"""Pruebas específicas de Fundamentos de Programación, sin datos reales."""

import pytest

from services.algoritmos_fundamentos import (
    arreglos_paralelos_mascotas, buscar_secuencial, buscar_en_matriz,
    evidencia_en_texto, matriz_atenciones, ordenar_pares_burbuja,
)
from services.clinica_service import ClinicaService


def poblar_servicio(tmp_path):
    s = ClinicaService(tmp_path / "datos.json")
    a = s.registrar_propietario("Ana Torres", "12345678", "999888777")
    b = s.registrar_propietario("Luis Perez", "87654321", "988777666")
    zeus = s.registrar_mascota("Zeus", "Canina", "5", a)
    bobby = s.registrar_mascota("Bobby", "Canina", "2", b)
    luna = s.registrar_mascota("Luna", "Felina", "3", a)
    return s, zeus, bobby, luna


def test_arreglos_paralelos_mantienen_propietarios(tmp_path):
    s, zeus, bobby, luna = poblar_servicio(tmp_path)
    codigos, nombres, edades, especies, propietarios = arreglos_paralelos_mascotas(s.mascotas)
    assert nombres == ["Zeus", "Bobby", "Luna"]
    assert edades == [5, 2, 3]
    assert propietarios == ["Ana Torres", "Luis Perez", "Ana Torres"]
    assert codigos == [zeus.id_ponkis, bobby.id_ponkis, luna.id_ponkis]
    assert buscar_secuencial(codigos, bobby.id_ponkis.lower()) == 1
    assert buscar_secuencial(codigos, "M-9999") == -1


@pytest.mark.parametrize("criterio,nombres", [
    ("Nombre A-Z", ["Bobby", "Luna", "Zeus"]),
    ("Nombre Z-A", ["Zeus", "Luna", "Bobby"]),
    ("Edad: menor a mayor", ["Bobby", "Luna", "Zeus"]),
    ("Edad: mayor a menor", ["Zeus", "Luna", "Bobby"]),
    ("Registro original", ["Zeus", "Bobby", "Luna"]),
])
def test_burbuja_orden_y_referencias(tmp_path, criterio, nombres):
    s, zeus, bobby, luna = poblar_servicio(tmp_path)
    pares = list(enumerate(s.mascotas))
    resultado = ordenar_pares_burbuja(pares, criterio)
    assert [m.nombre for _, m in resultado] == nombres
    assert [s.mascotas[i] is m for i, m in resultado] == [True] * 3
    assert [m.nombre for m in s.mascotas] == ["Zeus", "Bobby", "Luna"]
    assert resultado is not pares


def test_matriz_bidimensional_e_informe(tmp_path):
    s, zeus, bobby, luna = poblar_servicio(tmp_path)
    s.registrar_atencion(luna, "19/10/2026", "Control", "Reposo", "Rabia")
    s.registrar_atencion(zeus, "20/10/2026", "Revisión", "Vitaminas", "Ninguna")
    matriz = matriz_atenciones(s.atenciones)
    assert len(matriz) == 2
    assert all(len(fila) == 5 for fila in matriz)
    assert buscar_en_matriz(matriz, luna.id_ponkis)[0][2] == "Control"
    assert buscar_en_matriz(matriz, "M-9999") == []
    texto = evidencia_en_texto(s.mascotas, s.atenciones)
    assert "ARREGLOS PARALELOS" in texto
    assert "MATRIZ BIDIMENSIONAL" in texto


@pytest.mark.parametrize("edad", ["-1", "3.5", "perro", "101", "20 años", ""])
def test_edad_invalida_rechazada(tmp_path, edad):
    s = ClinicaService(tmp_path / "datos.json")
    p = s.registrar_propietario("Ana", "12345678", "999888777")
    with pytest.raises(ValueError):
        s.registrar_mascota("Luna", "Canina", edad, p)
    assert not s.mascotas


def test_fecha_hora_invalidas_no_se_guardan(tmp_path):
    s, zeus, _, _ = poblar_servicio(tmp_path)
    with pytest.raises(ValueError, match="Fecha inválida"):
        s.registrar_cita(zeus, "30/02/2026", "10:00", "Control")
    with pytest.raises(ValueError, match="Hora inválida"):
        s.registrar_cita(zeus, "21/10/2026", "25:00", "Control")
    with pytest.raises(ValueError, match="Fecha inválida"):
        s.registrar_atencion(zeus, "99/10/2026", "A", "B", "C")
    assert not s.citas and not s.atenciones


def test_cita_duplicada_y_cancelacion(tmp_path):
    s, zeus, bobby, _ = poblar_servicio(tmp_path)
    primera = s.registrar_cita(zeus, "20/10/2026", "09:30", "Control")
    with pytest.raises(ValueError, match="cita activa"):
        s.registrar_cita(bobby, "2026-10-20", "09:30", "Vacuna")
    s.cambiar_estado_cita(0, "Cancelada")
    nueva = s.registrar_cita(bobby, "2026-10-20", "09:30", "Vacuna")
    assert primera.estado == "Cancelada" and nueva.estado == "Pendiente"


def test_edicion_cita_no_puede_colisionar(tmp_path):
    s, zeus, bobby, _ = poblar_servicio(tmp_path)
    s.registrar_cita(zeus, "20/10/2026", "09:30", "Control")
    s.registrar_cita(bobby, "20/10/2026", "10:30", "Vacuna")
    with pytest.raises(ValueError, match="cita activa"):
        s.actualizar_cita(1, bobby, "2026-10-20", "09:30", "Vacuna", "Pendiente")
    assert s.citas[1].hora == "10:30"


def test_pago_infinito_rechazado(tmp_path):
    s = ClinicaService(tmp_path / "datos.json")
    with pytest.raises(ValueError):
        s.registrar_pago("Consulta", "nan", "Yape", "Confirmado")
    with pytest.raises(ValueError):
        s.registrar_pago("Consulta", "inf", "Yape", "Confirmado")


def test_persistencia_integral(tmp_path):
    s, zeus, _, _ = poblar_servicio(tmp_path)
    s.registrar_cita(zeus, "20/10/2026", "09:30", "Control")
    s.registrar_atencion(zeus, "20/10/2026", "Sin hallazgos", "Seguimiento", "Rabia")
    recuperado = ClinicaService(tmp_path / "datos.json")
    assert len(recuperado.mascotas) == 3
    assert len(recuperado.citas) == 1
    assert len(recuperado.atenciones) == 1
    assert recuperado.mascotas[0].propietario.nombre == "Ana Torres"
