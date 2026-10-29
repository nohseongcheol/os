/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "يىراق_قىممىتى.h"
#include "암호기반.h"
#include "ئارخىپ_1c9b560a.h"
#include "../تور_دۆۋە/تور_دۆۋە.h"
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
static struct assh_context_s *كونتېكست_قىممىتى;
static struct assh_session_s *ئۇلىنىش_e05f319b;
static struct assh_channel_s *قانال_كىرگۈزۈش;
static int 듣는곳=-1,باراۋەرلىك_قىممىتى=-1,인증됨,셸시작됨,بۇيرۇق_تىپ,تاماملىماق_ھالەت=-1,닫을예정,قوزغىتىش_خاتالىق,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *سۆز_تېكست,unsigned قىممىتى) {
    while(*سۆز_تېكست)보드글자쓰기(*سۆز_تېكست++);
    char خانا_قىممىتى[12];unsigned 수=0;do{خانا_قىممىتى[수++]='0'+قىممىتى%10;قىممىتى/=10;}while(قىممىتى);
    while(수)보드글자쓰기(خانا_قىممىتى[--수]);보드글자쓰기(10);
}
static assh_status_t تەييارلىماق_ساقلىغۇچ(void *مەلۇمات,void **ئادرېس,size_t چوڭلۇقى,enum assh_alloc_type_e 종류) {
    (void)مەلۇمات;(void)종류;
    if(!چوڭلۇقى){تارقىتىش_يىراق(*ئادرېس);*ئادرېس=0;return ASSH_OK;}
    void *새주소=원격재할당(*ئادرېس,چوڭلۇقى);
    if(!새주소)return ASSH_ERR_MEM;*ئادرېس=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *مەلۇمات,const struct assh_buffer_s *ئۇرۇق_قىممىتى) {
    (void)مەلۇمات;(void)ئۇرۇق_قىممىتى;unsigned char 시험[32];int ئۆلچەم=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return ئۆلچەم?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *مەلۇمات,uint8_t *ئۆلچەم,size_t ئۇزۇنلۇق_قىممىتى,uint_fast8_t 종류) {
    (void)مەلۇمات;(void)종류;if(ئۇزۇنلۇق_قىممىتى>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(ئۆلچەم,ئۇزۇنلۇق_قىممىتى)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *مەلۇمات){(void)مەلۇمات;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void ئاياغ_ئۇلىنىش(void) {
    인증됨=셸시작됨=0;قانال_كىرگۈزۈش=0;
    if(ئۇلىنىش_e05f319b)assh_session_release(ئۇلىنىش_e05f319b);ئۇلىنىش_e05f319b=0;
    if(باراۋەرلىك_قىممىتى>=0)ئاياغ_تور(باراۋەرلىك_قىممىتى);باراۋەرلىك_قىممىتى=-1;بۇيرۇق_تىپ=0;تاماملىماق_ھالەت=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *مەلۇمات,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=مەلۇمات[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int ھەرپ_بەلگە_قىممىتى=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return ھەرپ_بەلگە_قىممىتى;
}
void 원격출력(unsigned char ھەرپ_بەلگە_قىممىتى) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=ھەرپ_بەلگە_قىممىتى==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=ھەرپ_بەلگە_قىممىتى;이전출력=ھەرپ_بەلگە_قىممىتى;
}
uintptr_t سۇپا_تاماملىماق_يىراق_بۇيرۇق(uintptr_t ھالەت_قىممىتى){if(셸시작됨&&بۇيرۇق_تىپ)تاماملىماق_ھالەت=(int)ھالەت_قىممىتى;return 0;}
uintptr_t 보드원격대기(uintptr_t ھالەت_قىممىتى){셸대기중=ھالەت_قىممىتى!=0;return 0;}
static int تەييارلىماق_قاپ(void) {
    if(듣는곳>=0)return 0;
    if(!كونتېكست_قىممىتى){
        assh_status_t خاتالىق=assh_context_create(&كونتېكست_قىممىتى,ASSH_SERVER,تەييارلىماق_ساقلىغۇچ,0,&난수기,0);
        if(خاتالىق)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *ئۇسۇل_ھالەت[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        خاتالىق=assh_algo_register(كونتېكست_قىممىتى,ASSH_SAFETY_WEAK,ئۇسۇل_ھالەت);
        if(!خاتالىق)خاتالىق=assh_service_register_va(كونتېكست_قىممىتى,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=كۆچمە_ئاچقۇچ;
        if(!خاتالىق)خاتالىق=assh_key_load(كونتېكست_قىممىتى,assh_context_keys(كونتېكست_قىممىتى),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(كۆچمە_ئاچقۇچ));
        if(خاتالىق){진단("SSH init error ",خاتالىق);assh_context_release(كونتېكست_قىممىتى);كونتېكست_قىممىتى=0;return -5;}
    }
    int ئېغىز_قىممىتى=통신끝점만들기(1);if(ئېغىز_قىممىتى<0)return ئېغىز_قىممىتى;통신주소재사용(ئېغىز_قىممىتى);
    int ئۆلچەم=망주소묶기(ئېغىز_قىممىتى,0,22);if(!ئۆلچەم)ئۆلچەم=연결기다리기(ئېغىز_قىممىتى);
    if(ئۆلچەم<0){ئاياغ_تور(ئېغىز_قىممىتى);return ئۆلچەم;}듣는곳=ئېغىز_قىممىتى;return 0;
}
uintptr_t سۇپا_سايىلەش(uintptr_t 종류,uintptr_t مەشغۇلات) {
    if(종류==1)return(uint32_t)كونترول_يىراق_كۆرسەتكۈچ(مەشغۇلات);
    if(مەشغۇلات==0){ئاياغ_ئۇلىنىش();if(듣는곳>=0)ئاياغ_تور(듣는곳);듣는곳=-1;return 0;}
    if(مەشغۇلات==1){قوزغىتىش_خاتالىق=تەييارلىماق_قاپ();return(uint32_t)قوزغىتىش_خاتالىق;}
    return(uint32_t)(듣는곳>=0?1:قوزغىتىش_خاتالىق);
}
void تەييارلىماق_يىراق(void){قوزغىتىش_خاتالىق=تەييارلىماق_قاپ();كونترول_يىراق_كۆرسەتكۈچ(1);}
static int 같은말(const struct assh_cbuffer_s *مەلۇمات,const char *سۆز_تېكست) {
    size_t ئۇزۇنلۇق_قىممىتى=strlen(سۆز_تېكست);return مەلۇمات->size==ئۇزۇنلۇق_قىممىتى&&!memcmp(مەلۇمات->data,سۆز_تېكست,ئۇزۇنلۇق_قىممىتى);
}
static int 터미널요청(const struct assh_cbuffer_s *مەلۇمات) {
    if(مەلۇمات->size<24)return 0;
    const unsigned char *مەلۇمات_ئورۇنلاشتۇرۇش=مەلۇمات->data;unsigned ئۇزۇنلۇق_قىممىتى=assh_load_u32(مەلۇمات_ئورۇنلاشتۇرۇش);
    if(ئۇزۇنلۇق_قىممىتى>128||مەلۇمات->size<ئۇزۇنلۇق_قىممىتى+24)return 0;
    unsigned ھالەت_قىممىتى_a83655ea=assh_load_u32(مەلۇمات_ئورۇنلاشتۇرۇش+4+ئۇزۇنلۇق_قىممىتى+16);
    return ھالەت_قىممىتى_a83655ea<=2048&&مەلۇمات->size==ئۇزۇنلۇق_قىممىتى+24+ھالەت_قىممىتى_a83655ea;
}
static void 요청처리(struct assh_event_request_s *ھادىسە) {
    if(!인증됨||ھادىسە->ch!=قانال_كىرگۈزۈش||!قانال_كىرگۈزۈش)return;
    if(같은말(&ھادىسە->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&ھادىسە->rq_data))ھادىسە->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&ھادىسە->type,"window-change")) {
        if(셸시작됨&&ھادىسە->rq_data.size==16)ھادىسە->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *بۇيرۇق=0;unsigned ئۇزۇنلۇق_قىممىتى=0;
    if(같은말(&ھادىسە->type,"exec")) {
        if(ھادىسە->rq_data.size<4)return;
        ئۇزۇنلۇق_قىممىتى=assh_load_u32(ھادىسە->rq_data.data);
        if(!ئۇزۇنلۇق_قىممىتى||ئۇزۇنلۇق_قىممىتى>2048||ھادىسە->rq_data.size!=ئۇزۇنلۇق_قىممىتى+4)return;
        بۇيرۇق=ھادىسە->rq_data.data+4;
        for(unsigned 순번=0;순번<ئۇزۇنلۇق_قىممىتى;순번++)if(!بۇيرۇق[순번])return;
        بۇيرۇق_تىپ=1;
    }else if(!같은말(&ھادىسە->type,"shell")||ھادىسە->rq_data.size)return;
    if(sizeof(입력줄)-입력수<ئۇزۇنلۇق_قىممىتى+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(ئۇزۇنلۇق_قىممىتى)원격입력넣기(بۇيرۇق,ئۇزۇنلۇق_قىممىتى);원격입력넣기(&끝,1);
    셸시작됨=1;ھادىسە->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!بۇيرۇق_تىپ){const char *چۈشەندۈرۈش_ھۆججىتى_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*چۈشەندۈرۈش_ھۆججىتى_eb81d7d9)원격출력(*چۈشەندۈرۈش_ھۆججىتى_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(باراۋەرلىك_قىممىتى<0){if(지금<재접속시각)return;باراۋەرلىك_قىممىتى=망연결받기(듣는곳);if(باراۋەرلىك_قىممىتى<0)return;
        접속시각=지금;assh_status_t خاتالىق=assh_session_create(كونتېكست_قىممىتى,&ئۇلىنىش_e05f319b);
        if(خاتالىق){ئۇلىنىش_e05f319b=0;진단("SSH session error ",خاتالىق);ئاياغ_ئۇلىنىش();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){ئاياغ_ئۇلىنىش();return;}
    if(قانال_كىرگۈزۈش&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t خاتالىق=assh_channel_data(قانال_كىرگۈزۈش,출력줄+출력앞,&수);
            if(!خاتالىق){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(خاتالىق!=ASSH_NO_DATA){ئاياغ_ئۇلىنىش();return;}
        }
        if(تاماملىماق_ھالەت>=0&&!출력수){unsigned char ھالەت_قىممىتى[4];assh_store_u32(ھالەت_قىممىتى,(uint32_t)تاماملىماق_ھالەت);
            if(assh_request(ئۇلىنىش_e05f319b,قانال_كىرگۈزۈش,"exit-status",11,ھالەت_قىممىتى,4,0)||assh_channel_eof(قانال_كىرگۈزۈش)||assh_channel_close(قانال_كىرگۈزۈش)) {ئاياغ_ئۇلىنىش();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s ھادىسە;
        if(!assh_event_get(ئۇلىنىش_e05f319b,&ھادىسە,지금/1000)){ئاياغ_ئۇلىنىش();return;}
        assh_status_t خاتالىق=ASSH_OK;int 쉬기=0,끊기=0;
        switch(ھادىسە.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(باراۋەرلىك_قىممىتى,ھادىسە.transport.read.buf.data,ھادىسە.transport.read.buf.size);
            if(수>0)ھادىسە.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(باراۋەرلىك_قىممىتى,ھادىسە.transport.write.buf.data,ھادىسە.transport.write.buf.size);
            if(수>0)ھادىسە.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ھادىسە.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ھادىسە.userauth_server.methods.retries>3)ھادىسە.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *مەلۇمات=&ھادىسە.userauth_server.password;
            if(같은말(&مەلۇمات->username,"user")&&مەلۇمات->password.size<=256&&!مەلۇمات->new_password.size) {
                unsigned char 요약[32];원격요약(مەلۇمات->password.data,مەلۇمات->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)مەلۇمات->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *مەلۇمات=&ھادىسە.connection.channel_open;
            if(인증됨&&!قانال_كىرگۈزۈش&&셸대기중&&같은말(&مەلۇمات->type,"session")&&!مەلۇمات->rq_data.size) {
                مەلۇمات->reply=ASSH_CONNECTION_REPLY_SUCCESS;مەلۇمات->pkt_size=4096;
                مەلۇمات->win_size=-1;قانال_كىرگۈزۈش=مەلۇمات->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&ھادىسە.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *مەلۇمات=&ھادىسە.connection.channel_data;
            if(!셸시작됨||مەلۇمات->ch!=قانال_كىرگۈزۈش||مەلۇمات->ext){끊기=1;break;}
            unsigned 수=مەلۇمات->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(مەلۇمات->data.data[순번]==4){تاماملىماق_ھالەت=0;수=순번;مەلۇمات->transferred=مەلۇمات->data.size;break;}
            원격입력넣기(مەلۇمات->data.data,수);if(!مەلۇمات->transferred)مەلۇمات->transferred=수;
            if(!수&&تاماملىماق_ھالەت<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: قانال_كىرگۈزۈش=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",ھادىسە.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(ئۇلىنىش_e05f319b,&ھادىسە,خاتالىق);
        if(끊기){ئاياغ_ئۇلىنىش();return;}if(쉬기)return;
    }
}
