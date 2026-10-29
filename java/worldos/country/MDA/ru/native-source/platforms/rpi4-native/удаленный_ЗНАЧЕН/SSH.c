/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "удаленный_ЗНАЧЕН.h"
#include "шифрование_опора.h"
#include "Profile.h"
#include "../сеть_стек/сеть_стек.h"
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
static struct assh_context_s *контекст_ЗНАЧЕН;
static struct assh_session_s *контакт_e05f319b;
static struct assh_channel_s *канал_ввод;
static int Слушаю_участник=-1,одноранговый_ЗНАЧЕН=-1,인증됨,셸시작됨,명령형,элемент_Состояние=-1,닫을예정,запуск_ошибка,оболочка_Заждался;
static uintptr_t контакт_ВРЕМЯ,재접속시각,закрытие_ВРЕМЯ;
static unsigned char входные_данные_линия[8192],выход_линия[65536];
static unsigned входные_данные_HEAD,входные_данные_СЧЁТ,выход_HEAD,выход_СЧЁТ,Назад_выход;
static void 진단(const char *Word_SMS,unsigned ЗНАЧЕН) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char цифра_ЗНАЧЕН[12];unsigned 수=0;do{цифра_ЗНАЧЕН[수++]='0'+ЗНАЧЕН%10;ЗНАЧЕН/=10;}while(ЗНАЧЕН);
    while(수)보드글자쓰기(цифра_ЗНАЧЕН[--수]);보드글자쓰기(10);
}
static assh_status_t Подготовить_Память(void *данные,void **АДРЕС,size_t Размер,enum assh_alloc_type_e Вид_ЗНАЧЕН) {
    (void)данные;(void)Вид_ЗНАЧЕН;
    if(!Размер){выпуск_удаленный(*АДРЕС);*АДРЕС=0;return ASSH_OK;}
    void *새주소=원격재할당(*АДРЕС,Размер);
    if(!새주소)return ASSH_ERR_MEM;*АДРЕС=새주소;return ASSH_OK;
}
static assh_status_t Подготовить_случайный(struct assh_context_s *данные,const struct assh_buffer_s *начальное_значение) {
    (void)данные;(void)начальное_значение;unsigned char испытания[32];int результат=удаленный_случайный(испытания,sizeof(испытания));memset(испытания,0,sizeof(испытания));
    return результат?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t чтение_случайный(struct assh_context_s *данные,uint8_t *результат,size_t длина_ЗНАЧЕН,uint_fast8_t Вид_ЗНАЧЕН) {
    (void)данные;(void)Вид_ЗНАЧЕН;if(длина_ЗНАЧЕН>65536)return ASSH_ERR_CRYPTO;
    return удаленный_случайный(результат,длина_ЗНАЧЕН)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void случайный_элемент(struct assh_context_s *данные){(void)данные;}
static const struct assh_prng_s случайный_генератор={Подготовить_случайный,чтение_случайный,случайный_элемент};
static void Close_контакт(void) {
    인증됨=셸시작됨=0;канал_ввод=0;
    if(контакт_e05f319b)assh_session_release(контакт_e05f319b);контакт_e05f319b=0;
    if(одноранговый_ЗНАЧЕН>=0)Close_сеть(одноранговый_ЗНАЧЕН);одноранговый_ЗНАЧЕН=-1;명령형=0;элемент_Состояние=-1;닫을예정=0;
    входные_данные_HEAD=входные_данные_СЧЁТ=выход_HEAD=выход_СЧЁТ=Назад_выход=0;재접속시각=보드밀리초()+250;
}
int канал_удаленный_входные_данные(const unsigned char *данные,unsigned 수) {
    if(수>sizeof(входные_данные_линия)-входные_данные_СЧЁТ)return -11;
    for(unsigned 순번=0;순번<수;순번++)входные_данные_линия[(входные_данные_HEAD+входные_данные_СЧЁТ++)%sizeof(входные_данные_линия)]=данные[순번];return 수;
}
int удаленный_входные_данные(void) {
    if(!входные_данные_СЧЁТ)return -1;int знак_ЗНАЧЕН=входные_данные_линия[входные_данные_HEAD];входные_данные_HEAD=(входные_данные_HEAD+1)%sizeof(входные_данные_линия);входные_данные_СЧЁТ--;return знак_ЗНАЧЕН;
}
void удаленный_выход(unsigned char знак_ЗНАЧЕН) {
    if(!셸시작됨||닫을예정)return;
    unsigned режим_добавления=знак_ЗНАЧЕН==10&&Назад_выход!=13;
    if(выход_СЧЁТ+1+режим_добавления>sizeof(выход_линия)){닫을예정=2;return;}
    if(режим_добавления)выход_линия[(выход_HEAD+выход_СЧЁТ++)%sizeof(выход_линия)]=13;
    выход_линия[(выход_HEAD+выход_СЧЁТ++)%sizeof(выход_линия)]=знак_ЗНАЧЕН;Назад_выход=знак_ЗНАЧЕН;
}
uintptr_t 보드원격명령끝(uintptr_t Состояние_ЗНАЧЕН){if(셸시작됨&&명령형)элемент_Состояние=(int)Состояние_ЗНАЧЕН;return 0;}
uintptr_t Доска_удаленный_минутку(uintptr_t Состояние_ЗНАЧЕН){оболочка_Заждался=Состояние_ЗНАЧЕН!=0;return 0;}
static int Подготовить_оболочка(void) {
    if(Слушаю_участник>=0)return 0;
    if(!контекст_ЗНАЧЕН){
        assh_status_t ошибка=assh_context_create(&контекст_ЗНАЧЕН,ASSH_SERVER,Подготовить_Память,0,&случайный_генератор,0);
        if(ошибка)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *метод_МОДА[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ошибка=assh_algo_register(контекст_ЗНАЧЕН,ASSH_SAFETY_WEAK,метод_МОДА);
        if(!ошибка)ошибка=assh_service_register_va(контекст_ЗНАЧЕН,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *Ключ_материал=устройство_Ключ;
        if(!ошибка)ошибка=assh_key_load(контекст_ЗНАЧЕН,assh_context_keys(контекст_ЗНАЧЕН),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&Ключ_материал,sizeof(устройство_Ключ));
        if(ошибка){진단("SSH init error ",ошибка);assh_context_release(контекст_ЗНАЧЕН);контекст_ЗНАЧЕН=0;return -5;}
    }
    int порт_ЗНАЧЕН=Create_сокет_участник(1);if(порт_ЗНАЧЕН<0)return порт_ЗНАЧЕН;통신주소재사용(порт_ЗНАЧЕН);
    int результат=NET_BIND(порт_ЗНАЧЕН,0,22);if(!результат)результат=NET_ожидать_передачи_данных(порт_ЗНАЧЕН);
    if(результат<0){Close_сеть(порт_ЗНАЧЕН);return результат;}Слушаю_участник=порт_ЗНАЧЕН;return 0;
}
uintptr_t Доска_удаленное_управление(uintptr_t Вид_ЗНАЧЕН,uintptr_t Действие) {
    if(Вид_ЗНАЧЕН==1)return(uint32_t)управление_удаленный_дисплей(Действие);
    if(Действие==0){Close_контакт();if(Слушаю_участник>=0)Close_сеть(Слушаю_участник);Слушаю_участник=-1;return 0;}
    if(Действие==1){запуск_ошибка=Подготовить_оболочка();return(uint32_t)запуск_ошибка;}
    return(uint32_t)(Слушаю_участник>=0?1:запуск_ошибка);
}
void Подготовить_удаленный(void){запуск_ошибка=Подготовить_оболочка();управление_удаленный_дисплей(1);}
static int согласование_Word(const struct assh_cbuffer_s *данные,const char *Word_SMS) {
    size_t длина_ЗНАЧЕН=strlen(Word_SMS);return данные->size==длина_ЗНАЧЕН&&!memcmp(данные->data,Word_SMS,длина_ЗНАЧЕН);
}
static int Терминал_запрос(const struct assh_cbuffer_s *данные) {
    if(данные->size<24)return 0;
    const unsigned char *данные_позиция=данные->data;unsigned длина_ЗНАЧЕН=assh_load_u32(данные_позиция);
    if(длина_ЗНАЧЕН>128||данные->size<длина_ЗНАЧЕН+24)return 0;
    unsigned МОДА_ЗНАЧЕН=assh_load_u32(данные_позиция+4+длина_ЗНАЧЕН+16);
    return МОДА_ЗНАЧЕН<=2048&&данные->size==длина_ЗНАЧЕН+24+МОДА_ЗНАЧЕН;
}
static void маркер_запрос(struct assh_event_request_s *Событие) {
    if(!인증됨||Событие->ch!=канал_ввод||!канал_ввод)return;
    if(согласование_Word(&Событие->type,"pty-req")) {
        if(!셸시작됨&&Терминал_запрос(&Событие->rq_data))Событие->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(согласование_Word(&Событие->type,"window-change")) {
        if(셸시작됨&&Событие->rq_data.size==16)Событие->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!оболочка_Заждался)return;
    const unsigned char *команда=0;unsigned длина_ЗНАЧЕН=0;
    if(согласование_Word(&Событие->type,"exec")) {
        if(Событие->rq_data.size<4)return;
        длина_ЗНАЧЕН=assh_load_u32(Событие->rq_data.data);
        if(!длина_ЗНАЧЕН||длина_ЗНАЧЕН>2048||Событие->rq_data.size!=длина_ЗНАЧЕН+4)return;
        команда=Событие->rq_data.data+4;
        for(unsigned 순번=0;순번<длина_ЗНАЧЕН;순번++)if(!команда[순번])return;
        명령형=1;
    }else if(!согласование_Word(&Событие->type,"shell")||Событие->rq_data.size)return;
    if(sizeof(входные_данные_линия)-входные_данные_СЧЁТ<длина_ЗНАЧЕН+2)return;
    const unsigned char 지움=21,끝=13;
    канал_удаленный_входные_данные(&지움,1);if(длина_ЗНАЧЕН)канал_удаленный_входные_данные(команда,длина_ЗНАЧЕН);канал_удаленный_входные_данные(&끝,1);
    셸시작됨=1;Событие->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!명령형){const char *файл_сведений_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*файл_сведений_eb81d7d9)удаленный_выход(*файл_сведений_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Слушаю_участник<0)return;
    uintptr_t ТДАТА_ЗНАЧЕН=보드밀리초();
    if(одноранговый_ЗНАЧЕН<0){if(ТДАТА_ЗНАЧЕН<재접속시각)return;одноранговый_ЗНАЧЕН=NET_принять(Слушаю_участник);if(одноранговый_ЗНАЧЕН<0)return;
        контакт_ВРЕМЯ=ТДАТА_ЗНАЧЕН;assh_status_t ошибка=assh_session_create(контекст_ЗНАЧЕН,&контакт_e05f319b);
        if(ошибка){контакт_e05f319b=0;진단("SSH session error ",ошибка);Close_контакт();return;}}
    if((!인증됨&&ТДАТА_ЗНАЧЕН-контакт_ВРЕМЯ>30000)||닫을예정==2||(닫을예정&&ТДАТА_ЗНАЧЕН>=закрытие_ВРЕМЯ)){Close_контакт();return;}
    if(канал_ввод&&셸시작됨&&!닫을예정) {
        if(выход_СЧЁТ){size_t 수=sizeof(выход_линия)-выход_HEAD;if(수>выход_СЧЁТ)수=выход_СЧЁТ;if(수>2048)수=2048;
            assh_status_t ошибка=assh_channel_data(канал_ввод,выход_линия+выход_HEAD,&수);
            if(!ошибка){выход_HEAD=(выход_HEAD+수)%sizeof(выход_линия);выход_СЧЁТ-=수;}
            else if(ошибка!=ASSH_NO_DATA){Close_контакт();return;}
        }
        if(элемент_Состояние>=0&&!выход_СЧЁТ){unsigned char Состояние_ЗНАЧЕН[4];assh_store_u32(Состояние_ЗНАЧЕН,(uint32_t)элемент_Состояние);
            if(assh_request(контакт_e05f319b,канал_ввод,"exit-status",11,Состояние_ЗНАЧЕН,4,0)||assh_channel_eof(канал_ввод)||assh_channel_close(канал_ввод)) {Close_контакт();return;}
            닫을예정=1;закрытие_ВРЕМЯ=ТДАТА_ЗНАЧЕН+3000;
        }
    }
    for(unsigned ПОСЛЕД_ЗНАЧЕН=0;ПОСЛЕД_ЗНАЧЕН<16;ПОСЛЕД_ЗНАЧЕН++) {
        struct assh_event_s Событие;
        if(!assh_event_get(контакт_e05f319b,&Событие,ТДАТА_ЗНАЧЕН/1000)){Close_контакт();return;}
        assh_status_t ошибка=ASSH_OK;int 쉬기=0,отключить_участник=0;
        switch(Событие.id) {
        case ASSH_EVENT_READ: {
            int 수=NET_чтение(одноранговый_ЗНАЧЕН,Событие.transport.read.buf.data,Событие.transport.read.buf.size);
            if(수>0)Событие.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else отключить_участник=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=NET_запись(одноранговый_ЗНАЧЕН,Событие.transport.write.buf.data,Событие.transport.write.buf.size);
            if(수>0)Событие.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else отключить_участник=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Событие.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Событие.userauth_server.methods.retries>3)Событие.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *данные=&Событие.userauth_server.password;
            if(согласование_Word(&данные->username,"user")&&данные->password.size<=256&&!данные->new_password.size) {
                unsigned char сводка_ЗНАЧЕН[32];удаленный_сводка(данные->password.data,данные->password.size,сводка_ЗНАЧЕН);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=сводка_ЗНАЧЕН[순번]^оболочка_пароль_сводка[순번];memset(сводка_ЗНАЧЕН,0,32);
                if(!차이)данные->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *данные=&Событие.connection.channel_open;
            if(인증됨&&!канал_ввод&&оболочка_Заждался&&согласование_Word(&данные->type,"session")&&!данные->rq_data.size) {
                данные->reply=ASSH_CONNECTION_REPLY_SUCCESS;данные->pkt_size=4096;
                данные->win_size=-1;канал_ввод=данные->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: маркер_запрос(&Событие.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *данные=&Событие.connection.channel_data;
            if(!셸시작됨||данные->ch!=канал_ввод||данные->ext){отключить_участник=1;break;}
            unsigned 수=данные->data.size;if(수>sizeof(входные_данные_линия)-входные_данные_СЧЁТ)수=sizeof(входные_данные_линия)-входные_данные_СЧЁТ;
            for(unsigned 순번=0;순번<수;순번++)if(данные->data.data[순번]==4){элемент_Состояние=0;수=순번;данные->transferred=данные->data.size;break;}
            канал_удаленный_входные_данные(данные->data.data,수);if(!данные->transferred)данные->transferred=수;
            if(!수&&элемент_Состояние<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: канал_ввод=0;셸시작됨=0;닫을예정=1;закрытие_ВРЕМЯ=ТДАТА_ЗНАЧЕН+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Событие.session.error.code);отключить_участник=1;break;
        case ASSH_EVENT_DISCONNECT: отключить_участник=1;break;
        default: break;
        }
        assh_event_done(контакт_e05f319b,&Событие,ошибка);
        if(отключить_участник){Close_контакт();return;}if(쉬기)return;
    }
}
