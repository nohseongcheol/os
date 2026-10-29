#include "ABIArchivo.h"
class GestorDocumento {
    int número;
public:
    GestorDocumento(const char *nombre) : número(abrirArchivo(nombre, EscribirLeer | AusenteSiCrear | ContenidoTruncar, 0600)) {}
    ~GestorDocumento() { if (número >= 0) cerrarArchivo(número); }
    tipoResultadoEntradaSalida escribir(const char *Datos, tipoNúmeroElementosByte tamaño) { return escribirDatosArchivo(número, Datos, tamaño); }
};
extern "C" int iniciarProgramaUsuario(int argumentos) {
    (void)argumentos;
    const char saludo[] = "C++에서 한글 클래스와 posix-kor invocar\n";
    GestorDocumento Documentación("C++Saludo.txt");
    escribirDatosArchivo(1, saludo, sizeof(saludo) - 1);
    return Documentación.escribir(saludo, sizeof(saludo) - 1) == sizeof(saludo) - 1 ? 0 : 1;
}
