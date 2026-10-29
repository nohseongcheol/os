// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t мерка) { if (мерка < 0) mp_raise_OSError(-мерка); return мерка; }
static const char *патека_аргумент(mp_obj_t VALUE) {
    size_t ставка_COUNT; const char *ПАТЕКА = mp_obj_str_get_data(VALUE, &ставка_COUNT);
    if (!ставка_COUNT || ставка_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < ставка_COUNT; 순번++) if (!ПАТЕКА[순번]) mp_raise_OSError(MP_EINVAL);
    return ПАТЕКА;
}
static mp_obj_t 파일읽기(mp_obj_t Име) {
    intptr_t датотека_рачка = 결과검사(사용자호출(3, (uintptr_t)патека_аргумент(Име), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Големина = 결과검사(사용자호출(9, датотека_рачка, 0, 0, 0, 0, 0));
        vstr_t податоци; vstr_init_len(&податоци, Големина);
        intptr_t мерка = 사용자호출(2, датотека_рачка, (uintptr_t)податоци.buf, Големина, 0, 0, 0);
        결과검사(мерка); податоци.len = мерка;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&податоци);
        nlr_pop(); 사용자호출(4, датотека_рачка, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, датотека_рачка, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(датотека_Читач_објект, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Големина=mp_obj_get_int(한도);
    if(Големина<0||Големина>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t податоци; vstr_init_len(&податоци,Големина);
    intptr_t ставка_COUNT=사용자호출(2,0,(uintptr_t)податоци.buf,Големина,0,0,0);
    if(ставка_COUNT<0) { vstr_clear(&податоци); 결과검사(ставка_COUNT); }
    податоци.len=ставка_COUNT; return mp_obj_new_bytes_from_vstr(&податоци);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t запиши_датотека(mp_obj_t Име, mp_obj_t Содржина_VALUE) {
    const char *ПАТЕКА = патека_аргумент(Име);
    mp_buffer_info_t податоци; mp_get_buffer_raise(Содржина_VALUE, &податоци, MP_BUFFER_READ);
    if (податоци.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t датотека_рачка = 결과검사(사용자호출(3, (uintptr_t)ПАТЕКА, 577, 0, 0, 0, 0));
    intptr_t внес_COUNT = 사용자호출(1, датотека_рачка, (uintptr_t)податоци.buf, податоци.len, 0, 0, 0);
    사용자호출(4, датотека_рачка, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(внес_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(датотека_Писател_објект, запиши_датотека);
static mp_obj_t отстрани_датотека(mp_obj_t Име) { 결과검사(사용자호출(11, (uintptr_t)патека_аргумент(Име), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, отстрани_датотека);
static mp_obj_t 사각형그리기(size_t ставка_COUNT, const mp_obj_t *аргумент_низа) {
    (void)ставка_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(аргумент_низа[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Големина[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Големина);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Часовник_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Часовник_објект, Часовник_VALUE);
static mp_obj_t УДП_отвори(mp_obj_t број_на_порта) {
    int податоци_позиционирање = mp_obj_get_int(број_на_порта); if (податоци_позиционирање < 0 || податоци_позиционирање > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t датотека_рачка = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(податоци_позиционирање); 첫째값.sin_addr.s_addr = 0;
    intptr_t мерка = 사용자호출(33, датотека_рачка, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (мерка < 0) { 사용자호출(4, датотека_рачка, 0, 0, 0, 0, 0); 결과검사(мерка); }
    return mp_obj_new_int(датотека_рачка);
}
static MP_DEFINE_CONST_FUN_OBJ_1(УДП_отвори_OBJ, УДП_отвори);
static mp_obj_t УДП_испрати(mp_obj_t датотека_рачка, mp_obj_t број_на_порта, mp_obj_t Содржина_VALUE) {
    int податоци_позиционирање = mp_obj_get_int(број_на_порта); if (податоци_позиционирање < 1 || податоци_позиционирање > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t податоци; mp_get_buffer_raise(Содржина_VALUE, &податоци, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(податоци_позиционирање); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(датотека_рачка), (uintptr_t)податоци.buf, податоци.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(УДП_испрати_OBJ, УДП_испрати);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t должина_VALUE; const char *Текст=mp_obj_str_get_data(VALUE,&должина_VALUE);
    unsigned 현재위치=0; uint32_t адреса=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,цифра_COUNT=0;
        while(현재위치<должина_VALUE&&Текст[현재위치]>='0'&&Текст[현재위치]<='9') {
            VALUE=VALUE*10+Текст[현재위치++]-'0'; if(++цифра_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!цифра_COUNT)mp_raise_OSError(MP_EINVAL);
        адреса=адреса<<8|VALUE;
        if(부분<3&&(현재위치>=должина_VALUE||Текст[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=должина_VALUE)mp_raise_OSError(MP_EINVAL);
    return адреса;
}
static mp_obj_t 전문주소전송(size_t внес_COUNT, const mp_obj_t *аргумент_низа) {
    (void)внес_COUNT; uint32_t адреса=인터넷주소읽기(аргумент_низа[1]);
    int број_на_порта=mp_obj_get_int(аргумент_низа[2]);if(број_на_порта<1||број_на_порта>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t податоци;mp_get_buffer_raise(аргумент_низа[3],&податоци,MP_BUFFER_READ);
    struct pk_sockaddr_in цел={0};цел.sin_family=AF_INET;цел.sin_port=pk_htons(број_на_порта);цел.sin_addr.s_addr=pk_htonl(адреса);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(аргумент_низа[0]),(uintptr_t)податоци.buf,податоци.len,0,(uintptr_t)&цел,sizeof(цел))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t датотека_рачка) {
    unsigned char податоци[512]; struct pk_sockaddr_in рамноправен_уред_VALUE; pk_socklen_t должина_податоци = sizeof(рамноправен_уред_VALUE);
    intptr_t Големина = 결과검사(사용자호출(35, mp_obj_get_int(датотека_рачка), (uintptr_t)податоци, 512, 0, (uintptr_t)&рамноправен_уред_VALUE, (uintptr_t)&должина_податоци));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(податоци, Големина), MP_OBJ_NEW_SMALL_INT(pk_htons(рамноправен_уред_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t УДП_затвори(mp_obj_t датотека_рачка) { 결과검사(사용자호출(4, mp_obj_get_int(датотека_рачка), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(УДП_затвори_OBJ, УДП_затвори);
static mp_obj_t отвори_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,облак_семејни,Stream_Мрежа,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,отвори_Stream);
static mp_obj_t ПОВРЗИ_Stream(mp_obj_t 종단,mp_obj_t адреса_СМС,mp_obj_t INDEX) {
    int број_на_порта=mp_obj_get_int(INDEX); if(број_на_порта<1||број_на_порта>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 адреса={0}; адреса.адреса_семејни=облак_семејни;
    адреса.број_на_порта=망차례짧은수(број_на_порта); адреса.Интернет_адреса.адреса_VALUE=Мрежа_цел_број(인터넷주소읽기(адреса_СМС));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&адреса,sizeof(адреса),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_приклучок_објект,ПОВРЗИ_Stream);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int должина_VALUE=mp_obj_get_int(한도); if(должина_VALUE<1||должина_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char податоци[512];
    intptr_t ставка_COUNT=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)податоци,должина_VALUE,0,0,0));
    return mp_obj_new_bytes(податоци,ставка_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Читач_објект,흐름읽기);
static mp_obj_t запиши_Stream(mp_obj_t 종단,mp_obj_t Содржина_VALUE) {
    mp_buffer_info_t податоци; mp_get_buffer_raise(Содржина_VALUE,&податоци,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)податоци.buf,податоци.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Писател_објект,запиши_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(почекај_објект,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Име) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)патека_аргумент(Име),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Create_Именик(mp_obj_t Име) {
    결과검사(사용자호출(18,(uintptr_t)патека_аргумент(Име),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Именик_создавач_објект,Create_Именик);
static mp_obj_t отстрани_Именик(mp_obj_t Име) {
    결과검사(사용자호출(18,(uintptr_t)патека_аргумент(Име),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,отстрани_Именик);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_приклучок_објект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_Читач_објект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Писател_објект) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&почекај_објект) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&Именик_создавач_објект) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&датотека_Читач_објект) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&датотека_Писател_објект) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Часовник_објект) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&УДП_отвори_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&УДП_испрати_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&УДП_затвори_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
