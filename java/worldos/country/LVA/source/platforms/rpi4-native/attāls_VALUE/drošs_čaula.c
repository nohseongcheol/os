/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "attāls_VALUE.h"
#include "kriptogrāfija_Atbalsts.h"
#include "Profils.h"
#include "../tīkls_kopa/tīkls_kopa.h"
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
static struct assh_context_s *konteksts_VALUE;
static struct assh_session_s *paziņa_e05f319b;
static struct assh_channel_s *Kanāls_ievade;
static int Klausīšanās_dalībnieks=-1,vienranga_VALUE=-1,인증됨,셸시작됨,komanda_TYPE,beigt_zvanu_Statuss=-1,닫을예정,palaišana_kļūda,čaula_Gaidu;
static uintptr_t paziņa_TIME,재접속시각,slēgšana_TIME;
static unsigned char 입력줄[8192],ražojums_līnija[65536];
static unsigned 입력앞,입력수,출력앞,ražojums_COUNT,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char cipars_VALUE[12];unsigned numurs=0;do{cipars_VALUE[numurs++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(numurs)보드글자쓰기(cipars_VALUE[--numurs]);보드글자쓰기(10);
}
static assh_status_t Sagatavot_atmiņa(void *dati,void **adrese,size_t Izmērs,enum assh_alloc_type_e 종류) {
    (void)dati;(void)종류;
    if(!Izmērs){izlaist_attāls(*adrese);*adrese=0;return ASSH_OK;}
    void *새주소=원격재할당(*adrese,Izmērs);
    if(!새주소)return ASSH_ERR_MEM;*adrese=새주소;return ASSH_OK;
}
static assh_status_t Sagatavot_nejaušs(struct assh_context_s *dati,const struct assh_buffer_s *sākotnējā_vērtība) {
    (void)dati;(void)sākotnējā_vērtība;unsigned char 시험[32];int mērs=attāls_nejaušs(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return mērs?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *dati,uint8_t *mērs,size_t 길이,uint_fast8_t 종류) {
    (void)dati;(void)종류;if(길이>65536)return ASSH_ERR_CRYPTO;
    return attāls_nejaušs(mērs,길이)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void nejaušs_beigt_zvanu(struct assh_context_s *dati){(void)dati;}
static const struct assh_prng_s nejaušs_ģenerētājs={Sagatavot_nejaušs,난수받기,nejaušs_beigt_zvanu};
static void Aizvērt_paziņa(void) {
    인증됨=셸시작됨=0;Kanāls_ievade=0;
    if(paziņa_e05f319b)assh_session_release(paziņa_e05f319b);paziņa_e05f319b=0;
    if(vienranga_VALUE>=0)Aizvērt_tīkls(vienranga_VALUE);vienranga_VALUE=-1;komanda_TYPE=0;beigt_zvanu_Statuss=-1;닫을예정=0;
    입력앞=입력수=출력앞=ražojums_COUNT=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *dati,unsigned numurs) {
    if(numurs>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<numurs;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=dati[순번];return numurs;
}
int 원격입력(void) {
    if(!입력수)return -1;int rakstzīme_VALUE=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return rakstzīme_VALUE;
}
void attāls_ražojums(unsigned char rakstzīme_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned Pievienot_MODE=rakstzīme_VALUE==10&&이전출력!=13;
    if(ražojums_COUNT+1+Pievienot_MODE>sizeof(ražojums_līnija)){닫을예정=2;return;}
    if(Pievienot_MODE)ražojums_līnija[(출력앞+ražojums_COUNT++)%sizeof(ražojums_līnija)]=13;
    ražojums_līnija[(출력앞+ražojums_COUNT++)%sizeof(ražojums_līnija)]=rakstzīme_VALUE;이전출력=rakstzīme_VALUE;
}
uintptr_t Panelis_beigt_zvanu_attāls_komanda(uintptr_t Statuss_VALUE){if(셸시작됨&&komanda_TYPE)beigt_zvanu_Statuss=(int)Statuss_VALUE;return 0;}
uintptr_t Panelis_attāls_pagaidi(uintptr_t Statuss_VALUE){čaula_Gaidu=Statuss_VALUE!=0;return 0;}
static int Sagatavot_čaula(void) {
    if(Klausīšanās_dalībnieks>=0)return 0;
    if(!konteksts_VALUE){
        assh_status_t Kļūda=assh_context_create(&konteksts_VALUE,ASSH_SERVER,Sagatavot_atmiņa,0,&nejaušs_ģenerētājs,0);
        if(Kļūda)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metode_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Kļūda=assh_algo_register(konteksts_VALUE,ASSH_SAFETY_WEAK,metode_MODE);
        if(!Kļūda)Kļūda=assh_service_register_va(konteksts_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=ierīce_Atslēga;
        if(!Kļūda)Kļūda=assh_key_load(konteksts_VALUE,assh_context_keys(konteksts_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(ierīce_Atslēga));
        if(Kļūda){진단("SSH init error ",Kļūda);assh_context_release(konteksts_VALUE);konteksts_VALUE=0;return -5;}
    }
    int ports_VALUE=통신끝점만들기(1);if(ports_VALUE<0)return ports_VALUE;통신주소재사용(ports_VALUE);
    int mērs=NET_BIND(ports_VALUE,0,22);if(!mērs)mērs=NET_klausīties(ports_VALUE);
    if(mērs<0){Aizvērt_tīkls(ports_VALUE);return mērs;}Klausīšanās_dalībnieks=ports_VALUE;return 0;
}
uintptr_t Panelis_attālā_vadība(uintptr_t 종류,uintptr_t Darbība) {
    if(종류==1)return(uint32_t)vadība_attāls_rādīt(Darbība);
    if(Darbība==0){Aizvērt_paziņa();if(Klausīšanās_dalībnieks>=0)Aizvērt_tīkls(Klausīšanās_dalībnieks);Klausīšanās_dalībnieks=-1;return 0;}
    if(Darbība==1){palaišana_kļūda=Sagatavot_čaula();return(uint32_t)palaišana_kļūda;}
    return(uint32_t)(Klausīšanās_dalībnieks>=0?1:palaišana_kļūda);
}
void Sagatavot_attāls(void){palaišana_kļūda=Sagatavot_čaula();vadība_attāls_rādīt(1);}
static int 같은말(const struct assh_cbuffer_s *dati,const char *Word_SMS) {
    size_t 길이=strlen(Word_SMS);return dati->size==길이&&!memcmp(dati->data,Word_SMS,길이);
}
static int Terminālis_pieprasījums(const struct assh_cbuffer_s *dati) {
    if(dati->size<24)return 0;
    const unsigned char *dati_amats=dati->data;unsigned 길이=assh_load_u32(dati_amats);
    if(길이>128||dati->size<길이+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(dati_amats+4+길이+16);
    return MODE_VALUE<=2048&&dati->size==길이+24+MODE_VALUE;
}
static void turis_pieprasījums(struct assh_event_request_s *Notikums) {
    if(!인증됨||Notikums->ch!=Kanāls_ievade||!Kanāls_ievade)return;
    if(같은말(&Notikums->type,"pty-req")) {
        if(!셸시작됨&&Terminālis_pieprasījums(&Notikums->rq_data))Notikums->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Notikums->type,"window-change")) {
        if(셸시작됨&&Notikums->rq_data.size==16)Notikums->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!čaula_Gaidu)return;
    const unsigned char *Komanda=0;unsigned 길이=0;
    if(같은말(&Notikums->type,"exec")) {
        if(Notikums->rq_data.size<4)return;
        길이=assh_load_u32(Notikums->rq_data.data);
        if(!길이||길이>2048||Notikums->rq_data.size!=길이+4)return;
        Komanda=Notikums->rq_data.data+4;
        for(unsigned 순번=0;순번<길이;순번++)if(!Komanda[순번])return;
        komanda_TYPE=1;
    }else if(!같은말(&Notikums->type,"shell")||Notikums->rq_data.size)return;
    if(sizeof(입력줄)-입력수<길이+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(길이)원격입력넣기(Komanda,길이);원격입력넣기(&끝,1);
    셸시작됨=1;Notikums->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!komanda_TYPE){const char *fails_Lasi_mani_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*fails_Lasi_mani_eb81d7d9)attāls_ražojums(*fails_Lasi_mani_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Klausīšanās_dalībnieks<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(vienranga_VALUE<0){if(NOW_VALUE<재접속시각)return;vienranga_VALUE=NET_akceptēt(Klausīšanās_dalībnieks);if(vienranga_VALUE<0)return;
        paziņa_TIME=NOW_VALUE;assh_status_t Kļūda=assh_session_create(konteksts_VALUE,&paziņa_e05f319b);
        if(Kļūda){paziņa_e05f319b=0;진단("SSH session error ",Kļūda);Aizvērt_paziņa();return;}}
    if((!인증됨&&NOW_VALUE-paziņa_TIME>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=slēgšana_TIME)){Aizvērt_paziņa();return;}
    if(Kanāls_ievade&&셸시작됨&&!닫을예정) {
        if(ražojums_COUNT){size_t numurs=sizeof(ražojums_līnija)-출력앞;if(numurs>ražojums_COUNT)numurs=ražojums_COUNT;if(numurs>2048)numurs=2048;
            assh_status_t Kļūda=assh_channel_data(Kanāls_ievade,ražojums_līnija+출력앞,&numurs);
            if(!Kļūda){출력앞=(출력앞+numurs)%sizeof(ražojums_līnija);ražojums_COUNT-=numurs;}
            else if(Kļūda!=ASSH_NO_DATA){Aizvērt_paziņa();return;}
        }
        if(beigt_zvanu_Statuss>=0&&!ražojums_COUNT){unsigned char Statuss_VALUE[4];assh_store_u32(Statuss_VALUE,(uint32_t)beigt_zvanu_Statuss);
            if(assh_request(paziņa_e05f319b,Kanāls_ievade,"exit-status",11,Statuss_VALUE,4,0)||assh_channel_eof(Kanāls_ievade)||assh_channel_close(Kanāls_ievade)) {Aizvērt_paziņa();return;}
            닫을예정=1;slēgšana_TIME=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s Notikums;
        if(!assh_event_get(paziņa_e05f319b,&Notikums,NOW_VALUE/1000)){Aizvērt_paziņa();return;}
        assh_status_t Kļūda=ASSH_OK;int 쉬기=0,atvienot_dalībnieks=0;
        switch(Notikums.id) {
        case ASSH_EVENT_READ: {
            int numurs=통신읽기(vienranga_VALUE,Notikums.transport.read.buf.data,Notikums.transport.read.buf.size);
            if(numurs>0)Notikums.transport.read.transferred=numurs;
            else if(numurs==-11)쉬기=1;else atvienot_dalībnieks=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int numurs=NET_rakstīšana(vienranga_VALUE,Notikums.transport.write.buf.data,Notikums.transport.write.buf.size);
            if(numurs>0)Notikums.transport.write.transferred=numurs;
            else if(numurs==-11)쉬기=1;else atvienot_dalībnieks=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Notikums.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Notikums.userauth_server.methods.retries>3)Notikums.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *dati=&Notikums.userauth_server.password;
            if(같은말(&dati->username,"user")&&dati->password.size<=256&&!dati->new_password.size) {
                unsigned char kopsavilkums_VALUE[32];attāls_kopsavilkums(dati->password.data,dati->password.size,kopsavilkums_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=kopsavilkums_VALUE[순번]^čaula_parole_kopsavilkums[순번];memset(kopsavilkums_VALUE,0,32);
                if(!차이)dati->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *dati=&Notikums.connection.channel_open;
            if(인증됨&&!Kanāls_ievade&&čaula_Gaidu&&같은말(&dati->type,"session")&&!dati->rq_data.size) {
                dati->reply=ASSH_CONNECTION_REPLY_SUCCESS;dati->pkt_size=4096;
                dati->win_size=-1;Kanāls_ievade=dati->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: turis_pieprasījums(&Notikums.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *dati=&Notikums.connection.channel_data;
            if(!셸시작됨||dati->ch!=Kanāls_ievade||dati->ext){atvienot_dalībnieks=1;break;}
            unsigned numurs=dati->data.size;if(numurs>sizeof(입력줄)-입력수)numurs=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<numurs;순번++)if(dati->data.data[순번]==4){beigt_zvanu_Statuss=0;numurs=순번;dati->transferred=dati->data.size;break;}
            원격입력넣기(dati->data.data,numurs);if(!dati->transferred)dati->transferred=numurs;
            if(!numurs&&beigt_zvanu_Statuss<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Kanāls_ievade=0;셸시작됨=0;닫을예정=1;slēgšana_TIME=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Notikums.session.error.code);atvienot_dalībnieks=1;break;
        case ASSH_EVENT_DISCONNECT: atvienot_dalībnieks=1;break;
        default: break;
        }
        assh_event_done(paziņa_e05f319b,&Notikums,Kļūda);
        if(atvienot_dalībnieks){Aizvērt_paziņa();return;}if(쉬기)return;
    }
}
