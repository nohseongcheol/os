#include "../denominación/nombresEnlazarMáquina.h"
#include "informaciónPantalla.h"
#include <stdint.h>
#include <stddef.h>
#include "Usuario.h"
#include "../PilaRed/PilaRed.h"
typedef uintptr_t palabraMáquina;
#define registroMáquina(valorPrimero) (*(volatile uint32_t *)(uintptr_t)(valorPrimero))
#define dispositivoSerie 0xfe201000u
#define entradaSalidaPropósitoGeneral 0xfe200000u
#define direcciónBuzón 0xfe00b880u
static inline void barreraMemoria(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t númeroElementosReloj(void) { uint64_t datosTemporal; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(datosTemporal)); return datosTemporal; }
static uint64_t frecuencia;
static volatile uint32_t datosBuzón[64] __attribute__((aligned(16)));
static unsigned listoPantalla;
static uint32_t unidadByteKibiMemoriaARM;

void *memset(void *posiciónDatos, int códigoCarácter, size_t númeroElementosElementoLista) { unsigned char *desfaseSiguiente = posiciónDatos; while (númeroElementosElementoLista--) *desfaseSiguiente++ = códigoCarácter; return posiciónDatos; }
void *memcpy(void *datosDestino, const void *datosCadena, size_t númeroElementosElementoLista) { unsigned char *valorPrimero = datosDestino; const unsigned char *valorSegundo = datosCadena; while (númeroElementosElementoLista--) *valorPrimero++ = *valorSegundo++; return datosDestino; }

static int buzón(void) {
    uint32_t petición = (uint32_t)(uintptr_t)datosBuzón | 8;
    uint64_t ponerEnMarcha = númeroElementosReloj();
    barreraMemoria();
    while (registroMáquina(direcciónBuzón + 0x38) & 0x80000000u)
        if (númeroElementosReloj() - ponerEnMarcha > frecuencia) return 0;
    registroMáquina(direcciónBuzón + 0x20) = petición;
    for (;;) {
        if (!(registroMáquina(direcciónBuzón + 0x18) & 0x40000000u)) {
            uint32_t respuesta = registroMáquina(direcciónBuzón);
            if (respuesta == petición) { barreraMemoria(); return datosBuzón[1] == 0x80000000u; }
        }
        if (númeroElementosReloj() - ponerEnMarcha > frecuencia) return 0;
    }
}

extern int32_t salidaConsolaJava(int32_t, int32_t), entradaConsolaJava(void);
extern void byteTerminal(unsigned);
extern int pendienteTerminal(void);
extern void punteroTerminal(unsigned,int,int),atajoTecladoTerminal(unsigned);
extern void modoEntradaTerminal(unsigned);
#include "../valorRemoto/valorRemoto.h"
static int flujos;
static unsigned elementoPrevioUART;
palabraMáquina flujosPlaca(palabraMáquina esUsado) { flujos=esUsado!=0; return 0; }
palabraMáquina canalPlaca(palabraMáquina canal, palabraMáquina códigoCarácter) {
    if(flujos && salidaConsolaJava((int32_t)canal,(int32_t)(códigoCarácter&255))) return 0;
    byteTerminal(códigoCarácter&255);
    salidaRemoto(códigoCarácter&255);
    if ((códigoCarácter&255)==10 && elementoPrevioUART!=13) {
        while (registroMáquina(dispositivoSerie + 0x18) & 0x20) __asm__ volatile("yield");
        registroMáquina(dispositivoSerie)=13;
    }
    elementoPrevioUART=códigoCarácter&255;
    while (registroMáquina(dispositivoSerie + 0x18) & 0x20) __asm__ volatile("yield");
    registroMáquina(dispositivoSerie) = (uint32_t)códigoCarácter & 255;
    return 0;
}
palabraMáquina escribirCarácterPlaca(palabraMáquina códigoCarácter) { return canalPlaca(1,códigoCarácter); }
palabraMáquina obtenerCarácterCrudoPlaca(void) {
    int carácterRemoto=entradaRemoto();if(carácterRemoto>=0)return carácterRemoto;
    if (registroMáquina(dispositivoSerie + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t valor = registroMáquina(dispositivoSerie);
    if (valor & 0xf00) { registroMáquina(dispositivoSerie + 4) = 0; return (uint32_t)-1; }
    return valor & 255;
}
palabraMáquina obtenerCarácterPlaca(void) {
    network_poll();
    static unsigned paqueteDatosEntrante,capacidadUsado; static unsigned char datosPaqueteDatos[6];
    if(pendienteTerminal())return (uint32_t)-4096;
    if(flujos){int32_t códigoCarácter=entradaConsolaJava();if(códigoCarácter!=-3)return (uint32_t)códigoCarácter;}
    for(;;){
        int códigoCarácter=(int32_t)obtenerCarácterCrudoPlaca();if(códigoCarácter<0)return (uint32_t)códigoCarácter;
        if(!paqueteDatosEntrante){if(códigoCarácter!=30)return códigoCarácter;paqueteDatosEntrante=1;capacidadUsado=0;continue;}
        datosPaqueteDatos[capacidadUsado++]=códigoCarácter;if(capacidadUsado<6)continue;paqueteDatosEntrante=0;
        if(datosPaqueteDatos[0]==1)punteroTerminal(datosPaqueteDatos[1],datosPaqueteDatos[2]+datosPaqueteDatos[3]*256,datosPaqueteDatos[4]+datosPaqueteDatos[5]*256);
        if(datosPaqueteDatos[0]==2)atajoTecladoTerminal(datosPaqueteDatos[1]);
        if(datosPaqueteDatos[0]==3)modoEntradaTerminal(datosPaqueteDatos[1]);
        if(pendienteTerminal())return (uint32_t)-4096;
    }
}
palabraMáquina milisegundosTranscurridosPlaca(void) { return (uint32_t)(númeroElementosReloj() / (frecuencia / 1000)); }
palabraMáquina nivelExcepciónPlaca(void) { uint64_t datosTemporal; __asm__ volatile("mrs %0, CurrentEL" : "=r"(datosTemporal)); return datosTemporal >> 2; }
static void uARTMostrarLínea(const char *datosCadena) { while (*datosCadena) escribirCarácterPlaca((unsigned char)*datosCadena++); }
static void uARTHexadecimalCorto(palabraMáquina númeroElementosElementoLista) { const char *dígitosHexadecimal = "0123456789abcdef"; for (int datosCadena = 60; datosCadena >= 0; datosCadena -= 4) escribirCarácterPlaca(dígitosHexadecimal[(númeroElementosElementoLista >> datosCadena) & 15]); }
palabraMáquina detenerPlaca(palabraMáquina valorEstadoValor) {
    uARTMostrarLínea("\r\nHALTED "); uARTHexadecimalCorto(valorEstadoValor); uARTMostrarLínea("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void paradaFatalNúcleo(const char *valorCausa) __attribute__((noreturn));
void paradaFatalNúcleo(const char *valorCausa) { uARTMostrarLínea("\r\nPANIC: "); uARTMostrarLínea(valorCausa); detenerPlaca(1); __builtin_unreachable(); }
void excepciónPlaca(palabraMáquina estadoValorExcepción, palabraMáquina posiciónComando, palabraMáquina direcciónInválido) {
    uARTMostrarLínea("\r\nEXCEPTION ESR="); uARTHexadecimalCorto(estadoValorExcepción);
    uARTMostrarLínea(" PC="); uARTHexadecimalCorto(posiciónComando); uARTMostrarLínea(" FAR="); uARTHexadecimalCorto(direcciónInválido);
    detenerPlaca(2);
}
int equipoFísicoFísicoPlaca(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    datosBuzón[0]=32;datosBuzón[1]=0;datosBuzón[2]=0x10004;datosBuzón[3]=8;datosBuzón[4]=0;
    datosBuzón[5]=datosBuzón[6]=datosBuzón[7]=0;
    return buzón()&&datosBuzón[4]==0x80000008u&&(datosBuzón[5]||datosBuzón[6]);
}
int direcciónMáquinaPlaca(unsigned char *dirección) {
    datosBuzón[0]=32;datosBuzón[1]=0;datosBuzón[2]=0x10003;datosBuzón[3]=8;datosBuzón[4]=0;
    datosBuzón[5]=datosBuzón[6]=datosBuzón[7]=0;
    if(!buzón()||(datosBuzón[4]&0x80000000u)==0||(datosBuzón[4]&0xffff)!=6)return 0;
    const unsigned char *Datos=(const unsigned char*)&datosBuzón[5];unsigned valorTotalSuma=0;
    for(unsigned índiceOrdinal=0;índiceOrdinal<6;índiceOrdinal++){dirección[índiceOrdinal]=Datos[índiceOrdinal];valorTotalSuma|=Datos[índiceOrdinal];}return valorTotalSuma&&!(dirección[0]&1);
}
void operaciónInicializaciónPlaca(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(frecuencia));
    registroMáquina(dispositivoSerie + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    registroMáquina(entradaSalidaPropósitoGeneral + 4) = (registroMáquina(entradaSalidaPropósitoGeneral + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    registroMáquina(entradaSalidaPropósitoGeneral + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. valorFallo 시 config.txt의 48MHz를 사용한다.
    datosBuzón[0] = 36; datosBuzón[1] = 0; datosBuzón[2] = 0x38002; datosBuzón[3] = 12;
    datosBuzón[4] = 0; datosBuzón[5] = 2; datosBuzón[6] = 48000000; datosBuzón[7] = 0; datosBuzón[8] = 0;
    int sanoReloj = buzón();
    uint32_t valorVelocidad = sanoReloj && datosBuzón[6] >= 1843200 ? datosBuzón[6] : 48000000;
    datosBuzón[0]=32; datosBuzón[1]=0; datosBuzón[2]=0x10005; datosBuzón[3]=8; datosBuzón[4]=0;
    datosBuzón[5]=datosBuzón[6]=datosBuzón[7]=0;
    if (buzón() && datosBuzón[4]==0x80000008u) unidadByteKibiMemoriaARM=datosBuzón[6]/1024;
    uint32_t divisor64 = (uint32_t)(((uint64_t)valorVelocidad * 4 + 57600) / 115200);
    registroMáquina(dispositivoSerie + 0x44) = 0x7ff;
    registroMáquina(dispositivoSerie + 0x24) = divisor64 / 64;
    registroMáquina(dispositivoSerie + 0x28) = divisor64 % 64;
    registroMáquina(dispositivoSerie + 0x2c) = (3u << 5) | (1u << 4);
    registroMáquina(dispositivoSerie + 0x38) = 0;
    registroMáquina(dispositivoSerie + 0x30) = 0x301;
    barreraMemoria();
    uARTMostrarLínea("JKOROS AARCH64 BARE METAL\r\n");
    operaciónInicializaciónSistemaUsuario();
    network_init();
}
palabraMáquina fTPPlaca(palabraMáquina acción) { return (uint32_t)ftp_control((int)acción); }
palabraMáquina estadoRedPlaca(palabraMáquina valorEntradaElemento, palabraMáquina número) { return leerEstadoRed(valorEntradaElemento, número); }
palabraMáquina ajustesRedPlaca(palabraMáquina acción, palabraMáquina dirección, palabraMáquina valorMáscara, palabraMáquina valorPasarela) { return (uint32_t)configurarRed(acción, dirección, valorMáscara, valorPasarela); }
palabraMáquina respuestaRetornoEnviarPlaca(palabraMáquina dirección, palabraMáquina valorOrden) { return (uint32_t)iniciarPruebaRespuestaRetorno(dirección, valorOrden); }
palabraMáquina respuestaRetornoLeerPlaca(palabraMáquina valorEntradaElemento) { return (uint32_t)leerPruebaRespuestaRetorno(valorEntradaElemento); }
palabraMáquina desactivadoAlimentaciónPlaca(void) {
    ftp_control(0);
    for (unsigned número=0; número<32; número++) cerrarRed(número);
    for (unsigned número=0; número<4; número++) controlUsuarioPlaca(32+número);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    uARTMostrarLínea("\r\nPOWER OFF\r\n");
    while (registroMáquina(dispositivoSerie+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    registroMáquina(0xfe100020ul)=0x5a000000u | (registroMáquina(0xfe100020ul)&~0xfffu) | 0x555;
    registroMáquina(0xfe100024ul)=0x5a000000u | 10;
    registroMáquina(0xfe10001cul)=0x5a000000u | (registroMáquina(0xfe10001cul)&~0x30u) | 0x20;
    barreraMemoria();
    for (;;) __asm__ volatile("wfe");
}

palabraMáquina búferImagenPlaca(void) {
    if (listoPantalla) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 elementoListaActual 크기를 읽는다. */
    const uint32_t valorConsultar[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t anchuraSolicitado = 640, alturaSolicitado = 480;
    for (size_t índiceOrdinal = 0; índiceOrdinal < sizeof(valorConsultar)/4; índiceOrdinal++) datosBuzón[índiceOrdinal] = valorConsultar[índiceOrdinal];
    if (buzón() && datosBuzón[4] == 0x80000008u &&
        datosBuzón[5] >= 640 && datosBuzón[5] <= 1920 &&
        datosBuzón[6] >= 480 && datosBuzón[6] <= 1080) {
        anchuraSolicitado = datosBuzón[5]; alturaSolicitado = datosBuzón[6];
    }
    const uint32_t petición[] = {
        35 * 4, 0,
        0x48003, 8, 0, anchuraSolicitado, alturaSolicitado,
        0x48004, 8, 0, anchuraSolicitado, alturaSolicitado,
        0x48005, 4, 0, 32,
        0x48006, 4, 0, 1,
        0x48009, 8, 0, 0, 0,
        0x40001, 8, 0, 4096, 0,
        0x40008, 4, 0, 0,
        0
    };
    for (size_t índiceOrdinal = 0; índiceOrdinal < sizeof(petición)/4; índiceOrdinal++) datosBuzón[índiceOrdinal] = petición[índiceOrdinal];
    // valorExtremoSuperior 메시지의 datosEfectivo 길이를 valorUsar: 태그 añadirFinalEntradaElemento 시 longitud 불일치를 방지한다.
    datosBuzón[0] = sizeof(petición);
    if (!buzón()) return 0;
    const unsigned respuestasLista[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned longitudRespuestaRetorno[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned índiceOrdinal = 0; índiceOrdinal < sizeof(respuestasLista)/sizeof(respuestasLista[0]); índiceOrdinal++)
        if (datosBuzón[respuestasLista[índiceOrdinal]] != (0x80000000u | longitudRespuestaRetorno[índiceOrdinal])) return 0;
    uint32_t valorFondo = datosBuzón[28] & 0x3fffffffu;
    uint32_t tamaño = datosBuzón[29];
    uint32_t anchuraRecibido = datosBuzón[5], alturaRecibido = datosBuzón[6], espaciadoLíneaRecibido = datosBuzón[33];
    if (datosBuzón[15] != 32 || datosBuzón[19] != 1 ||
        anchuraRecibido < 640 || anchuraRecibido > 1920 || alturaRecibido < 480 || alturaRecibido > 1080 ||
        datosBuzón[10] < anchuraRecibido || datosBuzón[11] < alturaRecibido || datosBuzón[23] || datosBuzón[24] ||
        !valorFondo || valorFondo < 0x1000000 || (valorFondo & 3) || espaciadoLíneaRecibido < anchuraRecibido * 4 || (espaciadoLíneaRecibido & 3) ||
        (uint64_t)espaciadoLíneaRecibido * alturaRecibido > tamaño || (uint64_t)valorFondo + tamaño > 0x40000000u)
        return 0;
    dibujoPrepararPlaca((volatile uint32_t *)(uintptr_t)valorFondo, anchuraRecibido, alturaRecibido, espaciadoLíneaRecibido);
    listoPantalla = 1;
    return 1;
}

// 단일 코어의 협력식 valorHiloEjecución. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t guardado[13]; } contexto;
static contexto contextos[3];
static unsigned char pilas[2][65536] __attribute__((aligned(16)));
static int esEnEjecución[3] = {1, 0, 0};
static int tareaActual;
extern void conmutarContexto(contexto *, contexto *);
extern void tareaJava(int32_t);
palabraMáquina cederPlaca(void) {
    network_poll();
    int elementoListaElementoPrevio = tareaActual, elementoListaSiguiente = (elementoListaElementoPrevio + 1) % 3;
    while (elementoListaSiguiente != elementoListaElementoPrevio && !esEnEjecución[elementoListaSiguiente]) elementoListaSiguiente = (elementoListaSiguiente + 1) % 3;
    if (elementoListaSiguiente != elementoListaElementoPrevio) {
        for (unsigned índiceOrdinal = 0; índiceOrdinal < 2; índiceOrdinal++)
            if (esEnEjecución[índiceOrdinal + 1] && *(uint64_t *)pilas[índiceOrdinal] != 0x6b6f726f7373746bull)
                paradaFatalNúcleo("task stack guard");
        tareaActual = elementoListaSiguiente;
        conmutarContexto(&contextos[elementoListaElementoPrevio], &contextos[elementoListaSiguiente]);
    }
    return 0;
}
static void arranqueInicialTarea(void) {
    tareaJava(tareaActual);
    esEnEjecución[tareaActual] = 0;
    cederPlaca();
    paradaFatalNúcleo("finished task resumed");
}
palabraMáquina crearTareaPlaca(palabraMáquina valorIdentificador) {
    if (valorIdentificador < 1 || valorIdentificador > 2 || esEnEjecución[valorIdentificador]) return (uint32_t)-1;
    memset(&contextos[valorIdentificador], 0, sizeof(contexto));
    *(uint64_t *)pilas[valorIdentificador - 1] = 0x6b6f726f7373746bull;
    contextos[valorIdentificador].guardado[11] = (uintptr_t)arranqueInicialTarea;
    contextos[valorIdentificador].guardado[12] = (uintptr_t)(pilas[valorIdentificador - 1] + sizeof(pilas[0]));
    esEnEjecución[valorIdentificador] = 1;
    return 0;
}
palabraMáquina estadoValorTareaPlaca(palabraMáquina valorIdentificador) { return valorIdentificador < 3 ? esEnEjecución[valorIdentificador] : (uint32_t)-1; }
extern palabraMáquina buscarMemoriaCompilaciónAnticipada(palabraMáquina);
extern uint32_t leerEstadoValorUsuario(unsigned, unsigned);
extern unsigned char ExtremoSuperiorPila[];
palabraMáquina sistemaConsultarPlaca(palabraMáquina valorEntradaElemento, palabraMáquina número) {
    if (valorEntradaElemento==0) return unidadByteKibiMemoriaARM;
    if (valorEntradaElemento==1) return ((uintptr_t)ExtremoSuperiorPila-0x80000+1023)/1024;
    if (valorEntradaElemento==2 || valorEntradaElemento==3) return buscarMemoriaCompilaciónAnticipada(valorEntradaElemento==3);
    if (valorEntradaElemento==4) return listoPantalla ? (anchuraPantallaPlaca()*alturaPantallaPlaca()*4+1023)/1024 : 0;
    if (valorEntradaElemento==5) return 80*1024; /* ejecutarComando regiónDirección 16 MiB + 네 세션 preservarValor regiónDirección. */
    if (valorEntradaElemento>=20) return leerEstadoValorUsuario(valorEntradaElemento-20, número);
    return 0;
}
int *pk_errno_location(void) { static int errores[3]; return &errores[tareaActual]; }
