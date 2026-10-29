/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "दुर्मीळ_मोल.h"
#include "암호기반.h"
#include "प्रोफायल.h"
#include "../नॅटवर्क_स्टॅक/नॅटवर्क_स्टॅक.h"
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
static struct assh_context_s *मजकूर_मोल;
static struct assh_session_s *कनॅक्शन_e05f319b;
static struct assh_channel_s *चॅनल_प्रवेश;
static int 듣는곳=-1,पीयर_मोल=-1,인증됨,셸시작됨,आदेश_TYPE,सोपोवचें_स्थिती_2bce2943=-1,닫을예정,स्टार्टअप_चूक,셸대기중;
static uintptr_t कनॅक्शन_TIME,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned मोल) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char अंक_मोल[12];unsigned 수=0;do{अंक_मोल[수++]='0'+मोल%10;मोल/=10;}while(मोल);
    while(수)보드글자쓰기(अंक_मोल[--수]);보드글자쓰기(10);
}
static assh_status_t तयार_करचें_मेमरी(void *डेटा,void **नामो,size_t आवाठ,enum assh_alloc_type_e 종류) {
    (void)डेटा;(void)종류;
    if(!आवाठ){रिलीज_दुर्मीळ(*नामो);*नामो=0;return ASSH_OK;}
    void *새주소=원격재할당(*नामो,आवाठ);
    if(!새주소)return ASSH_ERR_MEM;*नामो=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *डेटा,const struct assh_buffer_s *सीड_मोल) {
    (void)डेटा;(void)सीड_मोल;unsigned char 시험[32];int मेजप=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return मेजप?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *डेटा,uint8_t *मेजप,size_t लांबाय_मोल,uint_fast8_t 종류) {
    (void)डेटा;(void)종류;if(लांबाय_मोल>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(मेजप,लांबाय_मोल)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *डेटा){(void)डेटा;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void शेवट_कनॅक्शन(void) {
    인증됨=셸시작됨=0;चॅनल_प्रवेश=0;
    if(कनॅक्शन_e05f319b)assh_session_release(कनॅक्शन_e05f319b);कनॅक्शन_e05f319b=0;
    if(पीयर_मोल>=0)शेवट_नॅटवर्क(पीयर_मोल);पीयर_मोल=-1;आदेश_TYPE=0;सोपोवचें_स्थिती_2bce2943=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *डेटा,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=डेटा[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int वर्ण_मोल=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return वर्ण_मोल;
}
void 원격출력(unsigned char वर्ण_मोल) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=वर्ण_मोल==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=वर्ण_मोल;이전출력=वर्ण_मोल;
}
uintptr_t बोर्ड_सोपोवचें_दुर्मीळ_आदेश(uintptr_t स्थिती_मोल_e10195a1){if(셸시작됨&&आदेश_TYPE)सोपोवचें_स्थिती_2bce2943=(int)स्थिती_मोल_e10195a1;return 0;}
uintptr_t 보드원격대기(uintptr_t स्थिती_मोल_e10195a1){셸대기중=स्थिती_मोल_e10195a1!=0;return 0;}
static int तयार_करचें_शॅल(void) {
    if(듣는곳>=0)return 0;
    if(!मजकूर_मोल){
        assh_status_t चूक=assh_context_create(&मजकूर_मोल,ASSH_SERVER,तयार_करचें_मेमरी,0,&난수기,0);
        if(चूक)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *पद्दत_मोड[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        चूक=assh_algo_register(मजकूर_मोल,ASSH_SAFETY_WEAK,पद्दत_मोड);
        if(!चूक)चूक=assh_service_register_va(मजकूर_मोल,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=मोबायल_की;
        if(!चूक)चूक=assh_key_load(मजकूर_मोल,assh_context_keys(मजकूर_मोल),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(मोबायल_की));
        if(चूक){진단("SSH init error ",चूक);assh_context_release(मजकूर_मोल);मजकूर_मोल=0;return -5;}
    }
    int पोर्ट_मोल=통신끝점만들기(1);if(पोर्ट_मोल<0)return पोर्ट_मोल;통신주소재사용(पोर्ट_मोल);
    int मेजप=망주소묶기(पोर्ट_मोल,0,22);if(!मेजप)मेजप=연결기다리기(पोर्ट_मोल);
    if(मेजप<0){शेवट_नॅटवर्क(पोर्ट_मोल);return मेजप;}듣는곳=पोर्ट_मोल;return 0;
}
uintptr_t बोर्ड_छायांकन(uintptr_t 종류,uintptr_t कृती) {
    if(종류==1)return(uint32_t)नियंत्रण_दुर्मीळ_प्रदर्शन(कृती);
    if(कृती==0){शेवट_कनॅक्शन();if(듣는곳>=0)शेवट_नॅटवर्क(듣는곳);듣는곳=-1;return 0;}
    if(कृती==1){स्टार्टअप_चूक=तयार_करचें_शॅल();return(uint32_t)स्टार्टअप_चूक;}
    return(uint32_t)(듣는곳>=0?1:स्टार्टअप_चूक);
}
void तयार_करचें_दुर्मीळ(void){स्टार्टअप_चूक=तयार_करचें_शॅल();नियंत्रण_दुर्मीळ_प्रदर्शन(1);}
static int 같은말(const struct assh_cbuffer_s *डेटा,const char *Word_SMS) {
    size_t लांबाय_मोल=strlen(Word_SMS);return डेटा->size==लांबाय_मोल&&!memcmp(डेटा->data,Word_SMS,लांबाय_मोल);
}
static int 터미널요청(const struct assh_cbuffer_s *डेटा) {
    if(डेटा->size<24)return 0;
    const unsigned char *डेटा_स्थिती=डेटा->data;unsigned लांबाय_मोल=assh_load_u32(डेटा_स्थिती);
    if(लांबाय_मोल>128||डेटा->size<लांबाय_मोल+24)return 0;
    unsigned मोड_मोल=assh_load_u32(डेटा_स्थिती+4+लांबाय_मोल+16);
    return मोड_मोल<=2048&&डेटा->size==लांबाय_मोल+24+मोड_मोल;
}
static void 요청처리(struct assh_event_request_s *प्रसंग) {
    if(!인증됨||प्रसंग->ch!=चॅनल_प्रवेश||!चॅनल_प्रवेश)return;
    if(같은말(&प्रसंग->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&प्रसंग->rq_data))प्रसंग->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&प्रसंग->type,"window-change")) {
        if(셸시작됨&&प्रसंग->rq_data.size==16)प्रसंग->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *आदेश=0;unsigned लांबाय_मोल=0;
    if(같은말(&प्रसंग->type,"exec")) {
        if(प्रसंग->rq_data.size<4)return;
        लांबाय_मोल=assh_load_u32(प्रसंग->rq_data.data);
        if(!लांबाय_मोल||लांबाय_मोल>2048||प्रसंग->rq_data.size!=लांबाय_मोल+4)return;
        आदेश=प्रसंग->rq_data.data+4;
        for(unsigned 순번=0;순번<लांबाय_मोल;순번++)if(!आदेश[순번])return;
        आदेश_TYPE=1;
    }else if(!같은말(&प्रसंग->type,"shell")||प्रसंग->rq_data.size)return;
    if(sizeof(입력줄)-입력수<लांबाय_मोल+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(लांबाय_मोल)원격입력넣기(आदेश,लांबाय_मोल);원격입력넣기(&끝,1);
    셸시작됨=1;प्रसंग->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!आदेश_TYPE){const char *README_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*README_eb81d7d9)원격출력(*README_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t NOW_मोल=보드밀리초();
    if(पीयर_मोल<0){if(NOW_मोल<재접속시각)return;पीयर_मोल=망연결받기(듣는곳);if(पीयर_मोल<0)return;
        कनॅक्शन_TIME=NOW_मोल;assh_status_t चूक=assh_session_create(मजकूर_मोल,&कनॅक्शन_e05f319b);
        if(चूक){कनॅक्शन_e05f319b=0;진단("SSH session error ",चूक);शेवट_कनॅक्शन();return;}}
    if((!인증됨&&NOW_मोल-कनॅक्शन_TIME>30000)||닫을예정==2||(닫을예정&&NOW_मोल>=닫는시각)){शेवट_कनॅक्शन();return;}
    if(चॅनल_प्रवेश&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t चूक=assh_channel_data(चॅनल_प्रवेश,출력줄+출력앞,&수);
            if(!चूक){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(चूक!=ASSH_NO_DATA){शेवट_कनॅक्शन();return;}
        }
        if(सोपोवचें_स्थिती_2bce2943>=0&&!출력수){unsigned char स्थिती_मोल_e10195a1[4];assh_store_u32(स्थिती_मोल_e10195a1,(uint32_t)सोपोवचें_स्थिती_2bce2943);
            if(assh_request(कनॅक्शन_e05f319b,चॅनल_प्रवेश,"exit-status",11,स्थिती_मोल_e10195a1,4,0)||assh_channel_eof(चॅनल_प्रवेश)||assh_channel_close(चॅनल_प्रवेश)) {शेवट_कनॅक्शन();return;}
            닫을예정=1;닫는시각=NOW_मोल+3000;
        }
    }
    for(unsigned SEQUENCE_मोल=0;SEQUENCE_मोल<16;SEQUENCE_मोल++) {
        struct assh_event_s प्रसंग;
        if(!assh_event_get(कनॅक्शन_e05f319b,&प्रसंग,NOW_मोल/1000)){शेवट_कनॅक्शन();return;}
        assh_status_t चूक=ASSH_OK;int 쉬기=0,끊기=0;
        switch(प्रसंग.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(पीयर_मोल,प्रसंग.transport.read.buf.data,प्रसंग.transport.read.buf.size);
            if(수>0)प्रसंग.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(पीयर_मोल,प्रसंग.transport.write.buf.data,प्रसंग.transport.write.buf.size);
            if(수>0)प्रसंग.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            प्रसंग.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(प्रसंग.userauth_server.methods.retries>3)प्रसंग.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *डेटा=&प्रसंग.userauth_server.password;
            if(같은말(&डेटा->username,"user")&&डेटा->password.size<=256&&!डेटा->new_password.size) {
                unsigned char सारांश_मोल[32];दुर्मीळ_सारांश(डेटा->password.data,डेटा->password.size,सारांश_मोल);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=सारांश_मोल[순번]^शॅल_पासवर्ड_सारांश[순번];memset(सारांश_मोल,0,32);
                if(!차이)डेटा->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *डेटा=&प्रसंग.connection.channel_open;
            if(인증됨&&!चॅनल_प्रवेश&&셸대기중&&같은말(&डेटा->type,"session")&&!डेटा->rq_data.size) {
                डेटा->reply=ASSH_CONNECTION_REPLY_SUCCESS;डेटा->pkt_size=4096;
                डेटा->win_size=-1;चॅनल_प्रवेश=डेटा->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&प्रसंग.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *डेटा=&प्रसंग.connection.channel_data;
            if(!셸시작됨||डेटा->ch!=चॅनल_प्रवेश||डेटा->ext){끊기=1;break;}
            unsigned 수=डेटा->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(डेटा->data.data[순번]==4){सोपोवचें_स्थिती_2bce2943=0;수=순번;डेटा->transferred=डेटा->data.size;break;}
            원격입력넣기(डेटा->data.data,수);if(!डेटा->transferred)डेटा->transferred=수;
            if(!수&&सोपोवचें_स्थिती_2bce2943<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: चॅनल_प्रवेश=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_मोल+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",प्रसंग.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(कनॅक्शन_e05f319b,&प्रसंग,चूक);
        if(끊기){शेवट_कनॅक्शन();return;}if(쉬기)return;
    }
}
