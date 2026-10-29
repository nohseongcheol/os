/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "giáTrịTừXa.h"
#include "hỗTrợMậtMãHọc.h"
#include "hồSơ.h"
#include "../NgănXếpMạng/NgănXếpMạng.h"
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
extern uintptr_t miliGiâyGọnBoMạch(void);
extern uintptr_t đặtKýTựBoMạch(uintptr_t);
static struct assh_context_s *giáTrịNgữCảnh;
static struct assh_session_s *kếtNối;
static struct assh_channel_s *mụcKênh;
static int điểmCuốiĐangLắngNghe=-1,giáTrịĐốiTác=-1,làĐãXácThực,đãBắtChạyVỏLệnh,kiểuLệnh,trạngTháiKếtThúc=-1,sẽĐóng,lỗiLúcKhởiChạy,đangĐợiVỏLệnh;
static uintptr_t thờiGianKếtNối,thờiGianKếtNốiLại,thờiGianĐangĐóng;
static unsigned char dòngĐầuVào[8192],dòngĐầuRa[65536];
static unsigned đầuĐầuVào,sốLượngĐầuVào,đầuĐầuRa,sốLượngĐầuRa,đầuRaTrướcĐó;
static void giáTrịChẩnĐoán(const char *vănBảnTừ,unsigned giáTrị) {
    while(*vănBảnTừ)đặtKýTựBoMạch(*vănBảnTừ++);
    char giáTrịChữSố[12];unsigned trịSố=0;do{giáTrịChữSố[trịSố++]='0'+giáTrị%10;giáTrị/=10;}while(giáTrị);
    while(trịSố)đặtKýTựBoMạch(giáTrịChữSố[--trịSố]);đặtKýTựBoMạch(10);
}
static assh_status_t chuẩnBịBộNhớ(void *DữLiệu,void **địaChỉ,size_t cỡ,enum assh_alloc_type_e giáTrịLoại) {
    (void)DữLiệu;(void)giáTrịLoại;
    if(!cỡ){giảiPhóngTừXa(*địaChỉ);*địaChỉ=0;return ASSH_OK;}
    void *địaChỉMới=cấpPhátLạiTừXa(*địaChỉ,cỡ);
    if(!địaChỉMới)return ASSH_ERR_MEM;*địaChỉ=địaChỉMới;return ASSH_OK;
}
static assh_status_t chuẩnBịNgẫuNhiên(struct assh_context_s *DữLiệu,const struct assh_buffer_s *giáTrịHạtGiống) {
    (void)DữLiệu;(void)giáTrịHạtGiống;unsigned char KiểmThử[32];int kếtQuả=ngẫuNhiênTừXa(KiểmThử,sizeof(KiểmThử));memset(KiểmThử,0,sizeof(KiểmThử));
    return kếtQuả?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t đọcNgẫuNhiên(struct assh_context_s *DữLiệu,uint8_t *kếtQuả,size_t độDài,uint_fast8_t giáTrịLoại) {
    (void)DữLiệu;(void)giáTrịLoại;if(độDài>65536)return ASSH_ERR_CRYPTO;
    return ngẫuNhiênTừXa(kếtQuả,độDài)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void kếtThúcNgẫuNhiên(struct assh_context_s *DữLiệu){(void)DữLiệu;}
static const struct assh_prng_s bộSinhNgẫuNhiên={chuẩnBịNgẫuNhiên,đọcNgẫuNhiên,kếtThúcNgẫuNhiên};
static void đóngKếtNối(void) {
    làĐãXácThực=đãBắtChạyVỏLệnh=0;mụcKênh=0;
    if(kếtNối)assh_session_release(kếtNối);kếtNối=0;
    if(giáTrịĐốiTác>=0)đóngMạng(giáTrịĐốiTác);giáTrịĐốiTác=-1;kiểuLệnh=0;trạngTháiKếtThúc=-1;sẽĐóng=0;
    đầuĐầuVào=sốLượngĐầuVào=đầuĐầuRa=sốLượngĐầuRa=đầuRaTrướcĐó=0;thờiGianKếtNốiLại=miliGiâyGọnBoMạch()+250;
}
int đầuVàoTừXaCấp(const unsigned char *DữLiệu,unsigned trịSố) {
    if(trịSố>sizeof(dòngĐầuVào)-sốLượngĐầuVào)return -11;
    for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<trịSố;chỉSốThứBậc++)dòngĐầuVào[(đầuĐầuVào+sốLượngĐầuVào++)%sizeof(dòngĐầuVào)]=DữLiệu[chỉSốThứBậc];return trịSố;
}
int đầuVàoTừXa(void) {
    if(!sốLượngĐầuVào)return -1;int giáTrịKýTự=dòngĐầuVào[đầuĐầuVào];đầuĐầuVào=(đầuĐầuVào+1)%sizeof(dòngĐầuVào);sốLượngĐầuVào--;return giáTrịKýTự;
}
void đầuRaTừXa(unsigned char giáTrịKýTự) {
    if(!đãBắtChạyVỏLệnh||sẽĐóng)return;
    unsigned thêmCuốiChếĐộ=giáTrịKýTự==10&&đầuRaTrướcĐó!=13;
    if(sốLượngĐầuRa+1+thêmCuốiChếĐộ>sizeof(dòngĐầuRa)){sẽĐóng=2;return;}
    if(thêmCuốiChếĐộ)dòngĐầuRa[(đầuĐầuRa+sốLượngĐầuRa++)%sizeof(dòngĐầuRa)]=13;
    dòngĐầuRa[(đầuĐầuRa+sốLượngĐầuRa++)%sizeof(dòngĐầuRa)]=giáTrịKýTự;đầuRaTrướcĐó=giáTrịKýTự;
}
uintptr_t lệnhTừXaKếtThúcBoMạch(uintptr_t giáTrịTrạngThái){if(đãBắtChạyVỏLệnh&&kiểuLệnh)trạngTháiKếtThúc=(int)giáTrịTrạngThái;return 0;}
uintptr_t chờTừXaBoMạch(uintptr_t giáTrịTrạngThái){đangĐợiVỏLệnh=giáTrịTrạngThái!=0;return 0;}
static int chuẩnBịVỏLệnh(void) {
    if(điểmCuốiĐangLắngNghe>=0)return 0;
    if(!giáTrịNgữCảnh){
        assh_status_t lỗi=assh_context_create(&giáTrịNgữCảnh,ASSH_SERVER,chuẩnBịBộNhớ,0,&bộSinhNgẫuNhiên,0);
        if(lỗi)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *chếĐộPhươngThức[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        lỗi=assh_algo_register(giáTrịNgữCảnh,ASSH_SAFETY_WEAK,chếĐộPhươngThức);
        if(!lỗi)lỗi=assh_service_register_va(giáTrịNgữCảnh,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *vậtLiệuPhím=phímThiếtBị;
        if(!lỗi)lỗi=assh_key_load(giáTrịNgữCảnh,assh_context_keys(giáTrịNgữCảnh),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&vậtLiệuPhím,sizeof(phímThiếtBị));
        if(lỗi){giáTrịChẩnĐoán("SSH init error ",lỗi);assh_context_release(giáTrịNgữCảnh);giáTrịNgữCảnh=0;return -5;}
    }
    int giáTrịCổng=tạoĐiểmCuốiỔCắmMạng(1);if(giáTrịCổng<0)return giáTrịCổng;địaChỉỔCắmMạngDùngLại(giáTrịCổng);
    int kếtQuả=ràngBuộcMạngGọn(giáTrịCổng,0,22);if(!kếtQuả)kếtQuả=lắngNgheMạngGọn(giáTrịCổng);
    if(kếtQuả<0){đóngMạng(giáTrịCổng);return kếtQuả;}điểmCuốiĐangLắngNghe=giáTrịCổng;return 0;
}
uintptr_t điềuKhiểnTừXaBoMạch(uintptr_t giáTrịLoại,uintptr_t hànhĐộng) {
    if(giáTrịLoại==1)return(uint32_t)hiểnThịTừXaĐiềuKhiển(hànhĐộng);
    if(hànhĐộng==0){đóngKếtNối();if(điểmCuốiĐangLắngNghe>=0)đóngMạng(điểmCuốiĐangLắngNghe);điểmCuốiĐangLắngNghe=-1;return 0;}
    if(hànhĐộng==1){lỗiLúcKhởiChạy=chuẩnBịVỏLệnh();return(uint32_t)lỗiLúcKhởiChạy;}
    return(uint32_t)(điểmCuốiĐangLắngNghe>=0?1:lỗiLúcKhởiChạy);
}
void chuẩnBịTừXa(void){lỗiLúcKhởiChạy=chuẩnBịVỏLệnh();hiểnThịTừXaĐiềuKhiển(1);}
static int từViệcSoKhớp(const struct assh_cbuffer_s *DữLiệu,const char *vănBảnTừ) {
    size_t độDài=strlen(vănBảnTừ);return DữLiệu->size==độDài&&!memcmp(DữLiệu->data,vănBảnTừ,độDài);
}
static int yêuCầuThiếtBịCuối(const struct assh_cbuffer_s *DữLiệu) {
    if(DữLiệu->size<24)return 0;
    const unsigned char *vịTríDữLiệu=DữLiệu->data;unsigned độDài=assh_load_u32(vịTríDữLiệu);
    if(độDài>128||DữLiệu->size<độDài+24)return 0;
    unsigned giáTrịChếĐộ=assh_load_u32(vịTríDữLiệu+4+độDài+16);
    return giáTrịChếĐộ<=2048&&DữLiệu->size==độDài+24+giáTrịChếĐộ;
}
static void yêuCầuThẻXửLý(struct assh_event_request_s *sựKiện) {
    if(!làĐãXácThực||sựKiện->ch!=mụcKênh||!mụcKênh)return;
    if(từViệcSoKhớp(&sựKiện->type,"pty-req")) {
        if(!đãBắtChạyVỏLệnh&&yêuCầuThiếtBịCuối(&sựKiện->rq_data))sựKiện->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(từViệcSoKhớp(&sựKiện->type,"window-change")) {
        if(đãBắtChạyVỏLệnh&&sựKiện->rq_data.size==16)sựKiện->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(đãBắtChạyVỏLệnh||!đangĐợiVỏLệnh)return;
    const unsigned char *lệnh=0;unsigned độDài=0;
    if(từViệcSoKhớp(&sựKiện->type,"exec")) {
        if(sựKiện->rq_data.size<4)return;
        độDài=assh_load_u32(sựKiện->rq_data.data);
        if(!độDài||độDài>2048||sựKiện->rq_data.size!=độDài+4)return;
        lệnh=sựKiện->rq_data.data+4;
        for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<độDài;chỉSốThứBậc++)if(!lệnh[chỉSốThứBậc])return;
        kiểuLệnh=1;
    }else if(!từViệcSoKhớp(&sựKiện->type,"shell")||sựKiện->rq_data.size)return;
    if(sizeof(dòngĐầuVào)-sốLượngĐầuVào<độDài+2)return;
    const unsigned char giáTrịĐãXóa=21,phầnKết=13;
    đầuVàoTừXaCấp(&giáTrịĐãXóa,1);if(độDài)đầuVàoTừXaCấp(lệnh,độDài);đầuVàoTừXaCấp(&phầnKết,1);
    đãBắtChạyVỏLệnh=1;sựKiện->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!kiểuLệnh){const char *HướngDẫn="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*HướngDẫn)đầuRaTừXa(*HướngDẫn++);}
}
void xemXétTừXa(void) {
    xemXétHiểnThịTừXa();
    if(điểmCuốiĐangLắngNghe<0)return;
    uintptr_t giáTrịBâyGiờ=miliGiâyGọnBoMạch();
    if(giáTrịĐốiTác<0){if(giáTrịBâyGiờ<thờiGianKếtNốiLại)return;giáTrịĐốiTác=chấpNhậnMạngGọn(điểmCuốiĐangLắngNghe);if(giáTrịĐốiTác<0)return;
        thờiGianKếtNối=giáTrịBâyGiờ;assh_status_t lỗi=assh_session_create(giáTrịNgữCảnh,&kếtNối);
        if(lỗi){kếtNối=0;giáTrịChẩnĐoán("SSH session error ",lỗi);đóngKếtNối();return;}}
    if((!làĐãXácThực&&giáTrịBâyGiờ-thờiGianKếtNối>30000)||sẽĐóng==2||(sẽĐóng&&giáTrịBâyGiờ>=thờiGianĐangĐóng)){đóngKếtNối();return;}
    if(mụcKênh&&đãBắtChạyVỏLệnh&&!sẽĐóng) {
        if(sốLượngĐầuRa){size_t trịSố=sizeof(dòngĐầuRa)-đầuĐầuRa;if(trịSố>sốLượngĐầuRa)trịSố=sốLượngĐầuRa;if(trịSố>2048)trịSố=2048;
            assh_status_t lỗi=assh_channel_data(mụcKênh,dòngĐầuRa+đầuĐầuRa,&trịSố);
            if(!lỗi){đầuĐầuRa=(đầuĐầuRa+trịSố)%sizeof(dòngĐầuRa);sốLượngĐầuRa-=trịSố;}
            else if(lỗi!=ASSH_NO_DATA){đóngKếtNối();return;}
        }
        if(trạngTháiKếtThúc>=0&&!sốLượngĐầuRa){unsigned char giáTrịTrạngThái[4];assh_store_u32(giáTrịTrạngThái,(uint32_t)trạngTháiKếtThúc);
            if(assh_request(kếtNối,mụcKênh,"exit-status",11,giáTrịTrạngThái,4,0)||assh_channel_eof(mụcKênh)||assh_channel_close(mụcKênh)) {đóngKếtNối();return;}
            sẽĐóng=1;thờiGianĐangĐóng=giáTrịBâyGiờ+3000;
        }
    }
    for(unsigned giáTrịDãy=0;giáTrịDãy<16;giáTrịDãy++) {
        struct assh_event_s sựKiện;
        if(!assh_event_get(kếtNối,&sựKiện,giáTrịBâyGiờ/1000)){đóngKếtNối();return;}
        assh_status_t lỗi=ASSH_OK;int ngắnPhầnCòn=0,điểmCuốiNgắtKếtNối=0;
        switch(sựKiện.id) {
        case ASSH_EVENT_READ: {
            int trịSố=đọcMạngGọn(giáTrịĐốiTác,sựKiện.transport.read.buf.data,sựKiện.transport.read.buf.size);
            if(trịSố>0)sựKiện.transport.read.transferred=trịSố;
            else if(trịSố==-11)ngắnPhầnCòn=1;else điểmCuốiNgắtKếtNối=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int trịSố=ghiMạngGọn(giáTrịĐốiTác,sựKiện.transport.write.buf.data,sựKiện.transport.write.buf.size);
            if(trịSố>0)sựKiện.transport.write.transferred=trịSố;
            else if(trịSố==-11)ngắnPhầnCòn=1;else điểmCuốiNgắtKếtNối=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            sựKiện.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(sựKiện.userauth_server.methods.retries>3)sựKiện.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *DữLiệu=&sựKiện.userauth_server.password;
            if(từViệcSoKhớp(&DữLiệu->username,"user")&&DữLiệu->password.size<=256&&!DữLiệu->new_password.size) {
                unsigned char giáTrịTómLược[32];tómLượcTừXa(DữLiệu->password.data,DữLiệu->password.size,giáTrịTómLược);
                unsigned giáTrịKhácBiệt=0;for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<32;chỉSốThứBậc++)giáTrịKhácBiệt|=giáTrịTómLược[chỉSốThứBậc]^tómLượcMậtKhẩuVỏLệnh[chỉSốThứBậc];memset(giáTrịTómLược,0,32);
                if(!giáTrịKhácBiệt)DữLiệu->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: làĐãXácThực=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *DữLiệu=&sựKiện.connection.channel_open;
            if(làĐãXácThực&&!mụcKênh&&đangĐợiVỏLệnh&&từViệcSoKhớp(&DữLiệu->type,"session")&&!DữLiệu->rq_data.size) {
                DữLiệu->reply=ASSH_CONNECTION_REPLY_SUCCESS;DữLiệu->pkt_size=4096;
                DữLiệu->win_size=-1;mụcKênh=DữLiệu->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: yêuCầuThẻXửLý(&sựKiện.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *DữLiệu=&sựKiện.connection.channel_data;
            if(!đãBắtChạyVỏLệnh||DữLiệu->ch!=mụcKênh||DữLiệu->ext){điểmCuốiNgắtKếtNối=1;break;}
            unsigned trịSố=DữLiệu->data.size;if(trịSố>sizeof(dòngĐầuVào)-sốLượngĐầuVào)trịSố=sizeof(dòngĐầuVào)-sốLượngĐầuVào;
            for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<trịSố;chỉSốThứBậc++)if(DữLiệu->data.data[chỉSốThứBậc]==4){trạngTháiKếtThúc=0;trịSố=chỉSốThứBậc;DữLiệu->transferred=DữLiệu->data.size;break;}
            đầuVàoTừXaCấp(DữLiệu->data.data,trịSố);if(!DữLiệu->transferred)DữLiệu->transferred=trịSố;
            if(!trịSố&&trạngTháiKếtThúc<0)ngắnPhầnCòn=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: mụcKênh=0;đãBắtChạyVỏLệnh=0;sẽĐóng=1;thờiGianĐangĐóng=giáTrịBâyGiờ+1000;break;
        case ASSH_EVENT_SESSION_ERROR: làĐãXácThực=đãBắtChạyVỏLệnh=0;giáTrịChẩnĐoán("SSH error ",sựKiện.session.error.code);điểmCuốiNgắtKếtNối=1;break;
        case ASSH_EVENT_DISCONNECT: điểmCuốiNgắtKếtNối=1;break;
        default: break;
        }
        assh_event_done(kếtNối,&sựKiện,lỗi);
        if(điểmCuốiNgắtKếtNối){đóngKếtNối();return;}if(ngắnPhầnCòn)return;
    }
}
