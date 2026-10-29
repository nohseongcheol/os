/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "ທາງ_ໄກ_ຄ່າ.h"
#include "암호기반.h"
#include "ໂປຣໄຟລ໌.h"
#include "../ເຄືອຂ່າຍ_ກຸ່ມບັດ/ເຄືອຂ່າຍ_ກຸ່ມບັດ.h"
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
static struct assh_context_s *ສະ_ພາບ_ເນື້ອ_ໃນ_ຄ່າ;
static struct assh_session_s *ການເຊື່ອມຕໍ່_e05f319b;
static struct assh_channel_s *ຊ່ອງທາງ_ເຂົ້າໃນ;
static int 듣는곳=-1,ລຸ້ນດຽວກັນ_ຄ່າ=-1,인증됨,셸시작됨,ຄໍາສັ່ງ_ພິມ,ຈົບ_ສະຖານະ=-1,닫을예정,ການ_ເລີ່ມ_ຕົ້ນ_ຂໍ້ຜິດພາດ,ເຊລ_ກໍາ_ລັງລໍຖ້າ;
static uintptr_t ການເຊື່ອມຕໍ່_ເວລາ,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ,unsigned ຄ່າ) {
    while(*ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ)보드글자쓰기(*ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ++);
    char ຕົວເລກ_ຄ່າ[12];unsigned 수=0;do{ຕົວເລກ_ຄ່າ[수++]='0'+ຄ່າ%10;ຄ່າ/=10;}while(ຄ່າ);
    while(수)보드글자쓰기(ຕົວເລກ_ຄ່າ[--수]);보드글자쓰기(10);
}
static assh_status_t ກະ_ກຽມ_ຄວາມຈໍາ(void *ຂໍ້ມູນ,void **ອີເມວ,size_t ຂະ_ຫນາດ,enum assh_alloc_type_e 종류) {
    (void)ຂໍ້ມູນ;(void)종류;
    if(!ຂະ_ຫນາດ){ເວີຊັນ_ທາງ_ໄກ(*ອີເມວ);*ອີເມວ=0;return ASSH_OK;}
    void *새주소=원격재할당(*ອີເມວ,ຂະ_ຫນາດ);
    if(!새주소)return ASSH_ERR_MEM;*ອີເມວ=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *ຂໍ້ມູນ,const struct assh_buffer_s *ຊີດ_ຄ່າ) {
    (void)ຂໍ້ມູນ;(void)ຊີດ_ຄ່າ;unsigned char 시험[32];int ມາດຕະການ=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return ມາດຕະການ?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *ຂໍ້ມູນ,uint8_t *ມາດຕະການ,size_t ຄວາມຍາວ_ຄ່າ,uint_fast8_t 종류) {
    (void)ຂໍ້ມູນ;(void)종류;if(ຄວາມຍາວ_ຄ່າ>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(ມາດຕະການ,ຄວາມຍາວ_ຄ່າ)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *ຂໍ້ມູນ){(void)ຂໍ້ມູນ;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void ປິດ_ການເຊື່ອມຕໍ່(void) {
    인증됨=셸시작됨=0;ຊ່ອງທາງ_ເຂົ້າໃນ=0;
    if(ການເຊື່ອມຕໍ່_e05f319b)assh_session_release(ການເຊື່ອມຕໍ່_e05f319b);ການເຊື່ອມຕໍ່_e05f319b=0;
    if(ລຸ້ນດຽວກັນ_ຄ່າ>=0)ປິດ_ເຄືອຂ່າຍ(ລຸ້ນດຽວກັນ_ຄ່າ);ລຸ້ນດຽວກັນ_ຄ່າ=-1;ຄໍາສັ່ງ_ພິມ=0;ຈົບ_ສະຖານະ=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *ຂໍ້ມູນ,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=ຂໍ້ມູນ[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int ຕົວອັກສອນ_ຄ່າ=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return ຕົວອັກສອນ_ຄ່າ;
}
void 원격출력(unsigned char ຕົວອັກສອນ_ຄ່າ) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=ຕົວອັກສອນ_ຄ່າ==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=ຕົວອັກສອນ_ຄ່າ;이전출력=ຕົວອັກສອນ_ຄ່າ;
}
uintptr_t ກະດານ_ຈົບ_ທາງ_ໄກ_ຄໍາສັ່ງ(uintptr_t ສະຖານະ_ຄ່າ){if(셸시작됨&&ຄໍາສັ່ງ_ພິມ)ຈົບ_ສະຖານະ=(int)ສະຖານະ_ຄ່າ;return 0;}
uintptr_t ກະດານ_ທາງ_ໄກ_ລໍຖ້າ(uintptr_t ສະຖານະ_ຄ່າ){ເຊລ_ກໍາ_ລັງລໍຖ້າ=ສະຖານະ_ຄ່າ!=0;return 0;}
static int ກະ_ກຽມ_ເຊລ(void) {
    if(듣는곳>=0)return 0;
    if(!ສະ_ພາບ_ເນື້ອ_ໃນ_ຄ່າ){
        assh_status_t ຂໍ້ຜິດພາດ=assh_context_create(&ສະ_ພາບ_ເນື້ອ_ໃນ_ຄ່າ,ASSH_SERVER,ກະ_ກຽມ_ຄວາມຈໍາ,0,&난수기,0);
        if(ຂໍ້ຜິດພາດ)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *ວິ_ທີ_ໂຫມດ[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ຂໍ້ຜິດພາດ=assh_algo_register(ສະ_ພາບ_ເນື້ອ_ໃນ_ຄ່າ,ASSH_SAFETY_WEAK,ວິ_ທີ_ໂຫມດ);
        if(!ຂໍ້ຜິດພາດ)ຂໍ້ຜິດພາດ=assh_service_register_va(ສະ_ພາບ_ເນື້ອ_ໃນ_ຄ່າ,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=ມືຖື_ກະແຈ;
        if(!ຂໍ້ຜິດພາດ)ຂໍ້ຜິດພາດ=assh_key_load(ສະ_ພາບ_ເນື້ອ_ໃນ_ຄ່າ,assh_context_keys(ສະ_ພາບ_ເນື້ອ_ໃນ_ຄ່າ),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(ມືຖື_ກະແຈ));
        if(ຂໍ້ຜິດພາດ){진단("SSH init error ",ຂໍ້ຜິດພາດ);assh_context_release(ສະ_ພາບ_ເນື້ອ_ໃນ_ຄ່າ);ສະ_ພາບ_ເນື້ອ_ໃນ_ຄ່າ=0;return -5;}
    }
    int ຜອດ_ຄ່າ=통신끝점만들기(1);if(ຜອດ_ຄ່າ<0)return ຜອດ_ຄ່າ;통신주소재사용(ຜອດ_ຄ່າ);
    int ມາດຕະການ=망주소묶기(ຜອດ_ຄ່າ,0,22);if(!ມາດຕະການ)ມາດຕະການ=연결기다리기(ຜອດ_ຄ່າ);
    if(ມາດຕະການ<0){ປິດ_ເຄືອຂ່າຍ(ຜອດ_ຄ່າ);return ມາດຕະການ;}듣는곳=ຜອດ_ຄ່າ;return 0;
}
uintptr_t ກະດານ_ທາງ_ໄກ_ຄວບຄຸມ(uintptr_t 종류,uintptr_t ຄໍາສັ່ງ) {
    if(종류==1)return(uint32_t)ຄວບຄຸມ_ທາງ_ໄກ_ສະແດງຜົນ(ຄໍາສັ່ງ);
    if(ຄໍາສັ່ງ==0){ປິດ_ການເຊື່ອມຕໍ່();if(듣는곳>=0)ປິດ_ເຄືອຂ່າຍ(듣는곳);듣는곳=-1;return 0;}
    if(ຄໍາສັ່ງ==1){ການ_ເລີ່ມ_ຕົ້ນ_ຂໍ້ຜິດພາດ=ກະ_ກຽມ_ເຊລ();return(uint32_t)ການ_ເລີ່ມ_ຕົ້ນ_ຂໍ້ຜິດພາດ;}
    return(uint32_t)(듣는곳>=0?1:ການ_ເລີ່ມ_ຕົ້ນ_ຂໍ້ຜິດພາດ);
}
void ກະ_ກຽມ_ທາງ_ໄກ(void){ການ_ເລີ່ມ_ຕົ້ນ_ຂໍ້ຜິດພາດ=ກະ_ກຽມ_ເຊລ();ຄວບຄຸມ_ທາງ_ໄກ_ສະແດງຜົນ(1);}
static int 같은말(const struct assh_cbuffer_s *ຂໍ້ມູນ,const char *ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ) {
    size_t ຄວາມຍາວ_ຄ່າ=strlen(ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ);return ຂໍ້ມູນ->size==ຄວາມຍາວ_ຄ່າ&&!memcmp(ຂໍ້ມູນ->data,ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ,ຄວາມຍາວ_ຄ່າ);
}
static int 터미널요청(const struct assh_cbuffer_s *ຂໍ້ມູນ) {
    if(ຂໍ້ມູນ->size<24)return 0;
    const unsigned char *ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ=ຂໍ້ມູນ->data;unsigned ຄວາມຍາວ_ຄ່າ=assh_load_u32(ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ);
    if(ຄວາມຍາວ_ຄ່າ>128||ຂໍ້ມູນ->size<ຄວາມຍາວ_ຄ່າ+24)return 0;
    unsigned ໂຫມດ_ຄ່າ=assh_load_u32(ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ+4+ຄວາມຍາວ_ຄ່າ+16);
    return ໂຫມດ_ຄ່າ<=2048&&ຂໍ້ມູນ->size==ຄວາມຍາວ_ຄ່າ+24+ໂຫມດ_ຄ່າ;
}
static void 요청처리(struct assh_event_request_s *ງານ) {
    if(!인증됨||ງານ->ch!=ຊ່ອງທາງ_ເຂົ້າໃນ||!ຊ່ອງທາງ_ເຂົ້າໃນ)return;
    if(같은말(&ງານ->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&ງານ->rq_data))ງານ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&ງານ->type,"window-change")) {
        if(셸시작됨&&ງານ->rq_data.size==16)ງານ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!ເຊລ_ກໍາ_ລັງລໍຖ້າ)return;
    const unsigned char *ຄໍາສັ່ງ_1f12b8e2=0;unsigned ຄວາມຍາວ_ຄ່າ=0;
    if(같은말(&ງານ->type,"exec")) {
        if(ງານ->rq_data.size<4)return;
        ຄວາມຍາວ_ຄ່າ=assh_load_u32(ງານ->rq_data.data);
        if(!ຄວາມຍາວ_ຄ່າ||ຄວາມຍາວ_ຄ່າ>2048||ງານ->rq_data.size!=ຄວາມຍາວ_ຄ່າ+4)return;
        ຄໍາສັ່ງ_1f12b8e2=ງານ->rq_data.data+4;
        for(unsigned 순번=0;순번<ຄວາມຍາວ_ຄ່າ;순번++)if(!ຄໍາສັ່ງ_1f12b8e2[순번])return;
        ຄໍາສັ່ງ_ພິມ=1;
    }else if(!같은말(&ງານ->type,"shell")||ງານ->rq_data.size)return;
    if(sizeof(입력줄)-입력수<ຄວາມຍາວ_ຄ່າ+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(ຄວາມຍາວ_ຄ່າ)원격입력넣기(ຄໍາສັ່ງ_1f12b8e2,ຄວາມຍາວ_ຄ່າ);원격입력넣기(&끝,1);
    셸시작됨=1;ງານ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!ຄໍາສັ່ງ_ພິມ){const char *ຂໍ້ແນະນໍາການໃຊ້_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*ຂໍ້ແນະນໍາການໃຊ້_eb81d7d9)원격출력(*ຂໍ້ແນະນໍາການໃຊ້_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(ລຸ້ນດຽວກັນ_ຄ່າ<0){if(지금<재접속시각)return;ລຸ້ນດຽວກັນ_ຄ່າ=망연결받기(듣는곳);if(ລຸ້ນດຽວກັນ_ຄ່າ<0)return;
        ການເຊື່ອມຕໍ່_ເວລາ=지금;assh_status_t ຂໍ້ຜິດພາດ=assh_session_create(ສະ_ພາບ_ເນື້ອ_ໃນ_ຄ່າ,&ການເຊື່ອມຕໍ່_e05f319b);
        if(ຂໍ້ຜິດພາດ){ການເຊື່ອມຕໍ່_e05f319b=0;진단("SSH session error ",ຂໍ້ຜິດພາດ);ປິດ_ການເຊື່ອມຕໍ່();return;}}
    if((!인증됨&&지금-ການເຊື່ອມຕໍ່_ເວລາ>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){ປິດ_ການເຊື່ອມຕໍ່();return;}
    if(ຊ່ອງທາງ_ເຂົ້າໃນ&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ຂໍ້ຜິດພາດ=assh_channel_data(ຊ່ອງທາງ_ເຂົ້າໃນ,출력줄+출력앞,&수);
            if(!ຂໍ້ຜິດພາດ){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ຂໍ້ຜິດພາດ!=ASSH_NO_DATA){ປິດ_ການເຊື່ອມຕໍ່();return;}
        }
        if(ຈົບ_ສະຖານະ>=0&&!출력수){unsigned char ສະຖານະ_ຄ່າ[4];assh_store_u32(ສະຖານະ_ຄ່າ,(uint32_t)ຈົບ_ສະຖານະ);
            if(assh_request(ການເຊື່ອມຕໍ່_e05f319b,ຊ່ອງທາງ_ເຂົ້າໃນ,"exit-status",11,ສະຖານະ_ຄ່າ,4,0)||assh_channel_eof(ຊ່ອງທາງ_ເຂົ້າໃນ)||assh_channel_close(ຊ່ອງທາງ_ເຂົ້າໃນ)) {ປິດ_ການເຊື່ອມຕໍ່();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s ງານ;
        if(!assh_event_get(ການເຊື່ອມຕໍ່_e05f319b,&ງານ,지금/1000)){ປິດ_ການເຊື່ອມຕໍ່();return;}
        assh_status_t ຂໍ້ຜິດພາດ=ASSH_OK;int 쉬기=0,끊기=0;
        switch(ງານ.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(ລຸ້ນດຽວກັນ_ຄ່າ,ງານ.transport.read.buf.data,ງານ.transport.read.buf.size);
            if(수>0)ງານ.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(ລຸ້ນດຽວກັນ_ຄ່າ,ງານ.transport.write.buf.data,ງານ.transport.write.buf.size);
            if(수>0)ງານ.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ງານ.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ງານ.userauth_server.methods.retries>3)ງານ.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *ຂໍ້ມູນ=&ງານ.userauth_server.password;
            if(같은말(&ຂໍ້ມູນ->username,"user")&&ຂໍ້ມູນ->password.size<=256&&!ຂໍ້ມູນ->new_password.size) {
                unsigned char 요약[32];원격요약(ຂໍ້ມູນ->password.data,ຂໍ້ມູນ->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)ຂໍ້ມູນ->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *ຂໍ້ມູນ=&ງານ.connection.channel_open;
            if(인증됨&&!ຊ່ອງທາງ_ເຂົ້າໃນ&&ເຊລ_ກໍາ_ລັງລໍຖ້າ&&같은말(&ຂໍ້ມູນ->type,"session")&&!ຂໍ້ມູນ->rq_data.size) {
                ຂໍ້ມູນ->reply=ASSH_CONNECTION_REPLY_SUCCESS;ຂໍ້ມູນ->pkt_size=4096;
                ຂໍ້ມູນ->win_size=-1;ຊ່ອງທາງ_ເຂົ້າໃນ=ຂໍ້ມູນ->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&ງານ.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *ຂໍ້ມູນ=&ງານ.connection.channel_data;
            if(!셸시작됨||ຂໍ້ມູນ->ch!=ຊ່ອງທາງ_ເຂົ້າໃນ||ຂໍ້ມູນ->ext){끊기=1;break;}
            unsigned 수=ຂໍ້ມູນ->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(ຂໍ້ມູນ->data.data[순번]==4){ຈົບ_ສະຖານະ=0;수=순번;ຂໍ້ມູນ->transferred=ຂໍ້ມູນ->data.size;break;}
            원격입력넣기(ຂໍ້ມູນ->data.data,수);if(!ຂໍ້ມູນ->transferred)ຂໍ້ມູນ->transferred=수;
            if(!수&&ຈົບ_ສະຖານະ<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: ຊ່ອງທາງ_ເຂົ້າໃນ=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",ງານ.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(ການເຊື່ອມຕໍ່_e05f319b,&ງານ,ຂໍ້ຜິດພາດ);
        if(끊기){ປິດ_ການເຊື່ອມຕໍ່();return;}if(쉬기)return;
    }
}
