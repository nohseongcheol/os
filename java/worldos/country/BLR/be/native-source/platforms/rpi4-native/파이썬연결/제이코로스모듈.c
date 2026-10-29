// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *шлях_аргумент(mp_obj_t значэнне) {
    size_t 개수; const char *ШЛЯХ = mp_obj_str_get_data(значэнне, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!ШЛЯХ[순번]) mp_raise_OSError(MP_EINVAL);
    return ШЛЯХ;
}
static mp_obj_t 파일읽기(mp_obj_t Назва) {
    intptr_t файл_маркер = 결과검사(사용자호출(3, (uintptr_t)шлях_аргумент(Назва), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Памер = 결과검사(사용자호출(9, файл_маркер, 0, 0, 0, 0, 0));
        vstr_t дадзеныя; vstr_init_len(&дадзеныя, Памер);
        intptr_t 결과 = 사용자호출(2, файл_маркер, (uintptr_t)дадзеныя.buf, Памер, 0, 0, 0);
        결과검사(결과); дадзеныя.len = 결과;
        mp_obj_t значэнне = mp_obj_new_bytes_from_vstr(&дадзеныя);
        nlr_pop(); 사용자호출(4, файл_маркер, 0, 0, 0, 0, 0); return значэнне;
    }
    사용자호출(4, файл_маркер, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(файл_чытач_аб_ект, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Памер=mp_obj_get_int(한도);
    if(Памер<0||Памер>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t дадзеныя; vstr_init_len(&дадзеныя,Памер);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)дадзеныя.buf,Памер,0,0,0);
    if(개수<0) { vstr_clear(&дадзеныя); 결과검사(개수); }
    дадзеныя.len=개수; return mp_obj_new_bytes_from_vstr(&дадзеныя);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t напісаць_файл(mp_obj_t Назва, mp_obj_t кантэнт_значэнне) {
    const char *ШЛЯХ = шлях_аргумент(Назва);
    mp_buffer_info_t дадзеныя; mp_get_buffer_raise(кантэнт_значэнне, &дадзеныя, MP_BUFFER_READ);
    if (дадзеныя.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t файл_маркер = 결과검사(사용자호출(3, (uintptr_t)ШЛЯХ, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, файл_маркер, (uintptr_t)дадзеныя.buf, дадзеныя.len, 0, 0, 0);
    사용자호출(4, файл_маркер, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(файл_Рэдактар_блогаў_аб_ект, напісаць_файл);
static mp_obj_t выдаліць_файл(mp_obj_t Назва) { 결과검사(사용자호출(11, (uintptr_t)шлях_аргумент(Назва), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, выдаліць_файл);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *аргумент_масіў) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(аргумент_масіў[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Памер[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Памер);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t гадзіннік_значэнне(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(гадзіннік_аб_ект, гадзіннік_значэнне);
static mp_obj_t 전문열기(mp_obj_t нумар_порта) {
    int 자료위치 = mp_obj_get_int(нумар_порта); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t файл_маркер = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, файл_маркер, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, файл_маркер, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(файл_маркер);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t файл_маркер, mp_obj_t нумар_порта, mp_obj_t кантэнт_значэнне) {
    int 자료위치 = mp_obj_get_int(нумар_порта); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t дадзеныя; mp_get_buffer_raise(кантэнт_значэнне, &дадзеныя, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(файл_маркер), (uintptr_t)дадзеныя.buf, дадзеныя.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t значэнне) {
    size_t даўжыня_значэнне; const char *Тэкст=mp_obj_str_get_data(значэнне,&даўжыня_значэнне);
    unsigned 현재위치=0; uint32_t адрас=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned значэнне=0,숫자수=0;
        while(현재위치<даўжыня_значэнне&&Тэкст[현재위치]>='0'&&Тэкст[현재위치]<='9') {
            значэнне=значэнне*10+Тэкст[현재위치++]-'0'; if(++숫자수>3||значэнне>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        адрас=адрас<<8|значэнне;
        if(부분<3&&(현재위치>=даўжыня_значэнне||Тэкст[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=даўжыня_значэнне)mp_raise_OSError(MP_EINVAL);
    return адрас;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *аргумент_масіў) {
    (void)항목수; uint32_t адрас=인터넷주소읽기(аргумент_масіў[1]);
    int нумар_порта=mp_obj_get_int(аргумент_масіў[2]);if(нумар_порта<1||нумар_порта>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t дадзеныя;mp_get_buffer_raise(аргумент_масіў[3],&дадзеныя,MP_BUFFER_READ);
    struct pk_sockaddr_in мэтавы_паказчык={0};мэтавы_паказчык.sin_family=AF_INET;мэтавы_паказчык.sin_port=pk_htons(нумар_порта);мэтавы_паказчык.sin_addr.s_addr=pk_htonl(адрас);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(аргумент_масіў[0]),(uintptr_t)дадзеныя.buf,дадзеныя.len,0,(uintptr_t)&мэтавы_паказчык,sizeof(мэтавы_паказчык))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t файл_маркер) {
    unsigned char дадзеныя[512]; struct pk_sockaddr_in аднарангавы_значэнне; pk_socklen_t даўжыня_дадзеныя = sizeof(аднарангавы_значэнне);
    intptr_t Памер = 결과검사(사용자호출(35, mp_obj_get_int(файл_маркер), (uintptr_t)дадзеныя, 512, 0, (uintptr_t)&аднарангавы_значэнне, (uintptr_t)&даўжыня_дадзеныя));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(дадзеныя, Памер), MP_OBJ_NEW_SMALL_INT(pk_htons(аднарангавы_значэнне.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t файл_маркер) { 결과검사(사용자호출(4, mp_obj_get_int(файл_маркер), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t адкрыць_паток(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,воблака_Сям_я,паток_Сетка,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,адкрыць_паток);
static mp_obj_t злучаць_паток(mp_obj_t 종단,mp_obj_t адрас_Тэкст,mp_obj_t індэкс) {
    int нумар_порта=mp_obj_get_int(індэкс); if(нумар_порта<1||нумар_порта>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 адрас={0}; адрас.адрас_Сям_я=воблака_Сям_я;
    адрас.нумар_порта=망차례짧은수(нумар_порта); адрас.інтэрнэт_адрас.адрас_значэнне=Сетка_цэлы_лік(인터넷주소읽기(адрас_Тэкст));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&адрас,sizeof(адрас),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(паток_злучальнік_аб_ект,злучаць_паток);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int даўжыня_значэнне=mp_obj_get_int(한도); if(даўжыня_значэнне<1||даўжыня_значэнне>512)mp_raise_OSError(MP_EINVAL);
    unsigned char дадзеныя[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)дадзеныя,даўжыня_значэнне,0,0,0));
    return mp_obj_new_bytes(дадзеныя,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(паток_чытач_аб_ект,흐름읽기);
static mp_obj_t напісаць_паток(mp_obj_t 종단,mp_obj_t кантэнт_значэнне) {
    mp_buffer_info_t дадзеныя; mp_get_buffer_raise(кантэнт_значэнне,&дадзеныя,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)дадзеныя.buf,дадзеныя.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(паток_Рэдактар_блогаў_аб_ект,напісаць_паток);
static mp_obj_t 잠시기다리기(mp_obj_t час_значэнне) {
    결과검사(사용자호출(17,mp_obj_get_int(час_значэнне),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(чакае_аб_ект,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Назва) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)шлях_аргумент(Назва),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t стварыць_каталог(mp_obj_t Назва) {
    결과검사(사용자호출(18,(uintptr_t)шлях_аргумент(Назва),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,стварыць_каталог);
static mp_obj_t выдаліць_каталог(mp_obj_t Назва) {
    결과검사(사용자호출(18,(uintptr_t)шлях_аргумент(Назва),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,выдаліць_каталог);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&паток_злучальнік_аб_ект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&паток_чытач_аб_ект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&паток_Рэдактар_блогаў_аб_ект) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&чакае_аб_ект) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&файл_чытач_аб_ект) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&файл_Рэдактар_блогаў_аб_ект) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&гадзіннік_аб_ект) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
