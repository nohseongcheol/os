/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "udaljeno_VALUE.h"
#include "kriptografija_Podrška.h"
#include "Profil.h"
#include "../mreža_hrpa/mreža_hrpa.h"
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
static struct assh_channel_s *kanal_unos;
static int Slušanje_sudionik=-1,ravnopravan_član_VALUE=-1,인증됨,셸시작됨,naredba_TYPE,završiti_razgovor_Stanje=-1,닫을예정,pokretanje_pogreška,ljuska_Čekanje;
static uintptr_t veza_TIME,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char znamenka_VALUE[12];unsigned 수=0;do{znamenka_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(znamenka_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Pripremi_Memorija(void *podaci,void **adresa,size_t Veličina,enum assh_alloc_type_e 종류) {
    (void)podaci;(void)종류;
    if(!Veličina){izdati_udaljeno(*adresa);*adresa=0;return ASSH_OK;}
    void *새주소=원격재할당(*adresa,Veličina);
    if(!새주소)return ASSH_ERR_MEM;*adresa=새주소;return ASSH_OK;
}
static assh_status_t Pripremi_slučajan(struct assh_context_s *podaci,const struct assh_buffer_s *početna_vrijednost) {
    (void)podaci;(void)početna_vrijednost;unsigned char 시험[32];int REZULTAT=udaljeno_slučajan(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return REZULTAT?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *podaci,uint8_t *REZULTAT,size_t 길이,uint_fast8_t 종류) {
    (void)podaci;(void)종류;if(길이>65536)return ASSH_ERR_CRYPTO;
    return udaljeno_slučajan(REZULTAT,길이)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void slučajan_završiti_razgovor(struct assh_context_s *podaci){(void)podaci;}
static const struct assh_prng_s slučajan_generator={Pripremi_slučajan,난수받기,slučajan_završiti_razgovor};
static void Zatvori_veza(void) {
    인증됨=셸시작됨=0;kanal_unos=0;
    if(veza_e05f319b)assh_session_release(veza_e05f319b);veza_e05f319b=0;
    if(ravnopravan_član_VALUE>=0)Zatvori_mreža(ravnopravan_član_VALUE);ravnopravan_član_VALUE=-1;naredba_TYPE=0;završiti_razgovor_Stanje=-1;닫을예정=0;
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
uintptr_t pano_završiti_razgovor_udaljeno_naredba(uintptr_t Stanje_VALUE){if(셸시작됨&&naredba_TYPE)završiti_razgovor_Stanje=(int)Stanje_VALUE;return 0;}
uintptr_t pano_udaljeno_čekaj(uintptr_t Stanje_VALUE){ljuska_Čekanje=Stanje_VALUE!=0;return 0;}
static int Pripremi_ljuska(void) {
    if(Slušanje_sudionik>=0)return 0;
    if(!문맥){
        assh_status_t GREŠKA=assh_context_create(&문맥,ASSH_SERVER,Pripremi_Memorija,0,&slučajan_generator,0);
        if(GREŠKA)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *postupak_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        GREŠKA=assh_algo_register(문맥,ASSH_SAFETY_WEAK,postupak_MODE);
        if(!GREŠKA)GREŠKA=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=uređaj_Ključ;
        if(!GREŠKA)GREŠKA=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(uređaj_Ključ));
        if(GREŠKA){진단("SSH init error ",GREŠKA);assh_context_release(문맥);문맥=0;return -5;}
    }
    int prebaciti_VALUE=통신끝점만들기(1);if(prebaciti_VALUE<0)return prebaciti_VALUE;통신주소재사용(prebaciti_VALUE);
    int REZULTAT=NET_BIND(prebaciti_VALUE,0,22);if(!REZULTAT)REZULTAT=NET_osluškivati(prebaciti_VALUE);
    if(REZULTAT<0){Zatvori_mreža(prebaciti_VALUE);return REZULTAT;}Slušanje_sudionik=prebaciti_VALUE;return 0;
}
uintptr_t pano_paralelna_sesija(uintptr_t 종류,uintptr_t Aktivnost) {
    if(종류==1)return(uint32_t)kontrola_udaljeno_zaslon(Aktivnost);
    if(Aktivnost==0){Zatvori_veza();if(Slušanje_sudionik>=0)Zatvori_mreža(Slušanje_sudionik);Slušanje_sudionik=-1;return 0;}
    if(Aktivnost==1){pokretanje_pogreška=Pripremi_ljuska();return(uint32_t)pokretanje_pogreška;}
    return(uint32_t)(Slušanje_sudionik>=0?1:pokretanje_pogreška);
}
void Pripremi_udaljeno(void){pokretanje_pogreška=Pripremi_ljuska();kontrola_udaljeno_zaslon(1);}
static int 같은말(const struct assh_cbuffer_s *podaci,const char *Word_SMS) {
    size_t 길이=strlen(Word_SMS);return podaci->size==길이&&!memcmp(podaci->data,Word_SMS,길이);
}
static int Terminal_zahtjev(const struct assh_cbuffer_s *podaci) {
    if(podaci->size<24)return 0;
    const unsigned char *podaci_položaj=podaci->data;unsigned 길이=assh_load_u32(podaci_položaj);
    if(길이>128||podaci->size<길이+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(podaci_položaj+4+길이+16);
    return MODE_VALUE<=2048&&podaci->size==길이+24+MODE_VALUE;
}
static void ustroj_zahtjev(struct assh_event_request_s *Događaj) {
    if(!인증됨||Događaj->ch!=kanal_unos||!kanal_unos)return;
    if(같은말(&Događaj->type,"pty-req")) {
        if(!셸시작됨&&Terminal_zahtjev(&Događaj->rq_data))Događaj->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Događaj->type,"window-change")) {
        if(셸시작됨&&Događaj->rq_data.size==16)Događaj->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!ljuska_Čekanje)return;
    const unsigned char *Naredba=0;unsigned 길이=0;
    if(같은말(&Događaj->type,"exec")) {
        if(Događaj->rq_data.size<4)return;
        길이=assh_load_u32(Događaj->rq_data.data);
        if(!길이||길이>2048||Događaj->rq_data.size!=길이+4)return;
        Naredba=Događaj->rq_data.data+4;
        for(unsigned 순번=0;순번<길이;순번++)if(!Naredba[순번])return;
        naredba_TYPE=1;
    }else if(!같은말(&Događaj->type,"shell")||Događaj->rq_data.size)return;
    if(sizeof(입력줄)-입력수<길이+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(길이)원격입력넣기(Naredba,길이);원격입력넣기(&끝,1);
    셸시작됨=1;Događaj->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!naredba_TYPE){const char *안내="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*안내)원격출력(*안내++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Slušanje_sudionik<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(ravnopravan_član_VALUE<0){if(NOW_VALUE<재접속시각)return;ravnopravan_član_VALUE=NET_prihvatiti(Slušanje_sudionik);if(ravnopravan_član_VALUE<0)return;
        veza_TIME=NOW_VALUE;assh_status_t GREŠKA=assh_session_create(문맥,&veza_e05f319b);
        if(GREŠKA){veza_e05f319b=0;진단("SSH session error ",GREŠKA);Zatvori_veza();return;}}
    if((!인증됨&&NOW_VALUE-veza_TIME>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){Zatvori_veza();return;}
    if(kanal_unos&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t GREŠKA=assh_channel_data(kanal_unos,출력줄+출력앞,&수);
            if(!GREŠKA){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(GREŠKA!=ASSH_NO_DATA){Zatvori_veza();return;}
        }
        if(završiti_razgovor_Stanje>=0&&!출력수){unsigned char Stanje_VALUE[4];assh_store_u32(Stanje_VALUE,(uint32_t)završiti_razgovor_Stanje);
            if(assh_request(veza_e05f319b,kanal_unos,"exit-status",11,Stanje_VALUE,4,0)||assh_channel_eof(kanal_unos)||assh_channel_close(kanal_unos)) {Zatvori_veza();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s Događaj;
        if(!assh_event_get(veza_e05f319b,&Događaj,NOW_VALUE/1000)){Zatvori_veza();return;}
        assh_status_t GREŠKA=ASSH_OK;int 쉬기=0,prekinuti_vezu_sudionik=0;
        switch(Događaj.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(ravnopravan_član_VALUE,Događaj.transport.read.buf.data,Događaj.transport.read.buf.size);
            if(수>0)Događaj.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else prekinuti_vezu_sudionik=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=NET_zapisivanje(ravnopravan_član_VALUE,Događaj.transport.write.buf.data,Događaj.transport.write.buf.size);
            if(수>0)Događaj.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else prekinuti_vezu_sudionik=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Događaj.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Događaj.userauth_server.methods.retries>3)Događaj.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *podaci=&Događaj.userauth_server.password;
            if(같은말(&podaci->username,"user")&&podaci->password.size<=256&&!podaci->new_password.size) {
                unsigned char sažetak_VALUE[32];udaljeno_sažetak(podaci->password.data,podaci->password.size,sažetak_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=sažetak_VALUE[순번]^ljuska_lozinka_sažetak[순번];memset(sažetak_VALUE,0,32);
                if(!차이)podaci->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *podaci=&Događaj.connection.channel_open;
            if(인증됨&&!kanal_unos&&ljuska_Čekanje&&같은말(&podaci->type,"session")&&!podaci->rq_data.size) {
                podaci->reply=ASSH_CONNECTION_REPLY_SUCCESS;podaci->pkt_size=4096;
                podaci->win_size=-1;kanal_unos=podaci->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: ustroj_zahtjev(&Događaj.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *podaci=&Događaj.connection.channel_data;
            if(!셸시작됨||podaci->ch!=kanal_unos||podaci->ext){prekinuti_vezu_sudionik=1;break;}
            unsigned 수=podaci->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(podaci->data.data[순번]==4){završiti_razgovor_Stanje=0;수=순번;podaci->transferred=podaci->data.size;break;}
            원격입력넣기(podaci->data.data,수);if(!podaci->transferred)podaci->transferred=수;
            if(!수&&završiti_razgovor_Stanje<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: kanal_unos=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Događaj.session.error.code);prekinuti_vezu_sudionik=1;break;
        case ASSH_EVENT_DISCONNECT: prekinuti_vezu_sudionik=1;break;
        default: break;
        }
        assh_event_done(veza_e05f319b,&Događaj,GREŠKA);
        if(prekinuti_vezu_sudionik){Zatvori_veza();return;}if(쉬기)return;
    }
}
