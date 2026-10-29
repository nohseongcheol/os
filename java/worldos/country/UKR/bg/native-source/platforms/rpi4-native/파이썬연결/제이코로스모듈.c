// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t РЕЗУЛТАТ) { if (РЕЗУЛТАТ < 0) mp_raise_OSError(-РЕЗУЛТАТ); return РЕЗУЛТАТ; }
static const char *път_аргумент(mp_obj_t стойност) {
    size_t 개수; const char *ПЪТ = mp_obj_str_get_data(стойност, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!ПЪТ[순번]) mp_raise_OSError(MP_EINVAL);
    return ПЪТ;
}
static mp_obj_t 파일읽기(mp_obj_t Име) {
    intptr_t Файл_манипулатор = 결과검사(사용자호출(3, (uintptr_t)път_аргумент(Име), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Размер = 결과검사(사용자호출(9, Файл_манипулатор, 0, 0, 0, 0, 0));
        vstr_t данни; vstr_init_len(&данни, Размер);
        intptr_t РЕЗУЛТАТ = 사용자호출(2, Файл_манипулатор, (uintptr_t)данни.buf, Размер, 0, 0, 0);
        결과검사(РЕЗУЛТАТ); данни.len = РЕЗУЛТАТ;
        mp_obj_t стойност = mp_obj_new_bytes_from_vstr(&данни);
        nlr_pop(); 사용자호출(4, Файл_манипулатор, 0, 0, 0, 0, 0); return стойност;
    }
    사용자호출(4, Файл_манипулатор, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Файл_читател_обект, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Размер=mp_obj_get_int(한도);
    if(Размер<0||Размер>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t данни; vstr_init_len(&данни,Размер);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)данни.buf,Размер,0,0,0);
    if(개수<0) { vstr_clear(&данни); 결과검사(개수); }
    данни.len=개수; return mp_obj_new_bytes_from_vstr(&данни);
}
static MP_DEFINE_CONST_FUN_OBJ_1(стандартен_вход_читател_обект, 표준입력읽기);
static mp_obj_t записване_Файл(mp_obj_t Име, mp_obj_t Съдържание_стойност) {
    const char *ПЪТ = път_аргумент(Име);
    mp_buffer_info_t данни; mp_get_buffer_raise(Съдържание_стойност, &данни, MP_BUFFER_READ);
    if (данни.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t Файл_манипулатор = 결과검사(사용자호출(3, (uintptr_t)ПЪТ, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, Файл_манипулатор, (uintptr_t)данни.buf, данни.len, 0, 0, 0);
    사용자호출(4, Файл_манипулатор, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(파일쓰기객체, записване_Файл);
static mp_obj_t премахвам_Файл(mp_obj_t Име) { 결과검사(사용자호출(11, (uintptr_t)път_аргумент(Име), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, премахвам_Файл);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *аргумент_масив) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(аргумент_масив[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(правоъгълник_обект, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Размер[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Размер);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Часовник_стойност(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Часовник_обект, Часовник_стойност);
static mp_obj_t 전문열기(mp_obj_t номер_на_порт) {
    int данни_позиция = mp_obj_get_int(номер_на_порт); if (данни_позиция < 0 || данни_позиция > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t Файл_манипулатор = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(данни_позиция); 첫째값.sin_addr.s_addr = 0;
    intptr_t РЕЗУЛТАТ = 사용자호출(33, Файл_манипулатор, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (РЕЗУЛТАТ < 0) { 사용자호출(4, Файл_манипулатор, 0, 0, 0, 0, 0); 결과검사(РЕЗУЛТАТ); }
    return mp_obj_new_int(Файл_манипулатор);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t Файл_манипулатор, mp_obj_t номер_на_порт, mp_obj_t Съдържание_стойност) {
    int данни_позиция = mp_obj_get_int(номер_на_порт); if (данни_позиция < 1 || данни_позиция > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t данни; mp_get_buffer_raise(Съдържание_стойност, &данни, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(данни_позиция); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(Файл_манипулатор), (uintptr_t)данни.buf, данни.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t стойност) {
    size_t 길이; const char *Текст=mp_obj_str_get_data(стойност,&길이);
    unsigned в_срок_позиция=0; uint32_t адрес=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned стойност=0,숫자수=0;
        while(в_срок_позиция<길이&&Текст[в_срок_позиция]>='0'&&Текст[в_срок_позиция]<='9') {
            стойност=стойност*10+Текст[в_срок_позиция++]-'0'; if(++숫자수>3||стойност>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        адрес=адрес<<8|стойност;
        if(부분<3&&(в_срок_позиция>=길이||Текст[в_срок_позиция++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(в_срок_позиция!=길이)mp_raise_OSError(MP_EINVAL);
    return адрес;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *аргумент_масив) {
    (void)항목수; uint32_t адрес=인터넷주소읽기(аргумент_масив[1]);
    int номер_на_порт=mp_obj_get_int(аргумент_масив[2]);if(номер_на_порт<1||номер_на_порт>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t данни;mp_get_buffer_raise(аргумент_масив[3],&данни,MP_BUFFER_READ);
    struct pk_sockaddr_in цел={0};цел.sin_family=AF_INET;цел.sin_port=pk_htons(номер_на_порт);цел.sin_addr.s_addr=pk_htonl(адрес);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(аргумент_масив[0]),(uintptr_t)данни.buf,данни.len,0,(uintptr_t)&цел,sizeof(цел))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t Файл_манипулатор) {
    unsigned char данни[512]; struct pk_sockaddr_in крайно_устройство_стойност; pk_socklen_t 길이값 = sizeof(крайно_устройство_стойност);
    intptr_t Размер = 결과검사(사용자호출(35, mp_obj_get_int(Файл_манипулатор), (uintptr_t)данни, 512, 0, (uintptr_t)&крайно_устройство_стойност, (uintptr_t)&길이값));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(данни, Размер), MP_OBJ_NEW_SMALL_INT(pk_htons(крайно_устройство_стойност.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t Файл_манипулатор) { 결과검사(사용자호출(4, mp_obj_get_int(Файл_манипулатор), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t отварям_поток(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,облак_семейни,поток_мрежа,поток_транспортен_протокол,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,отварям_поток);
static mp_obj_t връзка_поток(mp_obj_t участник,mp_obj_t адрес_Текст,mp_obj_t индекс) {
    int номер_на_порт=mp_obj_get_int(индекс); if(номер_на_порт<1||номер_на_порт>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 адрес={0}; адрес.адрес_семейни=облак_семейни;
    адрес.номер_на_порт=망차례짧은수(номер_на_порт); адрес.Интернет_адрес.адрес_стойност=мрежа_цяло_число(인터넷주소읽기(адрес_Текст));
    결과검사(사용자호출(37,mp_obj_get_int(участник),(uintptr_t)&адрес,sizeof(адрес),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(поток_Конектор_обект,връзка_поток);
static mp_obj_t 흐름읽기(mp_obj_t участник,mp_obj_t 한도) {
    int 길이=mp_obj_get_int(한도); if(길이<1||길이>512)mp_raise_OSError(MP_EINVAL);
    unsigned char данни[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(участник),(uintptr_t)данни,길이,0,0,0));
    return mp_obj_new_bytes(данни,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(поток_читател_обект,흐름읽기);
static mp_obj_t записване_поток(mp_obj_t участник,mp_obj_t Съдържание_стойност) {
    mp_buffer_info_t данни; mp_get_buffer_raise(Съдържание_стойност,&данни,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(участник),(uintptr_t)данни.buf,данни.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(흐름쓰기객체,записване_поток);
static mp_obj_t 잠시기다리기(mp_obj_t час_стойност) {
    결과검사(사용자호출(17,mp_obj_get_int(час_стойност),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(почакай_обект,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Име) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)път_аргумент(Име),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Създаване_указател(mp_obj_t Име) {
    결과검사(사용자호출(18,(uintptr_t)път_аргумент(Име),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(указател_автор_обект,Създаване_указател);
static mp_obj_t премахвам_указател(mp_obj_t Име) {
    결과검사(사용자호출(18,(uintptr_t)път_аргумент(Име),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,премахвам_указател);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&поток_Конектор_обект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&поток_читател_обект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&흐름쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&почакай_обект) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&указател_автор_обект) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&стандартен_вход_читател_обект) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Файл_читател_обект) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&파일쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&правоъгълник_обект) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Часовник_обект) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
