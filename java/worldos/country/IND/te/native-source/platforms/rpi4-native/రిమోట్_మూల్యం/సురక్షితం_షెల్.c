/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "రిమోట్_మూల్యం.h"
#include "암호기반.h"
#include "ప్రొఫైల్.h"
#include "../నెట్_వర్క్_దొంతర/నెట్_వర్క్_దొంతర.h"
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
static struct assh_context_s *సందర్భం_మూల్యం;
static struct assh_session_s *కనెక్షన్_e05f319b;
static struct assh_channel_s *ఛానల్_ప్రవేశం;
static int 듣는곳=-1,పియర్_మూల్యం=-1,인증됨,셸시작됨,ఆదేశం_టైప్_చేయండి,ముగించు_స్థితి=-1,닫을예정,బూట్_దోషం,셸대기중;
static uintptr_t కనెక్షన్_సమయం,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *పదం_పాఠం,unsigned మూల్యం) {
    while(*పదం_పాఠం)보드글자쓰기(*పదం_పాఠం++);
    char అంకె_మూల్యం[12];unsigned 수=0;do{అంకె_మూల్యం[수++]='0'+మూల్యం%10;మూల్యం/=10;}while(మూల్యం);
    while(수)보드글자쓰기(అంకె_మూల్యం[--수]);보드글자쓰기(10);
}
static assh_status_t సిద్ధం_చేయు_మెమరీ(void *డేటా,void **ఇమెయిల్,size_t పరిమాణం,enum assh_alloc_type_e 종류) {
    (void)డేటా;(void)종류;
    if(!పరిమాణం){విడుదల_రిమోట్(*ఇమెయిల్);*ఇమెయిల్=0;return ASSH_OK;}
    void *새주소=원격재할당(*ఇమెయిల్,పరిమాణం);
    if(!새주소)return ASSH_ERR_MEM;*ఇమెయిల్=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *డేటా,const struct assh_buffer_s *సీడ్_మూల్యం) {
    (void)డేటా;(void)సీడ్_మూల్యం;unsigned char 시험[32];int ప్రమాణం=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return ప్రమాణం?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *డేటా,uint8_t *ప్రమాణం,size_t పొడవు_మూల్యం,uint_fast8_t 종류) {
    (void)డేటా;(void)종류;if(పొడవు_మూల్యం>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(ప్రమాణం,పొడవు_మూల్యం)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *డేటా){(void)డేటా;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void మూసివేయి_కనెక్షన్(void) {
    인증됨=셸시작됨=0;ఛానల్_ప్రవేశం=0;
    if(కనెక్షన్_e05f319b)assh_session_release(కనెక్షన్_e05f319b);కనెక్షన్_e05f319b=0;
    if(పియర్_మూల్యం>=0)మూసివేయి_నెట్_వర్క్(పియర్_మూల్యం);పియర్_మూల్యం=-1;ఆదేశం_టైప్_చేయండి=0;ముగించు_స్థితి=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *డేటా,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=డేటా[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int అక్షరం_మూల్యం=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return అక్షరం_మూల్యం;
}
void 원격출력(unsigned char అక్షరం_మూల్యం) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=అక్షరం_మూల్యం==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=అక్షరం_మూల్యం;이전출력=అక్షరం_మూల్యం;
}
uintptr_t బోర్డు_ముగించు_రిమోట్_ఆదేశం(uintptr_t స్థితి_మూల్యం){if(셸시작됨&&ఆదేశం_టైప్_చేయండి)ముగించు_స్థితి=(int)స్థితి_మూల్యం;return 0;}
uintptr_t బోర్డు_రిమోట్_వేచియుండు(uintptr_t స్థితి_మూల్యం){셸대기중=స్థితి_మూల్యం!=0;return 0;}
static int సిద్ధం_చేయు_షెల్(void) {
    if(듣는곳>=0)return 0;
    if(!సందర్భం_మూల్యం){
        assh_status_t దోషం=assh_context_create(&సందర్భం_మూల్యం,ASSH_SERVER,సిద్ధం_చేయు_మెమరీ,0,&난수기,0);
        if(దోషం)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *విధానం_మోడ్_3f5e5497[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        దోషం=assh_algo_register(సందర్భం_మూల్యం,ASSH_SAFETY_WEAK,విధానం_మోడ్_3f5e5497);
        if(!దోషం)దోషం=assh_service_register_va(సందర్భం_మూల్యం,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=పరికరం_కీ;
        if(!దోషం)దోషం=assh_key_load(సందర్భం_మూల్యం,assh_context_keys(సందర్భం_మూల్యం),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(పరికరం_కీ));
        if(దోషం){진단("SSH init error ",దోషం);assh_context_release(సందర్భం_మూల్యం);సందర్భం_మూల్యం=0;return -5;}
    }
    int పోర్టు_మూల్యం=통신끝점만들기(1);if(పోర్టు_మూల్యం<0)return పోర్టు_మూల్యం;통신주소재사용(పోర్టు_మూల్యం);
    int ప్రమాణం=망주소묶기(పోర్టు_మూల్యం,0,22);if(!ప్రమాణం)ప్రమాణం=연결기다리기(పోర్టు_మూల్యం);
    if(ప్రమాణం<0){మూసివేయి_నెట్_వర్క్(పోర్టు_మూల్యం);return ప్రమాణం;}듣는곳=పోర్టు_మూల్యం;return 0;
}
uintptr_t బోర్డు_వ్యవహిత_నియంత్రణ(uintptr_t 종류,uintptr_t చర్య) {
    if(종류==1)return(uint32_t)నియంత్రణ_రిమోట్_ప్రదర్శన(చర్య);
    if(చర్య==0){మూసివేయి_కనెక్షన్();if(듣는곳>=0)మూసివేయి_నెట్_వర్క్(듣는곳);듣는곳=-1;return 0;}
    if(చర్య==1){బూట్_దోషం=సిద్ధం_చేయు_షెల్();return(uint32_t)బూట్_దోషం;}
    return(uint32_t)(듣는곳>=0?1:బూట్_దోషం);
}
void సిద్ధం_చేయు_రిమోట్(void){బూట్_దోషం=సిద్ధం_చేయు_షెల్();నియంత్రణ_రిమోట్_ప్రదర్శన(1);}
static int 같은말(const struct assh_cbuffer_s *డేటా,const char *పదం_పాఠం) {
    size_t పొడవు_మూల్యం=strlen(పదం_పాఠం);return డేటా->size==పొడవు_మూల్యం&&!memcmp(డేటా->data,పదం_పాఠం,పొడవు_మూల్యం);
}
static int 터미널요청(const struct assh_cbuffer_s *డేటా) {
    if(డేటా->size<24)return 0;
    const unsigned char *డేటా_స్థాయి=డేటా->data;unsigned పొడవు_మూల్యం=assh_load_u32(డేటా_స్థాయి);
    if(పొడవు_మూల్యం>128||డేటా->size<పొడవు_మూల్యం+24)return 0;
    unsigned మోడ్_మూల్యం=assh_load_u32(డేటా_స్థాయి+4+పొడవు_మూల్యం+16);
    return మోడ్_మూల్యం<=2048&&డేటా->size==పొడవు_మూల్యం+24+మోడ్_మూల్యం;
}
static void 요청처리(struct assh_event_request_s *ఈవెంట్) {
    if(!인증됨||ఈవెంట్->ch!=ఛానల్_ప్రవేశం||!ఛానల్_ప్రవేశం)return;
    if(같은말(&ఈవెంట్->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&ఈవెంట్->rq_data))ఈవెంట్->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&ఈవెంట్->type,"window-change")) {
        if(셸시작됨&&ఈవెంట్->rq_data.size==16)ఈవెంట్->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *ఆదేశము=0;unsigned పొడవు_మూల్యం=0;
    if(같은말(&ఈవెంట్->type,"exec")) {
        if(ఈవెంట్->rq_data.size<4)return;
        పొడవు_మూల్యం=assh_load_u32(ఈవెంట్->rq_data.data);
        if(!పొడవు_మూల్యం||పొడవు_మూల్యం>2048||ఈవెంట్->rq_data.size!=పొడవు_మూల్యం+4)return;
        ఆదేశము=ఈవెంట్->rq_data.data+4;
        for(unsigned 순번=0;순번<పొడవు_మూల్యం;순번++)if(!ఆదేశము[순번])return;
        ఆదేశం_టైప్_చేయండి=1;
    }else if(!같은말(&ఈవెంట్->type,"shell")||ఈవెంట్->rq_data.size)return;
    if(sizeof(입력줄)-입력수<పొడవు_మూల్యం+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(పొడవు_మూల్యం)원격입력넣기(ఆదేశము,పొడవు_మూల్యం);원격입력넣기(&끝,1);
    셸시작됨=1;ఈవెంట్->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!ఆదేశం_టైప్_చేయండి){const char *మార్గదర్శక_సమాచారం_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*మార్గదర్శక_సమాచారం_eb81d7d9)원격출력(*మార్గదర్శక_సమాచారం_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(పియర్_మూల్యం<0){if(지금<재접속시각)return;పియర్_మూల్యం=망연결받기(듣는곳);if(పియర్_మూల్యం<0)return;
        కనెక్షన్_సమయం=지금;assh_status_t దోషం=assh_session_create(సందర్భం_మూల్యం,&కనెక్షన్_e05f319b);
        if(దోషం){కనెక్షన్_e05f319b=0;진단("SSH session error ",దోషం);మూసివేయి_కనెక్షన్();return;}}
    if((!인증됨&&지금-కనెక్షన్_సమయం>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){మూసివేయి_కనెక్షన్();return;}
    if(ఛానల్_ప్రవేశం&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t దోషం=assh_channel_data(ఛానల్_ప్రవేశం,출력줄+출력앞,&수);
            if(!దోషం){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(దోషం!=ASSH_NO_DATA){మూసివేయి_కనెక్షన్();return;}
        }
        if(ముగించు_స్థితి>=0&&!출력수){unsigned char స్థితి_మూల్యం[4];assh_store_u32(స్థితి_మూల్యం,(uint32_t)ముగించు_స్థితి);
            if(assh_request(కనెక్షన్_e05f319b,ఛానల్_ప్రవేశం,"exit-status",11,స్థితి_మూల్యం,4,0)||assh_channel_eof(ఛానల్_ప్రవేశం)||assh_channel_close(ఛానల్_ప్రవేశం)) {మూసివేయి_కనెక్షన్();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s ఈవెంట్;
        if(!assh_event_get(కనెక్షన్_e05f319b,&ఈవెంట్,지금/1000)){మూసివేయి_కనెక్షన్();return;}
        assh_status_t దోషం=ASSH_OK;int 쉬기=0,끊기=0;
        switch(ఈవెంట్.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(పియర్_మూల్యం,ఈవెంట్.transport.read.buf.data,ఈవెంట్.transport.read.buf.size);
            if(수>0)ఈవెంట్.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(పియర్_మూల్యం,ఈవెంట్.transport.write.buf.data,ఈవెంట్.transport.write.buf.size);
            if(수>0)ఈవెంట్.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ఈవెంట్.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ఈవెంట్.userauth_server.methods.retries>3)ఈవెంట్.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *డేటా=&ఈవెంట్.userauth_server.password;
            if(같은말(&డేటా->username,"user")&&డేటా->password.size<=256&&!డేటా->new_password.size) {
                unsigned char 요약[32];원격요약(డేటా->password.data,డేటా->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)డేటా->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *డేటా=&ఈవెంట్.connection.channel_open;
            if(인증됨&&!ఛానల్_ప్రవేశం&&셸대기중&&같은말(&డేటా->type,"session")&&!డేటా->rq_data.size) {
                డేటా->reply=ASSH_CONNECTION_REPLY_SUCCESS;డేటా->pkt_size=4096;
                డేటా->win_size=-1;ఛానల్_ప్రవేశం=డేటా->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&ఈవెంట్.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *డేటా=&ఈవెంట్.connection.channel_data;
            if(!셸시작됨||డేటా->ch!=ఛానల్_ప్రవేశం||డేటా->ext){끊기=1;break;}
            unsigned 수=డేటా->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(డేటా->data.data[순번]==4){ముగించు_స్థితి=0;수=순번;డేటా->transferred=డేటా->data.size;break;}
            원격입력넣기(డేటా->data.data,수);if(!డేటా->transferred)డేటా->transferred=수;
            if(!수&&ముగించు_స్థితి<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: ఛానల్_ప్రవేశం=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",ఈవెంట్.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(కనెక్షన్_e05f319b,&ఈవెంట్,దోషం);
        if(끊기){మూసివేయి_కనెక్షన్();return;}if(쉬기)return;
    }
}
