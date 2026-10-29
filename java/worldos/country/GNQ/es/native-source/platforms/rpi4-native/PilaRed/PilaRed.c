#include "../denominación/nombresEnlazarMáquina.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "PilaRed.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../valorRemoto/valorRemoto.h"
#include "redCableado.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define registroMáquina(valorPrimero) (*(volatile uint32_t *)(uintptr_t)(valorPrimero))
#define dispositivoAuxiliar 0xfe215000ul
extern uintptr_t milisegundosTranscurridosPlaca(void);
static struct netif dispositivoConexión;
static int esPreparado, sondeo;
static int redCableadoUsar;
static unsigned recibirUso, recibirEscapar, recibirError;
static unsigned char recibirBúferDatos[1600];
static unsigned char datosTransmitir[32768];
static unsigned cabeceraLadoEmisión, númeroElementosLadoEmisión;
static uint32_t númeroElementosDatagramaRecibido, númeroElementosDatagramaEnviado, númeroElementosByteRecibido, númeroElementosByteEnviado, númeroElementosDatagramaDescartadosNúmero;
typedef struct {
    int categoríaTipo, recibirPuerto, esPendiente, conectado, finArchivo, error;
    struct tcp_pcb *controlConexión;
    struct udp_pcb *controlDatagrama;
    unsigned entradaElementoLadoDelantero, númeroElementosEntradaElemento;
    unsigned char Datos[4096];
    unsigned longitudes[4], puertos[4], númeroExtremoParRed;
    uint32_t direcciones[4], direcciónParRed;
} extremoConectorRed;
static extremoConectorRed extremosConectorRed[32];
u32_t sys_now(void) { return (u32_t)milisegundosTranscurridosPlaca(); }
static int númeroError(err_t entradaElementoAuxiliar) {
    return entradaElementoAuxiliar == ERR_MEM || entradaElementoAuxiliar == ERR_BUF || entradaElementoAuxiliar == ERR_WOULDBLOCK ? -11 : entradaElementoAuxiliar == ERR_USE ? -98 :
        entradaElementoAuxiliar == ERR_RTE ? -101 : entradaElementoAuxiliar == ERR_RST ? -104 : entradaElementoAuxiliar == ERR_CONN ? -107 : entradaElementoAuxiliar == ERR_TIMEOUT ? -110 : -5;
}
static extremoConectorRed *obtenerValor(int manejadorArchivo) { return manejadorArchivo >= 0 && manejadorArchivo < 32 && extremosConectorRed[manejadorArchivo].categoríaTipo ? &extremosConectorRed[manejadorArchivo] : 0; }
static int reservar(int categoríaTipo) {
    for (int índiceOrdinal = 0; índiceOrdinal < 32; ++índiceOrdinal) if (!extremosConectorRed[índiceOrdinal].categoríaTipo) {
        memset(&extremosConectorRed[índiceOrdinal], 0, sizeof(extremoConectorRed)); extremosConectorRed[índiceOrdinal].categoríaTipo = categoríaTipo; extremosConectorRed[índiceOrdinal].esPendiente = -1; return índiceOrdinal;
    }
    return -24;
}
static void emitirValor(unsigned códigoCarácter) { datosTransmitir[(cabeceraLadoEmisión + númeroElementosLadoEmisión++) % sizeof(datosTransmitir)] = códigoCarácter; }
static err_t salida(struct netif *númeroElementosElementoLista, struct pbuf *posiciónDatos, const ip4_addr_t *dirección) {
    (void)númeroElementosElementoLista; (void)dirección;
    if (posiciónDatos->tot_len > 1500 || númeroElementosLadoEmisión + 2 * posiciónDatos->tot_len + 2 > sizeof(datosTransmitir)) return ERR_MEM;
    emitirValor(192);
    for (struct pbuf *desfaseSiguiente = posiciónDatos; desfaseSiguiente; desfaseSiguiente = desfaseSiguiente->next) for (unsigned índiceOrdinal = 0; índiceOrdinal < desfaseSiguiente->len; índiceOrdinal++) {
        unsigned códigoCarácter = ((unsigned char *)desfaseSiguiente->payload)[índiceOrdinal];
        if (códigoCarácter == 192 || códigoCarácter == 219) { emitirValor(219); emitirValor(códigoCarácter == 192 ? 220 : 221); } else emitirValor(códigoCarácter);
    }
    emitirValor(192); númeroElementosDatagramaEnviado++; númeroElementosByteEnviado += posiciónDatos->tot_len; return ERR_OK;
}
static err_t prepararEntornoEjecución(struct netif *númeroElementosElementoLista) { númeroElementosElementoLista->name[0] = 's'; númeroElementosElementoLista->name[1] = 'l'; númeroElementosElementoLista->mtu = 1500; númeroElementosElementoLista->output = salida; return ERR_OK; }
void prepararRed(void) {
    if (esPreparado) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    registroMáquina(dispositivoAuxiliar + 4) |= 1; registroMáquina(dispositivoAuxiliar + 0x60) = 0; registroMáquina(dispositivoAuxiliar + 0x44) = 0;
    registroMáquina(dispositivoAuxiliar + 0x48) = 0xc6; registroMáquina(dispositivoAuxiliar + 0x4c) = 3; registroMáquina(dispositivoAuxiliar + 0x68) = 270; registroMáquina(dispositivoAuxiliar + 0x60) = 3;
    lwip_init();
    ip4_addr_t DirecciónInternet, máscaraBit, direcciónPasarela;
    redCableadoUsar=tieneDispositivoCableado();
    ip4_addr_set_u32(&DirecciónInternet, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&máscaraBit, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&direcciónPasarela, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&dispositivoConexión, &DirecciónInternet, &máscaraBit, &direcciónPasarela, 0, redCableadoUsar?prepararRedCableado:prepararEntornoEjecución, redCableadoUsar?ethernet_input:ip4_input))return;
    netif_set_default(&dispositivoConexión); netif_set_up(&dispositivoConexión);if(!redCableadoUsar)netif_set_link_up(&dispositivoConexión); esPreparado = 1;
    prepararRemoto();
}
static err_t tieneRecibido(void *argumentosAdicional, struct tcp_pcb *bloqueControlTransmisión, struct pbuf *posiciónDatos, err_t error) {
    extremoConectorRed *datosCadena = argumentosAdicional; (void)bloqueControlTransmisión; (void)error;
    if (!posiciónDatos) { datosCadena->finArchivo = 1; return ERR_OK; }
    if (posiciónDatos->tot_len > sizeof(datosCadena->Datos) - datosCadena->númeroElementosEntradaElemento) return ERR_MEM;
    unsigned posiciónActual = (datosCadena->entradaElementoLadoDelantero + datosCadena->númeroElementosEntradaElemento) % sizeof(datosCadena->Datos);
    for (struct pbuf *desfaseSiguiente = posiciónDatos; desfaseSiguiente; desfaseSiguiente = desfaseSiguiente->next) for (unsigned índiceOrdinal = 0; índiceOrdinal < desfaseSiguiente->len; índiceOrdinal++) {
        datosCadena->Datos[posiciónActual] = ((unsigned char *)desfaseSiguiente->payload)[índiceOrdinal]; posiciónActual = (posiciónActual + 1) % sizeof(datosCadena->Datos);
    }
    datosCadena->númeroElementosEntradaElemento += posiciónDatos->tot_len; pbuf_free(posiciónDatos); return ERR_OK;
}
static void tieneFallido(void *argumentosAdicional, err_t error) { extremoConectorRed *datosCadena = argumentosAdicional; datosCadena->controlConexión = 0; datosCadena->error = númeroError(error); }
static void retrollamadas(extremoConectorRed *datosCadena) { tcp_arg(datosCadena->controlConexión, datosCadena); tcp_recv(datosCadena->controlConexión, tieneRecibido); tcp_err(datosCadena->controlConexión, tieneFallido); }
static err_t conectado(void *argumentosAdicional, struct tcp_pcb *bloqueControlTransmisión, err_t error) {
    extremoConectorRed *datosCadena = argumentosAdicional; (void)bloqueControlTransmisión; if (error) datosCadena->error = númeroError(error); else datosCadena->conectado = 1; return ERR_OK;
}
static err_t aceptado(void *argumentosAdicional, struct tcp_pcb *bloqueControlTransmisión, err_t error) {
    extremoConectorRed *padre = argumentosAdicional; if (error) return error;
    int manejadorArchivo = reservar(1); if (manejadorArchivo < 0) return ERR_MEM;
    extremoConectorRed *datosCadena = &extremosConectorRed[manejadorArchivo]; datosCadena->controlConexión = bloqueControlTransmisión; datosCadena->conectado = 1; datosCadena->esPendiente = (int)(padre - extremosConectorRed);
    datosCadena->direcciónParRed = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&bloqueControlTransmisión->remote_ip))); datosCadena->númeroExtremoParRed = bloqueControlTransmisión->remote_port;
    retrollamadas(datosCadena); return ERR_OK;
}
static void datagrama(void *argumentosAdicional, struct udp_pcb *bloqueControlTransmisión, struct pbuf *posiciónDatos, const ip_addr_t *dirección, u16_t númeroPuerto) {
    extremoConectorRed *datosCadena = argumentosAdicional; (void)bloqueControlTransmisión;
    if (datosCadena->númeroElementosEntradaElemento < 4 && posiciónDatos->tot_len <= 512) {
        unsigned índicePosición = (datosCadena->entradaElementoLadoDelantero + datosCadena->númeroElementosEntradaElemento) % 4;
        pbuf_copy_partial(posiciónDatos, datosCadena->Datos + índicePosición * 512, posiciónDatos->tot_len, 0);
        datosCadena->longitudes[índicePosición] = posiciónDatos->tot_len; datosCadena->puertos[índicePosición] = númeroPuerto;
        datosCadena->direcciones[índicePosición] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(dirección))); datosCadena->númeroElementosEntradaElemento++;
    }
    pbuf_free(posiciónDatos);
}
int crearExtremoConectorRed(int categoríaTipo) {
    if (!esPreparado) return -100;
    if (categoríaTipo != 1 && categoríaTipo != 2) return -93;
    int manejadorArchivo = reservar(categoríaTipo); if (manejadorArchivo < 0) return manejadorArchivo;
    extremoConectorRed *datosCadena = &extremosConectorRed[manejadorArchivo];
    if (categoríaTipo == 1) { datosCadena->controlConexión = tcp_new(); if (datosCadena->controlConexión) retrollamadas(datosCadena); }
    else { datosCadena->controlDatagrama = udp_new(); if (datosCadena->controlDatagrama) udp_recv(datosCadena->controlDatagrama, datagrama, datosCadena); }
    if (!datosCadena->controlConexión && !datosCadena->controlDatagrama) { datosCadena->categoríaTipo = 0; return -12; } return manejadorArchivo;
}
int asociarRedCorta(int manejadorArchivo, uint32_t dirección, unsigned númeroPuerto) {
    extremoConectorRed *datosCadena = obtenerValor(manejadorArchivo); if (!datosCadena) return -9;
    if (númeroPuerto > 65535 || (dirección && dirección != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&dispositivoConexión))) && dirección != 0x7f000001)) return -99;
    ip_addr_t DirecciónInternet; ip_addr_set_ip4_u32(&DirecciónInternet, lwip_htonl(dirección));
    err_t entradaElementoAuxiliar = datosCadena->categoríaTipo == 1 ? tcp_bind(datosCadena->controlConexión, &DirecciónInternet, númeroPuerto) : udp_bind(datosCadena->controlDatagrama, &DirecciónInternet, númeroPuerto); return entradaElementoAuxiliar ? númeroError(entradaElementoAuxiliar) : 0;
}
void direcciónConectorRedReutilizar(int manejadorArchivo) { extremoConectorRed *datosCadena = obtenerValor(manejadorArchivo); if (datosCadena && datosCadena->controlConexión) ip_set_option(datosCadena->controlConexión, SOF_REUSEADDR); }
int escucharRedCorta(int manejadorArchivo) {
    extremoConectorRed *datosCadena = obtenerValor(manejadorArchivo); if (!datosCadena || datosCadena->categoríaTipo != 1) return -9;
    if (datosCadena->recibirPuerto) return 0;
    err_t entradaElementoAuxiliar; struct tcp_pcb *bloqueControlTransmisión = tcp_listen_with_backlog_and_err(datosCadena->controlConexión, 4, &entradaElementoAuxiliar);
    if (!bloqueControlTransmisión) return númeroError(entradaElementoAuxiliar); datosCadena->controlConexión = bloqueControlTransmisión; datosCadena->recibirPuerto = 1; tcp_arg(bloqueControlTransmisión, datosCadena); tcp_accept(bloqueControlTransmisión, aceptado); return 0;
}
int conectarRedCorta(int manejadorArchivo, uint32_t dirección, unsigned númeroPuerto) {
    extremoConectorRed *datosCadena = obtenerValor(manejadorArchivo); if (!datosCadena || datosCadena->categoríaTipo != 1) return -9;
    if (datosCadena->error) return datosCadena->error;
    if (datosCadena->conectado) return 0;
    if (datosCadena->númeroExtremoParRed) return -115;
    if (!númeroPuerto || númeroPuerto > 65535 || !dirección) return -22;
    ip_addr_t DirecciónInternet; ip_addr_set_ip4_u32(&DirecciónInternet, lwip_htonl(dirección));
    datosCadena->direcciónParRed = dirección; datosCadena->númeroExtremoParRed = númeroPuerto;
    err_t entradaElementoAuxiliar = tcp_connect(datosCadena->controlConexión, &DirecciónInternet, númeroPuerto, conectado); return entradaElementoAuxiliar ? númeroError(entradaElementoAuxiliar) : -115;
}
int aceptarRedCorta(int manejadorArchivo) {
    extremoConectorRed *datosCadena = obtenerValor(manejadorArchivo); if (!datosCadena || !datosCadena->recibirPuerto) return -22;
    for (int índiceOrdinal = 0; índiceOrdinal < 32; índiceOrdinal++) if (extremosConectorRed[índiceOrdinal].categoríaTipo == 1 && extremosConectorRed[índiceOrdinal].esPendiente == manejadorArchivo) { extremosConectorRed[índiceOrdinal].esPendiente = -1; return índiceOrdinal; }
    return -11;
}
int leerRedCorta(int manejadorArchivo, void *Datos, unsigned númeroElementosElementoLista) {
    extremoConectorRed *datosCadena = obtenerValor(manejadorArchivo); if (!datosCadena || datosCadena->categoríaTipo != 1) return -9;
    if (!númeroElementosElementoLista) return 0; if (!datosCadena->númeroElementosEntradaElemento) return datosCadena->error ? datosCadena->error : datosCadena->finArchivo ? 0 : -11;
    if (númeroElementosElementoLista > datosCadena->númeroElementosEntradaElemento) númeroElementosElementoLista = datosCadena->númeroElementosEntradaElemento;
    for (unsigned índiceOrdinal = 0; índiceOrdinal < númeroElementosElementoLista; índiceOrdinal++) { ((unsigned char *)Datos)[índiceOrdinal] = datosCadena->Datos[datosCadena->entradaElementoLadoDelantero]; datosCadena->entradaElementoLadoDelantero = (datosCadena->entradaElementoLadoDelantero + 1) % sizeof(datosCadena->Datos); }
    datosCadena->númeroElementosEntradaElemento -= númeroElementosElementoLista; if (datosCadena->controlConexión) tcp_recved(datosCadena->controlConexión, númeroElementosElementoLista); return númeroElementosElementoLista;
}
int escribirRedCorta(int manejadorArchivo, const void *Datos, unsigned númeroElementosElementoLista) {
    extremoConectorRed *datosCadena = obtenerValor(manejadorArchivo); if (!datosCadena || datosCadena->categoríaTipo != 1) return -9;
    if (datosCadena->error) return datosCadena->error; if (!datosCadena->controlConexión || !datosCadena->conectado) return -107;
    if (!númeroElementosElementoLista) return 0; if (númeroElementosElementoLista > tcp_sndbuf(datosCadena->controlConexión)) númeroElementosElementoLista = tcp_sndbuf(datosCadena->controlConexión);
    if (!númeroElementosElementoLista) return -11; if (númeroElementosElementoLista > 1024) númeroElementosElementoLista = 1024;
    err_t entradaElementoAuxiliar = tcp_write(datosCadena->controlConexión, Datos, númeroElementosElementoLista, TCP_WRITE_FLAG_COPY); if (entradaElementoAuxiliar) return númeroError(entradaElementoAuxiliar);
    tcp_output(datosCadena->controlConexión); return númeroElementosElementoLista;
}
int enviarDatagrama(int manejadorArchivo, const void *Datos, unsigned númeroElementosElementoLista, uint32_t dirección, unsigned númeroPuerto) {
    extremoConectorRed *datosCadena = obtenerValor(manejadorArchivo); if (!datosCadena || datosCadena->categoríaTipo != 2) return -9;
    if (númeroElementosElementoLista > 512) return -90; if (!númeroPuerto || númeroPuerto > 65535) return -22;
    struct pbuf *posiciónDatos = pbuf_alloc(PBUF_TRANSPORT, númeroElementosElementoLista, PBUF_RAM); if (!posiciónDatos) return -11;
    pbuf_take(posiciónDatos, Datos, númeroElementosElementoLista); ip_addr_t DirecciónInternet; ip_addr_set_ip4_u32(&DirecciónInternet, lwip_htonl(dirección));
    err_t entradaElementoAuxiliar = udp_sendto(datosCadena->controlDatagrama, posiciónDatos, &DirecciónInternet, númeroPuerto); pbuf_free(posiciónDatos); return entradaElementoAuxiliar ? númeroError(entradaElementoAuxiliar) : (int)númeroElementosElementoLista;
}
int recibirDatagrama(int manejadorArchivo, void *Datos, unsigned númeroElementosElementoLista) {
    extremoConectorRed *datosCadena = obtenerValor(manejadorArchivo); if (!datosCadena || datosCadena->categoríaTipo != 2) return -9;
    if (!datosCadena->númeroElementosEntradaElemento) return -11; unsigned posiciónActual = datosCadena->entradaElementoLadoDelantero;
    if (númeroElementosElementoLista > datosCadena->longitudes[posiciónActual]) númeroElementosElementoLista = datosCadena->longitudes[posiciónActual]; memcpy(Datos, datosCadena->Datos + posiciónActual * 512, númeroElementosElementoLista);
    datosCadena->númeroExtremoParRed = datosCadena->puertos[posiciónActual]; datosCadena->direcciónParRed = datosCadena->direcciones[posiciónActual]; datosCadena->entradaElementoLadoDelantero = (posiciónActual + 1) % 4; datosCadena->númeroElementosEntradaElemento--; return númeroElementosElementoLista;
}
unsigned númeroPuertoRed(int manejadorArchivo) { extremoConectorRed *datosCadena = obtenerValor(manejadorArchivo); return !datosCadena ? 0 : datosCadena->controlConexión ? datosCadena->controlConexión->local_port : datosCadena->controlDatagrama ? datosCadena->controlDatagrama->local_port : 0; }
unsigned númeroPuertoParRed(int manejadorArchivo) { extremoConectorRed *datosCadena = obtenerValor(manejadorArchivo); return datosCadena ? datosCadena->númeroExtremoParRed : 0; }
uint32_t direcciónParRedRedCorta(int manejadorArchivo) { extremoConectorRed *datosCadena = obtenerValor(manejadorArchivo); return datosCadena ? datosCadena->direcciónParRed : 0; }
void cerrarRed(int manejadorArchivo) {
    extremoConectorRed *datosCadena = obtenerValor(manejadorArchivo); if (!datosCadena) return;
    if (datosCadena->recibirPuerto) for (int índiceOrdinal = 0; índiceOrdinal < 32; ++índiceOrdinal) if (extremosConectorRed[índiceOrdinal].categoríaTipo && extremosConectorRed[índiceOrdinal].esPendiente == manejadorArchivo) cerrarRed(índiceOrdinal);
    if (datosCadena->controlConexión) {
        tcp_arg(datosCadena->controlConexión, 0); if (datosCadena->recibirPuerto) tcp_accept(datosCadena->controlConexión, 0); else { tcp_recv(datosCadena->controlConexión, 0); tcp_err(datosCadena->controlConexión, 0); }
        if (tcp_close(datosCadena->controlConexión) != ERR_OK) tcp_abort(datosCadena->controlConexión);
    }
    if (datosCadena->controlDatagrama) udp_remove(datosCadena->controlDatagrama); datosCadena->categoríaTipo = 0;
}
void inspeccionarRed(void) {
    if (!esPreparado || sondeo) return; sondeo = 1;
    if(redCableadoUsar)inspeccionarRedCableado(&dispositivoConexión);
    for (unsigned presupuesto = 0; !redCableadoUsar && presupuesto < 4096 && (registroMáquina(dispositivoAuxiliar + 0x54) & 1); presupuesto++) {
        unsigned códigoCarácter = registroMáquina(dispositivoAuxiliar + 0x40) & 255;
        if (códigoCarácter == 192) {
            if (recibirUso && !recibirError && !recibirEscapar) {
                struct pbuf *posiciónDatos = pbuf_alloc(PBUF_RAW, recibirUso, PBUF_POOL);
                if (posiciónDatos) { númeroElementosDatagramaRecibido++; númeroElementosByteRecibido += recibirUso; pbuf_take(posiciónDatos, recibirBúferDatos, recibirUso); if (dispositivoConexión.input(posiciónDatos, &dispositivoConexión) != ERR_OK) { númeroElementosDatagramaDescartadosNúmero++; pbuf_free(posiciónDatos); } }
                else númeroElementosDatagramaDescartadosNúmero++;
            }
            else if (recibirUso) númeroElementosDatagramaDescartadosNúmero++;
            recibirUso = recibirError = recibirEscapar = 0;
        } else if (códigoCarácter == 219 && !recibirEscapar) recibirEscapar = 1;
        else {
            if (recibirEscapar) { if (códigoCarácter != 220 && códigoCarácter != 221) recibirError = 1; códigoCarácter = códigoCarácter == 220 ? 192 : 219; recibirEscapar = 0; }
            if (recibirUso < sizeof(recibirBúferDatos)) recibirBúferDatos[recibirUso++] = códigoCarácter; else recibirError = 1;
        }
    }
    netif_poll(&dispositivoConexión); sys_check_timeouts(); inspeccionarTransferenciaArchivo(); inspeccionarRemoto();
    for (unsigned presupuesto = 0; presupuesto < 4096 && númeroElementosLadoEmisión && (registroMáquina(dispositivoAuxiliar + 0x54) & 0x20); presupuesto++) {
        registroMáquina(dispositivoAuxiliar + 0x40) = datosTransmitir[cabeceraLadoEmisión]; cabeceraLadoEmisión = (cabeceraLadoEmisión + 1) % sizeof(datosTransmitir); númeroElementosLadoEmisión--;
    }
    sondeo = 0;
}

/* ajustes·조회는 lwIP의 datosEfectivo 인터페이스와 puntoFin 표를 사용한다. */
uint32_t leerEstadoRed(unsigned valorEntradaElemento, unsigned número) {
    if(valorEntradaElemento==20)return redCableadoUsar;
    if(valorEntradaElemento==21)return esPreparado&&netif_is_link_up(&dispositivoConexión);
    if(valorEntradaElemento==22)return redCableadoUsar?estadísticasRedCableado(5):0;
    if (!esPreparado) return 0;
    if(redCableadoUsar&&valorEntradaElemento>=4&&valorEntradaElemento<=8)return estadísticasRedCableado(valorEntradaElemento-4);
    if (valorEntradaElemento == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&dispositivoConexión)));
    if (valorEntradaElemento == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&dispositivoConexión)));
    if (valorEntradaElemento == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&dispositivoConexión)));
    if (valorEntradaElemento == 3) return netif_is_up(&dispositivoConexión) != 0;
    if (valorEntradaElemento == 4) return númeroElementosDatagramaRecibido;
    if (valorEntradaElemento == 5) return númeroElementosDatagramaEnviado;
    if (valorEntradaElemento == 6) return númeroElementosByteRecibido;
    if (valorEntradaElemento == 7) return númeroElementosByteEnviado;
    if (valorEntradaElemento == 8) return númeroElementosDatagramaDescartadosNúmero;
    if (valorEntradaElemento == 9) return númeroElementosLadoEmisión;
    if (número >= 32) return 0;
    extremoConectorRed *puntoFin = &extremosConectorRed[número];
    if (valorEntradaElemento == 10) return puntoFin->categoríaTipo;
    if (!puntoFin->categoríaTipo) return 0;
    if (valorEntradaElemento == 11) return númeroPuertoRed(número);
    if (valorEntradaElemento == 12) return puntoFin->direcciónParRed;
    if (valorEntradaElemento == 13) return puntoFin->númeroExtremoParRed;
    if (valorEntradaElemento == 14) return puntoFin->recibirPuerto ? 1 : puntoFin->finArchivo ? 3 : puntoFin->error ? 4 : puntoFin->conectado ? 2 : 0;
    if (valorEntradaElemento == 15) return puntoFin->númeroElementosEntradaElemento;
    if (valorEntradaElemento == 16) {
        const ip_addr_t *dirección = puntoFin->categoríaTipo == 1 && puntoFin->controlConexión ? &puntoFin->controlConexión->local_ip :
            puntoFin->categoríaTipo == 2 && puntoFin->controlDatagrama ? &puntoFin->controlDatagrama->local_ip : 0;
        return dirección ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(dirección))) : 0;
    }
    return 0;
}

int configurarRed(unsigned acción, uint32_t dirección, uint32_t valorMáscara, uint32_t valorPasarela) {
    if (!esPreparado) return -100;
    if (acción == 1) { netif_set_up(&dispositivoConexión); return 0; }
    if (acción == 2) { netif_set_down(&dispositivoConexión); return 0; }
    if (acción != 0) return -22;
    /* 유니캐스트 IPv4, casosConmutarDenso valorMáscara, 같은 망의 선택적 valorPredeterminado valorPasarela. */
    uint32_t máscaraInvertido = ~valorMáscara;
    if (!valorMáscara || (máscaraInvertido & (máscaraInvertido + 1)) || !dirección || (dirección >> 24) == 127 ||
        (dirección >> 24) == 0 || (dirección >> 28) >= 14 ||
        (máscaraInvertido > 1 && (!(dirección & máscaraInvertido) || (dirección & máscaraInvertido) == máscaraInvertido)) ||
        (valorPasarela && ((valorPasarela & valorMáscara) != (dirección & valorMáscara) || valorPasarela == dirección || (valorPasarela >> 28) >= 14 ||
         (máscaraInvertido > 1 && (!(valorPasarela & máscaraInvertido) || (valorPasarela & máscaraInvertido) == máscaraInvertido))))) return -22;
    /* 기존 연결을 dirección 변경으로 몰래 끊지 않는다. */
    for (unsigned número = 0; número < 32; número++) if (extremosConectorRed[número].categoríaTipo &&
        !(extremosConectorRed[número].recibirPuerto && extremosConectorRed[número].controlConexión && ip_addr_isany(&extremosConectorRed[número].controlConexión->local_ip))) return -16;
    if(redCableadoUsar)dhcp_stop(&dispositivoConexión);
    ip4_addr_t direcciónNuevo, máscaraNuevo, valorPasarelaNuevo;
    ip4_addr_set_u32(&direcciónNuevo, lwip_htonl(dirección)); ip4_addr_set_u32(&máscaraNuevo, lwip_htonl(valorMáscara)); ip4_addr_set_u32(&valorPasarelaNuevo, lwip_htonl(valorPasarela));
    netif_set_addr(&dispositivoConexión, &direcciónNuevo, &máscaraNuevo, &valorPasarelaNuevo);
    return 0;
}

static struct raw_pcb *extremoRespuestaRetorno;
static uint32_t pruebaDirección, pruebaTiempo, tiempoRespuestaRetorno;
static unsigned pruebaSecuencia, pruebaIdentificador, secuenciaRespuestaRetorno;
static int estadoValorRespuestaRetorno;
static u8_t tieneRespuestaRetorno(void *argumentos, struct raw_pcb *puntoFin, struct pbuf *Datos, const ip_addr_t *dirección) {
    (void)argumentos; (void)puntoFin;
    unsigned char valorCabecera[20], respuesta[16];
    if (estadoValorRespuestaRetorno != -11 || Datos->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(dirección))) != pruebaDirección || pbuf_copy_partial(Datos, valorCabecera, 20, 0) != 20) return 0;
    unsigned tamañoEncabezado = (valorCabecera[0] & 15) * 4;
    if ((valorCabecera[0] >> 4) != 4 || tamañoEncabezado < 20 || Datos->tot_len < tamañoEncabezado + 16 ||
        pbuf_copy_partial(Datos, respuesta, 16, tamañoEncabezado) != 16 || respuesta[0] || respuesta[1] ||
        (((unsigned)respuesta[4] << 8) | respuesta[5]) != pruebaIdentificador ||
        (((unsigned)respuesta[6] << 8) | respuesta[7]) != pruebaSecuencia ||
        respuesta[8] != 'J' || respuesta[9] != 'K' || respuesta[10] != 'O' || respuesta[11] != 'S' ||
        (((uint32_t)respuesta[12] << 24) | ((uint32_t)respuesta[13] << 16) | ((uint32_t)respuesta[14] << 8) | respuesta[15]) != pruebaTiempo) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(Datos, tamañoEncabezado)) return 0;
    if (inet_chksum_pbuf(Datos)) { pbuf_add_header(Datos, tamañoEncabezado); return 0; }
    tiempoRespuestaRetorno = (uint32_t)milisegundosTranscurridosPlaca() - pruebaTiempo; secuenciaRespuestaRetorno = valorCabecera[8]; estadoValorRespuestaRetorno = 0;
    pbuf_free(Datos); return 1;
}
int iniciarPruebaRespuestaRetorno(uint32_t dirección, unsigned valorOrden) {
    if (!esPreparado || !netif_is_up(&dispositivoConexión)) return -100;
    if (!dirección || (dirección >> 28) >= 14 || dirección == 0xffffffffu) return -22;
    if (!extremoRespuestaRetorno) { extremoRespuestaRetorno = raw_new(IP_PROTO_ICMP); if (!extremoRespuestaRetorno) return -12; raw_recv(extremoRespuestaRetorno, tieneRespuestaRetorno, 0); }
    pruebaDirección = dirección; pruebaSecuencia = valorOrden & 65535; pruebaIdentificador = (pruebaIdentificador + 1) & 65535;
    pruebaTiempo = milisegundosTranscurridosPlaca(); estadoValorRespuestaRetorno = -11; tiempoRespuestaRetorno = secuenciaRespuestaRetorno = 0;
    unsigned char Datos[32] = {8,0,0,0};
    Datos[4] = pruebaIdentificador >> 8; Datos[5] = pruebaIdentificador; Datos[6] = pruebaSecuencia >> 8; Datos[7] = pruebaSecuencia;
    Datos[8]='J'; Datos[9]='K'; Datos[10]='O'; Datos[11]='S';
    Datos[12]=pruebaTiempo >> 24; Datos[13]=pruebaTiempo >> 16; Datos[14]=pruebaTiempo >> 8; Datos[15]=pruebaTiempo;
    for (unsigned índicePosición = 16; índicePosición < sizeof(Datos); índicePosición++) Datos[índicePosición] = índicePosición;
    uint16_t sumaComprobaciónVerificación = inet_chksum(Datos, sizeof(Datos)); memcpy(Datos + 2, &sumaComprobaciónVerificación, 2);
    struct pbuf *datagrama = pbuf_alloc(PBUF_IP, sizeof(Datos), PBUF_RAM); if (!datagrama) return -12;
    pbuf_take(datagrama, Datos, sizeof(Datos)); ip_addr_t extremoDestino; ip_addr_set_ip4_u32(&extremoDestino, lwip_htonl(dirección));
    err_t valorProcesado = raw_sendto(extremoRespuestaRetorno, datagrama, &extremoDestino); pbuf_free(datagrama);
    if (valorProcesado) estadoValorRespuestaRetorno = númeroError(valorProcesado);
    return valorProcesado ? estadoValorRespuestaRetorno : 0;
}
int leerPruebaRespuestaRetorno(unsigned valorEntradaElemento) {
    inspeccionarRed();
    return valorEntradaElemento == 0 ? estadoValorRespuestaRetorno : valorEntradaElemento == 1 ? (int)tiempoRespuestaRetorno : valorEntradaElemento == 2 ? (int)secuenciaRespuestaRetorno : -22;
}
