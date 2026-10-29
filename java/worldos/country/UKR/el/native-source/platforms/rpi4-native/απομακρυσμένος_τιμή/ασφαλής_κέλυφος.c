/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "απομακρυσμένος_τιμή.h"
#include "κρυπτογράφηση_στήριγμα.h"
#include "Προφίλ.h"
#include "../δίκτυο_δέσμη/δίκτυο_δέσμη.h"
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
static struct assh_context_s *περιβάλλον_τιμή;
static struct assh_session_s *σύνδεση_e05f319b;
static struct assh_channel_s *Κανάλι_καταχώρηση;
static int Ακρόαση_τελικό_σημείο=-1,ομότιμος_τιμή=-1,인증됨,셸시작됨,εντολή_Τύπος,Τελική_οντότητα_Κατάσταση=-1,닫을예정,시작오류,κέλυφος_Αναμονή;
static uintptr_t σύνδεση_ώρα,재접속시각,닫는시각;
static unsigned char είσοδος_γραμμή[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *λέξη_μήνυμα,unsigned τιμή) {
    while(*λέξη_μήνυμα)보드글자쓰기(*λέξη_μήνυμα++);
    char ψηφίο_τιμή[12];unsigned 수=0;do{ψηφίο_τιμή[수++]='0'+τιμή%10;τιμή/=10;}while(τιμή);
    while(수)보드글자쓰기(ψηφίο_τιμή[--수]);보드글자쓰기(10);
}
static assh_status_t Προετοίμασε_Μνήμη(void *δεδομένα,void **διεύθυνση,size_t Μέγεθος,enum assh_alloc_type_e 종류) {
    (void)δεδομένα;(void)종류;
    if(!Μέγεθος){έκδοση_απομακρυσμένος(*διεύθυνση);*διεύθυνση=0;return ASSH_OK;}
    void *새주소=원격재할당(*διεύθυνση,Μέγεθος);
    if(!새주소)return ASSH_ERR_MEM;*διεύθυνση=새주소;return ASSH_OK;
}
static assh_status_t Προετοίμασε_τυχαίος(struct assh_context_s *δεδομένα,const struct assh_buffer_s *αρχική_τιμή) {
    (void)δεδομένα;(void)αρχική_τιμή;unsigned char 시험[32];int μέτρηση=απομακρυσμένος_τυχαίος(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return μέτρηση?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *δεδομένα,uint8_t *μέτρηση,size_t διάρκεια_τιμή,uint_fast8_t 종류) {
    (void)δεδομένα;(void)종류;if(διάρκεια_τιμή>65536)return ASSH_ERR_CRYPTO;
    return απομακρυσμένος_τυχαίος(μέτρηση,διάρκεια_τιμή)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void τυχαίος_Τελική_οντότητα(struct assh_context_s *δεδομένα){(void)δεδομένα;}
static const struct assh_prng_s τυχαίος_δημιουργία={Προετοίμασε_τυχαίος,난수받기,τυχαίος_Τελική_οντότητα};
static void κλείνω_σύνδεση(void) {
    인증됨=셸시작됨=0;Κανάλι_καταχώρηση=0;
    if(σύνδεση_e05f319b)assh_session_release(σύνδεση_e05f319b);σύνδεση_e05f319b=0;
    if(ομότιμος_τιμή>=0)κλείνω_δίκτυο(ομότιμος_τιμή);ομότιμος_τιμή=-1;εντολή_Τύπος=0;Τελική_οντότητα_Κατάσταση=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int τροφοδοσία_απομακρυσμένος_είσοδος(const unsigned char *δεδομένα,unsigned 수) {
    if(수>sizeof(είσοδος_γραμμή)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)είσοδος_γραμμή[(입력앞+입력수++)%sizeof(είσοδος_γραμμή)]=δεδομένα[순번];return 수;
}
int απομακρυσμένος_είσοδος(void) {
    if(!입력수)return -1;int χαρακτήρας_τιμή=είσοδος_γραμμή[입력앞];입력앞=(입력앞+1)%sizeof(είσοδος_γραμμή);입력수--;return χαρακτήρας_τιμή;
}
void 원격출력(unsigned char χαρακτήρας_τιμή) {
    if(!셸시작됨||닫을예정)return;
    unsigned προσαρτώ_λειτουργία=χαρακτήρας_τιμή==10&&이전출력!=13;
    if(출력수+1+προσαρτώ_λειτουργία>sizeof(출력줄)){닫을예정=2;return;}
    if(προσαρτώ_λειτουργία)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=χαρακτήρας_τιμή;이전출력=χαρακτήρας_τιμή;
}
uintptr_t Πίνακας_Τελική_οντότητα_απομακρυσμένος_εντολή(uintptr_t Κατάσταση_τιμή){if(셸시작됨&&εντολή_Τύπος)Τελική_οντότητα_Κατάσταση=(int)Κατάσταση_τιμή;return 0;}
uintptr_t Πίνακας_απομακρυσμένος_περίμενε(uintptr_t Κατάσταση_τιμή){κέλυφος_Αναμονή=Κατάσταση_τιμή!=0;return 0;}
static int Προετοίμασε_κέλυφος(void) {
    if(Ακρόαση_τελικό_σημείο>=0)return 0;
    if(!περιβάλλον_τιμή){
        assh_status_t ΣΦΑΛΜΑ=assh_context_create(&περιβάλλον_τιμή,ASSH_SERVER,Προετοίμασε_Μνήμη,0,&τυχαίος_δημιουργία,0);
        if(ΣΦΑΛΜΑ)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *μέθοδος_λειτουργία[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ΣΦΑΛΜΑ=assh_algo_register(περιβάλλον_τιμή,ASSH_SAFETY_WEAK,μέθοδος_λειτουργία);
        if(!ΣΦΑΛΜΑ)ΣΦΑΛΜΑ=assh_service_register_va(περιβάλλον_τιμή,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=συσκευή_Κλειδί;
        if(!ΣΦΑΛΜΑ)ΣΦΑΛΜΑ=assh_key_load(περιβάλλον_τιμή,assh_context_keys(περιβάλλον_τιμή),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(συσκευή_Κλειδί));
        if(ΣΦΑΛΜΑ){진단("SSH init error ",ΣΦΑΛΜΑ);assh_context_release(περιβάλλον_τιμή);περιβάλλον_τιμή=0;return -5;}
    }
    int θύρα_τιμή=ανοίγω_υποδοχή_τελικό_σημείο(1);if(θύρα_τιμή<0)return θύρα_τιμή;통신주소재사용(θύρα_τιμή);
    int μέτρηση=망주소묶기(θύρα_τιμή,0,22);if(!μέτρηση)μέτρηση=연결기다리기(θύρα_τιμή);
    if(μέτρηση<0){κλείνω_δίκτυο(θύρα_τιμή);return μέτρηση;}Ακρόαση_τελικό_σημείο=θύρα_τιμή;return 0;
}
uintptr_t Πίνακας_απομακρυσμένος_έλεγχος(uintptr_t 종류,uintptr_t Ενέργεια) {
    if(종류==1)return(uint32_t)έλεγχος_απομακρυσμένος_οθόνη(Ενέργεια);
    if(Ενέργεια==0){κλείνω_σύνδεση();if(Ακρόαση_τελικό_σημείο>=0)κλείνω_δίκτυο(Ακρόαση_τελικό_σημείο);Ακρόαση_τελικό_σημείο=-1;return 0;}
    if(Ενέργεια==1){시작오류=Προετοίμασε_κέλυφος();return(uint32_t)시작오류;}
    return(uint32_t)(Ακρόαση_τελικό_σημείο>=0?1:시작오류);
}
void Προετοίμασε_απομακρυσμένος(void){시작오류=Προετοίμασε_κέλυφος();έλεγχος_απομακρυσμένος_οθόνη(1);}
static int 같은말(const struct assh_cbuffer_s *δεδομένα,const char *λέξη_μήνυμα) {
    size_t διάρκεια_τιμή=strlen(λέξη_μήνυμα);return δεδομένα->size==διάρκεια_τιμή&&!memcmp(δεδομένα->data,λέξη_μήνυμα,διάρκεια_τιμή);
}
static int Τερματικό_αίτηση(const struct assh_cbuffer_s *δεδομένα) {
    if(δεδομένα->size<24)return 0;
    const unsigned char *δεδομένα_θέση=δεδομένα->data;unsigned διάρκεια_τιμή=assh_load_u32(δεδομένα_θέση);
    if(διάρκεια_τιμή>128||δεδομένα->size<διάρκεια_τιμή+24)return 0;
    unsigned λειτουργία_τιμή=assh_load_u32(δεδομένα_θέση+4+διάρκεια_τιμή+16);
    return λειτουργία_τιμή<=2048&&δεδομένα->size==διάρκεια_τιμή+24+λειτουργία_τιμή;
}
static void δείκτης_χειρισμού_αίτηση(struct assh_event_request_s *Συμβάν) {
    if(!인증됨||Συμβάν->ch!=Κανάλι_καταχώρηση||!Κανάλι_καταχώρηση)return;
    if(같은말(&Συμβάν->type,"pty-req")) {
        if(!셸시작됨&&Τερματικό_αίτηση(&Συμβάν->rq_data))Συμβάν->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Συμβάν->type,"window-change")) {
        if(셸시작됨&&Συμβάν->rq_data.size==16)Συμβάν->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!κέλυφος_Αναμονή)return;
    const unsigned char *Εντολή=0;unsigned διάρκεια_τιμή=0;
    if(같은말(&Συμβάν->type,"exec")) {
        if(Συμβάν->rq_data.size<4)return;
        διάρκεια_τιμή=assh_load_u32(Συμβάν->rq_data.data);
        if(!διάρκεια_τιμή||διάρκεια_τιμή>2048||Συμβάν->rq_data.size!=διάρκεια_τιμή+4)return;
        Εντολή=Συμβάν->rq_data.data+4;
        for(unsigned 순번=0;순번<διάρκεια_τιμή;순번++)if(!Εντολή[순번])return;
        εντολή_Τύπος=1;
    }else if(!같은말(&Συμβάν->type,"shell")||Συμβάν->rq_data.size)return;
    if(sizeof(είσοδος_γραμμή)-입력수<διάρκεια_τιμή+2)return;
    const unsigned char 지움=21,끝=13;
    τροφοδοσία_απομακρυσμένος_είσοδος(&지움,1);if(διάρκεια_τιμή)τροφοδοσία_απομακρυσμένος_είσοδος(Εντολή,διάρκεια_τιμή);τροφοδοσία_απομακρυσμένος_είσοδος(&끝,1);
    셸시작됨=1;Συμβάν->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!εντολή_Τύπος){const char *αρχείο_readme_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*αρχείο_readme_eb81d7d9)원격출력(*αρχείο_readme_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Ακρόαση_τελικό_σημείο<0)return;
    uintptr_t 지금=보드밀리초();
    if(ομότιμος_τιμή<0){if(지금<재접속시각)return;ομότιμος_τιμή=망연결받기(Ακρόαση_τελικό_σημείο);if(ομότιμος_τιμή<0)return;
        σύνδεση_ώρα=지금;assh_status_t ΣΦΑΛΜΑ=assh_session_create(περιβάλλον_τιμή,&σύνδεση_e05f319b);
        if(ΣΦΑΛΜΑ){σύνδεση_e05f319b=0;진단("SSH session error ",ΣΦΑΛΜΑ);κλείνω_σύνδεση();return;}}
    if((!인증됨&&지금-σύνδεση_ώρα>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){κλείνω_σύνδεση();return;}
    if(Κανάλι_καταχώρηση&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ΣΦΑΛΜΑ=assh_channel_data(Κανάλι_καταχώρηση,출력줄+출력앞,&수);
            if(!ΣΦΑΛΜΑ){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ΣΦΑΛΜΑ!=ASSH_NO_DATA){κλείνω_σύνδεση();return;}
        }
        if(Τελική_οντότητα_Κατάσταση>=0&&!출력수){unsigned char Κατάσταση_τιμή[4];assh_store_u32(Κατάσταση_τιμή,(uint32_t)Τελική_οντότητα_Κατάσταση);
            if(assh_request(σύνδεση_e05f319b,Κανάλι_καταχώρηση,"exit-status",11,Κατάσταση_τιμή,4,0)||assh_channel_eof(Κανάλι_καταχώρηση)||assh_channel_close(Κανάλι_καταχώρηση)) {κλείνω_σύνδεση();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned ακολουθία_τιμή=0;ακολουθία_τιμή<16;ακολουθία_τιμή++) {
        struct assh_event_s Συμβάν;
        if(!assh_event_get(σύνδεση_e05f319b,&Συμβάν,지금/1000)){κλείνω_σύνδεση();return;}
        assh_status_t ΣΦΑΛΜΑ=ASSH_OK;int 쉬기=0,αποσυνδέω_τελικό_σημείο=0;
        switch(Συμβάν.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(ομότιμος_τιμή,Συμβάν.transport.read.buf.data,Συμβάν.transport.read.buf.size);
            if(수>0)Συμβάν.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else αποσυνδέω_τελικό_σημείο=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(ομότιμος_τιμή,Συμβάν.transport.write.buf.data,Συμβάν.transport.write.buf.size);
            if(수>0)Συμβάν.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else αποσυνδέω_τελικό_σημείο=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Συμβάν.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Συμβάν.userauth_server.methods.retries>3)Συμβάν.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *δεδομένα=&Συμβάν.userauth_server.password;
            if(같은말(&δεδομένα->username,"user")&&δεδομένα->password.size<=256&&!δεδομένα->new_password.size) {
                unsigned char σύνοψη_τιμή[32];απομακρυσμένος_σύνοψη(δεδομένα->password.data,δεδομένα->password.size,σύνοψη_τιμή);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=σύνοψη_τιμή[순번]^κέλυφος_κωδικός_πρόσβασης_σύνοψη[순번];memset(σύνοψη_τιμή,0,32);
                if(!차이)δεδομένα->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *δεδομένα=&Συμβάν.connection.channel_open;
            if(인증됨&&!Κανάλι_καταχώρηση&&κέλυφος_Αναμονή&&같은말(&δεδομένα->type,"session")&&!δεδομένα->rq_data.size) {
                δεδομένα->reply=ASSH_CONNECTION_REPLY_SUCCESS;δεδομένα->pkt_size=4096;
                δεδομένα->win_size=-1;Κανάλι_καταχώρηση=δεδομένα->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: δείκτης_χειρισμού_αίτηση(&Συμβάν.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *δεδομένα=&Συμβάν.connection.channel_data;
            if(!셸시작됨||δεδομένα->ch!=Κανάλι_καταχώρηση||δεδομένα->ext){αποσυνδέω_τελικό_σημείο=1;break;}
            unsigned 수=δεδομένα->data.size;if(수>sizeof(είσοδος_γραμμή)-입력수)수=sizeof(είσοδος_γραμμή)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(δεδομένα->data.data[순번]==4){Τελική_οντότητα_Κατάσταση=0;수=순번;δεδομένα->transferred=δεδομένα->data.size;break;}
            τροφοδοσία_απομακρυσμένος_είσοδος(δεδομένα->data.data,수);if(!δεδομένα->transferred)δεδομένα->transferred=수;
            if(!수&&Τελική_οντότητα_Κατάσταση<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Κανάλι_καταχώρηση=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Συμβάν.session.error.code);αποσυνδέω_τελικό_σημείο=1;break;
        case ASSH_EVENT_DISCONNECT: αποσυνδέω_τελικό_σημείο=1;break;
        default: break;
        }
        assh_event_done(σύνδεση_e05f319b,&Συμβάν,ΣΦΑΛΜΑ);
        if(αποσυνδέω_τελικό_σημείο){κλείνω_σύνδεση();return;}if(쉬기)return;
    }
}
