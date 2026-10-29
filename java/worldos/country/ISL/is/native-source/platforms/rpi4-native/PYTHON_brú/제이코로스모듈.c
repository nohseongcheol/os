// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t NIÐURSTAÐA) { if (NIÐURSTAÐA < 0) mp_raise_OSError(-NIÐURSTAÐA); return NIÐURSTAÐA; }
static const char *slóð_frumbreyta(mp_obj_t VALUE) {
    size_t vara_COUNT; const char *SLÓÐ = mp_obj_str_get_data(VALUE, &vara_COUNT);
    if (!vara_COUNT || vara_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < vara_COUNT; 순번++) if (!SLÓÐ[순번]) mp_raise_OSError(MP_EINVAL);
    return SLÓÐ;
}
static mp_obj_t 파일읽기(mp_obj_t Heiti) {
    intptr_t skrá_hald = 결과검사(사용자호출(3, (uintptr_t)slóð_frumbreyta(Heiti), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Stærð = 결과검사(사용자호출(9, skrá_hald, 0, 0, 0, 0, 0));
        vstr_t gögn; vstr_init_len(&gögn, Stærð);
        intptr_t NIÐURSTAÐA = 사용자호출(2, skrá_hald, (uintptr_t)gögn.buf, Stærð, 0, 0, 0);
        결과검사(NIÐURSTAÐA); gögn.len = NIÐURSTAÐA;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&gögn);
        nlr_pop(); 사용자호출(4, skrá_hald, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, skrá_hald, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(skrá_Lesari_hlutur, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Stærð=mp_obj_get_int(한도);
    if(Stærð<0||Stærð>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t gögn; vstr_init_len(&gögn,Stærð);
    intptr_t vara_COUNT=사용자호출(2,0,(uintptr_t)gögn.buf,Stærð,0,0,0);
    if(vara_COUNT<0) { vstr_clear(&gögn); 결과검사(vara_COUNT); }
    gögn.len=vara_COUNT; return mp_obj_new_bytes_from_vstr(&gögn);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t skrifa_skrá(mp_obj_t Heiti, mp_obj_t Efni_VALUE) {
    const char *SLÓÐ = slóð_frumbreyta(Heiti);
    mp_buffer_info_t gögn; mp_get_buffer_raise(Efni_VALUE, &gögn, MP_BUFFER_READ);
    if (gögn.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t skrá_hald = 결과검사(사용자호출(3, (uintptr_t)SLÓÐ, 577, 0, 0, 0, 0));
    intptr_t færsla_COUNT = 사용자호출(1, skrá_hald, (uintptr_t)gögn.buf, gögn.len, 0, 0, 0);
    사용자호출(4, skrá_hald, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(færsla_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(skrá_Writer_hlutur, skrifa_skrá);
static mp_obj_t fjarlægja_skrá(mp_obj_t Heiti) { 결과검사(사용자호출(11, (uintptr_t)slóð_frumbreyta(Heiti), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, fjarlægja_skrá);
static mp_obj_t 사각형그리기(size_t vara_COUNT, const mp_obj_t *frumbreyta_ARRAY) {
    (void)vara_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(frumbreyta_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Stærð[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Stærð);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t klukka_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(klukka_hlutur, klukka_VALUE);
static mp_obj_t UDP_opið(mp_obj_t tengisnúmer) {
    int gögn_staða = mp_obj_get_int(tengisnúmer); if (gögn_staða < 0 || gögn_staða > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t skrá_hald = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(gögn_staða); 첫째값.sin_addr.s_addr = 0;
    intptr_t NIÐURSTAÐA = 사용자호출(33, skrá_hald, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (NIÐURSTAÐA < 0) { 사용자호출(4, skrá_hald, 0, 0, 0, 0, 0); 결과검사(NIÐURSTAÐA); }
    return mp_obj_new_int(skrá_hald);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_opið_OBJ, UDP_opið);
static mp_obj_t UDP_senda(mp_obj_t skrá_hald, mp_obj_t tengisnúmer, mp_obj_t Efni_VALUE) {
    int gögn_staða = mp_obj_get_int(tengisnúmer); if (gögn_staða < 1 || gögn_staða > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t gögn; mp_get_buffer_raise(Efni_VALUE, &gögn, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(gögn_staða); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(skrá_hald), (uintptr_t)gögn.buf, gögn.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_senda_OBJ, UDP_senda);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t lengd_VALUE; const char *Texti=mp_obj_str_get_data(VALUE,&lengd_VALUE);
    unsigned 현재위치=0; uint32_t slóð=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,tölustafur_COUNT=0;
        while(현재위치<lengd_VALUE&&Texti[현재위치]>='0'&&Texti[현재위치]<='9') {
            VALUE=VALUE*10+Texti[현재위치++]-'0'; if(++tölustafur_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!tölustafur_COUNT)mp_raise_OSError(MP_EINVAL);
        slóð=slóð<<8|VALUE;
        if(부분<3&&(현재위치>=lengd_VALUE||Texti[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=lengd_VALUE)mp_raise_OSError(MP_EINVAL);
    return slóð;
}
static mp_obj_t 전문주소전송(size_t færsla_COUNT, const mp_obj_t *frumbreyta_ARRAY) {
    (void)færsla_COUNT; uint32_t slóð=인터넷주소읽기(frumbreyta_ARRAY[1]);
    int tengisnúmer=mp_obj_get_int(frumbreyta_ARRAY[2]);if(tengisnúmer<1||tengisnúmer>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t gögn;mp_get_buffer_raise(frumbreyta_ARRAY[3],&gögn,MP_BUFFER_READ);
    struct pk_sockaddr_in markmið={0};markmið.sin_family=AF_INET;markmið.sin_port=pk_htons(tengisnúmer);markmið.sin_addr.s_addr=pk_htonl(slóð);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(frumbreyta_ARRAY[0]),(uintptr_t)gögn.buf,gögn.len,0,(uintptr_t)&markmið,sizeof(markmið))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t skrá_hald) {
    unsigned char gögn[512]; struct pk_sockaddr_in jafningi_VALUE; pk_socklen_t lengd_gögn = sizeof(jafningi_VALUE);
    intptr_t Stærð = 결과검사(사용자호출(35, mp_obj_get_int(skrá_hald), (uintptr_t)gögn, 512, 0, (uintptr_t)&jafningi_VALUE, (uintptr_t)&lengd_gögn));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(gögn, Stærð), MP_OBJ_NEW_SMALL_INT(pk_htons(jafningi_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_loka(mp_obj_t skrá_hald) { 결과검사(사용자호출(4, mp_obj_get_int(skrá_hald), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_loka_OBJ, UDP_loka);
static mp_obj_t opið_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,skýið_Fjölskylda,Stream_Net,Stream_flutningur_samskiptaregla,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,opið_Stream);
static mp_obj_t TENGJA_Stream(mp_obj_t endastöð,mp_obj_t slóð_SMS,mp_obj_t INDEX) {
    int tengisnúmer=mp_obj_get_int(INDEX); if(tengisnúmer<1||tengisnúmer>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 slóð={0}; slóð.slóð_Fjölskylda=skýið_Fjölskylda;
    slóð.tengisnúmer=망차례짧은수(tengisnúmer); slóð.veffang.slóð_VALUE=Net_heiltala(인터넷주소읽기(slóð_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(endastöð),(uintptr_t)&slóð,sizeof(slóð),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_Tengill_hlutur,TENGJA_Stream);
static mp_obj_t 흐름읽기(mp_obj_t endastöð,mp_obj_t 한도) {
    int lengd_VALUE=mp_obj_get_int(한도); if(lengd_VALUE<1||lengd_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char gögn[512];
    intptr_t vara_COUNT=결과검사(사용자호출(2,mp_obj_get_int(endastöð),(uintptr_t)gögn,lengd_VALUE,0,0,0));
    return mp_obj_new_bytes(gögn,vara_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Lesari_hlutur,흐름읽기);
static mp_obj_t skrifa_Stream(mp_obj_t endastöð,mp_obj_t Efni_VALUE) {
    mp_buffer_info_t gögn; mp_get_buffer_raise(Efni_VALUE,&gögn,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(endastöð),(uintptr_t)gögn.buf,gögn.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Writer_hlutur,skrifa_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Bíddu_hlutur,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Heiti) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)slóð_frumbreyta(Heiti),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t stofna_skráasafn(mp_obj_t Heiti) {
    결과검사(사용자호출(18,(uintptr_t)slóð_frumbreyta(Heiti),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,stofna_skráasafn);
static mp_obj_t fjarlægja_skráasafn(mp_obj_t Heiti) {
    결과검사(사용자호출(18,(uintptr_t)slóð_frumbreyta(Heiti),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,fjarlægja_skráasafn);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_Tengill_hlutur) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_Lesari_hlutur) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Writer_hlutur) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&Bíddu_hlutur) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&skrá_Lesari_hlutur) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&skrá_Writer_hlutur) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&klukka_hlutur) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_opið_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_senda_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_loka_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
