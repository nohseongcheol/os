/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "në_largësi_VALUE.h"
#include "암호기반.h"
#include "profil.h"
#include "../rrjet_Stivë/rrjet_Stivë.h"
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
static struct assh_context_s *Konteksti_VALUE;
static struct assh_session_s *lidhje_e05f319b;
static struct assh_channel_s *kanal_futje;
static int 듣는곳=-1,homolog_VALUE=-1,인증됨,셸시작됨,komandë_TYPE,mbaroj_status=-1,닫을예정,nisje_gabim,pasues_Po_pres;
static uintptr_t lidhje_Ora,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char shifër_VALUE[12];unsigned 수=0;do{shifër_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(shifër_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Përgatit_Memorie(void *të_dhëna,void **email,size_t Madhësi,enum assh_alloc_type_e 종류) {
    (void)të_dhëna;(void)종류;
    if(!Madhësi){liroj_në_largësi(*email);*email=0;return ASSH_OK;}
    void *새주소=원격재할당(*email,Madhësi);
    if(!새주소)return ASSH_ERR_MEM;*email=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *të_dhëna,const struct assh_buffer_s *jap_VALUE) {
    (void)të_dhëna;(void)jap_VALUE;unsigned char 시험[32];int llogaritje=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return llogaritje?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *të_dhëna,uint8_t *llogaritje,size_t gjatësi_VALUE,uint_fast8_t 종류) {
    (void)të_dhëna;(void)종류;if(gjatësi_VALUE>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(llogaritje,gjatësi_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *të_dhëna){(void)të_dhëna;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void mbyll_lidhje(void) {
    인증됨=셸시작됨=0;kanal_futje=0;
    if(lidhje_e05f319b)assh_session_release(lidhje_e05f319b);lidhje_e05f319b=0;
    if(homolog_VALUE>=0)mbyll_rrjet(homolog_VALUE);homolog_VALUE=-1;komandë_TYPE=0;mbaroj_status=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *të_dhëna,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=të_dhëna[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int karakter_VALUE=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return karakter_VALUE;
}
void 원격출력(unsigned char karakter_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=karakter_VALUE==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=karakter_VALUE;이전출력=karakter_VALUE;
}
uintptr_t panel_mbaroj_në_largësi_komandë(uintptr_t status_VALUE){if(셸시작됨&&komandë_TYPE)mbaroj_status=(int)status_VALUE;return 0;}
uintptr_t panel_në_largësi_Prit(uintptr_t status_VALUE){pasues_Po_pres=status_VALUE!=0;return 0;}
static int Përgatit_pasues(void) {
    if(듣는곳>=0)return 0;
    if(!Konteksti_VALUE){
        assh_status_t GABIM=assh_context_create(&Konteksti_VALUE,ASSH_SERVER,Përgatit_Memorie,0,&난수기,0);
        if(GABIM)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metoda_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        GABIM=assh_algo_register(Konteksti_VALUE,ASSH_SAFETY_WEAK,metoda_MODE);
        if(!GABIM)GABIM=assh_service_register_va(Konteksti_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=pajisje_tast;
        if(!GABIM)GABIM=assh_key_load(Konteksti_VALUE,assh_context_keys(Konteksti_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(pajisje_tast));
        if(GABIM){진단("SSH init error ",GABIM);assh_context_release(Konteksti_VALUE);Konteksti_VALUE=0;return -5;}
    }
    int portë_VALUE=통신끝점만들기(1);if(portë_VALUE<0)return portë_VALUE;통신주소재사용(portë_VALUE);
    int llogaritje=망주소묶기(portë_VALUE,0,22);if(!llogaritje)llogaritje=연결기다리기(portë_VALUE);
    if(llogaritje<0){mbyll_rrjet(portë_VALUE);return llogaritje;}듣는곳=portë_VALUE;return 0;
}
uintptr_t panel_ndjekja_paralele(uintptr_t 종류,uintptr_t Veprim) {
    if(종류==1)return(uint32_t)kontroll_në_largësi_afishim(Veprim);
    if(Veprim==0){mbyll_lidhje();if(듣는곳>=0)mbyll_rrjet(듣는곳);듣는곳=-1;return 0;}
    if(Veprim==1){nisje_gabim=Përgatit_pasues();return(uint32_t)nisje_gabim;}
    return(uint32_t)(듣는곳>=0?1:nisje_gabim);
}
void Përgatit_në_largësi(void){nisje_gabim=Përgatit_pasues();kontroll_në_largësi_afishim(1);}
static int 같은말(const struct assh_cbuffer_s *të_dhëna,const char *Word_SMS) {
    size_t gjatësi_VALUE=strlen(Word_SMS);return të_dhëna->size==gjatësi_VALUE&&!memcmp(të_dhëna->data,Word_SMS,gjatësi_VALUE);
}
static int 터미널요청(const struct assh_cbuffer_s *të_dhëna) {
    if(të_dhëna->size<24)return 0;
    const unsigned char *të_dhëna_pozicioni=të_dhëna->data;unsigned gjatësi_VALUE=assh_load_u32(të_dhëna_pozicioni);
    if(gjatësi_VALUE>128||të_dhëna->size<gjatësi_VALUE+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(të_dhëna_pozicioni+4+gjatësi_VALUE+16);
    return MODE_VALUE<=2048&&të_dhëna->size==gjatësi_VALUE+24+MODE_VALUE;
}
static void 요청처리(struct assh_event_request_s *Ngjarje) {
    if(!인증됨||Ngjarje->ch!=kanal_futje||!kanal_futje)return;
    if(같은말(&Ngjarje->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&Ngjarje->rq_data))Ngjarje->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Ngjarje->type,"window-change")) {
        if(셸시작됨&&Ngjarje->rq_data.size==16)Ngjarje->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!pasues_Po_pres)return;
    const unsigned char *Komanda=0;unsigned gjatësi_VALUE=0;
    if(같은말(&Ngjarje->type,"exec")) {
        if(Ngjarje->rq_data.size<4)return;
        gjatësi_VALUE=assh_load_u32(Ngjarje->rq_data.data);
        if(!gjatësi_VALUE||gjatësi_VALUE>2048||Ngjarje->rq_data.size!=gjatësi_VALUE+4)return;
        Komanda=Ngjarje->rq_data.data+4;
        for(unsigned 순번=0;순번<gjatësi_VALUE;순번++)if(!Komanda[순번])return;
        komandë_TYPE=1;
    }else if(!같은말(&Ngjarje->type,"shell")||Ngjarje->rq_data.size)return;
    if(sizeof(입력줄)-입력수<gjatësi_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(gjatësi_VALUE)원격입력넣기(Komanda,gjatësi_VALUE);원격입력넣기(&끝,1);
    셸시작됨=1;Ngjarje->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!komandë_TYPE){const char *LEXOMË_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*LEXOMË_eb81d7d9)원격출력(*LEXOMË_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(homolog_VALUE<0){if(NOW_VALUE<재접속시각)return;homolog_VALUE=망연결받기(듣는곳);if(homolog_VALUE<0)return;
        lidhje_Ora=NOW_VALUE;assh_status_t GABIM=assh_session_create(Konteksti_VALUE,&lidhje_e05f319b);
        if(GABIM){lidhje_e05f319b=0;진단("SSH session error ",GABIM);mbyll_lidhje();return;}}
    if((!인증됨&&NOW_VALUE-lidhje_Ora>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){mbyll_lidhje();return;}
    if(kanal_futje&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t GABIM=assh_channel_data(kanal_futje,출력줄+출력앞,&수);
            if(!GABIM){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(GABIM!=ASSH_NO_DATA){mbyll_lidhje();return;}
        }
        if(mbaroj_status>=0&&!출력수){unsigned char status_VALUE[4];assh_store_u32(status_VALUE,(uint32_t)mbaroj_status);
            if(assh_request(lidhje_e05f319b,kanal_futje,"exit-status",11,status_VALUE,4,0)||assh_channel_eof(kanal_futje)||assh_channel_close(kanal_futje)) {mbyll_lidhje();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s Ngjarje;
        if(!assh_event_get(lidhje_e05f319b,&Ngjarje,NOW_VALUE/1000)){mbyll_lidhje();return;}
        assh_status_t GABIM=ASSH_OK;int 쉬기=0,끊기=0;
        switch(Ngjarje.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(homolog_VALUE,Ngjarje.transport.read.buf.data,Ngjarje.transport.read.buf.size);
            if(수>0)Ngjarje.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(homolog_VALUE,Ngjarje.transport.write.buf.data,Ngjarje.transport.write.buf.size);
            if(수>0)Ngjarje.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Ngjarje.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Ngjarje.userauth_server.methods.retries>3)Ngjarje.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *të_dhëna=&Ngjarje.userauth_server.password;
            if(같은말(&të_dhëna->username,"user")&&të_dhëna->password.size<=256&&!të_dhëna->new_password.size) {
                unsigned char përmbledhje_VALUE[32];në_largësi_përmbledhje(të_dhëna->password.data,të_dhëna->password.size,përmbledhje_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=përmbledhje_VALUE[순번]^pasues_fjalëkalim_përmbledhje[순번];memset(përmbledhje_VALUE,0,32);
                if(!차이)të_dhëna->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *të_dhëna=&Ngjarje.connection.channel_open;
            if(인증됨&&!kanal_futje&&pasues_Po_pres&&같은말(&të_dhëna->type,"session")&&!të_dhëna->rq_data.size) {
                të_dhëna->reply=ASSH_CONNECTION_REPLY_SUCCESS;të_dhëna->pkt_size=4096;
                të_dhëna->win_size=-1;kanal_futje=të_dhëna->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&Ngjarje.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *të_dhëna=&Ngjarje.connection.channel_data;
            if(!셸시작됨||të_dhëna->ch!=kanal_futje||të_dhëna->ext){끊기=1;break;}
            unsigned 수=të_dhëna->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(të_dhëna->data.data[순번]==4){mbaroj_status=0;수=순번;të_dhëna->transferred=të_dhëna->data.size;break;}
            원격입력넣기(të_dhëna->data.data,수);if(!të_dhëna->transferred)të_dhëna->transferred=수;
            if(!수&&mbaroj_status<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: kanal_futje=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Ngjarje.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(lidhje_e05f319b,&Ngjarje,GABIM);
        if(끊기){mbyll_lidhje();return;}if(쉬기)return;
    }
}
