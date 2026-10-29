#include "ABIArchivo.h"
int iniciarProgramaUsuario(int argumentos) {
    (void)argumentos;
    const char saludo[] = "C에서 한글 이름과 posix-kor invocar\n";
    int Documentación = abrirArchivo("C인사.txt", EscribirLeer | AusenteSiCrear | ContenidoTruncar, 0600);
    if (Documentación < 0) return 1;
    tipoResultadoEntradaSalida númeroElementosRegistrado = escribirDatosArchivo(Documentación, saludo, sizeof(saludo) - 1);
    cerrarArchivo(Documentación);
    escribirDatosArchivo(1, saludo, sizeof(saludo) - 1);
    return númeroElementosRegistrado == sizeof(saludo) - 1 ? 0 : 2;
}
