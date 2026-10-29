// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t НӘТИЖЕ) { if (НӘТИЖЕ < 0) mp_raise_OSError(-НӘТИЖЕ); return НӘТИЖЕ; }
static const char *жол_аргумент(mp_obj_t мән) {
    size_t 개수; const char *Жол_2 = mp_obj_str_get_data(мән, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!Жол_2[순번]) mp_raise_OSError(MP_EINVAL);
    return Жол_2;
}
static mp_obj_t 파일읽기(mp_obj_t Аты) {
    intptr_t файл_дескриптор = 결과검사(사용자호출(3, (uintptr_t)жол_аргумент(Аты), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Өлшемі = 결과검사(사용자호출(9, файл_дескриптор, 0, 0, 0, 0, 0));
        vstr_t деректер; vstr_init_len(&деректер, Өлшемі);
        intptr_t НӘТИЖЕ = 사용자호출(2, файл_дескриптор, (uintptr_t)деректер.buf, Өлшемі, 0, 0, 0);
        결과검사(НӘТИЖЕ); деректер.len = НӘТИЖЕ;
        mp_obj_t мән = mp_obj_new_bytes_from_vstr(&деректер);
        nlr_pop(); 사용자호출(4, файл_дескриптор, 0, 0, 0, 0, 0); return мән;
    }
    사용자호출(4, файл_дескриптор, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(файл_оқушы_нысан, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Өлшемі=mp_obj_get_int(한도);
    if(Өлшемі<0||Өлшемі>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t деректер; vstr_init_len(&деректер,Өлшемі);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)деректер.buf,Өлшемі,0,0,0);
    if(개수<0) { vstr_clear(&деректер); 결과검사(개수); }
    деректер.len=개수; return mp_obj_new_bytes_from_vstr(&деректер);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t жазу_файл(mp_obj_t Аты, mp_obj_t мазмұн_мән) {
    const char *Жол_2 = жол_аргумент(Аты);
    mp_buffer_info_t деректер; mp_get_buffer_raise(мазмұн_мән, &деректер, MP_BUFFER_READ);
    if (деректер.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t файл_дескриптор = 결과검사(사용자호출(3, (uintptr_t)Жол_2, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, файл_дескриптор, (uintptr_t)деректер.buf, деректер.len, 0, 0, 0);
    사용자호출(4, файл_дескриптор, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(файл_Жазу_бағдарламасы_нысан, жазу_файл);
static mp_obj_t жою_файл(mp_obj_t Аты) { 결과검사(사용자호출(11, (uintptr_t)жол_аргумент(Аты), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, жою_файл);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *аргумент_массив) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(аргумент_массив[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(тік_төртбұрыш_нысан, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Өлшемі[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Өлшемі);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Сағат_мән(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Сағат_нысан, Сағат_мән);
static mp_obj_t пайдаланушы_датаграммасының_протоколы_ашу(mp_obj_t порт_нөмірі) {
    int деректер_лауазым = mp_obj_get_int(порт_нөмірі); if (деректер_лауазым < 0 || деректер_лауазым > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t файл_дескриптор = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(деректер_лауазым); 첫째값.sin_addr.s_addr = 0;
    intptr_t НӘТИЖЕ = 사용자호출(33, файл_дескриптор, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (НӘТИЖЕ < 0) { 사용자호출(4, файл_дескриптор, 0, 0, 0, 0, 0); 결과검사(НӘТИЖЕ); }
    return mp_obj_new_int(файл_дескриптор);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, пайдаланушы_датаграммасының_протоколы_ашу);
static mp_obj_t пайдаланушы_датаграммасының_протоколы_жіберу(mp_obj_t файл_дескриптор, mp_obj_t порт_нөмірі, mp_obj_t мазмұн_мән) {
    int деректер_лауазым = mp_obj_get_int(порт_нөмірі); if (деректер_лауазым < 1 || деректер_лауазым > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t деректер; mp_get_buffer_raise(мазмұн_мән, &деректер, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(деректер_лауазым); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(файл_дескриптор), (uintptr_t)деректер.buf, деректер.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, пайдаланушы_датаграммасының_протоколы_жіберу);
static uint32_t 인터넷주소읽기(mp_obj_t мән) {
    size_t ұзындық_мән; const char *Мәтін=mp_obj_str_get_data(мән,&ұзындық_мән);
    unsigned ток_лауазым=0; uint32_t мекенжай=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned мән=0,숫자수=0;
        while(ток_лауазым<ұзындық_мән&&Мәтін[ток_лауазым]>='0'&&Мәтін[ток_лауазым]<='9') {
            мән=мән*10+Мәтін[ток_лауазым++]-'0'; if(++숫자수>3||мән>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        мекенжай=мекенжай<<8|мән;
        if(부분<3&&(ток_лауазым>=ұзындық_мән||Мәтін[ток_лауазым++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(ток_лауазым!=ұзындық_мән)mp_raise_OSError(MP_EINVAL);
    return мекенжай;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *аргумент_массив) {
    (void)항목수; uint32_t мекенжай=인터넷주소읽기(аргумент_массив[1]);
    int порт_нөмірі=mp_obj_get_int(аргумент_массив[2]);if(порт_нөмірі<1||порт_нөмірі>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t деректер;mp_get_buffer_raise(аргумент_массив[3],&деректер,MP_BUFFER_READ);
    struct pk_sockaddr_in мақсатты_мән={0};мақсатты_мән.sin_family=AF_INET;мақсатты_мән.sin_port=pk_htons(порт_нөмірі);мақсатты_мән.sin_addr.s_addr=pk_htonl(мекенжай);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(аргумент_массив[0]),(uintptr_t)деректер.buf,деректер.len,0,(uintptr_t)&мақсатты_мән,sizeof(мақсатты_мән))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t файл_дескриптор) {
    unsigned char деректер[512]; struct pk_sockaddr_in бір_рангілі_мән; pk_socklen_t ұзындық_деректер = sizeof(бір_рангілі_мән);
    intptr_t Өлшемі = 결과검사(사용자호출(35, mp_obj_get_int(файл_дескриптор), (uintptr_t)деректер, 512, 0, (uintptr_t)&бір_рангілі_мән, (uintptr_t)&ұзындық_деректер));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(деректер, Өлшемі), MP_OBJ_NEW_SMALL_INT(pk_htons(бір_рангілі_мән.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t пайдаланушы_датаграммасының_протоколы_Жабу(mp_obj_t файл_дескриптор) { 결과검사(사용자호출(4, mp_obj_get_int(файл_дескриптор), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, пайдаланушы_датаграммасының_протоколы_Жабу);
static mp_obj_t ашу_ағым(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,бұлт_топ,ағым_желі,ағым_транспорт_протоколы,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,ашу_ағым);
static mp_obj_t қосу_ағым(mp_obj_t қатысушы,mp_obj_t мекенжай_Мәтін,mp_obj_t индекс) {
    int порт_нөмірі=mp_obj_get_int(индекс); if(порт_нөмірі<1||порт_нөмірі>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 мекенжай={0}; мекенжай.мекенжай_топ=бұлт_топ;
    мекенжай.порт_нөмірі=망차례짧은수(порт_нөмірі); мекенжай.Интернет_мекенжайы.мекенжай_мән=желі_бүтін_сан(인터넷주소읽기(мекенжай_Мәтін));
    결과검사(사용자호출(37,mp_obj_get_int(қатысушы),(uintptr_t)&мекенжай,sizeof(мекенжай),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ағым_Қосқыш_нысан,қосу_ағым);
static mp_obj_t 흐름읽기(mp_obj_t қатысушы,mp_obj_t 한도) {
    int ұзындық_мән=mp_obj_get_int(한도); if(ұзындық_мән<1||ұзындық_мән>512)mp_raise_OSError(MP_EINVAL);
    unsigned char деректер[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(қатысушы),(uintptr_t)деректер,ұзындық_мән,0,0,0));
    return mp_obj_new_bytes(деректер,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ағым_оқушы_нысан,흐름읽기);
static mp_obj_t жазу_ағым(mp_obj_t қатысушы,mp_obj_t мазмұн_мән) {
    mp_buffer_info_t деректер; mp_get_buffer_raise(мазмұн_мән,&деректер,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(қатысушы),(uintptr_t)деректер.buf,деректер.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ағым_Жазу_бағдарламасы_нысан,жазу_ағым);
static mp_obj_t 잠시기다리기(mp_obj_t уақыт_мән) {
    결과검사(사용자호출(17,mp_obj_get_int(уақыт_мән),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(күте_тұрыңыз_нысан,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Аты) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)жол_аргумент(Аты),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t жасау_каталог(mp_obj_t Аты) {
    결과검사(사용자호출(18,(uintptr_t)жол_аргумент(Аты),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,жасау_каталог);
static mp_obj_t жою_каталог(mp_obj_t Аты) {
    결과검사(사용자호출(18,(uintptr_t)жол_аргумент(Аты),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,жою_каталог);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ағым_Қосқыш_нысан) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ағым_оқушы_нысан) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&ағым_Жазу_бағдарламасы_нысан) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&күте_тұрыңыз_нысан) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&файл_оқушы_нысан) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&файл_Жазу_бағдарламасы_нысан) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&тік_төртбұрыш_нысан) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Сағат_нысан) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
