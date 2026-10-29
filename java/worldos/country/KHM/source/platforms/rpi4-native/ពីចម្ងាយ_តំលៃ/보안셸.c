/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "ពីចម្ងាយ_តំលៃ.h"
#include "암호기반.h"
#include "ទម្រង់.h"
#include "../ណិតវឺក_គរ/ណិតវឺក_គរ.h"
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
static struct assh_context_s *បរិបទ_តំលៃ;
static struct assh_session_s *ការភ្ជាប់_e05f319b;
static struct assh_channel_s *កាណាល់_ការបញ្ចូល;
static int 듣는곳=-1,សិទ្ធស្មើ_តំលៃ=-1,인증됨,셸시작됨,ពាក្យបញ្ជា_វាយបញ្ចូល,បញ្ចប់_ភាព=-1,닫을예정,ការចាប់ផ្តើម_កំហុស,셸대기중;
static uintptr_t ការភ្ជាប់_ពេល_វេលា,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *ពាក្យ_អត្ថបទ,unsigned តំលៃ) {
    while(*ពាក្យ_អត្ថបទ)보드글자쓰기(*ពាក្យ_អត្ថបទ++);
    char 숫자[12];unsigned 수=0;do{숫자[수++]='0'+តំលៃ%10;តំលៃ/=10;}while(តំលៃ);
    while(수)보드글자쓰기(숫자[--수]);보드글자쓰기(10);
}
static assh_status_t រៀបចំ_សតិ(void *ទិន្នន័យ,void **អ៊ីម៉ែល,size_t ដាក់ទំហំ,enum assh_alloc_type_e 종류) {
    (void)ទិន្នន័យ;(void)종류;
    if(!ដាក់ទំហំ){លែង_ពីចម្ងាយ(*អ៊ីម៉ែល);*អ៊ីម៉ែល=0;return ASSH_OK;}
    void *새주소=원격재할당(*អ៊ីម៉ែល,ដាក់ទំហំ);
    if(!새주소)return ASSH_ERR_MEM;*អ៊ីម៉ែល=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *ទិន្នន័យ,const struct assh_buffer_s *តម្លៃដើម_តំលៃ) {
    (void)ទិន្នន័យ;(void)តម្លៃដើម_តំលៃ;unsigned char 시험[32];int ការវាស់វែង=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return ការវាស់វែង?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *ទិន្នន័យ,uint8_t *ការវាស់វែង,size_t ប្រវែង_តំលៃ,uint_fast8_t 종류) {
    (void)ទិន្នន័យ;(void)종류;if(ប្រវែង_តំលៃ>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(ការវាស់វែង,ប្រវែង_តំលៃ)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *ទិន្នន័យ){(void)ទិន្នន័យ;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void បិទ_ការភ្ជាប់(void) {
    인증됨=셸시작됨=0;កាណាល់_ការបញ្ចូល=0;
    if(ការភ្ជាប់_e05f319b)assh_session_release(ការភ្ជាប់_e05f319b);ការភ្ជាប់_e05f319b=0;
    if(សិទ្ធស្មើ_តំលៃ>=0)បិទ_ណិតវឺក(សិទ្ធស្មើ_តំលៃ);សិទ្ធស្មើ_តំលៃ=-1;ពាក្យបញ្ជា_វាយបញ្ចូល=0;បញ្ចប់_ភាព=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *ទិន្នន័យ,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=ទិន្នន័យ[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int តួអក្សរ_តំលៃ=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return តួអក្សរ_តំលៃ;
}
void 원격출력(unsigned char តួអក្សរ_តំលៃ) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=តួអក្សរ_តំលៃ==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=តួអក្សរ_តំលៃ;이전출력=តួអក្សរ_តំលៃ;
}
uintptr_t ផ្ទាំង_បញ្ចប់_ពីចម្ងាយ_ពាក្យបញ្ជា(uintptr_t ភាព_តំលៃ){if(셸시작됨&&ពាក្យបញ្ជា_វាយបញ្ចូល)បញ្ចប់_ភាព=(int)ភាព_តំលៃ;return 0;}
uintptr_t ផ្ទាំង_ពីចម្ងាយ_រង់ចាំ(uintptr_t ភាព_តំលៃ){셸대기중=ភាព_តំលៃ!=0;return 0;}
static int 셸준비(void) {
    if(듣는곳>=0)return 0;
    if(!បរិបទ_តំលៃ){
        assh_status_t កំហុស=assh_context_create(&បរិបទ_តំលៃ,ASSH_SERVER,រៀបចំ_សតិ,0,&난수기,0);
        if(កំហុស)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *វិធីសាស្រ្ត_ម៉ូដ[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        កំហុស=assh_algo_register(បរិបទ_តំលៃ,ASSH_SAFETY_WEAK,វិធីសាស្រ្ត_ម៉ូដ);
        if(!កំហុស)កំហុស=assh_service_register_va(បរិបទ_តំលៃ,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=ឧបករណ៍_ឃី;
        if(!កំហុស)កំហុស=assh_key_load(បរិបទ_តំលៃ,assh_context_keys(បរិបទ_តំលៃ),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(ឧបករណ៍_ឃី));
        if(កំហុស){진단("SSH init error ",កំហុស);assh_context_release(បរិបទ_តំលៃ);បរិបទ_តំលៃ=0;return -5;}
    }
    int ច្រក_តំលៃ=통신끝점만들기(1);if(ច្រក_តំលៃ<0)return ច្រក_តំលៃ;통신주소재사용(ច្រក_តំលៃ);
    int ការវាស់វែង=망주소묶기(ច្រក_តំលៃ,0,22);if(!ការវាស់វែង)ការវាស់វែង=연결기다리기(ច្រក_តំលៃ);
    if(ការវាស់វែង<0){បិទ_ណិតវឺក(ច្រក_តំលៃ);return ការវាស់វែង;}듣는곳=ច្រក_តំលៃ;return 0;
}
uintptr_t ផ្ទាំង_ការបញ្ជាពីចម្ងាយ(uintptr_t 종류,uintptr_t អំពើ) {
    if(종류==1)return(uint32_t)អង្គបញ្ជា_ពីចម្ងាយ_បង្ហាញ(អំពើ);
    if(អំពើ==0){បិទ_ការភ្ជាប់();if(듣는곳>=0)បិទ_ណិតវឺក(듣는곳);듣는곳=-1;return 0;}
    if(អំពើ==1){ការចាប់ផ្តើម_កំហុស=셸준비();return(uint32_t)ការចាប់ផ្តើម_កំហុស;}
    return(uint32_t)(듣는곳>=0?1:ការចាប់ផ្តើម_កំហុស);
}
void រៀបចំ_ពីចម្ងាយ(void){ការចាប់ផ្តើម_កំហុស=셸준비();អង្គបញ្ជា_ពីចម្ងាយ_បង្ហាញ(1);}
static int 같은말(const struct assh_cbuffer_s *ទិន្នន័យ,const char *ពាក្យ_អត្ថបទ) {
    size_t ប្រវែង_តំលៃ=strlen(ពាក្យ_អត្ថបទ);return ទិន្នន័យ->size==ប្រវែង_តំលៃ&&!memcmp(ទិន្នន័យ->data,ពាក្យ_អត្ថបទ,ប្រវែង_តំលៃ);
}
static int 터미널요청(const struct assh_cbuffer_s *ទិន្នន័យ) {
    if(ទិន្នន័យ->size<24)return 0;
    const unsigned char *ទិន្នន័យ_កំណត់ទីតាំង=ទិន្នន័យ->data;unsigned ប្រវែង_តំលៃ=assh_load_u32(ទិន្នន័យ_កំណត់ទីតាំង);
    if(ប្រវែង_តំលៃ>128||ទិន្នន័យ->size<ប្រវែង_តំលៃ+24)return 0;
    unsigned ម៉ូដ_តំលៃ=assh_load_u32(ទិន្នន័យ_កំណត់ទីតាំង+4+ប្រវែង_តំលៃ+16);
    return ម៉ូដ_តំលៃ<=2048&&ទិន្នន័យ->size==ប្រវែង_តំលៃ+24+ម៉ូដ_តំលៃ;
}
static void 요청처리(struct assh_event_request_s *ព្រឹត្តិការណ៍) {
    if(!인증됨||ព្រឹត្តិការណ៍->ch!=កាណាល់_ការបញ្ចូល||!កាណាល់_ការបញ្ចូល)return;
    if(같은말(&ព្រឹត្តិការណ៍->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&ព្រឹត្តិការណ៍->rq_data))ព្រឹត្តិការណ៍->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&ព្រឹត្តិការណ៍->type,"window-change")) {
        if(셸시작됨&&ព្រឹត្តិការណ៍->rq_data.size==16)ព្រឹត្តិការណ៍->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *ពាក្យ_បញ្ជា=0;unsigned ប្រវែង_តំលៃ=0;
    if(같은말(&ព្រឹត្តិការណ៍->type,"exec")) {
        if(ព្រឹត្តិការណ៍->rq_data.size<4)return;
        ប្រវែង_តំលៃ=assh_load_u32(ព្រឹត្តិការណ៍->rq_data.data);
        if(!ប្រវែង_តំលៃ||ប្រវែង_តំលៃ>2048||ព្រឹត្តិការណ៍->rq_data.size!=ប្រវែង_តំលៃ+4)return;
        ពាក្យ_បញ្ជា=ព្រឹត្តិការណ៍->rq_data.data+4;
        for(unsigned 순번=0;순번<ប្រវែង_តំលៃ;순번++)if(!ពាក្យ_បញ្ជា[순번])return;
        ពាក្យបញ្ជា_វាយបញ្ចូល=1;
    }else if(!같은말(&ព្រឹត្តិការណ៍->type,"shell")||ព្រឹត្តិការណ៍->rq_data.size)return;
    if(sizeof(입력줄)-입력수<ប្រវែង_តំលៃ+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(ប្រវែង_តំលៃ)원격입력넣기(ពាក្យ_បញ្ជា,ប្រវែង_តំលៃ);원격입력넣기(&끝,1);
    셸시작됨=1;ព្រឹត្តិការណ៍->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!ពាក្យបញ្ជា_វាយបញ្ចូល){const char *អានខ្ញុំ_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*អានខ្ញុំ_eb81d7d9)원격출력(*អានខ្ញុំ_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t ឥឡូវ_តំលៃ=보드밀리초();
    if(សិទ្ធស្មើ_តំលៃ<0){if(ឥឡូវ_តំលៃ<재접속시각)return;សិទ្ធស្មើ_តំលៃ=망연결받기(듣는곳);if(សិទ្ធស្មើ_តំលៃ<0)return;
        ការភ្ជាប់_ពេល_វេលា=ឥឡូវ_តំលៃ;assh_status_t កំហុស=assh_session_create(បរិបទ_តំលៃ,&ការភ្ជាប់_e05f319b);
        if(កំហុស){ការភ្ជាប់_e05f319b=0;진단("SSH session error ",កំហុស);បិទ_ការភ្ជាប់();return;}}
    if((!인증됨&&ឥឡូវ_តំលៃ-ការភ្ជាប់_ពេល_វេលា>30000)||닫을예정==2||(닫을예정&&ឥឡូវ_តំលៃ>=닫는시각)){បិទ_ការភ្ជាប់();return;}
    if(កាណាល់_ការបញ្ចូល&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t កំហុស=assh_channel_data(កាណាល់_ការបញ្ចូល,출력줄+출력앞,&수);
            if(!កំហុស){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(កំហុស!=ASSH_NO_DATA){បិទ_ការភ្ជាប់();return;}
        }
        if(បញ្ចប់_ភាព>=0&&!출력수){unsigned char ភាព_តំលៃ[4];assh_store_u32(ភាព_តំលៃ,(uint32_t)បញ្ចប់_ភាព);
            if(assh_request(ការភ្ជាប់_e05f319b,កាណាល់_ការបញ្ចូល,"exit-status",11,ភាព_តំលៃ,4,0)||assh_channel_eof(កាណាល់_ការបញ្ចូល)||assh_channel_close(កាណាល់_ការបញ្ចូល)) {បិទ_ការភ្ជាប់();return;}
            닫을예정=1;닫는시각=ឥឡូវ_តំលៃ+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s ព្រឹត្តិការណ៍;
        if(!assh_event_get(ការភ្ជាប់_e05f319b,&ព្រឹត្តិការណ៍,ឥឡូវ_តំលៃ/1000)){បិទ_ការភ្ជាប់();return;}
        assh_status_t កំហុស=ASSH_OK;int 쉬기=0,끊기=0;
        switch(ព្រឹត្តិការណ៍.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(សិទ្ធស្មើ_តំលៃ,ព្រឹត្តិការណ៍.transport.read.buf.data,ព្រឹត្តិការណ៍.transport.read.buf.size);
            if(수>0)ព្រឹត្តិការណ៍.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(សិទ្ធស្មើ_តំលៃ,ព្រឹត្តិការណ៍.transport.write.buf.data,ព្រឹត្តិការណ៍.transport.write.buf.size);
            if(수>0)ព្រឹត្តិការណ៍.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ព្រឹត្តិការណ៍.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ព្រឹត្តិការណ៍.userauth_server.methods.retries>3)ព្រឹត្តិការណ៍.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *ទិន្នន័យ=&ព្រឹត្តិការណ៍.userauth_server.password;
            if(같은말(&ទិន្នន័យ->username,"user")&&ទិន្នន័យ->password.size<=256&&!ទិន្នន័យ->new_password.size) {
                unsigned char ការសង្ខេប_តំលៃ[32];ពីចម្ងាយ_ការសង្ខេប(ទិន្នន័យ->password.data,ទិន្នន័យ->password.size,ការសង្ខេប_តំលៃ);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=ការសង្ខេប_តំលៃ[순번]^셸암호요약[순번];memset(ការសង្ខេប_តំលៃ,0,32);
                if(!차이)ទិន្នន័យ->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *ទិន្នន័យ=&ព្រឹត្តិការណ៍.connection.channel_open;
            if(인증됨&&!កាណាល់_ការបញ្ចូល&&셸대기중&&같은말(&ទិន្នន័យ->type,"session")&&!ទិន្នន័យ->rq_data.size) {
                ទិន្នន័យ->reply=ASSH_CONNECTION_REPLY_SUCCESS;ទិន្នន័យ->pkt_size=4096;
                ទិន្នន័យ->win_size=-1;កាណាល់_ការបញ្ចូល=ទិន្នន័យ->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&ព្រឹត្តិការណ៍.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *ទិន្នន័យ=&ព្រឹត្តិការណ៍.connection.channel_data;
            if(!셸시작됨||ទិន្នន័យ->ch!=កាណាល់_ការបញ្ចូល||ទិន្នន័យ->ext){끊기=1;break;}
            unsigned 수=ទិន្នន័យ->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(ទិន្នន័យ->data.data[순번]==4){បញ្ចប់_ភាព=0;수=순번;ទិន្នន័យ->transferred=ទិន្នន័យ->data.size;break;}
            원격입력넣기(ទិន្នន័យ->data.data,수);if(!ទិន្នន័យ->transferred)ទិន្នន័យ->transferred=수;
            if(!수&&បញ្ចប់_ភាព<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: កាណាល់_ការបញ្ចូល=0;셸시작됨=0;닫을예정=1;닫는시각=ឥឡូវ_តំលៃ+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",ព្រឹត្តិការណ៍.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(ការភ្ជាប់_e05f319b,&ព្រឹត្តិការណ៍,កំហុស);
        if(끊기){បិទ_ការភ្ជាប់();return;}if(쉬기)return;
    }
}
