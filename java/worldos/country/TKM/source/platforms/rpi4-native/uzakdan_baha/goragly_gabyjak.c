/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "uzakdan_baha.h"
#include "암호기반.h"
#include "profil.h"
#include "../Tor_Desse/Tor_Desse.h"
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
static struct assh_context_s *Kontekst_baha;
static struct assh_session_s *birikme_e05f319b;
static struct assh_channel_s *kanal_girizmeklik;
static int 듣는곳=-1,deň_derejeli_düwün_baha=-1,인증됨,셸시작됨,buýruk_ýaz,tamamla_ýagdaý=-1,닫을예정,başlangyç_säwlik,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Söz_SMS,unsigned baha) {
    while(*Söz_SMS)보드글자쓰기(*Söz_SMS++);
    char san_baha[12];unsigned 수=0;do{san_baha[수++]='0'+baha%10;baha/=10;}while(baha);
    while(수)보드글자쓰기(san_baha[--수]);보드글자쓰기(10);
}
static assh_status_t Taýýarla_ýat(void *maglumat,void **salgy,size_t Ululyk,enum assh_alloc_type_e 종류) {
    (void)maglumat;(void)종류;
    if(!Ululyk){goýbermek_uzakdan(*salgy);*salgy=0;return ASSH_OK;}
    void *새주소=원격재할당(*salgy,Ululyk);
    if(!새주소)return ASSH_ERR_MEM;*salgy=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *maglumat,const struct assh_buffer_s *deslapky_baha_baha) {
    (void)maglumat;(void)deslapky_baha_baha;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *maglumat,uint8_t *결과,size_t dowamlylyk_baha,uint_fast8_t 종류) {
    (void)maglumat;(void)종류;if(dowamlylyk_baha>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,dowamlylyk_baha)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *maglumat){(void)maglumat;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void ýap_birikme(void) {
    인증됨=셸시작됨=0;kanal_girizmeklik=0;
    if(birikme_e05f319b)assh_session_release(birikme_e05f319b);birikme_e05f319b=0;
    if(deň_derejeli_düwün_baha>=0)ýap_Tor(deň_derejeli_düwün_baha);deň_derejeli_düwün_baha=-1;buýruk_ýaz=0;tamamla_ýagdaý=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *maglumat,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=maglumat[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int nyşan_baha_068c2631=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return nyşan_baha_068c2631;
}
void 원격출력(unsigned char nyşan_baha_068c2631) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=nyşan_baha_068c2631==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=nyşan_baha_068c2631;이전출력=nyşan_baha_068c2631;
}
uintptr_t 보드원격명령끝(uintptr_t ýagdaý_baha){if(셸시작됨&&buýruk_ýaz)tamamla_ýagdaý=(int)ýagdaý_baha;return 0;}
uintptr_t 보드원격대기(uintptr_t ýagdaý_baha){셸대기중=ýagdaý_baha!=0;return 0;}
static int Taýýarla_gabyjak(void) {
    if(듣는곳>=0)return 0;
    if(!Kontekst_baha){
        assh_status_t Hata=assh_context_create(&Kontekst_baha,ASSH_SERVER,Taýýarla_ýat,0,&난수기,0);
        if(Hata)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *usul_reje[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Hata=assh_algo_register(Kontekst_baha,ASSH_SAFETY_WEAK,usul_reje);
        if(!Hata)Hata=assh_service_register_va(Kontekst_baha,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=enjam_açar;
        if(!Hata)Hata=assh_key_load(Kontekst_baha,assh_context_keys(Kontekst_baha),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(enjam_açar));
        if(Hata){진단("SSH init error ",Hata);assh_context_release(Kontekst_baha);Kontekst_baha=0;return -5;}
    }
    int port_baha=통신끝점만들기(1);if(port_baha<0)return port_baha;통신주소재사용(port_baha);
    int 결과=망주소묶기(port_baha,0,22);if(!결과)결과=연결기다리기(port_baha);
    if(결과<0){ýap_Tor(port_baha);return 결과;}듣는곳=port_baha;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t iş) {
    if(종류==1)return(uint32_t)dolandyryş_uzakdan_ekran(iş);
    if(iş==0){ýap_birikme();if(듣는곳>=0)ýap_Tor(듣는곳);듣는곳=-1;return 0;}
    if(iş==1){başlangyç_säwlik=Taýýarla_gabyjak();return(uint32_t)başlangyç_säwlik;}
    return(uint32_t)(듣는곳>=0?1:başlangyç_säwlik);
}
void Taýýarla_uzakdan(void){başlangyç_säwlik=Taýýarla_gabyjak();dolandyryş_uzakdan_ekran(1);}
static int 같은말(const struct assh_cbuffer_s *maglumat,const char *Söz_SMS) {
    size_t dowamlylyk_baha=strlen(Söz_SMS);return maglumat->size==dowamlylyk_baha&&!memcmp(maglumat->data,Söz_SMS,dowamlylyk_baha);
}
static int 터미널요청(const struct assh_cbuffer_s *maglumat) {
    if(maglumat->size<24)return 0;
    const unsigned char *자료위치=maglumat->data;unsigned dowamlylyk_baha=assh_load_u32(자료위치);
    if(dowamlylyk_baha>128||maglumat->size<dowamlylyk_baha+24)return 0;
    unsigned reje_baha=assh_load_u32(자료위치+4+dowamlylyk_baha+16);
    return reje_baha<=2048&&maglumat->size==dowamlylyk_baha+24+reje_baha;
}
static void 요청처리(struct assh_event_request_s *waka) {
    if(!인증됨||waka->ch!=kanal_girizmeklik||!kanal_girizmeklik)return;
    if(같은말(&waka->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&waka->rq_data))waka->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&waka->type,"window-change")) {
        if(셸시작됨&&waka->rq_data.size==16)waka->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *buýruk=0;unsigned dowamlylyk_baha=0;
    if(같은말(&waka->type,"exec")) {
        if(waka->rq_data.size<4)return;
        dowamlylyk_baha=assh_load_u32(waka->rq_data.data);
        if(!dowamlylyk_baha||dowamlylyk_baha>2048||waka->rq_data.size!=dowamlylyk_baha+4)return;
        buýruk=waka->rq_data.data+4;
        for(unsigned 순번=0;순번<dowamlylyk_baha;순번++)if(!buýruk[순번])return;
        buýruk_ýaz=1;
    }else if(!같은말(&waka->type,"shell")||waka->rq_data.size)return;
    if(sizeof(입력줄)-입력수<dowamlylyk_baha+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(dowamlylyk_baha)원격입력넣기(buýruk,dowamlylyk_baha);원격입력넣기(&끝,1);
    셸시작됨=1;waka->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!buýruk_ýaz){const char *README_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*README_eb81d7d9)원격출력(*README_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(deň_derejeli_düwün_baha<0){if(지금<재접속시각)return;deň_derejeli_düwün_baha=망연결받기(듣는곳);if(deň_derejeli_düwün_baha<0)return;
        접속시각=지금;assh_status_t Hata=assh_session_create(Kontekst_baha,&birikme_e05f319b);
        if(Hata){birikme_e05f319b=0;진단("SSH session error ",Hata);ýap_birikme();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){ýap_birikme();return;}
    if(kanal_girizmeklik&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Hata=assh_channel_data(kanal_girizmeklik,출력줄+출력앞,&수);
            if(!Hata){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Hata!=ASSH_NO_DATA){ýap_birikme();return;}
        }
        if(tamamla_ýagdaý>=0&&!출력수){unsigned char ýagdaý_baha[4];assh_store_u32(ýagdaý_baha,(uint32_t)tamamla_ýagdaý);
            if(assh_request(birikme_e05f319b,kanal_girizmeklik,"exit-status",11,ýagdaý_baha,4,0)||assh_channel_eof(kanal_girizmeklik)||assh_channel_close(kanal_girizmeklik)) {ýap_birikme();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned SEQUENCE_baha=0;SEQUENCE_baha<16;SEQUENCE_baha++) {
        struct assh_event_s waka;
        if(!assh_event_get(birikme_e05f319b,&waka,지금/1000)){ýap_birikme();return;}
        assh_status_t Hata=ASSH_OK;int 쉬기=0,끊기=0;
        switch(waka.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(deň_derejeli_düwün_baha,waka.transport.read.buf.data,waka.transport.read.buf.size);
            if(수>0)waka.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(deň_derejeli_düwün_baha,waka.transport.write.buf.data,waka.transport.write.buf.size);
            if(수>0)waka.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            waka.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(waka.userauth_server.methods.retries>3)waka.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *maglumat=&waka.userauth_server.password;
            if(같은말(&maglumat->username,"user")&&maglumat->password.size<=256&&!maglumat->new_password.size) {
                unsigned char gysgaça_mazmun_baha[32];uzakdan_gysgaça_mazmun(maglumat->password.data,maglumat->password.size,gysgaça_mazmun_baha);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=gysgaça_mazmun_baha[순번]^gabyjak_parol_gysgaça_mazmun[순번];memset(gysgaça_mazmun_baha,0,32);
                if(!차이)maglumat->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *maglumat=&waka.connection.channel_open;
            if(인증됨&&!kanal_girizmeklik&&셸대기중&&같은말(&maglumat->type,"session")&&!maglumat->rq_data.size) {
                maglumat->reply=ASSH_CONNECTION_REPLY_SUCCESS;maglumat->pkt_size=4096;
                maglumat->win_size=-1;kanal_girizmeklik=maglumat->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&waka.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *maglumat=&waka.connection.channel_data;
            if(!셸시작됨||maglumat->ch!=kanal_girizmeklik||maglumat->ext){끊기=1;break;}
            unsigned 수=maglumat->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(maglumat->data.data[순번]==4){tamamla_ýagdaý=0;수=순번;maglumat->transferred=maglumat->data.size;break;}
            원격입력넣기(maglumat->data.data,수);if(!maglumat->transferred)maglumat->transferred=수;
            if(!수&&tamamla_ýagdaý<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: kanal_girizmeklik=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",waka.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(birikme_e05f319b,&waka,Hata);
        if(끊기){ýap_birikme();return;}if(쉬기)return;
    }
}
