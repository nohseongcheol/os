/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "lu_soree_xëyma.h"
#include "암호기반.h"
#include "profil.h"
#include "../mbaal_Tegalo/mbaal_Tegalo.h"
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
static struct assh_context_s *péete_xëyma;
static struct assh_session_s *jokkalóo_e05f319b;
static struct assh_channel_s *Yoon_dugal_xabaar;
static int 듣는곳=-1,Nàttangoo_xëyma=-1,인증됨,셸시작됨,ndigel_xeet,jeexal_nekkin=-1,닫을예정,buuraat_njumte,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned xëyma) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char siifar_xëyma[12];unsigned 수=0;do{siifar_xëyma[수++]='0'+xëyma%10;xëyma/=10;}while(xëyma);
    while(수)보드글자쓰기(siifar_xëyma[--수]);보드글자쓰기(10);
}
static assh_status_t jël_matuwaay_fatlekookaay(void *mbir,void **dëkkuwaay,size_t tolluwaay,enum assh_alloc_type_e 종류) {
    (void)mbir;(void)종류;
    if(!tolluwaay){yewwi_lu_soree(*dëkkuwaay);*dëkkuwaay=0;return ASSH_OK;}
    void *새주소=원격재할당(*dëkkuwaay,tolluwaay);
    if(!새주소)return ASSH_ERR_MEM;*dëkkuwaay=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *mbir,const struct assh_buffer_s *tolluwaay_bu_njëkk_xëyma) {
    (void)mbir;(void)tolluwaay_bu_njëkk_xëyma;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *mbir,uint8_t *결과,size_t diir_xëyma,uint_fast8_t 종류) {
    (void)mbir;(void)종류;if(diir_xëyma>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,diir_xëyma)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *mbir){(void)mbir;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void Tej_jokkalóo(void) {
    인증됨=셸시작됨=0;Yoon_dugal_xabaar=0;
    if(jokkalóo_e05f319b)assh_session_release(jokkalóo_e05f319b);jokkalóo_e05f319b=0;
    if(Nàttangoo_xëyma>=0)Tej_mbaal(Nàttangoo_xëyma);Nàttangoo_xëyma=-1;ndigel_xeet=0;jeexal_nekkin=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *mbir,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=mbir[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int Araf_xëyma=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return Araf_xëyma;
}
void 원격출력(unsigned char Araf_xëyma) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=Araf_xëyma==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=Araf_xëyma;이전출력=Araf_xëyma;
}
uintptr_t 보드원격명령끝(uintptr_t nekkin_xëyma){if(셸시작됨&&ndigel_xeet)jeexal_nekkin=(int)nekkin_xëyma;return 0;}
uintptr_t 보드원격대기(uintptr_t nekkin_xëyma){셸대기중=nekkin_xëyma!=0;return 0;}
static int jël_matuwaay_Wëreef(void) {
    if(듣는곳>=0)return 0;
    if(!péete_xëyma){
        assh_status_t njumte=assh_context_create(&péete_xëyma,ASSH_SERVER,jël_matuwaay_fatlekookaay,0,&난수기,0);
        if(njumte)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *doxalin_anam[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        njumte=assh_algo_register(péete_xëyma,ASSH_SAFETY_WEAK,doxalin_anam);
        if(!njumte)njumte=assh_service_register_va(péete_xëyma,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=toftal_kër;
        if(!njumte)njumte=assh_key_load(péete_xëyma,assh_context_keys(péete_xëyma),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(toftal_kër));
        if(njumte){진단("SSH init error ",njumte);assh_context_release(péete_xëyma);péete_xëyma=0;return -5;}
    }
    int jël_xëyma=통신끝점만들기(1);if(jël_xëyma<0)return jël_xëyma;통신주소재사용(jël_xëyma);
    int 결과=망주소묶기(jël_xëyma,0,22);if(!결과)결과=연결기다리기(jël_xëyma);
    if(결과<0){Tej_mbaal(jël_xëyma);return 결과;}듣는곳=jël_xëyma;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t jëf) {
    if(종류==1)return(uint32_t)Saytu_doxinu_ordinateur_lu_soree_laa(jëf);
    if(jëf==0){Tej_jokkalóo();if(듣는곳>=0)Tej_mbaal(듣는곳);듣는곳=-1;return 0;}
    if(jëf==1){buuraat_njumte=jël_matuwaay_Wëreef();return(uint32_t)buuraat_njumte;}
    return(uint32_t)(듣는곳>=0?1:buuraat_njumte);
}
void jël_matuwaay_lu_soree(void){buuraat_njumte=jël_matuwaay_Wëreef();Saytu_doxinu_ordinateur_lu_soree_laa(1);}
static int 같은말(const struct assh_cbuffer_s *mbir,const char *Word_SMS) {
    size_t diir_xëyma=strlen(Word_SMS);return mbir->size==diir_xëyma&&!memcmp(mbir->data,Word_SMS,diir_xëyma);
}
static int 터미널요청(const struct assh_cbuffer_s *mbir) {
    if(mbir->size<24)return 0;
    const unsigned char *자료위치=mbir->data;unsigned diir_xëyma=assh_load_u32(자료위치);
    if(diir_xëyma>128||mbir->size<diir_xëyma+24)return 0;
    unsigned anam_xëyma=assh_load_u32(자료위치+4+diir_xëyma+16);
    return anam_xëyma<=2048&&mbir->size==diir_xëyma+24+anam_xëyma;
}
static void 요청처리(struct assh_event_request_s *xewxew) {
    if(!인증됨||xewxew->ch!=Yoon_dugal_xabaar||!Yoon_dugal_xabaar)return;
    if(같은말(&xewxew->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&xewxew->rq_data))xewxew->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&xewxew->type,"window-change")) {
        if(셸시작됨&&xewxew->rq_data.size==16)xewxew->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *ndigel=0;unsigned diir_xëyma=0;
    if(같은말(&xewxew->type,"exec")) {
        if(xewxew->rq_data.size<4)return;
        diir_xëyma=assh_load_u32(xewxew->rq_data.data);
        if(!diir_xëyma||diir_xëyma>2048||xewxew->rq_data.size!=diir_xëyma+4)return;
        ndigel=xewxew->rq_data.data+4;
        for(unsigned 순번=0;순번<diir_xëyma;순번++)if(!ndigel[순번])return;
        ndigel_xeet=1;
    }else if(!같은말(&xewxew->type,"shell")||xewxew->rq_data.size)return;
    if(sizeof(입력줄)-입력수<diir_xëyma+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(diir_xëyma)원격입력넣기(ndigel,diir_xëyma);원격입력넣기(&끝,1);
    셸시작됨=1;xewxew->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!ndigel_xeet){const char *JANG_MA_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*JANG_MA_eb81d7d9)원격출력(*JANG_MA_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(Nàttangoo_xëyma<0){if(지금<재접속시각)return;Nàttangoo_xëyma=망연결받기(듣는곳);if(Nàttangoo_xëyma<0)return;
        접속시각=지금;assh_status_t njumte=assh_session_create(péete_xëyma,&jokkalóo_e05f319b);
        if(njumte){jokkalóo_e05f319b=0;진단("SSH session error ",njumte);Tej_jokkalóo();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){Tej_jokkalóo();return;}
    if(Yoon_dugal_xabaar&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t njumte=assh_channel_data(Yoon_dugal_xabaar,출력줄+출력앞,&수);
            if(!njumte){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(njumte!=ASSH_NO_DATA){Tej_jokkalóo();return;}
        }
        if(jeexal_nekkin>=0&&!출력수){unsigned char nekkin_xëyma[4];assh_store_u32(nekkin_xëyma,(uint32_t)jeexal_nekkin);
            if(assh_request(jokkalóo_e05f319b,Yoon_dugal_xabaar,"exit-status",11,nekkin_xëyma,4,0)||assh_channel_eof(Yoon_dugal_xabaar)||assh_channel_close(Yoon_dugal_xabaar)) {Tej_jokkalóo();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned SEQUENCE_xëyma=0;SEQUENCE_xëyma<16;SEQUENCE_xëyma++) {
        struct assh_event_s xewxew;
        if(!assh_event_get(jokkalóo_e05f319b,&xewxew,지금/1000)){Tej_jokkalóo();return;}
        assh_status_t njumte=ASSH_OK;int 쉬기=0,끊기=0;
        switch(xewxew.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(Nàttangoo_xëyma,xewxew.transport.read.buf.data,xewxew.transport.read.buf.size);
            if(수>0)xewxew.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(Nàttangoo_xëyma,xewxew.transport.write.buf.data,xewxew.transport.write.buf.size);
            if(수>0)xewxew.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            xewxew.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(xewxew.userauth_server.methods.retries>3)xewxew.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *mbir=&xewxew.userauth_server.password;
            if(같은말(&mbir->username,"user")&&mbir->password.size<=256&&!mbir->new_password.size) {
                unsigned char 요약[32];원격요약(mbir->password.data,mbir->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)mbir->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *mbir=&xewxew.connection.channel_open;
            if(인증됨&&!Yoon_dugal_xabaar&&셸대기중&&같은말(&mbir->type,"session")&&!mbir->rq_data.size) {
                mbir->reply=ASSH_CONNECTION_REPLY_SUCCESS;mbir->pkt_size=4096;
                mbir->win_size=-1;Yoon_dugal_xabaar=mbir->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&xewxew.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *mbir=&xewxew.connection.channel_data;
            if(!셸시작됨||mbir->ch!=Yoon_dugal_xabaar||mbir->ext){끊기=1;break;}
            unsigned 수=mbir->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(mbir->data.data[순번]==4){jeexal_nekkin=0;수=순번;mbir->transferred=mbir->data.size;break;}
            원격입력넣기(mbir->data.data,수);if(!mbir->transferred)mbir->transferred=수;
            if(!수&&jeexal_nekkin<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Yoon_dugal_xabaar=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",xewxew.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(jokkalóo_e05f319b,&xewxew,njumte);
        if(끊기){Tej_jokkalóo();return;}if(쉬기)return;
    }
}
