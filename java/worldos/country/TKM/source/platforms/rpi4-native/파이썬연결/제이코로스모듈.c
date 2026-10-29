// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *ýol_argument(mp_obj_t baha) {
    size_t 개수; const char *Ýol = mp_obj_str_get_data(baha, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!Ýol[순번]) mp_raise_OSError(MP_EINVAL);
    return Ýol;
}
static mp_obj_t 파일읽기(mp_obj_t Ad) {
    intptr_t faýl_ryçag = 결과검사(사용자호출(3, (uintptr_t)ýol_argument(Ad), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Ululyk = 결과검사(사용자호출(9, faýl_ryçag, 0, 0, 0, 0, 0));
        vstr_t maglumat; vstr_init_len(&maglumat, Ululyk);
        intptr_t 결과 = 사용자호출(2, faýl_ryçag, (uintptr_t)maglumat.buf, Ululyk, 0, 0, 0);
        결과검사(결과); maglumat.len = 결과;
        mp_obj_t baha = mp_obj_new_bytes_from_vstr(&maglumat);
        nlr_pop(); 사용자호출(4, faýl_ryçag, 0, 0, 0, 0, 0); return baha;
    }
    사용자호출(4, faýl_ryçag, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(faýl_okyjy_obýekt, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Ululyk=mp_obj_get_int(한도);
    if(Ululyk<0||Ululyk>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t maglumat; vstr_init_len(&maglumat,Ululyk);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)maglumat.buf,Ululyk,0,0,0);
    if(개수<0) { vstr_clear(&maglumat); 결과검사(개수); }
    maglumat.len=개수; return mp_obj_new_bytes_from_vstr(&maglumat);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t ýaz_faýl(mp_obj_t Ad, mp_obj_t Mazmun_baha) {
    const char *Ýol = ýol_argument(Ad);
    mp_buffer_info_t maglumat; mp_get_buffer_raise(Mazmun_baha, &maglumat, MP_BUFFER_READ);
    if (maglumat.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t faýl_ryçag = 결과검사(사용자호출(3, (uintptr_t)Ýol, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, faýl_ryçag, (uintptr_t)maglumat.buf, maglumat.len, 0, 0, 0);
    사용자호출(4, faýl_ryçag, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(faýl_Blog_Düzedijisi_obýekt, ýaz_faýl);
static mp_obj_t aýyr_faýl(mp_obj_t Ad) { 결과검사(사용자호출(11, (uintptr_t)ýol_argument(Ad), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, aýyr_faýl);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *argument_ARRAY) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argument_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Ululyk[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Ululyk);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t sagat_baha(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(sagat_obýekt, sagat_baha);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t faýl_ryçag = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, faýl_ryçag, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, faýl_ryçag, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(faýl_ryçag);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t faýl_ryçag, mp_obj_t 접속번호, mp_obj_t Mazmun_baha) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t maglumat; mp_get_buffer_raise(Mazmun_baha, &maglumat, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(faýl_ryçag), (uintptr_t)maglumat.buf, maglumat.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t baha) {
    size_t dowamlylyk_baha; const char *Metin=mp_obj_str_get_data(baha,&dowamlylyk_baha);
    unsigned 현재위치=0; uint32_t salgy=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned baha=0,숫자수=0;
        while(현재위치<dowamlylyk_baha&&Metin[현재위치]>='0'&&Metin[현재위치]<='9') {
            baha=baha*10+Metin[현재위치++]-'0'; if(++숫자수>3||baha>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        salgy=salgy<<8|baha;
        if(부분<3&&(현재위치>=dowamlylyk_baha||Metin[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=dowamlylyk_baha)mp_raise_OSError(MP_EINVAL);
    return salgy;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *argument_ARRAY) {
    (void)항목수; uint32_t salgy=인터넷주소읽기(argument_ARRAY[1]);
    int 접속번호=mp_obj_get_int(argument_ARRAY[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t maglumat;mp_get_buffer_raise(argument_ARRAY[3],&maglumat,MP_BUFFER_READ);
    struct pk_sockaddr_in niýet={0};niýet.sin_family=AF_INET;niýet.sin_port=pk_htons(접속번호);niýet.sin_addr.s_addr=pk_htonl(salgy);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argument_ARRAY[0]),(uintptr_t)maglumat.buf,maglumat.len,0,(uintptr_t)&niýet,sizeof(niýet))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t faýl_ryçag) {
    unsigned char maglumat[512]; struct pk_sockaddr_in deň_derejeli_düwün_baha; pk_socklen_t dowamlylyk_maglumat = sizeof(deň_derejeli_düwün_baha);
    intptr_t Ululyk = 결과검사(사용자호출(35, mp_obj_get_int(faýl_ryçag), (uintptr_t)maglumat, 512, 0, (uintptr_t)&deň_derejeli_düwün_baha, (uintptr_t)&dowamlylyk_maglumat));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(maglumat, Ululyk), MP_OBJ_NEW_SMALL_INT(pk_htons(deň_derejeli_düwün_baha.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t faýl_ryçag) { 결과검사(사용자호출(4, mp_obj_get_int(faýl_ryçag), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t aç_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,bulut_Maşgala,Stream_Tor,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,aç_Stream);
static mp_obj_t Birikme_Stream(mp_obj_t 종단,mp_obj_t salgy_SMS,mp_obj_t indeks) {
    int 접속번호=mp_obj_get_int(indeks); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 salgy={0}; salgy.salgy_Maşgala=bulut_Maşgala;
    salgy.접속번호=망차례짧은수(접속번호); salgy.Internet_salgy.salgy_baha=Tor_bitin(인터넷주소읽기(salgy_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&salgy,sizeof(salgy),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_birikdiriji_obýekt,Birikme_Stream);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int dowamlylyk_baha=mp_obj_get_int(한도); if(dowamlylyk_baha<1||dowamlylyk_baha>512)mp_raise_OSError(MP_EINVAL);
    unsigned char maglumat[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)maglumat,dowamlylyk_baha,0,0,0));
    return mp_obj_new_bytes(maglumat,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_okyjy_obýekt,흐름읽기);
static mp_obj_t ýaz_Stream(mp_obj_t 종단,mp_obj_t Mazmun_baha) {
    mp_buffer_info_t maglumat; mp_get_buffer_raise(Mazmun_baha,&maglumat,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)maglumat.buf,maglumat.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Blog_Düzedijisi_obýekt,ýaz_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Ad) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)ýol_argument(Ad),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t döretmek_katalog(mp_obj_t Ad) {
    결과검사(사용자호출(18,(uintptr_t)ýol_argument(Ad),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,döretmek_katalog);
static mp_obj_t aýyr_katalog(mp_obj_t Ad) {
    결과검사(사용자호출(18,(uintptr_t)ýol_argument(Ad),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,aýyr_katalog);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_birikdiriji_obýekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_okyjy_obýekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Blog_Düzedijisi_obýekt) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&faýl_okyjy_obýekt) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&faýl_Blog_Düzedijisi_obýekt) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&sagat_obýekt) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
