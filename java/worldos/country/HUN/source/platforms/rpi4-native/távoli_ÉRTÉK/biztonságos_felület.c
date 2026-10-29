/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "távoli_ÉRTÉK.h"
#include "kriptográfia_támogat.h"
#include "Profil.h"
#include "../hálózat_Sor/hálózat_Sor.h"
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
static struct assh_context_s *környezet_ÉRTÉK;
static struct assh_session_s *ismerős_e05f319b;
static struct assh_channel_s *Csatorna_bejegyzés;
static int Hallgatás_végpont=-1,társ_ÉRTÉK=-1,인증됨,셸시작됨,parancs_beír,megszüntet_Állapot=-1,닫을예정,rendszerindítás_hiba,felület_Várok;
static uintptr_t ismerős_IDŐ,재접속시각,zárás_IDŐ;
static unsigned char bevitel_sor[8192],kimenet_sor[65536];
static unsigned 입력앞,bevitel_DARAB,출력앞,kimenet_DARAB,Előző_kimenet;
static void 진단(const char *szó_SMS,unsigned ÉRTÉK) {
    while(*szó_SMS)보드글자쓰기(*szó_SMS++);
    char számjegy_ÉRTÉK[12];unsigned szám=0;do{számjegy_ÉRTÉK[szám++]='0'+ÉRTÉK%10;ÉRTÉK/=10;}while(ÉRTÉK);
    while(szám)보드글자쓰기(számjegy_ÉRTÉK[--szám]);보드글자쓰기(10);
}
static assh_status_t Előkészítés_Memória(void *adat,void **CÍM,size_t Méret,enum assh_alloc_type_e Altípus_ÉRTÉK) {
    (void)adat;(void)Altípus_ÉRTÉK;
    if(!Méret){kiad_távoli(*CÍM);*CÍM=0;return ASSH_OK;}
    void *새주소=원격재할당(*CÍM,Méret);
    if(!새주소)return ASSH_ERR_MEM;*CÍM=새주소;return ASSH_OK;
}
static assh_status_t Előkészítés_véletlenszerű(struct assh_context_s *adat,const struct assh_buffer_s *kezdőérték) {
    (void)adat;(void)kezdőérték;unsigned char 시험[32];int KR=távoli_véletlenszerű(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return KR?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *adat,uint8_t *KR,size_t hossz_ÉRTÉK,uint_fast8_t Altípus_ÉRTÉK) {
    (void)adat;(void)Altípus_ÉRTÉK;if(hossz_ÉRTÉK>65536)return ASSH_ERR_CRYPTO;
    return távoli_véletlenszerű(KR,hossz_ÉRTÉK)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void véletlenszerű_megszüntet(struct assh_context_s *adat){(void)adat;}
static const struct assh_prng_s véletlenszerű_generátor={Előkészítés_véletlenszerű,난수받기,véletlenszerű_megszüntet};
static void bezár_ismerős(void) {
    인증됨=셸시작됨=0;Csatorna_bejegyzés=0;
    if(ismerős_e05f319b)assh_session_release(ismerős_e05f319b);ismerős_e05f319b=0;
    if(társ_ÉRTÉK>=0)bezár_hálózat(társ_ÉRTÉK);társ_ÉRTÉK=-1;parancs_beír=0;megszüntet_Állapot=-1;닫을예정=0;
    입력앞=bevitel_DARAB=출력앞=kimenet_DARAB=Előző_kimenet=0;재접속시각=보드밀리초()+250;
}
int csatorna_távoli_bevitel(const unsigned char *adat,unsigned szám) {
    if(szám>sizeof(bevitel_sor)-bevitel_DARAB)return -11;
    for(unsigned 순번=0;순번<szám;순번++)bevitel_sor[(입력앞+bevitel_DARAB++)%sizeof(bevitel_sor)]=adat[순번];return szám;
}
int távoli_bevitel(void) {
    if(!bevitel_DARAB)return -1;int karakter_ÉRTÉK=bevitel_sor[입력앞];입력앞=(입력앞+1)%sizeof(bevitel_sor);bevitel_DARAB--;return karakter_ÉRTÉK;
}
void távoli_kimenet(unsigned char karakter_ÉRTÉK) {
    if(!셸시작됨||닫을예정)return;
    unsigned hozzáfűz_mód=karakter_ÉRTÉK==10&&Előző_kimenet!=13;
    if(kimenet_DARAB+1+hozzáfűz_mód>sizeof(kimenet_sor)){닫을예정=2;return;}
    if(hozzáfűz_mód)kimenet_sor[(출력앞+kimenet_DARAB++)%sizeof(kimenet_sor)]=13;
    kimenet_sor[(출력앞+kimenet_DARAB++)%sizeof(kimenet_sor)]=karakter_ÉRTÉK;Előző_kimenet=karakter_ÉRTÉK;
}
uintptr_t fal_megszüntet_távoli_parancs(uintptr_t Állapot_ÉRTÉK){if(셸시작됨&&parancs_beír)megszüntet_Állapot=(int)Állapot_ÉRTÉK;return 0;}
uintptr_t fal_távoli_várj(uintptr_t Állapot_ÉRTÉK){felület_Várok=Állapot_ÉRTÉK!=0;return 0;}
static int Előkészítés_felület(void) {
    if(Hallgatás_végpont>=0)return 0;
    if(!környezet_ÉRTÉK){
        assh_status_t HIBA=assh_context_create(&környezet_ÉRTÉK,ASSH_SERVER,Előkészítés_Memória,0,&véletlenszerű_generátor,0);
        if(HIBA)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metódus_mód[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        HIBA=assh_algo_register(környezet_ÉRTÉK,ASSH_SAFETY_WEAK,metódus_mód);
        if(!HIBA)HIBA=assh_service_register_va(környezet_ÉRTÉK,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=mobil_Kulcs;
        if(!HIBA)HIBA=assh_key_load(környezet_ÉRTÉK,assh_context_keys(környezet_ÉRTÉK),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(mobil_Kulcs));
        if(HIBA){진단("SSH init error ",HIBA);assh_context_release(környezet_ÉRTÉK);környezet_ÉRTÉK=0;return -5;}
    }
    int port_ÉRTÉK=készít_szoftvercsatorna_végpont(1);if(port_ÉRTÉK<0)return port_ÉRTÉK;통신주소재사용(port_ÉRTÉK);
    int KR=NET_BIND(port_ÉRTÉK,0,22);if(!KR)KR=NET_figyelés(port_ÉRTÉK);
    if(KR<0){bezár_hálózat(port_ÉRTÉK);return KR;}Hallgatás_végpont=port_ÉRTÉK;return 0;
}
uintptr_t fal_távkezelés(uintptr_t Altípus_ÉRTÉK,uintptr_t Művelet) {
    if(Altípus_ÉRTÉK==1)return(uint32_t)vezérlő_távoli_kijelző(Művelet);
    if(Művelet==0){bezár_ismerős();if(Hallgatás_végpont>=0)bezár_hálózat(Hallgatás_végpont);Hallgatás_végpont=-1;return 0;}
    if(Művelet==1){rendszerindítás_hiba=Előkészítés_felület();return(uint32_t)rendszerindítás_hiba;}
    return(uint32_t)(Hallgatás_végpont>=0?1:rendszerindítás_hiba);
}
void Előkészítés_távoli(void){rendszerindítás_hiba=Előkészítés_felület();vezérlő_távoli_kijelző(1);}
static int 같은말(const struct assh_cbuffer_s *adat,const char *szó_SMS) {
    size_t hossz_ÉRTÉK=strlen(szó_SMS);return adat->size==hossz_ÉRTÉK&&!memcmp(adat->data,szó_SMS,hossz_ÉRTÉK);
}
static int Terminál_kérés(const struct assh_cbuffer_s *adat) {
    if(adat->size<24)return 0;
    const unsigned char *adat_pozíció=adat->data;unsigned hossz_ÉRTÉK=assh_load_u32(adat_pozíció);
    if(hossz_ÉRTÉK>128||adat->size<hossz_ÉRTÉK+24)return 0;
    unsigned mód_ÉRTÉK=assh_load_u32(adat_pozíció+4+hossz_ÉRTÉK+16);
    return mód_ÉRTÉK<=2048&&adat->size==hossz_ÉRTÉK+24+mód_ÉRTÉK;
}
static void leíró_kérés(struct assh_event_request_s *Esemény) {
    if(!인증됨||Esemény->ch!=Csatorna_bejegyzés||!Csatorna_bejegyzés)return;
    if(같은말(&Esemény->type,"pty-req")) {
        if(!셸시작됨&&Terminál_kérés(&Esemény->rq_data))Esemény->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Esemény->type,"window-change")) {
        if(셸시작됨&&Esemény->rq_data.size==16)Esemény->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!felület_Várok)return;
    const unsigned char *Parancs=0;unsigned hossz_ÉRTÉK=0;
    if(같은말(&Esemény->type,"exec")) {
        if(Esemény->rq_data.size<4)return;
        hossz_ÉRTÉK=assh_load_u32(Esemény->rq_data.data);
        if(!hossz_ÉRTÉK||hossz_ÉRTÉK>2048||Esemény->rq_data.size!=hossz_ÉRTÉK+4)return;
        Parancs=Esemény->rq_data.data+4;
        for(unsigned 순번=0;순번<hossz_ÉRTÉK;순번++)if(!Parancs[순번])return;
        parancs_beír=1;
    }else if(!같은말(&Esemény->type,"shell")||Esemény->rq_data.size)return;
    if(sizeof(bevitel_sor)-bevitel_DARAB<hossz_ÉRTÉK+2)return;
    const unsigned char 지움=21,끝=13;
    csatorna_távoli_bevitel(&지움,1);if(hossz_ÉRTÉK)csatorna_távoli_bevitel(Parancs,hossz_ÉRTÉK);csatorna_távoli_bevitel(&끝,1);
    셸시작됨=1;Esemény->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!parancs_beír){const char *fontos_fájl_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*fontos_fájl_eb81d7d9)távoli_kimenet(*fontos_fájl_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Hallgatás_végpont<0)return;
    uintptr_t MOST_ÉRTÉK=보드밀리초();
    if(társ_ÉRTÉK<0){if(MOST_ÉRTÉK<재접속시각)return;társ_ÉRTÉK=NET_elfogad(Hallgatás_végpont);if(társ_ÉRTÉK<0)return;
        ismerős_IDŐ=MOST_ÉRTÉK;assh_status_t HIBA=assh_session_create(környezet_ÉRTÉK,&ismerős_e05f319b);
        if(HIBA){ismerős_e05f319b=0;진단("SSH session error ",HIBA);bezár_ismerős();return;}}
    if((!인증됨&&MOST_ÉRTÉK-ismerős_IDŐ>30000)||닫을예정==2||(닫을예정&&MOST_ÉRTÉK>=zárás_IDŐ)){bezár_ismerős();return;}
    if(Csatorna_bejegyzés&&셸시작됨&&!닫을예정) {
        if(kimenet_DARAB){size_t szám=sizeof(kimenet_sor)-출력앞;if(szám>kimenet_DARAB)szám=kimenet_DARAB;if(szám>2048)szám=2048;
            assh_status_t HIBA=assh_channel_data(Csatorna_bejegyzés,kimenet_sor+출력앞,&szám);
            if(!HIBA){출력앞=(출력앞+szám)%sizeof(kimenet_sor);kimenet_DARAB-=szám;}
            else if(HIBA!=ASSH_NO_DATA){bezár_ismerős();return;}
        }
        if(megszüntet_Állapot>=0&&!kimenet_DARAB){unsigned char Állapot_ÉRTÉK[4];assh_store_u32(Állapot_ÉRTÉK,(uint32_t)megszüntet_Állapot);
            if(assh_request(ismerős_e05f319b,Csatorna_bejegyzés,"exit-status",11,Állapot_ÉRTÉK,4,0)||assh_channel_eof(Csatorna_bejegyzés)||assh_channel_close(Csatorna_bejegyzés)) {bezár_ismerős();return;}
            닫을예정=1;zárás_IDŐ=MOST_ÉRTÉK+3000;
        }
    }
    for(unsigned szekvencia_ÉRTÉK=0;szekvencia_ÉRTÉK<16;szekvencia_ÉRTÉK++) {
        struct assh_event_s Esemény;
        if(!assh_event_get(ismerős_e05f319b,&Esemény,MOST_ÉRTÉK/1000)){bezár_ismerős();return;}
        assh_status_t HIBA=ASSH_OK;int 쉬기=0,megszakít_végpont=0;
        switch(Esemény.id) {
        case ASSH_EVENT_READ: {
            int szám=통신읽기(társ_ÉRTÉK,Esemény.transport.read.buf.data,Esemény.transport.read.buf.size);
            if(szám>0)Esemény.transport.read.transferred=szám;
            else if(szám==-11)쉬기=1;else megszakít_végpont=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int szám=NET_ír(társ_ÉRTÉK,Esemény.transport.write.buf.data,Esemény.transport.write.buf.size);
            if(szám>0)Esemény.transport.write.transferred=szám;
            else if(szám==-11)쉬기=1;else megszakít_végpont=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Esemény.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Esemény.userauth_server.methods.retries>3)Esemény.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *adat=&Esemény.userauth_server.password;
            if(같은말(&adat->username,"user")&&adat->password.size<=256&&!adat->new_password.size) {
                unsigned char összegzés_ÉRTÉK[32];távoli_összegzés(adat->password.data,adat->password.size,összegzés_ÉRTÉK);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=összegzés_ÉRTÉK[순번]^felület_jelszó_összegzés[순번];memset(összegzés_ÉRTÉK,0,32);
                if(!차이)adat->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *adat=&Esemény.connection.channel_open;
            if(인증됨&&!Csatorna_bejegyzés&&felület_Várok&&같은말(&adat->type,"session")&&!adat->rq_data.size) {
                adat->reply=ASSH_CONNECTION_REPLY_SUCCESS;adat->pkt_size=4096;
                adat->win_size=-1;Csatorna_bejegyzés=adat->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: leíró_kérés(&Esemény.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *adat=&Esemény.connection.channel_data;
            if(!셸시작됨||adat->ch!=Csatorna_bejegyzés||adat->ext){megszakít_végpont=1;break;}
            unsigned szám=adat->data.size;if(szám>sizeof(bevitel_sor)-bevitel_DARAB)szám=sizeof(bevitel_sor)-bevitel_DARAB;
            for(unsigned 순번=0;순번<szám;순번++)if(adat->data.data[순번]==4){megszüntet_Állapot=0;szám=순번;adat->transferred=adat->data.size;break;}
            csatorna_távoli_bevitel(adat->data.data,szám);if(!adat->transferred)adat->transferred=szám;
            if(!szám&&megszüntet_Állapot<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Csatorna_bejegyzés=0;셸시작됨=0;닫을예정=1;zárás_IDŐ=MOST_ÉRTÉK+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Esemény.session.error.code);megszakít_végpont=1;break;
        case ASSH_EVENT_DISCONNECT: megszakít_végpont=1;break;
        default: break;
        }
        assh_event_done(ismerős_e05f319b,&Esemény,HIBA);
        if(megszakít_végpont){bezár_ismerős();return;}if(쉬기)return;
    }
}
