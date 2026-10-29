// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t REZULTAT) { if (REZULTAT < 0) mp_raise_OSError(-REZULTAT); return REZULTAT; }
static const char *put_argument(mp_obj_t VALUE) {
    size_t artikl_COUNT; const char *PUTANJA = mp_obj_str_get_data(VALUE, &artikl_COUNT);
    if (!artikl_COUNT || artikl_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < artikl_COUNT; 순번++) if (!PUTANJA[순번]) mp_raise_OSError(MP_EINVAL);
    return PUTANJA;
}
static mp_obj_t 파일읽기(mp_obj_t Ime) {
    intptr_t Datoteka_ustroj = 결과검사(사용자호출(3, (uintptr_t)put_argument(Ime), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Veličina = 결과검사(사용자호출(9, Datoteka_ustroj, 0, 0, 0, 0, 0));
        vstr_t podaci; vstr_init_len(&podaci, Veličina);
        intptr_t REZULTAT = 사용자호출(2, Datoteka_ustroj, (uintptr_t)podaci.buf, Veličina, 0, 0, 0);
        결과검사(REZULTAT); podaci.len = REZULTAT;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&podaci);
        nlr_pop(); 사용자호출(4, Datoteka_ustroj, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, Datoteka_ustroj, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Datoteka_Čitač_objekt, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Veličina=mp_obj_get_int(한도);
    if(Veličina<0||Veličina>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t podaci; vstr_init_len(&podaci,Veličina);
    intptr_t artikl_COUNT=사용자호출(2,0,(uintptr_t)podaci.buf,Veličina,0,0,0);
    if(artikl_COUNT<0) { vstr_clear(&podaci); 결과검사(artikl_COUNT); }
    podaci.len=artikl_COUNT; return mp_obj_new_bytes_from_vstr(&podaci);
}
static MP_DEFINE_CONST_FUN_OBJ_1(STDIN_Čitač_objekt, 표준입력읽기);
static mp_obj_t zapisivanje_Datoteka(mp_obj_t Ime, mp_obj_t Sadržaj_VALUE) {
    const char *PUTANJA = put_argument(Ime);
    mp_buffer_info_t podaci; mp_get_buffer_raise(Sadržaj_VALUE, &podaci, MP_BUFFER_READ);
    if (podaci.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t Datoteka_ustroj = 결과검사(사용자호출(3, (uintptr_t)PUTANJA, 577, 0, 0, 0, 0));
    intptr_t unos_COUNT = 사용자호출(1, Datoteka_ustroj, (uintptr_t)podaci.buf, podaci.len, 0, 0, 0);
    사용자호출(4, Datoteka_ustroj, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(unos_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Datoteka_Writer_objekt, zapisivanje_Datoteka);
static mp_obj_t ukloniti_Datoteka(mp_obj_t Ime) { 결과검사(사용자호출(11, (uintptr_t)put_argument(Ime), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, ukloniti_Datoteka);
static mp_obj_t Bojanje_pravokutnik(size_t artikl_COUNT, const mp_obj_t *argument_ARRAY) {
    (void)artikl_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argument_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(pravokutnik_objekt, 5, 5, Bojanje_pravokutnik);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Veličina[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Veličina);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Sat_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Sat_objekt, Sat_VALUE);
static mp_obj_t UDP_otvoreno(mp_obj_t broj_priključka) {
    int podaci_položaj = mp_obj_get_int(broj_priključka); if (podaci_položaj < 0 || podaci_položaj > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t Datoteka_ustroj = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(podaci_položaj); 첫째값.sin_addr.s_addr = 0;
    intptr_t REZULTAT = 사용자호출(33, Datoteka_ustroj, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (REZULTAT < 0) { 사용자호출(4, Datoteka_ustroj, 0, 0, 0, 0, 0); 결과검사(REZULTAT); }
    return mp_obj_new_int(Datoteka_ustroj);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_otvoreno_OBJ, UDP_otvoreno);
static mp_obj_t UDP_slati(mp_obj_t Datoteka_ustroj, mp_obj_t broj_priključka, mp_obj_t Sadržaj_VALUE) {
    int podaci_položaj = mp_obj_get_int(broj_priključka); if (podaci_položaj < 1 || podaci_položaj > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t podaci; mp_get_buffer_raise(Sadržaj_VALUE, &podaci, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(podaci_položaj); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(Datoteka_ustroj), (uintptr_t)podaci.buf, podaci.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_slati_OBJ, UDP_slati);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t 길이; const char *Tekst=mp_obj_str_get_data(VALUE,&길이);
    unsigned redovno_položaj=0; uint32_t adresa=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,znamenka_COUNT=0;
        while(redovno_položaj<길이&&Tekst[redovno_položaj]>='0'&&Tekst[redovno_položaj]<='9') {
            VALUE=VALUE*10+Tekst[redovno_položaj++]-'0'; if(++znamenka_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!znamenka_COUNT)mp_raise_OSError(MP_EINVAL);
        adresa=adresa<<8|VALUE;
        if(부분<3&&(redovno_položaj>=길이||Tekst[redovno_položaj++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(redovno_položaj!=길이)mp_raise_OSError(MP_EINVAL);
    return adresa;
}
static mp_obj_t 전문주소전송(size_t unos_COUNT, const mp_obj_t *argument_ARRAY) {
    (void)unos_COUNT; uint32_t adresa=인터넷주소읽기(argument_ARRAY[1]);
    int broj_priključka=mp_obj_get_int(argument_ARRAY[2]);if(broj_priključka<1||broj_priključka>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t podaci;mp_get_buffer_raise(argument_ARRAY[3],&podaci,MP_BUFFER_READ);
    struct pk_sockaddr_in cilj={0};cilj.sin_family=AF_INET;cilj.sin_port=pk_htons(broj_priključka);cilj.sin_addr.s_addr=pk_htonl(adresa);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argument_ARRAY[0]),(uintptr_t)podaci.buf,podaci.len,0,(uintptr_t)&cilj,sizeof(cilj))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t Datoteka_ustroj) {
    unsigned char podaci[512]; struct pk_sockaddr_in ravnopravan_član_VALUE; pk_socklen_t 길이값 = sizeof(ravnopravan_član_VALUE);
    intptr_t Veličina = 결과검사(사용자호출(35, mp_obj_get_int(Datoteka_ustroj), (uintptr_t)podaci, 512, 0, (uintptr_t)&ravnopravan_član_VALUE, (uintptr_t)&길이값));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(podaci, Veličina), MP_OBJ_NEW_SMALL_INT(pk_htons(ravnopravan_član_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Zatvori(mp_obj_t Datoteka_ustroj) { 결과검사(사용자호출(4, mp_obj_get_int(Datoteka_ustroj), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Zatvori_OBJ, UDP_Zatvori);
static mp_obj_t otvoreno_tok(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,oblak_linija,tok_mreža,tok_protokol_za_prijenos,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,otvoreno_tok);
static mp_obj_t CONNECT_tok(mp_obj_t sudionik,mp_obj_t adresa_SMS,mp_obj_t INDEX) {
    int broj_priključka=mp_obj_get_int(INDEX); if(broj_priključka<1||broj_priključka>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 adresa={0}; adresa.adresa_linija=oblak_linija;
    adresa.broj_priključka=망차례짧은수(broj_priključka); adresa.internetska_adresa.adresa_VALUE=mreža_cijeli_broj(인터넷주소읽기(adresa_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(sudionik),(uintptr_t)&adresa,sizeof(adresa),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(tok_Poveznik_objekt,CONNECT_tok);
static mp_obj_t 흐름읽기(mp_obj_t sudionik,mp_obj_t 한도) {
    int 길이=mp_obj_get_int(한도); if(길이<1||길이>512)mp_raise_OSError(MP_EINVAL);
    unsigned char podaci[512];
    intptr_t artikl_COUNT=결과검사(사용자호출(2,mp_obj_get_int(sudionik),(uintptr_t)podaci,길이,0,0,0));
    return mp_obj_new_bytes(podaci,artikl_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(tok_Čitač_objekt,흐름읽기);
static mp_obj_t zapisivanje_tok(mp_obj_t sudionik,mp_obj_t Sadržaj_VALUE) {
    mp_buffer_info_t podaci; mp_get_buffer_raise(Sadržaj_VALUE,&podaci,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(sudionik),(uintptr_t)podaci.buf,podaci.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(tok_Writer_objekt,zapisivanje_tok);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(čekaj_objekt,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Ime) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)put_argument(Ime),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Create_imenik(mp_obj_t Ime) {
    결과검사(사용자호출(18,(uintptr_t)put_argument(Ime),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(imenik_autor_objekt,Create_imenik);
static mp_obj_t ukloniti_imenik(mp_obj_t Ime) {
    결과검사(사용자호출(18,(uintptr_t)put_argument(Ime),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,ukloniti_imenik);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&tok_Poveznik_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&tok_Čitač_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&tok_Writer_objekt) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&čekaj_objekt) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&imenik_autor_objekt) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&STDIN_Čitač_objekt) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Datoteka_Čitač_objekt) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Datoteka_Writer_objekt) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&pravokutnik_objekt) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Sat_objekt) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_otvoreno_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_slati_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Zatvori_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
