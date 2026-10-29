// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *зам_аргумент(mp_obj_t утга) {
    size_t 개수; const char *ЗАМ = mp_obj_str_get_data(утга, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!ЗАМ[순번]) mp_raise_OSError(MP_EINVAL);
    return ЗАМ;
}
static mp_obj_t 파일읽기(mp_obj_t Нэр) {
    intptr_t файл_барих = 결과검사(사용자호출(3, (uintptr_t)зам_аргумент(Нэр), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Хэмжээ = 결과검사(사용자호출(9, файл_барих, 0, 0, 0, 0, 0));
        vstr_t өгөгдөл; vstr_init_len(&өгөгдөл, Хэмжээ);
        intptr_t 결과 = 사용자호출(2, файл_барих, (uintptr_t)өгөгдөл.buf, Хэмжээ, 0, 0, 0);
        결과검사(결과); өгөгдөл.len = 결과;
        mp_obj_t утга = mp_obj_new_bytes_from_vstr(&өгөгдөл);
        nlr_pop(); 사용자호출(4, файл_барих, 0, 0, 0, 0, 0); return утга;
    }
    사용자호출(4, файл_барих, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(файл_Уншигч_объект, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Хэмжээ=mp_obj_get_int(한도);
    if(Хэмжээ<0||Хэмжээ>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t өгөгдөл; vstr_init_len(&өгөгдөл,Хэмжээ);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)өгөгдөл.buf,Хэмжээ,0,0,0);
    if(개수<0) { vstr_clear(&өгөгдөл); 결과검사(개수); }
    өгөгдөл.len=개수; return mp_obj_new_bytes_from_vstr(&өгөгдөл);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t бичих_файл(mp_obj_t Нэр, mp_obj_t Агуулга_утга) {
    const char *ЗАМ = зам_аргумент(Нэр);
    mp_buffer_info_t өгөгдөл; mp_get_buffer_raise(Агуулга_утга, &өгөгдөл, MP_BUFFER_READ);
    if (өгөгдөл.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t файл_барих = 결과검사(사용자호출(3, (uintptr_t)ЗАМ, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, файл_барих, (uintptr_t)өгөгдөл.buf, өгөгдөл.len, 0, 0, 0);
    사용자호출(4, файл_барих, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(файл_Зохиолч_объект, бичих_файл);
static mp_obj_t арилгах_файл(mp_obj_t Нэр) { 결과검사(사용자호출(11, (uintptr_t)зам_аргумент(Нэр), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, арилгах_файл);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *аргумент_олонлог) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(аргумент_олонлог[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Хэмжээ[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Хэмжээ);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t тактын_дохио_утга(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(тактын_дохио_объект, тактын_дохио_утга);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t файл_барих = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, файл_барих, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, файл_барих, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(файл_барих);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t файл_барих, mp_obj_t 접속번호, mp_obj_t Агуулга_утга) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t өгөгдөл; mp_get_buffer_raise(Агуулга_утга, &өгөгдөл, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(файл_барих), (uintptr_t)өгөгдөл.buf, өгөгдөл.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t утга) {
    size_t урт_утга; const char *Бичвэр=mp_obj_str_get_data(утга,&урт_утга);
    unsigned 현재위치=0; uint32_t хаяг=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned утга=0,숫자수=0;
        while(현재위치<урт_утга&&Бичвэр[현재위치]>='0'&&Бичвэр[현재위치]<='9') {
            утга=утга*10+Бичвэр[현재위치++]-'0'; if(++숫자수>3||утга>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        хаяг=хаяг<<8|утга;
        if(부분<3&&(현재위치>=урт_утга||Бичвэр[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=урт_утга)mp_raise_OSError(MP_EINVAL);
    return хаяг;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *аргумент_олонлог) {
    (void)항목수; uint32_t хаяг=인터넷주소읽기(аргумент_олонлог[1]);
    int 접속번호=mp_obj_get_int(аргумент_олонлог[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t өгөгдөл;mp_get_buffer_raise(аргумент_олонлог[3],&өгөгдөл,MP_BUFFER_READ);
    struct pk_sockaddr_in зорилго={0};зорилго.sin_family=AF_INET;зорилго.sin_port=pk_htons(접속번호);зорилго.sin_addr.s_addr=pk_htonl(хаяг);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(аргумент_олонлог[0]),(uintptr_t)өгөгдөл.buf,өгөгдөл.len,0,(uintptr_t)&зорилго,sizeof(зорилго))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t файл_барих) {
    unsigned char өгөгдөл[512]; struct pk_sockaddr_in ижил_түвшин_утга; pk_socklen_t урт_өгөгдөл = sizeof(ижил_түвшин_утга);
    intptr_t Хэмжээ = 결과검사(사용자호출(35, mp_obj_get_int(файл_барих), (uintptr_t)өгөгдөл, 512, 0, (uintptr_t)&ижил_түвшин_утга, (uintptr_t)&урт_өгөгдөл));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(өгөгдөл, Хэмжээ), MP_OBJ_NEW_SMALL_INT(pk_htons(ижил_түвшин_утга.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t файл_барих) { 결과검사(사용자호출(4, mp_obj_get_int(файл_барих), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t нээх_урсгал(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,үүл_Гэр_бүл,урсгал_Сүлжээ,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,нээх_урсгал);
static mp_obj_t холбох_урсгал(mp_obj_t 종단,mp_obj_t хаяг_Бичвэр,mp_obj_t индекс) {
    int 접속번호=mp_obj_get_int(индекс); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 хаяг={0}; хаяг.хаяг_Гэр_бүл=үүл_Гэр_бүл;
    хаяг.접속번호=망차례짧은수(접속번호); хаяг.Интернет_хаяг.хаяг_утга=Сүлжээ_бүхэл_тоо(인터넷주소읽기(хаяг_Бичвэр));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&хаяг,sizeof(хаяг),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(урсгал_холбогч_объект,холбох_урсгал);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int урт_утга=mp_obj_get_int(한도); if(урт_утга<1||урт_утга>512)mp_raise_OSError(MP_EINVAL);
    unsigned char өгөгдөл[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)өгөгдөл,урт_утга,0,0,0));
    return mp_obj_new_bytes(өгөгдөл,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(урсгал_Уншигч_объект,흐름읽기);
static mp_obj_t бичих_урсгал(mp_obj_t 종단,mp_obj_t Агуулга_утга) {
    mp_buffer_info_t өгөгдөл; mp_get_buffer_raise(Агуулга_утга,&өгөгдөл,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)өгөгдөл.buf,өгөгдөл.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(урсгал_Зохиолч_объект,бичих_урсгал);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Нэр) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)зам_аргумент(Нэр),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t үүсгэх_лавлах(mp_obj_t Нэр) {
    결과검사(사용자호출(18,(uintptr_t)зам_аргумент(Нэр),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,үүсгэх_лавлах);
static mp_obj_t арилгах_лавлах(mp_obj_t Нэр) {
    결과검사(사용자호출(18,(uintptr_t)зам_аргумент(Нэр),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,арилгах_лавлах);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&урсгал_холбогч_объект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&урсгал_Уншигч_объект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&урсгал_Зохиолч_объект) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&файл_Уншигч_объект) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&файл_Зохиолч_объект) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&тактын_дохио_объект) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
