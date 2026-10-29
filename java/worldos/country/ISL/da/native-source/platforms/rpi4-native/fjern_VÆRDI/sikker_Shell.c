/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "fjern_VÆRDI.h"
#include "kryptografi_støtte.h"
#include "Profil.h"
#include "../netværk_Stak/netværk_Stak.h"
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
static struct assh_context_s *kontekst_VÆRDI;
static struct assh_session_s *forbindelse_e05f319b;
static struct assh_channel_s *Kanal_post;
static int Lytter_slutpunkt=-1,peer_VÆRDI=-1,인증됨,셸시작됨,kommando_Type,afslutte_et_opkald_status=-1,닫을예정,IPL_fejl,Shell_Venter;
static uintptr_t forbindelse_TID,재접속시각,ultimo_TID;
static unsigned char input_linje[8192],produktoutput_linje[65536];
static unsigned 입력앞,input_TÆL,출력앞,produktoutput_TÆL,Forrige_produktoutput;
static void 진단(const char *Ord_sms,unsigned VÆRDI) {
    while(*Ord_sms)보드글자쓰기(*Ord_sms++);
    char ciffer_VÆRDI[12];unsigned tal=0;do{ciffer_VÆRDI[tal++]='0'+VÆRDI%10;VÆRDI/=10;}while(VÆRDI);
    while(tal)보드글자쓰기(ciffer_VÆRDI[--tal]);보드글자쓰기(10);
}
static assh_status_t Tilrettelæg_Hukommelse(void *data,void **mail,size_t Størrelse,enum assh_alloc_type_e 종류) {
    (void)data;(void)종류;
    if(!Størrelse){udgive_fjern(*mail);*mail=0;return ASSH_OK;}
    void *새주소=원격재할당(*mail,Størrelse);
    if(!새주소)return ASSH_ERR_MEM;*mail=새주소;return ASSH_OK;
}
static assh_status_t Tilrettelæg_vilkårlig(struct assh_context_s *data,const struct assh_buffer_s *basisværdi) {
    (void)data;(void)basisværdi;unsigned char 시험[32];int KR=fjern_vilkårlig(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return KR?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *data,uint8_t *KR,size_t varighed_VÆRDI,uint_fast8_t 종류) {
    (void)data;(void)종류;if(varighed_VÆRDI>65536)return ASSH_ERR_CRYPTO;
    return fjern_vilkårlig(KR,varighed_VÆRDI)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void vilkårlig_afslutte_et_opkald(struct assh_context_s *data){(void)data;}
static const struct assh_prng_s vilkårlig_generator={Tilrettelæg_vilkårlig,난수받기,vilkårlig_afslutte_et_opkald};
static void Luk_forbindelse(void) {
    인증됨=셸시작됨=0;Kanal_post=0;
    if(forbindelse_e05f319b)assh_session_release(forbindelse_e05f319b);forbindelse_e05f319b=0;
    if(peer_VÆRDI>=0)Luk_netværk(peer_VÆRDI);peer_VÆRDI=-1;kommando_Type=0;afslutte_et_opkald_status=-1;닫을예정=0;
    입력앞=input_TÆL=출력앞=produktoutput_TÆL=Forrige_produktoutput=0;재접속시각=보드밀리초()+250;
}
int feed_fjern_input(const unsigned char *data,unsigned tal) {
    if(tal>sizeof(input_linje)-input_TÆL)return -11;
    for(unsigned 순번=0;순번<tal;순번++)input_linje[(입력앞+input_TÆL++)%sizeof(input_linje)]=data[순번];return tal;
}
int fjern_input(void) {
    if(!input_TÆL)return -1;int tegn_VÆRDI=input_linje[입력앞];입력앞=(입력앞+1)%sizeof(input_linje);input_TÆL--;return tegn_VÆRDI;
}
void fjern_produktoutput(unsigned char tegn_VÆRDI) {
    if(!셸시작됨||닫을예정)return;
    unsigned tilføj_HYPPIGST=tegn_VÆRDI==10&&Forrige_produktoutput!=13;
    if(produktoutput_TÆL+1+tilføj_HYPPIGST>sizeof(produktoutput_linje)){닫을예정=2;return;}
    if(tilføj_HYPPIGST)produktoutput_linje[(출력앞+produktoutput_TÆL++)%sizeof(produktoutput_linje)]=13;
    produktoutput_linje[(출력앞+produktoutput_TÆL++)%sizeof(produktoutput_linje)]=tegn_VÆRDI;Forrige_produktoutput=tegn_VÆRDI;
}
uintptr_t Tavle_afslutte_et_opkald_fjern_kommando(uintptr_t status_VÆRDI){if(셸시작됨&&kommando_Type)afslutte_et_opkald_status=(int)status_VÆRDI;return 0;}
uintptr_t Tavle_fjern_vent(uintptr_t status_VÆRDI){Shell_Venter=status_VÆRDI!=0;return 0;}
static int Tilrettelæg_Shell(void) {
    if(Lytter_slutpunkt>=0)return 0;
    if(!kontekst_VÆRDI){
        assh_status_t fejl=assh_context_create(&kontekst_VÆRDI,ASSH_SERVER,Tilrettelæg_Hukommelse,0,&vilkårlig_generator,0);
        if(fejl)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metode_HYPPIGST[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        fejl=assh_algo_register(kontekst_VÆRDI,ASSH_SAFETY_WEAK,metode_HYPPIGST);
        if(!fejl)fejl=assh_service_register_va(kontekst_VÆRDI,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=enhed_tast;
        if(!fejl)fejl=assh_key_load(kontekst_VÆRDI,assh_context_keys(kontekst_VÆRDI),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(enhed_tast));
        if(fejl){진단("SSH init error ",fejl);assh_context_release(kontekst_VÆRDI);kontekst_VÆRDI=0;return -5;}
    }
    int port_VÆRDI=åbne_socket_slutpunkt(1);if(port_VÆRDI<0)return port_VÆRDI;통신주소재사용(port_VÆRDI);
    int KR=NET_BIND(port_VÆRDI,0,22);if(!KR)KR=NET_lytte(port_VÆRDI);
    if(KR<0){Luk_netværk(port_VÆRDI);return KR;}Lytter_slutpunkt=port_VÆRDI;return 0;
}
uintptr_t Tavle_skygning(uintptr_t 종류,uintptr_t Handling) {
    if(종류==1)return(uint32_t)kontrol_fjern_vise(Handling);
    if(Handling==0){Luk_forbindelse();if(Lytter_slutpunkt>=0)Luk_netværk(Lytter_slutpunkt);Lytter_slutpunkt=-1;return 0;}
    if(Handling==1){IPL_fejl=Tilrettelæg_Shell();return(uint32_t)IPL_fejl;}
    return(uint32_t)(Lytter_slutpunkt>=0?1:IPL_fejl);
}
void Tilrettelæg_fjern(void){IPL_fejl=Tilrettelæg_Shell();kontrol_fjern_vise(1);}
static int afstemning_Ord(const struct assh_cbuffer_s *data,const char *Ord_sms) {
    size_t varighed_VÆRDI=strlen(Ord_sms);return data->size==varighed_VÆRDI&&!memcmp(data->data,Ord_sms,varighed_VÆRDI);
}
static int Terminal_anmodning(const struct assh_cbuffer_s *data) {
    if(data->size<24)return 0;
    const unsigned char *data_placere=data->data;unsigned varighed_VÆRDI=assh_load_u32(data_placere);
    if(varighed_VÆRDI>128||data->size<varighed_VÆRDI+24)return 0;
    unsigned HYPPIGST_VÆRDI=assh_load_u32(data_placere+4+varighed_VÆRDI+16);
    return HYPPIGST_VÆRDI<=2048&&data->size==varighed_VÆRDI+24+HYPPIGST_VÆRDI;
}
static void handle_anmodning(struct assh_event_request_s *hændelse) {
    if(!인증됨||hændelse->ch!=Kanal_post||!Kanal_post)return;
    if(afstemning_Ord(&hændelse->type,"pty-req")) {
        if(!셸시작됨&&Terminal_anmodning(&hændelse->rq_data))hændelse->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(afstemning_Ord(&hændelse->type,"window-change")) {
        if(셸시작됨&&hændelse->rq_data.size==16)hændelse->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!Shell_Venter)return;
    const unsigned char *Kommando=0;unsigned varighed_VÆRDI=0;
    if(afstemning_Ord(&hændelse->type,"exec")) {
        if(hændelse->rq_data.size<4)return;
        varighed_VÆRDI=assh_load_u32(hændelse->rq_data.data);
        if(!varighed_VÆRDI||varighed_VÆRDI>2048||hændelse->rq_data.size!=varighed_VÆRDI+4)return;
        Kommando=hændelse->rq_data.data+4;
        for(unsigned 순번=0;순번<varighed_VÆRDI;순번++)if(!Kommando[순번])return;
        kommando_Type=1;
    }else if(!afstemning_Ord(&hændelse->type,"shell")||hændelse->rq_data.size)return;
    if(sizeof(input_linje)-input_TÆL<varighed_VÆRDI+2)return;
    const unsigned char 지움=21,끝=13;
    feed_fjern_input(&지움,1);if(varighed_VÆRDI)feed_fjern_input(Kommando,varighed_VÆRDI);feed_fjern_input(&끝,1);
    셸시작됨=1;hændelse->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!kommando_Type){const char *Vigtigt_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*Vigtigt_eb81d7d9)fjern_produktoutput(*Vigtigt_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Lytter_slutpunkt<0)return;
    uintptr_t NU_VÆRDI=보드밀리초();
    if(peer_VÆRDI<0){if(NU_VÆRDI<재접속시각)return;peer_VÆRDI=NET_acceptere(Lytter_slutpunkt);if(peer_VÆRDI<0)return;
        forbindelse_TID=NU_VÆRDI;assh_status_t fejl=assh_session_create(kontekst_VÆRDI,&forbindelse_e05f319b);
        if(fejl){forbindelse_e05f319b=0;진단("SSH session error ",fejl);Luk_forbindelse();return;}}
    if((!인증됨&&NU_VÆRDI-forbindelse_TID>30000)||닫을예정==2||(닫을예정&&NU_VÆRDI>=ultimo_TID)){Luk_forbindelse();return;}
    if(Kanal_post&&셸시작됨&&!닫을예정) {
        if(produktoutput_TÆL){size_t tal=sizeof(produktoutput_linje)-출력앞;if(tal>produktoutput_TÆL)tal=produktoutput_TÆL;if(tal>2048)tal=2048;
            assh_status_t fejl=assh_channel_data(Kanal_post,produktoutput_linje+출력앞,&tal);
            if(!fejl){출력앞=(출력앞+tal)%sizeof(produktoutput_linje);produktoutput_TÆL-=tal;}
            else if(fejl!=ASSH_NO_DATA){Luk_forbindelse();return;}
        }
        if(afslutte_et_opkald_status>=0&&!produktoutput_TÆL){unsigned char status_VÆRDI[4];assh_store_u32(status_VÆRDI,(uint32_t)afslutte_et_opkald_status);
            if(assh_request(forbindelse_e05f319b,Kanal_post,"exit-status",11,status_VÆRDI,4,0)||assh_channel_eof(Kanal_post)||assh_channel_close(Kanal_post)) {Luk_forbindelse();return;}
            닫을예정=1;ultimo_TID=NU_VÆRDI+3000;
        }
    }
    for(unsigned SEKVENS_VÆRDI=0;SEKVENS_VÆRDI<16;SEKVENS_VÆRDI++) {
        struct assh_event_s hændelse;
        if(!assh_event_get(forbindelse_e05f319b,&hændelse,NU_VÆRDI/1000)){Luk_forbindelse();return;}
        assh_status_t fejl=ASSH_OK;int 쉬기=0,afbryde_forbindelsen_slutpunkt=0;
        switch(hændelse.id) {
        case ASSH_EVENT_READ: {
            int tal=통신읽기(peer_VÆRDI,hændelse.transport.read.buf.data,hændelse.transport.read.buf.size);
            if(tal>0)hændelse.transport.read.transferred=tal;
            else if(tal==-11)쉬기=1;else afbryde_forbindelsen_slutpunkt=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int tal=NET_skrive(peer_VÆRDI,hændelse.transport.write.buf.data,hændelse.transport.write.buf.size);
            if(tal>0)hændelse.transport.write.transferred=tal;
            else if(tal==-11)쉬기=1;else afbryde_forbindelsen_slutpunkt=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            hændelse.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(hændelse.userauth_server.methods.retries>3)hændelse.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *data=&hændelse.userauth_server.password;
            if(afstemning_Ord(&data->username,"user")&&data->password.size<=256&&!data->new_password.size) {
                unsigned char resume_VÆRDI[32];fjern_resume(data->password.data,data->password.size,resume_VÆRDI);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=resume_VÆRDI[순번]^Shell_adgangskode_resume[순번];memset(resume_VÆRDI,0,32);
                if(!차이)data->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *data=&hændelse.connection.channel_open;
            if(인증됨&&!Kanal_post&&Shell_Venter&&afstemning_Ord(&data->type,"session")&&!data->rq_data.size) {
                data->reply=ASSH_CONNECTION_REPLY_SUCCESS;data->pkt_size=4096;
                data->win_size=-1;Kanal_post=data->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: handle_anmodning(&hændelse.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *data=&hændelse.connection.channel_data;
            if(!셸시작됨||data->ch!=Kanal_post||data->ext){afbryde_forbindelsen_slutpunkt=1;break;}
            unsigned tal=data->data.size;if(tal>sizeof(input_linje)-input_TÆL)tal=sizeof(input_linje)-input_TÆL;
            for(unsigned 순번=0;순번<tal;순번++)if(data->data.data[순번]==4){afslutte_et_opkald_status=0;tal=순번;data->transferred=data->data.size;break;}
            feed_fjern_input(data->data.data,tal);if(!data->transferred)data->transferred=tal;
            if(!tal&&afslutte_et_opkald_status<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Kanal_post=0;셸시작됨=0;닫을예정=1;ultimo_TID=NU_VÆRDI+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",hændelse.session.error.code);afbryde_forbindelsen_slutpunkt=1;break;
        case ASSH_EVENT_DISCONNECT: afbryde_forbindelsen_slutpunkt=1;break;
        default: break;
        }
        assh_event_done(forbindelse_e05f319b,&hændelse,fejl);
        if(afbryde_forbindelsen_slutpunkt){Luk_forbindelse();return;}if(쉬기)return;
    }
}
