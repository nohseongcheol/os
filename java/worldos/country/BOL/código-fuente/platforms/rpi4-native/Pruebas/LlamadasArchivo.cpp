#include "../denominación/nombresEnlazarMáquina.h"
#include "ABIArchivo.h"
// 표준 C++ biblioteca 없는 freestanding C++11 Programa. 커널에 valorEstático 링크한다.
extern "C" uintptr_t pruebaProgramasCpp(void) {
    const char valorContenidoValor[] = "C++ → Java valorNúcleo · 한글 😀";
    unsigned char leerValor[sizeof(valorContenidoValor)] = {};
    int Archivo = abrirArchivo("Pruebas.txt", EscribirLeer | AusenteSiCrear | ContenidoTruncar, 0600);
    if (Archivo < 0) return 1;
    if (escribirDatosArchivo(Archivo, valorContenidoValor, sizeof(valorContenidoValor)) != sizeof(valorContenidoValor)) return 2;
    if (posicionarArchivo(Archivo, 0, PrincipioDesde) != 0) return 3;
    if (leerDatosArchivo(Archivo, leerValor, sizeof(leerValor)) != sizeof(leerValor)) return 4;
    for (size_t índiceOrdinal = 0; índiceOrdinal < sizeof(valorContenidoValor); índiceOrdinal++) if (leerValor[índiceOrdinal] != (unsigned char)valorContenidoValor[índiceOrdinal]) return 5;
    if (leerDatosArchivo(Archivo, leerValor, 1) != 0) return 6;
    if (almacenamientoArchivoConfirmar(Archivo) != -1 || númeroError != 38) return 7;
    if (cerrarArchivo(Archivo) || cerrarArchivo(Archivo) != -1 || númeroError != 9) return 8;
    Archivo = abrirArchivo("Pruebas.txt", leerValorSolamente);
    if (Archivo < 0 || escribirDatosArchivo(Archivo, valorContenidoValor, 1) != -1 || númeroError != 9) return 9;
    if (cerrarArchivo(Archivo)) return 10;
    Archivo = abrirArchivo("Pruebas.txt", EscribirLeer | añadirFinalFinEnPosición);
    if (Archivo < 0 || posicionarArchivo(Archivo, 0, PrincipioDesde) != 0 || escribirDatosArchivo(Archivo, "!", 1) != 1 || tamañoArchivo(Archivo) != sizeof(valorContenidoValor) + 1) return 11;
    if (establecerLongitudArchivo(Archivo, 2) || posicionarArchivo(Archivo, 4, PrincipioDesde) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (escribirDatosArchivo(Archivo, "x", 1) != 1 || tamañoArchivo(Archivo) != 3 || cerrarArchivo(Archivo)) return 13;
    Archivo = abrirArchivo("구멍.bin", EscribirLeer | AusenteSiCrear | ContenidoTruncar, 0600);
    if (Archivo < 0 || posicionarArchivo(Archivo, 3, PrincipioDesde) != 3 || escribirDatosArchivo(Archivo, "z", 1) != 1) return 14;
    if (posicionarArchivo(Archivo, 0, PrincipioDesde) != 0 || leerDatosArchivo(Archivo, leerValor, 4) != 4 || leerValor[0] || leerValor[1] || leerValor[2] || leerValor[3] != 'z') return 15;
    if (eliminarNombreEntradaElementoArchivo("구멍.bin") || tamañoArchivo(Archivo) != 4 || cerrarArchivo(Archivo)) return 16;
    if (abrirArchivo("구멍.bin", leerValorSolamente) != -1 || númeroError != 2) return 17;
    if (abrirArchivo("Pruebas.txt", EscribirLeer | crearArchivoNuevo, 0600) != -1 || númeroError != 17) return 18;
    if (abrirArchivo("../valorVedado", leerValorSolamente) != -1) return 19;
    return 0;
}
