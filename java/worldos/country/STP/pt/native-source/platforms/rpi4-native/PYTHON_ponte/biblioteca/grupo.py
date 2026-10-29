"""nativo 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 host 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as SO

Lista_caminho = "/lib/.pip.json"


def impressão_digital_VALOR(dados):
    return "".join("%02x" % VALOR for VALOR in hashlib.sha256(dados).digest())


def leitura_Lista():
    if SO.path_kind(Lista_caminho) == 0:
        return {}
    return json.loads(SO.read(Lista_caminho).decode("utf-8"))


def gravar_LOG(caminho, dados):
    if SO.write(caminho, dados) != len(dados):
        raise OSError(28)


def cheque_caminho(caminho):
    if not isinstance(caminho, str) or not caminho.endswith(".py"):
        raise ValueError("Python 소스만 설치할 número 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in caminho.split("/")):
        raise ValueError("허용하지 않는 grupo caminho")
    if "\\" in caminho or any(ord(caractere_VALOR) < 32 or ord(caractere_VALOR) == 127 for caractere_VALOR in caminho):
        raise ValueError("잘못된 caminho 문자")
    resultado = "/lib/" + caminho
    if len(resultado.encode("utf-8")) > 63 or caminho in ("Português.py", "grupo.py"):
        raise ValueError("grupo 경로가 너무 길거나 valor_padrão 라이브러리와 겹칩니다.")
    return resultado


class receber_fluxo:
    def __init__(자신, empresa):
        자신.empresa = empresa
        자신.남은자료 = b""
        자신.iniciar = SO.ticks_ms()

    def 정확히읽기(자신, duração_VALOR):
        dados = bytearray()
        while len(dados) < duração_VALOR:
            if SO.ticks_ms() - 자신.iniciar > 90000:
                raise ValueError("grupo relé_VALOR resposta valor_temporal 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = SO.tcp_read(자신.empresa, 512)
                except OSError as erro:
                    if erro.args[0] != 11:
                        raise
                    SO.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("grupo 전송이 중간에 끝났습니다.")
            item_CONT_NÚM = min(duração_VALOR - len(dados), len(자신.남은자료))
            dados.extend(자신.남은자료[:item_CONT_NÚM])
            자신.남은자료 = 자신.남은자료[item_CONT_NÚM:]
            SO.sleep_ms(0)
        return bytes(dados)


def baixar(solicitação, número_da_porta):
    if len(solicitação) > 96 or any(caractere_VALOR not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for caractere_VALOR in solicitação):
        raise ValueError("사용법: pip install Nome 또는 Nome==버전")
    empresa = SO.tcp_open()
    try:
        iniciar = SO.ticks_ms()
        while True:
            try:
                SO.tcp_connect(empresa, "10.0.2.2", número_da_porta)
                break
            except OSError as erro:
                if erro.args[0] not in (11, 115) or SO.ticks_ms() - iniciar > 5000:
                    raise ValueError("grupo relé_VALOR Ligar falha_VALOR: 호스트에서 --network --pip로 실행하십시오.")
                SO.sleep_ms(10)
        dados = (solicitação + "\n").encode()
        while dados:
            try:
                item_CONT_NÚM = SO.tcp_write(empresa, dados)
                if not item_CONT_NÚM:
                    raise ValueError("grupo solicitação Transferir_VALOR falha_VALOR")
                dados = dados[item_CONT_NÚM:]
            except OSError as erro:
                if erro.args[0] != 11:
                    raise
                SO.sleep_ms(10)
                if SO.ticks_ms() - iniciar > 10000:
                    raise ValueError("grupo solicitação Transferir_VALOR valor_temporal 초과")
        fluxo_VALOR = receber_fluxo(empresa)
        HEAD_VALOR = fluxo_VALOR.정확히읽기(8)
        if HEAD_VALOR[:4] != b"JKP1":
            raise ValueError("grupo Transferir_VALOR valor_do_contrato 불일치")
        duração_VALOR = (HEAD_VALOR[4] << 24) | (HEAD_VALOR[5] << 16) | (HEAD_VALOR[6] << 8) | HEAD_VALOR[7]
        if duração_VALOR > 8192:
            raise ValueError("grupo 명세가 너무 큽니다.")
        especificação = json.loads(fluxo_VALOR.정확히읽기(duração_VALOR).decode())
        if "error" in especificação:
            raise ValueError(especificação["error"])
        if not 1 <= len(especificação["files"]) <= 16:
            raise ValueError("꾸러미당 fonte_árvore 파일은 1~16개여야 합니다.")
        if sum(entrada_VALOR_962f286b["size"] for entrada_VALOR_962f286b in especificação["files"]) > 65536:
            raise ValueError("grupo fonte_árvore 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for entrada_VALOR_962f286b in especificação["files"]:
            caminho = cheque_caminho(entrada_VALOR_962f286b["path"])
            if caminho in 파일들 or not 0 <= entrada_VALOR_962f286b["size"] <= 16384:
                raise ValueError("중복 caminho 또는 ficheiro Tamanho 초과")
            dados = fluxo_VALOR.정확히읽기(entrada_VALOR_962f286b["size"])
            if impressão_digital_VALOR(dados) != entrada_VALOR_962f286b["sha256"]:
                raise ValueError("grupo ficheiro SHA-256 불일치")
            # 실행하지 않고 em_dia_item MicroPython의 문법으로 먼저 검사한다.
            compile(dados.decode("utf-8"), caminho, "exec")
            파일들[caminho] = dados
            gc.collect()
        return especificação, 파일들
    finally:
        SO.udp_close(empresa)


def instalar_VALOR(solicitação, número_da_porta):
    print("grupo baixar:", solicitação)
    especificação, 파일들 = baixar(solicitação, número_da_porta)
    entrada_Lista_f07b3200 = leitura_Lista()
    Nome = especificação["name"]
    if Nome in entrada_Lista_f07b3200:
        if entrada_Lista_f07b3200[Nome]["version"] == especificação["version"]:
            for caminho, impressão_digital_dados in entrada_Lista_f07b3200[Nome]["files"].items():
                if SO.path_kind(caminho) != 1 or impressão_digital_VALOR(SO.read(caminho)) != impressão_digital_dados:
                    raise ValueError("설치된 grupo 파일이 달라졌습니다: " + caminho)
            print("이미 설치됨:", Nome, especificação["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 BACK_VALOR 설치하십시오.")
    for caminho in 파일들:
        if SO.path_kind(caminho):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + caminho)
    entrada_Lista_f07b3200[Nome] = {"version": especificação["version"], "files": {caminho: impressão_digital_VALOR(dados) for caminho, dados in 파일들.items()}}
    새목록 = json.dumps(entrada_Lista_f07b3200).encode()
    if len(새목록) > 16384:
        raise ValueError("grupo entrada_Lista_f07b3200 Tamanho 초과")
    Anterior_Lista = SO.read(Lista_caminho) if SO.path_kind(Lista_caminho) else None
    만든파일 = []
    만든폴더 = []
    try:
        for caminho, dados in 파일들.items():
            부분들 = caminho.split("/")
            for número in range(2, len(부분들)):
                Diretório_VALOR = "/".join(부분들[:número])
                Tipo_VALOR = SO.path_kind(Diretório_VALOR)
                if Tipo_VALOR == 0:
                    SO.mkdir(Diretório_VALOR)
                    만든폴더.append(Diretório_VALOR)
                elif Tipo_VALOR != 2:
                    raise ValueError("Diretório_VALOR 경로에 파일이 있습니다: " + Diretório_VALOR)
            만든파일.append(caminho)
            gravar_LOG(caminho, dados)
        gravar_LOG(Lista_caminho, 새목록)
    except Exception:
        for caminho in 만든파일:
            if SO.path_kind(caminho):
                SO.remove(caminho)
        for Diretório_VALOR in reversed(만든폴더):
            SO.rmdir(Diretório_VALOR)
        if Anterior_Lista is not None:
            gravar_LOG(Lista_caminho, Anterior_Lista)
        elif SO.path_kind(Lista_caminho):
            SO.remove(Lista_caminho)
        raise
    print("instalar_VALOR 완료:", Nome, especificação["version"], "→ /lib (RAM)")


def remover_entrada(Nome):
    entrada_Lista_f07b3200 = leitura_Lista()
    if Nome not in entrada_Lista_f07b3200:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Nome)
    for caminho, impressão_digital_dados in entrada_Lista_f07b3200[Nome]["files"].items():
        if SO.path_kind(caminho) != 1 or impressão_digital_VALOR(SO.read(caminho)) != impressão_digital_dados:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + caminho)
    for caminho in entrada_Lista_f07b3200[Nome]["files"]:
        SO.remove(caminho)
    del entrada_Lista_f07b3200[Nome]
    gravar_LOG(Lista_caminho, json.dumps(entrada_Lista_f07b3200).encode())
    print("remover_entrada 완료:", Nome)


def iniciar(argumentos):
    número_da_porta = 8027
    if len(argumentos) >= 2 and argumentos[-2] == "--port":
        número_da_porta = int(argumentos[-1])
        argumentos = argumentos[:-2]
    if argumentos == ["list"]:
        for Nome, msinfo32_exe in leitura_Lista().items():
            print(Nome, msinfo32_exe["version"])
    elif len(argumentos) == 2 and argumentos[0] == "install":
        instalar_VALOR(argumentos[1], número_da_porta)
    elif len(argumentos) == 2 and argumentos[0] == "uninstall":
        remover_entrada(argumentos[1])
    elif not argumentos or argumentos in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython fonte_árvore 설치기 (PyPA pip 전체가 아님)")
        print("pip install Nome[==버전] [--port 8027] | pip list | pip uninstall Nome")
        print("host: ferramentas/Executar_comando.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        iniciar(sys.argv[1:])
    except Exception as erro:
        print("grupo erro:", erro)
        sys.exit(1)
