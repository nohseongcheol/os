/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "jauh_VALUE.h"
#include "kriptografi_Sokongan.h"
#include "Profil.h"
#include "../rangkaian_tindan/rangkaian_tindan.h"
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
static struct assh_context_s *konteks_VALUE;
static struct assh_session_s *hubungan_e05f319b;
static struct assh_channel_s *Saluran_pemasukan;
static int Mendengar_peserta=-1,rakan_VALUE=-1,인증됨,셸시작됨,perintah_TYPE,tamat_status=-1,닫을예정,butstrap_ralat,cangkerang_Menunggu;
static uintptr_t hubungan_TIME,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char digit_VALUE[12];unsigned 수=0;do{digit_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(digit_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Sediakan_Memori(void *data,void **e_mel,size_t Saiz,enum assh_alloc_type_e 종류) {
    (void)data;(void)종류;
    if(!Saiz){keluaran_jauh(*e_mel);*e_mel=0;return ASSH_OK;}
    void *새주소=원격재할당(*e_mel,Saiz);
    if(!새주소)return ASSH_ERR_MEM;*e_mel=새주소;return ASSH_OK;
}
static assh_status_t Sediakan_rawak(struct assh_context_s *data,const struct assh_buffer_s *nilai_benih) {
    (void)data;(void)nilai_benih;unsigned char ujian[32];int ukuran=jauh_rawak(ujian,sizeof(ujian));memset(ujian,0,sizeof(ujian));
    return ukuran?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *data,uint8_t *ukuran,size_t kepanjangan_VALUE,uint_fast8_t 종류) {
    (void)data;(void)종류;if(kepanjangan_VALUE>65536)return ASSH_ERR_CRYPTO;
    return jauh_rawak(ukuran,kepanjangan_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void rawak_tamat(struct assh_context_s *data){(void)data;}
static const struct assh_prng_s rawak_penjana={Sediakan_rawak,난수받기,rawak_tamat};
static void Tutup_hubungan(void) {
    인증됨=셸시작됨=0;Saluran_pemasukan=0;
    if(hubungan_e05f319b)assh_session_release(hubungan_e05f319b);hubungan_e05f319b=0;
    if(rakan_VALUE>=0)Tutup_rangkaian(rakan_VALUE);rakan_VALUE=-1;perintah_TYPE=0;tamat_status=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *data,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=data[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int aksara_VALUE=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return aksara_VALUE;
}
void 원격출력(unsigned char aksara_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned Tambah_mod=aksara_VALUE==10&&이전출력!=13;
    if(출력수+1+Tambah_mod>sizeof(출력줄)){닫을예정=2;return;}
    if(Tambah_mod)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=aksara_VALUE;이전출력=aksara_VALUE;
}
uintptr_t Papan_tamat_jauh_perintah(uintptr_t status_VALUE){if(셸시작됨&&perintah_TYPE)tamat_status=(int)status_VALUE;return 0;}
uintptr_t Papan_jauh_tunggu(uintptr_t status_VALUE){cangkerang_Menunggu=status_VALUE!=0;return 0;}
static int Sediakan_cangkerang(void) {
    if(Mendengar_peserta>=0)return 0;
    if(!konteks_VALUE){
        assh_status_t RALAT=assh_context_create(&konteks_VALUE,ASSH_SERVER,Sediakan_Memori,0,&rawak_penjana,0);
        if(RALAT)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *kaedah_mod[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        RALAT=assh_algo_register(konteks_VALUE,ASSH_SAFETY_WEAK,kaedah_mod);
        if(!RALAT)RALAT=assh_service_register_va(konteks_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=peranti_Kunci;
        if(!RALAT)RALAT=assh_key_load(konteks_VALUE,assh_context_keys(konteks_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(peranti_Kunci));
        if(RALAT){진단("SSH init error ",RALAT);assh_context_release(konteks_VALUE);konteks_VALUE=0;return -5;}
    }
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int ukuran=망주소묶기(port_VALUE,0,22);if(!ukuran)ukuran=연결기다리기(port_VALUE);
    if(ukuran<0){Tutup_rangkaian(port_VALUE);return ukuran;}Mendengar_peserta=port_VALUE;return 0;
}
uintptr_t Papan_pembayangan(uintptr_t 종류,uintptr_t Aksi) {
    if(종류==1)return(uint32_t)kawalan_jauh_papar(Aksi);
    if(Aksi==0){Tutup_hubungan();if(Mendengar_peserta>=0)Tutup_rangkaian(Mendengar_peserta);Mendengar_peserta=-1;return 0;}
    if(Aksi==1){butstrap_ralat=Sediakan_cangkerang();return(uint32_t)butstrap_ralat;}
    return(uint32_t)(Mendengar_peserta>=0?1:butstrap_ralat);
}
void Sediakan_jauh(void){butstrap_ralat=Sediakan_cangkerang();kawalan_jauh_papar(1);}
static int 같은말(const struct assh_cbuffer_s *data,const char *Word_SMS) {
    size_t kepanjangan_VALUE=strlen(Word_SMS);return data->size==kepanjangan_VALUE&&!memcmp(data->data,Word_SMS,kepanjangan_VALUE);
}
static int Terminal_permintaan(const struct assh_cbuffer_s *data) {
    if(data->size<24)return 0;
    const unsigned char *data_jawatan=data->data;unsigned kepanjangan_VALUE=assh_load_u32(data_jawatan);
    if(kepanjangan_VALUE>128||data->size<kepanjangan_VALUE+24)return 0;
    unsigned mod_VALUE=assh_load_u32(data_jawatan+4+kepanjangan_VALUE+16);
    return mod_VALUE<=2048&&data->size==kepanjangan_VALUE+24+mod_VALUE;
}
static void pemegang_permintaan(struct assh_event_request_s *Peristiwa) {
    if(!인증됨||Peristiwa->ch!=Saluran_pemasukan||!Saluran_pemasukan)return;
    if(같은말(&Peristiwa->type,"pty-req")) {
        if(!셸시작됨&&Terminal_permintaan(&Peristiwa->rq_data))Peristiwa->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Peristiwa->type,"window-change")) {
        if(셸시작됨&&Peristiwa->rq_data.size==16)Peristiwa->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!cangkerang_Menunggu)return;
    const unsigned char *Perintah=0;unsigned kepanjangan_VALUE=0;
    if(같은말(&Peristiwa->type,"exec")) {
        if(Peristiwa->rq_data.size<4)return;
        kepanjangan_VALUE=assh_load_u32(Peristiwa->rq_data.data);
        if(!kepanjangan_VALUE||kepanjangan_VALUE>2048||Peristiwa->rq_data.size!=kepanjangan_VALUE+4)return;
        Perintah=Peristiwa->rq_data.data+4;
        for(unsigned 순번=0;순번<kepanjangan_VALUE;순번++)if(!Perintah[순번])return;
        perintah_TYPE=1;
    }else if(!같은말(&Peristiwa->type,"shell")||Peristiwa->rq_data.size)return;
    if(sizeof(입력줄)-입력수<kepanjangan_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(kepanjangan_VALUE)원격입력넣기(Perintah,kepanjangan_VALUE);원격입력넣기(&끝,1);
    셸시작됨=1;Peristiwa->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!perintah_TYPE){const char *README_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*README_eb81d7d9)원격출력(*README_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Mendengar_peserta<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(rakan_VALUE<0){if(NOW_VALUE<재접속시각)return;rakan_VALUE=망연결받기(Mendengar_peserta);if(rakan_VALUE<0)return;
        hubungan_TIME=NOW_VALUE;assh_status_t RALAT=assh_session_create(konteks_VALUE,&hubungan_e05f319b);
        if(RALAT){hubungan_e05f319b=0;진단("SSH session error ",RALAT);Tutup_hubungan();return;}}
    if((!인증됨&&NOW_VALUE-hubungan_TIME>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){Tutup_hubungan();return;}
    if(Saluran_pemasukan&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t RALAT=assh_channel_data(Saluran_pemasukan,출력줄+출력앞,&수);
            if(!RALAT){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(RALAT!=ASSH_NO_DATA){Tutup_hubungan();return;}
        }
        if(tamat_status>=0&&!출력수){unsigned char status_VALUE[4];assh_store_u32(status_VALUE,(uint32_t)tamat_status);
            if(assh_request(hubungan_e05f319b,Saluran_pemasukan,"exit-status",11,status_VALUE,4,0)||assh_channel_eof(Saluran_pemasukan)||assh_channel_close(Saluran_pemasukan)) {Tutup_hubungan();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned jujukan_VALUE=0;jujukan_VALUE<16;jujukan_VALUE++) {
        struct assh_event_s Peristiwa;
        if(!assh_event_get(hubungan_e05f319b,&Peristiwa,NOW_VALUE/1000)){Tutup_hubungan();return;}
        assh_status_t RALAT=ASSH_OK;int 쉬기=0,putuskan_sambungan_peserta=0;
        switch(Peristiwa.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(rakan_VALUE,Peristiwa.transport.read.buf.data,Peristiwa.transport.read.buf.size);
            if(수>0)Peristiwa.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else putuskan_sambungan_peserta=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(rakan_VALUE,Peristiwa.transport.write.buf.data,Peristiwa.transport.write.buf.size);
            if(수>0)Peristiwa.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else putuskan_sambungan_peserta=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Peristiwa.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Peristiwa.userauth_server.methods.retries>3)Peristiwa.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *data=&Peristiwa.userauth_server.password;
            if(같은말(&data->username,"user")&&data->password.size<=256&&!data->new_password.size) {
                unsigned char ringkasan_VALUE[32];jauh_ringkasan(data->password.data,data->password.size,ringkasan_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=ringkasan_VALUE[순번]^cangkerang_kata_laluan_ringkasan[순번];memset(ringkasan_VALUE,0,32);
                if(!차이)data->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *data=&Peristiwa.connection.channel_open;
            if(인증됨&&!Saluran_pemasukan&&cangkerang_Menunggu&&같은말(&data->type,"session")&&!data->rq_data.size) {
                data->reply=ASSH_CONNECTION_REPLY_SUCCESS;data->pkt_size=4096;
                data->win_size=-1;Saluran_pemasukan=data->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: pemegang_permintaan(&Peristiwa.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *data=&Peristiwa.connection.channel_data;
            if(!셸시작됨||data->ch!=Saluran_pemasukan||data->ext){putuskan_sambungan_peserta=1;break;}
            unsigned 수=data->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(data->data.data[순번]==4){tamat_status=0;수=순번;data->transferred=data->data.size;break;}
            원격입력넣기(data->data.data,수);if(!data->transferred)data->transferred=수;
            if(!수&&tamat_status<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Saluran_pemasukan=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Peristiwa.session.error.code);putuskan_sambungan_peserta=1;break;
        case ASSH_EVENT_DISCONNECT: putuskan_sambungan_peserta=1;break;
        default: break;
        }
        assh_event_done(hubungan_e05f319b,&Peristiwa,RALAT);
        if(putuskan_sambungan_peserta){Tutup_hubungan();return;}if(쉬기)return;
    }
}
