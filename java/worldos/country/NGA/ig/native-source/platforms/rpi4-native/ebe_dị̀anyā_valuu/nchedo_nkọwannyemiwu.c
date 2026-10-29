/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "ebe_dị̀anyā_valuu.h"
#include "암호기반.h"
#include "Profaịl.h"
#include "../Netwọọkụ_ikpo/Netwọọkụ_ikpo.h"
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
static struct assh_context_s *Ọnọdụ_valuu;
static struct assh_session_s *njikọ_e05f319b;
static struct assh_channel_s *ọwa_ndebà;
static int 듣는곳=-1,ibè_valuu=-1,인증됨,셸시작됨,nnyemiwu_pinye,mèdebe_ọnọdụ=-1,닫을예정,mbido_mmejọ,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Mkpụrụokwu_SMS,unsigned valuu) {
    while(*Mkpụrụokwu_SMS)보드글자쓰기(*Mkpụrụokwu_SMS++);
    char ọbula_valuu[12];unsigned 수=0;do{ọbula_valuu[수++]='0'+valuu%10;valuu/=10;}while(valuu);
    while(수)보드글자쓰기(ọbula_valuu[--수]);보드글자쓰기(10);
}
static assh_status_t Kwado_memọrị(void *datà,void **àdreèsì,size_t Ụhara,enum assh_alloc_type_e 종류) {
    (void)datà;(void)종류;
    if(!Ụhara){bupute_ebe_dị̀anyā(*àdreèsì);*àdreèsì=0;return ASSH_OK;}
    void *새주소=원격재할당(*àdreèsì,Ụhara);
    if(!새주소)return ASSH_ERR_MEM;*àdreèsì=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *datà,const struct assh_buffer_s *mkpụrụ_valuu) {
    (void)datà;(void)mkpụrụ_valuu;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *datà,uint8_t *결과,size_t ogologo_valuu,uint_fast8_t 종류) {
    (void)datà;(void)종류;if(ogologo_valuu>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,ogologo_valuu)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *datà){(void)datà;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void mmechi_njikọ(void) {
    인증됨=셸시작됨=0;ọwa_ndebà=0;
    if(njikọ_e05f319b)assh_session_release(njikọ_e05f319b);njikọ_e05f319b=0;
    if(ibè_valuu>=0)mmechi_Netwọọkụ(ibè_valuu);ibè_valuu=-1;nnyemiwu_pinye=0;mèdebe_ọnọdụ=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *datà,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=datà[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int mkpụrụedemede_valuu=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return mkpụrụedemede_valuu;
}
void 원격출력(unsigned char mkpụrụedemede_valuu) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=mkpụrụedemede_valuu==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=mkpụrụedemede_valuu;이전출력=mkpụrụedemede_valuu;
}
uintptr_t 보드원격명령끝(uintptr_t ọnọdụ_valuu){if(셸시작됨&&nnyemiwu_pinye)mèdebe_ọnọdụ=(int)ọnọdụ_valuu;return 0;}
uintptr_t 보드원격대기(uintptr_t ọnọdụ_valuu){셸대기중=ọnọdụ_valuu!=0;return 0;}
static int Kwado_nkọwannyemiwu(void) {
    if(듣는곳>=0)return 0;
    if(!Ọnọdụ_valuu){
        assh_status_t mmejọ=assh_context_create(&Ọnọdụ_valuu,ASSH_SERVER,Kwado_memọrị,0,&난수기,0);
        if(mmejọ)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *usoro_moòdù[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        mmejọ=assh_algo_register(Ọnọdụ_valuu,ASSH_SAFETY_WEAK,usoro_moòdù);
        if(!mmejọ)mmejọ=assh_service_register_va(Ọnọdụ_valuu,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=njìarụ_ọtụgwo;
        if(!mmejọ)mmejọ=assh_key_load(Ọnọdụ_valuu,assh_context_keys(Ọnọdụ_valuu),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(njìarụ_ọtụgwo));
        if(mmejọ){진단("SSH init error ",mmejọ);assh_context_release(Ọnọdụ_valuu);Ọnọdụ_valuu=0;return -5;}
    }
    int pọọt_valuu=통신끝점만들기(1);if(pọọt_valuu<0)return pọọt_valuu;통신주소재사용(pọọt_valuu);
    int 결과=망주소묶기(pọọt_valuu,0,22);if(!결과)결과=연결기다리기(pọọt_valuu);
    if(결과<0){mmechi_Netwọọkụ(pọọt_valuu);return 결과;}듣는곳=pọọt_valuu;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t mmèm) {
    if(종류==1)return(uint32_t)njizi_ebe_dị̀anyā_gosịpụta(mmèm);
    if(mmèm==0){mmechi_njikọ();if(듣는곳>=0)mmechi_Netwọọkụ(듣는곳);듣는곳=-1;return 0;}
    if(mmèm==1){mbido_mmejọ=Kwado_nkọwannyemiwu();return(uint32_t)mbido_mmejọ;}
    return(uint32_t)(듣는곳>=0?1:mbido_mmejọ);
}
void Kwado_ebe_dị̀anyā(void){mbido_mmejọ=Kwado_nkọwannyemiwu();njizi_ebe_dị̀anyā_gosịpụta(1);}
static int 같은말(const struct assh_cbuffer_s *datà,const char *Mkpụrụokwu_SMS) {
    size_t ogologo_valuu=strlen(Mkpụrụokwu_SMS);return datà->size==ogologo_valuu&&!memcmp(datà->data,Mkpụrụokwu_SMS,ogologo_valuu);
}
static int 터미널요청(const struct assh_cbuffer_s *datà) {
    if(datà->size<24)return 0;
    const unsigned char *자료위치=datà->data;unsigned ogologo_valuu=assh_load_u32(자료위치);
    if(ogologo_valuu>128||datà->size<ogologo_valuu+24)return 0;
    unsigned moòdù_valuu=assh_load_u32(자료위치+4+ogologo_valuu+16);
    return moòdù_valuu<=2048&&datà->size==ogologo_valuu+24+moòdù_valuu;
}
static void 요청처리(struct assh_event_request_s *mmèrème) {
    if(!인증됨||mmèrème->ch!=ọwa_ndebà||!ọwa_ndebà)return;
    if(같은말(&mmèrème->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&mmèrème->rq_data))mmèrème->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&mmèrème->type,"window-change")) {
        if(셸시작됨&&mmèrème->rq_data.size==16)mmèrème->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *Ntiiwu=0;unsigned ogologo_valuu=0;
    if(같은말(&mmèrème->type,"exec")) {
        if(mmèrème->rq_data.size<4)return;
        ogologo_valuu=assh_load_u32(mmèrème->rq_data.data);
        if(!ogologo_valuu||ogologo_valuu>2048||mmèrème->rq_data.size!=ogologo_valuu+4)return;
        Ntiiwu=mmèrème->rq_data.data+4;
        for(unsigned 순번=0;순번<ogologo_valuu;순번++)if(!Ntiiwu[순번])return;
        nnyemiwu_pinye=1;
    }else if(!같은말(&mmèrème->type,"shell")||mmèrème->rq_data.size)return;
    if(sizeof(입력줄)-입력수<ogologo_valuu+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(ogologo_valuu)원격입력넣기(Ntiiwu,ogologo_valuu);원격입력넣기(&끝,1);
    셸시작됨=1;mmèrème->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!nnyemiwu_pinye){const char *GỤ̀ỌM_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*GỤ̀ỌM_eb81d7d9)원격출력(*GỤ̀ỌM_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(ibè_valuu<0){if(지금<재접속시각)return;ibè_valuu=망연결받기(듣는곳);if(ibè_valuu<0)return;
        접속시각=지금;assh_status_t mmejọ=assh_session_create(Ọnọdụ_valuu,&njikọ_e05f319b);
        if(mmejọ){njikọ_e05f319b=0;진단("SSH session error ",mmejọ);mmechi_njikọ();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){mmechi_njikọ();return;}
    if(ọwa_ndebà&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t mmejọ=assh_channel_data(ọwa_ndebà,출력줄+출력앞,&수);
            if(!mmejọ){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(mmejọ!=ASSH_NO_DATA){mmechi_njikọ();return;}
        }
        if(mèdebe_ọnọdụ>=0&&!출력수){unsigned char ọnọdụ_valuu[4];assh_store_u32(ọnọdụ_valuu,(uint32_t)mèdebe_ọnọdụ);
            if(assh_request(njikọ_e05f319b,ọwa_ndebà,"exit-status",11,ọnọdụ_valuu,4,0)||assh_channel_eof(ọwa_ndebà)||assh_channel_close(ọwa_ndebà)) {mmechi_njikọ();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned NSOTANSO_valuu=0;NSOTANSO_valuu<16;NSOTANSO_valuu++) {
        struct assh_event_s mmèrème;
        if(!assh_event_get(njikọ_e05f319b,&mmèrème,지금/1000)){mmechi_njikọ();return;}
        assh_status_t mmejọ=ASSH_OK;int 쉬기=0,끊기=0;
        switch(mmèrème.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(ibè_valuu,mmèrème.transport.read.buf.data,mmèrème.transport.read.buf.size);
            if(수>0)mmèrème.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(ibè_valuu,mmèrème.transport.write.buf.data,mmèrème.transport.write.buf.size);
            if(수>0)mmèrème.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            mmèrème.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(mmèrème.userauth_server.methods.retries>3)mmèrème.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *datà=&mmèrème.userauth_server.password;
            if(같은말(&datà->username,"user")&&datà->password.size<=256&&!datà->new_password.size) {
                unsigned char nchịkọta_valuu[32];ebe_dị̀anyā_nchịkọta(datà->password.data,datà->password.size,nchịkọta_valuu);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=nchịkọta_valuu[순번]^nkọwannyemiwu_okwuntughe_nchịkọta[순번];memset(nchịkọta_valuu,0,32);
                if(!차이)datà->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *datà=&mmèrème.connection.channel_open;
            if(인증됨&&!ọwa_ndebà&&셸대기중&&같은말(&datà->type,"session")&&!datà->rq_data.size) {
                datà->reply=ASSH_CONNECTION_REPLY_SUCCESS;datà->pkt_size=4096;
                datà->win_size=-1;ọwa_ndebà=datà->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&mmèrème.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *datà=&mmèrème.connection.channel_data;
            if(!셸시작됨||datà->ch!=ọwa_ndebà||datà->ext){끊기=1;break;}
            unsigned 수=datà->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(datà->data.data[순번]==4){mèdebe_ọnọdụ=0;수=순번;datà->transferred=datà->data.size;break;}
            원격입력넣기(datà->data.data,수);if(!datà->transferred)datà->transferred=수;
            if(!수&&mèdebe_ọnọdụ<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: ọwa_ndebà=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",mmèrème.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(njikọ_e05f319b,&mmèrème,mmejọ);
        if(끊기){mmechi_njikọ();return;}if(쉬기)return;
    }
}
