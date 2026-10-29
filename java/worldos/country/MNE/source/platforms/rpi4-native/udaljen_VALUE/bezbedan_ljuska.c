/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "udaljen_VALUE.h"
#include "kriptografija_Podrška.h"
#include "Profil.h"
#include "../Mreža_stek/Mreža_stek.h"
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
static struct assh_session_s *veza_e05f319b;
static struct assh_channel_s *Kanal_stavka;
static int Slušanje_učesnik=-1,ravnopravni_uređaj_VALUE=-1,인증됨,셸시작됨,komanda_tip,završiti_razgovor_Status=-1,닫을예정,시작오류,셸대기중;
static uintptr_t veza_TIME,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char cifra_VALUE[12];unsigned 수=0;do{cifra_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(cifra_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Pripremi_Memorija(void *podaci,void **adresa,size_t promeniti_veličinu,enum assh_alloc_type_e 종류) {
    (void)podaci;(void)종류;
    if(!promeniti_veličinu){izdanje_udaljen(*adresa);*adresa=0;return ASSH_OK;}
    void *새주소=원격재할당(*adresa,promeniti_veličinu);
    if(!새주소)return ASSH_ERR_MEM;*adresa=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *podaci,const struct assh_buffer_s *početna_vrednost) {
    (void)podaci;(void)početna_vrednost;unsigned char 시험[32];int KR=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return KR?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *podaci,uint8_t *KR,size_t 길이,uint_fast8_t 종류) {
    (void)podaci;(void)종류;if(길이>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(KR,길이)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *podaci){(void)podaci;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void Zatvori_veza(void) {
    인증됨=셸시작됨=0;Kanal_stavka=0;
    if(veza_e05f319b)assh_session_release(veza_e05f319b);veza_e05f319b=0;
    if(ravnopravni_uređaj_VALUE>=0)Zatvori_Mreža(ravnopravni_uređaj_VALUE);ravnopravni_uređaj_VALUE=-1;komanda_tip=0;završiti_razgovor_Status=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *podaci,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=podaci[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int znak_VALUE=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return znak_VALUE;
}
void 원격출력(unsigned char znak_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned dodati_MODE=znak_VALUE==10&&이전출력!=13;
    if(출력수+1+dodati_MODE>sizeof(출력줄)){닫을예정=2;return;}
    if(dodati_MODE)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=znak_VALUE;이전출력=znak_VALUE;
}
uintptr_t Tabla_završiti_razgovor_udaljen_komanda(uintptr_t Status_VALUE){if(셸시작됨&&komanda_tip)završiti_razgovor_Status=(int)Status_VALUE;return 0;}
uintptr_t Tabla_udaljen_čekaj(uintptr_t Status_VALUE){셸대기중=Status_VALUE!=0;return 0;}
static int Pripremi_ljuska(void) {
    if(Slušanje_učesnik>=0)return 0;
    if(!문맥){
        assh_status_t greška=assh_context_create(&문맥,ASSH_SERVER,Pripremi_Memorija,0,&난수기,0);
        if(greška)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metod_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        greška=assh_algo_register(문맥,ASSH_SAFETY_WEAK,metod_MODE);
        if(!greška)greška=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=uređaj_Ključ;
        if(!greška)greška=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(uređaj_Ključ));
        if(greška){진단("SSH init error ",greška);assh_context_release(문맥);문맥=0;return -5;}
    }
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int KR=NET_povezati(port_VALUE,0,22);if(!KR)KR=NET_slušati(port_VALUE);
    if(KR<0){Zatvori_Mreža(port_VALUE);return KR;}Slušanje_učesnik=port_VALUE;return 0;
}
uintptr_t Tabla_daljinska_kontrola(uintptr_t 종류,uintptr_t radnja) {
    if(종류==1)return(uint32_t)kontrola_udaljen_ekran(radnja);
    if(radnja==0){Zatvori_veza();if(Slušanje_učesnik>=0)Zatvori_Mreža(Slušanje_učesnik);Slušanje_učesnik=-1;return 0;}
    if(radnja==1){시작오류=Pripremi_ljuska();return(uint32_t)시작오류;}
    return(uint32_t)(Slušanje_učesnik>=0?1:시작오류);
}
void Pripremi_udaljen(void){시작오류=Pripremi_ljuska();kontrola_udaljen_ekran(1);}
static int 같은말(const struct assh_cbuffer_s *podaci,const char *Word_SMS) {
    size_t 길이=strlen(Word_SMS);return podaci->size==길이&&!memcmp(podaci->data,Word_SMS,길이);
}
static int Terminal_zahtev(const struct assh_cbuffer_s *podaci) {
    if(podaci->size<24)return 0;
    const unsigned char *podaci_pozicija=podaci->data;unsigned 길이=assh_load_u32(podaci_pozicija);
    if(길이>128||podaci->size<길이+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(podaci_pozicija+4+길이+16);
    return MODE_VALUE<=2048&&podaci->size==길이+24+MODE_VALUE;
}
static void pokazivač_zahtev(struct assh_event_request_s *događaj) {
    if(!인증됨||događaj->ch!=Kanal_stavka||!Kanal_stavka)return;
    if(같은말(&događaj->type,"pty-req")) {
        if(!셸시작됨&&Terminal_zahtev(&događaj->rq_data))događaj->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&događaj->type,"window-change")) {
        if(셸시작됨&&događaj->rq_data.size==16)događaj->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *komanda=0;unsigned 길이=0;
    if(같은말(&događaj->type,"exec")) {
        if(događaj->rq_data.size<4)return;
        길이=assh_load_u32(događaj->rq_data.data);
        if(!길이||길이>2048||događaj->rq_data.size!=길이+4)return;
        komanda=događaj->rq_data.data+4;
        for(unsigned 순번=0;순번<길이;순번++)if(!komanda[순번])return;
        komanda_tip=1;
    }else if(!같은말(&događaj->type,"shell")||događaj->rq_data.size)return;
    if(sizeof(입력줄)-입력수<길이+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(길이)원격입력넣기(komanda,길이);원격입력넣기(&끝,1);
    셸시작됨=1;događaj->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!komanda_tip){const char *안내="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*안내)원격출력(*안내++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Slušanje_učesnik<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(ravnopravni_uređaj_VALUE<0){if(NOW_VALUE<재접속시각)return;ravnopravni_uređaj_VALUE=NET_prihvatiti(Slušanje_učesnik);if(ravnopravni_uređaj_VALUE<0)return;
        veza_TIME=NOW_VALUE;assh_status_t greška=assh_session_create(문맥,&veza_e05f319b);
        if(greška){veza_e05f319b=0;진단("SSH session error ",greška);Zatvori_veza();return;}}
    if((!인증됨&&NOW_VALUE-veza_TIME>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){Zatvori_veza();return;}
    if(Kanal_stavka&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t greška=assh_channel_data(Kanal_stavka,출력줄+출력앞,&수);
            if(!greška){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(greška!=ASSH_NO_DATA){Zatvori_veza();return;}
        }
        if(završiti_razgovor_Status>=0&&!출력수){unsigned char Status_VALUE[4];assh_store_u32(Status_VALUE,(uint32_t)završiti_razgovor_Status);
            if(assh_request(veza_e05f319b,Kanal_stavka,"exit-status",11,Status_VALUE,4,0)||assh_channel_eof(Kanal_stavka)||assh_channel_close(Kanal_stavka)) {Zatvori_veza();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s događaj;
        if(!assh_event_get(veza_e05f319b,&događaj,NOW_VALUE/1000)){Zatvori_veza();return;}
        assh_status_t greška=ASSH_OK;int 쉬기=0,prekinuti_vezu_učesnik=0;
        switch(događaj.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(ravnopravni_uređaj_VALUE,događaj.transport.read.buf.data,događaj.transport.read.buf.size);
            if(수>0)događaj.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else prekinuti_vezu_učesnik=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(ravnopravni_uređaj_VALUE,događaj.transport.write.buf.data,događaj.transport.write.buf.size);
            if(수>0)događaj.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else prekinuti_vezu_učesnik=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            događaj.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(događaj.userauth_server.methods.retries>3)događaj.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *podaci=&događaj.userauth_server.password;
            if(같은말(&podaci->username,"user")&&podaci->password.size<=256&&!podaci->new_password.size) {
                unsigned char rezime_VALUE[32];udaljen_rezime(podaci->password.data,podaci->password.size,rezime_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=rezime_VALUE[순번]^ljuska_lozinka_rezime[순번];memset(rezime_VALUE,0,32);
                if(!차이)podaci->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *podaci=&događaj.connection.channel_open;
            if(인증됨&&!Kanal_stavka&&셸대기중&&같은말(&podaci->type,"session")&&!podaci->rq_data.size) {
                podaci->reply=ASSH_CONNECTION_REPLY_SUCCESS;podaci->pkt_size=4096;
                podaci->win_size=-1;Kanal_stavka=podaci->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: pokazivač_zahtev(&događaj.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *podaci=&događaj.connection.channel_data;
            if(!셸시작됨||podaci->ch!=Kanal_stavka||podaci->ext){prekinuti_vezu_učesnik=1;break;}
            unsigned 수=podaci->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(podaci->data.data[순번]==4){završiti_razgovor_Status=0;수=순번;podaci->transferred=podaci->data.size;break;}
            원격입력넣기(podaci->data.data,수);if(!podaci->transferred)podaci->transferred=수;
            if(!수&&završiti_razgovor_Status<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Kanal_stavka=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",događaj.session.error.code);prekinuti_vezu_učesnik=1;break;
        case ASSH_EVENT_DISCONNECT: prekinuti_vezu_učesnik=1;break;
        default: break;
        }
        assh_event_done(veza_e05f319b,&događaj,greška);
        if(prekinuti_vezu_učesnik){Zatvori_veza();return;}if(쉬기)return;
    }
}
