from español import ErrorSistema, ErrorOtraVezIntentar, abrirDatagrama, recibirDatagrama, cerrarRed, leerArchivo, Salida

extremo = abrirDatagrama(0)
try:
    try:
        recibirDatagrama(extremo)
        raise AssertionError("비어 있는 datagrama 대기에서 예외가 필요합니다.")
    except ErrorSistema as error:
        assert error.número == ErrorOtraVezIntentar
        assert error.descripción == "SistemaOperativo 작업에 실패했습니다."
        Salida("español datagrama excepción verificar")
finally:
    cerrarRed(extremo)
try:
    leerArchivo("/없는파일")
except ErrorSistema as error:
    assert error.número == 2
    Salida("español Archivo excepción verificar")
else:
    raise AssertionError("Archivo métodoAusente 예외가 필요합니다.")
