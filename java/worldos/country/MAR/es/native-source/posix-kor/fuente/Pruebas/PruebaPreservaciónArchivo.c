#include <ABIArchivo.h>
#include <stdio.h>
int main(int númeroElementosElementoLista, char **listaEntradaElemento) {
    (void)númeroElementosElementoLista; (void)listaEntradaElemento;
    int Archivo = abrirArchivo("stored.txt", EscribirLeer | AusenteSiCrear | ContenidoTruncar, 0600);
    if (Archivo < 0 || escribirDatosArchivo(Archivo, "saved-from-C", 12) != 12) return 1;
    if (almacenamientoArchivoConfirmar(Archivo) < 0) return 2;
    if (cerrarArchivo(Archivo) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
