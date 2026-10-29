/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "ርሑቕ_ዋጋ.h"
#include "암호기반.h"
#include "መግለጺ_መንነት.h"
#include "../ማሕበራዊ_ኔትወርክ_ድርደራ/ማሕበራዊ_ኔትወርክ_ድርደራ.h"
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
static struct assh_context_s *ኣተኣታትዋ_ዋጋ;
static struct assh_session_s *ርክብ_e05f319b;
static struct assh_channel_s *ጣብያ_ምእታው;
static int 듣는곳=-1,መዘና_ዋጋ=-1,인증됨,셸시작됨,ትእዛዝ_ዓይነት,ኣቑም_ደረጃ=-1,닫을예정,ምጅማር_ጌጋ,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *ናይ_ቃል_ጸወታ_ጽሑፍ,unsigned ዋጋ) {
    while(*ናይ_ቃል_ጸወታ_ጽሑፍ)보드글자쓰기(*ናይ_ቃል_ጸወታ_ጽሑፍ++);
    char ኣሃዝ_ዋጋ[12];unsigned 수=0;do{ኣሃዝ_ዋጋ[수++]='0'+ዋጋ%10;ዋጋ/=10;}while(ዋጋ);
    while(수)보드글자쓰기(ኣሃዝ_ዋጋ[--수]);보드글자쓰기(10);
}
static assh_status_t ኣዳልው_ማህደር_ዝኽረት(void *ሓበሬታ,void **ኣድራሻ,size_t መጠን,enum assh_alloc_type_e 종류) {
    (void)ሓበሬታ;(void)종류;
    if(!መጠን){ፍታሕ_ርሑቕ(*ኣድራሻ);*ኣድራሻ=0;return ASSH_OK;}
    void *새주소=원격재할당(*ኣድራሻ,መጠን);
    if(!새주소)return ASSH_ERR_MEM;*ኣድራሻ=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *ሓበሬታ,const struct assh_buffer_s *씨앗) {
    (void)ሓበሬታ;(void)씨앗;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *ሓበሬታ,uint8_t *결과,size_t ንውሓት_ዋጋ,uint_fast8_t 종류) {
    (void)ሓበሬታ;(void)종류;if(ንውሓት_ዋጋ>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,ንውሓት_ዋጋ)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *ሓበሬታ){(void)ሓበሬታ;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void ዕጸው_ርክብ(void) {
    인증됨=셸시작됨=0;ጣብያ_ምእታው=0;
    if(ርክብ_e05f319b)assh_session_release(ርክብ_e05f319b);ርክብ_e05f319b=0;
    if(መዘና_ዋጋ>=0)ዕጸው_ማሕበራዊ_ኔትወርክ(መዘና_ዋጋ);መዘና_ዋጋ=-1;ትእዛዝ_ዓይነት=0;ኣቑም_ደረጃ=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *ሓበሬታ,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=ሓበሬታ[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int ፊደል_ዋጋ=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return ፊደል_ዋጋ;
}
void 원격출력(unsigned char ፊደል_ዋጋ) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=ፊደል_ዋጋ==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=ፊደል_ዋጋ;이전출력=ፊደል_ዋጋ;
}
uintptr_t 보드원격명령끝(uintptr_t ደረጃ_ዋጋ){if(셸시작됨&&ትእዛዝ_ዓይነት)ኣቑም_ደረጃ=(int)ደረጃ_ዋጋ;return 0;}
uintptr_t 보드원격대기(uintptr_t ደረጃ_ዋጋ){셸대기중=ደረጃ_ዋጋ!=0;return 0;}
static int ኣዳልው_ሽፋን(void) {
    if(듣는곳>=0)return 0;
    if(!ኣተኣታትዋ_ዋጋ){
        assh_status_t ጌጋ=assh_context_create(&ኣተኣታትዋ_ዋጋ,ASSH_SERVER,ኣዳልው_ማህደር_ዝኽረት,0,&난수기,0);
        if(ጌጋ)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *ሜላ_ኹነት[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ጌጋ=assh_algo_register(ኣተኣታትዋ_ዋጋ,ASSH_SAFETY_WEAK,ሜላ_ኹነት);
        if(!ጌጋ)ጌጋ=assh_service_register_va(ኣተኣታትዋ_ዋጋ,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=መሳርሒ_መፍትሕ;
        if(!ጌጋ)ጌጋ=assh_key_load(ኣተኣታትዋ_ዋጋ,assh_context_keys(ኣተኣታትዋ_ዋጋ),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(መሳርሒ_መፍትሕ));
        if(ጌጋ){진단("SSH init error ",ጌጋ);assh_context_release(ኣተኣታትዋ_ዋጋ);ኣተኣታትዋ_ዋጋ=0;return -5;}
    }
    int ወደብ_ዋጋ=통신끝점만들기(1);if(ወደብ_ዋጋ<0)return ወደብ_ዋጋ;통신주소재사용(ወደብ_ዋጋ);
    int 결과=망주소묶기(ወደብ_ዋጋ,0,22);if(!결과)결과=연결기다리기(ወደብ_ዋጋ);
    if(결과<0){ዕጸው_ማሕበራዊ_ኔትወርክ(ወደብ_ዋጋ);return 결과;}듣는곳=ወደብ_ዋጋ;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t ስጉምቲ) {
    if(종류==1)return(uint32_t)ቁጽጽር_ርሑቕ_መርኣዪ(ስጉምቲ);
    if(ስጉምቲ==0){ዕጸው_ርክብ();if(듣는곳>=0)ዕጸው_ማሕበራዊ_ኔትወርክ(듣는곳);듣는곳=-1;return 0;}
    if(ስጉምቲ==1){ምጅማር_ጌጋ=ኣዳልው_ሽፋን();return(uint32_t)ምጅማር_ጌጋ;}
    return(uint32_t)(듣는곳>=0?1:ምጅማር_ጌጋ);
}
void ኣዳልው_ርሑቕ(void){ምጅማር_ጌጋ=ኣዳልው_ሽፋን();ቁጽጽር_ርሑቕ_መርኣዪ(1);}
static int 같은말(const struct assh_cbuffer_s *ሓበሬታ,const char *ናይ_ቃል_ጸወታ_ጽሑፍ) {
    size_t ንውሓት_ዋጋ=strlen(ናይ_ቃል_ጸወታ_ጽሑፍ);return ሓበሬታ->size==ንውሓት_ዋጋ&&!memcmp(ሓበሬታ->data,ናይ_ቃል_ጸወታ_ጽሑፍ,ንውሓት_ዋጋ);
}
static int 터미널요청(const struct assh_cbuffer_s *ሓበሬታ) {
    if(ሓበሬታ->size<24)return 0;
    const unsigned char *자료위치=ሓበሬታ->data;unsigned ንውሓት_ዋጋ=assh_load_u32(자료위치);
    if(ንውሓት_ዋጋ>128||ሓበሬታ->size<ንውሓት_ዋጋ+24)return 0;
    unsigned ኹነት_ዋጋ=assh_load_u32(자료위치+4+ንውሓት_ዋጋ+16);
    return ኹነት_ዋጋ<=2048&&ሓበሬታ->size==ንውሓት_ዋጋ+24+ኹነት_ዋጋ;
}
static void 요청처리(struct assh_event_request_s *ፍጻመ) {
    if(!인증됨||ፍጻመ->ch!=ጣብያ_ምእታው||!ጣብያ_ምእታው)return;
    if(같은말(&ፍጻመ->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&ፍጻመ->rq_data))ፍጻመ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&ፍጻመ->type,"window-change")) {
        if(셸시작됨&&ፍጻመ->rq_data.size==16)ፍጻመ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *ትእዛዝ=0;unsigned ንውሓት_ዋጋ=0;
    if(같은말(&ፍጻመ->type,"exec")) {
        if(ፍጻመ->rq_data.size<4)return;
        ንውሓት_ዋጋ=assh_load_u32(ፍጻመ->rq_data.data);
        if(!ንውሓት_ዋጋ||ንውሓት_ዋጋ>2048||ፍጻመ->rq_data.size!=ንውሓት_ዋጋ+4)return;
        ትእዛዝ=ፍጻመ->rq_data.data+4;
        for(unsigned 순번=0;순번<ንውሓት_ዋጋ;순번++)if(!ትእዛዝ[순번])return;
        ትእዛዝ_ዓይነት=1;
    }else if(!같은말(&ፍጻመ->type,"shell")||ፍጻመ->rq_data.size)return;
    if(sizeof(입력줄)-입력수<ንውሓት_ዋጋ+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(ንውሓት_ዋጋ)원격입력넣기(ትእዛዝ,ንውሓት_ዋጋ);원격입력넣기(&끝,1);
    셸시작됨=1;ፍጻመ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!ትእዛዝ_ዓይነት){const char *ኣንብበኒ_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*ኣንብበኒ_eb81d7d9)원격출력(*ኣንብበኒ_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(መዘና_ዋጋ<0){if(지금<재접속시각)return;መዘና_ዋጋ=망연결받기(듣는곳);if(መዘና_ዋጋ<0)return;
        접속시각=지금;assh_status_t ጌጋ=assh_session_create(ኣተኣታትዋ_ዋጋ,&ርክብ_e05f319b);
        if(ጌጋ){ርክብ_e05f319b=0;진단("SSH session error ",ጌጋ);ዕጸው_ርክብ();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){ዕጸው_ርክብ();return;}
    if(ጣብያ_ምእታው&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ጌጋ=assh_channel_data(ጣብያ_ምእታው,출력줄+출력앞,&수);
            if(!ጌጋ){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ጌጋ!=ASSH_NO_DATA){ዕጸው_ርክብ();return;}
        }
        if(ኣቑም_ደረጃ>=0&&!출력수){unsigned char ደረጃ_ዋጋ[4];assh_store_u32(ደረጃ_ዋጋ,(uint32_t)ኣቑም_ደረጃ);
            if(assh_request(ርክብ_e05f319b,ጣብያ_ምእታው,"exit-status",11,ደረጃ_ዋጋ,4,0)||assh_channel_eof(ጣብያ_ምእታው)||assh_channel_close(ጣብያ_ምእታው)) {ዕጸው_ርክብ();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s ፍጻመ;
        if(!assh_event_get(ርክብ_e05f319b,&ፍጻመ,지금/1000)){ዕጸው_ርክብ();return;}
        assh_status_t ጌጋ=ASSH_OK;int 쉬기=0,끊기=0;
        switch(ፍጻመ.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(መዘና_ዋጋ,ፍጻመ.transport.read.buf.data,ፍጻመ.transport.read.buf.size);
            if(수>0)ፍጻመ.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(መዘና_ዋጋ,ፍጻመ.transport.write.buf.data,ፍጻመ.transport.write.buf.size);
            if(수>0)ፍጻመ.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ፍጻመ.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ፍጻመ.userauth_server.methods.retries>3)ፍጻመ.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *ሓበሬታ=&ፍጻመ.userauth_server.password;
            if(같은말(&ሓበሬታ->username,"user")&&ሓበሬታ->password.size<=256&&!ሓበሬታ->new_password.size) {
                unsigned char 요약[32];원격요약(ሓበሬታ->password.data,ሓበሬታ->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)ሓበሬታ->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *ሓበሬታ=&ፍጻመ.connection.channel_open;
            if(인증됨&&!ጣብያ_ምእታው&&셸대기중&&같은말(&ሓበሬታ->type,"session")&&!ሓበሬታ->rq_data.size) {
                ሓበሬታ->reply=ASSH_CONNECTION_REPLY_SUCCESS;ሓበሬታ->pkt_size=4096;
                ሓበሬታ->win_size=-1;ጣብያ_ምእታው=ሓበሬታ->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&ፍጻመ.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *ሓበሬታ=&ፍጻመ.connection.channel_data;
            if(!셸시작됨||ሓበሬታ->ch!=ጣብያ_ምእታው||ሓበሬታ->ext){끊기=1;break;}
            unsigned 수=ሓበሬታ->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(ሓበሬታ->data.data[순번]==4){ኣቑም_ደረጃ=0;수=순번;ሓበሬታ->transferred=ሓበሬታ->data.size;break;}
            원격입력넣기(ሓበሬታ->data.data,수);if(!ሓበሬታ->transferred)ሓበሬታ->transferred=수;
            if(!수&&ኣቑም_ደረጃ<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: ጣብያ_ምእታው=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",ፍጻመ.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(ርክብ_e05f319b,&ፍጻመ,ጌጋ);
        if(끊기){ዕጸው_ርክብ();return;}if(쉬기)return;
    }
}
