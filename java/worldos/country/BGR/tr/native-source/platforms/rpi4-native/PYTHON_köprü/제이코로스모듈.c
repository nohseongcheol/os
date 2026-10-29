// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "ağ_ABI.h"
static intptr_t 결과검사(intptr_t sonuç) { if (sonuç < 0) mp_raise_OSError(-sonuç); return sonuç; }
static const char *yol_bağımsız_değişken(mp_obj_t değer) {
    size_t öğe_BAĞ_DEĞ_SAY; const char *yol = mp_obj_str_get_data(değer, &öğe_BAĞ_DEĞ_SAY);
    if (!öğe_BAĞ_DEĞ_SAY || öğe_BAĞ_DEĞ_SAY > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < öğe_BAĞ_DEĞ_SAY; 순번++) if (!yol[순번]) mp_raise_OSError(MP_EINVAL);
    return yol;
}
static mp_obj_t 파일읽기(mp_obj_t İsim) {
    intptr_t dosya_tanıtıcısı = 결과검사(사용자호출(3, (uintptr_t)yol_bağımsız_değişken(İsim), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Boyut = 결과검사(사용자호출(9, dosya_tanıtıcısı, 0, 0, 0, 0, 0));
        vstr_t veri; vstr_init_len(&veri, Boyut);
        intptr_t sonuç = 사용자호출(2, dosya_tanıtıcısı, (uintptr_t)veri.buf, Boyut, 0, 0, 0);
        결과검사(sonuç); veri.len = sonuç;
        mp_obj_t değer = mp_obj_new_bytes_from_vstr(&veri);
        nlr_pop(); 사용자호출(4, dosya_tanıtıcısı, 0, 0, 0, 0, 0); return değer;
    }
    사용자호출(4, dosya_tanıtıcısı, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Dosya_Okuyucu_nesne, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Boyut=mp_obj_get_int(한도);
    if(Boyut<0||Boyut>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t veri; vstr_init_len(&veri,Boyut);
    intptr_t öğe_BAĞ_DEĞ_SAY=사용자호출(2,0,(uintptr_t)veri.buf,Boyut,0,0,0);
    if(öğe_BAĞ_DEĞ_SAY<0) { vstr_clear(&veri); 결과검사(öğe_BAĞ_DEĞ_SAY); }
    veri.len=öğe_BAĞ_DEĞ_SAY; return mp_obj_new_bytes_from_vstr(&veri);
}
static MP_DEFINE_CONST_FUN_OBJ_1(STDIN_Okuyucu_nesne, 표준입력읽기);
static mp_obj_t yazma_Dosya(mp_obj_t İsim, mp_obj_t içerik_değer) {
    const char *yol = yol_bağımsız_değişken(İsim);
    mp_buffer_info_t veri; mp_get_buffer_raise(içerik_değer, &veri, MP_BUFFER_READ);
    if (veri.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t dosya_tanıtıcısı = 결과검사(사용자호출(3, (uintptr_t)yol, 577, 0, 0, 0, 0));
    intptr_t girdi_BAĞ_DEĞ_SAY = 사용자호출(1, dosya_tanıtıcısı, (uintptr_t)veri.buf, veri.len, 0, 0, 0);
    사용자호출(4, dosya_tanıtıcısı, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(girdi_BAĞ_DEĞ_SAY));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Dosya_Yazar_nesne, yazma_Dosya);
static mp_obj_t kaldırmak_Dosya(mp_obj_t İsim) { 결과검사(사용자호출(11, (uintptr_t)yol_bağımsız_değişken(İsim), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, kaldırmak_Dosya);
static mp_obj_t Paint_dikdörtgen(size_t öğe_BAĞ_DEĞ_SAY, const mp_obj_t *bağımsız_değişken_DİZİ) {
    (void)öğe_BAĞ_DEĞ_SAY; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(bağımsız_değişken_DİZİ[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(dikdörtgen_nesne, 5, 5, Paint_dikdörtgen);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Boyut[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Boyut);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Saat_değer(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Saat_nesne, Saat_değer);
static mp_obj_t UDP_açık(mp_obj_t bağlantı_noktası_numarası) {
    int veri_konum = mp_obj_get_int(bağlantı_noktası_numarası); if (veri_konum < 0 || veri_konum > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t dosya_tanıtıcısı = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(veri_konum); 첫째값.sin_addr.s_addr = 0;
    intptr_t sonuç = 사용자호출(33, dosya_tanıtıcısı, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (sonuç < 0) { 사용자호출(4, dosya_tanıtıcısı, 0, 0, 0, 0, 0); 결과검사(sonuç); }
    return mp_obj_new_int(dosya_tanıtıcısı);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_açık_OBJ, UDP_açık);
static mp_obj_t UDP_göndermek(mp_obj_t dosya_tanıtıcısı, mp_obj_t bağlantı_noktası_numarası, mp_obj_t içerik_değer) {
    int veri_konum = mp_obj_get_int(bağlantı_noktası_numarası); if (veri_konum < 1 || veri_konum > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t veri; mp_get_buffer_raise(içerik_değer, &veri, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(veri_konum); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(dosya_tanıtıcısı), (uintptr_t)veri.buf, veri.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_göndermek_OBJ, UDP_göndermek);
static uint32_t 인터넷주소읽기(mp_obj_t değer) {
    size_t süre_değer; const char *metin=mp_obj_str_get_data(değer,&süre_değer);
    unsigned geçerli_konum=0; uint32_t ADRES=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned değer=0,rakam_BAĞ_DEĞ_SAY=0;
        while(geçerli_konum<süre_değer&&metin[geçerli_konum]>='0'&&metin[geçerli_konum]<='9') {
            değer=değer*10+metin[geçerli_konum++]-'0'; if(++rakam_BAĞ_DEĞ_SAY>3||değer>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!rakam_BAĞ_DEĞ_SAY)mp_raise_OSError(MP_EINVAL);
        ADRES=ADRES<<8|değer;
        if(부분<3&&(geçerli_konum>=süre_değer||metin[geçerli_konum++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(geçerli_konum!=süre_değer)mp_raise_OSError(MP_EINVAL);
    return ADRES;
}
static mp_obj_t 전문주소전송(size_t girdi_BAĞ_DEĞ_SAY, const mp_obj_t *bağımsız_değişken_DİZİ) {
    (void)girdi_BAĞ_DEĞ_SAY; uint32_t ADRES=인터넷주소읽기(bağımsız_değişken_DİZİ[1]);
    int bağlantı_noktası_numarası=mp_obj_get_int(bağımsız_değişken_DİZİ[2]);if(bağlantı_noktası_numarası<1||bağlantı_noktası_numarası>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t veri;mp_get_buffer_raise(bağımsız_değişken_DİZİ[3],&veri,MP_BUFFER_READ);
    struct pk_sockaddr_in hedef={0};hedef.sin_family=AF_INET;hedef.sin_port=pk_htons(bağlantı_noktası_numarası);hedef.sin_addr.s_addr=pk_htonl(ADRES);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(bağımsız_değişken_DİZİ[0]),(uintptr_t)veri.buf,veri.len,0,(uintptr_t)&hedef,sizeof(hedef))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t dosya_tanıtıcısı) {
    unsigned char veri[512]; struct pk_sockaddr_in eş_değer; pk_socklen_t süre_veri = sizeof(eş_değer);
    intptr_t Boyut = 결과검사(사용자호출(35, mp_obj_get_int(dosya_tanıtıcısı), (uintptr_t)veri, 512, 0, (uintptr_t)&eş_değer, (uintptr_t)&süre_veri));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(veri, Boyut), MP_OBJ_NEW_SMALL_INT(pk_htons(eş_değer.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Kapat(mp_obj_t dosya_tanıtıcısı) { 결과검사(사용자호출(4, mp_obj_get_int(dosya_tanıtıcısı), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Kapat_OBJ, UDP_Kapat);
static mp_obj_t açık_akış(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,bulut_Aile,akış_ağ,akış_aktarım_protokolü,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,açık_akış);
static mp_obj_t bağla_akış(mp_obj_t uç_nokta,mp_obj_t ADRES_SMS,mp_obj_t Dizin) {
    int bağlantı_noktası_numarası=mp_obj_get_int(Dizin); if(bağlantı_noktası_numarası<1||bağlantı_noktası_numarası>65535)mp_raise_OSError(MP_EINVAL);
    struct bulut_yuva_ADRES ADRES={0}; ADRES.ADRES_Aile=bulut_Aile;
    ADRES.bağlantı_noktası_numarası=망차례짧은수(bağlantı_noktası_numarası); ADRES.İnternet_adresi.ADRES_değer=ağ_bilgi(인터넷주소읽기(ADRES_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(uç_nokta),(uintptr_t)&ADRES,sizeof(ADRES),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(akış_Bağlayıcı_nesne,bağla_akış);
static mp_obj_t 흐름읽기(mp_obj_t uç_nokta,mp_obj_t 한도) {
    int süre_değer=mp_obj_get_int(한도); if(süre_değer<1||süre_değer>512)mp_raise_OSError(MP_EINVAL);
    unsigned char veri[512];
    intptr_t öğe_BAĞ_DEĞ_SAY=결과검사(사용자호출(2,mp_obj_get_int(uç_nokta),(uintptr_t)veri,süre_değer,0,0,0));
    return mp_obj_new_bytes(veri,öğe_BAĞ_DEĞ_SAY);
}
static MP_DEFINE_CONST_FUN_OBJ_2(akış_Okuyucu_nesne,흐름읽기);
static mp_obj_t yazma_akış(mp_obj_t uç_nokta,mp_obj_t içerik_değer) {
    mp_buffer_info_t veri; mp_get_buffer_raise(içerik_değer,&veri,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(uç_nokta),(uintptr_t)veri.buf,veri.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(akış_Yazar_nesne,yazma_akış);
static mp_obj_t 잠시기다리기(mp_obj_t zaman_değeri) {
    결과검사(사용자호출(17,mp_obj_get_int(zaman_değeri),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(bekle_nesne,잠시기다리기);
static mp_obj_t girdi_Tip(mp_obj_t İsim) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)yol_bağımsız_değişken(İsim),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(girdi_Tip_nesne,girdi_Tip);
static mp_obj_t açmak_dizin(mp_obj_t İsim) {
    결과검사(사용자호출(18,(uintptr_t)yol_bağımsız_değişken(İsim),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(dizin_yazar_nesne,açmak_dizin);
static mp_obj_t kaldırmak_dizin(mp_obj_t İsim) {
    결과검사(사용자호출(18,(uintptr_t)yol_bağımsız_değişken(İsim),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,kaldırmak_dizin);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&akış_Bağlayıcı_nesne) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&akış_Okuyucu_nesne) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&akış_Yazar_nesne) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&bekle_nesne) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&girdi_Tip_nesne) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&dizin_yazar_nesne) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&STDIN_Okuyucu_nesne) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Dosya_Okuyucu_nesne) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Dosya_Yazar_nesne) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&dikdörtgen_nesne) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Saat_nesne) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_açık_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_göndermek_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Kapat_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
