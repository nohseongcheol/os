/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "വിദൂര_മൂല്യം.h"
#include "ക്രിപ്റ്റോഗ്രഫി_പിന്തുണ.h"
#include "പ്രൊഫൈൽ.h"
#include "../നെറ്റ്_വർക്ക്_സ്റ്റാക്ക്_ചെയ്യുക/നെറ്റ്_വർക്ക്_സ്റ്റാക്ക്_ചെയ്യുക.h"
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
static struct assh_context_s *സന്ദര്_ഭം_മൂല്യം;
static struct assh_session_s *കണക്ഷൻ_e05f319b;
static struct assh_channel_s *ചാനല്_എന്_ട്രി;
static int ശ്രവിക്കൽ_അവസാനബിന്ദു=-1,പീര്_മൂല്യം=-1,인증됨,셸시작됨,കമാന്_ഡ്_ടൈപ്പ്_ചെയ്യുക,അവസാനിപ്പിക്കുക_അവസ്ഥ=-1,닫을예정,ബൂട്ട്_തെറ്റ്,ഷെല്_കാക്കൽ;
static uintptr_t കണക്ഷൻ_സമയം,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *വാക്ക്_ലിഖിതം,unsigned മൂല്യം) {
    while(*വാക്ക്_ലിഖിതം)보드글자쓰기(*വാക്ക്_ലിഖിതം++);
    char അക്കം_മൂല്യം[12];unsigned 수=0;do{അക്കം_മൂല്യം[수++]='0'+മൂല്യം%10;മൂല്യം/=10;}while(മൂല്യം);
    while(수)보드글자쓰기(അക്കം_മൂല്യം[--수]);보드글자쓰기(10);
}
static assh_status_t തയ്യാറാക്കുക_മെമ്മറി(void *ഡാറ്റാ,void **ഇമെയിൽ,size_t വലിപ്പം,enum assh_alloc_type_e 종류) {
    (void)ഡാറ്റാ;(void)종류;
    if(!വലിപ്പം){റിലീസ്_വിദൂര(*ഇമെയിൽ);*ഇമെയിൽ=0;return ASSH_OK;}
    void *새주소=원격재할당(*ഇമെയിൽ,വലിപ്പം);
    if(!새주소)return ASSH_ERR_MEM;*ഇമെയിൽ=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *ഡാറ്റാ,const struct assh_buffer_s *സീഡ്_മൂല്യം) {
    (void)ഡാറ്റാ;(void)സീഡ്_മൂല്യം;unsigned char 시험[32];int അളവ്=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return അളവ്?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *ഡാറ്റാ,uint8_t *അളവ്,size_t ദൈര്_ഘ്യം_മൂല്യം,uint_fast8_t 종류) {
    (void)ഡാറ്റാ;(void)종류;if(ദൈര്_ഘ്യം_മൂല്യം>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(അളവ്,ദൈര്_ഘ്യം_മൂല്യം)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *ഡാറ്റാ){(void)ഡാറ്റാ;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void അടയ്ക്കുക_കണക്ഷൻ(void) {
    인증됨=셸시작됨=0;ചാനല്_എന്_ട്രി=0;
    if(കണക്ഷൻ_e05f319b)assh_session_release(കണക്ഷൻ_e05f319b);കണക്ഷൻ_e05f319b=0;
    if(പീര്_മൂല്യം>=0)അടയ്ക്കുക_നെറ്റ്_വർക്ക്(പീര്_മൂല്യം);പീര്_മൂല്യം=-1;കമാന്_ഡ്_ടൈപ്പ്_ചെയ്യുക=0;അവസാനിപ്പിക്കുക_അവസ്ഥ=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *ഡാറ്റാ,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=ഡാറ്റാ[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int പ്രതീകം_മൂല്യം=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return പ്രതീകം_മൂല്യം;
}
void 원격출력(unsigned char പ്രതീകം_മൂല്യം) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=പ്രതീകം_മൂല്യം==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=പ്രതീകം_മൂല്യം;이전출력=പ്രതീകം_മൂല്യം;
}
uintptr_t ബോർഡ്_അവസാനിപ്പിക്കുക_വിദൂര_കമാന്_ഡ്(uintptr_t അവസ്ഥ_മൂല്യം){if(셸시작됨&&കമാന്_ഡ്_ടൈപ്പ്_ചെയ്യുക)അവസാനിപ്പിക്കുക_അവസ്ഥ=(int)അവസ്ഥ_മൂല്യം;return 0;}
uintptr_t ബോർഡ്_വിദൂര_കാക്കുക(uintptr_t അവസ്ഥ_മൂല്യം){ഷെല്_കാക്കൽ=അവസ്ഥ_മൂല്യം!=0;return 0;}
static int തയ്യാറാക്കുക_ഷെല്(void) {
    if(ശ്രവിക്കൽ_അവസാനബിന്ദു>=0)return 0;
    if(!സന്ദര്_ഭം_മൂല്യം){
        assh_status_t പിശക്=assh_context_create(&സന്ദര്_ഭം_മൂല്യം,ASSH_SERVER,തയ്യാറാക്കുക_മെമ്മറി,0,&난수기,0);
        if(പിശക്)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *విధానం_മോഡ്[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        പിശക്=assh_algo_register(സന്ദര്_ഭം_മൂല്യം,ASSH_SAFETY_WEAK,విధానం_മോഡ്);
        if(!പിശക്)പിശക്=assh_service_register_va(സന്ദര്_ഭം_മൂല്യം,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=മൊബൈൽ_കീ;
        if(!പിശക്)പിശക്=assh_key_load(സന്ദര്_ഭം_മൂല്യം,assh_context_keys(സന്ദര്_ഭം_മൂല്യം),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(മൊബൈൽ_കീ));
        if(പിശക്){진단("SSH init error ",പിശക്);assh_context_release(സന്ദര്_ഭം_മൂല്യം);സന്ദര്_ഭം_മൂല്യം=0;return -5;}
    }
    int പോര്_ട്ട്_മൂല്യം=통신끝점만들기(1);if(പോര്_ട്ട്_മൂല്യം<0)return പോര്_ട്ട്_മൂല്യം;통신주소재사용(പോര്_ട്ട്_മൂല്യം);
    int അളവ്=망주소묶기(പോര്_ട്ട്_മൂല്യം,0,22);if(!അളവ്)അളവ്=연결기다리기(പോര്_ട്ട്_മൂല്യം);
    if(അളവ്<0){അടയ്ക്കുക_നെറ്റ്_വർക്ക്(പോര്_ട്ട്_മൂല്യം);return അളവ്;}ശ്രവിക്കൽ_അവസാനബിന്ദു=പോര്_ട്ട്_മൂല്യം;return 0;
}
uintptr_t ബോർഡ്_ഷാഡോയിംഗ്(uintptr_t 종류,uintptr_t നടപടി) {
    if(종류==1)return(uint32_t)നിയന്ത്രണം_വിദൂര_പ്രദര്_ശനം(നടപടി);
    if(നടപടി==0){അടയ്ക്കുക_കണക്ഷൻ();if(ശ്രവിക്കൽ_അവസാനബിന്ദു>=0)അടയ്ക്കുക_നെറ്റ്_വർക്ക്(ശ്രവിക്കൽ_അവസാനബിന്ദു);ശ്രവിക്കൽ_അവസാനബിന്ദു=-1;return 0;}
    if(നടപടി==1){ബൂട്ട്_തെറ്റ്=തയ്യാറാക്കുക_ഷെല്();return(uint32_t)ബൂട്ട്_തെറ്റ്;}
    return(uint32_t)(ശ്രവിക്കൽ_അവസാനബിന്ദു>=0?1:ബൂട്ട്_തെറ്റ്);
}
void തയ്യാറാക്കുക_വിദൂര(void){ബൂട്ട്_തെറ്റ്=തയ്യാറാക്കുക_ഷെല്();നിയന്ത്രണം_വിദൂര_പ്രദര്_ശനം(1);}
static int 같은말(const struct assh_cbuffer_s *ഡാറ്റാ,const char *വാക്ക്_ലിഖിതം) {
    size_t ദൈര്_ഘ്യം_മൂല്യം=strlen(വാക്ക്_ലിഖിതം);return ഡാറ്റാ->size==ദൈര്_ഘ്യം_മൂല്യം&&!memcmp(ഡാറ്റാ->data,വാക്ക്_ലിഖിതം,ദൈര്_ഘ്യം_മൂല്യം);
}
static int ടെർമിനൽ_HTTP_അപേക്ഷ(const struct assh_cbuffer_s *ഡാറ്റാ) {
    if(ഡാറ്റാ->size<24)return 0;
    const unsigned char *ഡാറ്റാ_പദവി=ഡാറ്റാ->data;unsigned ദൈര്_ഘ്യം_മൂല്യം=assh_load_u32(ഡാറ്റാ_പദവി);
    if(ദൈര്_ഘ്യം_മൂല്യം>128||ഡാറ്റാ->size<ദൈര്_ഘ്യം_മൂല്യം+24)return 0;
    unsigned മോഡ്_മൂല്യം=assh_load_u32(ഡാറ്റാ_പദവി+4+ദൈര്_ഘ്യം_മൂല്യം+16);
    return മോഡ്_മൂല്യം<=2048&&ഡാറ്റാ->size==ദൈര്_ഘ്യം_മൂല്യം+24+മോഡ്_മൂല്യം;
}
static void കൈകാര്യംചെയ്യല്_HTTP_അപേക്ഷ(struct assh_event_request_s *ഇവന്റ്) {
    if(!인증됨||ഇവന്റ്->ch!=ചാനല്_എന്_ട്രി||!ചാനല്_എന്_ട്രി)return;
    if(같은말(&ഇവന്റ്->type,"pty-req")) {
        if(!셸시작됨&&ടെർമിനൽ_HTTP_അപേക്ഷ(&ഇവന്റ്->rq_data))ഇവന്റ്->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&ഇവന്റ്->type,"window-change")) {
        if(셸시작됨&&ഇവന്റ്->rq_data.size==16)ഇവന്റ്->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!ഷെല്_കാക്കൽ)return;
    const unsigned char *ആജ്ഞ=0;unsigned ദൈര്_ഘ്യം_മൂല്യം=0;
    if(같은말(&ഇവന്റ്->type,"exec")) {
        if(ഇവന്റ്->rq_data.size<4)return;
        ദൈര്_ഘ്യം_മൂല്യം=assh_load_u32(ഇവന്റ്->rq_data.data);
        if(!ദൈര്_ഘ്യം_മൂല്യം||ദൈര്_ഘ്യം_മൂല്യം>2048||ഇവന്റ്->rq_data.size!=ദൈര്_ഘ്യം_മൂല്യം+4)return;
        ആജ്ഞ=ഇവന്റ്->rq_data.data+4;
        for(unsigned 순번=0;순번<ദൈര്_ഘ്യം_മൂല്യം;순번++)if(!ആജ്ഞ[순번])return;
        കമാന്_ഡ്_ടൈപ്പ്_ചെയ്യുക=1;
    }else if(!같은말(&ഇവന്റ്->type,"shell")||ഇവന്റ്->rq_data.size)return;
    if(sizeof(입력줄)-입력수<ദൈര്_ഘ്യം_മൂല്യം+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(ദൈര്_ഘ്യം_മൂല്യം)원격입력넣기(ആജ്ഞ,ദൈര്_ഘ്യം_മൂല്യം);원격입력넣기(&끝,1);
    셸시작됨=1;ഇവന്റ്->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!കമാന്_ഡ്_ടൈപ്പ്_ചെയ്യുക){const char *readme_ഫയല്_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*readme_ഫയല്_eb81d7d9)원격출력(*readme_ഫയല്_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(ശ്രവിക്കൽ_അവസാനബിന്ദു<0)return;
    uintptr_t ഇപ്പോൾ_മൂല്യം=보드밀리초();
    if(പീര്_മൂല്യം<0){if(ഇപ്പോൾ_മൂല്യം<재접속시각)return;പീര്_മൂല്യം=망연결받기(ശ്രവിക്കൽ_അവസാനബിന്ദു);if(പീര്_മൂല്യം<0)return;
        കണക്ഷൻ_സമയം=ഇപ്പോൾ_മൂല്യം;assh_status_t പിശക്=assh_session_create(സന്ദര്_ഭം_മൂല്യം,&കണക്ഷൻ_e05f319b);
        if(പിശക്){കണക്ഷൻ_e05f319b=0;진단("SSH session error ",പിശക്);അടയ്ക്കുക_കണക്ഷൻ();return;}}
    if((!인증됨&&ഇപ്പോൾ_മൂല്യം-കണക്ഷൻ_സമയം>30000)||닫을예정==2||(닫을예정&&ഇപ്പോൾ_മൂല്യം>=닫는시각)){അടയ്ക്കുക_കണക്ഷൻ();return;}
    if(ചാനല്_എന്_ട്രി&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t പിശക്=assh_channel_data(ചാനല്_എന്_ട്രി,출력줄+출력앞,&수);
            if(!പിശക്){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(പിശക്!=ASSH_NO_DATA){അടയ്ക്കുക_കണക്ഷൻ();return;}
        }
        if(അവസാനിപ്പിക്കുക_അവസ്ഥ>=0&&!출력수){unsigned char അവസ്ഥ_മൂല്യം[4];assh_store_u32(അവസ്ഥ_മൂല്യം,(uint32_t)അവസാനിപ്പിക്കുക_അവസ്ഥ);
            if(assh_request(കണക്ഷൻ_e05f319b,ചാനല്_എന്_ട്രി,"exit-status",11,അവസ്ഥ_മൂല്യം,4,0)||assh_channel_eof(ചാനല്_എന്_ട്രി)||assh_channel_close(ചാനല്_എന്_ട്രി)) {അടയ്ക്കുക_കണക്ഷൻ();return;}
            닫을예정=1;닫는시각=ഇപ്പോൾ_മൂല്യം+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s ഇവന്റ്;
        if(!assh_event_get(കണക്ഷൻ_e05f319b,&ഇവന്റ്,ഇപ്പോൾ_മൂല്യം/1000)){അടയ്ക്കുക_കണക്ഷൻ();return;}
        assh_status_t പിശക്=ASSH_OK;int 쉬기=0,വിച്ഛേദിക്കുക_അവസാനബിന്ദു=0;
        switch(ഇവന്റ്.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(പീര്_മൂല്യം,ഇവന്റ്.transport.read.buf.data,ഇവന്റ്.transport.read.buf.size);
            if(수>0)ഇവന്റ്.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else വിച്ഛേദിക്കുക_അവസാനബിന്ദു=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(പീര്_മൂല്യം,ഇവന്റ്.transport.write.buf.data,ഇവന്റ്.transport.write.buf.size);
            if(수>0)ഇവന്റ്.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else വിച്ഛേദിക്കുക_അവസാനബിന്ദു=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ഇവന്റ്.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ഇവന്റ്.userauth_server.methods.retries>3)ഇവന്റ്.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *ഡാറ്റാ=&ഇവന്റ്.userauth_server.password;
            if(같은말(&ഡാറ്റാ->username,"user")&&ഡാറ്റാ->password.size<=256&&!ഡാറ്റാ->new_password.size) {
                unsigned char 요약[32];원격요약(ഡാറ്റാ->password.data,ഡാറ്റാ->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)ഡാറ്റാ->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *ഡാറ്റാ=&ഇവന്റ്.connection.channel_open;
            if(인증됨&&!ചാനല്_എന്_ട്രി&&ഷെല്_കാക്കൽ&&같은말(&ഡാറ്റാ->type,"session")&&!ഡാറ്റാ->rq_data.size) {
                ഡാറ്റാ->reply=ASSH_CONNECTION_REPLY_SUCCESS;ഡാറ്റാ->pkt_size=4096;
                ഡാറ്റാ->win_size=-1;ചാനല്_എന്_ട്രി=ഡാറ്റാ->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: കൈകാര്യംചെയ്യല്_HTTP_അപേക്ഷ(&ഇവന്റ്.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *ഡാറ്റാ=&ഇവന്റ്.connection.channel_data;
            if(!셸시작됨||ഡാറ്റാ->ch!=ചാനല്_എന്_ട്രി||ഡാറ്റാ->ext){വിച്ഛേദിക്കുക_അവസാനബിന്ദു=1;break;}
            unsigned 수=ഡാറ്റാ->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(ഡാറ്റാ->data.data[순번]==4){അവസാനിപ്പിക്കുക_അവസ്ഥ=0;수=순번;ഡാറ്റാ->transferred=ഡാറ്റാ->data.size;break;}
            원격입력넣기(ഡാറ്റാ->data.data,수);if(!ഡാറ്റാ->transferred)ഡാറ്റാ->transferred=수;
            if(!수&&അവസാനിപ്പിക്കുക_അവസ്ഥ<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: ചാനല്_എന്_ട്രി=0;셸시작됨=0;닫을예정=1;닫는시각=ഇപ്പോൾ_മൂല്യം+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",ഇവന്റ്.session.error.code);വിച്ഛേദിക്കുക_അവസാനബിന്ദു=1;break;
        case ASSH_EVENT_DISCONNECT: വിച്ഛേദിക്കുക_അവസാനബിന്ദു=1;break;
        default: break;
        }
        assh_event_done(കണക്ഷൻ_e05f319b,&ഇവന്റ്,പിശക്);
        if(വിച്ഛേദിക്കുക_അവസാനബിന്ദു){അടയ്ക്കുക_കണക്ഷൻ();return;}if(쉬기)return;
    }
}
