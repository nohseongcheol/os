#include "ABIRed.h"

int iniciarProgramaUsuario(int argumentos) {
    (void)argumentos;
    struct DirecciónConectorRedInternet dirección = {0};
    dirección.familiaDirección = FamiliaInternet;
    dirección.númeroPuerto = cortoRed(9260);
    dirección.DirecciónInternet.valorDirección = enteroValorRed(direcciónBucleRetorno);
    int valorServidor = crearExtremo(FamiliaInternet, RedFlujo, protocoloTransporteFlujo);
    if (valorServidor < 0 || asociarDirección(valorServidor, (struct DirecciónConectorRed *)&dirección, sizeof(dirección)) < 0 ||
        esperarConexiónRedPara(valorServidor, 4) < 0) return 1;
    if (aceptarConexiónRed(valorServidor, 0, 0) != -1 || númeroError != 11) return 2;
    int valorInvitado = crearExtremo(FamiliaInternet, RedFlujo, protocoloTransporteFlujo);
    if (valorInvitado < 0 || conectarRed(valorInvitado, (struct DirecciónConectorRed *)&dirección, sizeof(dirección)) < 0) return 3;
    int conectar = aceptarConexiónRed(valorServidor, 0, 0);
    if (conectar < 0) return 4;
    unsigned char enviarHaciaElementoLista[1500], elementoListaRecibido[1500];
    for (int númeroValor = 0; númeroValor < 1500; númeroValor++) enviarHaciaElementoLista[númeroValor] = (unsigned char)númeroValor;
    int númeroElementosEnviado = 0;
    while (númeroElementosEnviado < 1024) {
        int longitud = escribirDatosArchivo(valorInvitado, enviarHaciaElementoLista + númeroElementosEnviado, sizeof(enviarHaciaElementoLista) - númeroElementosEnviado);
        if (longitud <= 0) return 5;
        númeroElementosEnviado += longitud;
    }
    if (escribirDatosArchivo(valorInvitado, enviarHaciaElementoLista, 1) != -1 || númeroError != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 construirTodos 읽은 valorLadoPosterior EOF가 된다. */
    cerrarArchivo(valorInvitado);
    int númeroElementosRecibido = 0;
    while (númeroElementosRecibido < númeroElementosEnviado) {
        int longitud = leerDatosArchivo(conectar, elementoListaRecibido + númeroElementosRecibido, sizeof(elementoListaRecibido) - númeroElementosRecibido);
        if (longitud <= 0) return 7;
        númeroElementosRecibido += longitud;
    }
    for (int númeroValor = 0; númeroValor < númeroElementosRecibido; númeroValor++) if (elementoListaRecibido[númeroValor] != enviarHaciaElementoLista[númeroValor]) return 8;
    if (leerDatosArchivo(conectar, elementoListaRecibido, 1) != 0) return 9;
    if (escribirDatosArchivo(conectar, enviarHaciaElementoLista, 1) != -1 || númeroError != 32) return 10;
    cerrarArchivo(conectar); cerrarArchivo(valorServidor);
    const char resultado[] = "C posix-kor 연결형 Comunicación PASS\n";
    escribirDatosArchivo(1, resultado, sizeof(resultado) - 1);
    return 0;
}
