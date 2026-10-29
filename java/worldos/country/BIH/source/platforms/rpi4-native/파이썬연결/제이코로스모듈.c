// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *пут_аргумент(mp_obj_t вриједност) {
    size_t 개수; const char *пут = mp_obj_str_get_data(вриједност, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!пут[순번]) mp_raise_OSError(MP_EINVAL);
    return пут;
}
static mp_obj_t 파일읽기(mp_obj_t назив) {
    intptr_t фајл_хватиште = 결과검사(사용자호출(3, (uintptr_t)пут_аргумент(назив), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t подесити_величину = 결과검사(사용자호출(9, фајл_хватиште, 0, 0, 0, 0, 0));
        vstr_t подаци; vstr_init_len(&подаци, подесити_величину);
        intptr_t 결과 = 사용자호출(2, фајл_хватиште, (uintptr_t)подаци.buf, подесити_величину, 0, 0, 0);
        결과검사(결과); подаци.len = 결과;
        mp_obj_t вриједност = mp_obj_new_bytes_from_vstr(&подаци);
        nlr_pop(); 사용자호출(4, фајл_хватиште, 0, 0, 0, 0, 0); return вриједност;
    }
    사용자호출(4, фајл_хватиште, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(фајл_читач_објект, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t подесити_величину=mp_obj_get_int(한도);
    if(подесити_величину<0||подесити_величину>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t подаци; vstr_init_len(&подаци,подесити_величину);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)подаци.buf,подесити_величину,0,0,0);
    if(개수<0) { vstr_clear(&подаци); 결과검사(개수); }
    подаци.len=개수; return mp_obj_new_bytes_from_vstr(&подаци);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t писати_фајл(mp_obj_t назив, mp_obj_t Садржај_вриједност) {
    const char *пут = пут_аргумент(назив);
    mp_buffer_info_t подаци; mp_get_buffer_raise(Садржај_вриједност, &подаци, MP_BUFFER_READ);
    if (подаци.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t фајл_хватиште = 결과검사(사용자호출(3, (uintptr_t)пут, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, фајл_хватиште, (uintptr_t)подаци.buf, подаци.len, 0, 0, 0);
    사용자호출(4, фајл_хватиште, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(фајл_Windows_Live_Писац_објект, писати_фајл);
static mp_obj_t уклонити_фајл(mp_obj_t назив) { 결과검사(사용자호출(11, (uintptr_t)пут_аргумент(назив), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, уклонити_фајл);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *аргумент_низ) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(аргумент_низ[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t подесити_величину[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, подесити_величину);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t сат_вриједност(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(сат_објект, сат_вриједност);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t фајл_хватиште = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, фајл_хватиште, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, фајл_хватиште, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(фајл_хватиште);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t фајл_хватиште, mp_obj_t 접속번호, mp_obj_t Садржај_вриједност) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t подаци; mp_get_buffer_raise(Садржај_вриједност, &подаци, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(фајл_хватиште), (uintptr_t)подаци.buf, подаци.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t вриједност) {
    size_t дужина_вриједност; const char *текст=mp_obj_str_get_data(вриједност,&дужина_вриједност);
    unsigned 현재위치=0; uint32_t адреса=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned вриједност=0,숫자수=0;
        while(현재위치<дужина_вриједност&&текст[현재위치]>='0'&&текст[현재위치]<='9') {
            вриједност=вриједност*10+текст[현재위치++]-'0'; if(++숫자수>3||вриједност>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        адреса=адреса<<8|вриједност;
        if(부분<3&&(현재위치>=дужина_вриједност||текст[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=дужина_вриједност)mp_raise_OSError(MP_EINVAL);
    return адреса;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *аргумент_низ) {
    (void)항목수; uint32_t адреса=인터넷주소읽기(аргумент_низ[1]);
    int 접속번호=mp_obj_get_int(аргумент_низ[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t подаци;mp_get_buffer_raise(аргумент_низ[3],&подаци,MP_BUFFER_READ);
    struct pk_sockaddr_in циљ={0};циљ.sin_family=AF_INET;циљ.sin_port=pk_htons(접속번호);циљ.sin_addr.s_addr=pk_htonl(адреса);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(аргумент_низ[0]),(uintptr_t)подаци.buf,подаци.len,0,(uintptr_t)&циљ,sizeof(циљ))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t фајл_хватиште) {
    unsigned char подаци[512]; struct pk_sockaddr_in peer_вриједност; pk_socklen_t дужина_подаци = sizeof(peer_вриједност);
    intptr_t подесити_величину = 결과검사(사용자호출(35, mp_obj_get_int(фајл_хватиште), (uintptr_t)подаци, 512, 0, (uintptr_t)&peer_вриједност, (uintptr_t)&дужина_подаци));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(подаци, подесити_величину), MP_OBJ_NEW_SMALL_INT(pk_htons(peer_вриједност.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t фајл_хватиште) { 결과검사(사용자호출(4, mp_obj_get_int(фајл_хватиште), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t отворити_ток(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,인터넷주소갈래,ток_Мрежа,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,отворити_ток);
static mp_obj_t повезати_ток(mp_obj_t крајња_тачка,mp_obj_t адреса_текст,mp_obj_t индекс) {
    int 접속번호=mp_obj_get_int(индекс); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 адреса={0}; адреса.адреса_породица=인터넷주소갈래;
    адреса.접속번호=망차례짧은수(접속번호); адреса.интернетска_адреса.адреса_вриједност=Мрежа_цијели_број(인터넷주소읽기(адреса_текст));
    결과검사(사용자호출(37,mp_obj_get_int(крајња_тачка),(uintptr_t)&адреса,sizeof(адреса),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ток_конектор_објект,повезати_ток);
static mp_obj_t 흐름읽기(mp_obj_t крајња_тачка,mp_obj_t 한도) {
    int дужина_вриједност=mp_obj_get_int(한도); if(дужина_вриједност<1||дужина_вриједност>512)mp_raise_OSError(MP_EINVAL);
    unsigned char подаци[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(крајња_тачка),(uintptr_t)подаци,дужина_вриједност,0,0,0));
    return mp_obj_new_bytes(подаци,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ток_читач_објект,흐름읽기);
static mp_obj_t писати_ток(mp_obj_t крајња_тачка,mp_obj_t Садржај_вриједност) {
    mp_buffer_info_t подаци; mp_get_buffer_raise(Садржај_вриједност,&подаци,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(крајња_тачка),(uintptr_t)подаци.buf,подаци.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ток_Windows_Live_Писац_објект,писати_ток);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t назив) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)пут_аргумент(назив),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t 폴더만들기(mp_obj_t назив) {
    결과검사(사용자호출(18,(uintptr_t)пут_аргумент(назив),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,폴더만들기);
static mp_obj_t уклонити_директориј(mp_obj_t назив) {
    결과검사(사용자호출(18,(uintptr_t)пут_аргумент(назив),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,уклонити_директориј);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ток_конектор_објект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ток_читач_објект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&ток_Windows_Live_Писац_објект) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&фајл_читач_објект) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&фајл_Windows_Live_Писац_објект) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&сат_објект) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
