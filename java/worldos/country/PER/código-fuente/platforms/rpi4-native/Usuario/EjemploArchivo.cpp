#include "ABIArchivo.h"
#include "invocar.h"
static int valorInicializador;
static volatile int semillaInicializador = 72;
static volatile double semillaPuntoFlotante = 1.25;
static int númeroElementosDestrucción;
struct pruebaInicialización { pruebaInicialización() { valorInicializador = semillaInicializador + 1; } } inicializarZonaEstática;
class archivoAutomático {
    int número;
public:
    explicit archivoAutomático(const char *nombre) : número(abrirArchivo(nombre, EscribirLeer | AusenteSiCrear | ContenidoTruncar, 0600)) {}
    ~archivoAutomático() { if (número >= 0) cerrarArchivo(número); númeroElementosDestrucción++; }
    int entradaElementoDescriptor() const { return número; }
};
extern "C" int iniciarProgramaUsuario(int) {
    if (valorInicializador != 73 || invocarUsuario(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double valorPuntoFlotante = semillaPuntoFlotante * 2.0 + 0.5;
    if (invocarUsuario(0, 0, 0, 0, 0, 0, 0) != 1 || valorPuntoFlotante != 3.0) return 16;
    static const char valorContenidoValor[] = "EL0 C++ → posix-kor → Java Archivo · 안녕하세요 😀\n";
    char leerValor[sizeof(valorContenidoValor)] = {};
    {
        archivoAutomático Archivo("Usuario.txt");
        int número = Archivo.entradaElementoDescriptor();
        if (número < 0 || escribirDatosArchivo(número, valorContenidoValor, sizeof(valorContenidoValor)) != sizeof(valorContenidoValor)) return 2;
        if (posicionarArchivo(número, 0, PrincipioDesde) || leerDatosArchivo(número, leerValor, sizeof(leerValor)) != sizeof(leerValor)) return 3;
        for (unsigned índiceOrdinal = 0; índiceOrdinal < sizeof(valorContenidoValor); índiceOrdinal++) if (leerValor[índiceOrdinal] != valorContenidoValor[índiceOrdinal]) return 4;
    }
    if (númeroElementosDestrucción != 1) return 5;
    if (escribirDatosArchivo(1, valorContenidoValor, sizeof(valorContenidoValor) - 1) != sizeof(valorContenidoValor) - 1) return 6;
    uintptr_t entradaElementoExtremoInferior = finMemoriaUsuario(0);
    if (entradaElementoExtremoInferior != 0x02c00000 || finMemoriaUsuario(entradaElementoExtremoInferior + 8192) != (intptr_t)(entradaElementoExtremoInferior + 8192)) return 7;
    volatile unsigned char *Memoria = (volatile unsigned char *)entradaElementoExtremoInferior;
    if (Memoria[0] || Memoria[8191]) return 8;
    Memoria[8191] = 137;
    if (finMemoriaUsuario(entradaElementoExtremoInferior) != (intptr_t)entradaElementoExtremoInferior || finMemoriaUsuario(entradaElementoExtremoInferior + 8192) != (intptr_t)(entradaElementoExtremoInferior + 8192) || Memoria[8191]) return 9;
    // 잘못된 Usuario puntero/번호는 오류이며 커널을 중단하지 않는다.
    if (escribirDatosArchivo(1, (const void *)0x80000, 8) != -1 || númeroError != 14) return 10;
    if (leerDatosArchivo(0, (void *)valorContenidoValor, 1) != -1 || númeroError != 14) return 11;
    if (invocarUsuario(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t extensiónRangoPantalla = leerAnchuraPantalla(), longitudPantalla = leerAlturaPantalla();
    if (extensiónRangoPantalla <= 0 || longitudPantalla <= 0 || invocarUsuario(13, extensiónRangoPantalla-1, longitudPantalla-1, 0, 2, 2, 0) != -22) return 13;
    if (rectánguloPantalla(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 programaSalir 시 열린 서술자가 자동 정리되어야 한다.
    if (abrirArchivo("Usuario.txt", leerValorSolamente) < 0) return 15;
    return 0;
}
