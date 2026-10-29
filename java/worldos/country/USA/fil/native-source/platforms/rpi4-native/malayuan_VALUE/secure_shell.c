/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "malayuan_VALUE.h"
#include "암호기반.h"
#include "Profile.h"
#include "../Network_Stack/Network_Stack.h"
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
static struct assh_context_s *Konteksto_VALUE;
static struct assh_session_s *koneksyon_e05f319b;
static struct assh_channel_s *channel_pagpasok;
static int 듣는곳=-1,peer_VALUE=-1,인증됨,셸시작됨,utos_TYPE,tapusin_katayuan=-1,닫을예정,magbukas_error,shell_Naghihintay;
static uintptr_t koneksyon_TIME,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char digit_VALUE[12];unsigned 수=0;do{digit_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(digit_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Ihanda_Memory(void *data,void **email,size_t sukat_82232621,enum assh_alloc_type_e 종류) {
    (void)data;(void)종류;
    if(!sukat_82232621){release_malayuan(*email);*email=0;return ASSH_OK;}
    void *새주소=원격재할당(*email,sukat_82232621);
    if(!새주소)return ASSH_ERR_MEM;*email=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *data,const struct assh_buffer_s *seed_VALUE) {
    (void)data;(void)seed_VALUE;unsigned char 시험[32];int sukat=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return sukat?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *data,uint8_t *sukat,size_t haba_VALUE,uint_fast8_t 종류) {
    (void)data;(void)종류;if(haba_VALUE>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(sukat,haba_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *data){(void)data;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void isara_koneksyon(void) {
    인증됨=셸시작됨=0;channel_pagpasok=0;
    if(koneksyon_e05f319b)assh_session_release(koneksyon_e05f319b);koneksyon_e05f319b=0;
    if(peer_VALUE>=0)isara_Network(peer_VALUE);peer_VALUE=-1;utos_TYPE=0;tapusin_katayuan=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *data,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=data[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int karakter_VALUE=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return karakter_VALUE;
}
void 원격출력(unsigned char karakter_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=karakter_VALUE==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=karakter_VALUE;이전출력=karakter_VALUE;
}
uintptr_t board_tapusin_malayuan_utos(uintptr_t katayuan_VALUE){if(셸시작됨&&utos_TYPE)tapusin_katayuan=(int)katayuan_VALUE;return 0;}
uintptr_t board_malayuan_maghintay(uintptr_t katayuan_VALUE){shell_Naghihintay=katayuan_VALUE!=0;return 0;}
static int Ihanda_shell(void) {
    if(듣는곳>=0)return 0;
    if(!Konteksto_VALUE){
        assh_status_t error=assh_context_create(&Konteksto_VALUE,ASSH_SERVER,Ihanda_Memory,0,&난수기,0);
        if(error)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *pamamaraan_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        error=assh_algo_register(Konteksto_VALUE,ASSH_SAFETY_WEAK,pamamaraan_MODE);
        if(!error)error=assh_service_register_va(Konteksto_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=device_key;
        if(!error)error=assh_key_load(Konteksto_VALUE,assh_context_keys(Konteksto_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(device_key));
        if(error){진단("SSH init error ",error);assh_context_release(Konteksto_VALUE);Konteksto_VALUE=0;return -5;}
    }
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int sukat=망주소묶기(port_VALUE,0,22);if(!sukat)sukat=연결기다리기(port_VALUE);
    if(sukat<0){isara_Network(port_VALUE);return sukat;}듣는곳=port_VALUE;return 0;
}
uintptr_t board_pag_shadow(uintptr_t 종류,uintptr_t aksyon) {
    if(종류==1)return(uint32_t)control_malayuan_display(aksyon);
    if(aksyon==0){isara_koneksyon();if(듣는곳>=0)isara_Network(듣는곳);듣는곳=-1;return 0;}
    if(aksyon==1){magbukas_error=Ihanda_shell();return(uint32_t)magbukas_error;}
    return(uint32_t)(듣는곳>=0?1:magbukas_error);
}
void Ihanda_malayuan(void){magbukas_error=Ihanda_shell();control_malayuan_display(1);}
static int 같은말(const struct assh_cbuffer_s *data,const char *Word_SMS) {
    size_t haba_VALUE=strlen(Word_SMS);return data->size==haba_VALUE&&!memcmp(data->data,Word_SMS,haba_VALUE);
}
static int 터미널요청(const struct assh_cbuffer_s *data) {
    if(data->size<24)return 0;
    const unsigned char *data_posisyon=data->data;unsigned haba_VALUE=assh_load_u32(data_posisyon);
    if(haba_VALUE>128||data->size<haba_VALUE+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(data_posisyon+4+haba_VALUE+16);
    return MODE_VALUE<=2048&&data->size==haba_VALUE+24+MODE_VALUE;
}
static void 요청처리(struct assh_event_request_s *kaganapan) {
    if(!인증됨||kaganapan->ch!=channel_pagpasok||!channel_pagpasok)return;
    if(같은말(&kaganapan->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&kaganapan->rq_data))kaganapan->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&kaganapan->type,"window-change")) {
        if(셸시작됨&&kaganapan->rq_data.size==16)kaganapan->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!shell_Naghihintay)return;
    const unsigned char *utos=0;unsigned haba_VALUE=0;
    if(같은말(&kaganapan->type,"exec")) {
        if(kaganapan->rq_data.size<4)return;
        haba_VALUE=assh_load_u32(kaganapan->rq_data.data);
        if(!haba_VALUE||haba_VALUE>2048||kaganapan->rq_data.size!=haba_VALUE+4)return;
        utos=kaganapan->rq_data.data+4;
        for(unsigned 순번=0;순번<haba_VALUE;순번++)if(!utos[순번])return;
        utos_TYPE=1;
    }else if(!같은말(&kaganapan->type,"shell")||kaganapan->rq_data.size)return;
    if(sizeof(입력줄)-입력수<haba_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(haba_VALUE)원격입력넣기(utos,haba_VALUE);원격입력넣기(&끝,1);
    셸시작됨=1;kaganapan->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!utos_TYPE){const char *BASAHINAKO_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*BASAHINAKO_eb81d7d9)원격출력(*BASAHINAKO_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(peer_VALUE<0){if(NOW_VALUE<재접속시각)return;peer_VALUE=망연결받기(듣는곳);if(peer_VALUE<0)return;
        koneksyon_TIME=NOW_VALUE;assh_status_t error=assh_session_create(Konteksto_VALUE,&koneksyon_e05f319b);
        if(error){koneksyon_e05f319b=0;진단("SSH session error ",error);isara_koneksyon();return;}}
    if((!인증됨&&NOW_VALUE-koneksyon_TIME>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){isara_koneksyon();return;}
    if(channel_pagpasok&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t error=assh_channel_data(channel_pagpasok,출력줄+출력앞,&수);
            if(!error){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(error!=ASSH_NO_DATA){isara_koneksyon();return;}
        }
        if(tapusin_katayuan>=0&&!출력수){unsigned char katayuan_VALUE[4];assh_store_u32(katayuan_VALUE,(uint32_t)tapusin_katayuan);
            if(assh_request(koneksyon_e05f319b,channel_pagpasok,"exit-status",11,katayuan_VALUE,4,0)||assh_channel_eof(channel_pagpasok)||assh_channel_close(channel_pagpasok)) {isara_koneksyon();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s kaganapan;
        if(!assh_event_get(koneksyon_e05f319b,&kaganapan,NOW_VALUE/1000)){isara_koneksyon();return;}
        assh_status_t error=ASSH_OK;int 쉬기=0,끊기=0;
        switch(kaganapan.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(peer_VALUE,kaganapan.transport.read.buf.data,kaganapan.transport.read.buf.size);
            if(수>0)kaganapan.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(peer_VALUE,kaganapan.transport.write.buf.data,kaganapan.transport.write.buf.size);
            if(수>0)kaganapan.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            kaganapan.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(kaganapan.userauth_server.methods.retries>3)kaganapan.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *data=&kaganapan.userauth_server.password;
            if(같은말(&data->username,"user")&&data->password.size<=256&&!data->new_password.size) {
                unsigned char buod_VALUE[32];malayuan_buod(data->password.data,data->password.size,buod_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=buod_VALUE[순번]^shell_password_buod[순번];memset(buod_VALUE,0,32);
                if(!차이)data->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *data=&kaganapan.connection.channel_open;
            if(인증됨&&!channel_pagpasok&&shell_Naghihintay&&같은말(&data->type,"session")&&!data->rq_data.size) {
                data->reply=ASSH_CONNECTION_REPLY_SUCCESS;data->pkt_size=4096;
                data->win_size=-1;channel_pagpasok=data->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&kaganapan.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *data=&kaganapan.connection.channel_data;
            if(!셸시작됨||data->ch!=channel_pagpasok||data->ext){끊기=1;break;}
            unsigned 수=data->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(data->data.data[순번]==4){tapusin_katayuan=0;수=순번;data->transferred=data->data.size;break;}
            원격입력넣기(data->data.data,수);if(!data->transferred)data->transferred=수;
            if(!수&&tapusin_katayuan<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: channel_pagpasok=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",kaganapan.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(koneksyon_e05f319b,&kaganapan,error);
        if(끊기){isara_koneksyon();return;}if(쉬기)return;
    }
}
