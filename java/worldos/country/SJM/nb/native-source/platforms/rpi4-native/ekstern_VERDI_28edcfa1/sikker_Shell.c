/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "ekstern_VERDI_28edcfa1.h"
#include "kryptografi_støtte.h"
#include "Profil.h"
#include "../nettverk_stakk/nettverk_stakk.h"
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
static struct assh_context_s *kontekst_VERDI;
static struct assh_session_s *kontakt_e05f319b;
static struct assh_channel_s *Kanal_oppføring;
static int Lytter_deltaker=-1,node_VERDI_6a3b6fa7=-1,인증됨,셸시작됨,kommando_Type,avslutte_en_samtale_status=-1,닫을예정,oppstart_feil,Shell_Venter;
static uintptr_t kontakt_TID,재접속시각,lukking_TID;
static unsigned char inndata_linje[8192],produksjon_linje[65536];
static unsigned 입력앞,inndata_ANTALL,출력앞,produksjon_ANTALL,Forrige_produksjon;
static void 진단(const char *ord_SMS,unsigned VERDI) {
    while(*ord_SMS)보드글자쓰기(*ord_SMS++);
    char siffer_VERDI[12];unsigned nummer=0;do{siffer_VERDI[nummer++]='0'+VERDI%10;VERDI/=10;}while(VERDI);
    while(nummer)보드글자쓰기(siffer_VERDI[--nummer]);보드글자쓰기(10);
}
static assh_status_t Forbered_Minne(void *data,void **e_post,size_t Størrelse,enum assh_alloc_type_e 종류) {
    (void)data;(void)종류;
    if(!Størrelse){frigi_ekstern(*e_post);*e_post=0;return ASSH_OK;}
    void *새주소=원격재할당(*e_post,Størrelse);
    if(!새주소)return ASSH_ERR_MEM;*e_post=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *data,const struct assh_buffer_s *utgangsverdi) {
    (void)data;(void)utgangsverdi;unsigned char 시험[32];int KR=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return KR?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *data,uint8_t *KR,size_t lengde_VERDI,uint_fast8_t 종류) {
    (void)data;(void)종류;if(lengde_VERDI>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(KR,lengde_VERDI)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *data){(void)data;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void Lukk_kontakt(void) {
    인증됨=셸시작됨=0;Kanal_oppføring=0;
    if(kontakt_e05f319b)assh_session_release(kontakt_e05f319b);kontakt_e05f319b=0;
    if(node_VERDI_6a3b6fa7>=0)Lukk_nettverk(node_VERDI_6a3b6fa7);node_VERDI_6a3b6fa7=-1;kommando_Type=0;avslutte_en_samtale_status=-1;닫을예정=0;
    입력앞=inndata_ANTALL=출력앞=produksjon_ANTALL=Forrige_produksjon=0;재접속시각=보드밀리초()+250;
}
int feed_ekstern_inndata(const unsigned char *data,unsigned nummer) {
    if(nummer>sizeof(inndata_linje)-inndata_ANTALL)return -11;
    for(unsigned 순번=0;순번<nummer;순번++)inndata_linje[(입력앞+inndata_ANTALL++)%sizeof(inndata_linje)]=data[순번];return nummer;
}
int ekstern_inndata(void) {
    if(!inndata_ANTALL)return -1;int tegn_VERDI=inndata_linje[입력앞];입력앞=(입력앞+1)%sizeof(inndata_linje);inndata_ANTALL--;return tegn_VERDI;
}
void ekstern_produksjon(unsigned char tegn_VERDI) {
    if(!셸시작됨||닫을예정)return;
    unsigned Tilføye_MODUS=tegn_VERDI==10&&Forrige_produksjon!=13;
    if(produksjon_ANTALL+1+Tilføye_MODUS>sizeof(produksjon_linje)){닫을예정=2;return;}
    if(Tilføye_MODUS)produksjon_linje[(출력앞+produksjon_ANTALL++)%sizeof(produksjon_linje)]=13;
    produksjon_linje[(출력앞+produksjon_ANTALL++)%sizeof(produksjon_linje)]=tegn_VERDI;Forrige_produksjon=tegn_VERDI;
}
uintptr_t Tavle_avslutte_en_samtale_ekstern_kommando(uintptr_t status_VERDI){if(셸시작됨&&kommando_Type)avslutte_en_samtale_status=(int)status_VERDI;return 0;}
uintptr_t Tavle_ekstern_vent(uintptr_t status_VERDI){Shell_Venter=status_VERDI!=0;return 0;}
static int Forbered_Shell(void) {
    if(Lytter_deltaker>=0)return 0;
    if(!kontekst_VERDI){
        assh_status_t feil=assh_context_create(&kontekst_VERDI,ASSH_SERVER,Forbered_Minne,0,&난수기,0);
        if(feil)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metode_MODUS[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        feil=assh_algo_register(kontekst_VERDI,ASSH_SAFETY_WEAK,metode_MODUS);
        if(!feil)feil=assh_service_register_va(kontekst_VERDI,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=enhet_tast;
        if(!feil)feil=assh_key_load(kontekst_VERDI,assh_context_keys(kontekst_VERDI),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(enhet_tast));
        if(feil){진단("SSH init error ",feil);assh_context_release(kontekst_VERDI);kontekst_VERDI=0;return -5;}
    }
    int port_VERDI=åpne_socket_deltaker(1);if(port_VERDI<0)return port_VERDI;통신주소재사용(port_VERDI);
    int KR=netto_BIND(port_VERDI,0,22);if(!KR)KR=연결기다리기(port_VERDI);
    if(KR<0){Lukk_nettverk(port_VERDI);return KR;}Lytter_deltaker=port_VERDI;return 0;
}
uintptr_t Tavle_skygging(uintptr_t 종류,uintptr_t Handling) {
    if(종류==1)return(uint32_t)kontroll_ekstern_vise(Handling);
    if(Handling==0){Lukk_kontakt();if(Lytter_deltaker>=0)Lukk_nettverk(Lytter_deltaker);Lytter_deltaker=-1;return 0;}
    if(Handling==1){oppstart_feil=Forbered_Shell();return(uint32_t)oppstart_feil;}
    return(uint32_t)(Lytter_deltaker>=0?1:oppstart_feil);
}
void Forbered_ekstern(void){oppstart_feil=Forbered_Shell();kontroll_ekstern_vise(1);}
static int avstemming_ord(const struct assh_cbuffer_s *data,const char *ord_SMS) {
    size_t lengde_VERDI=strlen(ord_SMS);return data->size==lengde_VERDI&&!memcmp(data->data,ord_SMS,lengde_VERDI);
}
static int Terminal_forespørsel(const struct assh_cbuffer_s *data) {
    if(data->size<24)return 0;
    const unsigned char *data_plassere=data->data;unsigned lengde_VERDI=assh_load_u32(data_plassere);
    if(lengde_VERDI>128||data->size<lengde_VERDI+24)return 0;
    unsigned MODUS_VERDI=assh_load_u32(data_plassere+4+lengde_VERDI+16);
    return MODUS_VERDI<=2048&&data->size==lengde_VERDI+24+MODUS_VERDI;
}
static void håndtak_forespørsel(struct assh_event_request_s *Hendelse) {
    if(!인증됨||Hendelse->ch!=Kanal_oppføring||!Kanal_oppføring)return;
    if(avstemming_ord(&Hendelse->type,"pty-req")) {
        if(!셸시작됨&&Terminal_forespørsel(&Hendelse->rq_data))Hendelse->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(avstemming_ord(&Hendelse->type,"window-change")) {
        if(셸시작됨&&Hendelse->rq_data.size==16)Hendelse->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!Shell_Venter)return;
    const unsigned char *Kommando=0;unsigned lengde_VERDI=0;
    if(avstemming_ord(&Hendelse->type,"exec")) {
        if(Hendelse->rq_data.size<4)return;
        lengde_VERDI=assh_load_u32(Hendelse->rq_data.data);
        if(!lengde_VERDI||lengde_VERDI>2048||Hendelse->rq_data.size!=lengde_VERDI+4)return;
        Kommando=Hendelse->rq_data.data+4;
        for(unsigned 순번=0;순번<lengde_VERDI;순번++)if(!Kommando[순번])return;
        kommando_Type=1;
    }else if(!avstemming_ord(&Hendelse->type,"shell")||Hendelse->rq_data.size)return;
    if(sizeof(inndata_linje)-inndata_ANTALL<lengde_VERDI+2)return;
    const unsigned char 지움=21,끝=13;
    feed_ekstern_inndata(&지움,1);if(lengde_VERDI)feed_ekstern_inndata(Kommando,lengde_VERDI);feed_ekstern_inndata(&끝,1);
    셸시작됨=1;Hendelse->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!kommando_Type){const char *Viktig_fil_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*Viktig_fil_eb81d7d9)ekstern_produksjon(*Viktig_fil_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Lytter_deltaker<0)return;
    uintptr_t NÅ_VERDI=보드밀리초();
    if(node_VERDI_6a3b6fa7<0){if(NÅ_VERDI<재접속시각)return;node_VERDI_6a3b6fa7=netto_godta(Lytter_deltaker);if(node_VERDI_6a3b6fa7<0)return;
        kontakt_TID=NÅ_VERDI;assh_status_t feil=assh_session_create(kontekst_VERDI,&kontakt_e05f319b);
        if(feil){kontakt_e05f319b=0;진단("SSH session error ",feil);Lukk_kontakt();return;}}
    if((!인증됨&&NÅ_VERDI-kontakt_TID>30000)||닫을예정==2||(닫을예정&&NÅ_VERDI>=lukking_TID)){Lukk_kontakt();return;}
    if(Kanal_oppføring&&셸시작됨&&!닫을예정) {
        if(produksjon_ANTALL){size_t nummer=sizeof(produksjon_linje)-출력앞;if(nummer>produksjon_ANTALL)nummer=produksjon_ANTALL;if(nummer>2048)nummer=2048;
            assh_status_t feil=assh_channel_data(Kanal_oppføring,produksjon_linje+출력앞,&nummer);
            if(!feil){출력앞=(출력앞+nummer)%sizeof(produksjon_linje);produksjon_ANTALL-=nummer;}
            else if(feil!=ASSH_NO_DATA){Lukk_kontakt();return;}
        }
        if(avslutte_en_samtale_status>=0&&!produksjon_ANTALL){unsigned char status_VERDI[4];assh_store_u32(status_VERDI,(uint32_t)avslutte_en_samtale_status);
            if(assh_request(kontakt_e05f319b,Kanal_oppføring,"exit-status",11,status_VERDI,4,0)||assh_channel_eof(Kanal_oppføring)||assh_channel_close(Kanal_oppføring)) {Lukk_kontakt();return;}
            닫을예정=1;lukking_TID=NÅ_VERDI+3000;
        }
    }
    for(unsigned SEKVENS_VERDI=0;SEKVENS_VERDI<16;SEKVENS_VERDI++) {
        struct assh_event_s Hendelse;
        if(!assh_event_get(kontakt_e05f319b,&Hendelse,NÅ_VERDI/1000)){Lukk_kontakt();return;}
        assh_status_t feil=ASSH_OK;int 쉬기=0,legg_på_deltaker=0;
        switch(Hendelse.id) {
        case ASSH_EVENT_READ: {
            int nummer=통신읽기(node_VERDI_6a3b6fa7,Hendelse.transport.read.buf.data,Hendelse.transport.read.buf.size);
            if(nummer>0)Hendelse.transport.read.transferred=nummer;
            else if(nummer==-11)쉬기=1;else legg_på_deltaker=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int nummer=netto_skrive(node_VERDI_6a3b6fa7,Hendelse.transport.write.buf.data,Hendelse.transport.write.buf.size);
            if(nummer>0)Hendelse.transport.write.transferred=nummer;
            else if(nummer==-11)쉬기=1;else legg_på_deltaker=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Hendelse.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Hendelse.userauth_server.methods.retries>3)Hendelse.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *data=&Hendelse.userauth_server.password;
            if(avstemming_ord(&data->username,"user")&&data->password.size<=256&&!data->new_password.size) {
                unsigned char sammendrag_VERDI[32];ekstern_sammendrag(data->password.data,data->password.size,sammendrag_VERDI);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=sammendrag_VERDI[순번]^Shell_passord_sammendrag[순번];memset(sammendrag_VERDI,0,32);
                if(!차이)data->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *data=&Hendelse.connection.channel_open;
            if(인증됨&&!Kanal_oppføring&&Shell_Venter&&avstemming_ord(&data->type,"session")&&!data->rq_data.size) {
                data->reply=ASSH_CONNECTION_REPLY_SUCCESS;data->pkt_size=4096;
                data->win_size=-1;Kanal_oppføring=data->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: håndtak_forespørsel(&Hendelse.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *data=&Hendelse.connection.channel_data;
            if(!셸시작됨||data->ch!=Kanal_oppføring||data->ext){legg_på_deltaker=1;break;}
            unsigned nummer=data->data.size;if(nummer>sizeof(inndata_linje)-inndata_ANTALL)nummer=sizeof(inndata_linje)-inndata_ANTALL;
            for(unsigned 순번=0;순번<nummer;순번++)if(data->data.data[순번]==4){avslutte_en_samtale_status=0;nummer=순번;data->transferred=data->data.size;break;}
            feed_ekstern_inndata(data->data.data,nummer);if(!data->transferred)data->transferred=nummer;
            if(!nummer&&avslutte_en_samtale_status<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Kanal_oppføring=0;셸시작됨=0;닫을예정=1;lukking_TID=NÅ_VERDI+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Hendelse.session.error.code);legg_på_deltaker=1;break;
        case ASSH_EVENT_DISCONNECT: legg_på_deltaker=1;break;
        default: break;
        }
        assh_event_done(kontakt_e05f319b,&Hendelse,feil);
        if(legg_på_deltaker){Lukk_kontakt();return;}if(쉬기)return;
    }
}
