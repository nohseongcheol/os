// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t үлчәм) { if (үлчәм < 0) mp_raise_OSError(-үлчәм); return үлчәм; }
static const char *юл_аргумент(mp_obj_t VALUE) {
    size_t элемент_COUNT; const char *Yul = mp_obj_str_get_data(VALUE, &элемент_COUNT);
    if (!элемент_COUNT || элемент_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < элемент_COUNT; 순번++) if (!Yul[순번]) mp_raise_OSError(MP_EINVAL);
    return Yul;
}
static mp_obj_t 파일읽기(mp_obj_t исем) {
    intptr_t файл_дескриптор = 결과검사(사용자호출(3, (uintptr_t)юл_аргумент(исем), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t үлчәмен_үзгәртү = 결과검사(사용자호출(9, файл_дескриптор, 0, 0, 0, 0, 0));
        vstr_t мәгълүмат; vstr_init_len(&мәгълүмат, үлчәмен_үзгәртү);
        intptr_t үлчәм = 사용자호출(2, файл_дескриптор, (uintptr_t)мәгълүмат.buf, үлчәмен_үзгәртү, 0, 0, 0);
        결과검사(үлчәм); мәгълүмат.len = үлчәм;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&мәгълүмат);
        nlr_pop(); 사용자호출(4, файл_дескриптор, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, файл_дескриптор, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(файл_укучы_объект, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t үлчәмен_үзгәртү=mp_obj_get_int(한도);
    if(үлчәмен_үзгәртү<0||үлчәмен_үзгәртү>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t мәгълүмат; vstr_init_len(&мәгълүмат,үлчәмен_үзгәртү);
    intptr_t элемент_COUNT=사용자호출(2,0,(uintptr_t)мәгълүмат.buf,үлчәмен_үзгәртү,0,0,0);
    if(элемент_COUNT<0) { vstr_clear(&мәгълүмат); 결과검사(элемент_COUNT); }
    мәгълүмат.len=элемент_COUNT; return mp_obj_new_bytes_from_vstr(&мәгълүмат);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t язу_файл(mp_obj_t исем, mp_obj_t Эчтәлек_VALUE) {
    const char *Yul = юл_аргумент(исем);
    mp_buffer_info_t мәгълүмат; mp_get_buffer_raise(Эчтәлек_VALUE, &мәгълүмат, MP_BUFFER_READ);
    if (мәгълүмат.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t файл_дескриптор = 결과검사(사용자호출(3, (uintptr_t)Yul, 577, 0, 0, 0, 0));
    intptr_t кертү_COUNT = 사용자호출(1, файл_дескриптор, (uintptr_t)мәгълүмат.buf, мәгълүмат.len, 0, 0, 0);
    사용자호출(4, файл_дескриптор, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(кертү_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(файл_Блог_редакторы_объект, язу_файл);
static mp_obj_t бетерү_файл(mp_obj_t исем) { 결과검사(사용자호출(11, (uintptr_t)юл_аргумент(исем), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, бетерү_файл);
static mp_obj_t 사각형그리기(size_t элемент_COUNT, const mp_obj_t *аргумент_МАССИВ) {
    (void)элемент_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(аргумент_МАССИВ[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t үлчәмен_үзгәртү[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, үлчәмен_үзгәртү);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Сәгать_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Сәгать_объект, Сәгать_VALUE);
static mp_obj_t UDP_ачу(mp_obj_t 접속번호) {
    int мәгълүмат_урнаштыру = mp_obj_get_int(접속번호); if (мәгълүмат_урнаштыру < 0 || мәгълүмат_урнаштыру > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t файл_дескриптор = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(мәгълүмат_урнаштыру); 첫째값.sin_addr.s_addr = 0;
    intptr_t үлчәм = 사용자호출(33, файл_дескриптор, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (үлчәм < 0) { 사용자호출(4, файл_дескриптор, 0, 0, 0, 0, 0); 결과검사(үлчәм); }
    return mp_obj_new_int(файл_дескриптор);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, UDP_ачу);
static mp_obj_t UDP_җибәрү(mp_obj_t файл_дескриптор, mp_obj_t 접속번호, mp_obj_t Эчтәлек_VALUE) {
    int мәгълүмат_урнаштыру = mp_obj_get_int(접속번호); if (мәгълүмат_урнаштыру < 1 || мәгълүмат_урнаштыру > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t мәгълүмат; mp_get_buffer_raise(Эчтәлек_VALUE, &мәгълүмат, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(мәгълүмат_урнаштыру); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(файл_дескриптор), (uintptr_t)мәгълүмат.buf, мәгълүмат.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, UDP_җибәрү);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t озынлык_VALUE; const char *Mäten=mp_obj_str_get_data(VALUE,&озынлык_VALUE);
    unsigned 현재위치=0; uint32_t адрес=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,сан_COUNT=0;
        while(현재위치<озынлык_VALUE&&Mäten[현재위치]>='0'&&Mäten[현재위치]<='9') {
            VALUE=VALUE*10+Mäten[현재위치++]-'0'; if(++сан_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!сан_COUNT)mp_raise_OSError(MP_EINVAL);
        адрес=адрес<<8|VALUE;
        if(부분<3&&(현재위치>=озынлык_VALUE||Mäten[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=озынлык_VALUE)mp_raise_OSError(MP_EINVAL);
    return адрес;
}
static mp_obj_t 전문주소전송(size_t кертү_COUNT, const mp_obj_t *аргумент_МАССИВ) {
    (void)кертү_COUNT; uint32_t адрес=인터넷주소읽기(аргумент_МАССИВ[1]);
    int 접속번호=mp_obj_get_int(аргумент_МАССИВ[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t мәгълүмат;mp_get_buffer_raise(аргумент_МАССИВ[3],&мәгълүмат,MP_BUFFER_READ);
    struct pk_sockaddr_in максат_кыйммәт={0};максат_кыйммәт.sin_family=AF_INET;максат_кыйммәт.sin_port=pk_htons(접속번호);максат_кыйммәт.sin_addr.s_addr=pk_htonl(адрес);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(аргумент_МАССИВ[0]),(uintptr_t)мәгълүмат.buf,мәгълүмат.len,0,(uintptr_t)&максат_кыйммәт,sizeof(максат_кыйммәт))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t файл_дескриптор) {
    unsigned char мәгълүмат[512]; struct pk_sockaddr_in тиңдәш_VALUE; pk_socklen_t озынлык_мәгълүмат = sizeof(тиңдәш_VALUE);
    intptr_t үлчәмен_үзгәртү = 결과검사(사용자호출(35, mp_obj_get_int(файл_дескриптор), (uintptr_t)мәгълүмат, 512, 0, (uintptr_t)&тиңдәш_VALUE, (uintptr_t)&озынлык_мәгълүмат));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(мәгълүмат, үлчәмен_үзгәртү), MP_OBJ_NEW_SMALL_INT(pk_htons(тиңдәш_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_чик(mp_obj_t файл_дескриптор) { 결과검사(사용자호출(4, mp_obj_get_int(файл_дескриптор), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, UDP_чик);
static mp_obj_t ачу_агым(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,болыт_Гаилә,агым_Челтәр,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,ачу_агым);
static mp_obj_t ялгау_агым(mp_obj_t 종단,mp_obj_t адрес_СМС,mp_obj_t INDEX) {
    int 접속번호=mp_obj_get_int(INDEX); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 адрес={0}; адрес.адрес_Гаилә=болыт_Гаилә;
    адрес.접속번호=망차례짧은수(접속번호); адрес.Интернеттагы_адрес.адрес_VALUE=Челтәр_бөтен_сан(인터넷주소읽기(адрес_СМС));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&адрес,sizeof(адрес),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(агым_бәйләүче_объект,ялгау_агым);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int озынлык_VALUE=mp_obj_get_int(한도); if(озынлык_VALUE<1||озынлык_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char мәгълүмат[512];
    intptr_t элемент_COUNT=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)мәгълүмат,озынлык_VALUE,0,0,0));
    return mp_obj_new_bytes(мәгълүмат,элемент_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(агым_укучы_объект,흐름읽기);
static mp_obj_t язу_агым(mp_obj_t 종단,mp_obj_t Эчтәлек_VALUE) {
    mp_buffer_info_t мәгълүмат; mp_get_buffer_raise(Эчтәлек_VALUE,&мәгълүмат,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)мәгълүмат.buf,мәгълүмат.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(агым_Блог_редакторы_объект,язу_агым);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t исем) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)юл_аргумент(исем),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Төзү_каталог(mp_obj_t исем) {
    결과검사(사용자호출(18,(uintptr_t)юл_аргумент(исем),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,Төзү_каталог);
static mp_obj_t бетерү_каталог(mp_obj_t исем) {
    결과검사(사용자호출(18,(uintptr_t)юл_аргумент(исем),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,бетерү_каталог);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&агым_бәйләүче_объект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&агым_укучы_объект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&агым_Блог_редакторы_объект) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&файл_укучы_объект) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&файл_Блог_редакторы_объект) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Сәгать_объект) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
