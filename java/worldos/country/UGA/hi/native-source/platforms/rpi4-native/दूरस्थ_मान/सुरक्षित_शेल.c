/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "दूरस्थ_मान.h"
#include "क्रिप्टोग्राफ़ी_समर्थन.h"
#include "प्रोफ़ाइल.h"
#include "../नेटवर्क_स्टैक/नेटवर्क_स्टैक.h"
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
static struct assh_session_s *कनेक्शन_e05f319b;
static struct assh_channel_s *चैनल_एन्ट्री;
static int सुन_रहा_है_एंडपॉइंट=-1,पीअर_मान=-1,인증됨,셸시작됨,आदेश_लिखें,समाप्त_करें_अवस्था=-1,닫을예정,स्टार्टअप_त्रुटि,शेल_प्रतीक्षा_कर_रहा_है;
static uintptr_t कनेक्शन_समय,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *शब्द_पाठ,unsigned मान) {
    while(*शब्द_पाठ)보드글자쓰기(*शब्द_पाठ++);
    char अंक_मान[12];unsigned 수=0;do{अंक_मान[수++]='0'+मान%10;मान/=10;}while(मान);
    while(수)보드글자쓰기(अंक_मान[--수]);보드글자쓰기(10);
}
static assh_status_t 기억마련(void *आँकड़े,void **पता,size_t आकार,enum assh_alloc_type_e 종류) {
    (void)आँकड़े;(void)종류;
    if(!आकार){रिलीज़_दूरस्थ(*पता);*पता=0;return ASSH_OK;}
    void *새주소=원격재할당(*पता,आकार);
    if(!새주소)return ASSH_ERR_MEM;*पता=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *आँकड़े,const struct assh_buffer_s *सीड_मान) {
    (void)आँकड़े;(void)सीड_मान;unsigned char 시험[32];int परिणाम=दूरस्थ_यादृच्_छिक(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return परिणाम?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t पढें_यादृच्_छिक(struct assh_context_s *आँकड़े,uint8_t *परिणाम,size_t 길이,uint_fast8_t 종류) {
    (void)आँकड़े;(void)종류;if(길이>65536)return ASSH_ERR_CRYPTO;
    return दूरस्थ_यादृच्_छिक(परिणाम,길이)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void यादृच्_छिक_समाप्त_करें(struct assh_context_s *आँकड़े){(void)आँकड़े;}
static const struct assh_prng_s यादृच्_छिक_जनरेटर={난수준비,पढें_यादृच्_छिक,यादृच्_छिक_समाप्त_करें};
static void बंद_कनेक्शन(void) {
    인증됨=셸시작됨=0;चैनल_एन्ट्री=0;
    if(कनेक्शन_e05f319b)assh_session_release(कनेक्शन_e05f319b);कनेक्शन_e05f319b=0;
    if(पीअर_मान>=0)बंद_नेटवर्क(पीअर_मान);पीअर_मान=-1;आदेश_लिखें=0;समाप्त_करें_अवस्था=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *आँकड़े,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=आँकड़े[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int कैरेक्टर_मान=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return कैरेक्टर_मान;
}
void 원격출력(unsigned char कैरेक्टर_मान) {
    if(!셸시작됨||닫을예정)return;
    unsigned जोड़ें_मोड=कैरेक्टर_मान==10&&이전출력!=13;
    if(출력수+1+जोड़ें_मोड>sizeof(출력줄)){닫을예정=2;return;}
    if(जोड़ें_मोड)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=कैरेक्टर_मान;이전출력=कैरेक्टर_मान;
}
uintptr_t बोर्ड_समाप्त_करें_दूरस्थ_आदेश(uintptr_t अवस्था_मान){if(셸시작됨&&आदेश_लिखें)समाप्त_करें_अवस्था=(int)अवस्था_मान;return 0;}
uintptr_t बोर्ड_दूरस्थ_प्रतीक्षा_करें(uintptr_t अवस्था_मान){शेल_प्रतीक्षा_कर_रहा_है=अवस्था_मान!=0;return 0;}
static int 셸준비(void) {
    if(सुन_रहा_है_एंडपॉइंट>=0)return 0;
    if(!문맥){
        assh_status_t त्रुटि=assh_context_create(&문맥,ASSH_SERVER,기억마련,0,&यादृच्_छिक_जनरेटर,0);
        if(त्रुटि)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *विधि_मोड[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        त्रुटि=assh_algo_register(문맥,ASSH_SAFETY_WEAK,विधि_मोड);
        if(!त्रुटि)त्रुटि=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=उपकरण_कुंजी;
        if(!त्रुटि)त्रुटि=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(उपकरण_कुंजी));
        if(त्रुटि){진단("SSH init error ",त्रुटि);assh_context_release(문맥);문맥=0;return -5;}
    }
    int पोर्ट_मान=बनाएँ_सॉकेट_एंडपॉइंट(1);if(पोर्ट_मान<0)return पोर्ट_मान;통신주소재사용(पोर्ट_मान);
    int परिणाम=망주소묶기(पोर्ट_मान,0,22);if(!परिणाम)परिणाम=연결기다리기(पोर्ट_मान);
    if(परिणाम<0){बंद_नेटवर्क(पोर्ट_मान);return परिणाम;}सुन_रहा_है_एंडपॉइंट=पोर्ट_मान;return 0;
}
uintptr_t बोर्ड_शैडोइंग(uintptr_t 종류,uintptr_t क्रिया) {
    if(종류==1)return(uint32_t)नियंत्रण_दूरस्थ_डिस्प्ले(क्रिया);
    if(क्रिया==0){बंद_कनेक्शन();if(सुन_रहा_है_एंडपॉइंट>=0)बंद_नेटवर्क(सुन_रहा_है_एंडपॉइंट);सुन_रहा_है_एंडपॉइंट=-1;return 0;}
    if(क्रिया==1){स्टार्टअप_त्रुटि=셸준비();return(uint32_t)स्टार्टअप_त्रुटि;}
    return(uint32_t)(सुन_रहा_है_एंडपॉइंट>=0?1:स्टार्टअप_त्रुटि);
}
void 원격준비(void){स्टार्टअप_त्रुटि=셸준비();नियंत्रण_दूरस्थ_डिस्प्ले(1);}
static int 같은말(const struct assh_cbuffer_s *आँकड़े,const char *शब्द_पाठ) {
    size_t 길이=strlen(शब्द_पाठ);return आँकड़े->size==길이&&!memcmp(आँकड़े->data,शब्द_पाठ,길이);
}
static int टर्मिनल_अनुरोध(const struct assh_cbuffer_s *आँकड़े) {
    if(आँकड़े->size<24)return 0;
    const unsigned char *डेटा_पद=आँकड़े->data;unsigned 길이=assh_load_u32(डेटा_पद);
    if(길이>128||आँकड़े->size<길이+24)return 0;
    unsigned मोड_मान=assh_load_u32(डेटा_पद+4+길이+16);
    return मोड_मान<=2048&&आँकड़े->size==길이+24+मोड_मान;
}
static void हैंडल_अनुरोध(struct assh_event_request_s *घटना) {
    if(!인증됨||घटना->ch!=चैनल_एन्ट्री||!चैनल_एन्ट्री)return;
    if(같은말(&घटना->type,"pty-req")) {
        if(!셸시작됨&&टर्मिनल_अनुरोध(&घटना->rq_data))घटना->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&घटना->type,"window-change")) {
        if(셸시작됨&&घटना->rq_data.size==16)घटना->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!शेल_प्रतीक्षा_कर_रहा_है)return;
    const unsigned char *आदेश=0;unsigned 길이=0;
    if(같은말(&घटना->type,"exec")) {
        if(घटना->rq_data.size<4)return;
        길이=assh_load_u32(घटना->rq_data.data);
        if(!길이||길이>2048||घटना->rq_data.size!=길이+4)return;
        आदेश=घटना->rq_data.data+4;
        for(unsigned 순번=0;순번<길이;순번++)if(!आदेश[순번])return;
        आदेश_लिखें=1;
    }else if(!같은말(&घटना->type,"shell")||घटना->rq_data.size)return;
    if(sizeof(입력줄)-입력수<길이+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(길이)원격입력넣기(आदेश,길이);원격입력넣기(&끝,1);
    셸시작됨=1;घटना->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!आदेश_लिखें){const char *ReadMe_फ़ाइल_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*ReadMe_फ़ाइल_eb81d7d9)원격출력(*ReadMe_फ़ाइल_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(सुन_रहा_है_एंडपॉइंट<0)return;
    uintptr_t अभी_प्रासंगिक_मान=보드밀리초();
    if(पीअर_मान<0){if(अभी_प्रासंगिक_मान<재접속시각)return;पीअर_मान=망연결받기(सुन_रहा_है_एंडपॉइंट);if(पीअर_मान<0)return;
        कनेक्शन_समय=अभी_प्रासंगिक_मान;assh_status_t त्रुटि=assh_session_create(문맥,&कनेक्शन_e05f319b);
        if(त्रुटि){कनेक्शन_e05f319b=0;진단("SSH session error ",त्रुटि);बंद_कनेक्शन();return;}}
    if((!인증됨&&अभी_प्रासंगिक_मान-कनेक्शन_समय>30000)||닫을예정==2||(닫을예정&&अभी_प्रासंगिक_मान>=닫는시각)){बंद_कनेक्शन();return;}
    if(चैनल_एन्ट्री&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t त्रुटि=assh_channel_data(चैनल_एन्ट्री,출력줄+출력앞,&수);
            if(!त्रुटि){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(त्रुटि!=ASSH_NO_DATA){बंद_कनेक्शन();return;}
        }
        if(समाप्त_करें_अवस्था>=0&&!출력수){unsigned char अवस्था_मान[4];assh_store_u32(अवस्था_मान,(uint32_t)समाप्त_करें_अवस्था);
            if(assh_request(कनेक्शन_e05f319b,चैनल_एन्ट्री,"exit-status",11,अवस्था_मान,4,0)||assh_channel_eof(चैनल_एन्ट्री)||assh_channel_close(चैनल_एन्ट्री)) {बंद_कनेक्शन();return;}
            닫을예정=1;닫는시각=अभी_प्रासंगिक_मान+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s घटना;
        if(!assh_event_get(कनेक्शन_e05f319b,&घटना,अभी_प्रासंगिक_मान/1000)){बंद_कनेक्शन();return;}
        assh_status_t त्रुटि=ASSH_OK;int 쉬기=0,डिस्कनेक्ट_करें_एंडपॉइंट=0;
        switch(घटना.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(पीअर_मान,घटना.transport.read.buf.data,घटना.transport.read.buf.size);
            if(수>0)घटना.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else डिस्कनेक्ट_करें_एंडपॉइंट=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(पीअर_मान,घटना.transport.write.buf.data,घटना.transport.write.buf.size);
            if(수>0)घटना.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else डिस्कनेक्ट_करें_एंडपॉइंट=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            घटना.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(घटना.userauth_server.methods.retries>3)घटना.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *आँकड़े=&घटना.userauth_server.password;
            if(같은말(&आँकड़े->username,"user")&&आँकड़े->password.size<=256&&!आँकड़े->new_password.size) {
                unsigned char सारांश_मान[32];दूरस्थ_सारांश(आँकड़े->password.data,आँकड़े->password.size,सारांश_मान);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=सारांश_मान[순번]^शेल_पासवर्ड_सारांश[순번];memset(सारांश_मान,0,32);
                if(!차이)आँकड़े->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *आँकड़े=&घटना.connection.channel_open;
            if(인증됨&&!चैनल_एन्ट्री&&शेल_प्रतीक्षा_कर_रहा_है&&같은말(&आँकड़े->type,"session")&&!आँकड़े->rq_data.size) {
                आँकड़े->reply=ASSH_CONNECTION_REPLY_SUCCESS;आँकड़े->pkt_size=4096;
                आँकड़े->win_size=-1;चैनल_एन्ट्री=आँकड़े->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: हैंडल_अनुरोध(&घटना.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *आँकड़े=&घटना.connection.channel_data;
            if(!셸시작됨||आँकड़े->ch!=चैनल_एन्ट्री||आँकड़े->ext){डिस्कनेक्ट_करें_एंडपॉइंट=1;break;}
            unsigned 수=आँकड़े->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(आँकड़े->data.data[순번]==4){समाप्त_करें_अवस्था=0;수=순번;आँकड़े->transferred=आँकड़े->data.size;break;}
            원격입력넣기(आँकड़े->data.data,수);if(!आँकड़े->transferred)आँकड़े->transferred=수;
            if(!수&&समाप्त_करें_अवस्था<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: चैनल_एन्ट्री=0;셸시작됨=0;닫을예정=1;닫는시각=अभी_प्रासंगिक_मान+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",घटना.session.error.code);डिस्कनेक्ट_करें_एंडपॉइंट=1;break;
        case ASSH_EVENT_DISCONNECT: डिस्कनेक्ट_करें_एंडपॉइंट=1;break;
        default: break;
        }
        assh_event_done(कनेक्शन_e05f319b,&घटना,त्रुटि);
        if(डिस्कनेक्ट_करें_एंडपॉइंट){बंद_कनेक्शन();return;}if(쉬기)return;
    }
}
