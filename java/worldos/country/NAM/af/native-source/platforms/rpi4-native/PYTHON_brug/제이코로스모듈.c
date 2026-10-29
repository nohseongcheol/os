// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t maatreël) { if (maatreël < 0) mp_raise_OSError(-maatreël); return maatreël; }
static const char *pad_argument(mp_obj_t VALUE) {
    size_t item_COUNT; const char *Pad = mp_obj_str_get_data(VALUE, &item_COUNT);
    if (!item_COUNT || item_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < item_COUNT; 순번++) if (!Pad[순번]) mp_raise_OSError(MP_EINVAL);
    return Pad;
}
static mp_obj_t 파일읽기(mp_obj_t Naam) {
    intptr_t lêer_handvatsel = 결과검사(사용자호출(3, (uintptr_t)pad_argument(Naam), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Grootte = 결과검사(사용자호출(9, lêer_handvatsel, 0, 0, 0, 0, 0));
        vstr_t data; vstr_init_len(&data, Grootte);
        intptr_t maatreël = 사용자호출(2, lêer_handvatsel, (uintptr_t)data.buf, Grootte, 0, 0, 0);
        결과검사(maatreël); data.len = maatreël;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&data);
        nlr_pop(); 사용자호출(4, lêer_handvatsel, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, lêer_handvatsel, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(lêer_Leser_objek, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Grootte=mp_obj_get_int(한도);
    if(Grootte<0||Grootte>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t data; vstr_init_len(&data,Grootte);
    intptr_t item_COUNT=사용자호출(2,0,(uintptr_t)data.buf,Grootte,0,0,0);
    if(item_COUNT<0) { vstr_clear(&data); 결과검사(item_COUNT); }
    data.len=item_COUNT; return mp_obj_new_bytes_from_vstr(&data);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t skryf_lêer(mp_obj_t Naam, mp_obj_t Inhoud_VALUE) {
    const char *Pad = pad_argument(Naam);
    mp_buffer_info_t data; mp_get_buffer_raise(Inhoud_VALUE, &data, MP_BUFFER_READ);
    if (data.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t lêer_handvatsel = 결과검사(사용자호출(3, (uintptr_t)Pad, 577, 0, 0, 0, 0));
    intptr_t inskrywing_COUNT = 사용자호출(1, lêer_handvatsel, (uintptr_t)data.buf, data.len, 0, 0, 0);
    사용자호출(4, lêer_handvatsel, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(inskrywing_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(lêer_Skrywer_objek, skryf_lêer);
static mp_obj_t verwyder_lêer(mp_obj_t Naam) { 결과검사(사용자호출(11, (uintptr_t)pad_argument(Naam), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, verwyder_lêer);
static mp_obj_t 사각형그리기(size_t item_COUNT, const mp_obj_t *argument_ARRAY) {
    (void)item_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argument_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Grootte[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Grootte);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Klok_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Klok_objek, Klok_VALUE);
static mp_obj_t GDP_Gebruikersdatagramprotokol_skep(mp_obj_t 접속번호) {
    int data_plaas = mp_obj_get_int(접속번호); if (data_plaas < 0 || data_plaas > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t lêer_handvatsel = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_plaas); 첫째값.sin_addr.s_addr = 0;
    intptr_t maatreël = 사용자호출(33, lêer_handvatsel, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (maatreël < 0) { 사용자호출(4, lêer_handvatsel, 0, 0, 0, 0, 0); 결과검사(maatreël); }
    return mp_obj_new_int(lêer_handvatsel);
}
static MP_DEFINE_CONST_FUN_OBJ_1(GDP_Gebruikersdatagramprotokol_skep_OBJ, GDP_Gebruikersdatagramprotokol_skep);
static mp_obj_t GDP_Gebruikersdatagramprotokol_e_pos(mp_obj_t lêer_handvatsel, mp_obj_t 접속번호, mp_obj_t Inhoud_VALUE) {
    int data_plaas = mp_obj_get_int(접속번호); if (data_plaas < 1 || data_plaas > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data; mp_get_buffer_raise(Inhoud_VALUE, &data, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_plaas); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(lêer_handvatsel), (uintptr_t)data.buf, data.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(GDP_Gebruikersdatagramprotokol_e_pos_OBJ, GDP_Gebruikersdatagramprotokol_e_pos);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t lengte_VALUE; const char *Teks=mp_obj_str_get_data(VALUE,&lengte_VALUE);
    unsigned 현재위치=0; uint32_t adres=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,syfer_COUNT=0;
        while(현재위치<lengte_VALUE&&Teks[현재위치]>='0'&&Teks[현재위치]<='9') {
            VALUE=VALUE*10+Teks[현재위치++]-'0'; if(++syfer_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!syfer_COUNT)mp_raise_OSError(MP_EINVAL);
        adres=adres<<8|VALUE;
        if(부분<3&&(현재위치>=lengte_VALUE||Teks[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=lengte_VALUE)mp_raise_OSError(MP_EINVAL);
    return adres;
}
static mp_obj_t 전문주소전송(size_t inskrywing_COUNT, const mp_obj_t *argument_ARRAY) {
    (void)inskrywing_COUNT; uint32_t adres=인터넷주소읽기(argument_ARRAY[1]);
    int 접속번호=mp_obj_get_int(argument_ARRAY[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data;mp_get_buffer_raise(argument_ARRAY[3],&data,MP_BUFFER_READ);
    struct pk_sockaddr_in teiken={0};teiken.sin_family=AF_INET;teiken.sin_port=pk_htons(접속번호);teiken.sin_addr.s_addr=pk_htonl(adres);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argument_ARRAY[0]),(uintptr_t)data.buf,data.len,0,(uintptr_t)&teiken,sizeof(teiken))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t lêer_handvatsel) {
    unsigned char data[512]; struct pk_sockaddr_in portuur_VALUE; pk_socklen_t lengte_data = sizeof(portuur_VALUE);
    intptr_t Grootte = 결과검사(사용자호출(35, mp_obj_get_int(lêer_handvatsel), (uintptr_t)data, 512, 0, (uintptr_t)&portuur_VALUE, (uintptr_t)&lengte_data));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(data, Grootte), MP_OBJ_NEW_SMALL_INT(pk_htons(portuur_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t GDP_Gebruikersdatagramprotokol_sluit(mp_obj_t lêer_handvatsel) { 결과검사(사용자호출(4, mp_obj_get_int(lêer_handvatsel), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(GDP_Gebruikersdatagramprotokol_sluit_OBJ, GDP_Gebruikersdatagramprotokol_sluit);
static mp_obj_t skep_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,wolk_Gesin,Stream_Netwerk,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,skep_Stream);
static mp_obj_t KOPPEL_Stream(mp_obj_t 종단,mp_obj_t adres_SMS,mp_obj_t INDEX) {
    int 접속번호=mp_obj_get_int(INDEX); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 adres={0}; adres.adres_Gesin=wolk_Gesin;
    adres.접속번호=망차례짧은수(접속번호); adres.internetadres.adres_VALUE=Netwerk_heelgetal(인터넷주소읽기(adres_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&adres,sizeof(adres),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_Verbinder_objek,KOPPEL_Stream);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int lengte_VALUE=mp_obj_get_int(한도); if(lengte_VALUE<1||lengte_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char data[512];
    intptr_t item_COUNT=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)data,lengte_VALUE,0,0,0));
    return mp_obj_new_bytes(data,item_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Leser_objek,흐름읽기);
static mp_obj_t skryf_Stream(mp_obj_t 종단,mp_obj_t Inhoud_VALUE) {
    mp_buffer_info_t data; mp_get_buffer_raise(Inhoud_VALUE,&data,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)data.buf,data.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Skrywer_objek,skryf_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t tyd_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(tyd_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(wag_objek,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Naam) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)pad_argument(Naam),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Skep_gids(mp_obj_t Naam) {
    결과검사(사용자호출(18,(uintptr_t)pad_argument(Naam),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,Skep_gids);
static mp_obj_t verwyder_gids(mp_obj_t Naam) {
    결과검사(사용자호출(18,(uintptr_t)pad_argument(Naam),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,verwyder_gids);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_Verbinder_objek) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_Leser_objek) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Skrywer_objek) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&wag_objek) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&lêer_Leser_objek) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&lêer_Skrywer_objek) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Klok_objek) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&GDP_Gebruikersdatagramprotokol_skep_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&GDP_Gebruikersdatagramprotokol_e_pos_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&GDP_Gebruikersdatagramprotokol_sluit_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
