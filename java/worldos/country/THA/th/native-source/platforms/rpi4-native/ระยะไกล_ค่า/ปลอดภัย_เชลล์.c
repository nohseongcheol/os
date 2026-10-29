/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "ระยะไกล_ค่า.h"
#include "การเข้ารหัส_สนับสนุน.h"
#include "โปรไฟล์.h"
#include "../เครือข่าย_สแตก/เครือข่าย_สแตก.h"
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
static struct assh_context_s *บริบท_ค่า;
static struct assh_session_s *เพื่อน_e05f319b;
static struct assh_channel_s *ช่อง_รายการ;
static int กําลังฟัง_ปลายทาง=-1,ชั้น_ค่า=-1,인증됨,셸시작됨,คําสั่ง_ชนิด,สิ้นสุดการโทร_สถานะ=-1,닫을예정,เริ่มต้นระบบ_ข้อผิดพลาด,เชลล์_กําลังรอ;
static uintptr_t เพื่อน_เวลา,재접속시각,การปิดบัญชี_เวลา;
static unsigned char 입력줄[8192],ผลผลิต_สาย[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *คํา_ข้อความ,unsigned ค่า) {
    while(*คํา_ข้อความ)보드글자쓰기(*คํา_ข้อความ++);
    char ตัวเลข_ค่า[12];unsigned หมายเลข=0;do{ตัวเลข_ค่า[หมายเลข++]='0'+ค่า%10;ค่า/=10;}while(ค่า);
    while(หมายเลข)보드글자쓰기(ตัวเลข_ค่า[--หมายเลข]);보드글자쓰기(10);
}
static assh_status_t จัดเตรียม_ความจํา(void *ข้อมูล,void **อีเมล,size_t ขนาด,enum assh_alloc_type_e 종류) {
    (void)ข้อมูล;(void)종류;
    if(!ขนาด){ปล่อย_ระยะไกล(*อีเมล);*อีเมล=0;return ASSH_OK;}
    void *새주소=원격재할당(*อีเมล,ขนาด);
    if(!새주소)return ASSH_ERR_MEM;*อีเมล=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *ข้อมูล,const struct assh_buffer_s *ค่าข้อมูลเริ่มต้น) {
    (void)ข้อมูล;(void)ค่าข้อมูลเริ่มต้น;unsigned char 시험[32];int ผลลัพธ์=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return ผลลัพธ์?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *ข้อมูล,uint8_t *ผลลัพธ์,size_t 길이,uint_fast8_t 종류) {
    (void)ข้อมูล;(void)종류;if(길이>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(ผลลัพธ์,길이)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *ข้อมูล){(void)ข้อมูล;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void ปิด_เพื่อน(void) {
    인증됨=셸시작됨=0;ช่อง_รายการ=0;
    if(เพื่อน_e05f319b)assh_session_release(เพื่อน_e05f319b);เพื่อน_e05f319b=0;
    if(ชั้น_ค่า>=0)ปิด_เครือข่าย(ชั้น_ค่า);ชั้น_ค่า=-1;คําสั่ง_ชนิด=0;สิ้นสุดการโทร_สถานะ=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *ข้อมูล,unsigned หมายเลข) {
    if(หมายเลข>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<หมายเลข;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=ข้อมูล[순번];return หมายเลข;
}
int 원격입력(void) {
    if(!입력수)return -1;int อักขระ_ค่า=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return อักขระ_ค่า;
}
void ระยะไกล_ผลผลิต(unsigned char อักขระ_ค่า) {
    if(!셸시작됨||닫을예정)return;
    unsigned ผนวก_โหมด=อักขระ_ค่า==10&&이전출력!=13;
    if(출력수+1+ผนวก_โหมด>sizeof(ผลผลิต_สาย)){닫을예정=2;return;}
    if(ผนวก_โหมด)ผลผลิต_สาย[(출력앞+출력수++)%sizeof(ผลผลิต_สาย)]=13;
    ผลผลิต_สาย[(출력앞+출력수++)%sizeof(ผลผลิต_สาย)]=อักขระ_ค่า;이전출력=อักขระ_ค่า;
}
uintptr_t บอร์ด_สิ้นสุดการโทร_ระยะไกล_คําสั่ง(uintptr_t สถานะ_ค่า){if(셸시작됨&&คําสั่ง_ชนิด)สิ้นสุดการโทร_สถานะ=(int)สถานะ_ค่า;return 0;}
uintptr_t บอร์ด_ระยะไกล_รอเดี๋ยว(uintptr_t สถานะ_ค่า){เชลล์_กําลังรอ=สถานะ_ค่า!=0;return 0;}
static int จัดเตรียม_เชลล์(void) {
    if(กําลังฟัง_ปลายทาง>=0)return 0;
    if(!บริบท_ค่า){
        assh_status_t ข้อผิดพลาด=assh_context_create(&บริบท_ค่า,ASSH_SERVER,จัดเตรียม_ความจํา,0,&난수기,0);
        if(ข้อผิดพลาด)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *เมธอด_โหมด[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ข้อผิดพลาด=assh_algo_register(บริบท_ค่า,ASSH_SAFETY_WEAK,เมธอด_โหมด);
        if(!ข้อผิดพลาด)ข้อผิดพลาด=assh_service_register_va(บริบท_ค่า,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=อุปกรณ์_คีย์;
        if(!ข้อผิดพลาด)ข้อผิดพลาด=assh_key_load(บริบท_ค่า,assh_context_keys(บริบท_ค่า),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(อุปกรณ์_คีย์));
        if(ข้อผิดพลาด){진단("SSH init error ",ข้อผิดพลาด);assh_context_release(บริบท_ค่า);บริบท_ค่า=0;return -5;}
    }
    int แปลง_ค่า=통신끝점만들기(1);if(แปลง_ค่า<0)return แปลง_ค่า;통신주소재사용(แปลง_ค่า);
    int ผลลัพธ์=สุทธิ_ผูก(แปลง_ค่า,0,22);if(!ผลลัพธ์)ผลลัพธ์=สุทธิ_รอการติดต่อ(แปลง_ค่า);
    if(ผลลัพธ์<0){ปิด_เครือข่าย(แปลง_ค่า);return ผลลัพธ์;}กําลังฟัง_ปลายทาง=แปลง_ค่า;return 0;
}
uintptr_t บอร์ด_การควบคุมระยะไกล(uintptr_t 종류,uintptr_t การกระทํา) {
    if(종류==1)return(uint32_t)ควบคุม_ระยะไกล_แสดง(การกระทํา);
    if(การกระทํา==0){ปิด_เพื่อน();if(กําลังฟัง_ปลายทาง>=0)ปิด_เครือข่าย(กําลังฟัง_ปลายทาง);กําลังฟัง_ปลายทาง=-1;return 0;}
    if(การกระทํา==1){เริ่มต้นระบบ_ข้อผิดพลาด=จัดเตรียม_เชลล์();return(uint32_t)เริ่มต้นระบบ_ข้อผิดพลาด;}
    return(uint32_t)(กําลังฟัง_ปลายทาง>=0?1:เริ่มต้นระบบ_ข้อผิดพลาด);
}
void จัดเตรียม_ระยะไกล(void){เริ่มต้นระบบ_ข้อผิดพลาด=จัดเตรียม_เชลล์();ควบคุม_ระยะไกล_แสดง(1);}
static int 같은말(const struct assh_cbuffer_s *ข้อมูล,const char *คํา_ข้อความ) {
    size_t 길이=strlen(คํา_ข้อความ);return ข้อมูล->size==길이&&!memcmp(ข้อมูล->data,คํา_ข้อความ,길이);
}
static int เทอร์มินัล_คําขอ(const struct assh_cbuffer_s *ข้อมูล) {
    if(ข้อมูล->size<24)return 0;
    const unsigned char *ข้อมูล_ตําแหน่ง=ข้อมูล->data;unsigned 길이=assh_load_u32(ข้อมูล_ตําแหน่ง);
    if(길이>128||ข้อมูล->size<길이+24)return 0;
    unsigned โหมด_ค่า=assh_load_u32(ข้อมูล_ตําแหน่ง+4+길이+16);
    return โหมด_ค่า<=2048&&ข้อมูล->size==길이+24+โหมด_ค่า;
}
static void จุดจับ_คําขอ(struct assh_event_request_s *เหตุการณ์) {
    if(!인증됨||เหตุการณ์->ch!=ช่อง_รายการ||!ช่อง_รายการ)return;
    if(같은말(&เหตุการณ์->type,"pty-req")) {
        if(!셸시작됨&&เทอร์มินัล_คําขอ(&เหตุการณ์->rq_data))เหตุการณ์->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&เหตุการณ์->type,"window-change")) {
        if(셸시작됨&&เหตุการณ์->rq_data.size==16)เหตุการณ์->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!เชลล์_กําลังรอ)return;
    const unsigned char *คําสั่ง=0;unsigned 길이=0;
    if(같은말(&เหตุการณ์->type,"exec")) {
        if(เหตุการณ์->rq_data.size<4)return;
        길이=assh_load_u32(เหตุการณ์->rq_data.data);
        if(!길이||길이>2048||เหตุการณ์->rq_data.size!=길이+4)return;
        คําสั่ง=เหตุการณ์->rq_data.data+4;
        for(unsigned 순번=0;순번<길이;순번++)if(!คําสั่ง[순번])return;
        คําสั่ง_ชนิด=1;
    }else if(!같은말(&เหตุการณ์->type,"shell")||เหตุการณ์->rq_data.size)return;
    if(sizeof(입력줄)-입력수<길이+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(길이)원격입력넣기(คําสั่ง,길이);원격입력넣기(&끝,1);
    셸시작됨=1;เหตุการณ์->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!คําสั่ง_ชนิด){const char *안내="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*안내)ระยะไกล_ผลผลิต(*안내++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(กําลังฟัง_ปลายทาง<0)return;
    uintptr_t 지금=보드밀리초();
    if(ชั้น_ค่า<0){if(지금<재접속시각)return;ชั้น_ค่า=สุทธิ_ยอมรับ(กําลังฟัง_ปลายทาง);if(ชั้น_ค่า<0)return;
        เพื่อน_เวลา=지금;assh_status_t ข้อผิดพลาด=assh_session_create(บริบท_ค่า,&เพื่อน_e05f319b);
        if(ข้อผิดพลาด){เพื่อน_e05f319b=0;진단("SSH session error ",ข้อผิดพลาด);ปิด_เพื่อน();return;}}
    if((!인증됨&&지금-เพื่อน_เวลา>30000)||닫을예정==2||(닫을예정&&지금>=การปิดบัญชี_เวลา)){ปิด_เพื่อน();return;}
    if(ช่อง_รายการ&&셸시작됨&&!닫을예정) {
        if(출력수){size_t หมายเลข=sizeof(ผลผลิต_สาย)-출력앞;if(หมายเลข>출력수)หมายเลข=출력수;if(หมายเลข>2048)หมายเลข=2048;
            assh_status_t ข้อผิดพลาด=assh_channel_data(ช่อง_รายการ,ผลผลิต_สาย+출력앞,&หมายเลข);
            if(!ข้อผิดพลาด){출력앞=(출력앞+หมายเลข)%sizeof(ผลผลิต_สาย);출력수-=หมายเลข;}
            else if(ข้อผิดพลาด!=ASSH_NO_DATA){ปิด_เพื่อน();return;}
        }
        if(สิ้นสุดการโทร_สถานะ>=0&&!출력수){unsigned char สถานะ_ค่า[4];assh_store_u32(สถานะ_ค่า,(uint32_t)สิ้นสุดการโทร_สถานะ);
            if(assh_request(เพื่อน_e05f319b,ช่อง_รายการ,"exit-status",11,สถานะ_ค่า,4,0)||assh_channel_eof(ช่อง_รายการ)||assh_channel_close(ช่อง_รายการ)) {ปิด_เพื่อน();return;}
            닫을예정=1;การปิดบัญชี_เวลา=지금+3000;
        }
    }
    for(unsigned ลําดับ_ค่า_e9fa7815=0;ลําดับ_ค่า_e9fa7815<16;ลําดับ_ค่า_e9fa7815++) {
        struct assh_event_s เหตุการณ์;
        if(!assh_event_get(เพื่อน_e05f319b,&เหตุการณ์,지금/1000)){ปิด_เพื่อน();return;}
        assh_status_t ข้อผิดพลาด=ASSH_OK;int 쉬기=0,ยกเลิกการเชื่อมต่อ_ปลายทาง=0;
        switch(เหตุการณ์.id) {
        case ASSH_EVENT_READ: {
            int หมายเลข=통신읽기(ชั้น_ค่า,เหตุการณ์.transport.read.buf.data,เหตุการณ์.transport.read.buf.size);
            if(หมายเลข>0)เหตุการณ์.transport.read.transferred=หมายเลข;
            else if(หมายเลข==-11)쉬기=1;else ยกเลิกการเชื่อมต่อ_ปลายทาง=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int หมายเลข=통신쓰기(ชั้น_ค่า,เหตุการณ์.transport.write.buf.data,เหตุการณ์.transport.write.buf.size);
            if(หมายเลข>0)เหตุการณ์.transport.write.transferred=หมายเลข;
            else if(หมายเลข==-11)쉬기=1;else ยกเลิกการเชื่อมต่อ_ปลายทาง=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            เหตุการณ์.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(เหตุการณ์.userauth_server.methods.retries>3)เหตุการณ์.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *ข้อมูล=&เหตุการณ์.userauth_server.password;
            if(같은말(&ข้อมูล->username,"user")&&ข้อมูล->password.size<=256&&!ข้อมูล->new_password.size) {
                unsigned char สรุป_ค่า[32];ระยะไกล_สรุป(ข้อมูล->password.data,ข้อมูล->password.size,สรุป_ค่า);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=สรุป_ค่า[순번]^เชลล์_รหัสผ่าน_สรุป[순번];memset(สรุป_ค่า,0,32);
                if(!차이)ข้อมูล->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *ข้อมูล=&เหตุการณ์.connection.channel_open;
            if(인증됨&&!ช่อง_รายการ&&เชลล์_กําลังรอ&&같은말(&ข้อมูล->type,"session")&&!ข้อมูล->rq_data.size) {
                ข้อมูล->reply=ASSH_CONNECTION_REPLY_SUCCESS;ข้อมูล->pkt_size=4096;
                ข้อมูล->win_size=-1;ช่อง_รายการ=ข้อมูล->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: จุดจับ_คําขอ(&เหตุการณ์.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *ข้อมูล=&เหตุการณ์.connection.channel_data;
            if(!셸시작됨||ข้อมูล->ch!=ช่อง_รายการ||ข้อมูล->ext){ยกเลิกการเชื่อมต่อ_ปลายทาง=1;break;}
            unsigned หมายเลข=ข้อมูล->data.size;if(หมายเลข>sizeof(입력줄)-입력수)หมายเลข=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<หมายเลข;순번++)if(ข้อมูล->data.data[순번]==4){สิ้นสุดการโทร_สถานะ=0;หมายเลข=순번;ข้อมูล->transferred=ข้อมูล->data.size;break;}
            원격입력넣기(ข้อมูล->data.data,หมายเลข);if(!ข้อมูล->transferred)ข้อมูล->transferred=หมายเลข;
            if(!หมายเลข&&สิ้นสุดการโทร_สถานะ<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: ช่อง_รายการ=0;셸시작됨=0;닫을예정=1;การปิดบัญชี_เวลา=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",เหตุการณ์.session.error.code);ยกเลิกการเชื่อมต่อ_ปลายทาง=1;break;
        case ASSH_EVENT_DISCONNECT: ยกเลิกการเชื่อมต่อ_ปลายทาง=1;break;
        default: break;
        }
        assh_event_done(เพื่อน_e05f319b,&เหตุการณ์,ข้อผิดพลาด);
        if(ยกเลิกการเชื่อมต่อ_ปลายทาง){ปิด_เพื่อน();return;}if(쉬기)return;
    }
}
