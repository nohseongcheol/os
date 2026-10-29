/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "தொலைநிலை_மதிப்பு.h"
#include "மறையீட்டியல்_ஆதரவு.h"
#include "குறிப்பு.h"
#include "../பிணையம்_அடுக்கு_49fba3da/பிணையம்_அடுக்கு_49fba3da.h"
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
static struct assh_context_s *சூழல்_மதிப்பு;
static struct assh_session_s *இணைப்பு_e05f319b;
static struct assh_channel_s *சேனல்_உள்ளீடு;
static int லிஸனிங்_முடிவுப்_புள்ளி=-1,பியர்_மதிப்பு=-1,인증됨,셸시작됨,கட்டளை_வகை,முடி_நிலை_2bce2943=-1,닫을예정,இயக்கம்_பிழை,셸대기중;
static uintptr_t இணைப்பு_நேரம்,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *சொல்_உரை,unsigned மதிப்பு) {
    while(*சொல்_உரை)보드글자쓰기(*சொல்_உரை++);
    char இலக்கம்_மதிப்பு[12];unsigned 수=0;do{இலக்கம்_மதிப்பு[수++]='0'+மதிப்பு%10;மதிப்பு/=10;}while(மதிப்பு);
    while(수)보드글자쓰기(இலக்கம்_மதிப்பு[--수]);보드글자쓰기(10);
}
static assh_status_t தயார்படுத்த_நினைவகம்(void *தரவு,void **முகவரி,size_t அளவு,enum assh_alloc_type_e 종류) {
    (void)தரவு;(void)종류;
    if(!அளவு){அனுப்பு_தொலைநிலை(*முகவரி);*முகவரி=0;return ASSH_OK;}
    void *새주소=원격재할당(*முகவரி,அளவு);
    if(!새주소)return ASSH_ERR_MEM;*முகவரி=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *தரவு,const struct assh_buffer_s *சீட்_மதிப்பு) {
    (void)தரவு;(void)சீட்_மதிப்பு;unsigned char 시험[32];int அளவிடக்கூடியது=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return அளவிடக்கூடியது?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *தரவு,uint8_t *அளவிடக்கூடியது,size_t நீளம்_மதிப்பு,uint_fast8_t 종류) {
    (void)தரவு;(void)종류;if(நீளம்_மதிப்பு>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(அளவிடக்கூடியது,நீளம்_மதிப்பு)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *தரவு){(void)தரவு;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void மூடு_இணைப்பு(void) {
    인증됨=셸시작됨=0;சேனல்_உள்ளீடு=0;
    if(இணைப்பு_e05f319b)assh_session_release(இணைப்பு_e05f319b);இணைப்பு_e05f319b=0;
    if(பியர்_மதிப்பு>=0)மூடு_பிணையம்(பியர்_மதிப்பு);பியர்_மதிப்பு=-1;கட்டளை_வகை=0;முடி_நிலை_2bce2943=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *தரவு,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=தரவு[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int எழுத்துக்குறி_மதிப்பு=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return எழுத்துக்குறி_மதிப்பு;
}
void 원격출력(unsigned char எழுத்துக்குறி_மதிப்பு) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=எழுத்துக்குறி_மதிப்பு==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=எழுத்துக்குறி_மதிப்பு;이전출력=எழுத்துக்குறி_மதிப்பு;
}
uintptr_t போர்டு_முடி_தொலைநிலை_கட்டளை(uintptr_t நிலை_மதிப்பு_e10195a1){if(셸시작됨&&கட்டளை_வகை)முடி_நிலை_2bce2943=(int)நிலை_மதிப்பு_e10195a1;return 0;}
uintptr_t போர்டு_தொலைநிலை_காத்திரு(uintptr_t நிலை_மதிப்பு_e10195a1){셸대기중=நிலை_மதிப்பு_e10195a1!=0;return 0;}
static int தயார்படுத்த_கூடு(void) {
    if(லிஸனிங்_முடிவுப்_புள்ளி>=0)return 0;
    if(!சூழல்_மதிப்பு){
        assh_status_t பிழை=assh_context_create(&சூழல்_மதிப்பு,ASSH_SERVER,தயார்படுத்த_நினைவகம்,0,&난수기,0);
        if(பிழை)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *முறை_பயன்முறை[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        பிழை=assh_algo_register(சூழல்_மதிப்பு,ASSH_SAFETY_WEAK,முறை_பயன்முறை);
        if(!பிழை)பிழை=assh_service_register_va(சூழல்_மதிப்பு,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=சாதனம்_சாவி;
        if(!பிழை)பிழை=assh_key_load(சூழல்_மதிப்பு,assh_context_keys(சூழல்_மதிப்பு),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(சாதனம்_சாவி));
        if(பிழை){진단("SSH init error ",பிழை);assh_context_release(சூழல்_மதிப்பு);சூழல்_மதிப்பு=0;return -5;}
    }
    int முணையம்_மதிப்பு=통신끝점만들기(1);if(முணையம்_மதிப்பு<0)return முணையம்_மதிப்பு;통신주소재사용(முணையம்_மதிப்பு);
    int அளவிடக்கூடியது=망주소묶기(முணையம்_மதிப்பு,0,22);if(!அளவிடக்கூடியது)அளவிடக்கூடியது=연결기다리기(முணையம்_மதிப்பு);
    if(அளவிடக்கூடியது<0){மூடு_பிணையம்(முணையம்_மதிப்பு);return அளவிடக்கூடியது;}லிஸனிங்_முடிவுப்_புள்ளி=முணையம்_மதிப்பு;return 0;
}
uintptr_t போர்டு_நிழலிடல்(uintptr_t 종류,uintptr_t செயல்) {
    if(종류==1)return(uint32_t)கட்டுப்பாடு_தொலைநிலை_காட்சி(செயல்);
    if(செயல்==0){மூடு_இணைப்பு();if(லிஸனிங்_முடிவுப்_புள்ளி>=0)மூடு_பிணையம்(லிஸனிங்_முடிவுப்_புள்ளி);லிஸனிங்_முடிவுப்_புள்ளி=-1;return 0;}
    if(செயல்==1){இயக்கம்_பிழை=தயார்படுத்த_கூடு();return(uint32_t)இயக்கம்_பிழை;}
    return(uint32_t)(லிஸனிங்_முடிவுப்_புள்ளி>=0?1:இயக்கம்_பிழை);
}
void தயார்படுத்த_தொலைநிலை(void){இயக்கம்_பிழை=தயார்படுத்த_கூடு();கட்டுப்பாடு_தொலைநிலை_காட்சி(1);}
static int 같은말(const struct assh_cbuffer_s *தரவு,const char *சொல்_உரை) {
    size_t நீளம்_மதிப்பு=strlen(சொல்_உரை);return தரவு->size==நீளம்_மதிப்பு&&!memcmp(தரவு->data,சொல்_உரை,நீளம்_மதிப்பு);
}
static int முனையம்_HTTP_வேண்டுதல்(const struct assh_cbuffer_s *தரவு) {
    if(தரவு->size<24)return 0;
    const unsigned char *தரவு_நிலை=தரவு->data;unsigned நீளம்_மதிப்பு=assh_load_u32(தரவு_நிலை);
    if(நீளம்_மதிப்பு>128||தரவு->size<நீளம்_மதிப்பு+24)return 0;
    unsigned பயன்முறை_மதிப்பு=assh_load_u32(தரவு_நிலை+4+நீளம்_மதிப்பு+16);
    return பயன்முறை_மதிப்பு<=2048&&தரவு->size==நீளம்_மதிப்பு+24+பயன்முறை_மதிப்பு;
}
static void நடத்தி_HTTP_வேண்டுதல்(struct assh_event_request_s *நிகழ்வு) {
    if(!인증됨||நிகழ்வு->ch!=சேனல்_உள்ளீடு||!சேனல்_உள்ளீடு)return;
    if(같은말(&நிகழ்வு->type,"pty-req")) {
        if(!셸시작됨&&முனையம்_HTTP_வேண்டுதல்(&நிகழ்வு->rq_data))நிகழ்வு->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&நிகழ்வு->type,"window-change")) {
        if(셸시작됨&&நிகழ்வு->rq_data.size==16)நிகழ்வு->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *கட்டளை=0;unsigned நீளம்_மதிப்பு=0;
    if(같은말(&நிகழ்வு->type,"exec")) {
        if(நிகழ்வு->rq_data.size<4)return;
        நீளம்_மதிப்பு=assh_load_u32(நிகழ்வு->rq_data.data);
        if(!நீளம்_மதிப்பு||நீளம்_மதிப்பு>2048||நிகழ்வு->rq_data.size!=நீளம்_மதிப்பு+4)return;
        கட்டளை=நிகழ்வு->rq_data.data+4;
        for(unsigned 순번=0;순번<நீளம்_மதிப்பு;순번++)if(!கட்டளை[순번])return;
        கட்டளை_வகை=1;
    }else if(!같은말(&நிகழ்வு->type,"shell")||நிகழ்வு->rq_data.size)return;
    if(sizeof(입력줄)-입력수<நீளம்_மதிப்பு+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(நீளம்_மதிப்பு)원격입력넣기(கட்டளை,நீளம்_மதிப்பு);원격입력넣기(&끝,1);
    셸시작됨=1;நிகழ்வு->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!கட்டளை_வகை){const char *பயனர்_உதவிக்_கோப்பு_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*பயனர்_உதவிக்_கோப்பு_eb81d7d9)원격출력(*பயனர்_உதவிக்_கோப்பு_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(லிஸனிங்_முடிவுப்_புள்ளி<0)return;
    uintptr_t தொடர்புடையவை_மதிப்பு=보드밀리초();
    if(பியர்_மதிப்பு<0){if(தொடர்புடையவை_மதிப்பு<재접속시각)return;பியர்_மதிப்பு=망연결받기(லிஸனிங்_முடிவுப்_புள்ளி);if(பியர்_மதிப்பு<0)return;
        இணைப்பு_நேரம்=தொடர்புடையவை_மதிப்பு;assh_status_t பிழை=assh_session_create(சூழல்_மதிப்பு,&இணைப்பு_e05f319b);
        if(பிழை){இணைப்பு_e05f319b=0;진단("SSH session error ",பிழை);மூடு_இணைப்பு();return;}}
    if((!인증됨&&தொடர்புடையவை_மதிப்பு-இணைப்பு_நேரம்>30000)||닫을예정==2||(닫을예정&&தொடர்புடையவை_மதிப்பு>=닫는시각)){மூடு_இணைப்பு();return;}
    if(சேனல்_உள்ளீடு&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t பிழை=assh_channel_data(சேனல்_உள்ளீடு,출력줄+출력앞,&수);
            if(!பிழை){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(பிழை!=ASSH_NO_DATA){மூடு_இணைப்பு();return;}
        }
        if(முடி_நிலை_2bce2943>=0&&!출력수){unsigned char நிலை_மதிப்பு_e10195a1[4];assh_store_u32(நிலை_மதிப்பு_e10195a1,(uint32_t)முடி_நிலை_2bce2943);
            if(assh_request(இணைப்பு_e05f319b,சேனல்_உள்ளீடு,"exit-status",11,நிலை_மதிப்பு_e10195a1,4,0)||assh_channel_eof(சேனல்_உள்ளீடு)||assh_channel_close(சேனல்_உள்ளீடு)) {மூடு_இணைப்பு();return;}
            닫을예정=1;닫는시각=தொடர்புடையவை_மதிப்பு+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s நிகழ்வு;
        if(!assh_event_get(இணைப்பு_e05f319b,&நிகழ்வு,தொடர்புடையவை_மதிப்பு/1000)){மூடு_இணைப்பு();return;}
        assh_status_t பிழை=ASSH_OK;int 쉬기=0,துண்டிப்பு_முடிவுப்_புள்ளி=0;
        switch(நிகழ்வு.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(பியர்_மதிப்பு,நிகழ்வு.transport.read.buf.data,நிகழ்வு.transport.read.buf.size);
            if(수>0)நிகழ்வு.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else துண்டிப்பு_முடிவுப்_புள்ளி=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(பியர்_மதிப்பு,நிகழ்வு.transport.write.buf.data,நிகழ்வு.transport.write.buf.size);
            if(수>0)நிகழ்வு.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else துண்டிப்பு_முடிவுப்_புள்ளி=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            நிகழ்வு.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(நிகழ்வு.userauth_server.methods.retries>3)நிகழ்வு.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *தரவு=&நிகழ்வு.userauth_server.password;
            if(같은말(&தரவு->username,"user")&&தரவு->password.size<=256&&!தரவு->new_password.size) {
                unsigned char 요약[32];원격요약(தரவு->password.data,தரவு->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)தரவு->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *தரவு=&நிகழ்வு.connection.channel_open;
            if(인증됨&&!சேனல்_உள்ளீடு&&셸대기중&&같은말(&தரவு->type,"session")&&!தரவு->rq_data.size) {
                தரவு->reply=ASSH_CONNECTION_REPLY_SUCCESS;தரவு->pkt_size=4096;
                தரவு->win_size=-1;சேனல்_உள்ளீடு=தரவு->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: நடத்தி_HTTP_வேண்டுதல்(&நிகழ்வு.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *தரவு=&நிகழ்வு.connection.channel_data;
            if(!셸시작됨||தரவு->ch!=சேனல்_உள்ளீடு||தரவு->ext){துண்டிப்பு_முடிவுப்_புள்ளி=1;break;}
            unsigned 수=தரவு->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(தரவு->data.data[순번]==4){முடி_நிலை_2bce2943=0;수=순번;தரவு->transferred=தரவு->data.size;break;}
            원격입력넣기(தரவு->data.data,수);if(!தரவு->transferred)தரவு->transferred=수;
            if(!수&&முடி_நிலை_2bce2943<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: சேனல்_உள்ளீடு=0;셸시작됨=0;닫을예정=1;닫는시각=தொடர்புடையவை_மதிப்பு+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",நிகழ்வு.session.error.code);துண்டிப்பு_முடிவுப்_புள்ளி=1;break;
        case ASSH_EVENT_DISCONNECT: துண்டிப்பு_முடிவுப்_புள்ளி=1;break;
        default: break;
        }
        assh_event_done(இணைப்பு_e05f319b,&நிகழ்வு,பிழை);
        if(துண்டிப்பு_முடிவுப்_புள்ளி){மூடு_இணைப்பு();return;}if(쉬기)return;
    }
}
