#include <ABIArchivo.h>
#include <stdio.h>
#include <string.h>
int main(int númeroElementosElementoLista, char **listaEntradaElemento) {
    (void)númeroElementosElementoLista; (void)listaEntradaElemento;
    char Datos[6]; int longitud = 0;
    puts("POSIX INPUT READY");
    while (longitud < 6) {
        int resultado = leerDatosArchivo(0, Datos + longitud, 6 - longitud);
        if (resultado <= 0) return 1;
        longitud += resultado;
    }
    if (memcmp(Datos, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
