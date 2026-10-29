/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "читтәге_VALUE.h"
#include "암호기반.h"
#include "Профиль.h"
#include "../Челтәр_Стәк/Челтәр_Стәк.h"
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
static struct assh_context_s *Контекст_VALUE;
static struct assh_session_s *тоташу_e05f319b;
static struct assh_channel_s *канал_кертү;
static int 듣는곳=-1,тиңдәш_VALUE=-1,인증됨,셸시작됨,команда_TYPE,тәмамлау_халәт=-1,닫을예정,йөкләү_хата,셸대기중;
static uintptr_t тоташу_TIME,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_СМС,unsigned VALUE) {
    while(*Word_СМС)보드글자쓰기(*Word_СМС++);
    char сан_VALUE[12];unsigned 수=0;do{сан_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(сан_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Әзерләү_Хәтер(void *мәгълүмат,void **адрес,size_t үлчәмен_үзгәртү,enum assh_alloc_type_e 종류) {
    (void)мәгълүмат;(void)종류;
    if(!үлчәмен_үзгәртү){Чыгарылыш_читтәге(*адрес);*адрес=0;return ASSH_OK;}
    void *새주소=원격재할당(*адрес,үлчәмен_үзгәртү);
    if(!새주소)return ASSH_ERR_MEM;*адрес=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *мәгълүмат,const struct assh_buffer_s *Башланма_сан_VALUE) {
    (void)мәгълүмат;(void)Башланма_сан_VALUE;unsigned char 시험[32];int үлчәм=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return үлчәм?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *мәгълүмат,uint8_t *үлчәм,size_t озынлык_VALUE,uint_fast8_t 종류) {
    (void)мәгълүмат;(void)종류;if(озынлык_VALUE>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(үлчәм,озынлык_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *мәгълүмат){(void)мәгълүмат;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void чик_тоташу(void) {
    인증됨=셸시작됨=0;канал_кертү=0;
    if(тоташу_e05f319b)assh_session_release(тоташу_e05f319b);тоташу_e05f319b=0;
    if(тиңдәш_VALUE>=0)чик_Челтәр(тиңдәш_VALUE);тиңдәш_VALUE=-1;команда_TYPE=0;тәмамлау_халәт=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *мәгълүмат,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=мәгълүмат[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int символ_VALUE_068c2631=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return символ_VALUE_068c2631;
}
void 원격출력(unsigned char символ_VALUE_068c2631) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=символ_VALUE_068c2631==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=символ_VALUE_068c2631;이전출력=символ_VALUE_068c2631;
}
uintptr_t такта_тәмамлау_читтәге_команда(uintptr_t халәт_VALUE){if(셸시작됨&&команда_TYPE)тәмамлау_халәт=(int)халәт_VALUE;return 0;}
uintptr_t 보드원격대기(uintptr_t халәт_VALUE){셸대기중=халәт_VALUE!=0;return 0;}
static int Әзерләү_тышча(void) {
    if(듣는곳>=0)return 0;
    if(!Контекст_VALUE){
        assh_status_t Хата=assh_context_create(&Контекст_VALUE,ASSH_SERVER,Әзерләү_Хәтер,0,&난수기,0);
        if(Хата)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *ысул_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Хата=assh_algo_register(Контекст_VALUE,ASSH_SAFETY_WEAK,ысул_MODE);
        if(!Хата)Хата=assh_service_register_va(Контекст_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=мобиль_ачкыч;
        if(!Хата)Хата=assh_key_load(Контекст_VALUE,assh_context_keys(Контекст_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(мобиль_ачкыч));
        if(Хата){진단("SSH init error ",Хата);assh_context_release(Контекст_VALUE);Контекст_VALUE=0;return -5;}
    }
    int порт_VALUE=통신끝점만들기(1);if(порт_VALUE<0)return порт_VALUE;통신주소재사용(порт_VALUE);
    int үлчәм=망주소묶기(порт_VALUE,0,22);if(!үлчәм)үлчәм=연결기다리기(порт_VALUE);
    if(үлчәм<0){чик_Челтәр(порт_VALUE);return үлчәм;}듣는곳=порт_VALUE;return 0;
}
uintptr_t такта_читтән_идарә(uintptr_t 종류,uintptr_t Гамәл) {
    if(종류==1)return(uint32_t)идарә_читтәге_дисплей(Гамәл);
    if(Гамәл==0){чик_тоташу();if(듣는곳>=0)чик_Челтәр(듣는곳);듣는곳=-1;return 0;}
    if(Гамәл==1){йөкләү_хата=Әзерләү_тышча();return(uint32_t)йөкләү_хата;}
    return(uint32_t)(듣는곳>=0?1:йөкләү_хата);
}
void Әзерләү_читтәге(void){йөкләү_хата=Әзерләү_тышча();идарә_читтәге_дисплей(1);}
static int 같은말(const struct assh_cbuffer_s *мәгълүмат,const char *Word_СМС) {
    size_t озынлык_VALUE=strlen(Word_СМС);return мәгълүмат->size==озынлык_VALUE&&!memcmp(мәгълүмат->data,Word_СМС,озынлык_VALUE);
}
static int 터미널요청(const struct assh_cbuffer_s *мәгълүмат) {
    if(мәгълүмат->size<24)return 0;
    const unsigned char *мәгълүмат_урнаштыру=мәгълүмат->data;unsigned озынлык_VALUE=assh_load_u32(мәгълүмат_урнаштыру);
    if(озынлык_VALUE>128||мәгълүмат->size<озынлык_VALUE+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(мәгълүмат_урнаштыру+4+озынлык_VALUE+16);
    return MODE_VALUE<=2048&&мәгълүмат->size==озынлык_VALUE+24+MODE_VALUE;
}
static void 요청처리(struct assh_event_request_s *вакыйга) {
    if(!인증됨||вакыйга->ch!=канал_кертү||!канал_кертү)return;
    if(같은말(&вакыйга->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&вакыйга->rq_data))вакыйга->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&вакыйга->type,"window-change")) {
        if(셸시작됨&&вакыйга->rq_data.size==16)вакыйга->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *команда=0;unsigned озынлык_VALUE=0;
    if(같은말(&вакыйга->type,"exec")) {
        if(вакыйга->rq_data.size<4)return;
        озынлык_VALUE=assh_load_u32(вакыйга->rq_data.data);
        if(!озынлык_VALUE||озынлык_VALUE>2048||вакыйга->rq_data.size!=озынлык_VALUE+4)return;
        команда=вакыйга->rq_data.data+4;
        for(unsigned 순번=0;순번<озынлык_VALUE;순번++)if(!команда[순번])return;
        команда_TYPE=1;
    }else if(!같은말(&вакыйга->type,"shell")||вакыйга->rq_data.size)return;
    if(sizeof(입력줄)-입력수<озынлык_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(озынлык_VALUE)원격입력넣기(команда,озынлык_VALUE);원격입력넣기(&끝,1);
    셸시작됨=1;вакыйга->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!команда_TYPE){const char *Белешмә_файлы_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*Белешмә_файлы_eb81d7d9)원격출력(*Белешмә_файлы_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(тиңдәш_VALUE<0){if(NOW_VALUE<재접속시각)return;тиңдәш_VALUE=망연결받기(듣는곳);if(тиңдәш_VALUE<0)return;
        тоташу_TIME=NOW_VALUE;assh_status_t Хата=assh_session_create(Контекст_VALUE,&тоташу_e05f319b);
        if(Хата){тоташу_e05f319b=0;진단("SSH session error ",Хата);чик_тоташу();return;}}
    if((!인증됨&&NOW_VALUE-тоташу_TIME>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){чик_тоташу();return;}
    if(канал_кертү&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Хата=assh_channel_data(канал_кертү,출력줄+출력앞,&수);
            if(!Хата){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Хата!=ASSH_NO_DATA){чик_тоташу();return;}
        }
        if(тәмамлау_халәт>=0&&!출력수){unsigned char халәт_VALUE[4];assh_store_u32(халәт_VALUE,(uint32_t)тәмамлау_халәт);
            if(assh_request(тоташу_e05f319b,канал_кертү,"exit-status",11,халәт_VALUE,4,0)||assh_channel_eof(канал_кертү)||assh_channel_close(канал_кертү)) {чик_тоташу();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s вакыйга;
        if(!assh_event_get(тоташу_e05f319b,&вакыйга,NOW_VALUE/1000)){чик_тоташу();return;}
        assh_status_t Хата=ASSH_OK;int 쉬기=0,끊기=0;
        switch(вакыйга.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(тиңдәш_VALUE,вакыйга.transport.read.buf.data,вакыйга.transport.read.buf.size);
            if(수>0)вакыйга.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(тиңдәш_VALUE,вакыйга.transport.write.buf.data,вакыйга.transport.write.buf.size);
            if(수>0)вакыйга.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            вакыйга.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(вакыйга.userauth_server.methods.retries>3)вакыйга.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *мәгълүмат=&вакыйга.userauth_server.password;
            if(같은말(&мәгълүмат->username,"user")&&мәгълүмат->password.size<=256&&!мәгълүмат->new_password.size) {
                unsigned char Җыелма_нәтиҗә_VALUE[32];читтәге_Җыелма_нәтиҗә(мәгълүмат->password.data,мәгълүмат->password.size,Җыелма_нәтиҗә_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=Җыелма_нәтиҗә_VALUE[순번]^тышча_серсүз_Җыелма_нәтиҗә[순번];memset(Җыелма_нәтиҗә_VALUE,0,32);
                if(!차이)мәгълүмат->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *мәгълүмат=&вакыйга.connection.channel_open;
            if(인증됨&&!канал_кертү&&셸대기중&&같은말(&мәгълүмат->type,"session")&&!мәгълүмат->rq_data.size) {
                мәгълүмат->reply=ASSH_CONNECTION_REPLY_SUCCESS;мәгълүмат->pkt_size=4096;
                мәгълүмат->win_size=-1;канал_кертү=мәгълүмат->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&вакыйга.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *мәгълүмат=&вакыйга.connection.channel_data;
            if(!셸시작됨||мәгълүмат->ch!=канал_кертү||мәгълүмат->ext){끊기=1;break;}
            unsigned 수=мәгълүмат->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(мәгълүмат->data.data[순번]==4){тәмамлау_халәт=0;수=순번;мәгълүмат->transferred=мәгълүмат->data.size;break;}
            원격입력넣기(мәгълүмат->data.data,수);if(!мәгълүмат->transferred)мәгълүмат->transferred=수;
            if(!수&&тәмамлау_халәт<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: канал_кертү=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",вакыйга.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(тоташу_e05f319b,&вакыйга,Хата);
        if(끊기){чик_тоташу();return;}if(쉬기)return;
    }
}
