/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "extern_VALUE.h"
#include "암호기반.h"
#include "Profil.h"
#include "../Reseau_Stapel/Reseau_Stapel.h"
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
static struct assh_context_s *Kontext_VALUE;
static struct assh_session_s *Verbindung_e05f319b;
static struct assh_channel_s *Kanal_Agab;
static int 듣는곳=-1,Peer_VALUE=-1,인증됨,셸시작됨,Befeel_TYPE,bëennegen_Status=-1,닫을예정,Start_Feeler,Shell_Waart;
static uintptr_t Verbindung_TIME,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char Ziffer_VALUE[12];unsigned 수=0;do{Ziffer_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(Ziffer_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Préparéieren_Späicher(void *Daten,void **Adress,size_t d_Gréisst_veränneren,enum assh_alloc_type_e 종류) {
    (void)Daten;(void)종류;
    if(!d_Gréisst_veränneren){Versioun_extern(*Adress);*Adress=0;return ASSH_OK;}
    void *새주소=원격재할당(*Adress,d_Gréisst_veränneren);
    if(!새주소)return ASSH_ERR_MEM;*Adress=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *Daten,const struct assh_buffer_s *Startwäert_VALUE) {
    (void)Daten;(void)Startwäert_VALUE;unsigned char 시험[32];int Mooss=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return Mooss?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *Daten,uint8_t *Mooss,size_t Längt_VALUE,uint_fast8_t 종류) {
    (void)Daten;(void)종류;if(Längt_VALUE>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(Mooss,Längt_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *Daten){(void)Daten;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void Clôture_Verbindung(void) {
    인증됨=셸시작됨=0;Kanal_Agab=0;
    if(Verbindung_e05f319b)assh_session_release(Verbindung_e05f319b);Verbindung_e05f319b=0;
    if(Peer_VALUE>=0)Clôture_Reseau(Peer_VALUE);Peer_VALUE=-1;Befeel_TYPE=0;bëennegen_Status=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *Daten,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=Daten[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int Zeechen_VALUE=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return Zeechen_VALUE;
}
void 원격출력(unsigned char Zeechen_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=Zeechen_VALUE==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=Zeechen_VALUE;이전출력=Zeechen_VALUE;
}
uintptr_t Board_bëennegen_extern_Befeel(uintptr_t Status_VALUE){if(셸시작됨&&Befeel_TYPE)bëennegen_Status=(int)Status_VALUE;return 0;}
uintptr_t Board_extern_Waart(uintptr_t Status_VALUE){Shell_Waart=Status_VALUE!=0;return 0;}
static int Préparéieren_Shell(void) {
    if(듣는곳>=0)return 0;
    if(!Kontext_VALUE){
        assh_status_t Feeler=assh_context_create(&Kontext_VALUE,ASSH_SERVER,Préparéieren_Späicher,0,&난수기,0);
        if(Feeler)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *Method_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Feeler=assh_algo_register(Kontext_VALUE,ASSH_SAFETY_WEAK,Method_MODE);
        if(!Feeler)Feeler=assh_service_register_va(Kontext_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=Mobil_Tast;
        if(!Feeler)Feeler=assh_key_load(Kontext_VALUE,assh_context_keys(Kontext_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(Mobil_Tast));
        if(Feeler){진단("SSH init error ",Feeler);assh_context_release(Kontext_VALUE);Kontext_VALUE=0;return -5;}
    }
    int Port_VALUE=통신끝점만들기(1);if(Port_VALUE<0)return Port_VALUE;통신주소재사용(Port_VALUE);
    int Mooss=망주소묶기(Port_VALUE,0,22);if(!Mooss)Mooss=연결기다리기(Port_VALUE);
    if(Mooss<0){Clôture_Reseau(Port_VALUE);return Mooss;}듣는곳=Port_VALUE;return 0;
}
uintptr_t Board_Shadowing(uintptr_t 종류,uintptr_t Aktioun) {
    if(종류==1)return(uint32_t)Kontroll_extern_Bildschierm(Aktioun);
    if(Aktioun==0){Clôture_Verbindung();if(듣는곳>=0)Clôture_Reseau(듣는곳);듣는곳=-1;return 0;}
    if(Aktioun==1){Start_Feeler=Préparéieren_Shell();return(uint32_t)Start_Feeler;}
    return(uint32_t)(듣는곳>=0?1:Start_Feeler);
}
void Préparéieren_extern(void){Start_Feeler=Préparéieren_Shell();Kontroll_extern_Bildschierm(1);}
static int 같은말(const struct assh_cbuffer_s *Daten,const char *Word_SMS) {
    size_t Längt_VALUE=strlen(Word_SMS);return Daten->size==Längt_VALUE&&!memcmp(Daten->data,Word_SMS,Längt_VALUE);
}
static int 터미널요청(const struct assh_cbuffer_s *Daten) {
    if(Daten->size<24)return 0;
    const unsigned char *Daten_positionéieren=Daten->data;unsigned Längt_VALUE=assh_load_u32(Daten_positionéieren);
    if(Längt_VALUE>128||Daten->size<Längt_VALUE+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(Daten_positionéieren+4+Längt_VALUE+16);
    return MODE_VALUE<=2048&&Daten->size==Längt_VALUE+24+MODE_VALUE;
}
static void 요청처리(struct assh_event_request_s *Evenement) {
    if(!인증됨||Evenement->ch!=Kanal_Agab||!Kanal_Agab)return;
    if(같은말(&Evenement->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&Evenement->rq_data))Evenement->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Evenement->type,"window-change")) {
        if(셸시작됨&&Evenement->rq_data.size==16)Evenement->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!Shell_Waart)return;
    const unsigned char *Befeel=0;unsigned Längt_VALUE=0;
    if(같은말(&Evenement->type,"exec")) {
        if(Evenement->rq_data.size<4)return;
        Längt_VALUE=assh_load_u32(Evenement->rq_data.data);
        if(!Längt_VALUE||Längt_VALUE>2048||Evenement->rq_data.size!=Längt_VALUE+4)return;
        Befeel=Evenement->rq_data.data+4;
        for(unsigned 순번=0;순번<Längt_VALUE;순번++)if(!Befeel[순번])return;
        Befeel_TYPE=1;
    }else if(!같은말(&Evenement->type,"shell")||Evenement->rq_data.size)return;
    if(sizeof(입력줄)-입력수<Längt_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(Längt_VALUE)원격입력넣기(Befeel,Längt_VALUE);원격입력넣기(&끝,1);
    셸시작됨=1;Evenement->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!Befeel_TYPE){const char *LIESMECH_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*LIESMECH_eb81d7d9)원격출력(*LIESMECH_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(Peer_VALUE<0){if(NOW_VALUE<재접속시각)return;Peer_VALUE=망연결받기(듣는곳);if(Peer_VALUE<0)return;
        Verbindung_TIME=NOW_VALUE;assh_status_t Feeler=assh_session_create(Kontext_VALUE,&Verbindung_e05f319b);
        if(Feeler){Verbindung_e05f319b=0;진단("SSH session error ",Feeler);Clôture_Verbindung();return;}}
    if((!인증됨&&NOW_VALUE-Verbindung_TIME>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){Clôture_Verbindung();return;}
    if(Kanal_Agab&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Feeler=assh_channel_data(Kanal_Agab,출력줄+출력앞,&수);
            if(!Feeler){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Feeler!=ASSH_NO_DATA){Clôture_Verbindung();return;}
        }
        if(bëennegen_Status>=0&&!출력수){unsigned char Status_VALUE[4];assh_store_u32(Status_VALUE,(uint32_t)bëennegen_Status);
            if(assh_request(Verbindung_e05f319b,Kanal_Agab,"exit-status",11,Status_VALUE,4,0)||assh_channel_eof(Kanal_Agab)||assh_channel_close(Kanal_Agab)) {Clôture_Verbindung();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s Evenement;
        if(!assh_event_get(Verbindung_e05f319b,&Evenement,NOW_VALUE/1000)){Clôture_Verbindung();return;}
        assh_status_t Feeler=ASSH_OK;int 쉬기=0,끊기=0;
        switch(Evenement.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(Peer_VALUE,Evenement.transport.read.buf.data,Evenement.transport.read.buf.size);
            if(수>0)Evenement.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(Peer_VALUE,Evenement.transport.write.buf.data,Evenement.transport.write.buf.size);
            if(수>0)Evenement.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Evenement.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Evenement.userauth_server.methods.retries>3)Evenement.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *Daten=&Evenement.userauth_server.password;
            if(같은말(&Daten->username,"user")&&Daten->password.size<=256&&!Daten->new_password.size) {
                unsigned char Zesummefaassung_VALUE[32];extern_Zesummefaassung(Daten->password.data,Daten->password.size,Zesummefaassung_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=Zesummefaassung_VALUE[순번]^Shell_Passwuert_Zesummefaassung[순번];memset(Zesummefaassung_VALUE,0,32);
                if(!차이)Daten->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *Daten=&Evenement.connection.channel_open;
            if(인증됨&&!Kanal_Agab&&Shell_Waart&&같은말(&Daten->type,"session")&&!Daten->rq_data.size) {
                Daten->reply=ASSH_CONNECTION_REPLY_SUCCESS;Daten->pkt_size=4096;
                Daten->win_size=-1;Kanal_Agab=Daten->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&Evenement.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *Daten=&Evenement.connection.channel_data;
            if(!셸시작됨||Daten->ch!=Kanal_Agab||Daten->ext){끊기=1;break;}
            unsigned 수=Daten->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(Daten->data.data[순번]==4){bëennegen_Status=0;수=순번;Daten->transferred=Daten->data.size;break;}
            원격입력넣기(Daten->data.data,수);if(!Daten->transferred)Daten->transferred=수;
            if(!수&&bëennegen_Status<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Kanal_Agab=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Evenement.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(Verbindung_e05f319b,&Evenement,Feeler);
        if(끊기){Clôture_Verbindung();return;}if(쉬기)return;
    }
}
