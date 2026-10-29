/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "remoto_VALOR.h"
#include "암호기반.h"
#include "Perfil.h"
#include "../Rede_Montón/Rede_Montón.h"
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
extern uintptr_t 보드밀리초(void);
extern uintptr_t 보드글자쓰기(uintptr_t);
static struct assh_context_s *문맥;
static struct assh_session_s *conexión_e05f319b;
static struct assh_channel_s *Canle_introdución;
static int A_escoitar_extremo=-1,punto_VALOR=-1,인증됨,셸시작됨,comando_TIPO,finalizar_Estado=-1,닫을예정,inicio_erro,shell_Agardando;
static uintptr_t conexión_hora,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALOR) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char díxito_VALOR[12];unsigned 수=0;do{díxito_VALOR[수++]='0'+VALOR%10;VALOR/=10;}while(VALOR);
    while(수)보드글자쓰기(díxito_VALOR[--수]);보드글자쓰기(10);
}
static assh_status_t 기억마련(void *datos,void **ENDEREZO,size_t Tamaño,enum assh_alloc_type_e 종류) {
    (void)datos;(void)종류;
    if(!Tamaño){liberar_remoto(*ENDEREZO);*ENDEREZO=0;return ASSH_OK;}
    void *새주소=원격재할당(*ENDEREZO,Tamaño);
    if(!새주소)return ASSH_ERR_MEM;*ENDEREZO=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *datos,const struct assh_buffer_s *valor_de_inicio) {
    (void)datos;(void)valor_de_inicio;unsigned char 시험[32];int RESULTANTE=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return RESULTANTE?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *datos,uint8_t *RESULTANTE,size_t duración_VALOR,uint_fast8_t 종류) {
    (void)datos;(void)종류;if(duración_VALOR>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(RESULTANTE,duración_VALOR)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *datos){(void)datos;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void peche_conexión(void) {
    인증됨=셸시작됨=0;Canle_introdución=0;
    if(conexión_e05f319b)assh_session_release(conexión_e05f319b);conexión_e05f319b=0;
    if(punto_VALOR>=0)peche_Rede(punto_VALOR);punto_VALOR=-1;comando_TIPO=0;finalizar_Estado=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *datos,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=datos[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int carácter_VALOR=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return carácter_VALOR;
}
void 원격출력(unsigned char carácter_VALOR) {
    if(!셸시작됨||닫을예정)return;
    unsigned Anexar_MODO=carácter_VALOR==10&&이전출력!=13;
    if(출력수+1+Anexar_MODO>sizeof(출력줄)){닫을예정=2;return;}
    if(Anexar_MODO)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=carácter_VALOR;이전출력=carácter_VALOR;
}
uintptr_t Panel_finalizar_remoto_comando(uintptr_t Estado_VALOR){if(셸시작됨&&comando_TIPO)finalizar_Estado=(int)Estado_VALOR;return 0;}
uintptr_t Panel_remoto_agarda(uintptr_t Estado_VALOR){shell_Agardando=Estado_VALOR!=0;return 0;}
static int 셸준비(void) {
    if(A_escoitar_extremo>=0)return 0;
    if(!문맥){
        assh_status_t ERRO=assh_context_create(&문맥,ASSH_SERVER,기억마련,0,&난수기,0);
        if(ERRO)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *방식[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ERRO=assh_algo_register(문맥,ASSH_SAFETY_WEAK,방식);
        if(!ERRO)ERRO=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=dispositivo_Chave;
        if(!ERRO)ERRO=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(dispositivo_Chave));
        if(ERRO){진단("SSH init error ",ERRO);assh_context_release(문맥);문맥=0;return -5;}
    }
    int porto_VALOR=통신끝점만들기(1);if(porto_VALOR<0)return porto_VALOR;통신주소재사용(porto_VALOR);
    int RESULTANTE=망주소묶기(porto_VALOR,0,22);if(!RESULTANTE)RESULTANTE=연결기다리기(porto_VALOR);
    if(RESULTANTE<0){peche_Rede(porto_VALOR);return RESULTANTE;}A_escoitar_extremo=porto_VALOR;return 0;
}
uintptr_t Panel_vixilancia(uintptr_t 종류,uintptr_t Acción) {
    if(종류==1)return(uint32_t)control_remoto_mostrar(Acción);
    if(Acción==0){peche_conexión();if(A_escoitar_extremo>=0)peche_Rede(A_escoitar_extremo);A_escoitar_extremo=-1;return 0;}
    if(Acción==1){inicio_erro=셸준비();return(uint32_t)inicio_erro;}
    return(uint32_t)(A_escoitar_extremo>=0?1:inicio_erro);
}
void 원격준비(void){inicio_erro=셸준비();control_remoto_mostrar(1);}
static int 같은말(const struct assh_cbuffer_s *datos,const char *Word_SMS) {
    size_t duración_VALOR=strlen(Word_SMS);return datos->size==duración_VALOR&&!memcmp(datos->data,Word_SMS,duración_VALOR);
}
static int Terminal_solicitude(const struct assh_cbuffer_s *datos) {
    if(datos->size<24)return 0;
    const unsigned char *datos_cargo=datos->data;unsigned duración_VALOR=assh_load_u32(datos_cargo);
    if(duración_VALOR>128||datos->size<duración_VALOR+24)return 0;
    unsigned MODO_VALOR=assh_load_u32(datos_cargo+4+duración_VALOR+16);
    return MODO_VALOR<=2048&&datos->size==duración_VALOR+24+MODO_VALOR;
}
static void agarradoira_solicitude(struct assh_event_request_s *Evento) {
    if(!인증됨||Evento->ch!=Canle_introdución||!Canle_introdución)return;
    if(같은말(&Evento->type,"pty-req")) {
        if(!셸시작됨&&Terminal_solicitude(&Evento->rq_data))Evento->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Evento->type,"window-change")) {
        if(셸시작됨&&Evento->rq_data.size==16)Evento->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!shell_Agardando)return;
    const unsigned char *Orde=0;unsigned duración_VALOR=0;
    if(같은말(&Evento->type,"exec")) {
        if(Evento->rq_data.size<4)return;
        duración_VALOR=assh_load_u32(Evento->rq_data.data);
        if(!duración_VALOR||duración_VALOR>2048||Evento->rq_data.size!=duración_VALOR+4)return;
        Orde=Evento->rq_data.data+4;
        for(unsigned 순번=0;순번<duración_VALOR;순번++)if(!Orde[순번])return;
        comando_TIPO=1;
    }else if(!같은말(&Evento->type,"shell")||Evento->rq_data.size)return;
    if(sizeof(입력줄)-입력수<duración_VALOR+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(duración_VALOR)원격입력넣기(Orde,duración_VALOR);원격입력넣기(&끝,1);
    셸시작됨=1;Evento->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!comando_TIPO){const char *Léame_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*Léame_eb81d7d9)원격출력(*Léame_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(A_escoitar_extremo<0)return;
    uintptr_t AGORA_VALOR=보드밀리초();
    if(punto_VALOR<0){if(AGORA_VALOR<재접속시각)return;punto_VALOR=망연결받기(A_escoitar_extremo);if(punto_VALOR<0)return;
        conexión_hora=AGORA_VALOR;assh_status_t ERRO=assh_session_create(문맥,&conexión_e05f319b);
        if(ERRO){conexión_e05f319b=0;진단("SSH session error ",ERRO);peche_conexión();return;}}
    if((!인증됨&&AGORA_VALOR-conexión_hora>30000)||닫을예정==2||(닫을예정&&AGORA_VALOR>=닫는시각)){peche_conexión();return;}
    if(Canle_introdución&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ERRO=assh_channel_data(Canle_introdución,출력줄+출력앞,&수);
            if(!ERRO){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ERRO!=ASSH_NO_DATA){peche_conexión();return;}
        }
        if(finalizar_Estado>=0&&!출력수){unsigned char Estado_VALOR[4];assh_store_u32(Estado_VALOR,(uint32_t)finalizar_Estado);
            if(assh_request(conexión_e05f319b,Canle_introdución,"exit-status",11,Estado_VALOR,4,0)||assh_channel_eof(Canle_introdución)||assh_channel_close(Canle_introdución)) {peche_conexión();return;}
            닫을예정=1;닫는시각=AGORA_VALOR+3000;
        }
    }
    for(unsigned SECUENCIA_VALOR=0;SECUENCIA_VALOR<16;SECUENCIA_VALOR++) {
        struct assh_event_s Evento;
        if(!assh_event_get(conexión_e05f319b,&Evento,AGORA_VALOR/1000)){peche_conexión();return;}
        assh_status_t ERRO=ASSH_OK;int 쉬기=0,desconectar_extremo=0;
        switch(Evento.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(punto_VALOR,Evento.transport.read.buf.data,Evento.transport.read.buf.size);
            if(수>0)Evento.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else desconectar_extremo=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(punto_VALOR,Evento.transport.write.buf.data,Evento.transport.write.buf.size);
            if(수>0)Evento.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else desconectar_extremo=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Evento.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Evento.userauth_server.methods.retries>3)Evento.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *datos=&Evento.userauth_server.password;
            if(같은말(&datos->username,"user")&&datos->password.size<=256&&!datos->new_password.size) {
                unsigned char resumo_VALOR[32];remoto_resumo(datos->password.data,datos->password.size,resumo_VALOR);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=resumo_VALOR[순번]^shell_contrasinal_resumo[순번];memset(resumo_VALOR,0,32);
                if(!차이)datos->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *datos=&Evento.connection.channel_open;
            if(인증됨&&!Canle_introdución&&shell_Agardando&&같은말(&datos->type,"session")&&!datos->rq_data.size) {
                datos->reply=ASSH_CONNECTION_REPLY_SUCCESS;datos->pkt_size=4096;
                datos->win_size=-1;Canle_introdución=datos->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: agarradoira_solicitude(&Evento.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *datos=&Evento.connection.channel_data;
            if(!셸시작됨||datos->ch!=Canle_introdución||datos->ext){desconectar_extremo=1;break;}
            unsigned 수=datos->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(datos->data.data[순번]==4){finalizar_Estado=0;수=순번;datos->transferred=datos->data.size;break;}
            원격입력넣기(datos->data.data,수);if(!datos->transferred)datos->transferred=수;
            if(!수&&finalizar_Estado<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Canle_introdución=0;셸시작됨=0;닫을예정=1;닫는시각=AGORA_VALOR+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Evento.session.error.code);desconectar_extremo=1;break;
        case ASSH_EVENT_DISCONNECT: desconectar_extremo=1;break;
        default: break;
        }
        assh_event_done(conexión_e05f319b,&Evento,ERRO);
        if(desconectar_extremo){peche_conexión();return;}if(쉬기)return;
    }
}
