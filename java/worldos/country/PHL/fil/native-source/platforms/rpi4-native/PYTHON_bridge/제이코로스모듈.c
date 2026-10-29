// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t sukat) { if (sukat < 0) mp_raise_OSError(-sukat); return sukat; }
static const char *path_argumento(mp_obj_t VALUE) {
    size_t item_COUNT; const char *path = mp_obj_str_get_data(VALUE, &item_COUNT);
    if (!item_COUNT || item_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < item_COUNT; 순번++) if (!path[순번]) mp_raise_OSError(MP_EINVAL);
    return path;
}
static mp_obj_t 파일읽기(mp_obj_t pangalan) {
    intptr_t file_hawakán = 결과검사(사용자호출(3, (uintptr_t)path_argumento(pangalan), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t sukat_82232621 = 결과검사(사용자호출(9, file_hawakán, 0, 0, 0, 0, 0));
        vstr_t data; vstr_init_len(&data, sukat_82232621);
        intptr_t sukat = 사용자호출(2, file_hawakán, (uintptr_t)data.buf, sukat_82232621, 0, 0, 0);
        결과검사(sukat); data.len = sukat;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&data);
        nlr_pop(); 사용자호출(4, file_hawakán, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, file_hawakán, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(file_Tagabasa_bagay, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t sukat_82232621=mp_obj_get_int(한도);
    if(sukat_82232621<0||sukat_82232621>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t data; vstr_init_len(&data,sukat_82232621);
    intptr_t item_COUNT=사용자호출(2,0,(uintptr_t)data.buf,sukat_82232621,0,0,0);
    if(item_COUNT<0) { vstr_clear(&data); 결과검사(item_COUNT); }
    data.len=item_COUNT; return mp_obj_new_bytes_from_vstr(&data);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t sumulat_file(mp_obj_t pangalan, mp_obj_t Nilalaman_VALUE) {
    const char *path = path_argumento(pangalan);
    mp_buffer_info_t data; mp_get_buffer_raise(Nilalaman_VALUE, &data, MP_BUFFER_READ);
    if (data.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t file_hawakán = 결과검사(사용자호출(3, (uintptr_t)path, 577, 0, 0, 0, 0));
    intptr_t pagpasok_COUNT = 사용자호출(1, file_hawakán, (uintptr_t)data.buf, data.len, 0, 0, 0);
    사용자호출(4, file_hawakán, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(pagpasok_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(file_Pansulat_bagay, sumulat_file);
static mp_obj_t tanggalin_file(mp_obj_t pangalan) { 결과검사(사용자호출(11, (uintptr_t)path_argumento(pangalan), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, tanggalin_file);
static mp_obj_t 사각형그리기(size_t item_COUNT, const mp_obj_t *argumento_ARRAY) {
    (void)item_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argumento_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t sukat_82232621[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, sukat_82232621);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Orasan_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Orasan_bagay, Orasan_VALUE);
static mp_obj_t UDP_buksan(mp_obj_t numero_ng_port) {
    int data_posisyon = mp_obj_get_int(numero_ng_port); if (data_posisyon < 0 || data_posisyon > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t file_hawakán = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_posisyon); 첫째값.sin_addr.s_addr = 0;
    intptr_t sukat = 사용자호출(33, file_hawakán, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (sukat < 0) { 사용자호출(4, file_hawakán, 0, 0, 0, 0, 0); 결과검사(sukat); }
    return mp_obj_new_int(file_hawakán);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_buksan_OBJ, UDP_buksan);
static mp_obj_t UDP_i_email(mp_obj_t file_hawakán, mp_obj_t numero_ng_port, mp_obj_t Nilalaman_VALUE) {
    int data_posisyon = mp_obj_get_int(numero_ng_port); if (data_posisyon < 1 || data_posisyon > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data; mp_get_buffer_raise(Nilalaman_VALUE, &data, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_posisyon); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(file_hawakán), (uintptr_t)data.buf, data.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_i_email_OBJ, UDP_i_email);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t haba_VALUE; const char *SMS=mp_obj_str_get_data(VALUE,&haba_VALUE);
    unsigned 현재위치=0; uint32_t email=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,digit_COUNT=0;
        while(현재위치<haba_VALUE&&SMS[현재위치]>='0'&&SMS[현재위치]<='9') {
            VALUE=VALUE*10+SMS[현재위치++]-'0'; if(++digit_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!digit_COUNT)mp_raise_OSError(MP_EINVAL);
        email=email<<8|VALUE;
        if(부분<3&&(현재위치>=haba_VALUE||SMS[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=haba_VALUE)mp_raise_OSError(MP_EINVAL);
    return email;
}
static mp_obj_t 전문주소전송(size_t pagpasok_COUNT, const mp_obj_t *argumento_ARRAY) {
    (void)pagpasok_COUNT; uint32_t email=인터넷주소읽기(argumento_ARRAY[1]);
    int numero_ng_port=mp_obj_get_int(argumento_ARRAY[2]);if(numero_ng_port<1||numero_ng_port>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data;mp_get_buffer_raise(argumento_ARRAY[3],&data,MP_BUFFER_READ);
    struct pk_sockaddr_in layunin={0};layunin.sin_family=AF_INET;layunin.sin_port=pk_htons(numero_ng_port);layunin.sin_addr.s_addr=pk_htonl(email);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argumento_ARRAY[0]),(uintptr_t)data.buf,data.len,0,(uintptr_t)&layunin,sizeof(layunin))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t file_hawakán) {
    unsigned char data[512]; struct pk_sockaddr_in peer_VALUE; pk_socklen_t haba_data = sizeof(peer_VALUE);
    intptr_t sukat_82232621 = 결과검사(사용자호출(35, mp_obj_get_int(file_hawakán), (uintptr_t)data, 512, 0, (uintptr_t)&peer_VALUE, (uintptr_t)&haba_data));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(data, sukat_82232621), MP_OBJ_NEW_SMALL_INT(pk_htons(peer_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_isara(mp_obj_t file_hawakán) { 결과검사(사용자호출(4, mp_obj_get_int(file_hawakán), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_isara_OBJ, UDP_isara);
static mp_obj_t buksan_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,cloud_Pamilya,Stream_Network,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,buksan_Stream);
static mp_obj_t CONNECT_Stream(mp_obj_t 종단,mp_obj_t email_SMS,mp_obj_t INDEX) {
    int numero_ng_port=mp_obj_get_int(INDEX); if(numero_ng_port<1||numero_ng_port>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 email={0}; email.email_Pamilya=cloud_Pamilya;
    email.numero_ng_port=망차례짧은수(numero_ng_port); email.Internet_address.email_VALUE=Network_integer_buong_numero(인터넷주소읽기(email_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&email,sizeof(email),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_tagapagkabit_bagay,CONNECT_Stream);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int haba_VALUE=mp_obj_get_int(한도); if(haba_VALUE<1||haba_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char data[512];
    intptr_t item_COUNT=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)data,haba_VALUE,0,0,0));
    return mp_obj_new_bytes(data,item_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Tagabasa_bagay,흐름읽기);
static mp_obj_t sumulat_Stream(mp_obj_t 종단,mp_obj_t Nilalaman_VALUE) {
    mp_buffer_info_t data; mp_get_buffer_raise(Nilalaman_VALUE,&data,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)data.buf,data.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Pansulat_bagay,sumulat_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(maghintay_bagay,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t pangalan) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)path_argumento(pangalan),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Create_Directory(mp_obj_t pangalan) {
    결과검사(사용자호출(18,(uintptr_t)path_argumento(pangalan),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Directory_creator_bagay,Create_Directory);
static mp_obj_t tanggalin_Directory(mp_obj_t pangalan) {
    결과검사(사용자호출(18,(uintptr_t)path_argumento(pangalan),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,tanggalin_Directory);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_tagapagkabit_bagay) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_Tagabasa_bagay) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Pansulat_bagay) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&maghintay_bagay) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&Directory_creator_bagay) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&file_Tagabasa_bagay) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&file_Pansulat_bagay) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Orasan_bagay) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_buksan_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_i_email_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_isara_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
