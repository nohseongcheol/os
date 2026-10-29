// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t REZULTAT) { if (REZULTAT < 0) mp_raise_OSError(-REZULTAT); return REZULTAT; }
static const char *pot_argument(mp_obj_t VALUE) {
    size_t element_COUNT; const char *POT = mp_obj_str_get_data(VALUE, &element_COUNT);
    if (!element_COUNT || element_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < element_COUNT; 순번++) if (!POT[순번]) mp_raise_OSError(MP_EINVAL);
    return POT;
}
static mp_obj_t 파일읽기(mp_obj_t Ime) {
    intptr_t Datoteka_ročica = 결과검사(사용자호출(3, (uintptr_t)pot_argument(Ime), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Velikost = 결과검사(사용자호출(9, Datoteka_ročica, 0, 0, 0, 0, 0));
        vstr_t podatki; vstr_init_len(&podatki, Velikost);
        intptr_t REZULTAT = 사용자호출(2, Datoteka_ročica, (uintptr_t)podatki.buf, Velikost, 0, 0, 0);
        결과검사(REZULTAT); podatki.len = REZULTAT;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&podatki);
        nlr_pop(); 사용자호출(4, Datoteka_ročica, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, Datoteka_ročica, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Datoteka_bralec_predmet, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Velikost=mp_obj_get_int(한도);
    if(Velikost<0||Velikost>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t podatki; vstr_init_len(&podatki,Velikost);
    intptr_t element_COUNT=사용자호출(2,0,(uintptr_t)podatki.buf,Velikost,0,0,0);
    if(element_COUNT<0) { vstr_clear(&podatki); 결과검사(element_COUNT); }
    podatki.len=element_COUNT; return mp_obj_new_bytes_from_vstr(&podatki);
}
static MP_DEFINE_CONST_FUN_OBJ_1(STDIN_bralec_predmet, 표준입력읽기);
static mp_obj_t pisati_Datoteka(mp_obj_t Ime, mp_obj_t vsebina_VALUE) {
    const char *POT = pot_argument(Ime);
    mp_buffer_info_t podatki; mp_get_buffer_raise(vsebina_VALUE, &podatki, MP_BUFFER_READ);
    if (podatki.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t Datoteka_ročica = 결과검사(사용자호출(3, (uintptr_t)POT, 577, 0, 0, 0, 0));
    intptr_t vnos_COUNT = 사용자호출(1, Datoteka_ročica, (uintptr_t)podatki.buf, podatki.len, 0, 0, 0);
    사용자호출(4, Datoteka_ročica, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(vnos_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Datoteka_Writer_predmet, pisati_Datoteka);
static mp_obj_t odstraniti_Datoteka(mp_obj_t Ime) { 결과검사(사용자호출(11, (uintptr_t)pot_argument(Ime), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, odstraniti_Datoteka);
static mp_obj_t Slikar_pravokotnik(size_t element_COUNT, const mp_obj_t *argument_ARRAY) {
    (void)element_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argument_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(pravokotnik_predmet, 5, 5, Slikar_pravokotnik);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Velikost[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Velikost);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Ura_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Ura_predmet, Ura_VALUE);
static mp_obj_t UDP_odprto(mp_obj_t številka_vrat) {
    int podatki_položaj = mp_obj_get_int(številka_vrat); if (podatki_položaj < 0 || podatki_položaj > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t Datoteka_ročica = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(podatki_položaj); 첫째값.sin_addr.s_addr = 0;
    intptr_t REZULTAT = 사용자호출(33, Datoteka_ročica, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (REZULTAT < 0) { 사용자호출(4, Datoteka_ročica, 0, 0, 0, 0, 0); 결과검사(REZULTAT); }
    return mp_obj_new_int(Datoteka_ročica);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_odprto_OBJ, UDP_odprto);
static mp_obj_t UDP_poslati(mp_obj_t Datoteka_ročica, mp_obj_t številka_vrat, mp_obj_t vsebina_VALUE) {
    int podatki_položaj = mp_obj_get_int(številka_vrat); if (podatki_položaj < 1 || podatki_položaj > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t podatki; mp_get_buffer_raise(vsebina_VALUE, &podatki, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(podatki_položaj); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(Datoteka_ročica), (uintptr_t)podatki.buf, podatki.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_poslati_OBJ, UDP_poslati);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t 길이; const char *Besedilo=mp_obj_str_get_data(VALUE,&길이);
    unsigned sprotno_položaj=0; uint32_t naslov=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,številka_COUNT=0;
        while(sprotno_položaj<길이&&Besedilo[sprotno_položaj]>='0'&&Besedilo[sprotno_položaj]<='9') {
            VALUE=VALUE*10+Besedilo[sprotno_položaj++]-'0'; if(++številka_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!številka_COUNT)mp_raise_OSError(MP_EINVAL);
        naslov=naslov<<8|VALUE;
        if(부분<3&&(sprotno_položaj>=길이||Besedilo[sprotno_položaj++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(sprotno_položaj!=길이)mp_raise_OSError(MP_EINVAL);
    return naslov;
}
static mp_obj_t 전문주소전송(size_t vnos_COUNT, const mp_obj_t *argument_ARRAY) {
    (void)vnos_COUNT; uint32_t naslov=인터넷주소읽기(argument_ARRAY[1]);
    int številka_vrat=mp_obj_get_int(argument_ARRAY[2]);if(številka_vrat<1||številka_vrat>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t podatki;mp_get_buffer_raise(argument_ARRAY[3],&podatki,MP_BUFFER_READ);
    struct pk_sockaddr_in tarča={0};tarča.sin_family=AF_INET;tarča.sin_port=pk_htons(številka_vrat);tarča.sin_addr.s_addr=pk_htonl(naslov);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argument_ARRAY[0]),(uintptr_t)podatki.buf,podatki.len,0,(uintptr_t)&tarča,sizeof(tarča))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t Datoteka_ročica) {
    unsigned char podatki[512]; struct pk_sockaddr_in enakovreden_VALUE; pk_socklen_t 길이값 = sizeof(enakovreden_VALUE);
    intptr_t Velikost = 결과검사(사용자호출(35, mp_obj_get_int(Datoteka_ročica), (uintptr_t)podatki, 512, 0, (uintptr_t)&enakovreden_VALUE, (uintptr_t)&길이값));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(podatki, Velikost), MP_OBJ_NEW_SMALL_INT(pk_htons(enakovreden_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Zapri(mp_obj_t Datoteka_ročica) { 결과검사(사용자호출(4, mp_obj_get_int(Datoteka_ročica), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Zapri_OBJ, UDP_Zapri);
static mp_obj_t odprto_tok(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,oblak_Družina,tok_mreža,tok_protokol_prenosa,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,odprto_tok);
static mp_obj_t POVEŽI_tok(mp_obj_t končna_točka,mp_obj_t naslov_SMS,mp_obj_t INDEX) {
    int številka_vrat=mp_obj_get_int(INDEX); if(številka_vrat<1||številka_vrat>65535)mp_raise_OSError(MP_EINVAL);
    struct oblak_vtičnica_naslov naslov={0}; naslov.naslov_Družina=oblak_Družina;
    naslov.številka_vrat=망차례짧은수(številka_vrat); naslov.internetni_račun.naslov_VALUE=mreža_celo_število(인터넷주소읽기(naslov_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(končna_točka),(uintptr_t)&naslov,sizeof(naslov),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(tok_priključek_predmet,POVEŽI_tok);
static mp_obj_t 흐름읽기(mp_obj_t končna_točka,mp_obj_t 한도) {
    int 길이=mp_obj_get_int(한도); if(길이<1||길이>512)mp_raise_OSError(MP_EINVAL);
    unsigned char podatki[512];
    intptr_t element_COUNT=결과검사(사용자호출(2,mp_obj_get_int(končna_točka),(uintptr_t)podatki,길이,0,0,0));
    return mp_obj_new_bytes(podatki,element_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(tok_bralec_predmet,흐름읽기);
static mp_obj_t pisati_tok(mp_obj_t končna_točka,mp_obj_t vsebina_VALUE) {
    mp_buffer_info_t podatki; mp_get_buffer_raise(vsebina_VALUE,&podatki,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(končna_točka),(uintptr_t)podatki.buf,podatki.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(tok_Writer_predmet,pisati_tok);
static mp_obj_t 잠시기다리기(mp_obj_t čas_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(čas_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(počakaj_predmet,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Ime) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)pot_argument(Ime),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Ustvari_Imenik(mp_obj_t Ime) {
    결과검사(사용자호출(18,(uintptr_t)pot_argument(Ime),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Imenik_avtor_predmet,Ustvari_Imenik);
static mp_obj_t odstraniti_Imenik(mp_obj_t Ime) {
    결과검사(사용자호출(18,(uintptr_t)pot_argument(Ime),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,odstraniti_Imenik);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&tok_priključek_predmet) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&tok_bralec_predmet) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&tok_Writer_predmet) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&počakaj_predmet) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&Imenik_avtor_predmet) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&STDIN_bralec_predmet) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Datoteka_bralec_predmet) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Datoteka_Writer_predmet) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&pravokotnik_predmet) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Ura_predmet) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_odprto_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_poslati_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Zapri_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
