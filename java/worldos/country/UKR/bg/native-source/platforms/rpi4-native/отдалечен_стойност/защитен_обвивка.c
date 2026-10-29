/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "отдалечен_стойност.h"
#include "криптография_Поддръжка.h"
#include "Профил.h"
#include "../мрежа_стек/мрежа_стек.h"
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
static struct assh_session_s *връзка_e05f319b;
static struct assh_channel_s *Канал_запис;
static int Слушане_участник=-1,крайно_устройство_стойност=-1,인증됨,셸시작됨,команда_Тип,прекратяване_на_повикването_Състояние=-1,닫을예정,начално_зареждане_на_ОС_грешка,обвивка_Изчакване;
static uintptr_t връзка_час,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Игри_с_думи_Текст,unsigned стойност) {
    while(*Игри_с_думи_Текст)보드글자쓰기(*Игри_с_думи_Текст++);
    char цифра_стойност[12];unsigned 수=0;do{цифра_стойност[수++]='0'+стойност%10;стойност/=10;}while(стойност);
    while(수)보드글자쓰기(цифра_стойност[--수]);보드글자쓰기(10);
}
static assh_status_t Подготвяне_Памет(void *данни,void **адрес,size_t Размер,enum assh_alloc_type_e 종류) {
    (void)данни;(void)종류;
    if(!Размер){издание_отдалечен(*адрес);*адрес=0;return ASSH_OK;}
    void *새주소=원격재할당(*адрес,Размер);
    if(!새주소)return ASSH_ERR_MEM;*адрес=새주소;return ASSH_OK;
}
static assh_status_t Подготвяне_случаен(struct assh_context_s *данни,const struct assh_buffer_s *начална_стойност) {
    (void)данни;(void)начална_стойност;unsigned char 시험[32];int РЕЗУЛТАТ=отдалечен_случаен(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return РЕЗУЛТАТ?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *данни,uint8_t *РЕЗУЛТАТ,size_t 길이,uint_fast8_t 종류) {
    (void)данни;(void)종류;if(길이>65536)return ASSH_ERR_CRYPTO;
    return отдалечен_случаен(РЕЗУЛТАТ,길이)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void случаен_прекратяване_на_повикването(struct assh_context_s *данни){(void)данни;}
static const struct assh_prng_s случаен_генератор={Подготвяне_случаен,난수받기,случаен_прекратяване_на_повикването};
static void затварям_връзка(void) {
    인증됨=셸시작됨=0;Канал_запис=0;
    if(връзка_e05f319b)assh_session_release(връзка_e05f319b);връзка_e05f319b=0;
    if(крайно_устройство_стойност>=0)затварям_мрежа(крайно_устройство_стойност);крайно_устройство_стойност=-1;команда_Тип=0;прекратяване_на_повикването_Състояние=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *данни,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=данни[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int знак_стойност=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return знак_стойност;
}
void 원격출력(unsigned char знак_стойност) {
    if(!셸시작됨||닫을예정)return;
    unsigned добавям_режим=знак_стойност==10&&이전출력!=13;
    if(출력수+1+добавям_режим>sizeof(출력줄)){닫을예정=2;return;}
    if(добавям_режим)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=знак_стойност;이전출력=знак_стойност;
}
uintptr_t Табло_прекратяване_на_повикването_отдалечен_команда(uintptr_t Състояние_стойност){if(셸시작됨&&команда_Тип)прекратяване_на_повикването_Състояние=(int)Състояние_стойност;return 0;}
uintptr_t Табло_отдалечен_почакай(uintptr_t Състояние_стойност){обвивка_Изчакване=Състояние_стойност!=0;return 0;}
static int Подготвяне_обвивка(void) {
    if(Слушане_участник>=0)return 0;
    if(!문맥){
        assh_status_t ГРЕШКА=assh_context_create(&문맥,ASSH_SERVER,Подготвяне_Памет,0,&случаен_генератор,0);
        if(ГРЕШКА)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *метод_режим[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ГРЕШКА=assh_algo_register(문맥,ASSH_SAFETY_WEAK,метод_режим);
        if(!ГРЕШКА)ГРЕШКА=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=устройство_Ключ;
        if(!ГРЕШКА)ГРЕШКА=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(устройство_Ключ));
        if(ГРЕШКА){진단("SSH init error ",ГРЕШКА);assh_context_release(문맥);문맥=0;return -5;}
    }
    int порт_стойност=통신끝점만들기(1);if(порт_стойност<0)return порт_стойност;통신주소재사용(порт_стойност);
    int РЕЗУЛТАТ=망주소묶기(порт_стойност,0,22);if(!РЕЗУЛТАТ)РЕЗУЛТАТ=연결기다리기(порт_стойност);
    if(РЕЗУЛТАТ<0){затварям_мрежа(порт_стойност);return РЕЗУЛТАТ;}Слушане_участник=порт_стойност;return 0;
}
uintptr_t Табло_отдалечено_управление(uintptr_t 종류,uintptr_t Операция) {
    if(종류==1)return(uint32_t)контрол_отдалечен_дисплей(Операция);
    if(Операция==0){затварям_връзка();if(Слушане_участник>=0)затварям_мрежа(Слушане_участник);Слушане_участник=-1;return 0;}
    if(Операция==1){начално_зареждане_на_ОС_грешка=Подготвяне_обвивка();return(uint32_t)начално_зареждане_на_ОС_грешка;}
    return(uint32_t)(Слушане_участник>=0?1:начално_зареждане_на_ОС_грешка);
}
void Подготвяне_отдалечен(void){начално_зареждане_на_ОС_грешка=Подготвяне_обвивка();контрол_отдалечен_дисплей(1);}
static int 같은말(const struct assh_cbuffer_s *данни,const char *Игри_с_думи_Текст) {
    size_t 길이=strlen(Игри_с_думи_Текст);return данни->size==길이&&!memcmp(данни->data,Игри_с_думи_Текст,길이);
}
static int Терминал_искане(const struct assh_cbuffer_s *данни) {
    if(данни->size<24)return 0;
    const unsigned char *данни_позиция=данни->data;unsigned 길이=assh_load_u32(данни_позиция);
    if(길이>128||данни->size<길이+24)return 0;
    unsigned режим_стойност=assh_load_u32(данни_позиция+4+길이+16);
    return режим_стойност<=2048&&данни->size==길이+24+режим_стойност;
}
static void манипулатор_искане(struct assh_event_request_s *Събитие) {
    if(!인증됨||Събитие->ch!=Канал_запис||!Канал_запис)return;
    if(같은말(&Събитие->type,"pty-req")) {
        if(!셸시작됨&&Терминал_искане(&Събитие->rq_data))Събитие->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Събитие->type,"window-change")) {
        if(셸시작됨&&Събитие->rq_data.size==16)Събитие->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!обвивка_Изчакване)return;
    const unsigned char *Команда=0;unsigned 길이=0;
    if(같은말(&Събитие->type,"exec")) {
        if(Събитие->rq_data.size<4)return;
        길이=assh_load_u32(Събитие->rq_data.data);
        if(!길이||길이>2048||Събитие->rq_data.size!=길이+4)return;
        Команда=Събитие->rq_data.data+4;
        for(unsigned 순번=0;순번<길이;순번++)if(!Команда[순번])return;
        команда_Тип=1;
    }else if(!같은말(&Събитие->type,"shell")||Събитие->rq_data.size)return;
    if(sizeof(입력줄)-입력수<길이+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(길이)원격입력넣기(Команда,길이);원격입력넣기(&끝,1);
    셸시작됨=1;Събитие->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!команда_Тип){const char *안내="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*안내)원격출력(*안내++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Слушане_участник<0)return;
    uintptr_t СЕГА_стойност=보드밀리초();
    if(крайно_устройство_стойност<0){if(СЕГА_стойност<재접속시각)return;крайно_устройство_стойност=망연결받기(Слушане_участник);if(крайно_устройство_стойност<0)return;
        връзка_час=СЕГА_стойност;assh_status_t ГРЕШКА=assh_session_create(문맥,&връзка_e05f319b);
        if(ГРЕШКА){връзка_e05f319b=0;진단("SSH session error ",ГРЕШКА);затварям_връзка();return;}}
    if((!인증됨&&СЕГА_стойност-връзка_час>30000)||닫을예정==2||(닫을예정&&СЕГА_стойност>=닫는시각)){затварям_връзка();return;}
    if(Канал_запис&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ГРЕШКА=assh_channel_data(Канал_запис,출력줄+출력앞,&수);
            if(!ГРЕШКА){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ГРЕШКА!=ASSH_NO_DATA){затварям_връзка();return;}
        }
        if(прекратяване_на_повикването_Състояние>=0&&!출력수){unsigned char Състояние_стойност[4];assh_store_u32(Състояние_стойност,(uint32_t)прекратяване_на_повикването_Състояние);
            if(assh_request(връзка_e05f319b,Канал_запис,"exit-status",11,Състояние_стойност,4,0)||assh_channel_eof(Канал_запис)||assh_channel_close(Канал_запис)) {затварям_връзка();return;}
            닫을예정=1;닫는시각=СЕГА_стойност+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s Събитие;
        if(!assh_event_get(връзка_e05f319b,&Събитие,СЕГА_стойност/1000)){затварям_връзка();return;}
        assh_status_t ГРЕШКА=ASSH_OK;int 쉬기=0,прекъсвам_връзката_участник=0;
        switch(Събитие.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(крайно_устройство_стойност,Събитие.transport.read.buf.data,Събитие.transport.read.buf.size);
            if(수>0)Събитие.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else прекъсвам_връзката_участник=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(крайно_устройство_стойност,Събитие.transport.write.buf.data,Събитие.transport.write.buf.size);
            if(수>0)Събитие.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else прекъсвам_връзката_участник=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Събитие.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Събитие.userauth_server.methods.retries>3)Събитие.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *данни=&Събитие.userauth_server.password;
            if(같은말(&данни->username,"user")&&данни->password.size<=256&&!данни->new_password.size) {
                unsigned char резюме_стойност[32];отдалечен_резюме(данни->password.data,данни->password.size,резюме_стойност);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=резюме_стойност[순번]^обвивка_парола_резюме[순번];memset(резюме_стойност,0,32);
                if(!차이)данни->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *данни=&Събитие.connection.channel_open;
            if(인증됨&&!Канал_запис&&обвивка_Изчакване&&같은말(&данни->type,"session")&&!данни->rq_data.size) {
                данни->reply=ASSH_CONNECTION_REPLY_SUCCESS;данни->pkt_size=4096;
                данни->win_size=-1;Канал_запис=данни->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: манипулатор_искане(&Събитие.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *данни=&Събитие.connection.channel_data;
            if(!셸시작됨||данни->ch!=Канал_запис||данни->ext){прекъсвам_връзката_участник=1;break;}
            unsigned 수=данни->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(данни->data.data[순번]==4){прекратяване_на_повикването_Състояние=0;수=순번;данни->transferred=данни->data.size;break;}
            원격입력넣기(данни->data.data,수);if(!данни->transferred)данни->transferred=수;
            if(!수&&прекратяване_на_повикването_Състояние<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Канал_запис=0;셸시작됨=0;닫을예정=1;닫는시각=СЕГА_стойност+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Събитие.session.error.code);прекъсвам_връзката_участник=1;break;
        case ASSH_EVENT_DISCONNECT: прекъсвам_връзката_участник=1;break;
        default: break;
        }
        assh_event_done(връзка_e05f319b,&Събитие,ГРЕШКА);
        if(прекъсвам_връзката_участник){затварям_връзка();return;}if(쉬기)return;
    }
}
