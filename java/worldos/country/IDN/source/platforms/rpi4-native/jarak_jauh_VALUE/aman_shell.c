/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "jarak_jauh_VALUE.h"
#include "암호기반.h"
#include "Profil.h"
#include "../jaringan_tumpuk/jaringan_tumpuk.h"
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
static struct assh_context_s *문맥;
static struct assh_session_s *koneksi_e05f319b;
static struct assh_channel_s *Saluran_entri;
static int Mendengarkan_peserta=-1,serekan_VALUE=-1,인증됨,셸시작됨,perintah_TYPE,mengakhiri_Status=-1,닫을예정,mulai_kesalahan,shell_Menunggu;
static uintptr_t koneksi_TIME,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Kata_SMS,unsigned VALUE) {
    while(*Kata_SMS)보드글자쓰기(*Kata_SMS++);
    char angka_VALUE[12];unsigned 수=0;do{angka_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(angka_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Siapkan_Memori(void *data,void **surel,size_t Ukuran,enum assh_alloc_type_e 종류) {
    (void)data;(void)종류;
    if(!Ukuran){lepas_jarak_jauh(*surel);*surel=0;return ASSH_OK;}
    void *새주소=원격재할당(*surel,Ukuran);
    if(!새주소)return ASSH_ERR_MEM;*surel=새주소;return ASSH_OK;
}
static assh_status_t Siapkan_acak(struct assh_context_s *data,const struct assh_buffer_s *nilai_awal) {
    (void)data;(void)nilai_awal;unsigned char pengujian[32];int hasil=jarak_jauh_acak(pengujian,sizeof(pengujian));memset(pengujian,0,sizeof(pengujian));
    return hasil?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *data,uint8_t *hasil,size_t panjang_VALUE,uint_fast8_t 종류) {
    (void)data;(void)종류;if(panjang_VALUE>65536)return ASSH_ERR_CRYPTO;
    return jarak_jauh_acak(hasil,panjang_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void acak_mengakhiri(struct assh_context_s *data){(void)data;}
static const struct assh_prng_s acak_generator={Siapkan_acak,난수받기,acak_mengakhiri};
static void Tutup_koneksi(void) {
    인증됨=셸시작됨=0;Saluran_entri=0;
    if(koneksi_e05f319b)assh_session_release(koneksi_e05f319b);koneksi_e05f319b=0;
    if(serekan_VALUE>=0)Tutup_jaringan(serekan_VALUE);serekan_VALUE=-1;perintah_TYPE=0;mengakhiri_Status=-1;닫을예정=0;
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
    unsigned tambah_MODE=karakter_VALUE==10&&이전출력!=13;
    if(출력수+1+tambah_MODE>sizeof(출력줄)){닫을예정=2;return;}
    if(tambah_MODE)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=karakter_VALUE;이전출력=karakter_VALUE;
}
uintptr_t Papan_mengakhiri_jarak_jauh_perintah(uintptr_t Status_VALUE){if(셸시작됨&&perintah_TYPE)mengakhiri_Status=(int)Status_VALUE;return 0;}
uintptr_t Papan_jarak_jauh_tunggu(uintptr_t Status_VALUE){shell_Menunggu=Status_VALUE!=0;return 0;}
static int Siapkan_shell(void) {
    if(Mendengarkan_peserta>=0)return 0;
    if(!문맥){
        assh_status_t galat=assh_context_create(&문맥,ASSH_SERVER,Siapkan_Memori,0,&acak_generator,0);
        if(galat)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metode_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        galat=assh_algo_register(문맥,ASSH_SAFETY_WEAK,metode_MODE);
        if(!galat)galat=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=Ponsel_Kunci;
        if(!galat)galat=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(Ponsel_Kunci));
        if(galat){진단("SSH init error ",galat);assh_context_release(문맥);문맥=0;return -5;}
    }
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int hasil=망주소묶기(port_VALUE,0,22);if(!hasil)hasil=연결기다리기(port_VALUE);
    if(hasil<0){Tutup_jaringan(port_VALUE);return hasil;}Mendengarkan_peserta=port_VALUE;return 0;
}
uintptr_t Papan_bayangan(uintptr_t 종류,uintptr_t Aksi) {
    if(종류==1)return(uint32_t)kontrol_jarak_jauh_tampilan(Aksi);
    if(Aksi==0){Tutup_koneksi();if(Mendengarkan_peserta>=0)Tutup_jaringan(Mendengarkan_peserta);Mendengarkan_peserta=-1;return 0;}
    if(Aksi==1){mulai_kesalahan=Siapkan_shell();return(uint32_t)mulai_kesalahan;}
    return(uint32_t)(Mendengarkan_peserta>=0?1:mulai_kesalahan);
}
void Siapkan_jarak_jauh(void){mulai_kesalahan=Siapkan_shell();kontrol_jarak_jauh_tampilan(1);}
static int 같은말(const struct assh_cbuffer_s *data,const char *Kata_SMS) {
    size_t panjang_VALUE=strlen(Kata_SMS);return data->size==panjang_VALUE&&!memcmp(data->data,Kata_SMS,panjang_VALUE);
}
static int Terminal_permintaan(const struct assh_cbuffer_s *data) {
    if(data->size<24)return 0;
    const unsigned char *data_posisi=data->data;unsigned panjang_VALUE=assh_load_u32(data_posisi);
    if(panjang_VALUE>128||data->size<panjang_VALUE+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(data_posisi+4+panjang_VALUE+16);
    return MODE_VALUE<=2048&&data->size==panjang_VALUE+24+MODE_VALUE;
}
static void handel_permintaan(struct assh_event_request_s *Even) {
    if(!인증됨||Even->ch!=Saluran_entri||!Saluran_entri)return;
    if(같은말(&Even->type,"pty-req")) {
        if(!셸시작됨&&Terminal_permintaan(&Even->rq_data))Even->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Even->type,"window-change")) {
        if(셸시작됨&&Even->rq_data.size==16)Even->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!shell_Menunggu)return;
    const unsigned char *perintah=0;unsigned panjang_VALUE=0;
    if(같은말(&Even->type,"exec")) {
        if(Even->rq_data.size<4)return;
        panjang_VALUE=assh_load_u32(Even->rq_data.data);
        if(!panjang_VALUE||panjang_VALUE>2048||Even->rq_data.size!=panjang_VALUE+4)return;
        perintah=Even->rq_data.data+4;
        for(unsigned 순번=0;순번<panjang_VALUE;순번++)if(!perintah[순번])return;
        perintah_TYPE=1;
    }else if(!같은말(&Even->type,"shell")||Even->rq_data.size)return;
    if(sizeof(입력줄)-입력수<panjang_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(panjang_VALUE)원격입력넣기(perintah,panjang_VALUE);원격입력넣기(&끝,1);
    셸시작됨=1;Even->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!perintah_TYPE){const char *baca_saya_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*baca_saya_eb81d7d9)원격출력(*baca_saya_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Mendengarkan_peserta<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(serekan_VALUE<0){if(NOW_VALUE<재접속시각)return;serekan_VALUE=망연결받기(Mendengarkan_peserta);if(serekan_VALUE<0)return;
        koneksi_TIME=NOW_VALUE;assh_status_t galat=assh_session_create(문맥,&koneksi_e05f319b);
        if(galat){koneksi_e05f319b=0;진단("SSH session error ",galat);Tutup_koneksi();return;}}
    if((!인증됨&&NOW_VALUE-koneksi_TIME>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){Tutup_koneksi();return;}
    if(Saluran_entri&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t galat=assh_channel_data(Saluran_entri,출력줄+출력앞,&수);
            if(!galat){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(galat!=ASSH_NO_DATA){Tutup_koneksi();return;}
        }
        if(mengakhiri_Status>=0&&!출력수){unsigned char Status_VALUE[4];assh_store_u32(Status_VALUE,(uint32_t)mengakhiri_Status);
            if(assh_request(koneksi_e05f319b,Saluran_entri,"exit-status",11,Status_VALUE,4,0)||assh_channel_eof(Saluran_entri)||assh_channel_close(Saluran_entri)) {Tutup_koneksi();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned urutan_VALUE_e9fa7815=0;urutan_VALUE_e9fa7815<16;urutan_VALUE_e9fa7815++) {
        struct assh_event_s Even;
        if(!assh_event_get(koneksi_e05f319b,&Even,NOW_VALUE/1000)){Tutup_koneksi();return;}
        assh_status_t galat=ASSH_OK;int 쉬기=0,putuskan_sambungan_peserta=0;
        switch(Even.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(serekan_VALUE,Even.transport.read.buf.data,Even.transport.read.buf.size);
            if(수>0)Even.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else putuskan_sambungan_peserta=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(serekan_VALUE,Even.transport.write.buf.data,Even.transport.write.buf.size);
            if(수>0)Even.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else putuskan_sambungan_peserta=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Even.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Even.userauth_server.methods.retries>3)Even.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *data=&Even.userauth_server.password;
            if(같은말(&data->username,"user")&&data->password.size<=256&&!data->new_password.size) {
                unsigned char ringkasan_VALUE[32];jarak_jauh_ringkasan(data->password.data,data->password.size,ringkasan_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=ringkasan_VALUE[순번]^shell_sandi_ringkasan[순번];memset(ringkasan_VALUE,0,32);
                if(!차이)data->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *data=&Even.connection.channel_open;
            if(인증됨&&!Saluran_entri&&shell_Menunggu&&같은말(&data->type,"session")&&!data->rq_data.size) {
                data->reply=ASSH_CONNECTION_REPLY_SUCCESS;data->pkt_size=4096;
                data->win_size=-1;Saluran_entri=data->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: handel_permintaan(&Even.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *data=&Even.connection.channel_data;
            if(!셸시작됨||data->ch!=Saluran_entri||data->ext){putuskan_sambungan_peserta=1;break;}
            unsigned 수=data->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(data->data.data[순번]==4){mengakhiri_Status=0;수=순번;data->transferred=data->data.size;break;}
            원격입력넣기(data->data.data,수);if(!data->transferred)data->transferred=수;
            if(!수&&mengakhiri_Status<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Saluran_entri=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Even.session.error.code);putuskan_sambungan_peserta=1;break;
        case ASSH_EVENT_DISCONNECT: putuskan_sambungan_peserta=1;break;
        default: break;
        }
        assh_event_done(koneksi_e05f319b,&Even,galat);
        if(putuskan_sambungan_peserta){Tutup_koneksi();return;}if(쉬기)return;
    }
}
