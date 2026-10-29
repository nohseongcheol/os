// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *жол_аргумент(mp_obj_t маани) {
    size_t 개수; const char *ЖОЛ = mp_obj_str_get_data(маани, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!ЖОЛ[순번]) mp_raise_OSError(MP_EINVAL);
    return ЖОЛ;
}
static mp_obj_t 파일읽기(mp_obj_t Аты) {
    intptr_t файл_тутка = 결과검사(사용자호출(3, (uintptr_t)жол_аргумент(Аты), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Өлчөмү = 결과검사(사용자호출(9, файл_тутка, 0, 0, 0, 0, 0));
        vstr_t берилмелер; vstr_init_len(&берилмелер, Өлчөмү);
        intptr_t 결과 = 사용자호출(2, файл_тутка, (uintptr_t)берилмелер.buf, Өлчөмү, 0, 0, 0);
        결과검사(결과); берилмелер.len = 결과;
        mp_obj_t маани = mp_obj_new_bytes_from_vstr(&берилмелер);
        nlr_pop(); 사용자호출(4, файл_тутка, 0, 0, 0, 0, 0); return маани;
    }
    사용자호출(4, файл_тутка, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(файл_окуучу_объект, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Өлчөмү=mp_obj_get_int(한도);
    if(Өлчөмү<0||Өлчөмү>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t берилмелер; vstr_init_len(&берилмелер,Өлчөмү);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)берилмелер.buf,Өлчөмү,0,0,0);
    if(개수<0) { vstr_clear(&берилмелер); 결과검사(개수); }
    берилмелер.len=개수; return mp_obj_new_bytes_from_vstr(&берилмелер);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t жазуу_файл(mp_obj_t Аты, mp_obj_t Мазмун_маани) {
    const char *ЖОЛ = жол_аргумент(Аты);
    mp_buffer_info_t берилмелер; mp_get_buffer_raise(Мазмун_маани, &берилмелер, MP_BUFFER_READ);
    if (берилмелер.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t файл_тутка = 결과검사(사용자호출(3, (uintptr_t)ЖОЛ, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, файл_тутка, (uintptr_t)берилмелер.buf, берилмелер.len, 0, 0, 0);
    사용자호출(4, файл_тутка, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(файл_Редактор_объект, жазуу_файл);
static mp_obj_t алып_салуу_файл(mp_obj_t Аты) { 결과검사(사용자호출(11, (uintptr_t)жол_аргумент(Аты), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, алып_салуу_файл);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *аргумент_МАССИВ) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(аргумент_МАССИВ[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Өлчөмү[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Өлчөмү);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t саат_маани(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(саат_объект, саат_маани);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t файл_тутка = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, файл_тутка, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, файл_тутка, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(файл_тутка);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t файл_тутка, mp_obj_t 접속번호, mp_obj_t Мазмун_маани) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t берилмелер; mp_get_buffer_raise(Мазмун_маани, &берилмелер, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(файл_тутка), (uintptr_t)берилмелер.buf, берилмелер.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t маани) {
    size_t узундук_маани; const char *Текст=mp_obj_str_get_data(маани,&узундук_маани);
    unsigned 현재위치=0; uint32_t дарек=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned маани=0,숫자수=0;
        while(현재위치<узундук_маани&&Текст[현재위치]>='0'&&Текст[현재위치]<='9') {
            маани=маани*10+Текст[현재위치++]-'0'; if(++숫자수>3||маани>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        дарек=дарек<<8|маани;
        if(부분<3&&(현재위치>=узундук_маани||Текст[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=узундук_маани)mp_raise_OSError(MP_EINVAL);
    return дарек;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *аргумент_МАССИВ) {
    (void)항목수; uint32_t дарек=인터넷주소읽기(аргумент_МАССИВ[1]);
    int 접속번호=mp_obj_get_int(аргумент_МАССИВ[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t берилмелер;mp_get_buffer_raise(аргумент_МАССИВ[3],&берилмелер,MP_BUFFER_READ);
    struct pk_sockaddr_in максат={0};максат.sin_family=AF_INET;максат.sin_port=pk_htons(접속번호);максат.sin_addr.s_addr=pk_htonl(дарек);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(аргумент_МАССИВ[0]),(uintptr_t)берилмелер.buf,берилмелер.len,0,(uintptr_t)&максат,sizeof(максат))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t файл_тутка) {
    unsigned char берилмелер[512]; struct pk_sockaddr_in бирдей_маани; pk_socklen_t узундук_берилмелер = sizeof(бирдей_маани);
    intptr_t Өлчөмү = 결과검사(사용자호출(35, mp_obj_get_int(файл_тутка), (uintptr_t)берилмелер, 512, 0, (uintptr_t)&бирдей_маани, (uintptr_t)&узундук_берилмелер));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(берилмелер, Өлчөмү), MP_OBJ_NEW_SMALL_INT(pk_htons(бирдей_маани.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t файл_тутка) { 결과검사(사용자호출(4, mp_obj_get_int(файл_тутка), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t ачуу_агым(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,Интернет_Үй_бүлө,агым_Желе,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,ачуу_агым);
static mp_obj_t ТУТАШУУ_агым(mp_obj_t 종단,mp_obj_t дарек_СМС,mp_obj_t индекс) {
    int 접속번호=mp_obj_get_int(индекс); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 дарек={0}; дарек.дарек_Үй_бүлө=Интернет_Үй_бүлө;
    дарек.접속번호=망차례짧은수(접속번호); дарек.Интернет_дарек.дарек_маани=Желе_бүтүн_сан(인터넷주소읽기(дарек_СМС));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&дарек,sizeof(дарек),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(агым_туташтыргыч_объект,ТУТАШУУ_агым);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int узундук_маани=mp_obj_get_int(한도); if(узундук_маани<1||узундук_маани>512)mp_raise_OSError(MP_EINVAL);
    unsigned char берилмелер[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)берилмелер,узундук_маани,0,0,0));
    return mp_obj_new_bytes(берилмелер,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(агым_окуучу_объект,흐름읽기);
static mp_obj_t жазуу_агым(mp_obj_t 종단,mp_obj_t Мазмун_маани) {
    mp_buffer_info_t берилмелер; mp_get_buffer_raise(Мазмун_маани,&берилмелер,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)берилмелер.buf,берилмелер.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(агым_Редактор_объект,жазуу_агым);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Аты) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)жол_аргумент(Аты),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t түзүү_каталог(mp_obj_t Аты) {
    결과검사(사용자호출(18,(uintptr_t)жол_аргумент(Аты),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,түзүү_каталог);
static mp_obj_t алып_салуу_каталог(mp_obj_t Аты) {
    결과검사(사용자호출(18,(uintptr_t)жол_аргумент(Аты),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,алып_салуу_каталог);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&агым_туташтыргыч_объект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&агым_окуучу_объект) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&агым_Редактор_объект) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&файл_окуучу_объект) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&файл_Редактор_объект) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&саат_объект) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
