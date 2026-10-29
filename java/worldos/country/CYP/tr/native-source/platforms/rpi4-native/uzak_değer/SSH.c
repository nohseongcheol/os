/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "uzak_değer.h"
#include "şifreleme_Destek.h"
#include "Profil.h"
#include "../ağ_Yığın/ağ_Yığın.h"
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
static struct assh_context_s *Bağlam_değer;
static struct assh_session_s *cxn_e05f319b;
static struct assh_channel_s *Kanal_girdi;
static int Dinleniyor_uç_nokta=-1,eş_değer=-1,인증됨,셸시작됨,komut_TÜR,Bitiş_Durum=-1,닫을예정,IPL_hata,kabuk_Bekliyor;
static uintptr_t cxn_saat,재접속시각,닫는시각;
static unsigned char artış_hat[8192],çıktı_hat[65536];
static unsigned 입력앞,artış_BAĞ_DEĞ_SAY,출력앞,çıktı_BAĞ_DEĞ_SAY,Önceki_çıktı;
static void 진단(const char *Word_SMS,unsigned değer) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char rakam_değer[12];unsigned 수=0;do{rakam_değer[수++]='0'+değer%10;değer/=10;}while(değer);
    while(수)보드글자쓰기(rakam_değer[--수]);보드글자쓰기(10);
}
static assh_status_t Hazırlan_Bellek(void *veri,void **ADRES,size_t Boyut,enum assh_alloc_type_e Tip_değer) {
    (void)veri;(void)Tip_değer;
    if(!Boyut){sürüm_uzak(*ADRES);*ADRES=0;return ASSH_OK;}
    void *새주소=원격재할당(*ADRES,Boyut);
    if(!새주소)return ASSH_ERR_MEM;*ADRES=새주소;return ASSH_OK;
}
static assh_status_t Hazırlan_rastgele(struct assh_context_s *veri,const struct assh_buffer_s *başlangıç_değeri) {
    (void)veri;(void)başlangıç_değeri;unsigned char sınamalar[32];int sonuç=uzak_rastgele(sınamalar,sizeof(sınamalar));memset(sınamalar,0,sizeof(sınamalar));
    return sonuç?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *veri,uint8_t *sonuç,size_t süre_değer,uint_fast8_t Tip_değer) {
    (void)veri;(void)Tip_değer;if(süre_değer>65536)return ASSH_ERR_CRYPTO;
    return uzak_rastgele(sonuç,süre_değer)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void rastgele_Bitiş(struct assh_context_s *veri){(void)veri;}
static const struct assh_prng_s rastgele_oluşturucu={Hazırlan_rastgele,난수받기,rastgele_Bitiş};
static void Kapat_cxn(void) {
    인증됨=셸시작됨=0;Kanal_girdi=0;
    if(cxn_e05f319b)assh_session_release(cxn_e05f319b);cxn_e05f319b=0;
    if(eş_değer>=0)Kapat_ağ(eş_değer);eş_değer=-1;komut_TÜR=0;Bitiş_Durum=-1;닫을예정=0;
    입력앞=artış_BAĞ_DEĞ_SAY=출력앞=çıktı_BAĞ_DEĞ_SAY=Önceki_çıktı=0;재접속시각=보드밀리초()+250;
}
int akış_uzak_artış(const unsigned char *veri,unsigned 수) {
    if(수>sizeof(artış_hat)-artış_BAĞ_DEĞ_SAY)return -11;
    for(unsigned 순번=0;순번<수;순번++)artış_hat[(입력앞+artış_BAĞ_DEĞ_SAY++)%sizeof(artış_hat)]=veri[순번];return 수;
}
int uzak_artış(void) {
    if(!artış_BAĞ_DEĞ_SAY)return -1;int karakter_değer=artış_hat[입력앞];입력앞=(입력앞+1)%sizeof(artış_hat);artış_BAĞ_DEĞ_SAY--;return karakter_değer;
}
void uzak_çıktı(unsigned char karakter_değer) {
    if(!셸시작됨||닫을예정)return;
    unsigned Ekleme_modu=karakter_değer==10&&Önceki_çıktı!=13;
    if(çıktı_BAĞ_DEĞ_SAY+1+Ekleme_modu>sizeof(çıktı_hat)){닫을예정=2;return;}
    if(Ekleme_modu)çıktı_hat[(출력앞+çıktı_BAĞ_DEĞ_SAY++)%sizeof(çıktı_hat)]=13;
    çıktı_hat[(출력앞+çıktı_BAĞ_DEĞ_SAY++)%sizeof(çıktı_hat)]=karakter_değer;Önceki_çıktı=karakter_değer;
}
uintptr_t Pano_Bitiş_uzak_komut(uintptr_t Durum_değer){if(셸시작됨&&komut_TÜR)Bitiş_Durum=(int)Durum_değer;return 0;}
uintptr_t Pano_uzak_bekle(uintptr_t Durum_değer){kabuk_Bekliyor=Durum_değer!=0;return 0;}
static int Hazırlan_kabuk(void) {
    if(Dinleniyor_uç_nokta>=0)return 0;
    if(!Bağlam_değer){
        assh_status_t hata=assh_context_create(&Bağlam_değer,ASSH_SERVER,Hazırlan_Bellek,0,&rastgele_oluşturucu,0);
        if(hata)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metot_mod[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        hata=assh_algo_register(Bağlam_değer,ASSH_SAFETY_WEAK,metot_mod);
        if(!hata)hata=assh_service_register_va(Bağlam_değer,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *tuş_malzeme=cihaz_tuş;
        if(!hata)hata=assh_key_load(Bağlam_değer,assh_context_keys(Bağlam_değer),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&tuş_malzeme,sizeof(cihaz_tuş));
        if(hata){진단("SSH init error ",hata);assh_context_release(Bağlam_değer);Bağlam_değer=0;return -5;}
    }
    int taşımak_değer=açmak_yuva_uç_nokta(1);if(taşımak_değer<0)return taşımak_değer;통신주소재사용(taşımak_değer);
    int sonuç=NET_BIND(taşımak_değer,0,22);if(!sonuç)sonuç=NET_dinlemek(taşımak_değer);
    if(sonuç<0){Kapat_ağ(taşımak_değer);return sonuç;}Dinleniyor_uç_nokta=taşımak_değer;return 0;
}
uintptr_t Pano_gölge_kullanım(uintptr_t Tip_değer,uintptr_t Eylem) {
    if(Tip_değer==1)return(uint32_t)denetim_uzak_monitör(Eylem);
    if(Eylem==0){Kapat_cxn();if(Dinleniyor_uç_nokta>=0)Kapat_ağ(Dinleniyor_uç_nokta);Dinleniyor_uç_nokta=-1;return 0;}
    if(Eylem==1){IPL_hata=Hazırlan_kabuk();return(uint32_t)IPL_hata;}
    return(uint32_t)(Dinleniyor_uç_nokta>=0?1:IPL_hata);
}
void Hazırlan_uzak(void){IPL_hata=Hazırlan_kabuk();denetim_uzak_monitör(1);}
static int 같은말(const struct assh_cbuffer_s *veri,const char *Word_SMS) {
    size_t süre_değer=strlen(Word_SMS);return veri->size==süre_değer&&!memcmp(veri->data,Word_SMS,süre_değer);
}
static int Terminal_istek(const struct assh_cbuffer_s *veri) {
    if(veri->size<24)return 0;
    const unsigned char *veri_konum=veri->data;unsigned süre_değer=assh_load_u32(veri_konum);
    if(süre_değer>128||veri->size<süre_değer+24)return 0;
    unsigned mod_değer=assh_load_u32(veri_konum+4+süre_değer+16);
    return mod_değer<=2048&&veri->size==süre_değer+24+mod_değer;
}
static void sap_istek(struct assh_event_request_s *Olay) {
    if(!인증됨||Olay->ch!=Kanal_girdi||!Kanal_girdi)return;
    if(같은말(&Olay->type,"pty-req")) {
        if(!셸시작됨&&Terminal_istek(&Olay->rq_data))Olay->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Olay->type,"window-change")) {
        if(셸시작됨&&Olay->rq_data.size==16)Olay->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!kabuk_Bekliyor)return;
    const unsigned char *komut=0;unsigned süre_değer=0;
    if(같은말(&Olay->type,"exec")) {
        if(Olay->rq_data.size<4)return;
        süre_değer=assh_load_u32(Olay->rq_data.data);
        if(!süre_değer||süre_değer>2048||Olay->rq_data.size!=süre_değer+4)return;
        komut=Olay->rq_data.data+4;
        for(unsigned 순번=0;순번<süre_değer;순번++)if(!komut[순번])return;
        komut_TÜR=1;
    }else if(!같은말(&Olay->type,"shell")||Olay->rq_data.size)return;
    if(sizeof(artış_hat)-artış_BAĞ_DEĞ_SAY<süre_değer+2)return;
    const unsigned char 지움=21,끝=13;
    akış_uzak_artış(&지움,1);if(süre_değer)akış_uzak_artış(komut,süre_değer);akış_uzak_artış(&끝,1);
    셸시작됨=1;Olay->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!komut_TÜR){const char *안내="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*안내)uzak_çıktı(*안내++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Dinleniyor_uç_nokta<0)return;
    uintptr_t ŞİMDİ_değer=보드밀리초();
    if(eş_değer<0){if(ŞİMDİ_değer<재접속시각)return;eş_değer=NET_kabul_etmek(Dinleniyor_uç_nokta);if(eş_değer<0)return;
        cxn_saat=ŞİMDİ_değer;assh_status_t hata=assh_session_create(Bağlam_değer,&cxn_e05f319b);
        if(hata){cxn_e05f319b=0;진단("SSH session error ",hata);Kapat_cxn();return;}}
    if((!인증됨&&ŞİMDİ_değer-cxn_saat>30000)||닫을예정==2||(닫을예정&&ŞİMDİ_değer>=닫는시각)){Kapat_cxn();return;}
    if(Kanal_girdi&&셸시작됨&&!닫을예정) {
        if(çıktı_BAĞ_DEĞ_SAY){size_t 수=sizeof(çıktı_hat)-출력앞;if(수>çıktı_BAĞ_DEĞ_SAY)수=çıktı_BAĞ_DEĞ_SAY;if(수>2048)수=2048;
            assh_status_t hata=assh_channel_data(Kanal_girdi,çıktı_hat+출력앞,&수);
            if(!hata){출력앞=(출력앞+수)%sizeof(çıktı_hat);çıktı_BAĞ_DEĞ_SAY-=수;}
            else if(hata!=ASSH_NO_DATA){Kapat_cxn();return;}
        }
        if(Bitiş_Durum>=0&&!çıktı_BAĞ_DEĞ_SAY){unsigned char Durum_değer[4];assh_store_u32(Durum_değer,(uint32_t)Bitiş_Durum);
            if(assh_request(cxn_e05f319b,Kanal_girdi,"exit-status",11,Durum_değer,4,0)||assh_channel_eof(Kanal_girdi)||assh_channel_close(Kanal_girdi)) {Kapat_cxn();return;}
            닫을예정=1;닫는시각=ŞİMDİ_değer+3000;
        }
    }
    for(unsigned dizi_değer=0;dizi_değer<16;dizi_değer++) {
        struct assh_event_s Olay;
        if(!assh_event_get(cxn_e05f319b,&Olay,ŞİMDİ_değer/1000)){Kapat_cxn();return;}
        assh_status_t hata=ASSH_OK;int 쉬기=0,bağlantıyı_kesmek_uç_nokta=0;
        switch(Olay.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(eş_değer,Olay.transport.read.buf.data,Olay.transport.read.buf.size);
            if(수>0)Olay.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else bağlantıyı_kesmek_uç_nokta=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=NET_yazma(eş_değer,Olay.transport.write.buf.data,Olay.transport.write.buf.size);
            if(수>0)Olay.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else bağlantıyı_kesmek_uç_nokta=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Olay.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Olay.userauth_server.methods.retries>3)Olay.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *veri=&Olay.userauth_server.password;
            if(같은말(&veri->username,"user")&&veri->password.size<=256&&!veri->new_password.size) {
                unsigned char özet_değer[32];uzak_özet(veri->password.data,veri->password.size,özet_değer);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=özet_değer[순번]^kabuk_parola_özet[순번];memset(özet_değer,0,32);
                if(!차이)veri->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *veri=&Olay.connection.channel_open;
            if(인증됨&&!Kanal_girdi&&kabuk_Bekliyor&&같은말(&veri->type,"session")&&!veri->rq_data.size) {
                veri->reply=ASSH_CONNECTION_REPLY_SUCCESS;veri->pkt_size=4096;
                veri->win_size=-1;Kanal_girdi=veri->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: sap_istek(&Olay.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *veri=&Olay.connection.channel_data;
            if(!셸시작됨||veri->ch!=Kanal_girdi||veri->ext){bağlantıyı_kesmek_uç_nokta=1;break;}
            unsigned 수=veri->data.size;if(수>sizeof(artış_hat)-artış_BAĞ_DEĞ_SAY)수=sizeof(artış_hat)-artış_BAĞ_DEĞ_SAY;
            for(unsigned 순번=0;순번<수;순번++)if(veri->data.data[순번]==4){Bitiş_Durum=0;수=순번;veri->transferred=veri->data.size;break;}
            akış_uzak_artış(veri->data.data,수);if(!veri->transferred)veri->transferred=수;
            if(!수&&Bitiş_Durum<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Kanal_girdi=0;셸시작됨=0;닫을예정=1;닫는시각=ŞİMDİ_değer+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Olay.session.error.code);bağlantıyı_kesmek_uç_nokta=1;break;
        case ASSH_EVENT_DISCONNECT: bağlantıyı_kesmek_uç_nokta=1;break;
        default: break;
        }
        assh_event_done(cxn_e05f319b,&Olay,hata);
        if(bağlantıyı_kesmek_uç_nokta){Kapat_cxn();return;}if(쉬기)return;
    }
}
