#include "../denominación/nombresEnlazarMáquina.h"
#include "informaciónPantalla.h"
// EL0 ejecutarComando máquina valorCapa. Archivo Datos/정책은 기존 AOT Java 커널에 위임한다.
#include "Usuario.h"
#include "ABIArchivo.h"
#include "ABIRed.h"
#include "../PilaRed/PilaRed.h"
extern int32_t remotoRedJava(int32_t), direcciónFlujoJava(int32_t);
#define registroMáquina(valorPrimero) (*(volatile uint32_t *)(uintptr_t)(valorPrimero))
#define distribuidorInterrumpir 0xff841000ul
#define interfazCPUInterrumpir 0xff842000ul
#define tamañoPágina 4096ul
#define marcadorAcceso (1ul << 10)
#define permisoEjecutarNinguno (1ul << 53)
#define ejecutarNingunoUsuario (1ul << 54)
#define memoriaNormal ((1ul << 2) | (3ul << 8) | marcadorAcceso)
#define páginaNúcleo (3ul | memoriaNormal | permisoEjecutarNinguno | ejecutarNingunoUsuario)
#define escribirLeerUsuario (3ul | memoriaNormal | (1ul << 6) | permisoEjecutarNinguno | ejecutarNingunoUsuario)
#define solamenteLeerUsuario (3ul | memoriaNormal | (3ul << 6) | permisoEjecutarNinguno | ejecutarNingunoUsuario)
#define ejecutarLeerUsuario (3ul | memoriaNormal | (3ul << 6) | permisoEjecutarNinguno)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t escribirCarácterPlaca(uintptr_t), obtenerCarácterPlaca(void), milisegundosTranscurridosPlaca(void);
extern uintptr_t píxelPlaca(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t búferImagenPlaca(void);
extern uintptr_t terminalPlaca(uintptr_t);
extern int pendienteTerminal(void);
extern int32_t interactivoConsolaJava(void);
extern int32_t iniciarRutaJava(int32_t), byteRutaJava(int32_t,int32_t);
extern int32_t directorioCrearJava(void), directorioEliminarJava(void), claseTipoEntradaElementoJava(void);
extern int invocarPantalla(int,unsigned,int,int,int,int,int),textoPantalla(int,int,const uint32_t *,unsigned);
extern void inicializarPantalla(int),pulsarPantalla(int,unsigned);
extern int reanudarUsuario(marcoUsuario *,void *);
extern void guardarComaFlotanteUsuario(void *);
extern int entrarUsuario(uintptr_t puntoEntradaElemento, uintptr_t almacenamientoPila, uintptr_t valorReenviado);
extern void retornarUsuario(void);
extern void paradaFatalNúcleo(const char *) __attribute__((noreturn));
static uint64_t direcciónRaíz[512] __attribute__((aligned(4096)));
static uint64_t medio[4][512] __attribute__((aligned(4096)));
static uint64_t listaPágina[númeroElementosPáginaUsuario] __attribute__((aligned(4096)));
static uint8_t listaPermisos[númeroElementosPáginaUsuario];
static int activo, listaArchivo[16], aBILinux;
static unsigned extremosConectorRed[24];
extern int32_t conectorRedRedJava(int32_t, int32_t, int32_t), asociarRedJava(int32_t, int32_t, int32_t);
extern int32_t ponerRedJava(int32_t, int32_t), obtenerRedJava(int32_t), enviarRedJava(int32_t, int32_t, int32_t, int32_t);
extern int32_t operaciónRecepciónRedJava(int32_t, int32_t), puertoRedJava(int32_t), direcciónRedJava(int32_t), parRedRedJava(int32_t), cerrarRedJava(int32_t);
extern int32_t crearFlujoJava(void),asociarFlujoJava(int32_t,int32_t,int32_t),escucharFlujoJava(int32_t,int32_t),conectarFlujoJava(int32_t,int32_t,int32_t),aceptarFlujoJava(int32_t),leerFlujoJava(int32_t,int32_t),escribirFlujoJava(int32_t,int32_t),puertoFlujoJava(int32_t),parRedFlujoJava(int32_t),cerrarFlujoJava(int32_t);
static int cerrarExtremoConectorRed(unsigned manejadorArchivo){return manejadorArchivo<40?cerrarRedJava(manejadorArchivo):cerrarFlujoJava(manejadorArchivo);}
static uint64_t frecuencia, tiempoPlazo;
static uintptr_t finMontículo;
// valorNúcleo 셸이 준비한 UTF-8 argumentos. EL0에는 copiarValor 호출만 제공한다.
static unsigned númeroElementosArgumentoReenviado, longitudArgumentoReenviado[8];
static unsigned char argumentoReenviado[8][256];
typedef struct {
    int estadoValorEnPausa,interactivo,aBILinux,listaArchivo[16]; unsigned extremosConectorRed[24],númeroElementosArgumentos,longitudArgumento[8];
    unsigned char arregloArgumento[8][256],listaPermisos[númeroElementosPáginaUsuario];
    uintptr_t almacenamientoMontículo; marcoUsuario marcoEjecución;
    unsigned char estadoValorPuntoFlotante[528] __attribute__((aligned(16)));
} procesoGuardado;
static procesoGuardado guardado[4];
static int objetoPropietario,interactivo;
static uint32_t númeroUsuario[4], tiempoIniciarUsuario[4], tiempoAcumuladoUsuario[4], tiempoEjecuciónUsuario[4], númeroUsuarioSiguiente=10;
static unsigned char nombreComandoUsuario[4][288];
uint32_t leerEstadoValorUsuario(unsigned valorEntradaElemento, unsigned número) {
    unsigned índicePosición=número&3;
    int valorEstadoValor=(activo && objetoPropietario==(int)índicePosición) ? 1 : guardado[índicePosición].estadoValorEnPausa ? 2 : 0;
    if (valorEntradaElemento==0) return valorEstadoValor;
    if (!valorEstadoValor) return 0;
    if (valorEntradaElemento==1) return númeroUsuario[índicePosición];
    if (valorEntradaElemento==2) {
        unsigned char *listaPáginas=valorEstadoValor==1?listaPermisos:guardado[índicePosición].listaPermisos;
        unsigned númeroElementosPágina=0; for (unsigned índiceOrdinal=0; índiceOrdinal<númeroElementosPáginaUsuario; índiceOrdinal++) if(listaPáginas[índiceOrdinal]) númeroElementosPágina++;
        return númeroElementosPágina*4;
    }
    if (valorEntradaElemento==3) return (uint32_t)milisegundosTranscurridosPlaca()-tiempoIniciarUsuario[índicePosición];
    if (valorEntradaElemento==4) return tiempoAcumuladoUsuario[índicePosición]+(valorEstadoValor==1?(uint32_t)milisegundosTranscurridosPlaca()-tiempoEjecuciónUsuario[índicePosición]:0);
    if (valorEntradaElemento==5) return número/4<sizeof(nombreComandoUsuario[0])?nombreComandoUsuario[índicePosición][número/4]:0;
    return 0;
}
uintptr_t inicioPosiciónArgumentosLlamadaPlaca(uintptr_t númeroElementosEntradaElemento) {
    if (activo || númeroElementosEntradaElemento > 8) return (uint32_t)-22;
    númeroElementosArgumentoReenviado = númeroElementosEntradaElemento;
    memset(longitudArgumentoReenviado, 0, sizeof(longitudArgumentoReenviado));
    memset(argumentoReenviado, 0, sizeof(argumentoReenviado));
    return 0;
}
uintptr_t byteArgumentosLlamadaPlaca(uintptr_t índiceBuscar, uintptr_t posiciónActual, uintptr_t datosByte) {
    if (activo || índiceBuscar >= númeroElementosArgumentoReenviado || posiciónActual >= 255 || posiciónActual != longitudArgumentoReenviado[índiceBuscar] || !datosByte || datosByte > 255)
        return (uint32_t)-22;
    argumentoReenviado[índiceBuscar][posiciónActual] = datosByte;
    longitudArgumentoReenviado[índiceBuscar] = posiciónActual + 1;
    return 0;
}
static void tablasSincronizarDatos(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t valorReloj(void) { uint64_t datosTemporal; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(datosTemporal)); return datosTemporal; }
static void detenerTiempoEspera(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    registroMáquina(distribuidorInterrumpir + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void iniciarTiempoEspera(void) {
    uint64_t valorEspaciado = frecuencia * 2, activar = 1;
    tiempoPlazo = valorReloj() + valorEspaciado;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(valorEspaciado), "r"(activar) : "memory");
}
void operaciónInicializaciónSistemaUsuario(void) {
    for (unsigned bloqueDatos = 0; bloqueDatos < 4; bloqueDatos++) {
        direcciónRaíz[bloqueDatos] = (uintptr_t)medio[bloqueDatos] | 3;
        for (unsigned índiceOrdinal = 0; índiceOrdinal < 512; índiceOrdinal++) {
            uintptr_t dirección = ((uintptr_t)bloqueDatos << 30) | ((uintptr_t)índiceOrdinal << 21);
            medio[bloqueDatos][índiceOrdinal] = dirección | 1 | marcadorAcceso | ejecutarNingunoUsuario;
            if (dirección >= 0xfc000000ul) medio[bloqueDatos][índiceOrdinal] |= permisoEjecutarNinguno; // Device-nGnRnE
            else medio[bloqueDatos][índiceOrdinal] |= memoriaNormal; // Normal, non-cacheable
        }
    }
    for (unsigned valorSegundo = 0; valorSegundo < númeroElementosPáginaUsuario / 512; valorSegundo++)
        medio[0][(baseUsuario >> 21) + valorSegundo] = (uintptr_t)(listaPágina + valorSegundo * 512) | 3;
    for (unsigned índiceOrdinal = 0; índiceOrdinal < númeroElementosPáginaUsuario; índiceOrdinal++) listaPágina[índiceOrdinal] = (baseUsuario + índiceOrdinal * tamañoPágina) | páginaNúcleo;
    uint64_t registroAtributoMemoria = 0x4400, controlTraducciónDirección = 32 | (3ul << 12) | (1ul << 23), registroControlSistema;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(registroAtributoMemoria), "r"(controlTraducciónDirección), "r"((uintptr_t)direcciónRaíz) : "memory");
    tablasSincronizarDatos();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(registroControlSistema));
    registroControlSistema = (registroControlSistema & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(registroControlSistema) : "memory");
    uint64_t estadoValorPuntoFlotante = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(estadoValorPuntoFlotante) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(frecuencia));
    detenerTiempoEspera();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 valorPuntoEntradaElemento 때만 permitirValor.
    registroMáquina(distribuidorInterrumpir) = 0;
    registroMáquina(distribuidorInterrumpir + 0x180) = 0xffffffff;
    registroMáquina(distribuidorInterrumpir + 0x80) = 0xffffffff;
    registroMáquina(distribuidorInterrumpir + 0x280) = 1u << 30;
    registroMáquina(distribuidorInterrumpir + 0x41c) = 0x80808080;
    registroMáquina(distribuidorInterrumpir + 0x100) = 1u << 30;
    registroMáquina(interfazCPUInterrumpir + 4) = 0xff;
    registroMáquina(interfazCPUInterrumpir + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 esNormal 확인할 númeroValor 있다.
    int seguridad = (registroMáquina(distribuidorInterrumpir + 4) & (1u << 10)) != 0;
    registroMáquina(distribuidorInterrumpir) = seguridad ? 1 : 3;
    registroMáquina(interfazCPUInterrumpir) = seguridad ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char identificador[16]; uint16_t categoríaTipo, tipoMáquina; uint32_t númeroVersión;
    uint64_t puntoEntradaElemento, desfaseEncabezadoPrograma, desfaseEncabezadoSección; uint32_t bitsConfiguración;
    uint16_t tamañoEncabezadoCódigoEjecutable, tamañoEntradaElementoEncabezadoPrograma, númeroElementosEncabezadoPrograma, tamañoEntradaElementoEncabezadoSección, númeroElementosEncabezadoSección, índiceTablaNombreSección;
} encabezadoELF;
typedef struct { uint32_t categoríaTipo, bitsConfiguración; uint64_t valorDesfase, dirección, direcciónFísico, tamañoZonaArchivo, tamañoZonaMemoria, fronteraAlinear; } programaELF;
_Static_assert(sizeof(encabezadoELF) == 64 && sizeof(programaELF) == 56, "ELF layout");
_Static_assert(sizeof(marcoUsuario) == 272, "exception assembly layout");
static int contenido(uint64_t valorDesfase, uint64_t tamaño, uint64_t desfaseFin) {
    return valorDesfase <= desfaseFin && tamaño <= desfaseFin - valorDesfase;
}
static int comprobarInformaciónAuxiliar(const unsigned char *posiciónDatos, size_t tamaño) {
    size_t posiciónActual = 0;
    while (contenido(posiciónActual, 12, tamaño)) {
        uint32_t palabrasLéxico[3]; memcpy(palabrasLéxico, posiciónDatos + posiciónActual, 12); posiciónActual += 12;
        uint64_t tamañoZonaNombre = ((uint64_t)palabrasLéxico[0] + 3) & ~3ul;
        uint64_t tamañoDescripción = ((uint64_t)palabrasLéxico[1] + 3) & ~3ul;
        if (!contenido(posiciónActual, tamañoZonaNombre, tamaño) || !contenido(posiciónActual + tamañoZonaNombre, tamañoDescripción, tamaño)) return 0;
        const unsigned char nombre[] = {'J','K','O','R','O','S',0};
        int esIgual = palabrasLéxico[0] == sizeof(nombre) && palabrasLéxico[1] == 4 && palabrasLéxico[2] == 1;
        if (esIgual) for (unsigned índiceOrdinal = 0; índiceOrdinal < sizeof(nombre); índiceOrdinal++) if (posiciónDatos[posiciónActual + índiceOrdinal] != nombre[índiceOrdinal]) esIgual = 0;
        uint32_t númeroVersión = 0;
        if (esIgual) memcpy(&númeroVersión, posiciónDatos + posiciónActual + tamañoZonaNombre, 4);
        if (esIgual && númeroVersión == 1) return 1;
        posiciónActual += tamañoZonaNombre + tamañoDescripción;
    }
    return 0;
}
static int validarELF(const unsigned char *Datos, size_t tamaño, int modoLinux) {
    if (tamaño < sizeof(encabezadoELF)) return errorCódigoEjecutableUsuario;
    encabezadoELF encabezadoCódigoEjecutable; memcpy(&encabezadoCódigoEjecutable, Datos, sizeof(encabezadoCódigoEjecutable));
    if (encabezadoCódigoEjecutable.identificador[0] != 127 || encabezadoCódigoEjecutable.identificador[1] != 'E' || encabezadoCódigoEjecutable.identificador[2] != 'L' || encabezadoCódigoEjecutable.identificador[3] != 'F' ||
        encabezadoCódigoEjecutable.identificador[4] != 2 || encabezadoCódigoEjecutable.identificador[5] != 1 || encabezadoCódigoEjecutable.identificador[6] != 1 || (encabezadoCódigoEjecutable.identificador[7] != 0 && (!modoLinux || encabezadoCódigoEjecutable.identificador[7] != 3)) ||
        encabezadoCódigoEjecutable.categoríaTipo != 2 || encabezadoCódigoEjecutable.tipoMáquina != 183 || encabezadoCódigoEjecutable.númeroVersión != 1 || encabezadoCódigoEjecutable.bitsConfiguración || encabezadoCódigoEjecutable.tamañoEncabezadoCódigoEjecutable != sizeof(encabezadoCódigoEjecutable) ||
        encabezadoCódigoEjecutable.tamañoEntradaElementoEncabezadoPrograma != sizeof(programaELF) || !encabezadoCódigoEjecutable.númeroElementosEncabezadoPrograma || encabezadoCódigoEjecutable.númeroElementosEncabezadoPrograma > 16 ||
        encabezadoCódigoEjecutable.desfaseEncabezadoPrograma < sizeof(encabezadoCódigoEjecutable) || !contenido(encabezadoCódigoEjecutable.desfaseEncabezadoPrograma, (uint64_t)encabezadoCódigoEjecutable.númeroElementosEncabezadoPrograma * sizeof(programaELF), tamaño)) return errorCódigoEjecutableUsuario;
    uint8_t capacidadUsado[(finImagenUsuario - baseUsuario) / tamañoPágina] = {0};
    int puntoEntradaElementoVálido = 0, estadoCorrectoABI = 0, cargas = 0;
    for (unsigned índiceOrdinal = 0; índiceOrdinal < encabezadoCódigoEjecutable.númeroElementosEncabezadoPrograma; índiceOrdinal++) {
        programaELF posiciónDatos; memcpy(&posiciónDatos, Datos + encabezadoCódigoEjecutable.desfaseEncabezadoPrograma + índiceOrdinal * sizeof(posiciónDatos), sizeof(posiciónDatos));
        if (posiciónDatos.categoríaTipo == 4) {
            if (!contenido(posiciónDatos.valorDesfase, posiciónDatos.tamañoZonaArchivo, tamaño)) return errorCódigoEjecutableUsuario;
            if (comprobarInformaciónAuxiliar(Datos + posiciónDatos.valorDesfase, posiciónDatos.tamañoZonaArchivo)) estadoCorrectoABI = 1;
            continue;
        }
        if (posiciónDatos.categoríaTipo == 0 || posiciónDatos.categoríaTipo == 6 || (posiciónDatos.categoríaTipo == 0x6474e551 && !(posiciónDatos.bitsConfiguración & 1))) continue;
        if (posiciónDatos.categoríaTipo != 1) return errorCódigoEjecutableUsuario; // PT_INTERP, DYNAMIC, TLS esNoAdmitido
        if (!posiciónDatos.tamañoZonaMemoria) continue;
        if (posiciónDatos.bitsConfiguración & ~7u || !(posiciónDatos.bitsConfiguración & 4) || (posiciónDatos.bitsConfiguración & 3) == 3 || posiciónDatos.tamañoZonaArchivo > posiciónDatos.tamañoZonaMemoria ||
            (posiciónDatos.tamañoZonaArchivo && !contenido(posiciónDatos.valorDesfase, posiciónDatos.tamañoZonaArchivo, tamaño)) || posiciónDatos.dirección < baseUsuario ||
            !contenido(posiciónDatos.dirección, posiciónDatos.tamañoZonaMemoria, finImagenUsuario) ||
            (!modoLinux && ((posiciónDatos.dirección & (tamañoPágina - 1)) || (posiciónDatos.valorDesfase & (tamañoPágina - 1)) || posiciónDatos.fronteraAlinear != tamañoPágina)) ||
            (modoLinux && (((posiciónDatos.dirección ^ posiciónDatos.valorDesfase) & (tamañoPágina - 1)) || !posiciónDatos.fronteraAlinear ||
                (posiciónDatos.fronteraAlinear & (posiciónDatos.fronteraAlinear - 1)) || posiciónDatos.fronteraAlinear > 0x200000 || ((posiciónDatos.dirección ^ posiciónDatos.valorDesfase) & (posiciónDatos.fronteraAlinear - 1))))) return errorCódigoEjecutableUsuario;
        unsigned entradaElementoPrimero = (posiciónDatos.dirección - baseUsuario) / tamañoPágina;
        unsigned númeroElementosEntradaElemento = ((posiciónDatos.dirección & (tamañoPágina - 1)) + posiciónDatos.tamañoZonaMemoria + tamañoPágina - 1) / tamañoPágina;
        for (unsigned valorPágina = entradaElementoPrimero; valorPágina < entradaElementoPrimero + númeroElementosEntradaElemento; valorPágina++) {
            if (capacidadUsado[valorPágina]) return errorCódigoEjecutableUsuario;
            capacidadUsado[valorPágina] = 1;
        }
        if ((posiciónDatos.bitsConfiguración & 1) && encabezadoCódigoEjecutable.puntoEntradaElemento >= posiciónDatos.dirección && encabezadoCódigoEjecutable.puntoEntradaElemento < posiciónDatos.dirección + posiciónDatos.tamañoZonaArchivo && !(encabezadoCódigoEjecutable.puntoEntradaElemento & 3)) puntoEntradaElementoVálido = 1;
        cargas++;
    }
    return puntoEntradaElementoVálido && (modoLinux ? !estadoCorrectoABI : estadoCorrectoABI) && cargas ? 0 : errorCódigoEjecutableUsuario;
}
int eLFValidarUsuario(const unsigned char *Datos, size_t tamaño) { return validarELF(Datos, tamaño, 0); }
static void disposiciónPágina(uintptr_t dirección, uint64_t bitsConfiguración, unsigned permisosAcceso) {
    unsigned índiceBuscar = (dirección - baseUsuario) / tamañoPágina;
    listaPágina[índiceBuscar] = dirección | bitsConfiguración;
    listaPermisos[índiceBuscar] = permisosAcceso;
}
static int rangoUsuario(uintptr_t dirección, size_t númeroElementosEntradaElemento, int escrituraEnCurso) {
    if (dirección < baseUsuario || !contenido(dirección, númeroElementosEntradaElemento, finUsuario)) return 0;
    if (!númeroElementosEntradaElemento) return 1;
    unsigned entradaElementoPrimero = (dirección - baseUsuario) / tamañoPágina, elementoListaÚltimo = (dirección + númeroElementosEntradaElemento - 1 - baseUsuario) / tamañoPágina;
    for (unsigned índiceOrdinal = entradaElementoPrimero; índiceOrdinal <= elementoListaÚltimo; índiceOrdinal++) if (!(listaPermisos[índiceOrdinal] & (escrituraEnCurso ? 2 : 1))) return 0;
    return 1;
}
static int copiarRuta(uintptr_t dirección, char *ruta) {
    for (unsigned índiceOrdinal = 0; índiceOrdinal < 65; índiceOrdinal++) {
        if (!rangoUsuario(dirección, 1, 0)) return -14;
        ruta[índiceOrdinal] = *(const char *)dirección++;
        if (!ruta[índiceOrdinal]) return 0;
    }
    return -36;
}
static intptr_t resultadoNúcleo(intptr_t resultado) { return resultado < 0 ? -númeroError : resultado; }
static int descriptorArchivoAsociado(uint64_t manejadorArchivo) { return manejadorArchivo >= 3 && manejadorArchivo < 19 ? listaArchivo[manejadorArchivo - 3] : -1; }
static int propietarioExtremoConectorRed(uint64_t manejadorArchivo) { return manejadorArchivo >= 32 && manejadorArchivo < 56 && extremosConectorRed[manejadorArchivo - 32]; }
static int entradaDirección(uintptr_t valorApuntadoEnCurso, size_t longitud, struct pk_sockaddr_in *dirección) {
    if (longitud != sizeof(*dirección)) return -22;
    if (!rangoUsuario(valorApuntadoEnCurso, longitud, 0)) return -14;
    memcpy(dirección, (const void *)valorApuntadoEnCurso, sizeof(*dirección));
    return dirección->sin_family == AF_INET ? 0 : -97;
}
static int comprobarSalidaDirección(uintptr_t valorApuntadoEnCurso, uintptr_t punteroLongitud, pk_socklen_t *capacidadBúfer) {
    if (!rangoUsuario(punteroLongitud, sizeof(*capacidadBúfer), 1)) return -14;
    memcpy(capacidadBúfer, (const void *)punteroLongitud, sizeof(*capacidadBúfer));
    if (*capacidadBúfer > sizeof(struct pk_sockaddr_in)) *capacidadBúfer = sizeof(struct pk_sockaddr_in);
    if (*capacidadBúfer && !rangoUsuario(valorApuntadoEnCurso, *capacidadBúfer, 1)) return -14;
    return 0;
}
static void salidaDirección(uintptr_t valorApuntadoEnCurso, uintptr_t punteroLongitud, pk_socklen_t capacidadBúfer, int dirección, int númeroPuerto) {
    struct pk_sockaddr_in valor; memset(&valor, 0, sizeof(valor));
    valor.sin_family = AF_INET; valor.sin_port = pk_htons(númeroPuerto); valor.sin_addr.s_addr = pk_htonl(dirección);
    if (capacidadBúfer) memcpy((void *)valorApuntadoEnCurso, &valor, capacidadBúfer);
    pk_socklen_t longitud = sizeof(valor); memcpy((void *)punteroLongitud, &longitud, sizeof(longitud));
}
extern uintptr_t canalPlaca(uintptr_t, uintptr_t);
static intptr_t llamadaSistemaNativo(marcoUsuario *entradaElementoArchivo) {
    uintptr_t valorPrimero = entradaElementoArchivo->registroDatos[0], valorSegundo = entradaElementoArchivo->registroDatos[1], códigoCarácter = entradaElementoArchivo->registroDatos[2];
    char ruta[65];
    int manejadorArchivo, resultado;
    switch (entradaElementoArchivo->registroDatos[8]) {
    case 0: return 1; // propio ABI 버전
    case 1: // write: puntero 전체를 검사한 valorLadoPosterior Salida/Archivo cambiarValor
        if (códigoCarácter > 65536) return -22;
        if (!rangoUsuario(valorSegundo, códigoCarácter, 0)) return -14;
        if (valorPrimero == 1 || valorPrimero == 2) {
            uint64_t iniciarSalida=valorReloj();
            for (size_t índiceOrdinal = 0; índiceOrdinal < códigoCarácter; índiceOrdinal++) canalPlaca(valorPrimero, ((const unsigned char *)valorSegundo)[índiceOrdinal]);
            /* 큰 tty를 그린 valorNúcleo 시간만 돌려준다. EL0 resultadoCálculo 기한은 늘리지 않는다. */
            if(interactivo){
                tiempoPlazo+=valorReloj()-iniciarSalida;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(tiempoPlazo) : "memory");
            }
            return códigoCarácter;
        }
        if(valorPrimero>=40&&propietarioExtremoConectorRed(valorPrimero)){
            size_t númeroElementosElementoLista=códigoCarácter>512?512:códigoCarácter;for(size_t índiceOrdinal=0;índiceOrdinal<númeroElementosElementoLista;índiceOrdinal++)ponerRedJava(índiceOrdinal,((const unsigned char *)valorSegundo)[índiceOrdinal]);return escribirFlujoJava(valorPrimero,númeroElementosElementoLista);
        }
        manejadorArchivo = descriptorArchivoAsociado(valorPrimero); if (manejadorArchivo < 0) return -9;
        return resultadoNúcleo(pk_write(manejadorArchivo, (const void *)valorSegundo, códigoCarácter));
    case 2:
        if (códigoCarácter > 65536) return -22;
        if (!rangoUsuario(valorSegundo, códigoCarácter, 1)) return -14;
        if (valorPrimero == 0) {
            size_t númeroElementosElementoLista = 0;
            while (númeroElementosElementoLista < códigoCarácter) {
                int valorCarácter = (int32_t)obtenerCarácterPlaca(); if (valorCarácter == -2) return númeroElementosElementoLista; if (valorCarácter < 0) break;
                ((unsigned char *)valorSegundo)[númeroElementosElementoLista++] = valorCarácter;
            }
            return númeroElementosElementoLista ? (intptr_t)númeroElementosElementoLista : (códigoCarácter ? -11 : 0);
        }
        if(valorPrimero>=40&&propietarioExtremoConectorRed(valorPrimero)){
            resultado=leerFlujoJava(valorPrimero,códigoCarácter>512?512:códigoCarácter);if(resultado>0)for(int índiceOrdinal=0;índiceOrdinal<resultado;índiceOrdinal++)((unsigned char *)valorSegundo)[índiceOrdinal]=obtenerRedJava(índiceOrdinal);return resultado;
        }
        manejadorArchivo = descriptorArchivoAsociado(valorPrimero); if (manejadorArchivo < 0) return -9;
        return resultadoNúcleo(pk_read(manejadorArchivo, (void *)valorSegundo, códigoCarácter));
    case 3:
        resultado = copiarRuta(valorPrimero, ruta); if (resultado) return resultado;
        if (valorSegundo > 0x7ff) return -22;
        for (unsigned índiceOrdinal = 0; índiceOrdinal < 16; índiceOrdinal++) if (listaArchivo[índiceOrdinal] < 0) {
            manejadorArchivo = pk_open(ruta, (int)valorSegundo, 0600);
            if (manejadorArchivo < 0) return -númeroError;
            listaArchivo[índiceOrdinal] = manejadorArchivo; return índiceOrdinal + 3;
        }
        return -24;
    case 4:
        if (propietarioExtremoConectorRed(valorPrimero)) { resultado = cerrarExtremoConectorRed(valorPrimero); if (!resultado) extremosConectorRed[valorPrimero - 32] = 0; return resultado; }
        manejadorArchivo = descriptorArchivoAsociado(valorPrimero); if (manejadorArchivo < 0) return -9;
        resultado = pk_close(manejadorArchivo); if (!resultado) listaArchivo[valorPrimero - 3] = -1;
        return resultadoNúcleo(resultado);
    case 5:
        manejadorArchivo = descriptorArchivoAsociado(valorPrimero); if (manejadorArchivo < 0) return -9;
        if (códigoCarácter > 2) return -22;
        return resultadoNúcleo(pk_lseek(manejadorArchivo, (int64_t)valorSegundo, códigoCarácter));
    case 7: return milisegundosTranscurridosPlaca();
    case 8: { // brk: 별도 Usuario RW/NX valorMontículo, 새로 노출되는 페이지는 0으로 inicializar
        if (!valorPrimero) return finMontículo;
        if (valorPrimero < finImagenUsuario || valorPrimero > finMontículoUsuario) return -12;
        uintptr_t páginasAntiguo = (finMontículo + tamañoPágina - 1) & ~(tamañoPágina - 1);
        uintptr_t páginasNuevo = (valorPrimero + tamañoPágina - 1) & ~(tamañoPágina - 1);
        if (páginasNuevo > páginasAntiguo) {
            for (uintptr_t posiciónDatos = páginasAntiguo; posiciónDatos < páginasNuevo; posiciónDatos += tamañoPágina) disposiciónPágina(posiciónDatos, páginaNúcleo, 0);
            tablasSincronizarDatos();
            memset((void *)páginasAntiguo, 0, páginasNuevo - páginasAntiguo);
            for (uintptr_t posiciónDatos = páginasAntiguo; posiciónDatos < páginasNuevo; posiciónDatos += tamañoPágina) disposiciónPágina(posiciónDatos, escribirLeerUsuario, 3);
        } else {
            for (uintptr_t posiciónDatos = páginasNuevo; posiciónDatos < páginasAntiguo; posiciónDatos += tamañoPágina) {
                listaPágina[(posiciónDatos - baseUsuario) / tamañoPágina] = 0; listaPermisos[(posiciónDatos - baseUsuario) / tamañoPágina] = 0;
            }
        }
        finMontículo = valorPrimero; tablasSincronizarDatos(); return valorPrimero;
    }
    case 9:
        manejadorArchivo = descriptorArchivoAsociado(valorPrimero); return manejadorArchivo < 0 ? -9 : resultadoNúcleo(pk_size(manejadorArchivo));
    case 10:
        manejadorArchivo = descriptorArchivoAsociado(valorPrimero); return manejadorArchivo < 0 ? -9 : resultadoNúcleo(pk_ftruncate(manejadorArchivo, (int64_t)valorSegundo));
    case 11:
        resultado = copiarRuta(valorPrimero, ruta); return resultado ? resultado : resultadoNúcleo(pk_unlink(ruta));
    case 12:
        manejadorArchivo = descriptorArchivoAsociado(valorPrimero); return manejadorArchivo < 0 ? -9 : resultadoNúcleo(pk_fsync(manejadorArchivo));
    case 13: { // 그래픽 기초 API: Usuario 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t valorAnchuraSolicitado = entradaElementoArchivo->registroDatos[3], valorAlturaSolicitado = entradaElementoArchivo->registroDatos[4];
        if (!búferImagenPlaca()) return -19;
        uintptr_t extensiónRangoPantalla = anchuraPantallaPlaca(), longitudPantalla = alturaPantallaPlaca();
        if (valorPrimero > extensiónRangoPantalla || valorSegundo > longitudPantalla || valorAnchuraSolicitado > extensiónRangoPantalla - valorPrimero || valorAlturaSolicitado > longitudPantalla - valorSegundo) return -22;
        for (uintptr_t coordenadaCoordenadaVertical = valorSegundo; coordenadaCoordenadaVertical < valorSegundo + valorAlturaSolicitado; coordenadaCoordenadaVertical++) for (uintptr_t coordenadaCoordenadaHorizontal = valorPrimero; coordenadaCoordenadaHorizontal < valorPrimero + valorAnchuraSolicitado; coordenadaCoordenadaHorizontal++) píxelPlaca(coordenadaCoordenadaHorizontal, coordenadaCoordenadaVertical, códigoCarácter);
        return 0;
    }
    case 14: return (int32_t)obtenerCarácterPlaca();
    case 15: // args(-1,0,0)=númeroElementosElementoLista; args(index,buffer,capacity)=UTF-8 longitud
        if (valorPrimero == UINTPTR_MAX) return númeroElementosArgumentoReenviado;
        if (valorPrimero >= númeroElementosArgumentoReenviado) return -22;
        if (códigoCarácter <= longitudArgumentoReenviado[valorPrimero]) return -36;
        if (!rangoUsuario(valorSegundo, longitudArgumentoReenviado[valorPrimero] + 1, 1)) return -14;
        memcpy((void *)valorSegundo, argumentoReenviado[valorPrimero], longitudArgumentoReenviado[valorPrimero] + 1);
        return longitudArgumentoReenviado[valorPrimero];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(valorPrimero==0){if(!interactivoConsolaJava())return -95;interactivo=1;return terminalPlaca(13);}
        if(valorPrimero==2){interactivo=0;return 0;}
        if(valorPrimero==3)return terminalPlaca(13);
        if(valorPrimero!=1||!interactivo)return -22;
        resultado=(int32_t)obtenerCarácterPlaca();
        if(resultado==-4096)return resultado;
        iniciarTiempoEspera();return resultado<0?-11:resultado;
    case 17: { // 유한한 협력 esperarValor: Comunicación 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (valorPrimero > 100) return -22;
        uint64_t tiempoFin = valorReloj() + frecuencia * valorPrimero / 1000;
        do { inspeccionarRed(); inspeccionarTransferenciaArchivo(); __asm__ volatile("yield"); } while (valorReloj() < tiempoFin);
        iniciarTiempoEspera(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 valorPadre·빈 폴더를 검사한다.
        if (valorSegundo > 2) return -22;
        resultado = copiarRuta(valorPrimero, ruta); if (resultado) return resultado;
        unsigned longitud = 0; while (ruta[longitud]) longitud++;
        resultado = iniciarRutaJava(longitud); if (resultado < 0) return resultado;
        for (unsigned índiceOrdinal = 0; índiceOrdinal < longitud; índiceOrdinal++) byteRutaJava(índiceOrdinal, (unsigned char)ruta[índiceOrdinal]);
        return valorSegundo == 0 ? claseTipoEntradaElementoJava() : valorSegundo == 1 ? directorioCrearJava() : directorioEliminarJava();
    }
    case 20:
        if(valorPrimero==5){int valorCarácter=(int32_t)obtenerCarácterPlaca();if(valorCarácter==-4096)return valorCarácter;if(valorCarácter>=0)pulsarPantalla(objetoPropietario,valorCarácter);iniciarTiempoEspera();}
        if(valorPrimero==3&&códigoCarácter){if(!interactivoConsolaJava())return -95;interactivo=1;terminalPlaca(300);}
        return invocarPantalla(objetoPropietario,valorPrimero,valorSegundo,códigoCarácter,entradaElementoArchivo->registroDatos[3],entradaElementoArchivo->registroDatos[4],entradaElementoArchivo->registroDatos[5]);
    case 21:
        if(códigoCarácter>127)return -22;if(!rangoUsuario(valorSegundo,códigoCarácter*sizeof(uint32_t),0))return -14;
        return textoPantalla(objetoPropietario,valorPrimero,(const uint32_t *)valorSegundo,códigoCarácter);
    case 22: // Pantalla tamaño valorConsultar: 0=valorAnchura, 1=valorAltura. 사용자에게 주소를 노출하지 않는다.
        if (valorPrimero > 1) return -22;
        if (!búferImagenPlaca()) return -19;
        return valorPrimero == 0 ? anchuraPantallaPlaca() : alturaPantallaPlaca();
    case 32:
        if (valorPrimero != AF_INET) return -97;
        if(valorSegundo==SOCK_STREAM&&(códigoCarácter==0||códigoCarácter==6))resultado=crearFlujoJava();
        else if(valorSegundo==SOCK_DGRAM&&(códigoCarácter==0||códigoCarácter==IPPROTO_UDP))resultado=conectorRedRedJava(valorPrimero,valorSegundo,códigoCarácter);
        else return -93;
        if (resultado >= 32 && resultado < 56) extremosConectorRed[resultado - 32] = 1;
        return resultado;
    case 33: {
        if (!propietarioExtremoConectorRed(valorPrimero)) return -9;
        struct pk_sockaddr_in dirección;
        resultado = entradaDirección(valorSegundo, códigoCarácter, &dirección); if (resultado) return resultado;
        return valorPrimero>=40?asociarFlujoJava(valorPrimero,pk_htonl(dirección.sin_addr.s_addr),pk_htons(dirección.sin_port)):asociarRedJava(valorPrimero, pk_htonl(dirección.sin_addr.s_addr), pk_htons(dirección.sin_port));
    }
    case 34: {
        if (!propietarioExtremoConectorRed(valorPrimero)) return -9;
        if(valorPrimero>=40)return -95;
        if (entradaElementoArchivo->registroDatos[3]) return -95;
        if (códigoCarácter > 512) return -90;
        if (códigoCarácter && !rangoUsuario(valorSegundo, códigoCarácter, 0)) return -14;
        struct pk_sockaddr_in dirección;
        resultado = entradaDirección(entradaElementoArchivo->registroDatos[4], entradaElementoArchivo->registroDatos[5], &dirección); if (resultado) return resultado;
        for (unsigned índiceOrdinal = 0; índiceOrdinal < códigoCarácter; índiceOrdinal++) ponerRedJava(índiceOrdinal, ((const unsigned char *)valorSegundo)[índiceOrdinal]);
        return enviarRedJava(valorPrimero, pk_htonl(dirección.sin_addr.s_addr), pk_htons(dirección.sin_port), códigoCarácter);
    }
    case 35: {
        if (!propietarioExtremoConectorRed(valorPrimero)) return -9;
        if(valorPrimero>=40)return -95;
        if (entradaElementoArchivo->registroDatos[3]) return -95;
        if (códigoCarácter > 512) return -90;
        if (códigoCarácter && !rangoUsuario(valorSegundo, códigoCarácter, 1)) return -14;
        pk_socklen_t capacidadBúfer = 0;
        if (entradaElementoArchivo->registroDatos[4]) { resultado = comprobarSalidaDirección(entradaElementoArchivo->registroDatos[4], entradaElementoArchivo->registroDatos[5], &capacidadBúfer); if (resultado) return resultado; }
        resultado = operaciónRecepciónRedJava(valorPrimero, códigoCarácter); if (resultado < 0) return resultado;
        for (int índiceOrdinal = 0; índiceOrdinal < resultado; índiceOrdinal++) ((unsigned char *)valorSegundo)[índiceOrdinal] = obtenerRedJava(índiceOrdinal);
        if (entradaElementoArchivo->registroDatos[4]) salidaDirección(entradaElementoArchivo->registroDatos[4], entradaElementoArchivo->registroDatos[5], capacidadBúfer, remotoRedJava(valorPrimero), parRedRedJava(valorPrimero));
        return resultado;
    }
    case 36: {
        if (!propietarioExtremoConectorRed(valorPrimero)) return -9;
        pk_socklen_t capacidadBúfer;
        resultado = comprobarSalidaDirección(valorSegundo, códigoCarácter, &capacidadBúfer); if (resultado) return resultado;
        salidaDirección(valorSegundo,códigoCarácter,capacidadBúfer,valorPrimero>=40?direcciónFlujoJava(valorPrimero):direcciónRedJava(valorPrimero),valorPrimero>=40?puertoFlujoJava(valorPrimero):puertoRedJava(valorPrimero)); return 0;
    }
    case 37: {
        if(valorPrimero<40||!propietarioExtremoConectorRed(valorPrimero))return -9;struct pk_sockaddr_in dirección;
        resultado=entradaDirección(valorSegundo,códigoCarácter,&dirección);if(resultado)return resultado;
        return conectarFlujoJava(valorPrimero,pk_htonl(dirección.sin_addr.s_addr),pk_htons(dirección.sin_port));
    }
    case 38: return valorPrimero>=40&&propietarioExtremoConectorRed(valorPrimero)?escucharFlujoJava(valorPrimero,valorSegundo):-9;
    case 39:
        if(valorPrimero<40||!propietarioExtremoConectorRed(valorPrimero))return -9;
        if(valorSegundo||códigoCarácter)return -95;resultado=aceptarFlujoJava(valorPrimero);if(resultado>=40&&resultado<56)extremosConectorRed[resultado-32]=1;return resultado;
    case 40: return valorPrimero>=40&&propietarioExtremoConectorRed(valorPrimero)?parRedFlujoJava(valorPrimero):-9;
    default: return -38; // esNoAdmitido 기능을 성공으로 가장하지 않음
    }
}
#include "compatibilidadLinux.inc"
static intptr_t LlamadaSistema(marcoUsuario *entradaElementoArchivo) {
    network_poll();
    return aBILinux ? llamadaSistemaLinux(entradaElementoArchivo) : llamadaSistemaNativo(entradaElementoArchivo);
}
static void núcleoRetornar(marcoUsuario *entradaElementoArchivo, int resultado) {
    detenerTiempoEspera();
    entradaElementoArchivo->registroDatos[0] = (uint64_t)(int64_t)resultado;
    entradaElementoArchivo->posiciónComando = (uintptr_t)retornarUsuario;
    entradaElementoArchivo->códigoEstadoValor = 0x3c5; // EL1h, DAIF masked
}
int excepciónUsuario(marcoUsuario *entradaElementoArchivo, unsigned interceptarSeñal) {
    if (!activo || (entradaElementoArchivo->códigoEstadoValor & 15) != 0) return 0;
    if (interceptarSeñal) {
        uint32_t valorAcuseRecibo = registroMáquina(interfazCPUInterrumpir + 0xc), valorIdentificador = valorAcuseRecibo & 1023;
        if (valorIdentificador == 30) { núcleoRetornar(entradaElementoArchivo, tiempoEsperaUsuario); registroMáquina(interfazCPUInterrumpir + 0x10) = valorAcuseRecibo; return 1; }
        if (valorIdentificador < 1020) registroMáquina(interfazCPUInterrumpir + 0x10) = valorAcuseRecibo;
        return 1;
    }
    uint64_t estadoValorExcepción; __asm__ volatile("mrs %0, esr_el1" : "=r"(estadoValorExcepción));
    if (valorReloj() >= tiempoPlazo) { núcleoRetornar(entradaElementoArchivo, tiempoEsperaUsuario); return 1; }
    unsigned categoríaExcepción = estadoValorExcepción >> 26;
    if (categoríaExcepción == 0x15 && (estadoValorExcepción & 0xffff) == 0) {
        if (aBILinux ? entradaElementoArchivo->registroDatos[8] == 93 || entradaElementoArchivo->registroDatos[8] == 94 : entradaElementoArchivo->registroDatos[8] == 6) núcleoRetornar(entradaElementoArchivo, (int)(entradaElementoArchivo->registroDatos[0] & 255));
        else {
            intptr_t resultado=LlamadaSistema(entradaElementoArchivo);
            if(resultado==-4096&&interactivo){
                guardado[objetoPropietario].marcoEjecución=*entradaElementoArchivo;guardado[objetoPropietario].marcoEjecución.posiciónComando-=4;
                guardarComaFlotanteUsuario(guardado[objetoPropietario].estadoValorPuntoFlotante);núcleoRetornar(entradaElementoArchivo,interrumpidoUsuario);
            }else entradaElementoArchivo->registroDatos[0]=(uint64_t)resultado;
        }
    } else núcleoRetornar(entradaElementoArchivo, categoríaExcepción == 0x24 ? errorDatosUsuario : categoríaExcepción == 0x20 ? errorEjecuciónUsuario : instrucciónMáquinaInválidoUsuario);
    return 1;
}

// 생성된 const ELF valorGrupo: 실행은 반드시 Programa 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *Datos; size_t tamaño; unsigned valorReenviado; } programa;
#include "programs.h"
static void *instantánea(unsigned índicePosición){return (void *)(0x04000000ul+índicePosición*(finUsuario-baseUsuario));}
static int terminarPrograma(int resultado){
    tiempoAcumuladoUsuario[objetoPropietario]+=(uint32_t)milisegundosTranscurridosPlaca()-tiempoEjecuciónUsuario[objetoPropietario];
    detenerTiempoEspera();activo=0;
    if(resultado==interrumpidoUsuario){
        procesoGuardado *datosCadena=&guardado[objetoPropietario];datosCadena->estadoValorEnPausa=1;datosCadena->interactivo=interactivo;datosCadena->aBILinux=aBILinux;datosCadena->almacenamientoMontículo=finMontículo;datosCadena->númeroElementosArgumentos=númeroElementosArgumentoReenviado;
        memcpy(datosCadena->listaPermisos,listaPermisos,sizeof(listaPermisos));memcpy(datosCadena->listaArchivo,listaArchivo,sizeof(listaArchivo));memcpy(datosCadena->extremosConectorRed,extremosConectorRed,sizeof(extremosConectorRed));
        memcpy(datosCadena->arregloArgumento,argumentoReenviado,sizeof(argumentoReenviado));memcpy(datosCadena->longitudArgumento,longitudArgumentoReenviado,sizeof(longitudArgumentoReenviado));
        for(unsigned índiceOrdinal=0;índiceOrdinal<númeroElementosPáginaUsuario;índiceOrdinal++)if(listaPermisos[índiceOrdinal])memcpy((unsigned char *)instantánea(objetoPropietario)+índiceOrdinal*tamañoPágina,(void *)(baseUsuario+índiceOrdinal*tamañoPágina),tamañoPágina);
    }else{
        guardado[objetoPropietario].estadoValorEnPausa=0;inicializarPantalla(objetoPropietario);
        for(unsigned índiceOrdinal=0;índiceOrdinal<16;índiceOrdinal++)if(listaArchivo[índiceOrdinal]>=0)pk_close(listaArchivo[índiceOrdinal]);
        for(unsigned índiceOrdinal=0;índiceOrdinal<24;índiceOrdinal++)if(extremosConectorRed[índiceOrdinal])cerrarExtremoConectorRed(índiceOrdinal+32);
    }
    for(unsigned índiceOrdinal=0;índiceOrdinal<númeroElementosPáginaUsuario;índiceOrdinal++){listaPágina[índiceOrdinal]=0;listaPermisos[índiceOrdinal]=0;}tablasSincronizarDatos();return resultado;
}
uintptr_t controlUsuarioPlaca(uintptr_t acción){
    unsigned índicePosición=acción&15;if(índicePosición>=4||activo)return (uint32_t)-22;
    procesoGuardado *datosCadena=&guardado[índicePosición];
    if(acción>=32){if(datosCadena->estadoValorEnPausa){for(unsigned índiceOrdinal=0;índiceOrdinal<16;índiceOrdinal++)if(datosCadena->listaArchivo[índiceOrdinal]>=0)pk_close(datosCadena->listaArchivo[índiceOrdinal]);for(unsigned índiceOrdinal=0;índiceOrdinal<24;índiceOrdinal++)if(datosCadena->extremosConectorRed[índiceOrdinal])cerrarExtremoConectorRed(índiceOrdinal+32);}datosCadena->estadoValorEnPausa=0;inicializarPantalla(índicePosición);return 0;}
    if(acción>=16)return datosCadena->estadoValorEnPausa;
    if(!datosCadena->estadoValorEnPausa)return (uint32_t)-22;
    objetoPropietario=índicePosición;interactivo=datosCadena->interactivo;aBILinux=datosCadena->aBILinux;finMontículo=datosCadena->almacenamientoMontículo;númeroElementosArgumentoReenviado=datosCadena->númeroElementosArgumentos;
    memcpy(listaArchivo,datosCadena->listaArchivo,sizeof(listaArchivo));memcpy(extremosConectorRed,datosCadena->extremosConectorRed,sizeof(extremosConectorRed));memcpy(argumentoReenviado,datosCadena->arregloArgumento,sizeof(argumentoReenviado));memcpy(longitudArgumentoReenviado,datosCadena->longitudArgumento,sizeof(longitudArgumentoReenviado));
    for(unsigned índiceOrdinal=0;índiceOrdinal<númeroElementosPáginaUsuario;índiceOrdinal++)listaPágina[índiceOrdinal]=(baseUsuario+índiceOrdinal*tamañoPágina)|páginaNúcleo;tablasSincronizarDatos();
    memset((void *)baseUsuario,0,finUsuario-baseUsuario);
    for(unsigned índiceOrdinal=0;índiceOrdinal<númeroElementosPáginaUsuario;índiceOrdinal++)if(datosCadena->listaPermisos[índiceOrdinal])memcpy((void *)(baseUsuario+índiceOrdinal*tamañoPágina),(unsigned char *)instantánea(índicePosición)+índiceOrdinal*tamañoPágina,tamañoPágina);
    memcpy(listaPermisos,datosCadena->listaPermisos,sizeof(listaPermisos));
    for(unsigned índiceOrdinal=0;índiceOrdinal<númeroElementosPáginaUsuario;índiceOrdinal++){unsigned posiciónDatos=listaPermisos[índiceOrdinal];listaPágina[índiceOrdinal]=posiciónDatos?(baseUsuario+índiceOrdinal*tamañoPágina)|(posiciónDatos==3?escribirLeerUsuario:posiciónDatos==5?ejecutarLeerUsuario:solamenteLeerUsuario):0;}
    tablasSincronizarDatos();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");activo=1;datosCadena->estadoValorEnPausa=0;iniciarTiempoEspera();
    tiempoEjecuciónUsuario[objetoPropietario]=milisegundosTranscurridosPlaca();
    return (uint32_t)terminarPrograma(reanudarUsuario(&datosCadena->marcoEjecución,datosCadena->estadoValorPuntoFlotante));
}
static int ponerEnMarchaPrograma(const unsigned char *Datos, size_t tamaño, unsigned valorReenviado, int modoLinux, const char *nombre) {
    if (activo) return -16;
    objetoPropietario=terminalPlaca(11);if(objetoPropietario<0||objetoPropietario>3||guardado[objetoPropietario].estadoValorEnPausa)return -16;interactivo=0;
    int válido = validarELF(Datos, tamaño, modoLinux); if (válido) return válido;
    aBILinux = modoLinux;
    unsigned índiceNombre=0;
    while (*nombre && índiceNombre<31) nombreComandoUsuario[objetoPropietario][índiceNombre++]=(unsigned char)*nombre++;
    if (númeroElementosArgumentoReenviado && longitudArgumentoReenviado[0]) {
        if (índiceNombre) nombreComandoUsuario[objetoPropietario][índiceNombre++]=' ';
        for (unsigned índicePosición=0; índicePosición<longitudArgumentoReenviado[0]; índicePosición++) nombreComandoUsuario[objetoPropietario][índiceNombre++]=argumentoReenviado[0][índicePosición];
    }
    nombreComandoUsuario[objetoPropietario][índiceNombre]=0; númeroUsuario[objetoPropietario]=númeroUsuarioSiguiente++;
    if (númeroUsuarioSiguiente>0x7fffffffu) númeroUsuarioSiguiente=10;
    tiempoIniciarUsuario[objetoPropietario]=milisegundosTranscurridosPlaca(); tiempoAcumuladoUsuario[objetoPropietario]=0;
    for (unsigned índiceOrdinal = 0; índiceOrdinal < númeroElementosPáginaUsuario; índiceOrdinal++) listaPágina[índiceOrdinal] = (baseUsuario + índiceOrdinal * tamañoPágina) | páginaNúcleo;
    tablasSincronizarDatos();
    memset((void *)baseUsuario, 0, finUsuario - baseUsuario);
    memset(listaPermisos, 0, sizeof(listaPermisos));
    encabezadoELF encabezadoCódigoEjecutable; memcpy(&encabezadoCódigoEjecutable, Datos, sizeof(encabezadoCódigoEjecutable));
    for (unsigned índiceOrdinal = 0; índiceOrdinal < encabezadoCódigoEjecutable.númeroElementosEncabezadoPrograma; índiceOrdinal++) {
        programaELF posiciónDatos; memcpy(&posiciónDatos, Datos + encabezadoCódigoEjecutable.desfaseEncabezadoPrograma + índiceOrdinal * sizeof(posiciónDatos), sizeof(posiciónDatos));
        if (posiciónDatos.categoríaTipo != 1 || !posiciónDatos.tamañoZonaMemoria) continue;
        if (posiciónDatos.tamañoZonaArchivo) memcpy((void *)(uintptr_t)posiciónDatos.dirección, Datos + posiciónDatos.valorDesfase, posiciónDatos.tamañoZonaArchivo);
        for (uintptr_t posiciónActual = posiciónDatos.dirección & ~(tamañoPágina - 1); posiciónActual < posiciónDatos.dirección + posiciónDatos.tamañoZonaMemoria; posiciónActual += tamañoPágina) {
            listaPermisos[(posiciónActual - baseUsuario) / tamañoPágina] = (posiciónDatos.bitsConfiguración & 2) ? 3 : ((posiciónDatos.bitsConfiguración & 1) ? 5 : 1);
        }
    }
    for (uintptr_t posiciónActual = direcciónPilaUsuario; posiciónActual < finUsuario; posiciónActual += tamañoPágina) listaPermisos[(posiciónActual - baseUsuario) / tamañoPágina] = 3;
    uintptr_t pilaInicialValor = modoLinux ? pilaIniciarLinux(encabezadoCódigoEjecutable.puntoEntradaElemento) : finUsuario;
    for (unsigned índiceOrdinal = 0; índiceOrdinal < númeroElementosPáginaUsuario; índiceOrdinal++) {
        unsigned permisosAcceso = listaPermisos[índiceOrdinal];
        listaPágina[índiceOrdinal] = permisosAcceso ? (baseUsuario + índiceOrdinal * tamañoPágina) | (permisosAcceso == 3 ? escribirLeerUsuario : permisosAcceso == 5 ? ejecutarLeerUsuario : solamenteLeerUsuario) : 0;
    }
    tablasSincronizarDatos();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned índiceOrdinal = 0; índiceOrdinal < 16; índiceOrdinal++) listaArchivo[índiceOrdinal] = -1;
    memset(extremosConectorRed, 0, sizeof(extremosConectorRed));
    finMontículo = finImagenUsuario;
    activo = 1; iniciarTiempoEspera();
    tiempoEjecuciónUsuario[objetoPropietario]=milisegundosTranscurridosPlaca();
    int resultado = entrarUsuario(encabezadoCódigoEjecutable.puntoEntradaElemento, pilaInicialValor, valorReenviado);
    return terminarPrograma(resultado);
}
uintptr_t ponerEnMarchaUsuarioPlaca(uintptr_t índiceBuscar) {
    if (índiceBuscar >= sizeof(entradasCódigoEjecutable) / sizeof(entradasCódigoEjecutable[0])) return (uint32_t)-22;
    const char *nombre=índiceBuscar==10?"javac":índiceBuscar==11?"java":índiceBuscar==12?"python":índiceBuscar==13?"vi":índiceBuscar==14?"jar":índiceBuscar==15?"cc":índiceBuscar==16?"jaot":"ELF";
    return (uint32_t)ponerEnMarchaPrograma(entradasCódigoEjecutable[índiceBuscar].Datos, entradasCódigoEjecutable[índiceBuscar].tamaño, entradasCódigoEjecutable[índiceBuscar].valorReenviado, 0, nombre);
}
static uintptr_t ejecutarArchivo(int modoLinux) {
    static unsigned char imagen[16384];
    if (activo || !númeroElementosArgumentoReenviado) return (uint32_t)-22;
    int manejadorArchivo = pk_open((const char *)argumentoReenviado[0], leerValorSolamente, 0);
    if (manejadorArchivo < 0) return (uint32_t)-númeroError;
    int tamaño = pk_size(manejadorArchivo);
    if (tamaño < 0 || (unsigned)tamaño > sizeof(imagen)) { pk_close(manejadorArchivo); return (uint32_t)-27; }
    int númeroElementosRecibido = pk_read(manejadorArchivo, imagen, tamaño); pk_close(manejadorArchivo);
    if (númeroElementosRecibido != tamaño) return (uint32_t)-5;
    return (uint32_t)ponerEnMarchaPrograma(imagen, tamaño, 0, modoLinux, "");
}
uintptr_t archivoUsuarioPlaca(void) { return ejecutarArchivo(0); }
uintptr_t archivoLinuxUsuarioPlaca(void) { return ejecutarArchivo(1); }
uintptr_t validarUsuarioPlaca(void) {
    for (unsigned índiceOrdinal = 0; índiceOrdinal < sizeof(ejecutablesInválido) / sizeof(ejecutablesInválido[0]); índiceOrdinal++)
        if (eLFValidarUsuario(ejecutablesInválido[índiceOrdinal].Datos, ejecutablesInválido[índiceOrdinal].tamaño) != errorCódigoEjecutableUsuario) return índiceOrdinal + 1;
    return 0;
}
