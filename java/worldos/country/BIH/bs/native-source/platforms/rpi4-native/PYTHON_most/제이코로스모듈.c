// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t mjera) { if (mjera < 0) mp_raise_OSError(-mjera); return mjera; }
static const char *put_argument(mp_obj_t VALUE) {
    size_t stavka_COUNT; const char *Putanja = mp_obj_str_get_data(VALUE, &stavka_COUNT);
    if (!stavka_COUNT || stavka_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < stavka_COUNT; 순번++) if (!Putanja[순번]) mp_raise_OSError(MP_EINVAL);
    return Putanja;
}
static mp_obj_t 파일읽기(mp_obj_t Naziv) {
    intptr_t fajl_hvatište = 결과검사(사용자호출(3, (uintptr_t)put_argument(Naziv), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Veličina = 결과검사(사용자호출(9, fajl_hvatište, 0, 0, 0, 0, 0));
        vstr_t podaci; vstr_init_len(&podaci, Veličina);
        intptr_t mjera = 사용자호출(2, fajl_hvatište, (uintptr_t)podaci.buf, Veličina, 0, 0, 0);
        결과검사(mjera); podaci.len = mjera;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&podaci);
        nlr_pop(); 사용자호출(4, fajl_hvatište, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, fajl_hvatište, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(fajl_Čitač_objekt, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Veličina=mp_obj_get_int(한도);
    if(Veličina<0||Veličina>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t podaci; vstr_init_len(&podaci,Veličina);
    intptr_t stavka_COUNT=사용자호출(2,0,(uintptr_t)podaci.buf,Veličina,0,0,0);
    if(stavka_COUNT<0) { vstr_clear(&podaci); 결과검사(stavka_COUNT); }
    podaci.len=stavka_COUNT; return mp_obj_new_bytes_from_vstr(&podaci);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t pisati_fajl(mp_obj_t Naziv, mp_obj_t Sadržaj_VALUE) {
    const char *Putanja = put_argument(Naziv);
    mp_buffer_info_t podaci; mp_get_buffer_raise(Sadržaj_VALUE, &podaci, MP_BUFFER_READ);
    if (podaci.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t fajl_hvatište = 결과검사(사용자호출(3, (uintptr_t)Putanja, 577, 0, 0, 0, 0));
    intptr_t unos_COUNT = 사용자호출(1, fajl_hvatište, (uintptr_t)podaci.buf, podaci.len, 0, 0, 0);
    사용자호출(4, fajl_hvatište, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(unos_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(fajl_Pisac_objekt, pisati_fajl);
static mp_obj_t ukloniti_fajl(mp_obj_t Naziv) { 결과검사(사용자호출(11, (uintptr_t)put_argument(Naziv), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, ukloniti_fajl);
static mp_obj_t 사각형그리기(size_t stavka_COUNT, const mp_obj_t *argument_niz) {
    (void)stavka_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argument_niz[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Veličina[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Veličina);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Sat_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Sat_objekt, Sat_VALUE);
static mp_obj_t UDP_kreirati(mp_obj_t broj_priključka) {
    int podaci_položaj = mp_obj_get_int(broj_priključka); if (podaci_položaj < 0 || podaci_položaj > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t fajl_hvatište = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(podaci_položaj); 첫째값.sin_addr.s_addr = 0;
    intptr_t mjera = 사용자호출(33, fajl_hvatište, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (mjera < 0) { 사용자호출(4, fajl_hvatište, 0, 0, 0, 0, 0); 결과검사(mjera); }
    return mp_obj_new_int(fajl_hvatište);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, UDP_kreirati);
static mp_obj_t UDP_poslati(mp_obj_t fajl_hvatište, mp_obj_t broj_priključka, mp_obj_t Sadržaj_VALUE) {
    int podaci_položaj = mp_obj_get_int(broj_priključka); if (podaci_položaj < 1 || podaci_položaj > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t podaci; mp_get_buffer_raise(Sadržaj_VALUE, &podaci, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(podaci_položaj); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(fajl_hvatište), (uintptr_t)podaci.buf, podaci.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, UDP_poslati);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t dužina_VALUE; const char *Tekst=mp_obj_str_get_data(VALUE,&dužina_VALUE);
    unsigned trenutno_položaj=0; uint32_t adresa=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,cifra_COUNT=0;
        while(trenutno_položaj<dužina_VALUE&&Tekst[trenutno_položaj]>='0'&&Tekst[trenutno_položaj]<='9') {
            VALUE=VALUE*10+Tekst[trenutno_položaj++]-'0'; if(++cifra_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!cifra_COUNT)mp_raise_OSError(MP_EINVAL);
        adresa=adresa<<8|VALUE;
        if(부분<3&&(trenutno_položaj>=dužina_VALUE||Tekst[trenutno_položaj++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(trenutno_položaj!=dužina_VALUE)mp_raise_OSError(MP_EINVAL);
    return adresa;
}
static mp_obj_t 전문주소전송(size_t unos_COUNT, const mp_obj_t *argument_niz) {
    (void)unos_COUNT; uint32_t adresa=인터넷주소읽기(argument_niz[1]);
    int broj_priključka=mp_obj_get_int(argument_niz[2]);if(broj_priključka<1||broj_priključka>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t podaci;mp_get_buffer_raise(argument_niz[3],&podaci,MP_BUFFER_READ);
    struct pk_sockaddr_in cilj={0};cilj.sin_family=AF_INET;cilj.sin_port=pk_htons(broj_priključka);cilj.sin_addr.s_addr=pk_htonl(adresa);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argument_niz[0]),(uintptr_t)podaci.buf,podaci.len,0,(uintptr_t)&cilj,sizeof(cilj))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t fajl_hvatište) {
    unsigned char podaci[512]; struct pk_sockaddr_in peer_VALUE; pk_socklen_t dužina_podaci = sizeof(peer_VALUE);
    intptr_t Veličina = 결과검사(사용자호출(35, mp_obj_get_int(fajl_hvatište), (uintptr_t)podaci, 512, 0, (uintptr_t)&peer_VALUE, (uintptr_t)&dužina_podaci));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(podaci, Veličina), MP_OBJ_NEW_SMALL_INT(pk_htons(peer_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_zatvoriti(mp_obj_t fajl_hvatište) { 결과검사(사용자호출(4, mp_obj_get_int(fajl_hvatište), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, UDP_zatvoriti);
static mp_obj_t kreirati_tok(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,oblak_Porodica,tok_Mreža,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,kreirati_tok);
static mp_obj_t povezati_tok(mp_obj_t završna_tačka,mp_obj_t adresa_SMS,mp_obj_t INDEX) {
    int broj_priključka=mp_obj_get_int(INDEX); if(broj_priključka<1||broj_priključka>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 adresa={0}; adresa.adresa_Porodica=oblak_Porodica;
    adresa.broj_priključka=망차례짧은수(broj_priključka); adresa.internetska_adresa.adresa_VALUE=Mreža_cijeli_broj(인터넷주소읽기(adresa_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(završna_tačka),(uintptr_t)&adresa,sizeof(adresa),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(tok_konektor_objekt,povezati_tok);
static mp_obj_t 흐름읽기(mp_obj_t završna_tačka,mp_obj_t 한도) {
    int dužina_VALUE=mp_obj_get_int(한도); if(dužina_VALUE<1||dužina_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char podaci[512];
    intptr_t stavka_COUNT=결과검사(사용자호출(2,mp_obj_get_int(završna_tačka),(uintptr_t)podaci,dužina_VALUE,0,0,0));
    return mp_obj_new_bytes(podaci,stavka_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(tok_Čitač_objekt,흐름읽기);
static mp_obj_t pisati_tok(mp_obj_t završna_tačka,mp_obj_t Sadržaj_VALUE) {
    mp_buffer_info_t podaci; mp_get_buffer_raise(Sadržaj_VALUE,&podaci,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(završna_tačka),(uintptr_t)podaci.buf,podaci.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(tok_Pisac_objekt,pisati_tok);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(čekaj_objekt,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Naziv) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)put_argument(Naziv),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Create_Direktorij(mp_obj_t Naziv) {
    결과검사(사용자호출(18,(uintptr_t)put_argument(Naziv),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,Create_Direktorij);
static mp_obj_t ukloniti_Direktorij(mp_obj_t Naziv) {
    결과검사(사용자호출(18,(uintptr_t)put_argument(Naziv),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,ukloniti_Direktorij);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&tok_konektor_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&tok_Čitač_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&tok_Pisac_objekt) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&čekaj_objekt) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&fajl_Čitač_objekt) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&fajl_Pisac_objekt) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Sat_objekt) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
