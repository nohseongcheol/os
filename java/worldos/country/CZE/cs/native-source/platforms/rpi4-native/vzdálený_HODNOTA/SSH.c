/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "vzdálený_HODNOTA.h"
#include "šifrování_vzpěra.h"
#include "Profil.h"
#include "../síť_Štos/síť_Štos.h"
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
static struct assh_context_s *kontext_HODNOTA;
static struct assh_session_s *kontakt_e05f319b;
static struct assh_channel_s *Kanál_položka;
static int Poslouchám_účastník=-1,partner_HODNOTA=-1,인증됨,셸시작됨,příkaz_TYP,konec_Stav=-1,닫을예정,spuštění_chyba,prostředí_Čekám;
static uintptr_t kontakt_ČAS,재접속시각,uzávěrka_ČAS;
static unsigned char vstup_čára[8192],výstup_čára[65536];
static unsigned 입력앞,vstup_POČET,출력앞,výstup_POČET,Předchozí_výstup;
static void 진단(const char *Word_SMS,unsigned HODNOTA) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char číslice_HODNOTA[12];unsigned číslo=0;do{číslice_HODNOTA[číslo++]='0'+HODNOTA%10;HODNOTA/=10;}while(HODNOTA);
    while(číslo)보드글자쓰기(číslice_HODNOTA[--číslo]);보드글자쓰기(10);
}
static assh_status_t Připravit_Paměť(void *data,void **Adresa,size_t Velikost,enum assh_alloc_type_e Druh_HODNOTA) {
    (void)data;(void)Druh_HODNOTA;
    if(!Velikost){verze_vzdálený(*Adresa);*Adresa=0;return ASSH_OK;}
    void *새주소=원격재할당(*Adresa,Velikost);
    if(!새주소)return ASSH_ERR_MEM;*Adresa=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *data,const struct assh_buffer_s *počáteční_hodnota) {
    (void)data;(void)počáteční_hodnota;unsigned char zkoušky[32];int VÝSLEDEK=원격난수(zkoušky,sizeof(zkoušky));memset(zkoušky,0,sizeof(zkoušky));
    return VÝSLEDEK?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *data,uint8_t *VÝSLEDEK,size_t délka_HODNOTA,uint_fast8_t Druh_HODNOTA) {
    (void)data;(void)Druh_HODNOTA;if(délka_HODNOTA>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(VÝSLEDEK,délka_HODNOTA)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *data){(void)data;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void Zavřít_kontakt(void) {
    인증됨=셸시작됨=0;Kanál_položka=0;
    if(kontakt_e05f319b)assh_session_release(kontakt_e05f319b);kontakt_e05f319b=0;
    if(partner_HODNOTA>=0)Zavřít_síť(partner_HODNOTA);partner_HODNOTA=-1;příkaz_TYP=0;konec_Stav=-1;닫을예정=0;
    입력앞=vstup_POČET=출력앞=výstup_POČET=Předchozí_výstup=0;재접속시각=보드밀리초()+250;
}
int novinky_vzdálený_vstup(const unsigned char *data,unsigned číslo) {
    if(číslo>sizeof(vstup_čára)-vstup_POČET)return -11;
    for(unsigned 순번=0;순번<číslo;순번++)vstup_čára[(입력앞+vstup_POČET++)%sizeof(vstup_čára)]=data[순번];return číslo;
}
int vzdálený_vstup(void) {
    if(!vstup_POČET)return -1;int znak_HODNOTA=vstup_čára[입력앞];입력앞=(입력앞+1)%sizeof(vstup_čára);vstup_POČET--;return znak_HODNOTA;
}
void vzdálený_výstup(unsigned char znak_HODNOTA) {
    if(!셸시작됨||닫을예정)return;
    unsigned režim_přidávání=znak_HODNOTA==10&&Předchozí_výstup!=13;
    if(výstup_POČET+1+režim_přidávání>sizeof(výstup_čára)){닫을예정=2;return;}
    if(režim_přidávání)výstup_čára[(출력앞+výstup_POČET++)%sizeof(výstup_čára)]=13;
    výstup_čára[(출력앞+výstup_POČET++)%sizeof(výstup_čára)]=znak_HODNOTA;Předchozí_výstup=znak_HODNOTA;
}
uintptr_t Panel_konec_vzdálený_příkaz(uintptr_t Stav_HODNOTA){if(셸시작됨&&příkaz_TYP)konec_Stav=(int)Stav_HODNOTA;return 0;}
uintptr_t Panel_vzdálený_počkej(uintptr_t Stav_HODNOTA){prostředí_Čekám=Stav_HODNOTA!=0;return 0;}
static int Připravit_prostředí(void) {
    if(Poslouchám_účastník>=0)return 0;
    if(!kontext_HODNOTA){
        assh_status_t chyba=assh_context_create(&kontext_HODNOTA,ASSH_SERVER,Připravit_Paměť,0,&난수기,0);
        if(chyba)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metoda_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        chyba=assh_algo_register(kontext_HODNOTA,ASSH_SAFETY_WEAK,metoda_MODE);
        if(!chyba)chyba=assh_service_register_va(kontext_HODNOTA,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *Klíč_materiál=mobilní_Klíč;
        if(!chyba)chyba=assh_key_load(kontext_HODNOTA,assh_context_keys(kontext_HODNOTA),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&Klíč_materiál,sizeof(mobilní_Klíč));
        if(chyba){진단("SSH init error ",chyba);assh_context_release(kontext_HODNOTA);kontext_HODNOTA=0;return -5;}
    }
    int port_HODNOTA=Create_soket_účastník(1);if(port_HODNOTA<0)return port_HODNOTA;통신주소재사용(port_HODNOTA);
    int VÝSLEDEK=čistý_vázat(port_HODNOTA,0,22);if(!VÝSLEDEK)VÝSLEDEK=čistý_naslouchat(port_HODNOTA);
    if(VÝSLEDEK<0){Zavřít_síť(port_HODNOTA);return VÝSLEDEK;}Poslouchám_účastník=port_HODNOTA;return 0;
}
uintptr_t Panel_stínový_provoz(uintptr_t Druh_HODNOTA,uintptr_t Akce) {
    if(Druh_HODNOTA==1)return(uint32_t)řízení_vzdálený_displej(Akce);
    if(Akce==0){Zavřít_kontakt();if(Poslouchám_účastník>=0)Zavřít_síť(Poslouchám_účastník);Poslouchám_účastník=-1;return 0;}
    if(Akce==1){spuštění_chyba=Připravit_prostředí();return(uint32_t)spuštění_chyba;}
    return(uint32_t)(Poslouchám_účastník>=0?1:spuštění_chyba);
}
void Připravit_vzdálený(void){spuštění_chyba=Připravit_prostředí();řízení_vzdálený_displej(1);}
static int 같은말(const struct assh_cbuffer_s *data,const char *Word_SMS) {
    size_t délka_HODNOTA=strlen(Word_SMS);return data->size==délka_HODNOTA&&!memcmp(data->data,Word_SMS,délka_HODNOTA);
}
static int Terminál_žádost(const struct assh_cbuffer_s *data) {
    if(data->size<24)return 0;
    const unsigned char *data_pozice=data->data;unsigned délka_HODNOTA=assh_load_u32(data_pozice);
    if(délka_HODNOTA>128||data->size<délka_HODNOTA+24)return 0;
    unsigned MODE_HODNOTA=assh_load_u32(data_pozice+4+délka_HODNOTA+16);
    return MODE_HODNOTA<=2048&&data->size==délka_HODNOTA+24+MODE_HODNOTA;
}
static void úchyt_žádost(struct assh_event_request_s *Události) {
    if(!인증됨||Události->ch!=Kanál_položka||!Kanál_položka)return;
    if(같은말(&Události->type,"pty-req")) {
        if(!셸시작됨&&Terminál_žádost(&Události->rq_data))Události->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Události->type,"window-change")) {
        if(셸시작됨&&Události->rq_data.size==16)Události->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!prostředí_Čekám)return;
    const unsigned char *příkaz=0;unsigned délka_HODNOTA=0;
    if(같은말(&Události->type,"exec")) {
        if(Události->rq_data.size<4)return;
        délka_HODNOTA=assh_load_u32(Události->rq_data.data);
        if(!délka_HODNOTA||délka_HODNOTA>2048||Události->rq_data.size!=délka_HODNOTA+4)return;
        příkaz=Události->rq_data.data+4;
        for(unsigned 순번=0;순번<délka_HODNOTA;순번++)if(!příkaz[순번])return;
        příkaz_TYP=1;
    }else if(!같은말(&Události->type,"shell")||Události->rq_data.size)return;
    if(sizeof(vstup_čára)-vstup_POČET<délka_HODNOTA+2)return;
    const unsigned char 지움=21,끝=13;
    novinky_vzdálený_vstup(&지움,1);if(délka_HODNOTA)novinky_vzdálený_vstup(příkaz,délka_HODNOTA);novinky_vzdálený_vstup(&끝,1);
    셸시작됨=1;Události->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!příkaz_TYP){const char *안내="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*안내)vzdálený_výstup(*안내++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Poslouchám_účastník<0)return;
    uintptr_t NOW_HODNOTA=보드밀리초();
    if(partner_HODNOTA<0){if(NOW_HODNOTA<재접속시각)return;partner_HODNOTA=čistý_přijmout(Poslouchám_účastník);if(partner_HODNOTA<0)return;
        kontakt_ČAS=NOW_HODNOTA;assh_status_t chyba=assh_session_create(kontext_HODNOTA,&kontakt_e05f319b);
        if(chyba){kontakt_e05f319b=0;진단("SSH session error ",chyba);Zavřít_kontakt();return;}}
    if((!인증됨&&NOW_HODNOTA-kontakt_ČAS>30000)||닫을예정==2||(닫을예정&&NOW_HODNOTA>=uzávěrka_ČAS)){Zavřít_kontakt();return;}
    if(Kanál_položka&&셸시작됨&&!닫을예정) {
        if(výstup_POČET){size_t číslo=sizeof(výstup_čára)-출력앞;if(číslo>výstup_POČET)číslo=výstup_POČET;if(číslo>2048)číslo=2048;
            assh_status_t chyba=assh_channel_data(Kanál_položka,výstup_čára+출력앞,&číslo);
            if(!chyba){출력앞=(출력앞+číslo)%sizeof(výstup_čára);výstup_POČET-=číslo;}
            else if(chyba!=ASSH_NO_DATA){Zavřít_kontakt();return;}
        }
        if(konec_Stav>=0&&!výstup_POČET){unsigned char Stav_HODNOTA[4];assh_store_u32(Stav_HODNOTA,(uint32_t)konec_Stav);
            if(assh_request(kontakt_e05f319b,Kanál_položka,"exit-status",11,Stav_HODNOTA,4,0)||assh_channel_eof(Kanál_položka)||assh_channel_close(Kanál_položka)) {Zavřít_kontakt();return;}
            닫을예정=1;uzávěrka_ČAS=NOW_HODNOTA+3000;
        }
    }
    for(unsigned SEQUENCE_HODNOTA=0;SEQUENCE_HODNOTA<16;SEQUENCE_HODNOTA++) {
        struct assh_event_s Události;
        if(!assh_event_get(kontakt_e05f319b,&Události,NOW_HODNOTA/1000)){Zavřít_kontakt();return;}
        assh_status_t chyba=ASSH_OK;int 쉬기=0,odpojit_účastník=0;
        switch(Události.id) {
        case ASSH_EVENT_READ: {
            int číslo=통신읽기(partner_HODNOTA,Události.transport.read.buf.data,Události.transport.read.buf.size);
            if(číslo>0)Události.transport.read.transferred=číslo;
            else if(číslo==-11)쉬기=1;else odpojit_účastník=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int číslo=čistý_zápis(partner_HODNOTA,Události.transport.write.buf.data,Události.transport.write.buf.size);
            if(číslo>0)Události.transport.write.transferred=číslo;
            else if(číslo==-11)쉬기=1;else odpojit_účastník=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Události.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Události.userauth_server.methods.retries>3)Události.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *data=&Události.userauth_server.password;
            if(같은말(&data->username,"user")&&data->password.size<=256&&!data->new_password.size) {
                unsigned char souhrn_HODNOTA[32];vzdálený_souhrn(data->password.data,data->password.size,souhrn_HODNOTA);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=souhrn_HODNOTA[순번]^prostředí_heslo_souhrn[순번];memset(souhrn_HODNOTA,0,32);
                if(!차이)data->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *data=&Události.connection.channel_open;
            if(인증됨&&!Kanál_položka&&prostředí_Čekám&&같은말(&data->type,"session")&&!data->rq_data.size) {
                data->reply=ASSH_CONNECTION_REPLY_SUCCESS;data->pkt_size=4096;
                data->win_size=-1;Kanál_položka=data->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: úchyt_žádost(&Události.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *data=&Události.connection.channel_data;
            if(!셸시작됨||data->ch!=Kanál_položka||data->ext){odpojit_účastník=1;break;}
            unsigned číslo=data->data.size;if(číslo>sizeof(vstup_čára)-vstup_POČET)číslo=sizeof(vstup_čára)-vstup_POČET;
            for(unsigned 순번=0;순번<číslo;순번++)if(data->data.data[순번]==4){konec_Stav=0;číslo=순번;data->transferred=data->data.size;break;}
            novinky_vzdálený_vstup(data->data.data,číslo);if(!data->transferred)data->transferred=číslo;
            if(!číslo&&konec_Stav<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Kanál_položka=0;셸시작됨=0;닫을예정=1;uzávěrka_ČAS=NOW_HODNOTA+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Události.session.error.code);odpojit_účastník=1;break;
        case ASSH_EVENT_DISCONNECT: odpojit_účastník=1;break;
        default: break;
        }
        assh_event_done(kontakt_e05f319b,&Události,chyba);
        if(odpojit_účastník){Zavřít_kontakt();return;}if(쉬기)return;
    }
}
