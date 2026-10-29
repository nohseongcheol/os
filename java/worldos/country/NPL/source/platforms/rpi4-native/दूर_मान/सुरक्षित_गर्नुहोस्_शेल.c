/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "दूर_मान.h"
#include "암호기반.h"
#include "प्रोफाइल.h"
#include "../सञ्जाल_चाङ/सञ्जाल_चाङ.h"
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
static struct assh_context_s *प्रसङ्ग_मान;
static struct assh_session_s *जडान_e05f319b;
static struct assh_channel_s *च्यानल_प्रविष्टि;
static int 듣는곳=-1,समान_मान=-1,인증됨,셸시작됨,आदेश_प्रकार,समाप्त_गर्नुहोस्_स्थिति=-1,닫을예정,स्टार्टअप_त्रुटि,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *शब्द_पाठ,unsigned मान) {
    while(*शब्द_पाठ)보드글자쓰기(*शब्द_पाठ++);
    char अङ्क_मान[12];unsigned 수=0;do{अङ्क_मान[수++]='0'+मान%10;मान/=10;}while(मान);
    while(수)보드글자쓰기(अङ्क_मान[--수]);보드글자쓰기(10);
}
static assh_status_t तयार_गर्नुहोस्_मेमोरी(void *लगत,void **ठेगाना,size_t आकार,enum assh_alloc_type_e 종류) {
    (void)लगत;(void)종류;
    if(!आकार){जारी_दूर(*ठेगाना);*ठेगाना=0;return ASSH_OK;}
    void *새주소=원격재할당(*ठेगाना,आकार);
    if(!새주소)return ASSH_ERR_MEM;*ठेगाना=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *लगत,const struct assh_buffer_s *सिड_मान) {
    (void)लगत;(void)सिड_मान;unsigned char 시험[32];int मापन=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return मापन?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *लगत,uint8_t *मापन,size_t लम्बाइ_मान,uint_fast8_t 종류) {
    (void)लगत;(void)종류;if(लम्बाइ_मान>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(मापन,लम्बाइ_मान)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *लगत){(void)लगत;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void बन्द_गर्नुहोस्_जडान(void) {
    인증됨=셸시작됨=0;च्यानल_प्रविष्टि=0;
    if(जडान_e05f319b)assh_session_release(जडान_e05f319b);जडान_e05f319b=0;
    if(समान_मान>=0)बन्द_गर्नुहोस्_सञ्जाल(समान_मान);समान_मान=-1;आदेश_प्रकार=0;समाप्त_गर्नुहोस्_स्थिति=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *लगत,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=लगत[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int वर्ण_मान=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return वर्ण_मान;
}
void 원격출력(unsigned char वर्ण_मान) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=वर्ण_मान==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=वर्ण_मान;이전출력=वर्ण_मान;
}
uintptr_t बोर्ड_समाप्त_गर्नुहोस्_दूर_आदेश(uintptr_t स्थिति_मान){if(셸시작됨&&आदेश_प्रकार)समाप्त_गर्नुहोस्_स्थिति=(int)स्थिति_मान;return 0;}
uintptr_t 보드원격대기(uintptr_t स्थिति_मान){셸대기중=स्थिति_मान!=0;return 0;}
static int तयार_गर्नुहोस्_शेल(void) {
    if(듣는곳>=0)return 0;
    if(!प्रसङ्ग_मान){
        assh_status_t त्रुटि=assh_context_create(&प्रसङ्ग_मान,ASSH_SERVER,तयार_गर्नुहोस्_मेमोरी,0,&난수기,0);
        if(त्रुटि)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *तरिका_मोड[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        त्रुटि=assh_algo_register(प्रसङ्ग_मान,ASSH_SAFETY_WEAK,तरिका_मोड);
        if(!त्रुटि)त्रुटि=assh_service_register_va(प्रसङ्ग_मान,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=मोबाइल_कुञ्जी;
        if(!त्रुटि)त्रुटि=assh_key_load(प्रसङ्ग_मान,assh_context_keys(प्रसङ्ग_मान),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(मोबाइल_कुञ्जी));
        if(त्रुटि){진단("SSH init error ",त्रुटि);assh_context_release(प्रसङ्ग_मान);प्रसङ्ग_मान=0;return -5;}
    }
    int पोर्ट_मान=통신끝점만들기(1);if(पोर्ट_मान<0)return पोर्ट_मान;통신주소재사용(पोर्ट_मान);
    int मापन=망주소묶기(पोर्ट_मान,0,22);if(!मापन)मापन=연결기다리기(पोर्ट_मान);
    if(मापन<0){बन्द_गर्नुहोस्_सञ्जाल(पोर्ट_मान);return मापन;}듣는곳=पोर्ट_मान;return 0;
}
uintptr_t बोर्ड_स्याडोइङ(uintptr_t 종류,uintptr_t कार्य) {
    if(종류==1)return(uint32_t)नियन्त्रण_दूर_प्रदर्शन(कार्य);
    if(कार्य==0){बन्द_गर्नुहोस्_जडान();if(듣는곳>=0)बन्द_गर्नुहोस्_सञ्जाल(듣는곳);듣는곳=-1;return 0;}
    if(कार्य==1){स्टार्टअप_त्रुटि=तयार_गर्नुहोस्_शेल();return(uint32_t)स्टार्टअप_त्रुटि;}
    return(uint32_t)(듣는곳>=0?1:स्टार्टअप_त्रुटि);
}
void तयार_गर्नुहोस्_दूर(void){स्टार्टअप_त्रुटि=तयार_गर्नुहोस्_शेल();नियन्त्रण_दूर_प्रदर्शन(1);}
static int 같은말(const struct assh_cbuffer_s *लगत,const char *शब्द_पाठ) {
    size_t लम्बाइ_मान=strlen(शब्द_पाठ);return लगत->size==लम्बाइ_मान&&!memcmp(लगत->data,शब्द_पाठ,लम्बाइ_मान);
}
static int 터미널요청(const struct assh_cbuffer_s *लगत) {
    if(लगत->size<24)return 0;
    const unsigned char *लगत_राख्नुहोस्=लगत->data;unsigned लम्बाइ_मान=assh_load_u32(लगत_राख्नुहोस्);
    if(लम्बाइ_मान>128||लगत->size<लम्बाइ_मान+24)return 0;
    unsigned मोड_मान=assh_load_u32(लगत_राख्नुहोस्+4+लम्बाइ_मान+16);
    return मोड_मान<=2048&&लगत->size==लम्बाइ_मान+24+मोड_मान;
}
static void 요청처리(struct assh_event_request_s *घटना) {
    if(!인증됨||घटना->ch!=च्यानल_प्रविष्टि||!च्यानल_प्रविष्टि)return;
    if(같은말(&घटना->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&घटना->rq_data))घटना->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&घटना->type,"window-change")) {
        if(셸시작됨&&घटना->rq_data.size==16)घटना->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *आदेश=0;unsigned लम्बाइ_मान=0;
    if(같은말(&घटना->type,"exec")) {
        if(घटना->rq_data.size<4)return;
        लम्बाइ_मान=assh_load_u32(घटना->rq_data.data);
        if(!लम्बाइ_मान||लम्बाइ_मान>2048||घटना->rq_data.size!=लम्बाइ_मान+4)return;
        आदेश=घटना->rq_data.data+4;
        for(unsigned 순번=0;순번<लम्बाइ_मान;순번++)if(!आदेश[순번])return;
        आदेश_प्रकार=1;
    }else if(!같은말(&घटना->type,"shell")||घटना->rq_data.size)return;
    if(sizeof(입력줄)-입력수<लम्बाइ_मान+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(लम्बाइ_मान)원격입력넣기(आदेश,लम्बाइ_मान);원격입력넣기(&끝,1);
    셸시작됨=1;घटना->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!आदेश_प्रकार){const char *readme_फाइल_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*readme_फाइल_eb81d7d9)원격출력(*readme_फाइल_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(समान_मान<0){if(지금<재접속시각)return;समान_मान=망연결받기(듣는곳);if(समान_मान<0)return;
        접속시각=지금;assh_status_t त्रुटि=assh_session_create(प्रसङ्ग_मान,&जडान_e05f319b);
        if(त्रुटि){जडान_e05f319b=0;진단("SSH session error ",त्रुटि);बन्द_गर्नुहोस्_जडान();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){बन्द_गर्नुहोस्_जडान();return;}
    if(च्यानल_प्रविष्टि&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t त्रुटि=assh_channel_data(च्यानल_प्रविष्टि,출력줄+출력앞,&수);
            if(!त्रुटि){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(त्रुटि!=ASSH_NO_DATA){बन्द_गर्नुहोस्_जडान();return;}
        }
        if(समाप्त_गर्नुहोस्_स्थिति>=0&&!출력수){unsigned char स्थिति_मान[4];assh_store_u32(स्थिति_मान,(uint32_t)समाप्त_गर्नुहोस्_स्थिति);
            if(assh_request(जडान_e05f319b,च्यानल_प्रविष्टि,"exit-status",11,स्थिति_मान,4,0)||assh_channel_eof(च्यानल_प्रविष्टि)||assh_channel_close(च्यानल_प्रविष्टि)) {बन्द_गर्नुहोस्_जडान();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s घटना;
        if(!assh_event_get(जडान_e05f319b,&घटना,지금/1000)){बन्द_गर्नुहोस्_जडान();return;}
        assh_status_t त्रुटि=ASSH_OK;int 쉬기=0,끊기=0;
        switch(घटना.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(समान_मान,घटना.transport.read.buf.data,घटना.transport.read.buf.size);
            if(수>0)घटना.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(समान_मान,घटना.transport.write.buf.data,घटना.transport.write.buf.size);
            if(수>0)घटना.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            घटना.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(घटना.userauth_server.methods.retries>3)घटना.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *लगत=&घटना.userauth_server.password;
            if(같은말(&लगत->username,"user")&&लगत->password.size<=256&&!लगत->new_password.size) {
                unsigned char सारांश_मान[32];दूर_सारांश(लगत->password.data,लगत->password.size,सारांश_मान);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=सारांश_मान[순번]^शेल_पासवर्ड_सारांश[순번];memset(सारांश_मान,0,32);
                if(!차이)लगत->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *लगत=&घटना.connection.channel_open;
            if(인증됨&&!च्यानल_प्रविष्टि&&셸대기중&&같은말(&लगत->type,"session")&&!लगत->rq_data.size) {
                लगत->reply=ASSH_CONNECTION_REPLY_SUCCESS;लगत->pkt_size=4096;
                लगत->win_size=-1;च्यानल_प्रविष्टि=लगत->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&घटना.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *लगत=&घटना.connection.channel_data;
            if(!셸시작됨||लगत->ch!=च्यानल_प्रविष्टि||लगत->ext){끊기=1;break;}
            unsigned 수=लगत->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(लगत->data.data[순번]==4){समाप्त_गर्नुहोस्_स्थिति=0;수=순번;लगत->transferred=लगत->data.size;break;}
            원격입력넣기(लगत->data.data,수);if(!लगत->transferred)लगत->transferred=수;
            if(!수&&समाप्त_गर्नुहोस्_स्थिति<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: च्यानल_प्रविष्टि=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",घटना.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(जडान_e05f319b,&घटना,त्रुटि);
        if(끊기){बन्द_गर्नुहोस्_जडान();return;}if(쉬기)return;
    }
}
