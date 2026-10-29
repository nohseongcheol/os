/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "la_distanță_VALUE.h"
#include "criptografie_suport.h"
#include "Profil.h"
#include "../rețea_Teanc/rețea_Teanc.h"
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
static struct assh_context_s *context_VALUE;
static struct assh_session_s *conexiune_e05f319b;
static struct assh_channel_s *Canal_intrare;
static int Ascult_participant=-1,pereche_VALUE=-1,인증됨,셸시작됨,comandă_Tip,termina_un_apel_Stare=-1,닫을예정,boot_eroare,shell_Aștept;
static uintptr_t conexiune_oră,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char cifră_VALUE[12];unsigned 수=0;do{cifră_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(cifră_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Pregătiți_Memorie(void *date,void **adresa,size_t Mărime,enum assh_alloc_type_e 종류) {
    (void)date;(void)종류;
    if(!Mărime){lansa_la_distanță(*adresa);*adresa=0;return ASSH_OK;}
    void *새주소=원격재할당(*adresa,Mărime);
    if(!새주소)return ASSH_ERR_MEM;*adresa=새주소;return ASSH_OK;
}
static assh_status_t Pregătiți_aleator(struct assh_context_s *date,const struct assh_buffer_s *valoare_inițială) {
    (void)date;(void)valoare_inițială;unsigned char 시험[32];int KR=la_distanță_aleator(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return KR?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *date,uint8_t *KR,size_t lungime_VALUE,uint_fast8_t 종류) {
    (void)date;(void)종류;if(lungime_VALUE>65536)return ASSH_ERR_CRYPTO;
    return la_distanță_aleator(KR,lungime_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void aleator_termina_un_apel(struct assh_context_s *date){(void)date;}
static const struct assh_prng_s aleator_generator={Pregătiți_aleator,난수받기,aleator_termina_un_apel};
static void închide_conexiune(void) {
    인증됨=셸시작됨=0;Canal_intrare=0;
    if(conexiune_e05f319b)assh_session_release(conexiune_e05f319b);conexiune_e05f319b=0;
    if(pereche_VALUE>=0)închide_rețea(pereche_VALUE);pereche_VALUE=-1;comandă_Tip=0;termina_un_apel_Stare=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *date,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=date[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int caracter_VALUE=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return caracter_VALUE;
}
void 원격출력(unsigned char caracter_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned adăuga_mod=caracter_VALUE==10&&이전출력!=13;
    if(출력수+1+adăuga_mod>sizeof(출력줄)){닫을예정=2;return;}
    if(adăuga_mod)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=caracter_VALUE;이전출력=caracter_VALUE;
}
uintptr_t Avizier_termina_un_apel_la_distanță_comandă(uintptr_t Stare_VALUE){if(셸시작됨&&comandă_Tip)termina_un_apel_Stare=(int)Stare_VALUE;return 0;}
uintptr_t 보드원격대기(uintptr_t Stare_VALUE){shell_Aștept=Stare_VALUE!=0;return 0;}
static int Pregătiți_shell(void) {
    if(Ascult_participant>=0)return 0;
    if(!context_VALUE){
        assh_status_t eroare=assh_context_create(&context_VALUE,ASSH_SERVER,Pregătiți_Memorie,0,&aleator_generator,0);
        if(eroare)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metodă_mod[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        eroare=assh_algo_register(context_VALUE,ASSH_SAFETY_WEAK,metodă_mod);
        if(!eroare)eroare=assh_service_register_va(context_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=mobil_Cheie;
        if(!eroare)eroare=assh_key_load(context_VALUE,assh_context_keys(context_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(mobil_Cheie));
        if(eroare){진단("SSH init error ",eroare);assh_context_release(context_VALUE);context_VALUE=0;return -5;}
    }
    int muta_VALUE=통신끝점만들기(1);if(muta_VALUE<0)return muta_VALUE;통신주소재사용(muta_VALUE);
    int KR=NET_BIND(muta_VALUE,0,22);if(!KR)KR=NET_asculta(muta_VALUE);
    if(KR<0){închide_rețea(muta_VALUE);return KR;}Ascult_participant=muta_VALUE;return 0;
}
uintptr_t Avizier_control_la_distanță(uintptr_t 종류,uintptr_t Acțiuni) {
    if(종류==1)return(uint32_t)control_la_distanță_afișa(Acțiuni);
    if(Acțiuni==0){închide_conexiune();if(Ascult_participant>=0)închide_rețea(Ascult_participant);Ascult_participant=-1;return 0;}
    if(Acțiuni==1){boot_eroare=Pregătiți_shell();return(uint32_t)boot_eroare;}
    return(uint32_t)(Ascult_participant>=0?1:boot_eroare);
}
void Pregătiți_la_distanță(void){boot_eroare=Pregătiți_shell();control_la_distanță_afișa(1);}
static int 같은말(const struct assh_cbuffer_s *date,const char *Word_SMS) {
    size_t lungime_VALUE=strlen(Word_SMS);return date->size==lungime_VALUE&&!memcmp(date->data,Word_SMS,lungime_VALUE);
}
static int Terminal_cerere(const struct assh_cbuffer_s *date) {
    if(date->size<24)return 0;
    const unsigned char *date_poziție=date->data;unsigned lungime_VALUE=assh_load_u32(date_poziție);
    if(lungime_VALUE>128||date->size<lungime_VALUE+24)return 0;
    unsigned mod_VALUE=assh_load_u32(date_poziție+4+lungime_VALUE+16);
    return mod_VALUE<=2048&&date->size==lungime_VALUE+24+mod_VALUE;
}
static void handle_cerere(struct assh_event_request_s *Eveniment) {
    if(!인증됨||Eveniment->ch!=Canal_intrare||!Canal_intrare)return;
    if(같은말(&Eveniment->type,"pty-req")) {
        if(!셸시작됨&&Terminal_cerere(&Eveniment->rq_data))Eveniment->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Eveniment->type,"window-change")) {
        if(셸시작됨&&Eveniment->rq_data.size==16)Eveniment->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!shell_Aștept)return;
    const unsigned char *Comandă=0;unsigned lungime_VALUE=0;
    if(같은말(&Eveniment->type,"exec")) {
        if(Eveniment->rq_data.size<4)return;
        lungime_VALUE=assh_load_u32(Eveniment->rq_data.data);
        if(!lungime_VALUE||lungime_VALUE>2048||Eveniment->rq_data.size!=lungime_VALUE+4)return;
        Comandă=Eveniment->rq_data.data+4;
        for(unsigned 순번=0;순번<lungime_VALUE;순번++)if(!Comandă[순번])return;
        comandă_Tip=1;
    }else if(!같은말(&Eveniment->type,"shell")||Eveniment->rq_data.size)return;
    if(sizeof(입력줄)-입력수<lungime_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(lungime_VALUE)원격입력넣기(Comandă,lungime_VALUE);원격입력넣기(&끝,1);
    셸시작됨=1;Eveniment->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!comandă_Tip){const char *안내="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*안내)원격출력(*안내++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Ascult_participant<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(pereche_VALUE<0){if(NOW_VALUE<재접속시각)return;pereche_VALUE=NET_accepta(Ascult_participant);if(pereche_VALUE<0)return;
        conexiune_oră=NOW_VALUE;assh_status_t eroare=assh_session_create(context_VALUE,&conexiune_e05f319b);
        if(eroare){conexiune_e05f319b=0;진단("SSH session error ",eroare);închide_conexiune();return;}}
    if((!인증됨&&NOW_VALUE-conexiune_oră>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){închide_conexiune();return;}
    if(Canal_intrare&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t eroare=assh_channel_data(Canal_intrare,출력줄+출력앞,&수);
            if(!eroare){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(eroare!=ASSH_NO_DATA){închide_conexiune();return;}
        }
        if(termina_un_apel_Stare>=0&&!출력수){unsigned char Stare_VALUE[4];assh_store_u32(Stare_VALUE,(uint32_t)termina_un_apel_Stare);
            if(assh_request(conexiune_e05f319b,Canal_intrare,"exit-status",11,Stare_VALUE,4,0)||assh_channel_eof(Canal_intrare)||assh_channel_close(Canal_intrare)) {închide_conexiune();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s Eveniment;
        if(!assh_event_get(conexiune_e05f319b,&Eveniment,NOW_VALUE/1000)){închide_conexiune();return;}
        assh_status_t eroare=ASSH_OK;int 쉬기=0,deconecta_participant=0;
        switch(Eveniment.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(pereche_VALUE,Eveniment.transport.read.buf.data,Eveniment.transport.read.buf.size);
            if(수>0)Eveniment.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else deconecta_participant=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=NET_scriere(pereche_VALUE,Eveniment.transport.write.buf.data,Eveniment.transport.write.buf.size);
            if(수>0)Eveniment.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else deconecta_participant=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Eveniment.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Eveniment.userauth_server.methods.retries>3)Eveniment.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *date=&Eveniment.userauth_server.password;
            if(같은말(&date->username,"user")&&date->password.size<=256&&!date->new_password.size) {
                unsigned char rezumat_VALUE[32];la_distanță_rezumat(date->password.data,date->password.size,rezumat_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=rezumat_VALUE[순번]^shell_parolă_rezumat[순번];memset(rezumat_VALUE,0,32);
                if(!차이)date->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *date=&Eveniment.connection.channel_open;
            if(인증됨&&!Canal_intrare&&shell_Aștept&&같은말(&date->type,"session")&&!date->rq_data.size) {
                date->reply=ASSH_CONNECTION_REPLY_SUCCESS;date->pkt_size=4096;
                date->win_size=-1;Canal_intrare=date->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: handle_cerere(&Eveniment.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *date=&Eveniment.connection.channel_data;
            if(!셸시작됨||date->ch!=Canal_intrare||date->ext){deconecta_participant=1;break;}
            unsigned 수=date->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(date->data.data[순번]==4){termina_un_apel_Stare=0;수=순번;date->transferred=date->data.size;break;}
            원격입력넣기(date->data.data,수);if(!date->transferred)date->transferred=수;
            if(!수&&termina_un_apel_Stare<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Canal_intrare=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Eveniment.session.error.code);deconecta_participant=1;break;
        case ASSH_EVENT_DISCONNECT: deconecta_participant=1;break;
        default: break;
        }
        assh_event_done(conexiune_e05f319b,&Eveniment,eroare);
        if(deconecta_participant){închide_conexiune();return;}if(쉬기)return;
    }
}
