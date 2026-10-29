/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "fjern_VALUE.h"
#include "암호기반.h"
#include "Profil.h"
#include "../Nettverk_Stabel/Nettverk_Stabel.h"
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
static struct assh_context_s *kontekst_VALUE;
static struct assh_session_s *kontakt_e05f319b;
static struct assh_channel_s *kanal_oppføring;
static int Lyttar_endepunkt=-1,node_VALUE_6a3b6fa7=-1,인증됨,셸시작됨,kommando_TYPE,avslutte_status=-1,닫을예정,oppstart_feil,grensesnitt_Ventar;
static uintptr_t kontakt_TIME,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char siffer_VALUE[12];unsigned 수=0;do{siffer_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(siffer_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Klargjer_Minne(void *data,void **ADDRESS,size_t Storleik,enum assh_alloc_type_e 종류) {
    (void)data;(void)종류;
    if(!Storleik){frigi_fjern(*ADDRESS);*ADDRESS=0;return ASSH_OK;}
    void *새주소=원격재할당(*ADDRESS,Storleik);
    if(!새주소)return ASSH_ERR_MEM;*ADDRESS=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *data,const struct assh_buffer_s *startverdi_VALUE) {
    (void)data;(void)startverdi_VALUE;unsigned char 시험[32];int forretningsmål=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return forretningsmål?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *data,uint8_t *forretningsmål,size_t lengd_VALUE,uint_fast8_t 종류) {
    (void)data;(void)종류;if(lengd_VALUE>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(forretningsmål,lengd_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *data){(void)data;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void Lukk_kontakt(void) {
    인증됨=셸시작됨=0;kanal_oppføring=0;
    if(kontakt_e05f319b)assh_session_release(kontakt_e05f319b);kontakt_e05f319b=0;
    if(node_VALUE_6a3b6fa7>=0)Lukk_Nettverk(node_VALUE_6a3b6fa7);node_VALUE_6a3b6fa7=-1;kommando_TYPE=0;avslutte_status=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *data,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=data[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int teikn_VALUE=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return teikn_VALUE;
}
void 원격출력(unsigned char teikn_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=teikn_VALUE==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=teikn_VALUE;이전출력=teikn_VALUE;
}
uintptr_t Tavle_avslutte_fjern_kommando(uintptr_t status_VALUE){if(셸시작됨&&kommando_TYPE)avslutte_status=(int)status_VALUE;return 0;}
uintptr_t Tavle_fjern_vent(uintptr_t status_VALUE){grensesnitt_Ventar=status_VALUE!=0;return 0;}
static int Klargjer_grensesnitt(void) {
    if(Lyttar_endepunkt>=0)return 0;
    if(!kontekst_VALUE){
        assh_status_t FEIL=assh_context_create(&kontekst_VALUE,ASSH_SERVER,Klargjer_Minne,0,&난수기,0);
        if(FEIL)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metode_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        FEIL=assh_algo_register(kontekst_VALUE,ASSH_SAFETY_WEAK,metode_MODE);
        if(!FEIL)FEIL=assh_service_register_va(kontekst_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=mobil_tast;
        if(!FEIL)FEIL=assh_key_load(kontekst_VALUE,assh_context_keys(kontekst_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(mobil_tast));
        if(FEIL){진단("SSH init error ",FEIL);assh_context_release(kontekst_VALUE);kontekst_VALUE=0;return -5;}
    }
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int forretningsmål=망주소묶기(port_VALUE,0,22);if(!forretningsmål)forretningsmål=연결기다리기(port_VALUE);
    if(forretningsmål<0){Lukk_Nettverk(port_VALUE);return forretningsmål;}Lyttar_endepunkt=port_VALUE;return 0;
}
uintptr_t Tavle_skygging(uintptr_t 종류,uintptr_t Handling) {
    if(종류==1)return(uint32_t)styring_fjern_vise(Handling);
    if(Handling==0){Lukk_kontakt();if(Lyttar_endepunkt>=0)Lukk_Nettverk(Lyttar_endepunkt);Lyttar_endepunkt=-1;return 0;}
    if(Handling==1){oppstart_feil=Klargjer_grensesnitt();return(uint32_t)oppstart_feil;}
    return(uint32_t)(Lyttar_endepunkt>=0?1:oppstart_feil);
}
void Klargjer_fjern(void){oppstart_feil=Klargjer_grensesnitt();styring_fjern_vise(1);}
static int 같은말(const struct assh_cbuffer_s *data,const char *Word_SMS) {
    size_t lengd_VALUE=strlen(Word_SMS);return data->size==lengd_VALUE&&!memcmp(data->data,Word_SMS,lengd_VALUE);
}
static int 터미널요청(const struct assh_cbuffer_s *data) {
    if(data->size<24)return 0;
    const unsigned char *data_plassere=data->data;unsigned lengd_VALUE=assh_load_u32(data_plassere);
    if(lengd_VALUE>128||data->size<lengd_VALUE+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(data_plassere+4+lengd_VALUE+16);
    return MODE_VALUE<=2048&&data->size==lengd_VALUE+24+MODE_VALUE;
}
static void 요청처리(struct assh_event_request_s *Hending) {
    if(!인증됨||Hending->ch!=kanal_oppføring||!kanal_oppføring)return;
    if(같은말(&Hending->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&Hending->rq_data))Hending->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Hending->type,"window-change")) {
        if(셸시작됨&&Hending->rq_data.size==16)Hending->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!grensesnitt_Ventar)return;
    const unsigned char *Kommando=0;unsigned lengd_VALUE=0;
    if(같은말(&Hending->type,"exec")) {
        if(Hending->rq_data.size<4)return;
        lengd_VALUE=assh_load_u32(Hending->rq_data.data);
        if(!lengd_VALUE||lengd_VALUE>2048||Hending->rq_data.size!=lengd_VALUE+4)return;
        Kommando=Hending->rq_data.data+4;
        for(unsigned 순번=0;순번<lengd_VALUE;순번++)if(!Kommando[순번])return;
        kommando_TYPE=1;
    }else if(!같은말(&Hending->type,"shell")||Hending->rq_data.size)return;
    if(sizeof(입력줄)-입력수<lengd_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(lengd_VALUE)원격입력넣기(Kommando,lengd_VALUE);원격입력넣기(&끝,1);
    셸시작됨=1;Hending->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!kommando_TYPE){const char *Viktig_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*Viktig_eb81d7d9)원격출력(*Viktig_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Lyttar_endepunkt<0)return;
    uintptr_t NO_VALUE=보드밀리초();
    if(node_VALUE_6a3b6fa7<0){if(NO_VALUE<재접속시각)return;node_VALUE_6a3b6fa7=망연결받기(Lyttar_endepunkt);if(node_VALUE_6a3b6fa7<0)return;
        kontakt_TIME=NO_VALUE;assh_status_t FEIL=assh_session_create(kontekst_VALUE,&kontakt_e05f319b);
        if(FEIL){kontakt_e05f319b=0;진단("SSH session error ",FEIL);Lukk_kontakt();return;}}
    if((!인증됨&&NO_VALUE-kontakt_TIME>30000)||닫을예정==2||(닫을예정&&NO_VALUE>=닫는시각)){Lukk_kontakt();return;}
    if(kanal_oppføring&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t FEIL=assh_channel_data(kanal_oppføring,출력줄+출력앞,&수);
            if(!FEIL){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(FEIL!=ASSH_NO_DATA){Lukk_kontakt();return;}
        }
        if(avslutte_status>=0&&!출력수){unsigned char status_VALUE[4];assh_store_u32(status_VALUE,(uint32_t)avslutte_status);
            if(assh_request(kontakt_e05f319b,kanal_oppføring,"exit-status",11,status_VALUE,4,0)||assh_channel_eof(kanal_oppføring)||assh_channel_close(kanal_oppføring)) {Lukk_kontakt();return;}
            닫을예정=1;닫는시각=NO_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s Hending;
        if(!assh_event_get(kontakt_e05f319b,&Hending,NO_VALUE/1000)){Lukk_kontakt();return;}
        assh_status_t FEIL=ASSH_OK;int 쉬기=0,kople_frå_endepunkt=0;
        switch(Hending.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(node_VALUE_6a3b6fa7,Hending.transport.read.buf.data,Hending.transport.read.buf.size);
            if(수>0)Hending.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else kople_frå_endepunkt=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(node_VALUE_6a3b6fa7,Hending.transport.write.buf.data,Hending.transport.write.buf.size);
            if(수>0)Hending.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else kople_frå_endepunkt=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Hending.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Hending.userauth_server.methods.retries>3)Hending.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *data=&Hending.userauth_server.password;
            if(같은말(&data->username,"user")&&data->password.size<=256&&!data->new_password.size) {
                unsigned char samandrag_VALUE[32];fjern_samandrag(data->password.data,data->password.size,samandrag_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=samandrag_VALUE[순번]^grensesnitt_passord_samandrag[순번];memset(samandrag_VALUE,0,32);
                if(!차이)data->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *data=&Hending.connection.channel_open;
            if(인증됨&&!kanal_oppføring&&grensesnitt_Ventar&&같은말(&data->type,"session")&&!data->rq_data.size) {
                data->reply=ASSH_CONNECTION_REPLY_SUCCESS;data->pkt_size=4096;
                data->win_size=-1;kanal_oppføring=data->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&Hending.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *data=&Hending.connection.channel_data;
            if(!셸시작됨||data->ch!=kanal_oppføring||data->ext){kople_frå_endepunkt=1;break;}
            unsigned 수=data->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(data->data.data[순번]==4){avslutte_status=0;수=순번;data->transferred=data->data.size;break;}
            원격입력넣기(data->data.data,수);if(!data->transferred)data->transferred=수;
            if(!수&&avslutte_status<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: kanal_oppføring=0;셸시작됨=0;닫을예정=1;닫는시각=NO_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Hending.session.error.code);kople_frå_endepunkt=1;break;
        case ASSH_EVENT_DISCONNECT: kople_frå_endepunkt=1;break;
        default: break;
        }
        assh_event_done(kontakt_e05f319b,&Hending,FEIL);
        if(kople_frå_endepunkt){Lukk_kontakt();return;}if(쉬기)return;
    }
}
