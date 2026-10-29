/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "алсын_утга.h"
#include "암호기반.h"
#include "Хувийн_тохиргоо.h"
#include "../Сүлжээ_давхцал/Сүлжээ_давхцал.h"
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
static struct assh_context_s *Хам_сэдэв_утга;
static struct assh_session_s *холболт_e05f319b;
static struct assh_channel_s *суваг_оролт;
static int 듣는곳=-1,ижил_түвшин_утга=-1,인증됨,셸시작됨,команд_бичих,дуусгах_төлөв=-1,닫을예정,ачаалагч_алдаа,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Үгэн_Бичвэр,unsigned утга) {
    while(*Үгэн_Бичвэр)보드글자쓰기(*Үгэн_Бичвэр++);
    char тоо_утга[12];unsigned 수=0;do{тоо_утга[수++]='0'+утга%10;утга/=10;}while(утга);
    while(수)보드글자쓰기(тоо_утга[--수]);보드글자쓰기(10);
}
static assh_status_t Бэлтгэх_санах_ой(void *өгөгдөл,void **хаяг,size_t Хэмжээ,enum assh_alloc_type_e 종류) {
    (void)өгөгдөл;(void)종류;
    if(!Хэмжээ){гарц_алсын(*хаяг);*хаяг=0;return ASSH_OK;}
    void *새주소=원격재할당(*хаяг,Хэмжээ);
    if(!새주소)return ASSH_ERR_MEM;*хаяг=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *өгөгдөл,const struct assh_buffer_s *үр_утга) {
    (void)өгөгдөл;(void)үр_утга;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *өгөгдөл,uint8_t *결과,size_t урт_утга,uint_fast8_t 종류) {
    (void)өгөгдөл;(void)종류;if(урт_утга>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,урт_утга)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *өгөгдөл){(void)өгөгдөл;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void хаах_холболт(void) {
    인증됨=셸시작됨=0;суваг_оролт=0;
    if(холболт_e05f319b)assh_session_release(холболт_e05f319b);холболт_e05f319b=0;
    if(ижил_түвшин_утга>=0)хаах_Сүлжээ(ижил_түвшин_утга);ижил_түвшин_утга=-1;команд_бичих=0;дуусгах_төлөв=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *өгөгдөл,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=өгөгдөл[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int тэмдэгт_утга=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return тэмдэгт_утга;
}
void 원격출력(unsigned char тэмдэгт_утга) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=тэмдэгт_утга==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=тэмдэгт_утга;이전출력=тэмдэгт_утга;
}
uintptr_t 보드원격명령끝(uintptr_t төлөв_утга){if(셸시작됨&&команд_бичих)дуусгах_төлөв=(int)төлөв_утга;return 0;}
uintptr_t 보드원격대기(uintptr_t төлөв_утга){셸대기중=төлөв_утга!=0;return 0;}
static int Бэлтгэх_бүрхүүл(void) {
    if(듣는곳>=0)return 0;
    if(!Хам_сэдэв_утга){
        assh_status_t Алдаа=assh_context_create(&Хам_сэдэв_утга,ASSH_SERVER,Бэлтгэх_санах_ой,0,&난수기,0);
        if(Алдаа)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *арга_горим[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Алдаа=assh_algo_register(Хам_сэдэв_утга,ASSH_SAFETY_WEAK,арга_горим);
        if(!Алдаа)Алдаа=assh_service_register_va(Хам_сэдэв_утга,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=гар_утас_түлхүүр;
        if(!Алдаа)Алдаа=assh_key_load(Хам_сэдэв_утга,assh_context_keys(Хам_сэдэв_утга),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(гар_утас_түлхүүр));
        if(Алдаа){진단("SSH init error ",Алдаа);assh_context_release(Хам_сэдэв_утга);Хам_сэдэв_утга=0;return -5;}
    }
    int порт_утга=통신끝점만들기(1);if(порт_утга<0)return порт_утга;통신주소재사용(порт_утга);
    int 결과=망주소묶기(порт_утга,0,22);if(!결과)결과=연결기다리기(порт_утга);
    if(결과<0){хаах_Сүлжээ(порт_утга);return 결과;}듣는곳=порт_утга;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t Үйлдэл) {
    if(종류==1)return(uint32_t)хяналт_алсын_дэлгэц(Үйлдэл);
    if(Үйлдэл==0){хаах_холболт();if(듣는곳>=0)хаах_Сүлжээ(듣는곳);듣는곳=-1;return 0;}
    if(Үйлдэл==1){ачаалагч_алдаа=Бэлтгэх_бүрхүүл();return(uint32_t)ачаалагч_алдаа;}
    return(uint32_t)(듣는곳>=0?1:ачаалагч_алдаа);
}
void Бэлтгэх_алсын(void){ачаалагч_алдаа=Бэлтгэх_бүрхүүл();хяналт_алсын_дэлгэц(1);}
static int 같은말(const struct assh_cbuffer_s *өгөгдөл,const char *Үгэн_Бичвэр) {
    size_t урт_утга=strlen(Үгэн_Бичвэр);return өгөгдөл->size==урт_утга&&!memcmp(өгөгдөл->data,Үгэн_Бичвэр,урт_утга);
}
static int 터미널요청(const struct assh_cbuffer_s *өгөгдөл) {
    if(өгөгдөл->size<24)return 0;
    const unsigned char *자료위치=өгөгдөл->data;unsigned урт_утга=assh_load_u32(자료위치);
    if(урт_утга>128||өгөгдөл->size<урт_утга+24)return 0;
    unsigned горим_утга=assh_load_u32(자료위치+4+урт_утга+16);
    return горим_утга<=2048&&өгөгдөл->size==урт_утга+24+горим_утга;
}
static void 요청처리(struct assh_event_request_s *үйлдэл) {
    if(!인증됨||үйлдэл->ch!=суваг_оролт||!суваг_оролт)return;
    if(같은말(&үйлдэл->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&үйлдэл->rq_data))үйлдэл->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&үйлдэл->type,"window-change")) {
        if(셸시작됨&&үйлдэл->rq_data.size==16)үйлдэл->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *Тушаал=0;unsigned урт_утга=0;
    if(같은말(&үйлдэл->type,"exec")) {
        if(үйлдэл->rq_data.size<4)return;
        урт_утга=assh_load_u32(үйлдэл->rq_data.data);
        if(!урт_утга||урт_утга>2048||үйлдэл->rq_data.size!=урт_утга+4)return;
        Тушаал=үйлдэл->rq_data.data+4;
        for(unsigned 순번=0;순번<урт_утга;순번++)if(!Тушаал[순번])return;
        команд_бичих=1;
    }else if(!같은말(&үйлдэл->type,"shell")||үйлдэл->rq_data.size)return;
    if(sizeof(입력줄)-입력수<урт_утга+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(урт_утга)원격입력넣기(Тушаал,урт_утга);원격입력넣기(&끝,1);
    셸시작됨=1;үйлдэл->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!команд_бичих){const char *заавал_унших_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*заавал_унших_eb81d7d9)원격출력(*заавал_унших_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(ижил_түвшин_утга<0){if(지금<재접속시각)return;ижил_түвшин_утга=망연결받기(듣는곳);if(ижил_түвшин_утга<0)return;
        접속시각=지금;assh_status_t Алдаа=assh_session_create(Хам_сэдэв_утга,&холболт_e05f319b);
        if(Алдаа){холболт_e05f319b=0;진단("SSH session error ",Алдаа);хаах_холболт();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){хаах_холболт();return;}
    if(суваг_оролт&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Алдаа=assh_channel_data(суваг_оролт,출력줄+출력앞,&수);
            if(!Алдаа){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Алдаа!=ASSH_NO_DATA){хаах_холболт();return;}
        }
        if(дуусгах_төлөв>=0&&!출력수){unsigned char төлөв_утга[4];assh_store_u32(төлөв_утга,(uint32_t)дуусгах_төлөв);
            if(assh_request(холболт_e05f319b,суваг_оролт,"exit-status",11,төлөв_утга,4,0)||assh_channel_eof(суваг_оролт)||assh_channel_close(суваг_оролт)) {хаах_холболт();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned ДАРААЛАЛ_утга=0;ДАРААЛАЛ_утга<16;ДАРААЛАЛ_утга++) {
        struct assh_event_s үйлдэл;
        if(!assh_event_get(холболт_e05f319b,&үйлдэл,지금/1000)){хаах_холболт();return;}
        assh_status_t Алдаа=ASSH_OK;int 쉬기=0,끊기=0;
        switch(үйлдэл.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(ижил_түвшин_утга,үйлдэл.transport.read.buf.data,үйлдэл.transport.read.buf.size);
            if(수>0)үйлдэл.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(ижил_түвшин_утга,үйлдэл.transport.write.buf.data,үйлдэл.transport.write.buf.size);
            if(수>0)үйлдэл.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            үйлдэл.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(үйлдэл.userauth_server.methods.retries>3)үйлдэл.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *өгөгдөл=&үйлдэл.userauth_server.password;
            if(같은말(&өгөгдөл->username,"user")&&өгөгдөл->password.size<=256&&!өгөгдөл->new_password.size) {
                unsigned char хураангуй_утга[32];алсын_хураангуй(өгөгдөл->password.data,өгөгдөл->password.size,хураангуй_утга);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=хураангуй_утга[순번]^бүрхүүл_нууц_үг_хураангуй[순번];memset(хураангуй_утга,0,32);
                if(!차이)өгөгдөл->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *өгөгдөл=&үйлдэл.connection.channel_open;
            if(인증됨&&!суваг_оролт&&셸대기중&&같은말(&өгөгдөл->type,"session")&&!өгөгдөл->rq_data.size) {
                өгөгдөл->reply=ASSH_CONNECTION_REPLY_SUCCESS;өгөгдөл->pkt_size=4096;
                өгөгдөл->win_size=-1;суваг_оролт=өгөгдөл->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&үйлдэл.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *өгөгдөл=&үйлдэл.connection.channel_data;
            if(!셸시작됨||өгөгдөл->ch!=суваг_оролт||өгөгдөл->ext){끊기=1;break;}
            unsigned 수=өгөгдөл->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(өгөгдөл->data.data[순번]==4){дуусгах_төлөв=0;수=순번;өгөгдөл->transferred=өгөгдөл->data.size;break;}
            원격입력넣기(өгөгдөл->data.data,수);if(!өгөгдөл->transferred)өгөгдөл->transferred=수;
            if(!수&&дуусгах_төлөв<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: суваг_оролт=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",үйлдэл.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(холболт_e05f319b,&үйлдэл,Алдаа);
        if(끊기){хаах_холболт();return;}if(쉬기)return;
    }
}
