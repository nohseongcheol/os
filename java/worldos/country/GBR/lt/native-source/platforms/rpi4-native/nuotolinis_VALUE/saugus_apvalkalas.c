/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "nuotolinis_VALUE.h"
#include "kriptografija_pagalba.h"
#include "Profilis.h"
#include "../tinklas_eilė/tinklas_eilė.h"
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
static struct assh_session_s *ryšys_e05f319b;
static struct assh_channel_s *kanalas_įrašas;
static int Klausausi_dalyvis=-1,lygiavertis_mazgas_VALUE=-1,인증됨,셸시작됨,komanda_TYPE,baigti_pokalbį_Būsena=-1,닫을예정,시작오류,apvalkalas_Vis_dar_laukiu;
static uintptr_t ryšys_TIME,재접속시각,uždarymo_TIME;
static unsigned char 입력줄[8192],išeiga_eilutė[65536];
static unsigned 입력앞,입력수,출력앞,išeiga_COUNT,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char skaitmuo_VALUE[12];unsigned numeris=0;do{skaitmuo_VALUE[numeris++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(numeris)보드글자쓰기(skaitmuo_VALUE[--numeris]);보드글자쓰기(10);
}
static assh_status_t Parengti_atmintis(void *duomenys,void **ADDRESS,size_t Dydis,enum assh_alloc_type_e 종류) {
    (void)duomenys;(void)종류;
    if(!Dydis){išleisti_nuotolinis(*ADDRESS);*ADDRESS=0;return ASSH_OK;}
    void *새주소=원격재할당(*ADDRESS,Dydis);
    if(!새주소)return ASSH_ERR_MEM;*ADDRESS=새주소;return ASSH_OK;
}
static assh_status_t Parengti_atsitiktinis(struct assh_context_s *duomenys,const struct assh_buffer_s *pirminė_reikšmė) {
    (void)duomenys;(void)pirminė_reikšmė;unsigned char 시험[32];int REZULTATAS=nuotolinis_atsitiktinis(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return REZULTATAS?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *duomenys,uint8_t *REZULTATAS,size_t 길이,uint_fast8_t 종류) {
    (void)duomenys;(void)종류;if(길이>65536)return ASSH_ERR_CRYPTO;
    return nuotolinis_atsitiktinis(REZULTATAS,길이)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void atsitiktinis_baigti_pokalbį(struct assh_context_s *duomenys){(void)duomenys;}
static const struct assh_prng_s atsitiktinis_generatorius={Parengti_atsitiktinis,난수받기,atsitiktinis_baigti_pokalbį};
static void Uždaryti_ryšys(void) {
    인증됨=셸시작됨=0;kanalas_įrašas=0;
    if(ryšys_e05f319b)assh_session_release(ryšys_e05f319b);ryšys_e05f319b=0;
    if(lygiavertis_mazgas_VALUE>=0)Uždaryti_tinklas(lygiavertis_mazgas_VALUE);lygiavertis_mazgas_VALUE=-1;komanda_TYPE=0;baigti_pokalbį_Būsena=-1;닫을예정=0;
    입력앞=입력수=출력앞=išeiga_COUNT=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *duomenys,unsigned numeris) {
    if(numeris>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<numeris;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=duomenys[순번];return numeris;
}
int 원격입력(void) {
    if(!입력수)return -1;int simbolis_VALUE_068c2631=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return simbolis_VALUE_068c2631;
}
void nuotolinis_išeiga(unsigned char simbolis_VALUE_068c2631) {
    if(!셸시작됨||닫을예정)return;
    unsigned sujungti_MODE=simbolis_VALUE_068c2631==10&&이전출력!=13;
    if(išeiga_COUNT+1+sujungti_MODE>sizeof(išeiga_eilutė)){닫을예정=2;return;}
    if(sujungti_MODE)išeiga_eilutė[(출력앞+išeiga_COUNT++)%sizeof(išeiga_eilutė)]=13;
    išeiga_eilutė[(출력앞+išeiga_COUNT++)%sizeof(išeiga_eilutė)]=simbolis_VALUE_068c2631;이전출력=simbolis_VALUE_068c2631;
}
uintptr_t Lenta_baigti_pokalbį_nuotolinis_komanda(uintptr_t Būsena_VALUE){if(셸시작됨&&komanda_TYPE)baigti_pokalbį_Būsena=(int)Būsena_VALUE;return 0;}
uintptr_t Lenta_nuotolinis_Palauk(uintptr_t Būsena_VALUE){apvalkalas_Vis_dar_laukiu=Būsena_VALUE!=0;return 0;}
static int Parengti_apvalkalas(void) {
    if(Klausausi_dalyvis>=0)return 0;
    if(!문맥){
        assh_status_t KLAIDA=assh_context_create(&문맥,ASSH_SERVER,Parengti_atmintis,0,&atsitiktinis_generatorius,0);
        if(KLAIDA)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metodas_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        KLAIDA=assh_algo_register(문맥,ASSH_SAFETY_WEAK,metodas_MODE);
        if(!KLAIDA)KLAIDA=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=įrenginys_Raktas;
        if(!KLAIDA)KLAIDA=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(įrenginys_Raktas));
        if(KLAIDA){진단("SSH init error ",KLAIDA);assh_context_release(문맥);문맥=0;return -5;}
    }
    int jungtis_VALUE=통신끝점만들기(1);if(jungtis_VALUE<0)return jungtis_VALUE;통신주소재사용(jungtis_VALUE);
    int REZULTATAS=NET_BIND(jungtis_VALUE,0,22);if(!REZULTATAS)REZULTATAS=NET_laukti(jungtis_VALUE);
    if(REZULTATAS<0){Uždaryti_tinklas(jungtis_VALUE);return REZULTATAS;}Klausausi_dalyvis=jungtis_VALUE;return 0;
}
uintptr_t Lenta_stebėjimas(uintptr_t 종류,uintptr_t Veiksmas) {
    if(종류==1)return(uint32_t)valdymas_nuotolinis_rodyti(Veiksmas);
    if(Veiksmas==0){Uždaryti_ryšys();if(Klausausi_dalyvis>=0)Uždaryti_tinklas(Klausausi_dalyvis);Klausausi_dalyvis=-1;return 0;}
    if(Veiksmas==1){시작오류=Parengti_apvalkalas();return(uint32_t)시작오류;}
    return(uint32_t)(Klausausi_dalyvis>=0?1:시작오류);
}
void Parengti_nuotolinis(void){시작오류=Parengti_apvalkalas();valdymas_nuotolinis_rodyti(1);}
static int 같은말(const struct assh_cbuffer_s *duomenys,const char *Word_SMS) {
    size_t 길이=strlen(Word_SMS);return duomenys->size==길이&&!memcmp(duomenys->data,Word_SMS,길이);
}
static int Terminalas_užklausa(const struct assh_cbuffer_s *duomenys) {
    if(duomenys->size<24)return 0;
    const unsigned char *duomenys_padėtis=duomenys->data;unsigned 길이=assh_load_u32(duomenys_padėtis);
    if(길이>128||duomenys->size<길이+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(duomenys_padėtis+4+길이+16);
    return MODE_VALUE<=2048&&duomenys->size==길이+24+MODE_VALUE;
}
static void rodyklė_užklausa(struct assh_event_request_s *Įvykis) {
    if(!인증됨||Įvykis->ch!=kanalas_įrašas||!kanalas_įrašas)return;
    if(같은말(&Įvykis->type,"pty-req")) {
        if(!셸시작됨&&Terminalas_užklausa(&Įvykis->rq_data))Įvykis->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Įvykis->type,"window-change")) {
        if(셸시작됨&&Įvykis->rq_data.size==16)Įvykis->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!apvalkalas_Vis_dar_laukiu)return;
    const unsigned char *Komanda=0;unsigned 길이=0;
    if(같은말(&Įvykis->type,"exec")) {
        if(Įvykis->rq_data.size<4)return;
        길이=assh_load_u32(Įvykis->rq_data.data);
        if(!길이||길이>2048||Įvykis->rq_data.size!=길이+4)return;
        Komanda=Įvykis->rq_data.data+4;
        for(unsigned 순번=0;순번<길이;순번++)if(!Komanda[순번])return;
        komanda_TYPE=1;
    }else if(!같은말(&Įvykis->type,"shell")||Įvykis->rq_data.size)return;
    if(sizeof(입력줄)-입력수<길이+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(길이)원격입력넣기(Komanda,길이);원격입력넣기(&끝,1);
    셸시작됨=1;Įvykis->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!komanda_TYPE){const char *안내="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*안내)nuotolinis_išeiga(*안내++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Klausausi_dalyvis<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(lygiavertis_mazgas_VALUE<0){if(NOW_VALUE<재접속시각)return;lygiavertis_mazgas_VALUE=NET_priimti(Klausausi_dalyvis);if(lygiavertis_mazgas_VALUE<0)return;
        ryšys_TIME=NOW_VALUE;assh_status_t KLAIDA=assh_session_create(문맥,&ryšys_e05f319b);
        if(KLAIDA){ryšys_e05f319b=0;진단("SSH session error ",KLAIDA);Uždaryti_ryšys();return;}}
    if((!인증됨&&NOW_VALUE-ryšys_TIME>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=uždarymo_TIME)){Uždaryti_ryšys();return;}
    if(kanalas_įrašas&&셸시작됨&&!닫을예정) {
        if(išeiga_COUNT){size_t numeris=sizeof(išeiga_eilutė)-출력앞;if(numeris>išeiga_COUNT)numeris=išeiga_COUNT;if(numeris>2048)numeris=2048;
            assh_status_t KLAIDA=assh_channel_data(kanalas_įrašas,išeiga_eilutė+출력앞,&numeris);
            if(!KLAIDA){출력앞=(출력앞+numeris)%sizeof(išeiga_eilutė);išeiga_COUNT-=numeris;}
            else if(KLAIDA!=ASSH_NO_DATA){Uždaryti_ryšys();return;}
        }
        if(baigti_pokalbį_Būsena>=0&&!išeiga_COUNT){unsigned char Būsena_VALUE[4];assh_store_u32(Būsena_VALUE,(uint32_t)baigti_pokalbį_Būsena);
            if(assh_request(ryšys_e05f319b,kanalas_įrašas,"exit-status",11,Būsena_VALUE,4,0)||assh_channel_eof(kanalas_įrašas)||assh_channel_close(kanalas_įrašas)) {Uždaryti_ryšys();return;}
            닫을예정=1;uždarymo_TIME=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s Įvykis;
        if(!assh_event_get(ryšys_e05f319b,&Įvykis,NOW_VALUE/1000)){Uždaryti_ryšys();return;}
        assh_status_t KLAIDA=ASSH_OK;int 쉬기=0,atjungti_dalyvis=0;
        switch(Įvykis.id) {
        case ASSH_EVENT_READ: {
            int numeris=통신읽기(lygiavertis_mazgas_VALUE,Įvykis.transport.read.buf.data,Įvykis.transport.read.buf.size);
            if(numeris>0)Įvykis.transport.read.transferred=numeris;
            else if(numeris==-11)쉬기=1;else atjungti_dalyvis=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int numeris=NET_rašymas(lygiavertis_mazgas_VALUE,Įvykis.transport.write.buf.data,Įvykis.transport.write.buf.size);
            if(numeris>0)Įvykis.transport.write.transferred=numeris;
            else if(numeris==-11)쉬기=1;else atjungti_dalyvis=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Įvykis.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Įvykis.userauth_server.methods.retries>3)Įvykis.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *duomenys=&Įvykis.userauth_server.password;
            if(같은말(&duomenys->username,"user")&&duomenys->password.size<=256&&!duomenys->new_password.size) {
                unsigned char suvestinė_VALUE[32];nuotolinis_suvestinė(duomenys->password.data,duomenys->password.size,suvestinė_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=suvestinė_VALUE[순번]^apvalkalas_slaptažodis_suvestinė[순번];memset(suvestinė_VALUE,0,32);
                if(!차이)duomenys->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *duomenys=&Įvykis.connection.channel_open;
            if(인증됨&&!kanalas_įrašas&&apvalkalas_Vis_dar_laukiu&&같은말(&duomenys->type,"session")&&!duomenys->rq_data.size) {
                duomenys->reply=ASSH_CONNECTION_REPLY_SUCCESS;duomenys->pkt_size=4096;
                duomenys->win_size=-1;kanalas_įrašas=duomenys->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: rodyklė_užklausa(&Įvykis.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *duomenys=&Įvykis.connection.channel_data;
            if(!셸시작됨||duomenys->ch!=kanalas_įrašas||duomenys->ext){atjungti_dalyvis=1;break;}
            unsigned numeris=duomenys->data.size;if(numeris>sizeof(입력줄)-입력수)numeris=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<numeris;순번++)if(duomenys->data.data[순번]==4){baigti_pokalbį_Būsena=0;numeris=순번;duomenys->transferred=duomenys->data.size;break;}
            원격입력넣기(duomenys->data.data,numeris);if(!duomenys->transferred)duomenys->transferred=numeris;
            if(!numeris&&baigti_pokalbį_Būsena<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: kanalas_įrašas=0;셸시작됨=0;닫을예정=1;uždarymo_TIME=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Įvykis.session.error.code);atjungti_dalyvis=1;break;
        case ASSH_EVENT_DISCONNECT: atjungti_dalyvis=1;break;
        default: break;
        }
        assh_event_done(ryšys_e05f319b,&Įvykis,KLAIDA);
        if(atjungti_dalyvis){Uždaryti_ryšys();return;}if(쉬기)return;
    }
}
