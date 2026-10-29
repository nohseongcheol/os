// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "сеть_ABI.h"
static intptr_t 결과검사(intptr_t результат) { if (результат < 0) mp_raise_OSError(-результат); return результат; }
static const char *путь_аргумент(mp_obj_t ЗНАЧЕН) {
    size_t товар_СЧЁТ; const char *путь = mp_obj_str_get_data(ЗНАЧЕН, &товар_СЧЁТ);
    if (!товар_СЧЁТ || товар_СЧЁТ > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < товар_СЧЁТ; 순번++) if (!путь[순번]) mp_raise_OSError(MP_EINVAL);
    return путь;
}
static mp_obj_t чтение_файл(mp_obj_t Название) {
    intptr_t дескриптор_файла = 결과검사(사용자호출(3, (uintptr_t)путь_аргумент(Название), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Размер = 결과검사(사용자호출(9, дескриптор_файла, 0, 0, 0, 0, 0));
        vstr_t данные; vstr_init_len(&данные, Размер);
        intptr_t результат = 사용자호출(2, дескриптор_файла, (uintptr_t)данные.buf, Размер, 0, 0, 0);
        결과검사(результат); данные.len = результат;
        mp_obj_t ЗНАЧЕН = mp_obj_new_bytes_from_vstr(&данные);
        nlr_pop(); 사용자호출(4, дескриптор_файла, 0, 0, 0, 0, 0); return ЗНАЧЕН;
    }
    사용자호출(4, дескриптор_файла, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(файл_Ридер_объект, чтение_файл);
static mp_obj_t чтение_стандарт_входные_данные(mp_obj_t 한도) {
    mp_int_t Размер=mp_obj_get_int(한도);
    if(Размер<0||Размер>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t данные; vstr_init_len(&данные,Размер);
    intptr_t товар_СЧЁТ=사용자호출(2,0,(uintptr_t)данные.buf,Размер,0,0,0);
    if(товар_СЧЁТ<0) { vstr_clear(&данные); 결과검사(товар_СЧЁТ); }
    данные.len=товар_СЧЁТ; return mp_obj_new_bytes_from_vstr(&данные);
}
static MP_DEFINE_CONST_FUN_OBJ_1(стандарт_входные_данные_Ридер_объект, чтение_стандарт_входные_данные);
static mp_obj_t запись_файл(mp_obj_t Название, mp_obj_t контент_ЗНАЧЕН) {
    const char *путь = путь_аргумент(Название);
    mp_buffer_info_t данные; mp_get_buffer_raise(контент_ЗНАЧЕН, &данные, MP_BUFFER_READ);
    if (данные.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t дескриптор_файла = 결과검사(사용자호출(3, (uintptr_t)путь, 577, 0, 0, 0, 0));
    intptr_t ввод_СЧЁТ = 사용자호출(1, дескриптор_файла, (uintptr_t)данные.buf, данные.len, 0, 0, 0);
    사용자호출(4, дескриптор_файла, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(ввод_СЧЁТ));
}
static MP_DEFINE_CONST_FUN_OBJ_2(файл_Редактор_блогов_объект, запись_файл);
static mp_obj_t удалить_файл(mp_obj_t Название) { 결과검사(사용자호출(11, (uintptr_t)путь_аргумент(Название), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, удалить_файл);
static mp_obj_t Paint_прямоугольник(size_t товар_СЧЁТ, const mp_obj_t *аргумент_МАССИВ) {
    (void)товар_СЧЁТ; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(аргумент_МАССИВ[순번]);
    결과검사(экран_прямоугольник(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(прямоугольник_объект, 5, 5, Paint_прямоугольник);
static mp_obj_t чтение_экран_изменить_размер(void) {
    mp_obj_t Размер[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Размер);
}
static MP_DEFINE_CONST_FUN_OBJ_0(экран_изменить_размер_объект, чтение_экран_изменить_размер);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(экран_минутку_объект, 화면입력기다리기);
static mp_obj_t Часы_ЗНАЧЕН(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Часы_объект, Часы_ЗНАЧЕН);
static mp_obj_t UDP_открыть(mp_obj_t номер_порта) {
    int данные_позиция = mp_obj_get_int(номер_порта); if (данные_позиция < 0 || данные_позиция > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t дескриптор_файла = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(данные_позиция); 첫째값.sin_addr.s_addr = 0;
    intptr_t результат = 사용자호출(33, дескриптор_файла, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (результат < 0) { 사용자호출(4, дескриптор_файла, 0, 0, 0, 0, 0); 결과검사(результат); }
    return mp_obj_new_int(дескриптор_файла);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_открыть_OBJ, UDP_открыть);
static mp_obj_t UDP_написать(mp_obj_t дескриптор_файла, mp_obj_t номер_порта, mp_obj_t контент_ЗНАЧЕН) {
    int данные_позиция = mp_obj_get_int(номер_порта); if (данные_позиция < 1 || данные_позиция > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t данные; mp_get_buffer_raise(контент_ЗНАЧЕН, &данные, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(данные_позиция); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(дескриптор_файла), (uintptr_t)данные.buf, данные.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_написать_OBJ, UDP_написать);
static uint32_t чтение_адрес_в_Интернете(mp_obj_t ЗНАЧЕН) {
    size_t длина_ЗНАЧЕН; const char *текст=mp_obj_str_get_data(ЗНАЧЕН,&длина_ЗНАЧЕН);
    unsigned текущий_позиция=0; uint32_t АДРЕС=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned ЗНАЧЕН=0,цифра_СЧЁТ=0;
        while(текущий_позиция<длина_ЗНАЧЕН&&текст[текущий_позиция]>='0'&&текст[текущий_позиция]<='9') {
            ЗНАЧЕН=ЗНАЧЕН*10+текст[текущий_позиция++]-'0'; if(++цифра_СЧЁТ>3||ЗНАЧЕН>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!цифра_СЧЁТ)mp_raise_OSError(MP_EINVAL);
        АДРЕС=АДРЕС<<8|ЗНАЧЕН;
        if(부분<3&&(текущий_позиция>=длина_ЗНАЧЕН||текст[текущий_позиция++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(текущий_позиция!=длина_ЗНАЧЕН)mp_raise_OSError(MP_EINVAL);
    return АДРЕС;
}
static mp_obj_t 전문주소전송(size_t ввод_СЧЁТ, const mp_obj_t *аргумент_МАССИВ) {
    (void)ввод_СЧЁТ; uint32_t АДРЕС=чтение_адрес_в_Интернете(аргумент_МАССИВ[1]);
    int номер_порта=mp_obj_get_int(аргумент_МАССИВ[2]);if(номер_порта<1||номер_порта>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t данные;mp_get_buffer_raise(аргумент_МАССИВ[3],&данные,MP_BUFFER_READ);
    struct pk_sockaddr_in целевое_значение={0};целевое_значение.sin_family=AF_INET;целевое_значение.sin_port=pk_htons(номер_порта);целевое_значение.sin_addr.s_addr=pk_htonl(АДРЕС);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(аргумент_МАССИВ[0]),(uintptr_t)данные.buf,данные.len,0,(uintptr_t)&целевое_значение,sizeof(целевое_значение))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t дескриптор_файла) {
    unsigned char данные[512]; struct pk_sockaddr_in одноранговый_ЗНАЧЕН; pk_socklen_t длина_данные = sizeof(одноранговый_ЗНАЧЕН);
    intptr_t Размер = 결과검사(사용자호출(35, mp_obj_get_int(дескриптор_файла), (uintptr_t)данные, 512, 0, (uintptr_t)&одноранговый_ЗНАЧЕН, (uintptr_t)&длина_данные));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(данные, Размер), MP_OBJ_NEW_SMALL_INT(pk_htons(одноранговый_ЗНАЧЕН.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Close(mp_obj_t дескриптор_файла) { 결과검사(사용자호출(4, mp_obj_get_int(дескриптор_файла), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Close_OBJ, UDP_Close);
static mp_obj_t открыть_поток(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,облако_Семья,поток_сеть,поток_транспортный_протокол,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,открыть_поток);
static mp_obj_t Connect_поток(mp_obj_t участник,mp_obj_t АДРЕС_SMS,mp_obj_t ИНДЕКС) {
    int номер_порта=mp_obj_get_int(ИНДЕКС); if(номер_порта<1||номер_порта>65535)mp_raise_OSError(MP_EINVAL);
    struct облако_сокет_АДРЕС АДРЕС={0}; АДРЕС.АДРЕС_Семья=облако_Семья;
    АДРЕС.номер_порта=망차례짧은수(номер_порта); АДРЕС.адрес_в_Интернете.АДРЕС_ЗНАЧЕН=сеть_целое_число(чтение_адрес_в_Интернете(АДРЕС_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(участник),(uintptr_t)&АДРЕС,sizeof(АДРЕС),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(поток_разъем_объект,Connect_поток);
static mp_obj_t чтение_поток(mp_obj_t участник,mp_obj_t 한도) {
    int длина_ЗНАЧЕН=mp_obj_get_int(한도); if(длина_ЗНАЧЕН<1||длина_ЗНАЧЕН>512)mp_raise_OSError(MP_EINVAL);
    unsigned char данные[512];
    intptr_t товар_СЧЁТ=결과검사(사용자호출(2,mp_obj_get_int(участник),(uintptr_t)данные,длина_ЗНАЧЕН,0,0,0));
    return mp_obj_new_bytes(данные,товар_СЧЁТ);
}
static MP_DEFINE_CONST_FUN_OBJ_2(поток_Ридер_объект,чтение_поток);
static mp_obj_t запись_поток(mp_obj_t участник,mp_obj_t контент_ЗНАЧЕН) {
    mp_buffer_info_t данные; mp_get_buffer_raise(контент_ЗНАЧЕН,&данные,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(участник),(uintptr_t)данные.buf,данные.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(поток_Редактор_блогов_объект,запись_поток);
static mp_obj_t 잠시기다리기(mp_obj_t значение_времени) {
    결과검사(사용자호출(17,mp_obj_get_int(значение_времени),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(минутку_объект,잠시기다리기);
static mp_obj_t ввод_Вид(mp_obj_t Название) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)путь_аргумент(Название),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(ввод_Вид_объект,ввод_Вид);
static mp_obj_t Create_Каталог(mp_obj_t Название) {
    결과검사(사용자호출(18,(uintptr_t)путь_аргумент(Название),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Каталог_автор_объект,Create_Каталог);
static mp_obj_t удалить_Каталог(mp_obj_t Название) {
    결과검사(사용자호출(18,(uintptr_t)путь_аргумент(Название),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,удалить_Каталог);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&поток_разъем_объект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&поток_Ридер_объект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&поток_Редактор_блогов_объект) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&минутку_объект) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&ввод_Вид_объект) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&Каталог_автор_объект) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&стандарт_входные_данные_Ридер_объект) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&файл_Ридер_объект) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&файл_Редактор_блогов_объект) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&прямоугольник_объект) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&экран_изменить_размер_объект) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&экран_минутку_объект) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Часы_объект) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_открыть_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_написать_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Close_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
