/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "na_nesa_Daraja.h"
#include "암호기반.h"
#include "furofayil.h"
#include "../Hanyar_sadarwa_tara/Hanyar_sadarwa_tara.h"
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
static struct assh_context_s *Kwaryar_rubutu_Daraja;
static struct assh_session_s *haɗi_e05f319b;
static struct assh_channel_s *tasha_Mashigar_bayanai;
static int 듣는곳=-1,Fiya_Daraja=-1,인증됨,셸시작됨,Umarni_rubuta,Ƙarshe_Matsayi=-1,닫을예정,Matakan_kunna_kwamfuta_Kuskure,Mai_fayyace_umani_Ana_jirawa;
static uintptr_t haɗi_lokaci,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Microsoft_Word_SMS,unsigned Daraja) {
    while(*Microsoft_Word_SMS)보드글자쓰기(*Microsoft_Word_SMS++);
    char lamba_Daraja[12];unsigned 수=0;do{lamba_Daraja[수++]='0'+Daraja%10;Daraja/=10;}while(Daraja);
    while(수)보드글자쓰기(lamba_Daraja[--수]);보드글자쓰기(10);
}
static assh_status_t Shirya_Mahardatar_kwamfuta(void *Tarin_bayani,void **imel,size_t Girma,enum assh_alloc_type_e 종류) {
    (void)Tarin_bayani;(void)종류;
    if(!Girma){saka_na_nesa(*imel);*imel=0;return ASSH_OK;}
    void *새주소=원격재할당(*imel,Girma);
    if(!새주소)return ASSH_ERR_MEM;*imel=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *Tarin_bayani,const struct assh_buffer_s *iri_Daraja) {
    (void)Tarin_bayani;(void)iri_Daraja;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *Tarin_bayani,uint8_t *결과,size_t Tsawo_Daraja,uint_fast8_t 종류) {
    (void)Tarin_bayani;(void)종류;if(Tsawo_Daraja>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,Tsawo_Daraja)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *Tarin_bayani){(void)Tarin_bayani;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void Rufe_haɗi(void) {
    인증됨=셸시작됨=0;tasha_Mashigar_bayanai=0;
    if(haɗi_e05f319b)assh_session_release(haɗi_e05f319b);haɗi_e05f319b=0;
    if(Fiya_Daraja>=0)Rufe_Hanyar_sadarwa(Fiya_Daraja);Fiya_Daraja=-1;Umarni_rubuta=0;Ƙarshe_Matsayi=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *Tarin_bayani,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=Tarin_bayani[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int Harafi_Daraja=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return Harafi_Daraja;
}
void 원격출력(unsigned char Harafi_Daraja) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=Harafi_Daraja==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=Harafi_Daraja;이전출력=Harafi_Daraja;
}
uintptr_t 보드원격명령끝(uintptr_t Matsayi_Daraja){if(셸시작됨&&Umarni_rubuta)Ƙarshe_Matsayi=(int)Matsayi_Daraja;return 0;}
uintptr_t 보드원격대기(uintptr_t Matsayi_Daraja){Mai_fayyace_umani_Ana_jirawa=Matsayi_Daraja!=0;return 0;}
static int Shirya_Mai_fayyace_umani(void) {
    if(듣는곳>=0)return 0;
    if(!Kwaryar_rubutu_Daraja){
        assh_status_t Kuskure=assh_context_create(&Kwaryar_rubutu_Daraja,ASSH_SERVER,Shirya_Mahardatar_kwamfuta,0,&난수기,0);
        if(Kuskure)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *tsari_yanayin_aiki[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Kuskure=assh_algo_register(Kwaryar_rubutu_Daraja,ASSH_SAFETY_WEAK,tsari_yanayin_aiki);
        if(!Kuskure)Kuskure=assh_service_register_va(Kwaryar_rubutu_Daraja,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=na_ura_Makulli;
        if(!Kuskure)Kuskure=assh_key_load(Kwaryar_rubutu_Daraja,assh_context_keys(Kwaryar_rubutu_Daraja),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(na_ura_Makulli));
        if(Kuskure){진단("SSH init error ",Kuskure);assh_context_release(Kwaryar_rubutu_Daraja);Kwaryar_rubutu_Daraja=0;return -5;}
    }
    int fot_Daraja=통신끝점만들기(1);if(fot_Daraja<0)return fot_Daraja;통신주소재사용(fot_Daraja);
    int 결과=망주소묶기(fot_Daraja,0,22);if(!결과)결과=연결기다리기(fot_Daraja);
    if(결과<0){Rufe_Hanyar_sadarwa(fot_Daraja);return 결과;}듣는곳=fot_Daraja;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t Aiki) {
    if(종류==1)return(uint32_t)masarrafa_na_nesa_Nuna(Aiki);
    if(Aiki==0){Rufe_haɗi();if(듣는곳>=0)Rufe_Hanyar_sadarwa(듣는곳);듣는곳=-1;return 0;}
    if(Aiki==1){Matakan_kunna_kwamfuta_Kuskure=Shirya_Mai_fayyace_umani();return(uint32_t)Matakan_kunna_kwamfuta_Kuskure;}
    return(uint32_t)(듣는곳>=0?1:Matakan_kunna_kwamfuta_Kuskure);
}
void Shirya_na_nesa(void){Matakan_kunna_kwamfuta_Kuskure=Shirya_Mai_fayyace_umani();masarrafa_na_nesa_Nuna(1);}
static int 같은말(const struct assh_cbuffer_s *Tarin_bayani,const char *Microsoft_Word_SMS) {
    size_t Tsawo_Daraja=strlen(Microsoft_Word_SMS);return Tarin_bayani->size==Tsawo_Daraja&&!memcmp(Tarin_bayani->data,Microsoft_Word_SMS,Tsawo_Daraja);
}
static int 터미널요청(const struct assh_cbuffer_s *Tarin_bayani) {
    if(Tarin_bayani->size<24)return 0;
    const unsigned char *자료위치=Tarin_bayani->data;unsigned Tsawo_Daraja=assh_load_u32(자료위치);
    if(Tsawo_Daraja>128||Tarin_bayani->size<Tsawo_Daraja+24)return 0;
    unsigned yanayin_aiki_Daraja=assh_load_u32(자료위치+4+Tsawo_Daraja+16);
    return yanayin_aiki_Daraja<=2048&&Tarin_bayani->size==Tsawo_Daraja+24+yanayin_aiki_Daraja;
}
static void 요청처리(struct assh_event_request_s *Faruwa) {
    if(!인증됨||Faruwa->ch!=tasha_Mashigar_bayanai||!tasha_Mashigar_bayanai)return;
    if(같은말(&Faruwa->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&Faruwa->rq_data))Faruwa->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Faruwa->type,"window-change")) {
        if(셸시작됨&&Faruwa->rq_data.size==16)Faruwa->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!Mai_fayyace_umani_Ana_jirawa)return;
    const unsigned char *Umarni=0;unsigned Tsawo_Daraja=0;
    if(같은말(&Faruwa->type,"exec")) {
        if(Faruwa->rq_data.size<4)return;
        Tsawo_Daraja=assh_load_u32(Faruwa->rq_data.data);
        if(!Tsawo_Daraja||Tsawo_Daraja>2048||Faruwa->rq_data.size!=Tsawo_Daraja+4)return;
        Umarni=Faruwa->rq_data.data+4;
        for(unsigned 순번=0;순번<Tsawo_Daraja;순번++)if(!Umarni[순번])return;
        Umarni_rubuta=1;
    }else if(!같은말(&Faruwa->type,"shell")||Faruwa->rq_data.size)return;
    if(sizeof(입력줄)-입력수<Tsawo_Daraja+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(Tsawo_Daraja)원격입력넣기(Umarni,Tsawo_Daraja);원격입력넣기(&끝,1);
    셸시작됨=1;Faruwa->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!Umarni_rubuta){const char *README_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*README_eb81d7d9)원격출력(*README_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t Yanzu_Daraja=보드밀리초();
    if(Fiya_Daraja<0){if(Yanzu_Daraja<재접속시각)return;Fiya_Daraja=망연결받기(듣는곳);if(Fiya_Daraja<0)return;
        haɗi_lokaci=Yanzu_Daraja;assh_status_t Kuskure=assh_session_create(Kwaryar_rubutu_Daraja,&haɗi_e05f319b);
        if(Kuskure){haɗi_e05f319b=0;진단("SSH session error ",Kuskure);Rufe_haɗi();return;}}
    if((!인증됨&&Yanzu_Daraja-haɗi_lokaci>30000)||닫을예정==2||(닫을예정&&Yanzu_Daraja>=닫는시각)){Rufe_haɗi();return;}
    if(tasha_Mashigar_bayanai&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Kuskure=assh_channel_data(tasha_Mashigar_bayanai,출력줄+출력앞,&수);
            if(!Kuskure){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Kuskure!=ASSH_NO_DATA){Rufe_haɗi();return;}
        }
        if(Ƙarshe_Matsayi>=0&&!출력수){unsigned char Matsayi_Daraja[4];assh_store_u32(Matsayi_Daraja,(uint32_t)Ƙarshe_Matsayi);
            if(assh_request(haɗi_e05f319b,tasha_Mashigar_bayanai,"exit-status",11,Matsayi_Daraja,4,0)||assh_channel_eof(tasha_Mashigar_bayanai)||assh_channel_close(tasha_Mashigar_bayanai)) {Rufe_haɗi();return;}
            닫을예정=1;닫는시각=Yanzu_Daraja+3000;
        }
    }
    for(unsigned JERI_Daraja=0;JERI_Daraja<16;JERI_Daraja++) {
        struct assh_event_s Faruwa;
        if(!assh_event_get(haɗi_e05f319b,&Faruwa,Yanzu_Daraja/1000)){Rufe_haɗi();return;}
        assh_status_t Kuskure=ASSH_OK;int 쉬기=0,끊기=0;
        switch(Faruwa.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(Fiya_Daraja,Faruwa.transport.read.buf.data,Faruwa.transport.read.buf.size);
            if(수>0)Faruwa.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(Fiya_Daraja,Faruwa.transport.write.buf.data,Faruwa.transport.write.buf.size);
            if(수>0)Faruwa.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Faruwa.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Faruwa.userauth_server.methods.retries>3)Faruwa.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *Tarin_bayani=&Faruwa.userauth_server.password;
            if(같은말(&Tarin_bayani->username,"user")&&Tarin_bayani->password.size<=256&&!Tarin_bayani->new_password.size) {
                unsigned char taƙaitawa_Daraja[32];na_nesa_taƙaitawa(Tarin_bayani->password.data,Tarin_bayani->password.size,taƙaitawa_Daraja);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=taƙaitawa_Daraja[순번]^Mai_fayyace_umani_kalmar_sirri_taƙaitawa[순번];memset(taƙaitawa_Daraja,0,32);
                if(!차이)Tarin_bayani->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *Tarin_bayani=&Faruwa.connection.channel_open;
            if(인증됨&&!tasha_Mashigar_bayanai&&Mai_fayyace_umani_Ana_jirawa&&같은말(&Tarin_bayani->type,"session")&&!Tarin_bayani->rq_data.size) {
                Tarin_bayani->reply=ASSH_CONNECTION_REPLY_SUCCESS;Tarin_bayani->pkt_size=4096;
                Tarin_bayani->win_size=-1;tasha_Mashigar_bayanai=Tarin_bayani->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&Faruwa.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *Tarin_bayani=&Faruwa.connection.channel_data;
            if(!셸시작됨||Tarin_bayani->ch!=tasha_Mashigar_bayanai||Tarin_bayani->ext){끊기=1;break;}
            unsigned 수=Tarin_bayani->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(Tarin_bayani->data.data[순번]==4){Ƙarshe_Matsayi=0;수=순번;Tarin_bayani->transferred=Tarin_bayani->data.size;break;}
            원격입력넣기(Tarin_bayani->data.data,수);if(!Tarin_bayani->transferred)Tarin_bayani->transferred=수;
            if(!수&&Ƙarshe_Matsayi<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: tasha_Mashigar_bayanai=0;셸시작됨=0;닫을예정=1;닫는시각=Yanzu_Daraja+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Faruwa.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(haɗi_e05f319b,&Faruwa,Kuskure);
        if(끊기){Rufe_haɗi();return;}if(쉬기)return;
    }
}
