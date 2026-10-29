/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "מרוחק_ערך.h"
#include "קריפטוגרפיה_תמך.h"
#include "פרופיל.h"
#include "../רשת_רמז/רשת_רמז.h"
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
static struct assh_context_s *הקשר_ערך;
static struct assh_session_s *קשר_e05f319b;
static struct assh_channel_s *ערוץ_ערך_a3973059;
static int מאזין_משתתף=-1,עמית_ערך=-1,인증됨,셸시작됨,פקודה_כתב,סיים_שיחה_מצב=-1,닫을예정,시작오류,מעטפת_ממתין;
static uintptr_t קשר_זמן,재접속시각,닫는시각;
static unsigned char קלט_קו[8192],פלט_קו[65536];
static unsigned קלט_ראש,입력수,פלט_ראש,출력수,이전출력;
static void 진단(const char *מילים_טקסט,unsigned ערך) {
    while(*מילים_טקסט)보드글자쓰기(*מילים_טקסט++);
    char ספרה_ערך[12];unsigned 수=0;do{ספרה_ערך[수++]='0'+ערך%10;ערך/=10;}while(ערך);
    while(수)보드글자쓰기(ספרה_ערך[--수]);보드글자쓰기(10);
}
static assh_status_t להכין_זיכרון(void *נתונים,void **למען,size_t גודל,enum assh_alloc_type_e 종류) {
    (void)נתונים;(void)종류;
    if(!גודל){לשחרר_מרוחק(*למען);*למען=0;return ASSH_OK;}
    void *새주소=원격재할당(*למען,גודל);
    if(!새주소)return ASSH_ERR_MEM;*למען=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *נתונים,const struct assh_buffer_s *ערך_זרע) {
    (void)נתונים;(void)ערך_זרע;unsigned char 시험[32];int תוצאה=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return תוצאה?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *נתונים,uint8_t *תוצאה,size_t 길이,uint_fast8_t 종류) {
    (void)נתונים;(void)종류;if(길이>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(תוצאה,길이)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *נתונים){(void)נתונים;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void סגור_קשר(void) {
    인증됨=셸시작됨=0;ערוץ_ערך_a3973059=0;
    if(קשר_e05f319b)assh_session_release(קשר_e05f319b);קשר_e05f319b=0;
    if(עמית_ערך>=0)סגור_רשת(עמית_ערך);עמית_ערך=-1;פקודה_כתב=0;סיים_שיחה_מצב=-1;닫을예정=0;
    קלט_ראש=입력수=פלט_ראש=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int הזנה_מרוחק_קלט(const unsigned char *נתונים,unsigned 수) {
    if(수>sizeof(קלט_קו)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)קלט_קו[(קלט_ראש+입력수++)%sizeof(קלט_קו)]=נתונים[순번];return 수;
}
int מרוחק_קלט(void) {
    if(!입력수)return -1;int תו_ערך=קלט_קו[קלט_ראש];קלט_ראש=(קלט_ראש+1)%sizeof(קלט_קו);입력수--;return תו_ערך;
}
void מרוחק_פלט(unsigned char תו_ערך) {
    if(!셸시작됨||닫을예정)return;
    unsigned צירוף_מצב=תו_ערך==10&&이전출력!=13;
    if(출력수+1+צירוף_מצב>sizeof(פלט_קו)){닫을예정=2;return;}
    if(צירוף_מצב)פלט_קו[(פלט_ראש+출력수++)%sizeof(פלט_קו)]=13;
    פלט_קו[(פלט_ראש+출력수++)%sizeof(פלט_קו)]=תו_ערך;이전출력=תו_ערך;
}
uintptr_t לוח_סיים_שיחה_מרוחק_פקודה(uintptr_t מצב_ערך){if(셸시작됨&&פקודה_כתב)סיים_שיחה_מצב=(int)מצב_ערך;return 0;}
uintptr_t לוח_מרוחק_רק_רגע(uintptr_t מצב_ערך){מעטפת_ממתין=מצב_ערך!=0;return 0;}
static int להכין_מעטפת(void) {
    if(מאזין_משתתף>=0)return 0;
    if(!הקשר_ערך){
        assh_status_t שגיאה=assh_context_create(&הקשר_ערך,ASSH_SERVER,להכין_זיכרון,0,&난수기,0);
        if(שגיאה)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *פעולת_שירות_מצב[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        שגיאה=assh_algo_register(הקשר_ערך,ASSH_SAFETY_WEAK,פעולת_שירות_מצב);
        if(!שגיאה)שגיאה=assh_service_register_va(הקשר_ערך,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=התקן_מקש;
        if(!שגיאה)שגיאה=assh_key_load(הקשר_ערך,assh_context_keys(הקשר_ערך),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(התקן_מקש));
        if(שגיאה){진단("SSH init error ",שגיאה);assh_context_release(הקשר_ערך);הקשר_ערך=0;return -5;}
    }
    int הסב_ערך=통신끝점만들기(1);if(הסב_ערך<0)return הסב_ערך;통신주소재사용(הסב_ערך);
    int תוצאה=נטו_לאגד(הסב_ערך,0,22);if(!תוצאה)תוצאה=נטו_להאזין(הסב_ערך);
    if(תוצאה<0){סגור_רשת(הסב_ערך);return תוצאה;}מאזין_משתתף=הסב_ערך;return 0;
}
uintptr_t לוח_הוספת_צל(uintptr_t 종류,uintptr_t פעולה) {
    if(종류==1)return(uint32_t)פקד_מרוחק_צג(פעולה);
    if(פעולה==0){סגור_קשר();if(מאזין_משתתף>=0)סגור_רשת(מאזין_משתתף);מאזין_משתתף=-1;return 0;}
    if(פעולה==1){시작오류=להכין_מעטפת();return(uint32_t)시작오류;}
    return(uint32_t)(מאזין_משתתף>=0?1:시작오류);
}
void להכין_מרוחק(void){시작오류=להכין_מעטפת();פקד_מרוחק_צג(1);}
static int 같은말(const struct assh_cbuffer_s *נתונים,const char *מילים_טקסט) {
    size_t 길이=strlen(מילים_טקסט);return נתונים->size==길이&&!memcmp(נתונים->data,מילים_טקסט,길이);
}
static int מסוף_בקשה(const struct assh_cbuffer_s *נתונים) {
    if(נתונים->size<24)return 0;
    const unsigned char *נתונים_עמדה=נתונים->data;unsigned 길이=assh_load_u32(נתונים_עמדה);
    if(길이>128||נתונים->size<길이+24)return 0;
    unsigned מצב_ערך_a83655ea=assh_load_u32(נתונים_עמדה+4+길이+16);
    return מצב_ערך_a83655ea<=2048&&נתונים->size==길이+24+מצב_ערך_a83655ea;
}
static void נקודת_אחיזה_בקשה(struct assh_event_request_s *אירוע) {
    if(!인증됨||אירוע->ch!=ערוץ_ערך_a3973059||!ערוץ_ערך_a3973059)return;
    if(같은말(&אירוע->type,"pty-req")) {
        if(!셸시작됨&&מסוף_בקשה(&אירוע->rq_data))אירוע->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&אירוע->type,"window-change")) {
        if(셸시작됨&&אירוע->rq_data.size==16)אירוע->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!מעטפת_ממתין)return;
    const unsigned char *פקודה=0;unsigned 길이=0;
    if(같은말(&אירוע->type,"exec")) {
        if(אירוע->rq_data.size<4)return;
        길이=assh_load_u32(אירוע->rq_data.data);
        if(!길이||길이>2048||אירוע->rq_data.size!=길이+4)return;
        פקודה=אירוע->rq_data.data+4;
        for(unsigned 순번=0;순번<길이;순번++)if(!פקודה[순번])return;
        פקודה_כתב=1;
    }else if(!같은말(&אירוע->type,"shell")||אירוע->rq_data.size)return;
    if(sizeof(קלט_קו)-입력수<길이+2)return;
    const unsigned char 지움=21,끝=13;
    הזנה_מרוחק_קלט(&지움,1);if(길이)הזנה_מרוחק_קלט(פקודה,길이);הזנה_מרוחק_קלט(&끝,1);
    셸시작됨=1;אירוע->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!פקודה_כתב){const char *안내="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*안내)מרוחק_פלט(*안내++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(מאזין_משתתף<0)return;
    uintptr_t עכשיו_ערך=보드밀리초();
    if(עמית_ערך<0){if(עכשיו_ערך<재접속시각)return;עמית_ערך=נטו_לקבל(מאזין_משתתף);if(עמית_ערך<0)return;
        קשר_זמן=עכשיו_ערך;assh_status_t שגיאה=assh_session_create(הקשר_ערך,&קשר_e05f319b);
        if(שגיאה){קשר_e05f319b=0;진단("SSH session error ",שגיאה);סגור_קשר();return;}}
    if((!인증됨&&עכשיו_ערך-קשר_זמן>30000)||닫을예정==2||(닫을예정&&עכשיו_ערך>=닫는시각)){סגור_קשר();return;}
    if(ערוץ_ערך_a3973059&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(פלט_קו)-פלט_ראש;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t שגיאה=assh_channel_data(ערוץ_ערך_a3973059,פלט_קו+פלט_ראש,&수);
            if(!שגיאה){פלט_ראש=(פלט_ראש+수)%sizeof(פלט_קו);출력수-=수;}
            else if(שגיאה!=ASSH_NO_DATA){סגור_קשר();return;}
        }
        if(סיים_שיחה_מצב>=0&&!출력수){unsigned char מצב_ערך[4];assh_store_u32(מצב_ערך,(uint32_t)סיים_שיחה_מצב);
            if(assh_request(קשר_e05f319b,ערוץ_ערך_a3973059,"exit-status",11,מצב_ערך,4,0)||assh_channel_eof(ערוץ_ערך_a3973059)||assh_channel_close(ערוץ_ערך_a3973059)) {סגור_קשר();return;}
            닫을예정=1;닫는시각=עכשיו_ערך+3000;
        }
    }
    for(unsigned רצף_ערך=0;רצף_ערך<16;רצף_ערך++) {
        struct assh_event_s אירוע;
        if(!assh_event_get(קשר_e05f319b,&אירוע,עכשיו_ערך/1000)){סגור_קשר();return;}
        assh_status_t שגיאה=ASSH_OK;int 쉬기=0,נתק_משתתף=0;
        switch(אירוע.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(עמית_ערך,אירוע.transport.read.buf.data,אירוע.transport.read.buf.size);
            if(수>0)אירוע.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else נתק_משתתף=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=נטו_כתיבה(עמית_ערך,אירוע.transport.write.buf.data,אירוע.transport.write.buf.size);
            if(수>0)אירוע.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else נתק_משתתף=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            אירוע.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(אירוע.userauth_server.methods.retries>3)אירוע.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *נתונים=&אירוע.userauth_server.password;
            if(같은말(&נתונים->username,"user")&&נתונים->password.size<=256&&!נתונים->new_password.size) {
                unsigned char סיכום_ערך[32];מרוחק_סיכום(נתונים->password.data,נתונים->password.size,סיכום_ערך);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=סיכום_ערך[순번]^מעטפת_סיסמה_סיכום[순번];memset(סיכום_ערך,0,32);
                if(!차이)נתונים->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *נתונים=&אירוע.connection.channel_open;
            if(인증됨&&!ערוץ_ערך_a3973059&&מעטפת_ממתין&&같은말(&נתונים->type,"session")&&!נתונים->rq_data.size) {
                נתונים->reply=ASSH_CONNECTION_REPLY_SUCCESS;נתונים->pkt_size=4096;
                נתונים->win_size=-1;ערוץ_ערך_a3973059=נתונים->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: נקודת_אחיזה_בקשה(&אירוע.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *נתונים=&אירוע.connection.channel_data;
            if(!셸시작됨||נתונים->ch!=ערוץ_ערך_a3973059||נתונים->ext){נתק_משתתף=1;break;}
            unsigned 수=נתונים->data.size;if(수>sizeof(קלט_קו)-입력수)수=sizeof(קלט_קו)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(נתונים->data.data[순번]==4){סיים_שיחה_מצב=0;수=순번;נתונים->transferred=נתונים->data.size;break;}
            הזנה_מרוחק_קלט(נתונים->data.data,수);if(!נתונים->transferred)נתונים->transferred=수;
            if(!수&&סיים_שיחה_מצב<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: ערוץ_ערך_a3973059=0;셸시작됨=0;닫을예정=1;닫는시각=עכשיו_ערך+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",אירוע.session.error.code);נתק_משתתף=1;break;
        case ASSH_EVENT_DISCONNECT: נתק_משתתף=1;break;
        default: break;
        }
        assh_event_done(קשר_e05f319b,&אירוע,שגיאה);
        if(נתק_משתתף){סגור_קשר();return;}if(쉬기)return;
    }
}
