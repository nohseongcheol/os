/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "vzdialený_VALUE.h"
#include "kryptografia_Podpora.h"
#include "Profil.h"
#include "../sieť_Vrstvy/sieť_Vrstvy.h"
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
static struct assh_session_s *kontakt_e05f319b;
static struct assh_channel_s *Kanál_položka;
static int Počúvanie_účastník=-1,partnerský_uzol_VALUE=-1,인증됨,셸시작됨,príkaz_Typ,ukončiť_hovor_Stav=-1,닫을예정,spustenie_Chyba,셸대기중;
static uintptr_t kontakt_čas,재접속시각,닫는시각;
static unsigned char vstup_linka[8192],출력줄[65536];
static unsigned 입력앞,vstup_COUNT,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char číslica_VALUE[12];unsigned 수=0;do{číslica_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(číslica_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Pripraviť_Pamäť(void *údaje,void **adresa,size_t Veľkosť,enum assh_alloc_type_e 종류) {
    (void)údaje;(void)종류;
    if(!Veľkosť){vydať_vzdialený(*adresa);*adresa=0;return ASSH_OK;}
    void *새주소=원격재할당(*adresa,Veľkosť);
    if(!새주소)return ASSH_ERR_MEM;*adresa=새주소;return ASSH_OK;
}
static assh_status_t Pripraviť_náhodný(struct assh_context_s *údaje,const struct assh_buffer_s *počiatočná_hodnota) {
    (void)údaje;(void)počiatočná_hodnota;unsigned char 시험[32];int KR=vzdialený_náhodný(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return KR?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *údaje,uint8_t *KR,size_t dĺžka_VALUE,uint_fast8_t 종류) {
    (void)údaje;(void)종류;if(dĺžka_VALUE>65536)return ASSH_ERR_CRYPTO;
    return vzdialený_náhodný(KR,dĺžka_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void náhodný_ukončiť_hovor(struct assh_context_s *údaje){(void)údaje;}
static const struct assh_prng_s náhodný_generátor={Pripraviť_náhodný,난수받기,náhodný_ukončiť_hovor};
static void Zavrieť_kontakt(void) {
    인증됨=셸시작됨=0;Kanál_položka=0;
    if(kontakt_e05f319b)assh_session_release(kontakt_e05f319b);kontakt_e05f319b=0;
    if(partnerský_uzol_VALUE>=0)Zavrieť_sieť(partnerský_uzol_VALUE);partnerský_uzol_VALUE=-1;príkaz_Typ=0;ukončiť_hovor_Stav=-1;닫을예정=0;
    입력앞=vstup_COUNT=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int súhrnný_obsah_vzdialený_vstup(const unsigned char *údaje,unsigned 수) {
    if(수>sizeof(vstup_linka)-vstup_COUNT)return -11;
    for(unsigned 순번=0;순번<수;순번++)vstup_linka[(입력앞+vstup_COUNT++)%sizeof(vstup_linka)]=údaje[순번];return 수;
}
int vzdialený_vstup(void) {
    if(!vstup_COUNT)return -1;int znak_VALUE=vstup_linka[입력앞];입력앞=(입력앞+1)%sizeof(vstup_linka);vstup_COUNT--;return znak_VALUE;
}
void 원격출력(unsigned char znak_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned Pripojiť_MODE=znak_VALUE==10&&이전출력!=13;
    if(출력수+1+Pripojiť_MODE>sizeof(출력줄)){닫을예정=2;return;}
    if(Pripojiť_MODE)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=znak_VALUE;이전출력=znak_VALUE;
}
uintptr_t Panel_ukončiť_hovor_vzdialený_príkaz(uintptr_t Stav_VALUE){if(셸시작됨&&príkaz_Typ)ukončiť_hovor_Stav=(int)Stav_VALUE;return 0;}
uintptr_t Panel_vzdialený_počkaj(uintptr_t Stav_VALUE){셸대기중=Stav_VALUE!=0;return 0;}
static int 셸준비(void) {
    if(Počúvanie_účastník>=0)return 0;
    if(!문맥){
        assh_status_t chyba=assh_context_create(&문맥,ASSH_SERVER,Pripraviť_Pamäť,0,&náhodný_generátor,0);
        if(chyba)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metóda_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        chyba=assh_algo_register(문맥,ASSH_SAFETY_WEAK,metóda_MODE);
        if(!chyba)chyba=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=telefón_Kľúč;
        if(!chyba)chyba=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(telefón_Kľúč));
        if(chyba){진단("SSH init error ",chyba);assh_context_release(문맥);문맥=0;return -5;}
    }
    int port_VALUE=Create_soket_účastník(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int KR=NET_BIND(port_VALUE,0,22);if(!KR)KR=NET_načúvať(port_VALUE);
    if(KR<0){Zavrieť_sieť(port_VALUE);return KR;}Počúvanie_účastník=port_VALUE;return 0;
}
uintptr_t Panel_tieňové_ovládanie(uintptr_t 종류,uintptr_t Akcia) {
    if(종류==1)return(uint32_t)riadenie_vzdialený_displej(Akcia);
    if(Akcia==0){Zavrieť_kontakt();if(Počúvanie_účastník>=0)Zavrieť_sieť(Počúvanie_účastník);Počúvanie_účastník=-1;return 0;}
    if(Akcia==1){spustenie_Chyba=셸준비();return(uint32_t)spustenie_Chyba;}
    return(uint32_t)(Počúvanie_účastník>=0?1:spustenie_Chyba);
}
void Pripraviť_vzdialený(void){spustenie_Chyba=셸준비();riadenie_vzdialený_displej(1);}
static int 같은말(const struct assh_cbuffer_s *údaje,const char *Word_SMS) {
    size_t dĺžka_VALUE=strlen(Word_SMS);return údaje->size==dĺžka_VALUE&&!memcmp(údaje->data,Word_SMS,dĺžka_VALUE);
}
static int Terminál_požiadavka(const struct assh_cbuffer_s *údaje) {
    if(údaje->size<24)return 0;
    const unsigned char *údaje_pozícia=údaje->data;unsigned dĺžka_VALUE=assh_load_u32(údaje_pozícia);
    if(dĺžka_VALUE>128||údaje->size<dĺžka_VALUE+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(údaje_pozícia+4+dĺžka_VALUE+16);
    return MODE_VALUE<=2048&&údaje->size==dĺžka_VALUE+24+MODE_VALUE;
}
static void rukoväť_požiadavka(struct assh_event_request_s *Udalosť) {
    if(!인증됨||Udalosť->ch!=Kanál_položka||!Kanál_položka)return;
    if(같은말(&Udalosť->type,"pty-req")) {
        if(!셸시작됨&&Terminál_požiadavka(&Udalosť->rq_data))Udalosť->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Udalosť->type,"window-change")) {
        if(셸시작됨&&Udalosť->rq_data.size==16)Udalosť->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *Príkaz=0;unsigned dĺžka_VALUE=0;
    if(같은말(&Udalosť->type,"exec")) {
        if(Udalosť->rq_data.size<4)return;
        dĺžka_VALUE=assh_load_u32(Udalosť->rq_data.data);
        if(!dĺžka_VALUE||dĺžka_VALUE>2048||Udalosť->rq_data.size!=dĺžka_VALUE+4)return;
        Príkaz=Udalosť->rq_data.data+4;
        for(unsigned 순번=0;순번<dĺžka_VALUE;순번++)if(!Príkaz[순번])return;
        príkaz_Typ=1;
    }else if(!같은말(&Udalosť->type,"shell")||Udalosť->rq_data.size)return;
    if(sizeof(vstup_linka)-vstup_COUNT<dĺžka_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    súhrnný_obsah_vzdialený_vstup(&지움,1);if(dĺžka_VALUE)súhrnný_obsah_vzdialený_vstup(Príkaz,dĺžka_VALUE);súhrnný_obsah_vzdialený_vstup(&끝,1);
    셸시작됨=1;Udalosť->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!príkaz_Typ){const char *안내="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*안내)원격출력(*안내++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Počúvanie_účastník<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(partnerský_uzol_VALUE<0){if(NOW_VALUE<재접속시각)return;partnerský_uzol_VALUE=NET_prijať(Počúvanie_účastník);if(partnerský_uzol_VALUE<0)return;
        kontakt_čas=NOW_VALUE;assh_status_t chyba=assh_session_create(문맥,&kontakt_e05f319b);
        if(chyba){kontakt_e05f319b=0;진단("SSH session error ",chyba);Zavrieť_kontakt();return;}}
    if((!인증됨&&NOW_VALUE-kontakt_čas>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){Zavrieť_kontakt();return;}
    if(Kanál_položka&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t chyba=assh_channel_data(Kanál_položka,출력줄+출력앞,&수);
            if(!chyba){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(chyba!=ASSH_NO_DATA){Zavrieť_kontakt();return;}
        }
        if(ukončiť_hovor_Stav>=0&&!출력수){unsigned char Stav_VALUE[4];assh_store_u32(Stav_VALUE,(uint32_t)ukončiť_hovor_Stav);
            if(assh_request(kontakt_e05f319b,Kanál_položka,"exit-status",11,Stav_VALUE,4,0)||assh_channel_eof(Kanál_položka)||assh_channel_close(Kanál_položka)) {Zavrieť_kontakt();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s Udalosť;
        if(!assh_event_get(kontakt_e05f319b,&Udalosť,NOW_VALUE/1000)){Zavrieť_kontakt();return;}
        assh_status_t chyba=ASSH_OK;int 쉬기=0,odpojiť_účastník=0;
        switch(Udalosť.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(partnerský_uzol_VALUE,Udalosť.transport.read.buf.data,Udalosť.transport.read.buf.size);
            if(수>0)Udalosť.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else odpojiť_účastník=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=NET_zapísať(partnerský_uzol_VALUE,Udalosť.transport.write.buf.data,Udalosť.transport.write.buf.size);
            if(수>0)Udalosť.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else odpojiť_účastník=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Udalosť.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Udalosť.userauth_server.methods.retries>3)Udalosť.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *údaje=&Udalosť.userauth_server.password;
            if(같은말(&údaje->username,"user")&&údaje->password.size<=256&&!údaje->new_password.size) {
                unsigned char súhrn_VALUE[32];vzdialený_súhrn(údaje->password.data,údaje->password.size,súhrn_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=súhrn_VALUE[순번]^셸암호요약[순번];memset(súhrn_VALUE,0,32);
                if(!차이)údaje->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *údaje=&Udalosť.connection.channel_open;
            if(인증됨&&!Kanál_položka&&셸대기중&&같은말(&údaje->type,"session")&&!údaje->rq_data.size) {
                údaje->reply=ASSH_CONNECTION_REPLY_SUCCESS;údaje->pkt_size=4096;
                údaje->win_size=-1;Kanál_položka=údaje->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: rukoväť_požiadavka(&Udalosť.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *údaje=&Udalosť.connection.channel_data;
            if(!셸시작됨||údaje->ch!=Kanál_položka||údaje->ext){odpojiť_účastník=1;break;}
            unsigned 수=údaje->data.size;if(수>sizeof(vstup_linka)-vstup_COUNT)수=sizeof(vstup_linka)-vstup_COUNT;
            for(unsigned 순번=0;순번<수;순번++)if(údaje->data.data[순번]==4){ukončiť_hovor_Stav=0;수=순번;údaje->transferred=údaje->data.size;break;}
            súhrnný_obsah_vzdialený_vstup(údaje->data.data,수);if(!údaje->transferred)údaje->transferred=수;
            if(!수&&ukončiť_hovor_Stav<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Kanál_položka=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Udalosť.session.error.code);odpojiť_účastník=1;break;
        case ASSH_EVENT_DISCONNECT: odpojiť_účastník=1;break;
        default: break;
        }
        assh_event_done(kontakt_e05f319b,&Udalosť,chyba);
        if(odpojiť_účastník){Zavrieť_kontakt();return;}if(쉬기)return;
    }
}
