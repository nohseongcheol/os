// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *Yoonu_jëmale_Tegtal(mp_obj_t xëyma) {
    size_t 개수; const char *Yoonu_jëmale = mp_obj_str_get_data(xëyma, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!Yoonu_jëmale[순번]) mp_raise_OSError(MP_EINVAL);
    return Yoonu_jëmale;
}
static mp_obj_t 파일읽기(mp_obj_t tur_253d1510) {
    intptr_t bara_denc_yombal = 결과검사(사용자호출(3, (uintptr_t)Yoonu_jëmale_Tegtal(tur_253d1510), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t tolluwaay = 결과검사(사용자호출(9, bara_denc_yombal, 0, 0, 0, 0, 0));
        vstr_t mbir; vstr_init_len(&mbir, tolluwaay);
        intptr_t 결과 = 사용자호출(2, bara_denc_yombal, (uintptr_t)mbir.buf, tolluwaay, 0, 0, 0);
        결과검사(결과); mbir.len = 결과;
        mp_obj_t xëyma = mp_obj_new_bytes_from_vstr(&mbir);
        nlr_pop(); 사용자호출(4, bara_denc_yombal, 0, 0, 0, 0, 0); return xëyma;
    }
    사용자호출(4, bara_denc_yombal, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(bara_denc_jangkat_yëf, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t tolluwaay=mp_obj_get_int(한도);
    if(tolluwaay<0||tolluwaay>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t mbir; vstr_init_len(&mbir,tolluwaay);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)mbir.buf,tolluwaay,0,0,0);
    if(개수<0) { vstr_clear(&mbir); 결과검사(개수); }
    mbir.len=개수; return mp_obj_new_bytes_from_vstr(&mbir);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t biir_bara_denc(mp_obj_t tur_253d1510, mp_obj_t Këmb_xëyma) {
    const char *Yoonu_jëmale = Yoonu_jëmale_Tegtal(tur_253d1510);
    mp_buffer_info_t mbir; mp_get_buffer_raise(Këmb_xëyma, &mbir, MP_BUFFER_READ);
    if (mbir.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t bara_denc_yombal = 결과검사(사용자호출(3, (uintptr_t)Yoonu_jëmale, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, bara_denc_yombal, (uintptr_t)mbir.buf, mbir.len, 0, 0, 0);
    사용자호출(4, bara_denc_yombal, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(bara_denc_Writer_yëf, biir_bara_denc);
static mp_obj_t dandal_bara_denc(mp_obj_t tur_253d1510) { 결과검사(사용자호출(11, (uintptr_t)Yoonu_jëmale_Tegtal(tur_253d1510), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, dandal_bara_denc);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *Tegtal_TABLO) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(Tegtal_TABLO[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t tolluwaay[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, tolluwaay);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Yeetekaay_ak_Montar_xëyma(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Yeetekaay_ak_Montar_yëf, Yeetekaay_ak_Montar_xëyma);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t bara_denc_yombal = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, bara_denc_yombal, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, bara_denc_yombal, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(bara_denc_yombal);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t bara_denc_yombal, mp_obj_t 접속번호, mp_obj_t Këmb_xëyma) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t mbir; mp_get_buffer_raise(Këmb_xëyma, &mbir, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(bara_denc_yombal), (uintptr_t)mbir.buf, mbir.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t xëyma) {
    size_t diir_xëyma; const char *Tekst=mp_obj_str_get_data(xëyma,&diir_xëyma);
    unsigned 현재위치=0; uint32_t dëkkuwaay=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned xëyma=0,숫자수=0;
        while(현재위치<diir_xëyma&&Tekst[현재위치]>='0'&&Tekst[현재위치]<='9') {
            xëyma=xëyma*10+Tekst[현재위치++]-'0'; if(++숫자수>3||xëyma>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        dëkkuwaay=dëkkuwaay<<8|xëyma;
        if(부분<3&&(현재위치>=diir_xëyma||Tekst[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=diir_xëyma)mp_raise_OSError(MP_EINVAL);
    return dëkkuwaay;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *Tegtal_TABLO) {
    (void)항목수; uint32_t dëkkuwaay=인터넷주소읽기(Tegtal_TABLO[1]);
    int 접속번호=mp_obj_get_int(Tegtal_TABLO[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t mbir;mp_get_buffer_raise(Tegtal_TABLO[3],&mbir,MP_BUFFER_READ);
    struct pk_sockaddr_in luñu_name={0};luñu_name.sin_family=AF_INET;luñu_name.sin_port=pk_htons(접속번호);luñu_name.sin_addr.s_addr=pk_htonl(dëkkuwaay);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(Tegtal_TABLO[0]),(uintptr_t)mbir.buf,mbir.len,0,(uintptr_t)&luñu_name,sizeof(luñu_name))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t bara_denc_yombal) {
    unsigned char mbir[512]; struct pk_sockaddr_in Nàttangoo_xëyma; pk_socklen_t diir_mbir = sizeof(Nàttangoo_xëyma);
    intptr_t tolluwaay = 결과검사(사용자호출(35, mp_obj_get_int(bara_denc_yombal), (uintptr_t)mbir, 512, 0, (uintptr_t)&Nàttangoo_xëyma, (uintptr_t)&diir_mbir));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(mbir, tolluwaay), MP_OBJ_NEW_SMALL_INT(pk_htons(Nàttangoo_xëyma.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t bara_denc_yombal) { 결과검사(사용자호출(4, mp_obj_get_int(bara_denc_yombal), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t sos_dawal(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,net_Njaboot,dawal_mbaal,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,sos_dawal);
static mp_obj_t JOKKOO_dawal(mp_obj_t 종단,mp_obj_t dëkkuwaay_SMS,mp_obj_t àlluwa_tur) {
    int 접속번호=mp_obj_get_int(àlluwa_tur); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 dëkkuwaay={0}; dëkkuwaay.dëkkuwaay_Njaboot=net_Njaboot;
    dëkkuwaay.접속번호=망차례짧은수(접속번호); dëkkuwaay.dëkkuwaayu_Internet.dëkkuwaay_xëyma=mbaal_lëmm(인터넷주소읽기(dëkkuwaay_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&dëkkuwaay,sizeof(dëkkuwaay),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(dawal_Jokkalóo_yëf,JOKKOO_dawal);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int diir_xëyma=mp_obj_get_int(한도); if(diir_xëyma<1||diir_xëyma>512)mp_raise_OSError(MP_EINVAL);
    unsigned char mbir[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)mbir,diir_xëyma,0,0,0));
    return mp_obj_new_bytes(mbir,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(dawal_jangkat_yëf,흐름읽기);
static mp_obj_t biir_dawal(mp_obj_t 종단,mp_obj_t Këmb_xëyma) {
    mp_buffer_info_t mbir; mp_get_buffer_raise(Këmb_xëyma,&mbir,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)mbir.buf,mbir.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(dawal_Writer_yëf,biir_dawal);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t tur_253d1510) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)Yoonu_jëmale_Tegtal(tur_253d1510),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t sos_dàmb(mp_obj_t tur_253d1510) {
    결과검사(사용자호출(18,(uintptr_t)Yoonu_jëmale_Tegtal(tur_253d1510),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,sos_dàmb);
static mp_obj_t dandal_dàmb(mp_obj_t tur_253d1510) {
    결과검사(사용자호출(18,(uintptr_t)Yoonu_jëmale_Tegtal(tur_253d1510),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,dandal_dàmb);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&dawal_Jokkalóo_yëf) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&dawal_jangkat_yëf) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&dawal_Writer_yëf) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&bara_denc_jangkat_yëf) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&bara_denc_Writer_yëf) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Yeetekaay_ak_Montar_yëf) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
