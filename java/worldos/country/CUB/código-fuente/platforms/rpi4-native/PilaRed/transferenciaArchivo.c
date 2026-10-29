#include "../denominación/nombresEnlazarMáquina.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "PilaRed.h"
#include "string.h"
#include "ABIArchivo.h"
extern uintptr_t milisegundosTranscurridosPlaca(void);
extern int32_t longitudEntradaElementoSistemaArchivosJava(int32_t), byteEntradaElementoSistemaArchivosJava(int32_t,int32_t), tamañoEntradaElementoSistemaArchivosJava(int32_t);
extern int32_t númeroElementosEntradaElementoSistemaArchivosJava(void);
static int recibirPuerto = -1, control = -1, conexiónManual = -1, Datos = -1;
static unsigned esEntranteRegistradoDiario, estadoCorrectoUsuario, tamañoLínea, incorrectoLínea, programaTerminarSesión, tareaEjecuciónEnCurso, capacidadUsado, númeroElementosEnviado, tieneFallido;
static unsigned tamañoRespuesta, enviadoRespuesta, númeroPuertoSiguiente;
static uint32_t actividad;
static char línea[256], respuestas[2048], nombreEntradaElementoArchivo[64], nombreTransferencia[64];
static unsigned char estadoValorTransferencia[16384];
static int igual(const char *valorPrimero, const char *valorSegundo) { while (*valorPrimero && *valorPrimero == *valorSegundo) { valorPrimero++; valorSegundo++; } return *valorPrimero == *valorSegundo; }
static void respuesta(const char *datosCadena) {
    size_t númeroElementosElementoLista = strlen(datosCadena);
    if (enviadoRespuesta) { memmove(respuestas, respuestas + enviadoRespuesta, tamañoRespuesta - enviadoRespuesta); tamañoRespuesta -= enviadoRespuesta; enviadoRespuesta = 0; }
    if (númeroElementosElementoLista > sizeof(respuestas) - tamañoRespuesta) { programaTerminarSesión = 1; return; }
    memcpy(respuestas + tamañoRespuesta, datosCadena, númeroElementosElementoLista); tamañoRespuesta += númeroElementosElementoLista;
}
static void valorNumérico(unsigned valor, char *datosResultado, unsigned *númeroElementosElementoLista) {
    char númeroElementosDígito[10]; unsigned númeroElementosEntradaElemento = 0;
    do { númeroElementosDígito[númeroElementosEntradaElemento++] = '0' + valor % 10; valor /= 10; } while (valor);
    while (númeroElementosEntradaElemento) datosResultado[(*númeroElementosElementoLista)++] = númeroElementosDígito[--númeroElementosEntradaElemento];
}
static void detenerTransferencia(void) {
    if (Datos >= 0) cerrarRed(Datos); if (conexiónManual >= 0) cerrarRed(conexiónManual);
    Datos = conexiónManual = -1; tareaEjecuciónEnCurso = capacidadUsado = númeroElementosEnviado = tieneFallido = 0;
}
static void desconectar(void) {
    detenerTransferencia(); if (control >= 0) cerrarRed(control); control = -1;
    esEntranteRegistradoDiario = estadoCorrectoUsuario = tamañoLínea = incorrectoLínea = tamañoRespuesta = enviadoRespuesta = programaTerminarSesión = 0;
}
int controlTransferenciaArchivo(int acción) {
    if (acción == 2) return recibirPuerto >= 0;
    if (acción == 0) { desconectar(); if (recibirPuerto >= 0) cerrarRed(recibirPuerto); recibirPuerto = -1; return 0; }
    if (acción != 1) return -22; if (recibirPuerto >= 0) return 0;
    recibirPuerto = crearExtremoConectorRed(1); if (recibirPuerto < 0) return recibirPuerto;
    int valorDevuelto = asociarRedCorta(recibirPuerto, leerEstadoRed(0,0), 21); if (!valorDevuelto) valorDevuelto = escucharRedCorta(recibirPuerto);
    if (valorDevuelto < 0) { cerrarRed(recibirPuerto); recibirPuerto = -1; } return valorDevuelto;
}
static int ruta(const char *nombre) {
    unsigned númeroElementosElementoLista = 0; if (*nombre == '/') nombre++;
    if (!*nombre || igual(nombre, ".") || igual(nombre, "..")) return 0;
    nombreEntradaElementoArchivo[númeroElementosElementoLista++] = '/';
    while (*nombre) {
        unsigned char códigoCarácter = *nombre++;
        if (númeroElementosElementoLista >= 63 || códigoCarácter < 32 || códigoCarácter == 127 || códigoCarácter == '/' || códigoCarácter == '\\') return 0;
        nombreEntradaElementoArchivo[númeroElementosElementoLista++] = códigoCarácter;
    }
    nombreEntradaElementoArchivo[númeroElementosElementoLista] = 0; return 1;
}
static void enviarLista(int detalle) {
    capacidadUsado = númeroElementosEnviado = 0;
    for (int índiceOrdinal = 0; índiceOrdinal < númeroElementosEntradaElementoSistemaArchivosJava(); índiceOrdinal++) {
        int númeroElementosElementoLista = longitudEntradaElementoSistemaArchivosJava(índiceOrdinal); if (númeroElementosElementoLista <= 0) continue;
        const char *partePrevio = detalle == 2 ? "type=file;size=" : detalle == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned númeroElementosEntradaElemento = strlen(partePrevio); memcpy(estadoValorTransferencia + capacidadUsado, partePrevio, númeroElementosEntradaElemento); capacidadUsado += númeroElementosEntradaElemento;
        if (detalle) valorNumérico(tamañoEntradaElementoSistemaArchivosJava(índiceOrdinal), (char *)estadoValorTransferencia, &capacidadUsado);
        const char *valorSufijo = detalle == 2 ? "; " : detalle == 1 ? " Jan 01 00:00 " : "";
        númeroElementosEntradaElemento = strlen(valorSufijo); memcpy(estadoValorTransferencia + capacidadUsado, valorSufijo, númeroElementosEntradaElemento); capacidadUsado += númeroElementosEntradaElemento;
        for (int ordinalInterior = 0; ordinalInterior < númeroElementosElementoLista; ordinalInterior++) estadoValorTransferencia[capacidadUsado++] = byteEntradaElementoSistemaArchivosJava(índiceOrdinal,ordinalInterior);
        estadoValorTransferencia[capacidadUsado++] = '\r'; estadoValorTransferencia[capacidadUsado++] = '\n';
    }
}
static void prepararConexiónManual(int ampliado) {
    if (tareaEjecuciónEnCurso) { respuesta("450 Transfer in progress\r\n"); return; }
    detenerTransferencia(); conexiónManual = crearExtremoConectorRed(1);
    if (conexiónManual >= 0) direcciónConectorRedReutilizar(conexiónManual);
    unsigned númeroPuerto = 50000 + númeroPuertoSiguiente++ % 8;
    if (conexiónManual < 0 || asociarRedCorta(conexiónManual, leerEstadoRed(0,0), númeroPuerto) || escucharRedCorta(conexiónManual)) {
        detenerTransferencia(); respuesta("425 Cannot open passive listener\r\n"); return;
    }
    char respuestaRetorno[96]; const char *partePrevio = ampliado ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned númeroElementosElementoLista = strlen(partePrevio); memcpy(respuestaRetorno, partePrevio, númeroElementosElementoLista);
    if (ampliado) { valorNumérico(númeroPuerto, respuestaRetorno, &númeroElementosElementoLista); respuestaRetorno[númeroElementosElementoLista++] = '|'; }
    else {
        uint32_t dirección=leerEstadoRed(0,0);
        for (int índicePosición=24;índicePosición>=0;índicePosición-=8) { valorNumérico((dirección>>índicePosición)&255,respuestaRetorno,&númeroElementosElementoLista);respuestaRetorno[númeroElementosElementoLista++]=','; }
        valorNumérico(númeroPuerto / 256, respuestaRetorno, &númeroElementosElementoLista); respuestaRetorno[númeroElementosElementoLista++] = ','; valorNumérico(númeroPuerto % 256, respuestaRetorno, &númeroElementosElementoLista);
    }
    respuestaRetorno[númeroElementosElementoLista++] = ')'; respuestaRetorno[númeroElementosElementoLista++] = '\r'; respuestaRetorno[númeroElementosElementoLista++] = '\n'; respuestaRetorno[númeroElementosElementoLista] = 0; respuesta(respuestaRetorno);
}
static void comando(void) {
    línea[tamañoLínea] = 0;
    char *argumentosAdicional = línea; while (*argumentosAdicional && *argumentosAdicional != ' ') { if (*argumentosAdicional >= 'a' && *argumentosAdicional <= 'z') *argumentosAdicional -= 32; argumentosAdicional++; }
    if (*argumentosAdicional) *argumentosAdicional++ = 0; while (*argumentosAdicional == ' ') argumentosAdicional++;
    if (igual(línea, "QUIT")) { detenerTransferencia(); respuesta("221 Goodbye\r\n"); programaTerminarSesión = 1; return; }
    if (igual(línea, "NOOP")) { respuesta("200 OK\r\n"); return; }
    if (igual(línea, "SYST")) { respuesta("215 UNIX Type: L8\r\n"); return; }
    if (igual(línea, "FEAT")) { respuesta("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (igual(línea, "USER")) { esEntranteRegistradoDiario = 0; estadoCorrectoUsuario = igual(argumentosAdicional, "anonymous") || igual(argumentosAdicional, "jkoros"); respuesta(estadoCorrectoUsuario ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (igual(línea, "PASS")) { esEntranteRegistradoDiario = estadoCorrectoUsuario; respuesta(esEntranteRegistradoDiario ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!esEntranteRegistradoDiario) { respuesta("530 Login first\r\n"); return; }
    if (igual(línea, "PWD")) respuesta("257 \"/\"\r\n");
    else if (igual(línea, "CWD")) respuesta(igual(argumentosAdicional, "/") || igual(argumentosAdicional, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (igual(línea, "TYPE")) respuesta(igual(argumentosAdicional, "I") || igual(argumentosAdicional, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (igual(línea, "OPTS")) respuesta(igual(argumentosAdicional, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (igual(línea, "PASV")) prepararConexiónManual(0);
    else if (igual(línea, "EPSV")) { if (*argumentosAdicional && !igual(argumentosAdicional, "1")) respuesta("522 IPv4 only\r\n"); else prepararConexiónManual(1); }
    else if (igual(línea, "ABOR")) { detenerTransferencia(); respuesta("226 Transfer aborted\r\n"); }
    else if (igual(línea, "DELE")) { respuesta(ruta(argumentosAdicional) && pk_unlink(nombreEntradaElementoArchivo) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (igual(línea, "LIST") || igual(línea, "NLST") || igual(línea, "MLSD")) {
        if (tareaEjecuciónEnCurso) { respuesta("450 Transfer in progress\r\n"); return; }
        if (conexiónManual < 0 && Datos < 0) { respuesta("425 Use PASV or EPSV\r\n"); return; }
        if (*argumentosAdicional && !igual(argumentosAdicional,"/") && !igual(argumentosAdicional,".") && !igual(argumentosAdicional,"-a") && !igual(argumentosAdicional,"-l") && !igual(argumentosAdicional,"-la")) { respuesta("550 Root listing only\r\n"); return; }
        enviarLista(igual(línea,"MLSD") ? 2 : igual(línea,"LIST") ? 1 : 0); tareaEjecuciónEnCurso = 2;
        respuesta("150 Opening directory listing\r\n");
    }
    else if (igual(línea, "SIZE")) {
        if (!ruta(argumentosAdicional)) { respuesta("550 Invalid filename\r\n"); return; }
        int manejadorArchivo = pk_open(nombreEntradaElementoArchivo, leerValorSolamente, 0); if (manejadorArchivo < 0) { respuesta("550 File unavailable\r\n"); return; }
        int tamaño = pk_size(manejadorArchivo); pk_close(manejadorArchivo); char respuestaRetorno[32] = "213 "; unsigned númeroElementosElementoLista = 4;
        valorNumérico(tamaño, respuestaRetorno, &númeroElementosElementoLista); respuestaRetorno[númeroElementosElementoLista++] = '\r'; respuestaRetorno[númeroElementosElementoLista++] = '\n'; respuestaRetorno[númeroElementosElementoLista] = 0; respuesta(respuestaRetorno);
    } else if (igual(línea, "STOR") || igual(línea, "RETR")) {
        if (tareaEjecuciónEnCurso) { respuesta("450 Transfer in progress\r\n"); return; }
        if (conexiónManual < 0 && Datos < 0) { respuesta("425 Use PASV or EPSV\r\n"); return; }
        if (!ruta(argumentosAdicional)) { respuesta("550 Invalid filename\r\n"); return; }
        tareaEjecuciónEnCurso = igual(línea, "STOR") ? 1 : 2; capacidadUsado = númeroElementosEnviado = tieneFallido = 0;
        memcpy(nombreTransferencia, nombreEntradaElementoArchivo, strlen(nombreEntradaElementoArchivo) + 1);
        if (tareaEjecuciónEnCurso == 2) {
            int manejadorArchivo = pk_open(nombreEntradaElementoArchivo, leerValorSolamente, 0);
            if (manejadorArchivo < 0) { tareaEjecuciónEnCurso = 0; respuesta("550 File unavailable\r\n"); return; }
            int númeroElementosElementoLista = pk_read(manejadorArchivo, estadoValorTransferencia, sizeof(estadoValorTransferencia)); pk_close(manejadorArchivo);
            if (númeroElementosElementoLista < 0) { tareaEjecuciónEnCurso = 0; respuesta("451 Read failed\r\n"); return; } capacidadUsado = númeroElementosElementoLista;
        }
        respuesta("150 Opening binary data connection\r\n");
    } else respuesta("502 Command not implemented\r\n");
}
void inspeccionarTransferenciaArchivo(void) {
    if (recibirPuerto < 0) return;
    int conexiónEntrando = aceptarRedCorta(recibirPuerto);
    if (conexiónEntrando >= 0) {
        if (control >= 0) { escribirRedCorta(conexiónEntrando, "421 One session at a time\r\n", 27); cerrarRed(conexiónEntrando); }
        else { control = conexiónEntrando; actividad = milisegundosTranscurridosPlaca(); respuesta("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (control < 0) return;
    if ((uint32_t)(milisegundosTranscurridosPlaca() - actividad) > 60000) { desconectar(); return; }
    if (!programaTerminarSesión) for (unsigned presupuesto = 0; presupuesto < 256; presupuesto++) {
        unsigned char códigoCarácter; int valorDevuelto = leerRedCorta(control, &códigoCarácter, 1);
        if (valorDevuelto == -11) break; if (valorDevuelto <= 0) { desconectar(); return; } actividad = milisegundosTranscurridosPlaca();
        if (códigoCarácter == '\n') { if (incorrectoLínea) respuesta("500 Command too long or invalid\r\n"); else comando(); tamañoLínea = incorrectoLínea = 0; if (programaTerminarSesión) break; }
        else if (códigoCarácter != '\r') { if (!códigoCarácter || tamañoLínea >= sizeof(línea) - 1) incorrectoLínea = 1; else línea[tamañoLínea++] = códigoCarácter; }
    }
    if (conexiónManual >= 0 && Datos < 0) {
        int valorDevuelto = aceptarRedCorta(conexiónManual);
        if (valorDevuelto >= 0) {
            if (direcciónParRedRedCorta(valorDevuelto) != direcciónParRedRedCorta(control)) cerrarRed(valorDevuelto);
            else { Datos = valorDevuelto; cerrarRed(conexiónManual); conexiónManual = -1; actividad = milisegundosTranscurridosPlaca(); }
        }
    }
    if (tareaEjecuciónEnCurso == 1 && Datos >= 0) for (unsigned presupuesto = 0; presupuesto < 8; presupuesto++) {
        unsigned char bloqueDatos[512]; int númeroElementosElementoLista = leerRedCorta(Datos, bloqueDatos, sizeof(bloqueDatos));
        if (númeroElementosElementoLista == -11) break;
        if (númeroElementosElementoLista < 0) { detenerTransferencia(); respuesta("426 Data connection failed\r\n"); break; }
        actividad = milisegundosTranscurridosPlaca();
        if (númeroElementosElementoLista == 0) {
            int resultado = -1;
            if (!tieneFallido) {
                int manejadorArchivo = pk_open(nombreTransferencia, escribirValorSolamente | AusenteSiCrear | ContenidoTruncar, 0600);
                if (manejadorArchivo >= 0) { resultado = pk_write(manejadorArchivo, estadoValorTransferencia, capacidadUsado); pk_close(manejadorArchivo); }
            }
            int esExitoso = !tieneFallido && resultado == (int)capacidadUsado; detenerTransferencia(); respuesta(esExitoso ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)númeroElementosElementoLista > sizeof(estadoValorTransferencia) - capacidadUsado) tieneFallido = 1;
        if (!tieneFallido) { memcpy(estadoValorTransferencia + capacidadUsado, bloqueDatos, númeroElementosElementoLista); capacidadUsado += númeroElementosElementoLista; }
    }
    if (tareaEjecuciónEnCurso == 2 && Datos >= 0) {
        int númeroElementosElementoLista = escribirRedCorta(Datos, estadoValorTransferencia + númeroElementosEnviado, capacidadUsado - númeroElementosEnviado);
        if (númeroElementosElementoLista >= 0) { númeroElementosEnviado += númeroElementosElementoLista; actividad = milisegundosTranscurridosPlaca(); if (númeroElementosEnviado == capacidadUsado) { detenerTransferencia(); respuesta("226 Transfer complete\r\n"); } }
        else if (númeroElementosElementoLista != -11) { detenerTransferencia(); respuesta("426 Data connection failed\r\n"); }
    }
    if (enviadoRespuesta < tamañoRespuesta) {
        int númeroElementosElementoLista = escribirRedCorta(control, respuestas + enviadoRespuesta, tamañoRespuesta - enviadoRespuesta);
        if (númeroElementosElementoLista > 0) enviadoRespuesta += númeroElementosElementoLista; else if (númeroElementosElementoLista != -11) { desconectar(); return; }
    }
    if (enviadoRespuesta == tamañoRespuesta) { tamañoRespuesta = enviadoRespuesta = 0; if (programaTerminarSesión) desconectar(); }
}
