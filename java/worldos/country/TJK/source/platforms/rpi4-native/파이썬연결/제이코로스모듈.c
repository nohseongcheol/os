// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *масир_аргумент(mp_obj_t қимат) {
    size_t 개수; const char *масир = mp_obj_str_get_data(қимат, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!масир[순번]) mp_raise_OSError(MP_EINVAL);
    return масир;
}
static mp_obj_t 파일읽기(mp_obj_t Ном) {
    intptr_t файл_дастак = 결과검사(사용자호출(3, (uintptr_t)масир_аргумент(Ном), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t андоза_кардан = 결과검사(사용자호출(9, файл_дастак, 0, 0, 0, 0, 0));
        vstr_t иттилоот; vstr_init_len(&иттилоот, андоза_кардан);
        intptr_t 결과 = 사용자호출(2, файл_дастак, (uintptr_t)иттилоот.buf, андоза_кардан, 0, 0, 0);
        결과검사(결과); иттилоот.len = 결과;
        mp_obj_t қимат = mp_obj_new_bytes_from_vstr(&иттилоот);
        nlr_pop(); 사용자호출(4, файл_дастак, 0, 0, 0, 0, 0); return қимат;
    }
    사용자호출(4, файл_дастак, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(файл_Хонанда_объект, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t андоза_кардан=mp_obj_get_int(한도);
    if(андоза_кардан<0||андоза_кардан>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t иттилоот; vstr_init_len(&иттилоот,андоза_кардан);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)иттилоот.buf,андоза_кардан,0,0,0);
    if(개수<0) { vstr_clear(&иттилоот); 결과검사(개수); }
    иттилоот.len=개수; return mp_obj_new_bytes_from_vstr(&иттилоот);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t навиштан_файл(mp_obj_t Ном, mp_obj_t Мӯҳтаво_қимат) {
    const char *масир = масир_аргумент(Ном);
    mp_buffer_info_t иттилоот; mp_get_buffer_raise(Мӯҳтаво_қимат, &иттилоот, MP_BUFFER_READ);
    if (иттилоот.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t файл_дастак = 결과검사(사용자호출(3, (uintptr_t)масир, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, файл_дастак, (uintptr_t)иттилоот.buf, иттилоот.len, 0, 0, 0);
    사용자호출(4, файл_дастак, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(файл_Нависанда_объект, навиштан_файл);
static mp_obj_t тоза_кардан_файл(mp_obj_t Ном) { 결과검사(사용자호출(11, (uintptr_t)масир_аргумент(Ном), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, тоза_кардан_файл);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *аргумент_қатор) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(аргумент_қатор[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t андоза_кардан[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, андоза_кардан);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t соат_қимат(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(соат_объект, соат_қимат);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t файл_дастак = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, файл_дастак, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, файл_дастак, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(файл_дастак);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t файл_дастак, mp_obj_t 접속번호, mp_obj_t Мӯҳтаво_қимат) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t иттилоот; mp_get_buffer_raise(Мӯҳтаво_қимат, &иттилоот, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(файл_дастак), (uintptr_t)иттилоот.buf, иттилоот.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t қимат) {
    size_t дарозӣ_қимат; const char *Матн=mp_obj_str_get_data(қимат,&дарозӣ_қимат);
    unsigned 현재위치=0; uint32_t суроға=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned қимат=0,숫자수=0;
        while(현재위치<дарозӣ_қимат&&Матн[현재위치]>='0'&&Матн[현재위치]<='9') {
            қимат=қимат*10+Матн[현재위치++]-'0'; if(++숫자수>3||қимат>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        суроға=суроға<<8|қимат;
        if(부분<3&&(현재위치>=дарозӣ_қимат||Матн[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=дарозӣ_қимат)mp_raise_OSError(MP_EINVAL);
    return суроға;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *аргумент_қатор) {
    (void)항목수; uint32_t суроға=인터넷주소읽기(аргумент_қатор[1]);
    int 접속번호=mp_obj_get_int(аргумент_қатор[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t иттилоот;mp_get_buffer_raise(аргумент_қатор[3],&иттилоот,MP_BUFFER_READ);
    struct pk_sockaddr_in ҳадаф={0};ҳадаф.sin_family=AF_INET;ҳадаф.sin_port=pk_htons(접속번호);ҳадаф.sin_addr.s_addr=pk_htonl(суроға);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(аргумент_қатор[0]),(uintptr_t)иттилоот.buf,иттилоот.len,0,(uintptr_t)&ҳадаф,sizeof(ҳадаф))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t файл_дастак) {
    unsigned char иттилоот[512]; struct pk_sockaddr_in ҳамсон_қимат; pk_socklen_t дарозӣ_иттилоот = sizeof(ҳамсон_қимат);
    intptr_t андоза_кардан = 결과검사(사용자호출(35, mp_obj_get_int(файл_дастак), (uintptr_t)иттилоот, 512, 0, (uintptr_t)&ҳамсон_қимат, (uintptr_t)&дарозӣ_иттилоот));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(иттилоот, андоза_кардан), MP_OBJ_NEW_SMALL_INT(pk_htons(ҳамсон_қимат.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t файл_дастак) { 결과검사(사용자호출(4, mp_obj_get_int(файл_дастак), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t кушодан_ҷараён(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,абр_Оила,ҷараён_Шабака,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,кушодан_ҷараён);
static mp_obj_t ПАЙВАСТ_ҷараён(mp_obj_t 종단,mp_obj_t суроға_Матн,mp_obj_t индекс) {
    int 접속번호=mp_obj_get_int(индекс); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 суроға={0}; суроға.суроға_Оила=абр_Оила;
    суроға.접속번호=망차례짧은수(접속번호); суроға.суроғаи_Интернет.суроға_қимат=Шабака_адади_яклухт(인터넷주소읽기(суроға_Матн));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&суроға,sizeof(суроға),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ҷараён_васлгар_объект,ПАЙВАСТ_ҷараён);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int дарозӣ_қимат=mp_obj_get_int(한도); if(дарозӣ_қимат<1||дарозӣ_қимат>512)mp_raise_OSError(MP_EINVAL);
    unsigned char иттилоот[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)иттилоот,дарозӣ_қимат,0,0,0));
    return mp_obj_new_bytes(иттилоот,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ҷараён_Хонанда_объект,흐름읽기);
static mp_obj_t навиштан_ҷараён(mp_obj_t 종단,mp_obj_t Мӯҳтаво_қимат) {
    mp_buffer_info_t иттилоот; mp_get_buffer_raise(Мӯҳтаво_қимат,&иттилоот,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)иттилоот.buf,иттилоот.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ҷараён_Нависанда_объект,навиштан_ҷараён);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Ном) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)масир_аргумент(Ном),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t эҷод_кардан_директория(mp_obj_t Ном) {
    결과검사(사용자호출(18,(uintptr_t)масир_аргумент(Ном),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,эҷод_кардан_директория);
static mp_obj_t тоза_кардан_директория(mp_obj_t Ном) {
    결과검사(사용자호출(18,(uintptr_t)масир_аргумент(Ном),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,тоза_кардан_директория);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ҷараён_васлгар_объект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ҷараён_Хонанда_объект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&ҷараён_Нависанда_объект) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&файл_Хонанда_объект) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&файл_Нависанда_объект) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&соат_объект) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
