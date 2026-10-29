// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t результат) { if (результат < 0) mp_raise_OSError(-результат); return результат; }
static const char *шлях_аргумент(mp_obj_t значення) {
    size_t 개수; const char *шлях = mp_obj_str_get_data(значення, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!шлях[순번]) mp_raise_OSError(MP_EINVAL);
    return шлях;
}
static mp_obj_t 파일읽기(mp_obj_t Назва) {
    intptr_t Файл_маркер = 결과검사(사용자호출(3, (uintptr_t)шлях_аргумент(Назва), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Розмір = 결과검사(사용자호출(9, Файл_маркер, 0, 0, 0, 0, 0));
        vstr_t дані; vstr_init_len(&дані, Розмір);
        intptr_t результат = 사용자호출(2, Файл_маркер, (uintptr_t)дані.buf, Розмір, 0, 0, 0);
        결과검사(результат); дані.len = результат;
        mp_obj_t значення = mp_obj_new_bytes_from_vstr(&дані);
        nlr_pop(); 사용자호출(4, Файл_маркер, 0, 0, 0, 0, 0); return значення;
    }
    사용자호출(4, Файл_маркер, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Файл_читач_об_єкт, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Розмір=mp_obj_get_int(한도);
    if(Розмір<0||Розмір>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t дані; vstr_init_len(&дані,Розмір);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)дані.buf,Розмір,0,0,0);
    if(개수<0) { vstr_clear(&дані); 결과검사(개수); }
    дані.len=개수; return mp_obj_new_bytes_from_vstr(&дані);
}
static MP_DEFINE_CONST_FUN_OBJ_1(стандартний_ввід_читач_об_єкт, 표준입력읽기);
static mp_obj_t записування_Файл(mp_obj_t Назва, mp_obj_t Вміст_значення) {
    const char *шлях = шлях_аргумент(Назва);
    mp_buffer_info_t дані; mp_get_buffer_raise(Вміст_значення, &дані, MP_BUFFER_READ);
    if (дані.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t Файл_маркер = 결과검사(사용자호출(3, (uintptr_t)шлях, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, Файл_маркер, (uintptr_t)дані.buf, дані.len, 0, 0, 0);
    사용자호출(4, Файл_маркер, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(파일쓰기객체, записування_Файл);
static mp_obj_t вилучати_Файл(mp_obj_t Назва) { 결과검사(사용자호출(11, (uintptr_t)шлях_аргумент(Назва), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, вилучати_Файл);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *аргумент_масив) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(аргумент_масив[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(прямокутник_об_єкт, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Розмір[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Розмір);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Годинник_значення(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Годинник_об_єкт, Годинник_значення);
static mp_obj_t протокол_користувацьких_дейтаграм_відкрито(mp_obj_t номер_порту) {
    int дані_посада = mp_obj_get_int(номер_порту); if (дані_посада < 0 || дані_посада > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t Файл_маркер = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(дані_посада); 첫째값.sin_addr.s_addr = 0;
    intptr_t результат = 사용자호출(33, Файл_маркер, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (результат < 0) { 사용자호출(4, Файл_маркер, 0, 0, 0, 0, 0); 결과검사(результат); }
    return mp_obj_new_int(Файл_маркер);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, протокол_користувацьких_дейтаграм_відкрито);
static mp_obj_t протокол_користувацьких_дейтаграм_надсилати(mp_obj_t Файл_маркер, mp_obj_t номер_порту, mp_obj_t Вміст_значення) {
    int дані_посада = mp_obj_get_int(номер_порту); if (дані_посада < 1 || дані_посада > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t дані; mp_get_buffer_raise(Вміст_значення, &дані, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(дані_посада); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(Файл_маркер), (uintptr_t)дані.buf, дані.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, протокол_користувацьких_дейтаграм_надсилати);
static uint32_t 인터넷주소읽기(mp_obj_t значення) {
    size_t 길이; const char *текст=mp_obj_str_get_data(значення,&길이);
    unsigned чинний_посада=0; uint32_t Адреса=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned значення=0,숫자수=0;
        while(чинний_посада<길이&&текст[чинний_посада]>='0'&&текст[чинний_посада]<='9') {
            значення=значення*10+текст[чинний_посада++]-'0'; if(++숫자수>3||значення>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        Адреса=Адреса<<8|значення;
        if(부분<3&&(чинний_посада>=길이||текст[чинний_посада++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(чинний_посада!=길이)mp_raise_OSError(MP_EINVAL);
    return Адреса;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *аргумент_масив) {
    (void)항목수; uint32_t Адреса=인터넷주소읽기(аргумент_масив[1]);
    int номер_порту=mp_obj_get_int(аргумент_масив[2]);if(номер_порту<1||номер_порту>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t дані;mp_get_buffer_raise(аргумент_масив[3],&дані,MP_BUFFER_READ);
    struct pk_sockaddr_in мета={0};мета.sin_family=AF_INET;мета.sin_port=pk_htons(номер_порту);мета.sin_addr.s_addr=pk_htonl(Адреса);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(аргумент_масив[0]),(uintptr_t)дані.buf,дані.len,0,(uintptr_t)&мета,sizeof(мета))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t Файл_маркер) {
    unsigned char дані[512]; struct pk_sockaddr_in точка_значення; pk_socklen_t 길이값 = sizeof(точка_значення);
    intptr_t Розмір = 결과검사(사용자호출(35, mp_obj_get_int(Файл_маркер), (uintptr_t)дані, 512, 0, (uintptr_t)&точка_значення, (uintptr_t)&길이값));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(дані, Розмір), MP_OBJ_NEW_SMALL_INT(pk_htons(точка_значення.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t протокол_користувацьких_дейтаграм_Закрити(mp_obj_t Файл_маркер) { 결과검사(사용자호출(4, mp_obj_get_int(Файл_маркер), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, протокол_користувацьких_дейтаграм_Закрити);
static mp_obj_t відкрито_потік(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,хмара_сім_я,потік_мережа,потік_транспортний_протокол,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,відкрито_потік);
static mp_obj_t зв_язок_потік(mp_obj_t учасник,mp_obj_t адреса_Текст,mp_obj_t індекс) {
    int номер_порту=mp_obj_get_int(індекс); if(номер_порту<1||номер_порту>65535)mp_raise_OSError(MP_EINVAL);
    struct хмара_сокет_адреса Адреса={0}; Адреса.адреса_сім_я=хмара_сім_я;
    Адреса.номер_порту=망차례짧은수(номер_порту); Адреса.адреса_в_Інтернеті.адреса_значення=мережа_ціле_число(인터넷주소읽기(адреса_Текст));
    결과검사(사용자호출(37,mp_obj_get_int(учасник),(uintptr_t)&Адреса,sizeof(Адреса),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(потік_Конектор_об_єкт,зв_язок_потік);
static mp_obj_t 흐름읽기(mp_obj_t учасник,mp_obj_t 한도) {
    int 길이=mp_obj_get_int(한도); if(길이<1||길이>512)mp_raise_OSError(MP_EINVAL);
    unsigned char дані[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(учасник),(uintptr_t)дані,길이,0,0,0));
    return mp_obj_new_bytes(дані,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(потік_читач_об_єкт,흐름읽기);
static mp_obj_t записування_потік(mp_obj_t учасник,mp_obj_t Вміст_значення) {
    mp_buffer_info_t дані; mp_get_buffer_raise(Вміст_значення,&дані,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(учасник),(uintptr_t)дані.buf,дані.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(흐름쓰기객체,записування_потік);
static mp_obj_t 잠시기다리기(mp_obj_t час_значення) {
    결과검사(사용자호출(17,mp_obj_get_int(час_значення),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(хвилиноньку_панове_об_єкт,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Назва) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)шлях_аргумент(Назва),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Створення_Каталог(mp_obj_t Назва) {
    결과검사(사용자호출(18,(uintptr_t)шлях_аргумент(Назва),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Каталог_автор_об_єкт,Створення_Каталог);
static mp_obj_t вилучати_Каталог(mp_obj_t Назва) {
    결과검사(사용자호출(18,(uintptr_t)шлях_аргумент(Назва),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,вилучати_Каталог);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&потік_Конектор_об_єкт) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&потік_читач_об_єкт) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&흐름쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&хвилиноньку_панове_об_єкт) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&Каталог_автор_об_єкт) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&стандартний_ввід_читач_об_єкт) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Файл_читач_об_єкт) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&파일쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&прямокутник_об_єкт) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Годинник_об_єкт) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
