/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "алыскы_маани.h"
#include "암호기반.h"
#include "Профиль.h"
#include "../Желе_стек/Желе_стек.h"
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
static struct assh_context_s *Контекст_маани;
static struct assh_session_s *туташуу_e05f319b;
static struct assh_channel_s *канал_киргизме_жазуу;
static int 듣는곳=-1,бирдей_маани=-1,인증됨,셸시작됨,буйрук_түрү,аяктоо_абал=-1,닫을예정,жүктөө_ката,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Сөз_СМС,unsigned маани) {
    while(*Сөз_СМС)보드글자쓰기(*Сөз_СМС++);
    char санарип_маани[12];unsigned 수=0;do{санарип_маани[수++]='0'+маани%10;маани/=10;}while(маани);
    while(수)보드글자쓰기(санарип_маани[--수]);보드글자쓰기(10);
}
static assh_status_t Даярдоо_эс(void *берилмелер,void **дарек,size_t Өлчөмү,enum assh_alloc_type_e 종류) {
    (void)берилмелер;(void)종류;
    if(!Өлчөмү){чыгаруу_алыскы(*дарек);*дарек=0;return ASSH_OK;}
    void *새주소=원격재할당(*дарек,Өлчөмү);
    if(!새주소)return ASSH_ERR_MEM;*дарек=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *берилмелер,const struct assh_buffer_s *үрөөн_маани) {
    (void)берилмелер;(void)үрөөн_маани;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *берилмелер,uint8_t *결과,size_t узундук_маани,uint_fast8_t 종류) {
    (void)берилмелер;(void)종류;if(узундук_маани>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,узундук_маани)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *берилмелер){(void)берилмелер;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void жабуу_туташуу(void) {
    인증됨=셸시작됨=0;канал_киргизме_жазуу=0;
    if(туташуу_e05f319b)assh_session_release(туташуу_e05f319b);туташуу_e05f319b=0;
    if(бирдей_маани>=0)жабуу_Желе(бирдей_маани);бирдей_маани=-1;буйрук_түрү=0;аяктоо_абал=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *берилмелер,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=берилмелер[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int символ_маани_068c2631=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return символ_маани_068c2631;
}
void 원격출력(unsigned char символ_маани_068c2631) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=символ_маани_068c2631==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=символ_маани_068c2631;이전출력=символ_маани_068c2631;
}
uintptr_t 보드원격명령끝(uintptr_t абал_маани){if(셸시작됨&&буйрук_түрү)аяктоо_абал=(int)абал_маани;return 0;}
uintptr_t 보드원격대기(uintptr_t абал_маани){셸대기중=абал_маани!=0;return 0;}
static int Даярдоо_сырты(void) {
    if(듣는곳>=0)return 0;
    if(!Контекст_маани){
        assh_status_t Ката=assh_context_create(&Контекст_маани,ASSH_SERVER,Даярдоо_эс,0,&난수기,0);
        if(Ката)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *ыкма_режим[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Ката=assh_algo_register(Контекст_маани,ASSH_SAFETY_WEAK,ыкма_режим);
        if(!Ката)Ката=assh_service_register_va(Контекст_маани,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=түзмөк_ачкыч;
        if(!Ката)Ката=assh_key_load(Контекст_маани,assh_context_keys(Контекст_маани),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(түзмөк_ачкыч));
        if(Ката){진단("SSH init error ",Ката);assh_context_release(Контекст_маани);Контекст_маани=0;return -5;}
    }
    int порт_маани=통신끝점만들기(1);if(порт_маани<0)return порт_маани;통신주소재사용(порт_маани);
    int 결과=망주소묶기(порт_маани,0,22);if(!결과)결과=연결기다리기(порт_маани);
    if(결과<0){жабуу_Желе(порт_маани);return 결과;}듣는곳=порт_маани;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t Аракети) {
    if(종류==1)return(uint32_t)башкаруу_алыскы_дисплей(Аракети);
    if(Аракети==0){жабуу_туташуу();if(듣는곳>=0)жабуу_Желе(듣는곳);듣는곳=-1;return 0;}
    if(Аракети==1){жүктөө_ката=Даярдоо_сырты();return(uint32_t)жүктөө_ката;}
    return(uint32_t)(듣는곳>=0?1:жүктөө_ката);
}
void Даярдоо_алыскы(void){жүктөө_ката=Даярдоо_сырты();башкаруу_алыскы_дисплей(1);}
static int 같은말(const struct assh_cbuffer_s *берилмелер,const char *Сөз_СМС) {
    size_t узундук_маани=strlen(Сөз_СМС);return берилмелер->size==узундук_маани&&!memcmp(берилмелер->data,Сөз_СМС,узундук_маани);
}
static int 터미널요청(const struct assh_cbuffer_s *берилмелер) {
    if(берилмелер->size<24)return 0;
    const unsigned char *자료위치=берилмелер->data;unsigned узундук_маани=assh_load_u32(자료위치);
    if(узундук_маани>128||берилмелер->size<узундук_маани+24)return 0;
    unsigned режим_маани=assh_load_u32(자료위치+4+узундук_маани+16);
    return режим_маани<=2048&&берилмелер->size==узундук_маани+24+режим_маани;
}
static void 요청처리(struct assh_event_request_s *окуя) {
    if(!인증됨||окуя->ch!=канал_киргизме_жазуу||!канал_киргизме_жазуу)return;
    if(같은말(&окуя->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&окуя->rq_data))окуя->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&окуя->type,"window-change")) {
        if(셸시작됨&&окуя->rq_data.size==16)окуя->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *Команда=0;unsigned узундук_маани=0;
    if(같은말(&окуя->type,"exec")) {
        if(окуя->rq_data.size<4)return;
        узундук_маани=assh_load_u32(окуя->rq_data.data);
        if(!узундук_маани||узундук_маани>2048||окуя->rq_data.size!=узундук_маани+4)return;
        Команда=окуя->rq_data.data+4;
        for(unsigned 순번=0;순번<узундук_маани;순번++)if(!Команда[순번])return;
        буйрук_түрү=1;
    }else if(!같은말(&окуя->type,"shell")||окуя->rq_data.size)return;
    if(sizeof(입력줄)-입력수<узундук_маани+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(узундук_маани)원격입력넣기(Команда,узундук_маани);원격입력넣기(&끝,1);
    셸시작됨=1;окуя->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!буйрук_түрү){const char *readme_файл_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*readme_файл_eb81d7d9)원격출력(*readme_файл_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(бирдей_маани<0){if(지금<재접속시각)return;бирдей_маани=망연결받기(듣는곳);if(бирдей_маани<0)return;
        접속시각=지금;assh_status_t Ката=assh_session_create(Контекст_маани,&туташуу_e05f319b);
        if(Ката){туташуу_e05f319b=0;진단("SSH session error ",Ката);жабуу_туташуу();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){жабуу_туташуу();return;}
    if(канал_киргизме_жазуу&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Ката=assh_channel_data(канал_киргизме_жазуу,출력줄+출력앞,&수);
            if(!Ката){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Ката!=ASSH_NO_DATA){жабуу_туташуу();return;}
        }
        if(аяктоо_абал>=0&&!출력수){unsigned char абал_маани[4];assh_store_u32(абал_маани,(uint32_t)аяктоо_абал);
            if(assh_request(туташуу_e05f319b,канал_киргизме_жазуу,"exit-status",11,абал_маани,4,0)||assh_channel_eof(канал_киргизме_жазуу)||assh_channel_close(канал_киргизме_жазуу)) {жабуу_туташуу();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned ЫРААТТУУЛУК_маани=0;ЫРААТТУУЛУК_маани<16;ЫРААТТУУЛУК_маани++) {
        struct assh_event_s окуя;
        if(!assh_event_get(туташуу_e05f319b,&окуя,지금/1000)){жабуу_туташуу();return;}
        assh_status_t Ката=ASSH_OK;int 쉬기=0,끊기=0;
        switch(окуя.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(бирдей_маани,окуя.transport.read.buf.data,окуя.transport.read.buf.size);
            if(수>0)окуя.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(бирдей_маани,окуя.transport.write.buf.data,окуя.transport.write.buf.size);
            if(수>0)окуя.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            окуя.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(окуя.userauth_server.methods.retries>3)окуя.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *берилмелер=&окуя.userauth_server.password;
            if(같은말(&берилмелер->username,"user")&&берилмелер->password.size<=256&&!берилмелер->new_password.size) {
                unsigned char жыйынтык_маани[32];алыскы_жыйынтык(берилмелер->password.data,берилмелер->password.size,жыйынтык_маани);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=жыйынтык_маани[순번]^сырты_жашыруун_сөз_жыйынтык[순번];memset(жыйынтык_маани,0,32);
                if(!차이)берилмелер->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *берилмелер=&окуя.connection.channel_open;
            if(인증됨&&!канал_киргизме_жазуу&&셸대기중&&같은말(&берилмелер->type,"session")&&!берилмелер->rq_data.size) {
                берилмелер->reply=ASSH_CONNECTION_REPLY_SUCCESS;берилмелер->pkt_size=4096;
                берилмелер->win_size=-1;канал_киргизме_жазуу=берилмелер->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&окуя.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *берилмелер=&окуя.connection.channel_data;
            if(!셸시작됨||берилмелер->ch!=канал_киргизме_жазуу||берилмелер->ext){끊기=1;break;}
            unsigned 수=берилмелер->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(берилмелер->data.data[순번]==4){аяктоо_абал=0;수=순번;берилмелер->transferred=берилмелер->data.size;break;}
            원격입력넣기(берилмелер->data.data,수);if(!берилмелер->transferred)берилмелер->transferred=수;
            if(!수&&аяктоо_абал<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: канал_киргизме_жазуу=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",окуя.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(туташуу_e05f319b,&окуя,Ката);
        if(끊기){жабуу_туташуу();return;}if(쉬기)return;
    }
}
