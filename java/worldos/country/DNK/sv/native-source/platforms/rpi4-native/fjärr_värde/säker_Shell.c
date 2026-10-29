/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "fjärr_värde.h"
#include "kryptografi_stöd.h"
#include "Profil.h"
#include "../nätverk_Stack/nätverk_Stack.h"
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
static struct assh_context_s *sammanhang_värde;
static struct assh_session_s *kontakt_e05f319b;
static struct assh_channel_s *Kanal_post;
static int Lyssnar_deltagare=-1,peer_värde=-1,인증됨,셸시작됨,kommando_Typ,avsluta_status=-1,닫을예정,start_fel,셸대기중;
static uintptr_t kontakt_tid,재접속시각,stängning_tid;
static unsigned char indata_rad[8192],utleverans_rad[65536];
static unsigned 입력앞,indata_ANTAL,출력앞,utleverans_ANTAL,Föregående_utleverans;
static void 진단(const char *Ord_SMS,unsigned värde) {
    while(*Ord_SMS)보드글자쓰기(*Ord_SMS++);
    char siffra_värde[12];unsigned nummer=0;do{siffra_värde[nummer++]='0'+värde%10;värde/=10;}while(värde);
    while(nummer)보드글자쓰기(siffra_värde[--nummer]);보드글자쓰기(10);
}
static assh_status_t Förbereda_Minne(void *data,void **Adress,size_t Storlek,enum assh_alloc_type_e variant_värde) {
    (void)data;(void)variant_värde;
    if(!Storlek){släppa_fjärr(*Adress);*Adress=0;return ASSH_OK;}
    void *새주소=원격재할당(*Adress,Storlek);
    if(!새주소)return ASSH_ERR_MEM;*Adress=새주소;return ASSH_OK;
}
static assh_status_t Förbereda_slumpmässig(struct assh_context_s *data,const struct assh_buffer_s *startvärde) {
    (void)data;(void)startvärde;unsigned char tester[32];int RESULTAT=fjärr_slumpmässig(tester,sizeof(tester));memset(tester,0,sizeof(tester));
    return RESULTAT?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t läsa_slumpmässig(struct assh_context_s *data,uint8_t *RESULTAT,size_t längd_värde,uint_fast8_t variant_värde) {
    (void)data;(void)variant_värde;if(längd_värde>65536)return ASSH_ERR_CRYPTO;
    return fjärr_slumpmässig(RESULTAT,längd_värde)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void slumpmässig_avsluta(struct assh_context_s *data){(void)data;}
static const struct assh_prng_s slumpmässig_generator={Förbereda_slumpmässig,läsa_slumpmässig,slumpmässig_avsluta};
static void Stäng_kontakt(void) {
    인증됨=셸시작됨=0;Kanal_post=0;
    if(kontakt_e05f319b)assh_session_release(kontakt_e05f319b);kontakt_e05f319b=0;
    if(peer_värde>=0)Stäng_nätverk(peer_värde);peer_värde=-1;kommando_Typ=0;avsluta_status=-1;닫을예정=0;
    입력앞=indata_ANTAL=출력앞=utleverans_ANTAL=Föregående_utleverans=0;재접속시각=보드밀리초()+250;
}
int feed_fjärr_indata(const unsigned char *data,unsigned nummer) {
    if(nummer>sizeof(indata_rad)-indata_ANTAL)return -11;
    for(unsigned 순번=0;순번<nummer;순번++)indata_rad[(입력앞+indata_ANTAL++)%sizeof(indata_rad)]=data[순번];return nummer;
}
int fjärr_indata(void) {
    if(!indata_ANTAL)return -1;int tecken_värde=indata_rad[입력앞];입력앞=(입력앞+1)%sizeof(indata_rad);indata_ANTAL--;return tecken_värde;
}
void fjärr_utleverans(unsigned char tecken_värde) {
    if(!셸시작됨||닫을예정)return;
    unsigned Lägga_till_läge=tecken_värde==10&&Föregående_utleverans!=13;
    if(utleverans_ANTAL+1+Lägga_till_läge>sizeof(utleverans_rad)){닫을예정=2;return;}
    if(Lägga_till_läge)utleverans_rad[(출력앞+utleverans_ANTAL++)%sizeof(utleverans_rad)]=13;
    utleverans_rad[(출력앞+utleverans_ANTAL++)%sizeof(utleverans_rad)]=tecken_värde;Föregående_utleverans=tecken_värde;
}
uintptr_t Tavla_avsluta_fjärr_kommando(uintptr_t status_värde){if(셸시작됨&&kommando_Typ)avsluta_status=(int)status_värde;return 0;}
uintptr_t Tavla_fjärr_vänta(uintptr_t status_värde){셸대기중=status_värde!=0;return 0;}
static int Förbereda_Shell(void) {
    if(Lyssnar_deltagare>=0)return 0;
    if(!sammanhang_värde){
        assh_status_t fel=assh_context_create(&sammanhang_värde,ASSH_SERVER,Förbereda_Minne,0,&slumpmässig_generator,0);
        if(fel)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metod_läge[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        fel=assh_algo_register(sammanhang_värde,ASSH_SAFETY_WEAK,metod_läge);
        if(!fel)fel=assh_service_register_va(sammanhang_värde,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=enhet_Nyckel;
        if(!fel)fel=assh_key_load(sammanhang_värde,assh_context_keys(sammanhang_värde),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(enhet_Nyckel));
        if(fel){진단("SSH init error ",fel);assh_context_release(sammanhang_värde);sammanhang_värde=0;return -5;}
    }
    int port_värde=Skapa_socket_deltagare(1);if(port_värde<0)return port_värde;통신주소재사용(port_värde);
    int RESULTAT=NET_BIND(port_värde,0,22);if(!RESULTAT)RESULTAT=NET_lyssna(port_värde);
    if(RESULTAT<0){Stäng_nätverk(port_värde);return RESULTAT;}Lyssnar_deltagare=port_värde;return 0;
}
uintptr_t Tavla_skuggning(uintptr_t variant_värde,uintptr_t Åtgärd) {
    if(variant_värde==1)return(uint32_t)kontroll_fjärr_visa(Åtgärd);
    if(Åtgärd==0){Stäng_kontakt();if(Lyssnar_deltagare>=0)Stäng_nätverk(Lyssnar_deltagare);Lyssnar_deltagare=-1;return 0;}
    if(Åtgärd==1){start_fel=Förbereda_Shell();return(uint32_t)start_fel;}
    return(uint32_t)(Lyssnar_deltagare>=0?1:start_fel);
}
void Förbereda_fjärr(void){start_fel=Förbereda_Shell();kontroll_fjärr_visa(1);}
static int matchning_Ord(const struct assh_cbuffer_s *data,const char *Ord_SMS) {
    size_t längd_värde=strlen(Ord_SMS);return data->size==längd_värde&&!memcmp(data->data,Ord_SMS,längd_värde);
}
static int Terminal_begäran(const struct assh_cbuffer_s *data) {
    if(data->size<24)return 0;
    const unsigned char *data_placera=data->data;unsigned längd_värde=assh_load_u32(data_placera);
    if(längd_värde>128||data->size<längd_värde+24)return 0;
    unsigned läge_värde=assh_load_u32(data_placera+4+längd_värde+16);
    return läge_värde<=2048&&data->size==längd_värde+24+läge_värde;
}
static void handtag_begäran(struct assh_event_request_s *Händelse) {
    if(!인증됨||Händelse->ch!=Kanal_post||!Kanal_post)return;
    if(matchning_Ord(&Händelse->type,"pty-req")) {
        if(!셸시작됨&&Terminal_begäran(&Händelse->rq_data))Händelse->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(matchning_Ord(&Händelse->type,"window-change")) {
        if(셸시작됨&&Händelse->rq_data.size==16)Händelse->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *kommando=0;unsigned längd_värde=0;
    if(matchning_Ord(&Händelse->type,"exec")) {
        if(Händelse->rq_data.size<4)return;
        längd_värde=assh_load_u32(Händelse->rq_data.data);
        if(!längd_värde||längd_värde>2048||Händelse->rq_data.size!=längd_värde+4)return;
        kommando=Händelse->rq_data.data+4;
        for(unsigned 순번=0;순번<längd_värde;순번++)if(!kommando[순번])return;
        kommando_Typ=1;
    }else if(!matchning_Ord(&Händelse->type,"shell")||Händelse->rq_data.size)return;
    if(sizeof(indata_rad)-indata_ANTAL<längd_värde+2)return;
    const unsigned char 지움=21,끝=13;
    feed_fjärr_indata(&지움,1);if(längd_värde)feed_fjärr_indata(kommando,längd_värde);feed_fjärr_indata(&끝,1);
    셸시작됨=1;Händelse->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!kommando_Typ){const char *VIKTIGT_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*VIKTIGT_eb81d7d9)fjärr_utleverans(*VIKTIGT_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Lyssnar_deltagare<0)return;
    uintptr_t NU_värde=보드밀리초();
    if(peer_värde<0){if(NU_värde<재접속시각)return;peer_värde=NET_acceptera(Lyssnar_deltagare);if(peer_värde<0)return;
        kontakt_tid=NU_värde;assh_status_t fel=assh_session_create(sammanhang_värde,&kontakt_e05f319b);
        if(fel){kontakt_e05f319b=0;진단("SSH session error ",fel);Stäng_kontakt();return;}}
    if((!인증됨&&NU_värde-kontakt_tid>30000)||닫을예정==2||(닫을예정&&NU_värde>=stängning_tid)){Stäng_kontakt();return;}
    if(Kanal_post&&셸시작됨&&!닫을예정) {
        if(utleverans_ANTAL){size_t nummer=sizeof(utleverans_rad)-출력앞;if(nummer>utleverans_ANTAL)nummer=utleverans_ANTAL;if(nummer>2048)nummer=2048;
            assh_status_t fel=assh_channel_data(Kanal_post,utleverans_rad+출력앞,&nummer);
            if(!fel){출력앞=(출력앞+nummer)%sizeof(utleverans_rad);utleverans_ANTAL-=nummer;}
            else if(fel!=ASSH_NO_DATA){Stäng_kontakt();return;}
        }
        if(avsluta_status>=0&&!utleverans_ANTAL){unsigned char status_värde[4];assh_store_u32(status_värde,(uint32_t)avsluta_status);
            if(assh_request(kontakt_e05f319b,Kanal_post,"exit-status",11,status_värde,4,0)||assh_channel_eof(Kanal_post)||assh_channel_close(Kanal_post)) {Stäng_kontakt();return;}
            닫을예정=1;stängning_tid=NU_värde+3000;
        }
    }
    for(unsigned SEKVENS_värde=0;SEKVENS_värde<16;SEKVENS_värde++) {
        struct assh_event_s Händelse;
        if(!assh_event_get(kontakt_e05f319b,&Händelse,NU_värde/1000)){Stäng_kontakt();return;}
        assh_status_t fel=ASSH_OK;int 쉬기=0,koppla_från_deltagare=0;
        switch(Händelse.id) {
        case ASSH_EVENT_READ: {
            int nummer=NET_läsa(peer_värde,Händelse.transport.read.buf.data,Händelse.transport.read.buf.size);
            if(nummer>0)Händelse.transport.read.transferred=nummer;
            else if(nummer==-11)쉬기=1;else koppla_från_deltagare=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int nummer=NET_skriva(peer_värde,Händelse.transport.write.buf.data,Händelse.transport.write.buf.size);
            if(nummer>0)Händelse.transport.write.transferred=nummer;
            else if(nummer==-11)쉬기=1;else koppla_från_deltagare=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Händelse.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Händelse.userauth_server.methods.retries>3)Händelse.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *data=&Händelse.userauth_server.password;
            if(matchning_Ord(&data->username,"user")&&data->password.size<=256&&!data->new_password.size) {
                unsigned char sammanfattning_värde[32];fjärr_sammanfattning(data->password.data,data->password.size,sammanfattning_värde);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=sammanfattning_värde[순번]^Shell_lösenord_sammanfattning[순번];memset(sammanfattning_värde,0,32);
                if(!차이)data->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *data=&Händelse.connection.channel_open;
            if(인증됨&&!Kanal_post&&셸대기중&&matchning_Ord(&data->type,"session")&&!data->rq_data.size) {
                data->reply=ASSH_CONNECTION_REPLY_SUCCESS;data->pkt_size=4096;
                data->win_size=-1;Kanal_post=data->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: handtag_begäran(&Händelse.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *data=&Händelse.connection.channel_data;
            if(!셸시작됨||data->ch!=Kanal_post||data->ext){koppla_från_deltagare=1;break;}
            unsigned nummer=data->data.size;if(nummer>sizeof(indata_rad)-indata_ANTAL)nummer=sizeof(indata_rad)-indata_ANTAL;
            for(unsigned 순번=0;순번<nummer;순번++)if(data->data.data[순번]==4){avsluta_status=0;nummer=순번;data->transferred=data->data.size;break;}
            feed_fjärr_indata(data->data.data,nummer);if(!data->transferred)data->transferred=nummer;
            if(!nummer&&avsluta_status<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Kanal_post=0;셸시작됨=0;닫을예정=1;stängning_tid=NU_värde+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Händelse.session.error.code);koppla_från_deltagare=1;break;
        case ASSH_EVENT_DISCONNECT: koppla_från_deltagare=1;break;
        default: break;
        }
        assh_event_done(kontakt_e05f319b,&Händelse,fel);
        if(koppla_från_deltagare){Stäng_kontakt();return;}if(쉬기)return;
    }
}
