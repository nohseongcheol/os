// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *inzira_ingingo(mp_obj_t agaciro) {
    size_t 개수; const char *Inzira = mp_obj_str_get_data(agaciro, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!Inzira[순번]) mp_raise_OSError(MP_EINVAL);
    return Inzira;
}
static mp_obj_t 파일읽기(mp_obj_t Izina) {
    intptr_t dosiye_umukondo = 결과검사(사용자호출(3, (uintptr_t)inzira_ingingo(Izina), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Ingano = 결과검사(사용자호출(9, dosiye_umukondo, 0, 0, 0, 0, 0));
        vstr_t amakurushingiro; vstr_init_len(&amakurushingiro, Ingano);
        intptr_t 결과 = 사용자호출(2, dosiye_umukondo, (uintptr_t)amakurushingiro.buf, Ingano, 0, 0, 0);
        결과검사(결과); amakurushingiro.len = 결과;
        mp_obj_t agaciro = mp_obj_new_bytes_from_vstr(&amakurushingiro);
        nlr_pop(); 사용자호출(4, dosiye_umukondo, 0, 0, 0, 0, 0); return agaciro;
    }
    사용자호출(4, dosiye_umukondo, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(dosiye_Musomyi_ikintu, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Ingano=mp_obj_get_int(한도);
    if(Ingano<0||Ingano>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t amakurushingiro; vstr_init_len(&amakurushingiro,Ingano);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)amakurushingiro.buf,Ingano,0,0,0);
    if(개수<0) { vstr_clear(&amakurushingiro); 결과검사(개수); }
    amakurushingiro.len=개수; return mp_obj_new_bytes_from_vstr(&amakurushingiro);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t kwandika_dosiye(mp_obj_t Izina, mp_obj_t Ibirimo_agaciro) {
    const char *Inzira = inzira_ingingo(Izina);
    mp_buffer_info_t amakurushingiro; mp_get_buffer_raise(Ibirimo_agaciro, &amakurushingiro, MP_BUFFER_READ);
    if (amakurushingiro.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t dosiye_umukondo = 결과검사(사용자호출(3, (uintptr_t)Inzira, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, dosiye_umukondo, (uintptr_t)amakurushingiro.buf, amakurushingiro.len, 0, 0, 0);
    사용자호출(4, dosiye_umukondo, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(dosiye_Writer_ikintu, kwandika_dosiye);
static mp_obj_t gukuramo_dosiye(mp_obj_t Izina) { 결과검사(사용자호출(11, (uintptr_t)inzira_ingingo(Izina), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, gukuramo_dosiye);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *ingingo_ARRAY) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(ingingo_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Ingano[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Ingano);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t isaha_agaciro(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(isaha_ikintu, isaha_agaciro);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t dosiye_umukondo = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, dosiye_umukondo, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, dosiye_umukondo, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(dosiye_umukondo);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t dosiye_umukondo, mp_obj_t 접속번호, mp_obj_t Ibirimo_agaciro) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t amakurushingiro; mp_get_buffer_raise(Ibirimo_agaciro, &amakurushingiro, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(dosiye_umukondo), (uintptr_t)amakurushingiro.buf, amakurushingiro.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t agaciro) {
    size_t uburebure_agaciro; const char *Umwandiko=mp_obj_str_get_data(agaciro,&uburebure_agaciro);
    unsigned 현재위치=0; uint32_t aderesi=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned agaciro=0,숫자수=0;
        while(현재위치<uburebure_agaciro&&Umwandiko[현재위치]>='0'&&Umwandiko[현재위치]<='9') {
            agaciro=agaciro*10+Umwandiko[현재위치++]-'0'; if(++숫자수>3||agaciro>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        aderesi=aderesi<<8|agaciro;
        if(부분<3&&(현재위치>=uburebure_agaciro||Umwandiko[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=uburebure_agaciro)mp_raise_OSError(MP_EINVAL);
    return aderesi;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *ingingo_ARRAY) {
    (void)항목수; uint32_t aderesi=인터넷주소읽기(ingingo_ARRAY[1]);
    int 접속번호=mp_obj_get_int(ingingo_ARRAY[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t amakurushingiro;mp_get_buffer_raise(ingingo_ARRAY[3],&amakurushingiro,MP_BUFFER_READ);
    struct pk_sockaddr_in gusimbuza_igishya={0};gusimbuza_igishya.sin_family=AF_INET;gusimbuza_igishya.sin_port=pk_htons(접속번호);gusimbuza_igishya.sin_addr.s_addr=pk_htonl(aderesi);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(ingingo_ARRAY[0]),(uintptr_t)amakurushingiro.buf,amakurushingiro.len,0,(uintptr_t)&gusimbuza_igishya,sizeof(gusimbuza_igishya))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t dosiye_umukondo) {
    unsigned char amakurushingiro[512]; struct pk_sockaddr_in Mugenzi_agaciro; pk_socklen_t uburebure_amakurushingiro = sizeof(Mugenzi_agaciro);
    intptr_t Ingano = 결과검사(사용자호출(35, mp_obj_get_int(dosiye_umukondo), (uintptr_t)amakurushingiro, 512, 0, (uintptr_t)&Mugenzi_agaciro, (uintptr_t)&uburebure_amakurushingiro));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(amakurushingiro, Ingano), MP_OBJ_NEW_SMALL_INT(pk_htons(Mugenzi_agaciro.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t dosiye_umukondo) { 결과검사(사용자호출(4, mp_obj_get_int(dosiye_umukondo), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t kurema_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,karawudi_Umuryango,Stream_Urusobemiyoboro,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,kurema_Stream);
static mp_obj_t Guhuza_Stream(mp_obj_t 종단,mp_obj_t aderesi_SMS,mp_obj_t umugerekashakiro) {
    int 접속번호=mp_obj_get_int(umugerekashakiro); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 aderesi={0}; aderesi.aderesi_Umuryango=karawudi_Umuryango;
    aderesi.접속번호=망차례짧은수(접속번호); aderesi.Aderesi_ya_Interineti.aderesi_agaciro=Urusobemiyoboro_umubare_wuzuye(인터넷주소읽기(aderesi_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&aderesi,sizeof(aderesi),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_agahuza_ikintu,Guhuza_Stream);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int uburebure_agaciro=mp_obj_get_int(한도); if(uburebure_agaciro<1||uburebure_agaciro>512)mp_raise_OSError(MP_EINVAL);
    unsigned char amakurushingiro[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)amakurushingiro,uburebure_agaciro,0,0,0));
    return mp_obj_new_bytes(amakurushingiro,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Musomyi_ikintu,흐름읽기);
static mp_obj_t kwandika_Stream(mp_obj_t 종단,mp_obj_t Ibirimo_agaciro) {
    mp_buffer_info_t amakurushingiro; mp_get_buffer_raise(Ibirimo_agaciro,&amakurushingiro,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)amakurushingiro.buf,amakurushingiro.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Writer_ikintu,kwandika_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Izina) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)inzira_ingingo(Izina),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t kurema_ububiko(mp_obj_t Izina) {
    결과검사(사용자호출(18,(uintptr_t)inzira_ingingo(Izina),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,kurema_ububiko);
static mp_obj_t gukuramo_ububiko(mp_obj_t Izina) {
    결과검사(사용자호출(18,(uintptr_t)inzira_ingingo(Izina),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,gukuramo_ububiko);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_agahuza_ikintu) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_Musomyi_ikintu) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Writer_ikintu) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&dosiye_Musomyi_ikintu) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&dosiye_Writer_ikintu) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&isaha_ikintu) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
