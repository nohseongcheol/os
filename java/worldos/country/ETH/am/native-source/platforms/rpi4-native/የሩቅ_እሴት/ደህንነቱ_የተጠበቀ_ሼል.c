/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "የሩቅ_እሴት.h"
#include "암호기반.h"
#include "መገለጫ.h"
#include "../መረብ_ክምር/መረብ_ክምር.h"
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
static struct assh_context_s *አገባበ_ነገር_እሴት;
static struct assh_session_s *ግንኙነት_e05f319b;
static struct assh_channel_s *ሰርጥ_ምዝግብ;
static int 듣는곳=-1,አቻ_እሴት=-1,인증됨,셸시작됨,ትእዛዝ_ተይብ,ጨርስ_ዞን=-1,닫을예정,መጀመር_ስህተት,ሼል_መጠበቅ;
static uintptr_t ግንኙነት_ጊዜ,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *ቃል_ጽሁፍ,unsigned እሴት) {
    while(*ቃል_ጽሁፍ)보드글자쓰기(*ቃል_ጽሁፍ++);
    char 숫자[12];unsigned 수=0;do{숫자[수++]='0'+እሴት%10;እሴት/=10;}while(እሴት);
    while(수)보드글자쓰기(숫자[--수]);보드글자쓰기(10);
}
static assh_status_t አዘጋጅ_ማስቀመጫ(void *ውሂብ,void **አድራሻ,size_t መጠን,enum assh_alloc_type_e 종류) {
    (void)ውሂብ;(void)종류;
    if(!መጠን){ልቀቅ_የሩቅ(*አድራሻ);*አድራሻ=0;return ASSH_OK;}
    void *새주소=원격재할당(*አድራሻ,መጠን);
    if(!새주소)return ASSH_ERR_MEM;*አድራሻ=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *ውሂብ,const struct assh_buffer_s *ዘር_እሴት) {
    (void)ውሂብ;(void)ዘር_እሴት;unsigned char 시험[32];int ልኬት=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return ልኬት?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *ውሂብ,uint8_t *ልኬት,size_t ርዝመት_እሴት,uint_fast8_t 종류) {
    (void)ውሂብ;(void)종류;if(ርዝመት_እሴት>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(ልኬት,ርዝመት_እሴት)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *ውሂብ){(void)ውሂብ;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void ዝጋ_ግንኙነት(void) {
    인증됨=셸시작됨=0;ሰርጥ_ምዝግብ=0;
    if(ግንኙነት_e05f319b)assh_session_release(ግንኙነት_e05f319b);ግንኙነት_e05f319b=0;
    if(አቻ_እሴት>=0)ዝጋ_መረብ(አቻ_እሴት);አቻ_እሴት=-1;ትእዛዝ_ተይብ=0;ጨርስ_ዞን=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *ውሂብ,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=ውሂብ[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int ቁምፊ_እሴት=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return ቁምፊ_እሴት;
}
void 원격출력(unsigned char ቁምፊ_እሴት) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=ቁምፊ_እሴት==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=ቁምፊ_እሴት;이전출력=ቁምፊ_እሴት;
}
uintptr_t ቦርድ_ጨርስ_የሩቅ_ትእዛዝ(uintptr_t ዞን_እሴት){if(셸시작됨&&ትእዛዝ_ተይብ)ጨርስ_ዞን=(int)ዞን_እሴት;return 0;}
uintptr_t ቦርድ_የሩቅ_መጠበቅ(uintptr_t ዞን_እሴት){ሼል_መጠበቅ=ዞን_እሴት!=0;return 0;}
static int አዘጋጅ_ሼል(void) {
    if(듣는곳>=0)return 0;
    if(!አገባበ_ነገር_እሴት){
        assh_status_t ስህተት=assh_context_create(&አገባበ_ነገር_እሴት,ASSH_SERVER,አዘጋጅ_ማስቀመጫ,0,&난수기,0);
        if(ስህተት)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *ስልት_ሁነታ[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ስህተት=assh_algo_register(አገባበ_ነገር_እሴት,ASSH_SAFETY_WEAK,ስልት_ሁነታ);
        if(!ስህተት)ስህተት=assh_service_register_va(አገባበ_ነገር_እሴት,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=መሳሪያ_ቁልፍ;
        if(!ስህተት)ስህተት=assh_key_load(አገባበ_ነገር_እሴት,assh_context_keys(አገባበ_ነገር_እሴት),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(መሳሪያ_ቁልፍ));
        if(ስህተት){진단("SSH init error ",ስህተት);assh_context_release(አገባበ_ነገር_እሴት);አገባበ_ነገር_እሴት=0;return -5;}
    }
    int ወደብ_እሴት=통신끝점만들기(1);if(ወደብ_እሴት<0)return ወደብ_እሴት;통신주소재사용(ወደብ_እሴት);
    int ልኬት=망주소묶기(ወደብ_እሴት,0,22);if(!ልኬት)ልኬት=연결기다리기(ወደብ_እሴት);
    if(ልኬት<0){ዝጋ_መረብ(ወደብ_እሴት);return ልኬት;}듣는곳=ወደብ_እሴት;return 0;
}
uintptr_t ቦርድ_ማጥላት(uintptr_t 종류,uintptr_t ተግባር) {
    if(종류==1)return(uint32_t)ቁጥጥር_የሩቅ_ማሳያ(ተግባር);
    if(ተግባር==0){ዝጋ_ግንኙነት();if(듣는곳>=0)ዝጋ_መረብ(듣는곳);듣는곳=-1;return 0;}
    if(ተግባር==1){መጀመር_ስህተት=አዘጋጅ_ሼል();return(uint32_t)መጀመር_ስህተት;}
    return(uint32_t)(듣는곳>=0?1:መጀመር_ስህተት);
}
void አዘጋጅ_የሩቅ(void){መጀመር_ስህተት=አዘጋጅ_ሼል();ቁጥጥር_የሩቅ_ማሳያ(1);}
static int 같은말(const struct assh_cbuffer_s *ውሂብ,const char *ቃል_ጽሁፍ) {
    size_t ርዝመት_እሴት=strlen(ቃል_ጽሁፍ);return ውሂብ->size==ርዝመት_እሴት&&!memcmp(ውሂብ->data,ቃል_ጽሁፍ,ርዝመት_እሴት);
}
static int 터미널요청(const struct assh_cbuffer_s *ውሂብ) {
    if(ውሂብ->size<24)return 0;
    const unsigned char *ውሂብ_በቦታ_አስቀመጠ=ውሂብ->data;unsigned ርዝመት_እሴት=assh_load_u32(ውሂብ_በቦታ_አስቀመጠ);
    if(ርዝመት_እሴት>128||ውሂብ->size<ርዝመት_እሴት+24)return 0;
    unsigned ሁነታ_እሴት=assh_load_u32(ውሂብ_በቦታ_አስቀመጠ+4+ርዝመት_እሴት+16);
    return ሁነታ_እሴት<=2048&&ውሂብ->size==ርዝመት_እሴት+24+ሁነታ_እሴት;
}
static void 요청처리(struct assh_event_request_s *ፍጻሜ) {
    if(!인증됨||ፍጻሜ->ch!=ሰርጥ_ምዝግብ||!ሰርጥ_ምዝግብ)return;
    if(같은말(&ፍጻሜ->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&ፍጻሜ->rq_data))ፍጻሜ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&ፍጻሜ->type,"window-change")) {
        if(셸시작됨&&ፍጻሜ->rq_data.size==16)ፍጻሜ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!ሼል_መጠበቅ)return;
    const unsigned char *ትእዛዝ=0;unsigned ርዝመት_እሴት=0;
    if(같은말(&ፍጻሜ->type,"exec")) {
        if(ፍጻሜ->rq_data.size<4)return;
        ርዝመት_እሴት=assh_load_u32(ፍጻሜ->rq_data.data);
        if(!ርዝመት_እሴት||ርዝመት_እሴት>2048||ፍጻሜ->rq_data.size!=ርዝመት_እሴት+4)return;
        ትእዛዝ=ፍጻሜ->rq_data.data+4;
        for(unsigned 순번=0;순번<ርዝመት_እሴት;순번++)if(!ትእዛዝ[순번])return;
        ትእዛዝ_ተይብ=1;
    }else if(!같은말(&ፍጻሜ->type,"shell")||ፍጻሜ->rq_data.size)return;
    if(sizeof(입력줄)-입력수<ርዝመት_እሴት+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(ርዝመት_እሴት)원격입력넣기(ትእዛዝ,ርዝመት_እሴት);원격입력넣기(&끝,1);
    셸시작됨=1;ፍጻሜ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!ትእዛዝ_ተይብ){const char *አንበኝ_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*አንበኝ_eb81d7d9)원격출력(*አንበኝ_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t አሁን_እሴት=보드밀리초();
    if(አቻ_እሴት<0){if(አሁን_እሴት<재접속시각)return;አቻ_እሴት=망연결받기(듣는곳);if(አቻ_እሴት<0)return;
        ግንኙነት_ጊዜ=አሁን_እሴት;assh_status_t ስህተት=assh_session_create(አገባበ_ነገር_እሴት,&ግንኙነት_e05f319b);
        if(ስህተት){ግንኙነት_e05f319b=0;진단("SSH session error ",ስህተት);ዝጋ_ግንኙነት();return;}}
    if((!인증됨&&አሁን_እሴት-ግንኙነት_ጊዜ>30000)||닫을예정==2||(닫을예정&&አሁን_እሴት>=닫는시각)){ዝጋ_ግንኙነት();return;}
    if(ሰርጥ_ምዝግብ&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ስህተት=assh_channel_data(ሰርጥ_ምዝግብ,출력줄+출력앞,&수);
            if(!ስህተት){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ስህተት!=ASSH_NO_DATA){ዝጋ_ግንኙነት();return;}
        }
        if(ጨርስ_ዞን>=0&&!출력수){unsigned char ዞን_እሴት[4];assh_store_u32(ዞን_እሴት,(uint32_t)ጨርስ_ዞን);
            if(assh_request(ግንኙነት_e05f319b,ሰርጥ_ምዝግብ,"exit-status",11,ዞን_እሴት,4,0)||assh_channel_eof(ሰርጥ_ምዝግብ)||assh_channel_close(ሰርጥ_ምዝግብ)) {ዝጋ_ግንኙነት();return;}
            닫을예정=1;닫는시각=አሁን_እሴት+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s ፍጻሜ;
        if(!assh_event_get(ግንኙነት_e05f319b,&ፍጻሜ,አሁን_እሴት/1000)){ዝጋ_ግንኙነት();return;}
        assh_status_t ስህተት=ASSH_OK;int 쉬기=0,끊기=0;
        switch(ፍጻሜ.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(አቻ_እሴት,ፍጻሜ.transport.read.buf.data,ፍጻሜ.transport.read.buf.size);
            if(수>0)ፍጻሜ.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(አቻ_እሴት,ፍጻሜ.transport.write.buf.data,ፍጻሜ.transport.write.buf.size);
            if(수>0)ፍጻሜ.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ፍጻሜ.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ፍጻሜ.userauth_server.methods.retries>3)ፍጻሜ.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *ውሂብ=&ፍጻሜ.userauth_server.password;
            if(같은말(&ውሂብ->username,"user")&&ውሂብ->password.size<=256&&!ውሂብ->new_password.size) {
                unsigned char ማጠቃለያ_እሴት[32];የሩቅ_ማጠቃለያ(ውሂብ->password.data,ውሂብ->password.size,ማጠቃለያ_እሴት);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=ማጠቃለያ_እሴት[순번]^ሼል_የይለፍ_ቃል_ማጠቃለያ[순번];memset(ማጠቃለያ_እሴት,0,32);
                if(!차이)ውሂብ->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *ውሂብ=&ፍጻሜ.connection.channel_open;
            if(인증됨&&!ሰርጥ_ምዝግብ&&ሼል_መጠበቅ&&같은말(&ውሂብ->type,"session")&&!ውሂብ->rq_data.size) {
                ውሂብ->reply=ASSH_CONNECTION_REPLY_SUCCESS;ውሂብ->pkt_size=4096;
                ውሂብ->win_size=-1;ሰርጥ_ምዝግብ=ውሂብ->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&ፍጻሜ.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *ውሂብ=&ፍጻሜ.connection.channel_data;
            if(!셸시작됨||ውሂብ->ch!=ሰርጥ_ምዝግብ||ውሂብ->ext){끊기=1;break;}
            unsigned 수=ውሂብ->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(ውሂብ->data.data[순번]==4){ጨርስ_ዞን=0;수=순번;ውሂብ->transferred=ውሂብ->data.size;break;}
            원격입력넣기(ውሂብ->data.data,수);if(!ውሂብ->transferred)ውሂብ->transferred=수;
            if(!수&&ጨርስ_ዞን<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: ሰርጥ_ምዝግብ=0;셸시작됨=0;닫을예정=1;닫는시각=አሁን_እሴት+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",ፍጻሜ.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(ግንኙነት_e05f319b,&ፍጻሜ,ስህተት);
        if(끊기){ዝጋ_ግንኙነት();return;}if(쉬기)return;
    }
}
