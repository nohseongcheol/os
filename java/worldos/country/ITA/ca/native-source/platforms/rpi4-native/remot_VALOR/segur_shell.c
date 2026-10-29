/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "remot_VALOR.h"
#include "암호기반.h"
#include "Perfil.h"
#include "../xarxa_Pila/xarxa_Pila.h"
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
static struct assh_session_s *connexió_e05f319b;
static struct assh_channel_s *Canal_introducció;
static int S_està_escoltant_extrem=-1,homòleg_VALOR=-1,인증됨,셸시작됨,ordre_TIPUS,finalitzar_Estat=-1,닫을예정,inici_error,shell_Esperant;
static uintptr_t connexió_Hora,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALOR) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char dígit_VALOR[12];unsigned 수=0;do{dígit_VALOR[수++]='0'+VALOR%10;VALOR/=10;}while(VALOR);
    while(수)보드글자쓰기(dígit_VALOR[--수]);보드글자쓰기(10);
}
static assh_status_t Prepara_Memòria(void *dades,void **Adreça,size_t Mida,enum assh_alloc_type_e 종류) {
    (void)dades;(void)종류;
    if(!Mida){versió_remot(*Adreça);*Adreça=0;return ASSH_OK;}
    void *새주소=원격재할당(*Adreça,Mida);
    if(!새주소)return ASSH_ERR_MEM;*Adreça=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *dades,const struct assh_buffer_s *valor_d_inicialització) {
    (void)dades;(void)valor_d_inicialització;unsigned char 시험[32];int RESULTAT=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return RESULTAT?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *dades,uint8_t *RESULTAT,size_t durada_VALOR,uint_fast8_t 종류) {
    (void)dades;(void)종류;if(durada_VALOR>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(RESULTAT,durada_VALOR)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *dades){(void)dades;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void Tanca_connexió(void) {
    인증됨=셸시작됨=0;Canal_introducció=0;
    if(connexió_e05f319b)assh_session_release(connexió_e05f319b);connexió_e05f319b=0;
    if(homòleg_VALOR>=0)Tanca_xarxa(homòleg_VALOR);homòleg_VALOR=-1;ordre_TIPUS=0;finalitzar_Estat=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *dades,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=dades[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int caràcter_VALOR=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return caràcter_VALOR;
}
void 원격출력(unsigned char caràcter_VALOR) {
    if(!셸시작됨||닫을예정)return;
    unsigned Annexa_MODA=caràcter_VALOR==10&&이전출력!=13;
    if(출력수+1+Annexa_MODA>sizeof(출력줄)){닫을예정=2;return;}
    if(Annexa_MODA)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=caràcter_VALOR;이전출력=caràcter_VALOR;
}
uintptr_t Tauler_finalitzar_remot_ordre(uintptr_t Estat_VALOR){if(셸시작됨&&ordre_TIPUS)finalitzar_Estat=(int)Estat_VALOR;return 0;}
uintptr_t Tauler_remot_Espera(uintptr_t Estat_VALOR){shell_Esperant=Estat_VALOR!=0;return 0;}
static int Prepara_shell(void) {
    if(S_està_escoltant_extrem>=0)return 0;
    if(!문맥){
        assh_status_t s_ha_produït_un_error=assh_context_create(&문맥,ASSH_SERVER,Prepara_Memòria,0,&난수기,0);
        if(s_ha_produït_un_error)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *방식[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        s_ha_produït_un_error=assh_algo_register(문맥,ASSH_SAFETY_WEAK,방식);
        if(!s_ha_produït_un_error)s_ha_produït_un_error=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=dispositiu_Clau;
        if(!s_ha_produït_un_error)s_ha_produït_un_error=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(dispositiu_Clau));
        if(s_ha_produït_un_error){진단("SSH init error ",s_ha_produït_un_error);assh_context_release(문맥);문맥=0;return -5;}
    }
    int port_VALOR=통신끝점만들기(1);if(port_VALOR<0)return port_VALOR;통신주소재사용(port_VALOR);
    int RESULTAT=망주소묶기(port_VALOR,0,22);if(!RESULTAT)RESULTAT=연결기다리기(port_VALOR);
    if(RESULTAT<0){Tanca_xarxa(port_VALOR);return RESULTAT;}S_està_escoltant_extrem=port_VALOR;return 0;
}
uintptr_t Tauler_vigilància(uintptr_t 종류,uintptr_t Acció) {
    if(종류==1)return(uint32_t)control_remot_mostrar(Acció);
    if(Acció==0){Tanca_connexió();if(S_està_escoltant_extrem>=0)Tanca_xarxa(S_està_escoltant_extrem);S_està_escoltant_extrem=-1;return 0;}
    if(Acció==1){inici_error=Prepara_shell();return(uint32_t)inici_error;}
    return(uint32_t)(S_està_escoltant_extrem>=0?1:inici_error);
}
void Prepara_remot(void){inici_error=Prepara_shell();control_remot_mostrar(1);}
static int 같은말(const struct assh_cbuffer_s *dades,const char *Word_SMS) {
    size_t durada_VALOR=strlen(Word_SMS);return dades->size==durada_VALOR&&!memcmp(dades->data,Word_SMS,durada_VALOR);
}
static int Terminal_sol_licitud(const struct assh_cbuffer_s *dades) {
    if(dades->size<24)return 0;
    const unsigned char *dades_càrrec=dades->data;unsigned durada_VALOR=assh_load_u32(dades_càrrec);
    if(durada_VALOR>128||dades->size<durada_VALOR+24)return 0;
    unsigned MODA_VALOR=assh_load_u32(dades_càrrec+4+durada_VALOR+16);
    return MODA_VALOR<=2048&&dades->size==durada_VALOR+24+MODA_VALOR;
}
static void control_sol_licitud(struct assh_event_request_s *Esdeveniment) {
    if(!인증됨||Esdeveniment->ch!=Canal_introducció||!Canal_introducció)return;
    if(같은말(&Esdeveniment->type,"pty-req")) {
        if(!셸시작됨&&Terminal_sol_licitud(&Esdeveniment->rq_data))Esdeveniment->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Esdeveniment->type,"window-change")) {
        if(셸시작됨&&Esdeveniment->rq_data.size==16)Esdeveniment->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!shell_Esperant)return;
    const unsigned char *Ordre=0;unsigned durada_VALOR=0;
    if(같은말(&Esdeveniment->type,"exec")) {
        if(Esdeveniment->rq_data.size<4)return;
        durada_VALOR=assh_load_u32(Esdeveniment->rq_data.data);
        if(!durada_VALOR||durada_VALOR>2048||Esdeveniment->rq_data.size!=durada_VALOR+4)return;
        Ordre=Esdeveniment->rq_data.data+4;
        for(unsigned 순번=0;순번<durada_VALOR;순번++)if(!Ordre[순번])return;
        ordre_TIPUS=1;
    }else if(!같은말(&Esdeveniment->type,"shell")||Esdeveniment->rq_data.size)return;
    if(sizeof(입력줄)-입력수<durada_VALOR+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(durada_VALOR)원격입력넣기(Ordre,durada_VALOR);원격입력넣기(&끝,1);
    셸시작됨=1;Esdeveniment->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!ordre_TIPUS){const char *LLEGIU_ME_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*LLEGIU_ME_eb81d7d9)원격출력(*LLEGIU_ME_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(S_està_escoltant_extrem<0)return;
    uintptr_t ARA_VALOR=보드밀리초();
    if(homòleg_VALOR<0){if(ARA_VALOR<재접속시각)return;homòleg_VALOR=망연결받기(S_està_escoltant_extrem);if(homòleg_VALOR<0)return;
        connexió_Hora=ARA_VALOR;assh_status_t s_ha_produït_un_error=assh_session_create(문맥,&connexió_e05f319b);
        if(s_ha_produït_un_error){connexió_e05f319b=0;진단("SSH session error ",s_ha_produït_un_error);Tanca_connexió();return;}}
    if((!인증됨&&ARA_VALOR-connexió_Hora>30000)||닫을예정==2||(닫을예정&&ARA_VALOR>=닫는시각)){Tanca_connexió();return;}
    if(Canal_introducció&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t s_ha_produït_un_error=assh_channel_data(Canal_introducció,출력줄+출력앞,&수);
            if(!s_ha_produït_un_error){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(s_ha_produït_un_error!=ASSH_NO_DATA){Tanca_connexió();return;}
        }
        if(finalitzar_Estat>=0&&!출력수){unsigned char Estat_VALOR[4];assh_store_u32(Estat_VALOR,(uint32_t)finalitzar_Estat);
            if(assh_request(connexió_e05f319b,Canal_introducció,"exit-status",11,Estat_VALOR,4,0)||assh_channel_eof(Canal_introducció)||assh_channel_close(Canal_introducció)) {Tanca_connexió();return;}
            닫을예정=1;닫는시각=ARA_VALOR+3000;
        }
    }
    for(unsigned SEQÜÈNCIA_VALOR=0;SEQÜÈNCIA_VALOR<16;SEQÜÈNCIA_VALOR++) {
        struct assh_event_s Esdeveniment;
        if(!assh_event_get(connexió_e05f319b,&Esdeveniment,ARA_VALOR/1000)){Tanca_connexió();return;}
        assh_status_t s_ha_produït_un_error=ASSH_OK;int 쉬기=0,desconnectar_extrem=0;
        switch(Esdeveniment.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(homòleg_VALOR,Esdeveniment.transport.read.buf.data,Esdeveniment.transport.read.buf.size);
            if(수>0)Esdeveniment.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else desconnectar_extrem=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(homòleg_VALOR,Esdeveniment.transport.write.buf.data,Esdeveniment.transport.write.buf.size);
            if(수>0)Esdeveniment.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else desconnectar_extrem=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Esdeveniment.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Esdeveniment.userauth_server.methods.retries>3)Esdeveniment.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *dades=&Esdeveniment.userauth_server.password;
            if(같은말(&dades->username,"user")&&dades->password.size<=256&&!dades->new_password.size) {
                unsigned char resum_VALOR[32];remot_resum(dades->password.data,dades->password.size,resum_VALOR);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=resum_VALOR[순번]^shell_contrasenya_resum[순번];memset(resum_VALOR,0,32);
                if(!차이)dades->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *dades=&Esdeveniment.connection.channel_open;
            if(인증됨&&!Canal_introducció&&shell_Esperant&&같은말(&dades->type,"session")&&!dades->rq_data.size) {
                dades->reply=ASSH_CONNECTION_REPLY_SUCCESS;dades->pkt_size=4096;
                dades->win_size=-1;Canal_introducció=dades->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: control_sol_licitud(&Esdeveniment.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *dades=&Esdeveniment.connection.channel_data;
            if(!셸시작됨||dades->ch!=Canal_introducció||dades->ext){desconnectar_extrem=1;break;}
            unsigned 수=dades->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(dades->data.data[순번]==4){finalitzar_Estat=0;수=순번;dades->transferred=dades->data.size;break;}
            원격입력넣기(dades->data.data,수);if(!dades->transferred)dades->transferred=수;
            if(!수&&finalitzar_Estat<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Canal_introducció=0;셸시작됨=0;닫을예정=1;닫는시각=ARA_VALOR+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Esdeveniment.session.error.code);desconnectar_extrem=1;break;
        case ASSH_EVENT_DISCONNECT: desconnectar_extrem=1;break;
        default: break;
        }
        assh_event_done(connexió_e05f319b,&Esdeveniment,s_ha_produït_un_error);
        if(desconnectar_extrem){Tanca_connexió();return;}if(쉬기)return;
    }
}
