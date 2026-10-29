"""propio 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 Anfitrión 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as SistemaOperativo

rutaLista = "/lib/.pip.json"


def valorHuella(Datos):
    return "".join("%02x" % valor for valor in hashlib.sha256(Datos).digest())


def leerLista():
    if SistemaOperativo.path_kind(rutaLista) == 0:
        return {}
    return json.loads(SistemaOperativo.read(rutaLista).decode("utf-8"))


def escribirDiario(ruta, Datos):
    if SistemaOperativo.write(ruta, Datos) != len(Datos):
        raise OSError(28)


def comprobarRuta(ruta):
    if not isinstance(ruta, str) or not ruta.endswith(".py"):
        raise ValueError("Python 소스만 설치할 númeroValor 있습니다.")
    if any(valorSubparte in ("", ".", "..") or valorSubparte.startswith(".") for valorSubparte in ruta.split("/")):
        raise ValueError("허용하지 않는 Paquete ruta")
    if "\\" in ruta or any(ord(valorCarácter) < 32 or ord(valorCarácter) == 127 for valorCarácter in ruta):
        raise ValueError("잘못된 ruta Caracteres")
    resultado = "/lib/" + ruta
    if len(resultado.encode("utf-8")) > 63 or ruta in ("español.py", "Paquete.py"):
        raise ValueError("Paquete 경로가 너무 길거나 valorPredeterminado 라이브러리와 겹칩니다.")
    return resultado


class recibirFlujo:
    def __init__(valorPropio, extremo):
        valorPropio.extremo = extremo
        valorPropio.datosRestante = b""
        valorPropio.ponerEnMarcha = SistemaOperativo.ticks_ms()

    def leerExactamente(valorPropio, longitud):
        Datos = bytearray()
        while len(Datos) < longitud:
            if SistemaOperativo.ticks_ms() - valorPropio.ponerEnMarcha > 90000:
                raise ValueError("Paquete retransmitirValor respuesta valorTiempo 초과")
            if not valorPropio.datosRestante:
                try:
                    valorPropio.datosRestante = SistemaOperativo.tcp_read(valorPropio.extremo, 512)
                except OSError as error:
                    if error.args[0] != 11:
                        raise
                    SistemaOperativo.sleep_ms(10)
                    continue
                if not valorPropio.datosRestante:
                    raise ValueError("Paquete 전송이 중간에 끝났습니다.")
            númeroElementosElementoLista = min(longitud - len(Datos), len(valorPropio.datosRestante))
            Datos.extend(valorPropio.datosRestante[:númeroElementosElementoLista])
            valorPropio.datosRestante = valorPropio.datosRestante[númeroElementosElementoLista:]
            SistemaOperativo.sleep_ms(0)
        return bytes(Datos)


def descargar(petición, númeroPuerto):
    if len(petición) > 96 or any(valorCarácter not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for valorCarácter in petición):
        raise ValueError("사용법: pip install nombre 또는 nombre==버전")
    extremo = SistemaOperativo.tcp_open()
    try:
        ponerEnMarcha = SistemaOperativo.ticks_ms()
        while True:
            try:
                SistemaOperativo.tcp_connect(extremo, "10.0.2.2", númeroPuerto)
                break
            except OSError as error:
                if error.args[0] not in (11, 115) or SistemaOperativo.ticks_ms() - ponerEnMarcha > 5000:
                    raise ValueError("Paquete retransmitirValor conectar valorFallo: 호스트에서 --network --pip로 실행하십시오.")
                SistemaOperativo.sleep_ms(10)
        Datos = (petición + "\n").encode()
        while Datos:
            try:
                númeroElementosElementoLista = SistemaOperativo.tcp_write(extremo, Datos)
                if not númeroElementosElementoLista:
                    raise ValueError("Paquete petición valorTransferencia valorFallo")
                Datos = Datos[númeroElementosElementoLista:]
            except OSError as error:
                if error.args[0] != 11:
                    raise
                SistemaOperativo.sleep_ms(10)
                if SistemaOperativo.ticks_ms() - ponerEnMarcha > 10000:
                    raise ValueError("Paquete petición valorTransferencia valorTiempo 초과")
        valorFlujo = recibirFlujo(extremo)
        valorCabecera = valorFlujo.leerExactamente(8)
        if valorCabecera[:4] != b"JKP1":
            raise ValueError("Paquete valorTransferencia valorContrato 불일치")
        longitud = (valorCabecera[4] << 24) | (valorCabecera[5] << 16) | (valorCabecera[6] << 8) | valorCabecera[7]
        if longitud > 8192:
            raise ValueError("Paquete 명세가 너무 큽니다.")
        especificación = json.loads(valorFlujo.leerExactamente(longitud).decode())
        if "error" in especificación:
            raise ValueError(especificación["error"])
        if not 1 <= len(especificación["files"]) <= 16:
            raise ValueError("꾸러미당 árbolFuente 파일은 1~16개여야 합니다.")
        if sum(valorEntradaElemento["size"] for valorEntradaElemento in especificación["files"]) > 65536:
            raise ValueError("Paquete árbolFuente 합계는 64 KiB 이하여야 합니다.")
        entradasArchivo = {}
        for valorEntradaElemento in especificación["files"]:
            ruta = comprobarRuta(valorEntradaElemento["path"])
            if ruta in entradasArchivo or not 0 <= valorEntradaElemento["size"] <= 16384:
                raise ValueError("중복 ruta 또는 Archivo tamaño 초과")
            Datos = valorFlujo.leerExactamente(valorEntradaElemento["size"])
            if valorHuella(Datos) != valorEntradaElemento["sha256"]:
                raise ValueError("Paquete Archivo SHA-256 불일치")
            # 실행하지 않고 elementoListaActual MicroPython의 문법으로 먼저 검사한다.
            compile(Datos.decode("utf-8"), ruta, "exec")
            entradasArchivo[ruta] = Datos
            gc.collect()
        return especificación, entradasArchivo
    finally:
        SistemaOperativo.udp_close(extremo)


def instalarValor(petición, númeroPuerto):
    print("Paquete descargar:", petición)
    especificación, entradasArchivo = descargar(petición, númeroPuerto)
    listaEntradaElemento = leerLista()
    nombre = especificación["name"]
    if nombre in listaEntradaElemento:
        if listaEntradaElemento[nombre]["version"] == especificación["version"]:
            for ruta, datosHuella in listaEntradaElemento[nombre]["files"].items():
                if SistemaOperativo.path_kind(ruta) != 1 or valorHuella(SistemaOperativo.read(ruta)) != datosHuella:
                    raise ValueError("설치된 Paquete 파일이 달라졌습니다: " + ruta)
            print("이미 설치됨:", nombre, especificación["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 valorLadoPosterior 설치하십시오.")
    for ruta in entradasArchivo:
        if SistemaOperativo.path_kind(ruta):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + ruta)
    listaEntradaElemento[nombre] = {"version": especificación["version"], "files": {ruta: valorHuella(Datos) for ruta, Datos in entradasArchivo.items()}}
    listaNuevo = json.dumps(listaEntradaElemento).encode()
    if len(listaNuevo) > 16384:
        raise ValueError("Paquete listaEntradaElemento tamaño 초과")
    listaElementoPrevio = SistemaOperativo.read(rutaLista) if SistemaOperativo.path_kind(rutaLista) else None
    archivoCreado = []
    directorioCreado = []
    try:
        for ruta, Datos in entradasArchivo.items():
            partes = ruta.split("/")
            for númeroValor in range(2, len(partes)):
                valorDirectorio = "/".join(partes[:númeroValor])
                valorClaseTipo = SistemaOperativo.path_kind(valorDirectorio)
                if valorClaseTipo == 0:
                    SistemaOperativo.mkdir(valorDirectorio)
                    directorioCreado.append(valorDirectorio)
                elif valorClaseTipo != 2:
                    raise ValueError("valorDirectorio 경로에 파일이 있습니다: " + valorDirectorio)
            archivoCreado.append(ruta)
            escribirDiario(ruta, Datos)
        escribirDiario(rutaLista, listaNuevo)
    except Exception:
        for ruta in archivoCreado:
            if SistemaOperativo.path_kind(ruta):
                SistemaOperativo.remove(ruta)
        for valorDirectorio in reversed(directorioCreado):
            SistemaOperativo.rmdir(valorDirectorio)
        if listaElementoPrevio is not None:
            escribirDiario(rutaLista, listaElementoPrevio)
        elif SistemaOperativo.path_kind(rutaLista):
            SistemaOperativo.remove(rutaLista)
        raise
    print("instalarValor esTerminado:", nombre, especificación["version"], "→ /lib (RAM)")


def eliminarEntradaElemento(nombre):
    listaEntradaElemento = leerLista()
    if nombre not in listaEntradaElemento:
        raise ValueError("설치되지 않은 꾸러미입니다: " + nombre)
    for ruta, datosHuella in listaEntradaElemento[nombre]["files"].items():
        if SistemaOperativo.path_kind(ruta) != 1 or valorHuella(SistemaOperativo.read(ruta)) != datosHuella:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + ruta)
    for ruta in listaEntradaElemento[nombre]["files"]:
        SistemaOperativo.remove(ruta)
    del listaEntradaElemento[nombre]
    escribirDiario(rutaLista, json.dumps(listaEntradaElemento).encode())
    print("eliminarEntradaElemento esTerminado:", nombre)


def ponerEnMarcha(argumentos):
    númeroPuerto = 8027
    if len(argumentos) >= 2 and argumentos[-2] == "--port":
        númeroPuerto = int(argumentos[-1])
        argumentos = argumentos[:-2]
    if argumentos == ["list"]:
        for nombre, informaciónSistema in leerLista().items():
            print(nombre, informaciónSistema["version"])
    elif len(argumentos) == 2 and argumentos[0] == "install":
        instalarValor(argumentos[1], númeroPuerto)
    elif len(argumentos) == 2 and argumentos[0] == "uninstall":
        eliminarEntradaElemento(argumentos[1])
    elif not argumentos or argumentos in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython árbolFuente 설치기 (PyPA pip 전체가 아님)")
        print("pip install nombre[==버전] [--port 8027] | pip list | pip uninstall nombre")
        print("Anfitrión: Herramientas/ejecutarComando.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        ponerEnMarcha(sys.argv[1:])
    except Exception as error:
        print("Paquete error:", error)
        sys.exit(1)
