/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "oddaljen_VALUE.h"
#include "kriptografija_Podpora.h"
#include "Profil.h"
#include "../mreža_Sklad/mreža_Sklad.h"
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
static struct assh_session_s *povezava_e05f319b;
static struct assh_channel_s *Kanal_vnos;
static int Poslušanje_končna_točka=-1,enakovreden_VALUE=-1,인증됨,셸시작됨,ukaz_Tip,končati_klic_stanje=-1,닫을예정,시작오류,lupina_Čakanje;
static uintptr_t povezava_čas,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char številka_VALUE[12];unsigned 수=0;do{številka_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(številka_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Pripravi_pomnilnik(void *podatki,void **naslov,size_t Velikost,enum assh_alloc_type_e 종류) {
    (void)podatki;(void)종류;
    if(!Velikost){izdaja_oddaljen(*naslov);*naslov=0;return ASSH_OK;}
    void *새주소=원격재할당(*naslov,Velikost);
    if(!새주소)return ASSH_ERR_MEM;*naslov=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *podatki,const struct assh_buffer_s *začetna_vrednost) {
    (void)podatki;(void)začetna_vrednost;unsigned char 시험[32];int REZULTAT=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return REZULTAT?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *podatki,uint8_t *REZULTAT,size_t 길이,uint_fast8_t 종류) {
    (void)podatki;(void)종류;if(길이>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(REZULTAT,길이)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *podatki){(void)podatki;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void Zapri_povezava(void) {
    인증됨=셸시작됨=0;Kanal_vnos=0;
    if(povezava_e05f319b)assh_session_release(povezava_e05f319b);povezava_e05f319b=0;
    if(enakovreden_VALUE>=0)Zapri_mreža(enakovreden_VALUE);enakovreden_VALUE=-1;ukaz_Tip=0;končati_klic_stanje=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *podatki,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=podatki[순번];return 수;
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
uintptr_t Tabla_končati_klic_oddaljen_ukaz(uintptr_t stanje_VALUE){if(셸시작됨&&ukaz_Tip)končati_klic_stanje=(int)stanje_VALUE;return 0;}
uintptr_t Tabla_oddaljen_počakaj(uintptr_t stanje_VALUE){lupina_Čakanje=stanje_VALUE!=0;return 0;}
static int Pripravi_lupina(void) {
    if(Poslušanje_končna_točka>=0)return 0;
    if(!문맥){
        assh_status_t NAPAKA=assh_context_create(&문맥,ASSH_SERVER,Pripravi_pomnilnik,0,&난수기,0);
        if(NAPAKA)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metoda_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        NAPAKA=assh_algo_register(문맥,ASSH_SAFETY_WEAK,metoda_MODE);
        if(!NAPAKA)NAPAKA=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=naprava_Ključ;
        if(!NAPAKA)NAPAKA=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(naprava_Ključ));
        if(NAPAKA){진단("SSH init error ",NAPAKA);assh_context_release(문맥);문맥=0;return -5;}
    }
    int vrata_VALUE=Ustvari_vtičnica_končna_točka(1);if(vrata_VALUE<0)return vrata_VALUE;통신주소재사용(vrata_VALUE);
    int REZULTAT=NET_BIND(vrata_VALUE,0,22);if(!REZULTAT)REZULTAT=NET_poslušati(vrata_VALUE);
    if(REZULTAT<0){Zapri_mreža(vrata_VALUE);return REZULTAT;}Poslušanje_končna_točka=vrata_VALUE;return 0;
}
uintptr_t Tabla_oddaljeni_nadzor(uintptr_t 종류,uintptr_t Dejanje) {
    if(종류==1)return(uint32_t)nadzor_oddaljen_zaslon(Dejanje);
    if(Dejanje==0){Zapri_povezava();if(Poslušanje_končna_točka>=0)Zapri_mreža(Poslušanje_končna_točka);Poslušanje_končna_točka=-1;return 0;}
    if(Dejanje==1){시작오류=Pripravi_lupina();return(uint32_t)시작오류;}
    return(uint32_t)(Poslušanje_končna_točka>=0?1:시작오류);
}
void Pripravi_oddaljen(void){시작오류=Pripravi_lupina();nadzor_oddaljen_zaslon(1);}
static int 같은말(const struct assh_cbuffer_s *podatki,const char *Word_SMS) {
    size_t 길이=strlen(Word_SMS);return podatki->size==길이&&!memcmp(podatki->data,Word_SMS,길이);
}
static int Terminal_zahteva(const struct assh_cbuffer_s *podatki) {
    if(podatki->size<24)return 0;
    const unsigned char *podatki_položaj=podatki->data;unsigned 길이=assh_load_u32(podatki_položaj);
    if(길이>128||podatki->size<길이+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(podatki_položaj+4+길이+16);
    return MODE_VALUE<=2048&&podatki->size==길이+24+MODE_VALUE;
}
static void ročica_zahteva(struct assh_event_request_s *dogodek) {
    if(!인증됨||dogodek->ch!=Kanal_vnos||!Kanal_vnos)return;
    if(같은말(&dogodek->type,"pty-req")) {
        if(!셸시작됨&&Terminal_zahteva(&dogodek->rq_data))dogodek->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&dogodek->type,"window-change")) {
        if(셸시작됨&&dogodek->rq_data.size==16)dogodek->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!lupina_Čakanje)return;
    const unsigned char *Ukaz=0;unsigned 길이=0;
    if(같은말(&dogodek->type,"exec")) {
        if(dogodek->rq_data.size<4)return;
        길이=assh_load_u32(dogodek->rq_data.data);
        if(!길이||길이>2048||dogodek->rq_data.size!=길이+4)return;
        Ukaz=dogodek->rq_data.data+4;
        for(unsigned 순번=0;순번<길이;순번++)if(!Ukaz[순번])return;
        ukaz_Tip=1;
    }else if(!같은말(&dogodek->type,"shell")||dogodek->rq_data.size)return;
    if(sizeof(입력줄)-입력수<길이+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(길이)원격입력넣기(Ukaz,길이);원격입력넣기(&끝,1);
    셸시작됨=1;dogodek->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!ukaz_Tip){const char *안내="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*안내)원격출력(*안내++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Poslušanje_končna_točka<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(enakovreden_VALUE<0){if(NOW_VALUE<재접속시각)return;enakovreden_VALUE=NET_sprejeti(Poslušanje_končna_točka);if(enakovreden_VALUE<0)return;
        povezava_čas=NOW_VALUE;assh_status_t NAPAKA=assh_session_create(문맥,&povezava_e05f319b);
        if(NAPAKA){povezava_e05f319b=0;진단("SSH session error ",NAPAKA);Zapri_povezava();return;}}
    if((!인증됨&&NOW_VALUE-povezava_čas>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){Zapri_povezava();return;}
    if(Kanal_vnos&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t NAPAKA=assh_channel_data(Kanal_vnos,출력줄+출력앞,&수);
            if(!NAPAKA){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(NAPAKA!=ASSH_NO_DATA){Zapri_povezava();return;}
        }
        if(končati_klic_stanje>=0&&!출력수){unsigned char stanje_VALUE[4];assh_store_u32(stanje_VALUE,(uint32_t)končati_klic_stanje);
            if(assh_request(povezava_e05f319b,Kanal_vnos,"exit-status",11,stanje_VALUE,4,0)||assh_channel_eof(Kanal_vnos)||assh_channel_close(Kanal_vnos)) {Zapri_povezava();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s dogodek;
        if(!assh_event_get(povezava_e05f319b,&dogodek,NOW_VALUE/1000)){Zapri_povezava();return;}
        assh_status_t NAPAKA=ASSH_OK;int 쉬기=0,prekiniti_povezavo_končna_točka=0;
        switch(dogodek.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(enakovreden_VALUE,dogodek.transport.read.buf.data,dogodek.transport.read.buf.size);
            if(수>0)dogodek.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else prekiniti_povezavo_končna_točka=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=NET_pisati(enakovreden_VALUE,dogodek.transport.write.buf.data,dogodek.transport.write.buf.size);
            if(수>0)dogodek.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else prekiniti_povezavo_končna_točka=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            dogodek.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(dogodek.userauth_server.methods.retries>3)dogodek.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *podatki=&dogodek.userauth_server.password;
            if(같은말(&podatki->username,"user")&&podatki->password.size<=256&&!podatki->new_password.size) {
                unsigned char povzetek_VALUE[32];oddaljen_povzetek(podatki->password.data,podatki->password.size,povzetek_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=povzetek_VALUE[순번]^lupina_geslo_povzetek[순번];memset(povzetek_VALUE,0,32);
                if(!차이)podatki->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *podatki=&dogodek.connection.channel_open;
            if(인증됨&&!Kanal_vnos&&lupina_Čakanje&&같은말(&podatki->type,"session")&&!podatki->rq_data.size) {
                podatki->reply=ASSH_CONNECTION_REPLY_SUCCESS;podatki->pkt_size=4096;
                podatki->win_size=-1;Kanal_vnos=podatki->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: ročica_zahteva(&dogodek.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *podatki=&dogodek.connection.channel_data;
            if(!셸시작됨||podatki->ch!=Kanal_vnos||podatki->ext){prekiniti_povezavo_končna_točka=1;break;}
            unsigned 수=podatki->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(podatki->data.data[순번]==4){končati_klic_stanje=0;수=순번;podatki->transferred=podatki->data.size;break;}
            원격입력넣기(podatki->data.data,수);if(!podatki->transferred)podatki->transferred=수;
            if(!수&&končati_klic_stanje<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Kanal_vnos=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",dogodek.session.error.code);prekiniti_povezavo_končna_točka=1;break;
        case ASSH_EVENT_DISCONNECT: prekiniti_povezavo_končna_točka=1;break;
        default: break;
        }
        assh_event_done(povezava_e05f319b,&dogodek,NAPAKA);
        if(prekiniti_povezavo_končna_točka){Zapri_povezava();return;}if(쉬기)return;
    }
}
