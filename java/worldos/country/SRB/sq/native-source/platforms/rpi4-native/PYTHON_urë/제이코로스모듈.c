// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t llogaritje) { if (llogaritje < 0) mp_raise_OSError(-llogaritje); return llogaritje; }
static const char *shteg_argument(mp_obj_t VALUE) {
    size_t njësi_COUNT; const char *POZICIONI = mp_obj_str_get_data(VALUE, &njësi_COUNT);
    if (!njësi_COUNT || njësi_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < njësi_COUNT; 순번++) if (!POZICIONI[순번]) mp_raise_OSError(MP_EINVAL);
    return POZICIONI;
}
static mp_obj_t 파일읽기(mp_obj_t Emër) {
    intptr_t skedar_dorezë = 결과검사(사용자호출(3, (uintptr_t)shteg_argument(Emër), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Madhësi = 결과검사(사용자호출(9, skedar_dorezë, 0, 0, 0, 0, 0));
        vstr_t të_dhëna; vstr_init_len(&të_dhëna, Madhësi);
        intptr_t llogaritje = 사용자호출(2, skedar_dorezë, (uintptr_t)të_dhëna.buf, Madhësi, 0, 0, 0);
        결과검사(llogaritje); të_dhëna.len = llogaritje;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&të_dhëna);
        nlr_pop(); 사용자호출(4, skedar_dorezë, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, skedar_dorezë, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(skedar_lexues_objekt, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Madhësi=mp_obj_get_int(한도);
    if(Madhësi<0||Madhësi>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t të_dhëna; vstr_init_len(&të_dhëna,Madhësi);
    intptr_t njësi_COUNT=사용자호출(2,0,(uintptr_t)të_dhëna.buf,Madhësi,0,0,0);
    if(njësi_COUNT<0) { vstr_clear(&të_dhëna); 결과검사(njësi_COUNT); }
    të_dhëna.len=njësi_COUNT; return mp_obj_new_bytes_from_vstr(&të_dhëna);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t shkruaj_skedar(mp_obj_t Emër, mp_obj_t Përmbajtje_VALUE) {
    const char *POZICIONI = shteg_argument(Emër);
    mp_buffer_info_t të_dhëna; mp_get_buffer_raise(Përmbajtje_VALUE, &të_dhëna, MP_BUFFER_READ);
    if (të_dhëna.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t skedar_dorezë = 결과검사(사용자호출(3, (uintptr_t)POZICIONI, 577, 0, 0, 0, 0));
    intptr_t futje_COUNT = 사용자호출(1, skedar_dorezë, (uintptr_t)të_dhëna.buf, të_dhëna.len, 0, 0, 0);
    사용자호출(4, skedar_dorezë, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(futje_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(skedar_Shkruesi_objekt, shkruaj_skedar);
static mp_obj_t heq_skedar(mp_obj_t Emër) { 결과검사(사용자호출(11, (uintptr_t)shteg_argument(Emër), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, heq_skedar);
static mp_obj_t 사각형그리기(size_t njësi_COUNT, const mp_obj_t *argument_ARRAY) {
    (void)njësi_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argument_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Madhësi[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Madhësi);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Ora_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Ora_objekt, Ora_VALUE);
static mp_obj_t UDP_hap(mp_obj_t numri_i_portës) {
    int të_dhëna_pozicioni = mp_obj_get_int(numri_i_portës); if (të_dhëna_pozicioni < 0 || të_dhëna_pozicioni > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t skedar_dorezë = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(të_dhëna_pozicioni); 첫째값.sin_addr.s_addr = 0;
    intptr_t llogaritje = 사용자호출(33, skedar_dorezë, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (llogaritje < 0) { 사용자호출(4, skedar_dorezë, 0, 0, 0, 0, 0); 결과검사(llogaritje); }
    return mp_obj_new_int(skedar_dorezë);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_hap_OBJ, UDP_hap);
static mp_obj_t UDP_dërgoj(mp_obj_t skedar_dorezë, mp_obj_t numri_i_portës, mp_obj_t Përmbajtje_VALUE) {
    int të_dhëna_pozicioni = mp_obj_get_int(numri_i_portës); if (të_dhëna_pozicioni < 1 || të_dhëna_pozicioni > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t të_dhëna; mp_get_buffer_raise(Përmbajtje_VALUE, &të_dhëna, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(të_dhëna_pozicioni); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(skedar_dorezë), (uintptr_t)të_dhëna.buf, të_dhëna.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_dërgoj_OBJ, UDP_dërgoj);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t gjatësi_VALUE; const char *Teksti=mp_obj_str_get_data(VALUE,&gjatësi_VALUE);
    unsigned 현재위치=0; uint32_t email=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,shifër_COUNT=0;
        while(현재위치<gjatësi_VALUE&&Teksti[현재위치]>='0'&&Teksti[현재위치]<='9') {
            VALUE=VALUE*10+Teksti[현재위치++]-'0'; if(++shifër_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!shifër_COUNT)mp_raise_OSError(MP_EINVAL);
        email=email<<8|VALUE;
        if(부분<3&&(현재위치>=gjatësi_VALUE||Teksti[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=gjatësi_VALUE)mp_raise_OSError(MP_EINVAL);
    return email;
}
static mp_obj_t 전문주소전송(size_t futje_COUNT, const mp_obj_t *argument_ARRAY) {
    (void)futje_COUNT; uint32_t email=인터넷주소읽기(argument_ARRAY[1]);
    int numri_i_portës=mp_obj_get_int(argument_ARRAY[2]);if(numri_i_portës<1||numri_i_portës>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t të_dhëna;mp_get_buffer_raise(argument_ARRAY[3],&të_dhëna,MP_BUFFER_READ);
    struct pk_sockaddr_in objektiv={0};objektiv.sin_family=AF_INET;objektiv.sin_port=pk_htons(numri_i_portës);objektiv.sin_addr.s_addr=pk_htonl(email);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argument_ARRAY[0]),(uintptr_t)të_dhëna.buf,të_dhëna.len,0,(uintptr_t)&objektiv,sizeof(objektiv))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t skedar_dorezë) {
    unsigned char të_dhëna[512]; struct pk_sockaddr_in homolog_VALUE; pk_socklen_t gjatësi_të_dhëna = sizeof(homolog_VALUE);
    intptr_t Madhësi = 결과검사(사용자호출(35, mp_obj_get_int(skedar_dorezë), (uintptr_t)të_dhëna, 512, 0, (uintptr_t)&homolog_VALUE, (uintptr_t)&gjatësi_të_dhëna));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(të_dhëna, Madhësi), MP_OBJ_NEW_SMALL_INT(pk_htons(homolog_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_mbyll(mp_obj_t skedar_dorezë) { 결과검사(사용자호출(4, mp_obj_get_int(skedar_dorezë), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_mbyll_OBJ, UDP_mbyll);
static mp_obj_t hap_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,Internet_Familja,Stream_rrjet,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,hap_Stream);
static mp_obj_t Lidh_Stream(mp_obj_t 종단,mp_obj_t email_SMS,mp_obj_t INDEX) {
    int numri_i_portës=mp_obj_get_int(INDEX); if(numri_i_portës<1||numri_i_portës>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 email={0}; email.email_Familja=Internet_Familja;
    email.numri_i_portës=망차례짧은수(numri_i_portës); email.adresë_në_internet.email_VALUE=rrjet_numër_i_plotë(인터넷주소읽기(email_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&email,sizeof(email),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_bashkues_objekt,Lidh_Stream);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int gjatësi_VALUE=mp_obj_get_int(한도); if(gjatësi_VALUE<1||gjatësi_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char të_dhëna[512];
    intptr_t njësi_COUNT=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)të_dhëna,gjatësi_VALUE,0,0,0));
    return mp_obj_new_bytes(të_dhëna,njësi_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_lexues_objekt,흐름읽기);
static mp_obj_t shkruaj_Stream(mp_obj_t 종단,mp_obj_t Përmbajtje_VALUE) {
    mp_buffer_info_t të_dhëna; mp_get_buffer_raise(Përmbajtje_VALUE,&të_dhëna,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)të_dhëna.buf,të_dhëna.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Shkruesi_objekt,shkruaj_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t Ora_VALUE_4692cef5) {
    결과검사(사용자호출(17,mp_obj_get_int(Ora_VALUE_4692cef5),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Prit_objekt,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Emër) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)shteg_argument(Emër),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Krijo_direktori(mp_obj_t Emër) {
    결과검사(사용자호출(18,(uintptr_t)shteg_argument(Emër),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,Krijo_direktori);
static mp_obj_t heq_direktori(mp_obj_t Emër) {
    결과검사(사용자호출(18,(uintptr_t)shteg_argument(Emër),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,heq_direktori);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_bashkues_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_lexues_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Shkruesi_objekt) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&Prit_objekt) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&skedar_lexues_objekt) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&skedar_Shkruesi_objekt) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Ora_objekt) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_hap_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_dërgoj_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_mbyll_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
