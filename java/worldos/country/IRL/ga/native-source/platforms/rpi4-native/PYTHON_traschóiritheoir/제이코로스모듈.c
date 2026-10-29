// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t tomhas) { if (tomhas < 0) mp_raise_OSError(-tomhas); return tomhas; }
static const char *cosán_argóint(mp_obj_t VALUE) {
    size_t mír_COUNT; const char *CONAIR = mp_obj_str_get_data(VALUE, &mír_COUNT);
    if (!mír_COUNT || mír_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < mír_COUNT; 순번++) if (!CONAIR[순번]) mp_raise_OSError(MP_EINVAL);
    return CONAIR;
}
static mp_obj_t 파일읽기(mp_obj_t Ainm) {
    intptr_t comhad_hanla = 결과검사(사용자호출(3, (uintptr_t)cosán_argóint(Ainm), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Méid = 결과검사(사용자호출(9, comhad_hanla, 0, 0, 0, 0, 0));
        vstr_t sonraí; vstr_init_len(&sonraí, Méid);
        intptr_t tomhas = 사용자호출(2, comhad_hanla, (uintptr_t)sonraí.buf, Méid, 0, 0, 0);
        결과검사(tomhas); sonraí.len = tomhas;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&sonraí);
        nlr_pop(); 사용자호출(4, comhad_hanla, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, comhad_hanla, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(comhad_Léitheoir_oibiacht, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Méid=mp_obj_get_int(한도);
    if(Méid<0||Méid>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t sonraí; vstr_init_len(&sonraí,Méid);
    intptr_t mír_COUNT=사용자호출(2,0,(uintptr_t)sonraí.buf,Méid,0,0,0);
    if(mír_COUNT<0) { vstr_clear(&sonraí); 결과검사(mír_COUNT); }
    sonraí.len=mír_COUNT; return mp_obj_new_bytes_from_vstr(&sonraí);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t scríobh_comhad(mp_obj_t Ainm, mp_obj_t Inneachar_VALUE) {
    const char *CONAIR = cosán_argóint(Ainm);
    mp_buffer_info_t sonraí; mp_get_buffer_raise(Inneachar_VALUE, &sonraí, MP_BUFFER_READ);
    if (sonraí.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t comhad_hanla = 결과검사(사용자호출(3, (uintptr_t)CONAIR, 577, 0, 0, 0, 0));
    intptr_t iontráil_COUNT = 사용자호출(1, comhad_hanla, (uintptr_t)sonraí.buf, sonraí.len, 0, 0, 0);
    사용자호출(4, comhad_hanla, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(iontráil_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(comhad_Scríbhneoir_oibiacht, scríobh_comhad);
static mp_obj_t bain_comhad(mp_obj_t Ainm) { 결과검사(사용자호출(11, (uintptr_t)cosán_argóint(Ainm), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, bain_comhad);
static mp_obj_t 사각형그리기(size_t mír_COUNT, const mp_obj_t *argóint_ARRAY) {
    (void)mír_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argóint_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Méid[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Méid);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Clog_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Clog_oibiacht, Clog_VALUE);
static mp_obj_t UDP_oscail(mp_obj_t uimhir_phoirt) {
    int sonraí_suíomh = mp_obj_get_int(uimhir_phoirt); if (sonraí_suíomh < 0 || sonraí_suíomh > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t comhad_hanla = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(sonraí_suíomh); 첫째값.sin_addr.s_addr = 0;
    intptr_t tomhas = 사용자호출(33, comhad_hanla, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (tomhas < 0) { 사용자호출(4, comhad_hanla, 0, 0, 0, 0, 0); 결과검사(tomhas); }
    return mp_obj_new_int(comhad_hanla);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, UDP_oscail);
static mp_obj_t UDP_seol(mp_obj_t comhad_hanla, mp_obj_t uimhir_phoirt, mp_obj_t Inneachar_VALUE) {
    int sonraí_suíomh = mp_obj_get_int(uimhir_phoirt); if (sonraí_suíomh < 1 || sonraí_suíomh > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t sonraí; mp_get_buffer_raise(Inneachar_VALUE, &sonraí, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(sonraí_suíomh); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(comhad_hanla), (uintptr_t)sonraí.buf, sonraí.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, UDP_seol);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t fad_VALUE; const char *Téacs=mp_obj_str_get_data(VALUE,&fad_VALUE);
    unsigned 현재위치=0; uint32_t ADDRESS=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,digit_COUNT=0;
        while(현재위치<fad_VALUE&&Téacs[현재위치]>='0'&&Téacs[현재위치]<='9') {
            VALUE=VALUE*10+Téacs[현재위치++]-'0'; if(++digit_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!digit_COUNT)mp_raise_OSError(MP_EINVAL);
        ADDRESS=ADDRESS<<8|VALUE;
        if(부분<3&&(현재위치>=fad_VALUE||Téacs[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=fad_VALUE)mp_raise_OSError(MP_EINVAL);
    return ADDRESS;
}
static mp_obj_t 전문주소전송(size_t iontráil_COUNT, const mp_obj_t *argóint_ARRAY) {
    (void)iontráil_COUNT; uint32_t ADDRESS=인터넷주소읽기(argóint_ARRAY[1]);
    int uimhir_phoirt=mp_obj_get_int(argóint_ARRAY[2]);if(uimhir_phoirt<1||uimhir_phoirt>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t sonraí;mp_get_buffer_raise(argóint_ARRAY[3],&sonraí,MP_BUFFER_READ);
    struct pk_sockaddr_in sprioc={0};sprioc.sin_family=AF_INET;sprioc.sin_port=pk_htons(uimhir_phoirt);sprioc.sin_addr.s_addr=pk_htonl(ADDRESS);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argóint_ARRAY[0]),(uintptr_t)sonraí.buf,sonraí.len,0,(uintptr_t)&sprioc,sizeof(sprioc))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t comhad_hanla) {
    unsigned char sonraí[512]; struct pk_sockaddr_in piara_VALUE; pk_socklen_t fad_sonraí = sizeof(piara_VALUE);
    intptr_t Méid = 결과검사(사용자호출(35, mp_obj_get_int(comhad_hanla), (uintptr_t)sonraí, 512, 0, (uintptr_t)&piara_VALUE, (uintptr_t)&fad_sonraí));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(sonraí, Méid), MP_OBJ_NEW_SMALL_INT(pk_htons(piara_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_dún(mp_obj_t comhad_hanla) { 결과검사(사용자호출(4, mp_obj_get_int(comhad_hanla), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, UDP_dún);
static mp_obj_t oscail_sruth(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,néal_Teaghlach,sruth_Líonra,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,oscail_sruth);
static mp_obj_t nasc_sruth(mp_obj_t 종단,mp_obj_t ADDRESS_SMS,mp_obj_t INDEX) {
    int uimhir_phoirt=mp_obj_get_int(INDEX); if(uimhir_phoirt<1||uimhir_phoirt>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ADDRESS={0}; ADDRESS.ADDRESS_Teaghlach=néal_Teaghlach;
    ADDRESS.uimhir_phoirt=망차례짧은수(uimhir_phoirt); ADDRESS.seoladh_Idirlín.ADDRESS_VALUE=Líonra_slánuimhir(인터넷주소읽기(ADDRESS_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ADDRESS,sizeof(ADDRESS),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(sruth_nascóir_oibiacht,nasc_sruth);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int fad_VALUE=mp_obj_get_int(한도); if(fad_VALUE<1||fad_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char sonraí[512];
    intptr_t mír_COUNT=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)sonraí,fad_VALUE,0,0,0));
    return mp_obj_new_bytes(sonraí,mír_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(sruth_Léitheoir_oibiacht,흐름읽기);
static mp_obj_t scríobh_sruth(mp_obj_t 종단,mp_obj_t Inneachar_VALUE) {
    mp_buffer_info_t sonraí; mp_get_buffer_raise(Inneachar_VALUE,&sonraí,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)sonraí.buf,sonraí.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(sruth_Scríbhneoir_oibiacht,scríobh_sruth);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Ainm) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)cosán_argóint(Ainm),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Create_eolaire(mp_obj_t Ainm) {
    결과검사(사용자호출(18,(uintptr_t)cosán_argóint(Ainm),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,Create_eolaire);
static mp_obj_t bain_eolaire(mp_obj_t Ainm) {
    결과검사(사용자호출(18,(uintptr_t)cosán_argóint(Ainm),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,bain_eolaire);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&sruth_nascóir_oibiacht) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&sruth_Léitheoir_oibiacht) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&sruth_Scríbhneoir_oibiacht) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&comhad_Léitheoir_oibiacht) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&comhad_Scríbhneoir_oibiacht) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Clog_oibiacht) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
