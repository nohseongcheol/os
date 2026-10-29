// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t forretningsmål) { if (forretningsmål < 0) mp_raise_OSError(-forretningsmål); return forretningsmål; }
static const char *bane_argument(mp_obj_t VALUE) {
    size_t vare_COUNT; const char *STIGE = mp_obj_str_get_data(VALUE, &vare_COUNT);
    if (!vare_COUNT || vare_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < vare_COUNT; 순번++) if (!STIGE[순번]) mp_raise_OSError(MP_EINVAL);
    return STIGE;
}
static mp_obj_t 파일읽기(mp_obj_t Namn) {
    intptr_t fil_handtak = 결과검사(사용자호출(3, (uintptr_t)bane_argument(Namn), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Storleik = 결과검사(사용자호출(9, fil_handtak, 0, 0, 0, 0, 0));
        vstr_t data; vstr_init_len(&data, Storleik);
        intptr_t forretningsmål = 사용자호출(2, fil_handtak, (uintptr_t)data.buf, Storleik, 0, 0, 0);
        결과검사(forretningsmål); data.len = forretningsmål;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&data);
        nlr_pop(); 사용자호출(4, fil_handtak, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, fil_handtak, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(fil_Lesar_objekt, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Storleik=mp_obj_get_int(한도);
    if(Storleik<0||Storleik>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t data; vstr_init_len(&data,Storleik);
    intptr_t vare_COUNT=사용자호출(2,0,(uintptr_t)data.buf,Storleik,0,0,0);
    if(vare_COUNT<0) { vstr_clear(&data); 결과검사(vare_COUNT); }
    data.len=vare_COUNT; return mp_obj_new_bytes_from_vstr(&data);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t skrive_fil(mp_obj_t Namn, mp_obj_t Innhald_VALUE) {
    const char *STIGE = bane_argument(Namn);
    mp_buffer_info_t data; mp_get_buffer_raise(Innhald_VALUE, &data, MP_BUFFER_READ);
    if (data.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t fil_handtak = 결과검사(사용자호출(3, (uintptr_t)STIGE, 577, 0, 0, 0, 0));
    intptr_t oppføring_COUNT = 사용자호출(1, fil_handtak, (uintptr_t)data.buf, data.len, 0, 0, 0);
    사용자호출(4, fil_handtak, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(oppføring_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(fil_Skrive_objekt, skrive_fil);
static mp_obj_t fjerne_fil(mp_obj_t Namn) { 결과검사(사용자호출(11, (uintptr_t)bane_argument(Namn), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, fjerne_fil);
static mp_obj_t 사각형그리기(size_t vare_COUNT, const mp_obj_t *argument_ARRAY) {
    (void)vare_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argument_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Storleik[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Storleik);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Klokke_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Klokke_objekt, Klokke_VALUE);
static mp_obj_t 전문열기(mp_obj_t portnummer) {
    int data_plassere = mp_obj_get_int(portnummer); if (data_plassere < 0 || data_plassere > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t fil_handtak = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_plassere); 첫째값.sin_addr.s_addr = 0;
    intptr_t forretningsmål = 사용자호출(33, fil_handtak, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (forretningsmål < 0) { 사용자호출(4, fil_handtak, 0, 0, 0, 0, 0); 결과검사(forretningsmål); }
    return mp_obj_new_int(fil_handtak);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t fil_handtak, mp_obj_t portnummer, mp_obj_t Innhald_VALUE) {
    int data_plassere = mp_obj_get_int(portnummer); if (data_plassere < 1 || data_plassere > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data; mp_get_buffer_raise(Innhald_VALUE, &data, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_plassere); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(fil_handtak), (uintptr_t)data.buf, data.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t lengd_VALUE; const char *Tekst=mp_obj_str_get_data(VALUE,&lengd_VALUE);
    unsigned betalt_plassere=0; uint32_t ADDRESS=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,siffer_COUNT=0;
        while(betalt_plassere<lengd_VALUE&&Tekst[betalt_plassere]>='0'&&Tekst[betalt_plassere]<='9') {
            VALUE=VALUE*10+Tekst[betalt_plassere++]-'0'; if(++siffer_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!siffer_COUNT)mp_raise_OSError(MP_EINVAL);
        ADDRESS=ADDRESS<<8|VALUE;
        if(부분<3&&(betalt_plassere>=lengd_VALUE||Tekst[betalt_plassere++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(betalt_plassere!=lengd_VALUE)mp_raise_OSError(MP_EINVAL);
    return ADDRESS;
}
static mp_obj_t 전문주소전송(size_t oppføring_COUNT, const mp_obj_t *argument_ARRAY) {
    (void)oppføring_COUNT; uint32_t ADDRESS=인터넷주소읽기(argument_ARRAY[1]);
    int portnummer=mp_obj_get_int(argument_ARRAY[2]);if(portnummer<1||portnummer>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data;mp_get_buffer_raise(argument_ARRAY[3],&data,MP_BUFFER_READ);
    struct pk_sockaddr_in mål={0};mål.sin_family=AF_INET;mål.sin_port=pk_htons(portnummer);mål.sin_addr.s_addr=pk_htonl(ADDRESS);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argument_ARRAY[0]),(uintptr_t)data.buf,data.len,0,(uintptr_t)&mål,sizeof(mål))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t fil_handtak) {
    unsigned char data[512]; struct pk_sockaddr_in node_VALUE_6a3b6fa7; pk_socklen_t lengd_data = sizeof(node_VALUE_6a3b6fa7);
    intptr_t Storleik = 결과검사(사용자호출(35, mp_obj_get_int(fil_handtak), (uintptr_t)data, 512, 0, (uintptr_t)&node_VALUE_6a3b6fa7, (uintptr_t)&lengd_data));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(data, Storleik), MP_OBJ_NEW_SMALL_INT(pk_htons(node_VALUE_6a3b6fa7.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t fil_handtak) { 결과검사(사용자호출(4, mp_obj_get_int(fil_handtak), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t opne_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,sky_Familie,Stream_Nettverk,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,opne_Stream);
static mp_obj_t KOPLE_TIL_Stream(mp_obj_t endepunkt,mp_obj_t ADDRESS_SMS,mp_obj_t INDEX) {
    int portnummer=mp_obj_get_int(INDEX); if(portnummer<1||portnummer>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ADDRESS={0}; ADDRESS.ADDRESS_Familie=sky_Familie;
    ADDRESS.portnummer=망차례짧은수(portnummer); ADDRESS.Internett_adresse.ADDRESS_VALUE=Nettverk_heiltal(인터넷주소읽기(ADDRESS_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(endepunkt),(uintptr_t)&ADDRESS,sizeof(ADDRESS),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_Kopling_objekt,KOPLE_TIL_Stream);
static mp_obj_t 흐름읽기(mp_obj_t endepunkt,mp_obj_t 한도) {
    int lengd_VALUE=mp_obj_get_int(한도); if(lengd_VALUE<1||lengd_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char data[512];
    intptr_t vare_COUNT=결과검사(사용자호출(2,mp_obj_get_int(endepunkt),(uintptr_t)data,lengd_VALUE,0,0,0));
    return mp_obj_new_bytes(data,vare_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Lesar_objekt,흐름읽기);
static mp_obj_t skrive_Stream(mp_obj_t endepunkt,mp_obj_t Innhald_VALUE) {
    mp_buffer_info_t data; mp_get_buffer_raise(Innhald_VALUE,&data,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(endepunkt),(uintptr_t)data.buf,data.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Skrive_objekt,skrive_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(vent_objekt,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Namn) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)bane_argument(Namn),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Opprett_katalog(mp_obj_t Namn) {
    결과검사(사용자호출(18,(uintptr_t)bane_argument(Namn),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,Opprett_katalog);
static mp_obj_t fjerne_katalog(mp_obj_t Namn) {
    결과검사(사용자호출(18,(uintptr_t)bane_argument(Namn),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,fjerne_katalog);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_Kopling_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_Lesar_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Skrive_objekt) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&vent_objekt) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&fil_Lesar_objekt) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&fil_Skrive_objekt) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Klokke_objekt) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
