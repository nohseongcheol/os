// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t REZULTATAS) { if (REZULTATAS < 0) mp_raise_OSError(-REZULTATAS); return REZULTATAS; }
static const char *kelias_argumentas(mp_obj_t VALUE) {
    size_t prekė_COUNT; const char *KELIAS = mp_obj_str_get_data(VALUE, &prekė_COUNT);
    if (!prekė_COUNT || prekė_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < prekė_COUNT; 순번++) if (!KELIAS[순번]) mp_raise_OSError(MP_EINVAL);
    return KELIAS;
}
static mp_obj_t 파일읽기(mp_obj_t Pavadinimas_2) {
    intptr_t Failas_rodyklė = 결과검사(사용자호출(3, (uintptr_t)kelias_argumentas(Pavadinimas_2), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Dydis = 결과검사(사용자호출(9, Failas_rodyklė, 0, 0, 0, 0, 0));
        vstr_t duomenys; vstr_init_len(&duomenys, Dydis);
        intptr_t REZULTATAS = 사용자호출(2, Failas_rodyklė, (uintptr_t)duomenys.buf, Dydis, 0, 0, 0);
        결과검사(REZULTATAS); duomenys.len = REZULTATAS;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&duomenys);
        nlr_pop(); 사용자호출(4, Failas_rodyklė, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, Failas_rodyklė, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Failas_Skaitytuvė_objektas, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Dydis=mp_obj_get_int(한도);
    if(Dydis<0||Dydis>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t duomenys; vstr_init_len(&duomenys,Dydis);
    intptr_t prekė_COUNT=사용자호출(2,0,(uintptr_t)duomenys.buf,Dydis,0,0,0);
    if(prekė_COUNT<0) { vstr_clear(&duomenys); 결과검사(prekė_COUNT); }
    duomenys.len=prekė_COUNT; return mp_obj_new_bytes_from_vstr(&duomenys);
}
static MP_DEFINE_CONST_FUN_OBJ_1(STDIN_Skaitytuvė_objektas, 표준입력읽기);
static mp_obj_t rašymas_Failas(mp_obj_t Pavadinimas_2, mp_obj_t Turinys_VALUE) {
    const char *KELIAS = kelias_argumentas(Pavadinimas_2);
    mp_buffer_info_t duomenys; mp_get_buffer_raise(Turinys_VALUE, &duomenys, MP_BUFFER_READ);
    if (duomenys.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t Failas_rodyklė = 결과검사(사용자호출(3, (uintptr_t)KELIAS, 577, 0, 0, 0, 0));
    intptr_t įrašas_COUNT = 사용자호출(1, Failas_rodyklė, (uintptr_t)duomenys.buf, duomenys.len, 0, 0, 0);
    사용자호출(4, Failas_rodyklė, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(įrašas_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Failas_Writer_objektas, rašymas_Failas);
static mp_obj_t pašalinti_Failas(mp_obj_t Pavadinimas_2) { 결과검사(사용자호출(11, (uintptr_t)kelias_argumentas(Pavadinimas_2), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, pašalinti_Failas);
static mp_obj_t Piešimas_stačiakampis(size_t prekė_COUNT, const mp_obj_t *argumentas_ARRAY) {
    (void)prekė_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argumentas_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(stačiakampis_objektas, 5, 5, Piešimas_stačiakampis);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Dydis[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Dydis);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t laikrodis_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(laikrodis_objektas, laikrodis_VALUE);
static mp_obj_t UDP_kurti(mp_obj_t prievado_numeris) {
    int duomenys_padėtis = mp_obj_get_int(prievado_numeris); if (duomenys_padėtis < 0 || duomenys_padėtis > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t Failas_rodyklė = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(duomenys_padėtis); 첫째값.sin_addr.s_addr = 0;
    intptr_t REZULTATAS = 사용자호출(33, Failas_rodyklė, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (REZULTATAS < 0) { 사용자호출(4, Failas_rodyklė, 0, 0, 0, 0, 0); 결과검사(REZULTATAS); }
    return mp_obj_new_int(Failas_rodyklė);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_kurti_OBJ, UDP_kurti);
static mp_obj_t UDP_siųsti(mp_obj_t Failas_rodyklė, mp_obj_t prievado_numeris, mp_obj_t Turinys_VALUE) {
    int duomenys_padėtis = mp_obj_get_int(prievado_numeris); if (duomenys_padėtis < 1 || duomenys_padėtis > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t duomenys; mp_get_buffer_raise(Turinys_VALUE, &duomenys, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(duomenys_padėtis); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(Failas_rodyklė), (uintptr_t)duomenys.buf, duomenys.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_siųsti_OBJ, UDP_siųsti);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t 길이; const char *Tekstas=mp_obj_str_get_data(VALUE,&길이);
    unsigned dabartinis_padėtis=0; uint32_t ADDRESS=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,skaitmuo_COUNT=0;
        while(dabartinis_padėtis<길이&&Tekstas[dabartinis_padėtis]>='0'&&Tekstas[dabartinis_padėtis]<='9') {
            VALUE=VALUE*10+Tekstas[dabartinis_padėtis++]-'0'; if(++skaitmuo_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!skaitmuo_COUNT)mp_raise_OSError(MP_EINVAL);
        ADDRESS=ADDRESS<<8|VALUE;
        if(부분<3&&(dabartinis_padėtis>=길이||Tekstas[dabartinis_padėtis++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(dabartinis_padėtis!=길이)mp_raise_OSError(MP_EINVAL);
    return ADDRESS;
}
static mp_obj_t 전문주소전송(size_t įrašas_COUNT, const mp_obj_t *argumentas_ARRAY) {
    (void)įrašas_COUNT; uint32_t ADDRESS=인터넷주소읽기(argumentas_ARRAY[1]);
    int prievado_numeris=mp_obj_get_int(argumentas_ARRAY[2]);if(prievado_numeris<1||prievado_numeris>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t duomenys;mp_get_buffer_raise(argumentas_ARRAY[3],&duomenys,MP_BUFFER_READ);
    struct pk_sockaddr_in tikslas={0};tikslas.sin_family=AF_INET;tikslas.sin_port=pk_htons(prievado_numeris);tikslas.sin_addr.s_addr=pk_htonl(ADDRESS);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argumentas_ARRAY[0]),(uintptr_t)duomenys.buf,duomenys.len,0,(uintptr_t)&tikslas,sizeof(tikslas))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t Failas_rodyklė) {
    unsigned char duomenys[512]; struct pk_sockaddr_in lygiavertis_mazgas_VALUE; pk_socklen_t 길이값 = sizeof(lygiavertis_mazgas_VALUE);
    intptr_t Dydis = 결과검사(사용자호출(35, mp_obj_get_int(Failas_rodyklė), (uintptr_t)duomenys, 512, 0, (uintptr_t)&lygiavertis_mazgas_VALUE, (uintptr_t)&길이값));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(duomenys, Dydis), MP_OBJ_NEW_SMALL_INT(pk_htons(lygiavertis_mazgas_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Uždaryti(mp_obj_t Failas_rodyklė) { 결과검사(사용자호출(4, mp_obj_get_int(Failas_rodyklė), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Uždaryti_OBJ, UDP_Uždaryti);
static mp_obj_t kurti_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,debesis_Šeima,Stream_tinklas,Stream_transportavimo_protokolas,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,kurti_Stream);
static mp_obj_t ryšys_Stream(mp_obj_t dalyvis,mp_obj_t ADDRESS_SMS,mp_obj_t INDEX) {
    int prievado_numeris=mp_obj_get_int(INDEX); if(prievado_numeris<1||prievado_numeris>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ADDRESS={0}; ADDRESS.ADDRESS_Šeima=debesis_Šeima;
    ADDRESS.prievado_numeris=망차례짧은수(prievado_numeris); ADDRESS.interneto_adresas.ADDRESS_VALUE=tinklas_sveikasis_skaičius(인터넷주소읽기(ADDRESS_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(dalyvis),(uintptr_t)&ADDRESS,sizeof(ADDRESS),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_Jungtis_objektas,ryšys_Stream);
static mp_obj_t 흐름읽기(mp_obj_t dalyvis,mp_obj_t 한도) {
    int 길이=mp_obj_get_int(한도); if(길이<1||길이>512)mp_raise_OSError(MP_EINVAL);
    unsigned char duomenys[512];
    intptr_t prekė_COUNT=결과검사(사용자호출(2,mp_obj_get_int(dalyvis),(uintptr_t)duomenys,길이,0,0,0));
    return mp_obj_new_bytes(duomenys,prekė_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Skaitytuvė_objektas,흐름읽기);
static mp_obj_t rašymas_Stream(mp_obj_t dalyvis,mp_obj_t Turinys_VALUE) {
    mp_buffer_info_t duomenys; mp_get_buffer_raise(Turinys_VALUE,&duomenys,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(dalyvis),(uintptr_t)duomenys.buf,duomenys.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Writer_objektas,rašymas_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Palauk_objektas,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Pavadinimas_2) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)kelias_argumentas(Pavadinimas_2),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t kurti_Katalogas(mp_obj_t Pavadinimas_2) {
    결과검사(사용자호출(18,(uintptr_t)kelias_argumentas(Pavadinimas_2),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Katalogas_kūrėjas_objektas,kurti_Katalogas);
static mp_obj_t pašalinti_Katalogas(mp_obj_t Pavadinimas_2) {
    결과검사(사용자호출(18,(uintptr_t)kelias_argumentas(Pavadinimas_2),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,pašalinti_Katalogas);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_Jungtis_objektas) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_Skaitytuvė_objektas) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Writer_objektas) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&Palauk_objektas) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&Katalogas_kūrėjas_objektas) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&STDIN_Skaitytuvė_objektas) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Failas_Skaitytuvė_objektas) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Failas_Writer_objektas) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&stačiakampis_objektas) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&laikrodis_objektas) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_kurti_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_siųsti_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Uždaryti_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
