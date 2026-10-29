/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "원격.h"
#include "암호기반.h"
#include "Профиль.h"
#include "../желі_Бума/желі_Бума.h"
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
static struct assh_session_s *қосылым_e05f319b;
static struct assh_channel_s *Арна_енгізу;
static int Құлақ_қою_қатысушы=-1,бір_рангілі_мән=-1,인증됨,셸시작됨,пәрмен_Түрі,тоқтату_күй=-1,닫을예정,іске_қосу_қате,қоршам_Күту;
static uintptr_t қосылым_уақыт,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Сөз_Мәтін,unsigned мән) {
    while(*Сөз_Мәтін)보드글자쓰기(*Сөз_Мәтін++);
    char сан_мән[12];unsigned 수=0;do{сан_мән[수++]='0'+мән%10;мән/=10;}while(мән);
    while(수)보드글자쓰기(сан_мән[--수]);보드글자쓰기(10);
}
static assh_status_t Дайындау_Жад(void *деректер,void **мекенжай,size_t Өлшемі,enum assh_alloc_type_e 종류) {
    (void)деректер;(void)종류;
    if(!Өлшемі){원격해제(*мекенжай);*мекенжай=0;return ASSH_OK;}
    void *새주소=원격재할당(*мекенжай,Өлшемі);
    if(!새주소)return ASSH_ERR_MEM;*мекенжай=새주소;return ASSH_OK;
}
static assh_status_t Дайындау_кездейсоқ(struct assh_context_s *деректер,const struct assh_buffer_s *бастапқы_мән) {
    (void)деректер;(void)бастапқы_мән;unsigned char 시험[32];int НӘТИЖЕ=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return НӘТИЖЕ?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *деректер,uint8_t *НӘТИЖЕ,size_t ұзындық_мән,uint_fast8_t 종류) {
    (void)деректер;(void)종류;if(ұзындық_мән>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(НӘТИЖЕ,ұзындық_мән)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void кездейсоқ_тоқтату(struct assh_context_s *деректер){(void)деректер;}
static const struct assh_prng_s кездейсоқ_генератор={Дайындау_кездейсоқ,난수받기,кездейсоқ_тоқтату};
static void Жабу_қосылым(void) {
    인증됨=셸시작됨=0;Арна_енгізу=0;
    if(қосылым_e05f319b)assh_session_release(қосылым_e05f319b);қосылым_e05f319b=0;
    if(бір_рангілі_мән>=0)Жабу_желі(бір_рангілі_мән);бір_рангілі_мән=-1;пәрмен_Түрі=0;тоқтату_күй=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *деректер,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=деректер[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int таңба_мән=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return таңба_мән;
}
void 원격출력(unsigned char таңба_мән) {
    if(!셸시작됨||닫을예정)return;
    unsigned қосу_режим=таңба_мән==10&&이전출력!=13;
    if(출력수+1+қосу_режим>sizeof(출력줄)){닫을예정=2;return;}
    if(қосу_режим)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=таңба_мән;이전출력=таңба_мән;
}
uintptr_t 보드원격명령끝(uintptr_t күй_мән){if(셸시작됨&&пәрмен_Түрі)тоқтату_күй=(int)күй_мән;return 0;}
uintptr_t 보드원격대기(uintptr_t күй_мән){қоршам_Күту=күй_мән!=0;return 0;}
static int Дайындау_қоршам(void) {
    if(Құлақ_қою_қатысушы>=0)return 0;
    if(!문맥){
        assh_status_t Қате=assh_context_create(&문맥,ASSH_SERVER,Дайындау_Жад,0,&кездейсоқ_генератор,0);
        if(Қате)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *әдіс_режим[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Қате=assh_algo_register(문맥,ASSH_SAFETY_WEAK,әдіс_режим);
        if(!Қате)Қате=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=құрылғы_Кілт;
        if(!Қате)Қате=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(құрылғы_Кілт));
        if(Қате){진단("SSH init error ",Қате);assh_context_release(문맥);문맥=0;return -5;}
    }
    int порт_мән=통신끝점만들기(1);if(порт_мән<0)return порт_мән;통신주소재사용(порт_мән);
    int НӘТИЖЕ=망주소묶기(порт_мән,0,22);if(!НӘТИЖЕ)НӘТИЖЕ=연결기다리기(порт_мән);
    if(НӘТИЖЕ<0){Жабу_желі(порт_мән);return НӘТИЖЕ;}Құлақ_қою_қатысушы=порт_мән;return 0;
}
uintptr_t Тақта_көлеңкелі_көшіру(uintptr_t 종류,uintptr_t Әрекет) {
    if(종류==1)return(uint32_t)원격화면제어(Әрекет);
    if(Әрекет==0){Жабу_қосылым();if(Құлақ_қою_қатысушы>=0)Жабу_желі(Құлақ_қою_қатысушы);Құлақ_қою_қатысушы=-1;return 0;}
    if(Әрекет==1){іске_қосу_қате=Дайындау_қоршам();return(uint32_t)іске_қосу_қате;}
    return(uint32_t)(Құлақ_қою_қатысушы>=0?1:іске_қосу_қате);
}
void 원격준비(void){іске_қосу_қате=Дайындау_қоршам();원격화면제어(1);}
static int 같은말(const struct assh_cbuffer_s *деректер,const char *Сөз_Мәтін) {
    size_t ұзындық_мән=strlen(Сөз_Мәтін);return деректер->size==ұзындық_мән&&!memcmp(деректер->data,Сөз_Мәтін,ұзындық_мән);
}
static int 터미널요청(const struct assh_cbuffer_s *деректер) {
    if(деректер->size<24)return 0;
    const unsigned char *деректер_лауазым=деректер->data;unsigned ұзындық_мән=assh_load_u32(деректер_лауазым);
    if(ұзындық_мән>128||деректер->size<ұзындық_мән+24)return 0;
    unsigned режим_мән=assh_load_u32(деректер_лауазым+4+ұзындық_мән+16);
    return режим_мән<=2048&&деректер->size==ұзындық_мән+24+режим_мән;
}
static void 요청처리(struct assh_event_request_s *Оқиға) {
    if(!인증됨||Оқиға->ch!=Арна_енгізу||!Арна_енгізу)return;
    if(같은말(&Оқиға->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&Оқиға->rq_data))Оқиға->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Оқиға->type,"window-change")) {
        if(셸시작됨&&Оқиға->rq_data.size==16)Оқиға->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!қоршам_Күту)return;
    const unsigned char *Команда=0;unsigned ұзындық_мән=0;
    if(같은말(&Оқиға->type,"exec")) {
        if(Оқиға->rq_data.size<4)return;
        ұзындық_мән=assh_load_u32(Оқиға->rq_data.data);
        if(!ұзындық_мән||ұзындық_мән>2048||Оқиға->rq_data.size!=ұзындық_мән+4)return;
        Команда=Оқиға->rq_data.data+4;
        for(unsigned 순번=0;순번<ұзындық_мән;순번++)if(!Команда[순번])return;
        пәрмен_Түрі=1;
    }else if(!같은말(&Оқиға->type,"shell")||Оқиға->rq_data.size)return;
    if(sizeof(입력줄)-입력수<ұзындық_мән+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(ұзындық_мән)원격입력넣기(Команда,ұзындық_мән);원격입력넣기(&끝,1);
    셸시작됨=1;Оқиға->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!пәрмен_Түрі){const char *readme_файлы_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*readme_файлы_eb81d7d9)원격출력(*readme_файлы_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Құлақ_қою_қатысушы<0)return;
    uintptr_t ҚАЗІР_мән=보드밀리초();
    if(бір_рангілі_мән<0){if(ҚАЗІР_мән<재접속시각)return;бір_рангілі_мән=망연결받기(Құлақ_қою_қатысушы);if(бір_рангілі_мән<0)return;
        қосылым_уақыт=ҚАЗІР_мән;assh_status_t Қате=assh_session_create(문맥,&қосылым_e05f319b);
        if(Қате){қосылым_e05f319b=0;진단("SSH session error ",Қате);Жабу_қосылым();return;}}
    if((!인증됨&&ҚАЗІР_мән-қосылым_уақыт>30000)||닫을예정==2||(닫을예정&&ҚАЗІР_мән>=닫는시각)){Жабу_қосылым();return;}
    if(Арна_енгізу&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Қате=assh_channel_data(Арна_енгізу,출력줄+출력앞,&수);
            if(!Қате){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Қате!=ASSH_NO_DATA){Жабу_қосылым();return;}
        }
        if(тоқтату_күй>=0&&!출력수){unsigned char күй_мән[4];assh_store_u32(күй_мән,(uint32_t)тоқтату_күй);
            if(assh_request(қосылым_e05f319b,Арна_енгізу,"exit-status",11,күй_мән,4,0)||assh_channel_eof(Арна_енгізу)||assh_channel_close(Арна_енгізу)) {Жабу_қосылым();return;}
            닫을예정=1;닫는시각=ҚАЗІР_мән+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s Оқиға;
        if(!assh_event_get(қосылым_e05f319b,&Оқиға,ҚАЗІР_мән/1000)){Жабу_қосылым();return;}
        assh_status_t Қате=ASSH_OK;int 쉬기=0,ажырату_қатысушы=0;
        switch(Оқиға.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(бір_рангілі_мән,Оқиға.transport.read.buf.data,Оқиға.transport.read.buf.size);
            if(수>0)Оқиға.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else ажырату_қатысушы=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(бір_рангілі_мән,Оқиға.transport.write.buf.data,Оқиға.transport.write.buf.size);
            if(수>0)Оқиға.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else ажырату_қатысушы=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Оқиға.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Оқиға.userauth_server.methods.retries>3)Оқиға.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *деректер=&Оқиға.userauth_server.password;
            if(같은말(&деректер->username,"user")&&деректер->password.size<=256&&!деректер->new_password.size) {
                unsigned char жиынтық_мән[32];원격요약(деректер->password.data,деректер->password.size,жиынтық_мән);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=жиынтық_мән[순번]^қоршам_құпиясөз_жиынтық[순번];memset(жиынтық_мән,0,32);
                if(!차이)деректер->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *деректер=&Оқиға.connection.channel_open;
            if(인증됨&&!Арна_енгізу&&қоршам_Күту&&같은말(&деректер->type,"session")&&!деректер->rq_data.size) {
                деректер->reply=ASSH_CONNECTION_REPLY_SUCCESS;деректер->pkt_size=4096;
                деректер->win_size=-1;Арна_енгізу=деректер->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&Оқиға.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *деректер=&Оқиға.connection.channel_data;
            if(!셸시작됨||деректер->ch!=Арна_енгізу||деректер->ext){ажырату_қатысушы=1;break;}
            unsigned 수=деректер->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(деректер->data.data[순번]==4){тоқтату_күй=0;수=순번;деректер->transferred=деректер->data.size;break;}
            원격입력넣기(деректер->data.data,수);if(!деректер->transferred)деректер->transferred=수;
            if(!수&&тоқтату_күй<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Арна_енгізу=0;셸시작됨=0;닫을예정=1;닫는시각=ҚАЗІР_мән+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Оқиға.session.error.code);ажырату_қатысушы=1;break;
        case ASSH_EVENT_DISCONNECT: ажырату_қатысушы=1;break;
        default: break;
        }
        assh_event_done(қосылым_e05f319b,&Оқиға,Қате);
        if(ажырату_қатысушы){Жабу_қосылым();return;}if(쉬기)return;
    }
}
