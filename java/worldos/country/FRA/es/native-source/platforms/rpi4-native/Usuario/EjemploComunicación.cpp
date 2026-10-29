#include "ABIRed.h"
static DirecciónConectorRedInternet dirección(unsigned valorPuerto) {
    DirecciónConectorRedInternet valor = {}; valor.familiaDirección = FamiliaInternet;
    valor.númeroPuerto = cortoRed(valorPuerto); valor.DirecciónInternet.valorDirección = enteroValorRed(direcciónBucleRetorno); return valor;
}
extern "C" int iniciarProgramaUsuario(int) {
    int extremoEnvíoEnCurso = crearExtremo(FamiliaInternet, ConectorRedDatagrama, 0);
    int extremoReceptor = crearExtremo(FamiliaInternet, ConectorRedDatagrama, ProtocoloDatagrama);
    if (extremoEnvíoEnCurso < 0 || extremoReceptor < 0) return 1;
    DirecciónConectorRedInternet valorLlegada = dirección(7777), valorPartida = dirección(7778), direcciónEnviado = {};
    tipoLongitudDirecciónConectorRed longitudDirección = sizeof(direcciónEnviado);
    if (asociarDirección(extremoReceptor, (DirecciónConectorRed *)&valorLlegada, sizeof(valorLlegada))) return 2;
    if (asociarDirección(extremoEnvíoEnCurso, (DirecciónConectorRed *)&valorLlegada, sizeof(valorLlegada)) != -1 || númeroError != 98) return 3;
    if (asociarDirección(extremoEnvíoEnCurso, (DirecciónConectorRed *)&valorPartida, sizeof(valorPartida))) return 4;
    static const char valorContenidoValor[] = "한글 UDP loopback 😀";
    char valorRecibido[64] = {};
    if (enviarDatosDatagrama(extremoEnvíoEnCurso, valorContenidoValor, sizeof(valorContenidoValor), 0, (DirecciónConectorRed *)&valorLlegada, sizeof(valorLlegada)) != sizeof(valorContenidoValor)) return 5;
    if (recibirDatosDatagrama(extremoReceptor, (void *)valorContenidoValor, sizeof(valorContenidoValor), 0, 0, 0) != -1 || númeroError != 14) return 6;
    if (recibirDatosDatagrama(extremoReceptor, valorRecibido, sizeof(valorRecibido), 0, (DirecciónConectorRed *)&direcciónEnviado, &longitudDirección) != sizeof(valorContenidoValor)) return 7;
    if (longitudDirección != sizeof(direcciónEnviado) || cortoOrdenDispositivo(direcciónEnviado.númeroPuerto) != 7778 || enteroValorOrdenDispositivo(direcciónEnviado.DirecciónInternet.valorDirección) != direcciónBucleRetorno) return 8;
    for (unsigned índiceOrdinal = 0; índiceOrdinal < sizeof(valorContenidoValor); índiceOrdinal++) if (valorRecibido[índiceOrdinal] != valorContenidoValor[índiceOrdinal]) return 9;
    if (recibirDatosDatagrama(extremoReceptor, valorRecibido, sizeof(valorRecibido), 0, 0, 0) != -1 || númeroError != 11) return 10;
    if (enviarDatosDatagrama(extremoReceptor, valorRecibido, sizeof(valorContenidoValor), 0, (DirecciónConectorRed *)&direcciónEnviado, sizeof(direcciónEnviado)) != sizeof(valorContenidoValor)) return 11;
    if (recibirDatosDatagrama(extremoEnvíoEnCurso, valorRecibido, 4, 0, 0, 0) != 4) return 12;
    if (recibirDatosDatagrama(extremoEnvíoEnCurso, valorRecibido, 4, 0, 0, 0) != -1 || númeroError != 11) return 13;
    for (int índiceOrdinal = 0; índiceOrdinal < 4; índiceOrdinal++) if (enviarDatosDatagrama(extremoEnvíoEnCurso, valorContenidoValor, sizeof(valorContenidoValor), 0, (DirecciónConectorRed *)&valorLlegada, sizeof(valorLlegada)) != sizeof(valorContenidoValor)) return 14;
    if (enviarDatosDatagrama(extremoEnvíoEnCurso, valorContenidoValor, sizeof(valorContenidoValor), 0, (DirecciónConectorRed *)&valorLlegada, sizeof(valorLlegada)) != -1 || númeroError != 11) return 15;
    for (int índiceOrdinal = 0; índiceOrdinal < 4; índiceOrdinal++) if (recibirDatosDatagrama(extremoReceptor, valorRecibido, sizeof(valorRecibido), 0, 0, 0) != sizeof(valorContenidoValor)) return 16;
    if (enviarDatosDatagrama(extremoEnvíoEnCurso, 0, 0, 0, (DirecciónConectorRed *)&valorLlegada, sizeof(valorLlegada)) != 0 ||
        recibirDatosDatagrama(extremoReceptor, 0, 0, 0, 0, 0) != 0) return 21;
    valorLlegada.DirecciónInternet.valorDirección = enteroValorRed(0x08080808);
    if (enviarDatosDatagrama(extremoEnvíoEnCurso, valorContenidoValor, sizeof(valorContenidoValor), 0, (DirecciónConectorRed *)&valorLlegada, sizeof(valorLlegada)) != -1 || númeroError != 101) return 17;
    if (crearExtremo(FamiliaInternet, RedFlujo, ProtocoloDatagrama) != -1 || númeroError != 93) return 18;
    longitudDirección = sizeof(direcciónEnviado);
    if (leerDirecciónConectorRed(extremoReceptor, (DirecciónConectorRed *)&direcciónEnviado, &longitudDirección) || cortoOrdenDispositivo(direcciónEnviado.númeroPuerto) != 7777) return 19;
    if (cerrarArchivo(extremoReceptor) || cerrarArchivo(extremoReceptor) != -1 || númeroError != 9) return 20;
    // 보내는곳은 열어 둔다: programaSalir 시 프로세스별 socket 정리를 검사한다.
    static const char esTerminado[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    escribirDatosArchivo(1, esTerminado, sizeof(esTerminado) - 1);
    return 0;
}
