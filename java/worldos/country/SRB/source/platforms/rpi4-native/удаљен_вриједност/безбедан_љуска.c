/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "удаљен_вриједност.h"
#include "암호기반.h"
#include "Профил.h"
#include "../Мрежа_комплет/Мрежа_комплет.h"
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
static struct assh_context_s *Контекст_вриједност;
static struct assh_session_s *веза_e05f319b;
static struct assh_channel_s *Канал_унос;
static int Слушање_крајња_тачка=-1,상대=-1,인증됨,셸시작됨,команда_тип,завршити_стање=-1,닫을예정,покретање_грешка,љуска_Чекам;
static uintptr_t веза_време,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Укрштенице_Текст,unsigned вриједност) {
    while(*Укрштенице_Текст)보드글자쓰기(*Укрштенице_Текст++);
    char цифра_вриједност[12];unsigned 수=0;do{цифра_вриједност[수++]='0'+вриједност%10;вриједност/=10;}while(вриједност);
    while(수)보드글자쓰기(цифра_вриједност[--수]);보드글자쓰기(10);
}
static assh_status_t Припремити_Меморија(void *подаци,void **адреса,size_t Величина,enum assh_alloc_type_e 종류) {
    (void)подаци;(void)종류;
    if(!Величина){издање_удаљен(*адреса);*адреса=0;return ASSH_OK;}
    void *새주소=원격재할당(*адреса,Величина);
    if(!새주소)return ASSH_ERR_MEM;*адреса=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *подаци,const struct assh_buffer_s *почетна_вредност) {
    (void)подаци;(void)почетна_вредност;unsigned char 시험[32];int ИСХОД=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return ИСХОД?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *подаци,uint8_t *ИСХОД,size_t дужина_вриједност,uint_fast8_t 종류) {
    (void)подаци;(void)종류;if(дужина_вриједност>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(ИСХОД,дужина_вриједност)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *подаци){(void)подаци;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void затварање_веза(void) {
    인증됨=셸시작됨=0;Канал_унос=0;
    if(веза_e05f319b)assh_session_release(веза_e05f319b);веза_e05f319b=0;
    if(상대>=0)затварање_Мрежа(상대);상대=-1;команда_тип=0;завршити_стање=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *подаци,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=подаци[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int знак_вриједност=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return знак_вриједност;
}
void 원격출력(unsigned char знак_вриједност) {
    if(!셸시작됨||닫을예정)return;
    unsigned додати_мод=знак_вриједност==10&&이전출력!=13;
    if(출력수+1+додати_мод>sizeof(출력줄)){닫을예정=2;return;}
    if(додати_мод)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=знак_вриједност;이전출력=знак_вриједност;
}
uintptr_t Табла_завршити_удаљен_команда(uintptr_t стање_вриједност){if(셸시작됨&&команда_тип)завршити_стање=(int)стање_вриједност;return 0;}
uintptr_t Табла_удаљен_чекај(uintptr_t стање_вриједност){љуска_Чекам=стање_вриједност!=0;return 0;}
static int Припремити_љуска(void) {
    if(Слушање_крајња_тачка>=0)return 0;
    if(!Контекст_вриједност){
        assh_status_t ГРЕШКА=assh_context_create(&Контекст_вриједност,ASSH_SERVER,Припремити_Меморија,0,&난수기,0);
        if(ГРЕШКА)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *метода_мод[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ГРЕШКА=assh_algo_register(Контекст_вриједност,ASSH_SAFETY_WEAK,метода_мод);
        if(!ГРЕШКА)ГРЕШКА=assh_service_register_va(Контекст_вриједност,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=уређај_Кључ;
        if(!ГРЕШКА)ГРЕШКА=assh_key_load(Контекст_вриједност,assh_context_keys(Контекст_вриједност),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(уређај_Кључ));
        if(ГРЕШКА){진단("SSH init error ",ГРЕШКА);assh_context_release(Контекст_вриједност);Контекст_вриједност=0;return -5;}
    }
    int порт_вриједност=통신끝점만들기(1);if(порт_вриједност<0)return порт_вриједност;통신주소재사용(порт_вриједност);
    int ИСХОД=망주소묶기(порт_вриједност,0,22);if(!ИСХОД)ИСХОД=연결기다리기(порт_вриједност);
    if(ИСХОД<0){затварање_Мрежа(порт_вриједност);return ИСХОД;}Слушање_крајња_тачка=порт_вриједност;return 0;
}
uintptr_t Табла_даљинска_контрола(uintptr_t 종류,uintptr_t радња) {
    if(종류==1)return(uint32_t)контрола_удаљен_екран(радња);
    if(радња==0){затварање_веза();if(Слушање_крајња_тачка>=0)затварање_Мрежа(Слушање_крајња_тачка);Слушање_крајња_тачка=-1;return 0;}
    if(радња==1){покретање_грешка=Припремити_љуска();return(uint32_t)покретање_грешка;}
    return(uint32_t)(Слушање_крајња_тачка>=0?1:покретање_грешка);
}
void Припремити_удаљен(void){покретање_грешка=Припремити_љуска();контрола_удаљен_екран(1);}
static int 같은말(const struct assh_cbuffer_s *подаци,const char *Укрштенице_Текст) {
    size_t дужина_вриједност=strlen(Укрштенице_Текст);return подаци->size==дужина_вриједност&&!memcmp(подаци->data,Укрштенице_Текст,дужина_вриједност);
}
static int Терминал_захтев(const struct assh_cbuffer_s *подаци) {
    if(подаци->size<24)return 0;
    const unsigned char *подаци_позиција=подаци->data;unsigned дужина_вриједност=assh_load_u32(подаци_позиција);
    if(дужина_вриједност>128||подаци->size<дужина_вриједност+24)return 0;
    unsigned мод_вриједност=assh_load_u32(подаци_позиција+4+дужина_вриједност+16);
    return мод_вриједност<=2048&&подаци->size==дужина_вриједност+24+мод_вриједност;
}
static void хватиште_захтев(struct assh_event_request_s *Догађај) {
    if(!인증됨||Догађај->ch!=Канал_унос||!Канал_унос)return;
    if(같은말(&Догађај->type,"pty-req")) {
        if(!셸시작됨&&Терминал_захтев(&Догађај->rq_data))Догађај->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Догађај->type,"window-change")) {
        if(셸시작됨&&Догађај->rq_data.size==16)Догађај->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!љуска_Чекам)return;
    const unsigned char *Наредба=0;unsigned дужина_вриједност=0;
    if(같은말(&Догађај->type,"exec")) {
        if(Догађај->rq_data.size<4)return;
        дужина_вриједност=assh_load_u32(Догађај->rq_data.data);
        if(!дужина_вриједност||дужина_вриједност>2048||Догађај->rq_data.size!=дужина_вриједност+4)return;
        Наредба=Догађај->rq_data.data+4;
        for(unsigned 순번=0;순번<дужина_вриједност;순번++)if(!Наредба[순번])return;
        команда_тип=1;
    }else if(!같은말(&Догађај->type,"shell")||Догађај->rq_data.size)return;
    if(sizeof(입력줄)-입력수<дужина_вриједност+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(дужина_вриједност)원격입력넣기(Наредба,дужина_вриједност);원격입력넣기(&끝,1);
    셸시작됨=1;Догађај->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!команда_тип){const char *Прочитај_ме_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*Прочитај_ме_eb81d7d9)원격출력(*Прочитај_ме_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Слушање_крајња_тачка<0)return;
    uintptr_t САДА_вриједност=보드밀리초();
    if(상대<0){if(САДА_вриједност<재접속시각)return;상대=망연결받기(Слушање_крајња_тачка);if(상대<0)return;
        веза_време=САДА_вриједност;assh_status_t ГРЕШКА=assh_session_create(Контекст_вриједност,&веза_e05f319b);
        if(ГРЕШКА){веза_e05f319b=0;진단("SSH session error ",ГРЕШКА);затварање_веза();return;}}
    if((!인증됨&&САДА_вриједност-веза_време>30000)||닫을예정==2||(닫을예정&&САДА_вриједност>=닫는시각)){затварање_веза();return;}
    if(Канал_унос&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ГРЕШКА=assh_channel_data(Канал_унос,출력줄+출력앞,&수);
            if(!ГРЕШКА){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ГРЕШКА!=ASSH_NO_DATA){затварање_веза();return;}
        }
        if(завршити_стање>=0&&!출력수){unsigned char стање_вриједност[4];assh_store_u32(стање_вриједност,(uint32_t)завршити_стање);
            if(assh_request(веза_e05f319b,Канал_унос,"exit-status",11,стање_вриједност,4,0)||assh_channel_eof(Канал_унос)||assh_channel_close(Канал_унос)) {затварање_веза();return;}
            닫을예정=1;닫는시각=САДА_вриједност+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s Догађај;
        if(!assh_event_get(веза_e05f319b,&Догађај,САДА_вриједност/1000)){затварање_веза();return;}
        assh_status_t ГРЕШКА=ASSH_OK;int 쉬기=0,прекинути_везу_крајња_тачка=0;
        switch(Догађај.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(상대,Догађај.transport.read.buf.data,Догађај.transport.read.buf.size);
            if(수>0)Догађај.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else прекинути_везу_крајња_тачка=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(상대,Догађај.transport.write.buf.data,Догађај.transport.write.buf.size);
            if(수>0)Догађај.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else прекинути_везу_крајња_тачка=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Догађај.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Догађај.userauth_server.methods.retries>3)Догађај.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *подаци=&Догађај.userauth_server.password;
            if(같은말(&подаци->username,"user")&&подаци->password.size<=256&&!подаци->new_password.size) {
                unsigned char резиме_вриједност[32];удаљен_резиме(подаци->password.data,подаци->password.size,резиме_вриједност);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=резиме_вриједност[순번]^љуска_лозинка_резиме[순번];memset(резиме_вриједност,0,32);
                if(!차이)подаци->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *подаци=&Догађај.connection.channel_open;
            if(인증됨&&!Канал_унос&&љуска_Чекам&&같은말(&подаци->type,"session")&&!подаци->rq_data.size) {
                подаци->reply=ASSH_CONNECTION_REPLY_SUCCESS;подаци->pkt_size=4096;
                подаци->win_size=-1;Канал_унос=подаци->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: хватиште_захтев(&Догађај.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *подаци=&Догађај.connection.channel_data;
            if(!셸시작됨||подаци->ch!=Канал_унос||подаци->ext){прекинути_везу_крајња_тачка=1;break;}
            unsigned 수=подаци->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(подаци->data.data[순번]==4){завршити_стање=0;수=순번;подаци->transferred=подаци->data.size;break;}
            원격입력넣기(подаци->data.data,수);if(!подаци->transferred)подаци->transferred=수;
            if(!수&&завршити_стање<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Канал_унос=0;셸시작됨=0;닫을예정=1;닫는시각=САДА_вриједност+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Догађај.session.error.code);прекинути_везу_крајња_тачка=1;break;
        case ASSH_EVENT_DISCONNECT: прекинути_везу_крајња_тачка=1;break;
        default: break;
        }
        assh_event_done(веза_e05f319b,&Догађај,ГРЕШКА);
        if(прекинути_везу_крајња_тачка){затварање_веза();return;}if(쉬기)return;
    }
}
