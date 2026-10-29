#include <ABIArchivo.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int númeroElementosArgumentos, char **listaArgumento) {
    if (númeroElementosArgumentos < 1 || !listaArgumento[0]) return 2;
    const char saludo[] = "propio 커널의 C와 español POSIX\n";
    int Documentación = abrirArchivo("Saludo.txt", EscribirLeer | AusenteSiCrear | ContenidoTruncar, 0600);
    if (Documentación < 0) return 1;
    tipoResultadoEntradaSalida longitud = escribirDatosArchivo(Documentación, saludo, sizeof(saludo) - 1);
    cerrarArchivo(Documentación);
    escribirDatosArchivo(1, saludo, sizeof(saludo) - 1);
    return longitud == sizeof(saludo) - 1 ? 0 : 3;
}
