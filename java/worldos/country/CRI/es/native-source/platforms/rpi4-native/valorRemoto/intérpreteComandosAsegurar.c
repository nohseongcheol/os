/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "valorRemoto.h"
#include "soporteCriptografía.h"
#include "perfil.h"
#include "../PilaRed/PilaRed.h"
/* The allocator/PRNG module descriptors are part of this pinned port's ABI. */
#define ASSH_PV
#include <assh/assh_session.h>
#include <assh/assh_context.h>
#include <assh/assh_service.h>
#include <assh/assh_transport.h>
#include <assh/assh_userauth_server.h>
#include <assh/assh_connection.h>
#include <assh/assh_kex.h>
#include <assh/assh_key.h>
#include <assh/assh_sign.h>
#include <assh/assh_cipher.h>
#include <assh/assh_mac.h>
#include <assh/assh_compress.h>
#include <assh/assh_alloc.h>
#include <assh/assh_prng.h>
#include <assh/mod_builtin.h>
#include <assh/assh_event.h>
#include <string.h>
extern uintptr_t milisegundosTranscurridosPlaca(void);
extern uintptr_t escribirCarácterPlaca(uintptr_t);
static struct assh_context_s *valorContexto;
static struct assh_session_s *conexión;
static struct assh_channel_s *entradaElementoCanal;
static int extremoEscuchaEnCurso=-1,valorParRed=-1,esAutenticado,iniciadoIntérpreteComandos,tipoComando,estadoValorFin=-1,futuroCerrar,errorInicioSistema,esperaEnCursoIntérpreteComandos;
static uintptr_t tiempoConexión,tiempoReconectar,tiempoCierreEnCurso;
static unsigned char líneaEntrada[8192],líneaSalida[65536];
static unsigned cabeceraEntrada,númeroElementosEntrada,cabeceraSalida,númeroElementosSalida,salidaElementoPrevio;
static void valorDiagnóstico(const char *textoPalabra,unsigned valor) {
    while(*textoPalabra)escribirCarácterPlaca(*textoPalabra++);
    char valorDígito[12];unsigned númeroValor=0;do{valorDígito[númeroValor++]='0'+valor%10;valor/=10;}while(valor);
    while(númeroValor)escribirCarácterPlaca(valorDígito[--númeroValor]);escribirCarácterPlaca(10);
}
static assh_status_t prepararMemoria(void *Datos,void **dirección,size_t tamaño,enum assh_alloc_type_e valorClaseTipo) {
    (void)Datos;(void)valorClaseTipo;
    if(!tamaño){liberarRemoto(*dirección);*dirección=0;return ASSH_OK;}
    void *direcciónNuevo=reasignarRemoto(*dirección,tamaño);
    if(!direcciónNuevo)return ASSH_ERR_MEM;*dirección=direcciónNuevo;return ASSH_OK;
}
static assh_status_t prepararAleatorio(struct assh_context_s *Datos,const struct assh_buffer_s *valorSemilla) {
    (void)Datos;(void)valorSemilla;unsigned char Pruebas[32];int resultado=aleatorioRemoto(Pruebas,sizeof(Pruebas));memset(Pruebas,0,sizeof(Pruebas));
    return resultado?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t leerAleatorio(struct assh_context_s *Datos,uint8_t *resultado,size_t longitud,uint_fast8_t valorClaseTipo) {
    (void)Datos;(void)valorClaseTipo;if(longitud>65536)return ASSH_ERR_CRYPTO;
    return aleatorioRemoto(resultado,longitud)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void finAleatorio(struct assh_context_s *Datos){(void)Datos;}
static const struct assh_prng_s generadorAleatorio={prepararAleatorio,leerAleatorio,finAleatorio};
static void cerrarConexión(void) {
    esAutenticado=iniciadoIntérpreteComandos=0;entradaElementoCanal=0;
    if(conexión)assh_session_release(conexión);conexión=0;
    if(valorParRed>=0)cerrarRed(valorParRed);valorParRed=-1;tipoComando=0;estadoValorFin=-1;futuroCerrar=0;
    cabeceraEntrada=númeroElementosEntrada=cabeceraSalida=númeroElementosSalida=salidaElementoPrevio=0;tiempoReconectar=milisegundosTranscurridosPlaca()+250;
}
int entradaRemotoAlimentar(const unsigned char *Datos,unsigned númeroValor) {
    if(númeroValor>sizeof(líneaEntrada)-númeroElementosEntrada)return -11;
    for(unsigned índiceOrdinal=0;índiceOrdinal<númeroValor;índiceOrdinal++)líneaEntrada[(cabeceraEntrada+númeroElementosEntrada++)%sizeof(líneaEntrada)]=Datos[índiceOrdinal];return númeroValor;
}
int entradaRemoto(void) {
    if(!númeroElementosEntrada)return -1;int valorCarácter=líneaEntrada[cabeceraEntrada];cabeceraEntrada=(cabeceraEntrada+1)%sizeof(líneaEntrada);númeroElementosEntrada--;return valorCarácter;
}
void salidaRemoto(unsigned char valorCarácter) {
    if(!iniciadoIntérpreteComandos||futuroCerrar)return;
    unsigned añadirFinalModo=valorCarácter==10&&salidaElementoPrevio!=13;
    if(númeroElementosSalida+1+añadirFinalModo>sizeof(líneaSalida)){futuroCerrar=2;return;}
    if(añadirFinalModo)líneaSalida[(cabeceraSalida+númeroElementosSalida++)%sizeof(líneaSalida)]=13;
    líneaSalida[(cabeceraSalida+númeroElementosSalida++)%sizeof(líneaSalida)]=valorCarácter;salidaElementoPrevio=valorCarácter;
}
uintptr_t comandoRemotoFinPlaca(uintptr_t valorEstadoValor){if(iniciadoIntérpreteComandos&&tipoComando)estadoValorFin=(int)valorEstadoValor;return 0;}
uintptr_t esperarRemotoPlaca(uintptr_t valorEstadoValor){esperaEnCursoIntérpreteComandos=valorEstadoValor!=0;return 0;}
static int prepararIntérpreteComandos(void) {
    if(extremoEscuchaEnCurso>=0)return 0;
    if(!valorContexto){
        assh_status_t error=assh_context_create(&valorContexto,ASSH_SERVER,prepararMemoria,0,&generadorAleatorio,0);
        if(error)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *modoMétodo[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        error=assh_algo_register(valorContexto,ASSH_SAFETY_WEAK,modoMétodo);
        if(!error)error=assh_service_register_va(valorContexto,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *materialTecla=teclaDispositivo;
        if(!error)error=assh_key_load(valorContexto,assh_context_keys(valorContexto),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&materialTecla,sizeof(teclaDispositivo));
        if(error){valorDiagnóstico("SSH init error ",error);assh_context_release(valorContexto);valorContexto=0;return -5;}
    }
    int valorPuerto=crearExtremoConectorRed(1);if(valorPuerto<0)return valorPuerto;direcciónConectorRedReutilizar(valorPuerto);
    int resultado=asociarRedCorta(valorPuerto,0,22);if(!resultado)resultado=escucharRedCorta(valorPuerto);
    if(resultado<0){cerrarRed(valorPuerto);return resultado;}extremoEscuchaEnCurso=valorPuerto;return 0;
}
uintptr_t controlRemotoPlaca(uintptr_t valorClaseTipo,uintptr_t acción) {
    if(valorClaseTipo==1)return(uint32_t)presentarRemotoControl(acción);
    if(acción==0){cerrarConexión();if(extremoEscuchaEnCurso>=0)cerrarRed(extremoEscuchaEnCurso);extremoEscuchaEnCurso=-1;return 0;}
    if(acción==1){errorInicioSistema=prepararIntérpreteComandos();return(uint32_t)errorInicioSistema;}
    return(uint32_t)(extremoEscuchaEnCurso>=0?1:errorInicioSistema);
}
void prepararRemoto(void){errorInicioSistema=prepararIntérpreteComandos();presentarRemotoControl(1);}
static int palabraConcordante(const struct assh_cbuffer_s *Datos,const char *textoPalabra) {
    size_t longitud=strlen(textoPalabra);return Datos->size==longitud&&!memcmp(Datos->data,textoPalabra,longitud);
}
static int peticiónTerminal(const struct assh_cbuffer_s *Datos) {
    if(Datos->size<24)return 0;
    const unsigned char *posiciónDatos=Datos->data;unsigned longitud=assh_load_u32(posiciónDatos);
    if(longitud>128||Datos->size<longitud+24)return 0;
    unsigned valorModo=assh_load_u32(posiciónDatos+4+longitud+16);
    return valorModo<=2048&&Datos->size==longitud+24+valorModo;
}
static void peticiónManejador(struct assh_event_request_s *evento) {
    if(!esAutenticado||evento->ch!=entradaElementoCanal||!entradaElementoCanal)return;
    if(palabraConcordante(&evento->type,"pty-req")) {
        if(!iniciadoIntérpreteComandos&&peticiónTerminal(&evento->rq_data))evento->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(palabraConcordante(&evento->type,"window-change")) {
        if(iniciadoIntérpreteComandos&&evento->rq_data.size==16)evento->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(iniciadoIntérpreteComandos||!esperaEnCursoIntérpreteComandos)return;
    const unsigned char *comando=0;unsigned longitud=0;
    if(palabraConcordante(&evento->type,"exec")) {
        if(evento->rq_data.size<4)return;
        longitud=assh_load_u32(evento->rq_data.data);
        if(!longitud||longitud>2048||evento->rq_data.size!=longitud+4)return;
        comando=evento->rq_data.data+4;
        for(unsigned índiceOrdinal=0;índiceOrdinal<longitud;índiceOrdinal++)if(!comando[índiceOrdinal])return;
        tipoComando=1;
    }else if(!palabraConcordante(&evento->type,"shell")||evento->rq_data.size)return;
    if(sizeof(líneaEntrada)-númeroElementosEntrada<longitud+2)return;
    const unsigned char valorBorrado=21,terminación=13;
    entradaRemotoAlimentar(&valorBorrado,1);if(longitud)entradaRemotoAlimentar(comando,longitud);entradaRemotoAlimentar(&terminación,1);
    iniciadoIntérpreteComandos=1;evento->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!tipoComando){const char *Guía="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*Guía)salidaRemoto(*Guía++);}
}
void inspeccionarRemoto(void) {
    inspeccionarPresentarRemoto();
    if(extremoEscuchaEnCurso<0)return;
    uintptr_t valorAhora=milisegundosTranscurridosPlaca();
    if(valorParRed<0){if(valorAhora<tiempoReconectar)return;valorParRed=aceptarRedCorta(extremoEscuchaEnCurso);if(valorParRed<0)return;
        tiempoConexión=valorAhora;assh_status_t error=assh_session_create(valorContexto,&conexión);
        if(error){conexión=0;valorDiagnóstico("SSH session error ",error);cerrarConexión();return;}}
    if((!esAutenticado&&valorAhora-tiempoConexión>30000)||futuroCerrar==2||(futuroCerrar&&valorAhora>=tiempoCierreEnCurso)){cerrarConexión();return;}
    if(entradaElementoCanal&&iniciadoIntérpreteComandos&&!futuroCerrar) {
        if(númeroElementosSalida){size_t númeroValor=sizeof(líneaSalida)-cabeceraSalida;if(númeroValor>númeroElementosSalida)númeroValor=númeroElementosSalida;if(númeroValor>2048)númeroValor=2048;
            assh_status_t error=assh_channel_data(entradaElementoCanal,líneaSalida+cabeceraSalida,&númeroValor);
            if(!error){cabeceraSalida=(cabeceraSalida+númeroValor)%sizeof(líneaSalida);númeroElementosSalida-=númeroValor;}
            else if(error!=ASSH_NO_DATA){cerrarConexión();return;}
        }
        if(estadoValorFin>=0&&!númeroElementosSalida){unsigned char valorEstadoValor[4];assh_store_u32(valorEstadoValor,(uint32_t)estadoValorFin);
            if(assh_request(conexión,entradaElementoCanal,"exit-status",11,valorEstadoValor,4,0)||assh_channel_eof(entradaElementoCanal)||assh_channel_close(entradaElementoCanal)) {cerrarConexión();return;}
            futuroCerrar=1;tiempoCierreEnCurso=valorAhora+3000;
        }
    }
    for(unsigned valorSecuencia=0;valorSecuencia<16;valorSecuencia++) {
        struct assh_event_s evento;
        if(!assh_event_get(conexión,&evento,valorAhora/1000)){cerrarConexión();return;}
        assh_status_t error=ASSH_OK;int brevementeRestanteParte=0,extremoDesconectar=0;
        switch(evento.id) {
        case ASSH_EVENT_READ: {
            int númeroValor=leerRedCorta(valorParRed,evento.transport.read.buf.data,evento.transport.read.buf.size);
            if(númeroValor>0)evento.transport.read.transferred=númeroValor;
            else if(númeroValor==-11)brevementeRestanteParte=1;else extremoDesconectar=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int númeroValor=escribirRedCorta(valorParRed,evento.transport.write.buf.data,evento.transport.write.buf.size);
            if(númeroValor>0)evento.transport.write.transferred=númeroValor;
            else if(númeroValor==-11)brevementeRestanteParte=1;else extremoDesconectar=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            evento.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(evento.userauth_server.methods.retries>3)evento.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *Datos=&evento.userauth_server.password;
            if(palabraConcordante(&Datos->username,"user")&&Datos->password.size<=256&&!Datos->new_password.size) {
                unsigned char valorResumen[32];resumenRemoto(Datos->password.data,Datos->password.size,valorResumen);
                unsigned valorDiferencia=0;for(unsigned índiceOrdinal=0;índiceOrdinal<32;índiceOrdinal++)valorDiferencia|=valorResumen[índiceOrdinal]^resumenContraseñaIntérpreteComandos[índiceOrdinal];memset(valorResumen,0,32);
                if(!valorDiferencia)Datos->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: esAutenticado=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *Datos=&evento.connection.channel_open;
            if(esAutenticado&&!entradaElementoCanal&&esperaEnCursoIntérpreteComandos&&palabraConcordante(&Datos->type,"session")&&!Datos->rq_data.size) {
                Datos->reply=ASSH_CONNECTION_REPLY_SUCCESS;Datos->pkt_size=4096;
                Datos->win_size=-1;entradaElementoCanal=Datos->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: peticiónManejador(&evento.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *Datos=&evento.connection.channel_data;
            if(!iniciadoIntérpreteComandos||Datos->ch!=entradaElementoCanal||Datos->ext){extremoDesconectar=1;break;}
            unsigned númeroValor=Datos->data.size;if(númeroValor>sizeof(líneaEntrada)-númeroElementosEntrada)númeroValor=sizeof(líneaEntrada)-númeroElementosEntrada;
            for(unsigned índiceOrdinal=0;índiceOrdinal<númeroValor;índiceOrdinal++)if(Datos->data.data[índiceOrdinal]==4){estadoValorFin=0;númeroValor=índiceOrdinal;Datos->transferred=Datos->data.size;break;}
            entradaRemotoAlimentar(Datos->data.data,númeroValor);if(!Datos->transferred)Datos->transferred=númeroValor;
            if(!númeroValor&&estadoValorFin<0)brevementeRestanteParte=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: entradaElementoCanal=0;iniciadoIntérpreteComandos=0;futuroCerrar=1;tiempoCierreEnCurso=valorAhora+1000;break;
        case ASSH_EVENT_SESSION_ERROR: esAutenticado=iniciadoIntérpreteComandos=0;valorDiagnóstico("SSH error ",evento.session.error.code);extremoDesconectar=1;break;
        case ASSH_EVENT_DISCONNECT: extremoDesconectar=1;break;
        default: break;
        }
        assh_event_done(conexión,&evento,error);
        if(extremoDesconectar){cerrarConexión();return;}if(brevementeRestanteParte)return;
    }
}
