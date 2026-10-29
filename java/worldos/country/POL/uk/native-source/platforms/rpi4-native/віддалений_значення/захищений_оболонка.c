/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "віддалений_значення.h"
#include "криптографія_опора.h"
#include "Профіль.h"
#include "../мережа_Стіс/мережа_Стіс.h"
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
static struct assh_context_s *문맥;
static struct assh_session_s *зв_язок_e05f319b;
static struct assh_channel_s *Канал_запис;
static int Слухаю_учасник=-1,точка_значення=-1,인증됨,셸시작됨,команда_Тип,завершити_виклик_Стан=-1,닫을예정,завантаження_помилка,оболонка_Чекаю;
static uintptr_t зв_язок_час,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Ігри_в_слова_Текст,unsigned значення) {
    while(*Ігри_в_слова_Текст)보드글자쓰기(*Ігри_в_слова_Текст++);
    char цифра_значення[12];unsigned 수=0;do{цифра_значення[수++]='0'+значення%10;значення/=10;}while(значення);
    while(수)보드글자쓰기(цифра_значення[--수]);보드글자쓰기(10);
}
static assh_status_t Готувати_Пам_ять(void *дані,void **Адреса,size_t Розмір,enum assh_alloc_type_e 종류) {
    (void)дані;(void)종류;
    if(!Розмір){випуск_віддалений(*Адреса);*Адреса=0;return ASSH_OK;}
    void *새주소=원격재할당(*Адреса,Розмір);
    if(!새주소)return ASSH_ERR_MEM;*Адреса=새주소;return ASSH_OK;
}
static assh_status_t Готувати_випадковий(struct assh_context_s *дані,const struct assh_buffer_s *початкове_значення) {
    (void)дані;(void)початкове_значення;unsigned char випробування[32];int результат=віддалений_випадковий(випробування,sizeof(випробування));memset(випробування,0,sizeof(випробування));
    return результат?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *дані,uint8_t *результат,size_t 길이,uint_fast8_t 종류) {
    (void)дані;(void)종류;if(길이>65536)return ASSH_ERR_CRYPTO;
    return віддалений_випадковий(результат,길이)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void випадковий_завершити_виклик(struct assh_context_s *дані){(void)дані;}
static const struct assh_prng_s випадковий_генератор={Готувати_випадковий,난수받기,випадковий_завершити_виклик};
static void Закрити_зв_язок(void) {
    인증됨=셸시작됨=0;Канал_запис=0;
    if(зв_язок_e05f319b)assh_session_release(зв_язок_e05f319b);зв_язок_e05f319b=0;
    if(точка_значення>=0)Закрити_мережа(точка_значення);точка_значення=-1;команда_Тип=0;завершити_виклик_Стан=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *дані,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=дані[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int символ_значення_068c2631=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return символ_значення_068c2631;
}
void 원격출력(unsigned char символ_значення_068c2631) {
    if(!셸시작됨||닫을예정)return;
    unsigned додавати_режим=символ_значення_068c2631==10&&이전출력!=13;
    if(출력수+1+додавати_режим>sizeof(출력줄)){닫을예정=2;return;}
    if(додавати_режим)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=символ_значення_068c2631;이전출력=символ_значення_068c2631;
}
uintptr_t Дошка_завершити_виклик_віддалений_команда(uintptr_t Стан_значення){if(셸시작됨&&команда_Тип)завершити_виклик_Стан=(int)Стан_значення;return 0;}
uintptr_t Дошка_віддалений_хвилиноньку_панове(uintptr_t Стан_значення){оболонка_Чекаю=Стан_значення!=0;return 0;}
static int Готувати_оболонка(void) {
    if(Слухаю_учасник>=0)return 0;
    if(!문맥){
        assh_status_t ПОМИЛКА=assh_context_create(&문맥,ASSH_SERVER,Готувати_Пам_ять,0,&випадковий_генератор,0);
        if(ПОМИЛКА)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *метод_режим[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ПОМИЛКА=assh_algo_register(문맥,ASSH_SAFETY_WEAK,метод_режим);
        if(!ПОМИЛКА)ПОМИЛКА=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=пристрій_Ключ;
        if(!ПОМИЛКА)ПОМИЛКА=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(пристрій_Ключ));
        if(ПОМИЛКА){진단("SSH init error ",ПОМИЛКА);assh_context_release(문맥);문맥=0;return -5;}
    }
    int порт_значення=Створення_сокет_учасник(1);if(порт_значення<0)return порт_значення;통신주소재사용(порт_значення);
    int результат=망주소묶기(порт_значення,0,22);if(!результат)результат=연결기다리기(порт_значення);
    if(результат<0){Закрити_мережа(порт_значення);return результат;}Слухаю_учасник=порт_значення;return 0;
}
uintptr_t Дошка_віддалене_керування(uintptr_t 종류,uintptr_t Дія) {
    if(종류==1)return(uint32_t)керування_віддалений_дисплей(Дія);
    if(Дія==0){Закрити_зв_язок();if(Слухаю_учасник>=0)Закрити_мережа(Слухаю_учасник);Слухаю_учасник=-1;return 0;}
    if(Дія==1){завантаження_помилка=Готувати_оболонка();return(uint32_t)завантаження_помилка;}
    return(uint32_t)(Слухаю_учасник>=0?1:завантаження_помилка);
}
void Готувати_віддалений(void){завантаження_помилка=Готувати_оболонка();керування_віддалений_дисплей(1);}
static int 같은말(const struct assh_cbuffer_s *дані,const char *Ігри_в_слова_Текст) {
    size_t 길이=strlen(Ігри_в_слова_Текст);return дані->size==길이&&!memcmp(дані->data,Ігри_в_слова_Текст,길이);
}
static int Термінал_запит(const struct assh_cbuffer_s *дані) {
    if(дані->size<24)return 0;
    const unsigned char *дані_посада=дані->data;unsigned 길이=assh_load_u32(дані_посада);
    if(길이>128||дані->size<길이+24)return 0;
    unsigned режим_значення=assh_load_u32(дані_посада+4+길이+16);
    return режим_значення<=2048&&дані->size==길이+24+режим_значення;
}
static void маркер_запит(struct assh_event_request_s *Подія) {
    if(!인증됨||Подія->ch!=Канал_запис||!Канал_запис)return;
    if(같은말(&Подія->type,"pty-req")) {
        if(!셸시작됨&&Термінал_запит(&Подія->rq_data))Подія->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Подія->type,"window-change")) {
        if(셸시작됨&&Подія->rq_data.size==16)Подія->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!оболонка_Чекаю)return;
    const unsigned char *команда=0;unsigned 길이=0;
    if(같은말(&Подія->type,"exec")) {
        if(Подія->rq_data.size<4)return;
        길이=assh_load_u32(Подія->rq_data.data);
        if(!길이||길이>2048||Подія->rq_data.size!=길이+4)return;
        команда=Подія->rq_data.data+4;
        for(unsigned 순번=0;순번<길이;순번++)if(!команда[순번])return;
        команда_Тип=1;
    }else if(!같은말(&Подія->type,"shell")||Подія->rq_data.size)return;
    if(sizeof(입력줄)-입력수<길이+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(길이)원격입력넣기(команда,길이);원격입력넣기(&끝,1);
    셸시작됨=1;Подія->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!команда_Тип){const char *файл_Readme_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*файл_Readme_eb81d7d9)원격출력(*файл_Readme_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Слухаю_учасник<0)return;
    uintptr_t ЗАРАЗ_значення=보드밀리초();
    if(точка_значення<0){if(ЗАРАЗ_значення<재접속시각)return;точка_значення=망연결받기(Слухаю_учасник);if(точка_значення<0)return;
        зв_язок_час=ЗАРАЗ_значення;assh_status_t ПОМИЛКА=assh_session_create(문맥,&зв_язок_e05f319b);
        if(ПОМИЛКА){зв_язок_e05f319b=0;진단("SSH session error ",ПОМИЛКА);Закрити_зв_язок();return;}}
    if((!인증됨&&ЗАРАЗ_значення-зв_язок_час>30000)||닫을예정==2||(닫을예정&&ЗАРАЗ_значення>=닫는시각)){Закрити_зв_язок();return;}
    if(Канал_запис&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ПОМИЛКА=assh_channel_data(Канал_запис,출력줄+출력앞,&수);
            if(!ПОМИЛКА){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ПОМИЛКА!=ASSH_NO_DATA){Закрити_зв_язок();return;}
        }
        if(завершити_виклик_Стан>=0&&!출력수){unsigned char Стан_значення[4];assh_store_u32(Стан_значення,(uint32_t)завершити_виклик_Стан);
            if(assh_request(зв_язок_e05f319b,Канал_запис,"exit-status",11,Стан_значення,4,0)||assh_channel_eof(Канал_запис)||assh_channel_close(Канал_запис)) {Закрити_зв_язок();return;}
            닫을예정=1;닫는시각=ЗАРАЗ_значення+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s Подія;
        if(!assh_event_get(зв_язок_e05f319b,&Подія,ЗАРАЗ_значення/1000)){Закрити_зв_язок();return;}
        assh_status_t ПОМИЛКА=ASSH_OK;int 쉬기=0,від_єднати_учасник=0;
        switch(Подія.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(точка_значення,Подія.transport.read.buf.data,Подія.transport.read.buf.size);
            if(수>0)Подія.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else від_єднати_учасник=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(точка_значення,Подія.transport.write.buf.data,Подія.transport.write.buf.size);
            if(수>0)Подія.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else від_єднати_учасник=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Подія.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Подія.userauth_server.methods.retries>3)Подія.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *дані=&Подія.userauth_server.password;
            if(같은말(&дані->username,"user")&&дані->password.size<=256&&!дані->new_password.size) {
                unsigned char зведення_значення[32];віддалений_зведення(дані->password.data,дані->password.size,зведення_значення);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=зведення_значення[순번]^оболонка_пароль_зведення[순번];memset(зведення_значення,0,32);
                if(!차이)дані->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *дані=&Подія.connection.channel_open;
            if(인증됨&&!Канал_запис&&оболонка_Чекаю&&같은말(&дані->type,"session")&&!дані->rq_data.size) {
                дані->reply=ASSH_CONNECTION_REPLY_SUCCESS;дані->pkt_size=4096;
                дані->win_size=-1;Канал_запис=дані->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: маркер_запит(&Подія.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *дані=&Подія.connection.channel_data;
            if(!셸시작됨||дані->ch!=Канал_запис||дані->ext){від_єднати_учасник=1;break;}
            unsigned 수=дані->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(дані->data.data[순번]==4){завершити_виклик_Стан=0;수=순번;дані->transferred=дані->data.size;break;}
            원격입력넣기(дані->data.data,수);if(!дані->transferred)дані->transferred=수;
            if(!수&&завершити_виклик_Стан<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Канал_запис=0;셸시작됨=0;닫을예정=1;닫는시각=ЗАРАЗ_значення+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Подія.session.error.code);від_єднати_учасник=1;break;
        case ASSH_EVENT_DISCONNECT: від_єднати_учасник=1;break;
        default: break;
        }
        assh_event_done(зв_язок_e05f319b,&Подія,ПОМИЛКА);
        if(від_єднати_учасник){Закрити_зв_язок();return;}if(쉬기)return;
    }
}
