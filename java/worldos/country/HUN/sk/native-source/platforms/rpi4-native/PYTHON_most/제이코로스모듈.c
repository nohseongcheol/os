// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t KR) { if (KR < 0) mp_raise_OSError(-KR); return KR; }
static const char *cesta_argument(mp_obj_t VALUE) {
    size_t položka_COUNT; const char *Cesta = mp_obj_str_get_data(VALUE, &položka_COUNT);
    if (!položka_COUNT || položka_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < položka_COUNT; 순번++) if (!Cesta[순번]) mp_raise_OSError(MP_EINVAL);
    return Cesta;
}
static mp_obj_t 파일읽기(mp_obj_t Názov) {
    intptr_t Súbor_rukoväť = 결과검사(사용자호출(3, (uintptr_t)cesta_argument(Názov), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Veľkosť = 결과검사(사용자호출(9, Súbor_rukoväť, 0, 0, 0, 0, 0));
        vstr_t údaje; vstr_init_len(&údaje, Veľkosť);
        intptr_t KR = 사용자호출(2, Súbor_rukoväť, (uintptr_t)údaje.buf, Veľkosť, 0, 0, 0);
        결과검사(KR); údaje.len = KR;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&údaje);
        nlr_pop(); 사용자호출(4, Súbor_rukoväť, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, Súbor_rukoväť, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Súbor_Čítačka_objekt, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Veľkosť=mp_obj_get_int(한도);
    if(Veľkosť<0||Veľkosť>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t údaje; vstr_init_len(&údaje,Veľkosť);
    intptr_t položka_COUNT=사용자호출(2,0,(uintptr_t)údaje.buf,Veľkosť,0,0,0);
    if(položka_COUNT<0) { vstr_clear(&údaje); 결과검사(položka_COUNT); }
    údaje.len=položka_COUNT; return mp_obj_new_bytes_from_vstr(&údaje);
}
static MP_DEFINE_CONST_FUN_OBJ_1(STDIN_Čítačka_objekt, 표준입력읽기);
static mp_obj_t zapísať_Súbor(mp_obj_t Názov, mp_obj_t obsah_VALUE) {
    const char *Cesta = cesta_argument(Názov);
    mp_buffer_info_t údaje; mp_get_buffer_raise(obsah_VALUE, &údaje, MP_BUFFER_READ);
    if (údaje.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t Súbor_rukoväť = 결과검사(사용자호출(3, (uintptr_t)Cesta, 577, 0, 0, 0, 0));
    intptr_t položka_COUNT_8f7753a1 = 사용자호출(1, Súbor_rukoväť, (uintptr_t)údaje.buf, údaje.len, 0, 0, 0);
    사용자호출(4, Súbor_rukoväť, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(položka_COUNT_8f7753a1));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Súbor_Writer_objekt, zapísať_Súbor);
static mp_obj_t odobrať_Súbor(mp_obj_t Názov) { 결과검사(사용자호출(11, (uintptr_t)cesta_argument(Názov), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, odobrať_Súbor);
static mp_obj_t Skicár_obdĺžnik(size_t položka_COUNT, const mp_obj_t *argument_pole) {
    (void)položka_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argument_pole[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(obdĺžnik_objekt, 5, 5, Skicár_obdĺžnik);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Veľkosť[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Veľkosť);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Hodiny_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Hodiny_objekt, Hodiny_VALUE);
static mp_obj_t UDP_otvoriť(mp_obj_t číslo_portu) {
    int údaje_pozícia = mp_obj_get_int(číslo_portu); if (údaje_pozícia < 0 || údaje_pozícia > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t Súbor_rukoväť = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(údaje_pozícia); 첫째값.sin_addr.s_addr = 0;
    intptr_t KR = 사용자호출(33, Súbor_rukoväť, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (KR < 0) { 사용자호출(4, Súbor_rukoväť, 0, 0, 0, 0, 0); 결과검사(KR); }
    return mp_obj_new_int(Súbor_rukoväť);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_otvoriť_OBJ, UDP_otvoriť);
static mp_obj_t UDP_odoslať(mp_obj_t Súbor_rukoväť, mp_obj_t číslo_portu, mp_obj_t obsah_VALUE) {
    int údaje_pozícia = mp_obj_get_int(číslo_portu); if (údaje_pozícia < 1 || údaje_pozícia > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t údaje; mp_get_buffer_raise(obsah_VALUE, &údaje, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(údaje_pozícia); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(Súbor_rukoväť), (uintptr_t)údaje.buf, údaje.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_odoslať_OBJ, UDP_odoslať);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t dĺžka_VALUE; const char *Spracovanie_textu=mp_obj_str_get_data(VALUE,&dĺžka_VALUE);
    unsigned v_termíne_splatnosti_pozícia=0; uint32_t adresa=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,číslica_COUNT=0;
        while(v_termíne_splatnosti_pozícia<dĺžka_VALUE&&Spracovanie_textu[v_termíne_splatnosti_pozícia]>='0'&&Spracovanie_textu[v_termíne_splatnosti_pozícia]<='9') {
            VALUE=VALUE*10+Spracovanie_textu[v_termíne_splatnosti_pozícia++]-'0'; if(++číslica_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!číslica_COUNT)mp_raise_OSError(MP_EINVAL);
        adresa=adresa<<8|VALUE;
        if(부분<3&&(v_termíne_splatnosti_pozícia>=dĺžka_VALUE||Spracovanie_textu[v_termíne_splatnosti_pozícia++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(v_termíne_splatnosti_pozícia!=dĺžka_VALUE)mp_raise_OSError(MP_EINVAL);
    return adresa;
}
static mp_obj_t 전문주소전송(size_t položka_COUNT_8f7753a1, const mp_obj_t *argument_pole) {
    (void)položka_COUNT_8f7753a1; uint32_t adresa=인터넷주소읽기(argument_pole[1]);
    int číslo_portu=mp_obj_get_int(argument_pole[2]);if(číslo_portu<1||číslo_portu>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t údaje;mp_get_buffer_raise(argument_pole[3],&údaje,MP_BUFFER_READ);
    struct pk_sockaddr_in cieľová_hodnota={0};cieľová_hodnota.sin_family=AF_INET;cieľová_hodnota.sin_port=pk_htons(číslo_portu);cieľová_hodnota.sin_addr.s_addr=pk_htonl(adresa);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argument_pole[0]),(uintptr_t)údaje.buf,údaje.len,0,(uintptr_t)&cieľová_hodnota,sizeof(cieľová_hodnota))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t Súbor_rukoväť) {
    unsigned char údaje[512]; struct pk_sockaddr_in partnerský_uzol_VALUE; pk_socklen_t dĺžka_údaje = sizeof(partnerský_uzol_VALUE);
    intptr_t Veľkosť = 결과검사(사용자호출(35, mp_obj_get_int(Súbor_rukoväť), (uintptr_t)údaje, 512, 0, (uintptr_t)&partnerský_uzol_VALUE, (uintptr_t)&dĺžka_údaje));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(údaje, Veľkosť), MP_OBJ_NEW_SMALL_INT(pk_htons(partnerský_uzol_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Zavrieť(mp_obj_t Súbor_rukoväť) { 결과검사(사용자호출(4, mp_obj_get_int(Súbor_rukoväť), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Zavrieť_OBJ, UDP_Zavrieť);
static mp_obj_t otvoriť_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,cloud_séria,Stream_sieť,Stream_prenosový_protokol,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,otvoriť_Stream);
static mp_obj_t spojiť_Stream(mp_obj_t účastník,mp_obj_t adresa_SMS,mp_obj_t INDEX) {
    int číslo_portu=mp_obj_get_int(INDEX); if(číslo_portu<1||číslo_portu>65535)mp_raise_OSError(MP_EINVAL);
    struct cloud_soket_adresa adresa={0}; adresa.adresa_séria=cloud_séria;
    adresa.číslo_portu=망차례짧은수(číslo_portu); adresa.internetová_adresa.adresa_VALUE=sieť_celé_číslo(인터넷주소읽기(adresa_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(účastník),(uintptr_t)&adresa,sizeof(adresa),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_Spojnica_objekt,spojiť_Stream);
static mp_obj_t 흐름읽기(mp_obj_t účastník,mp_obj_t 한도) {
    int dĺžka_VALUE=mp_obj_get_int(한도); if(dĺžka_VALUE<1||dĺžka_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char údaje[512];
    intptr_t položka_COUNT=결과검사(사용자호출(2,mp_obj_get_int(účastník),(uintptr_t)údaje,dĺžka_VALUE,0,0,0));
    return mp_obj_new_bytes(údaje,položka_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Čítačka_objekt,흐름읽기);
static mp_obj_t zapísať_Stream(mp_obj_t účastník,mp_obj_t obsah_VALUE) {
    mp_buffer_info_t údaje; mp_get_buffer_raise(obsah_VALUE,&údaje,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(účastník),(uintptr_t)údaje.buf,údaje.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Writer_objekt,zapísať_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t čas_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(čas_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(počkaj_objekt,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Názov) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)cesta_argument(Názov),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Create_Adresár(mp_obj_t Názov) {
    결과검사(사용자호출(18,(uintptr_t)cesta_argument(Názov),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Adresár_autor_objekt,Create_Adresár);
static mp_obj_t odobrať_Adresár(mp_obj_t Názov) {
    결과검사(사용자호출(18,(uintptr_t)cesta_argument(Názov),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,odobrať_Adresár);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_Spojnica_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_Čítačka_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Writer_objekt) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&počkaj_objekt) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&Adresár_autor_objekt) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&STDIN_Čítačka_objekt) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Súbor_Čítačka_objekt) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Súbor_Writer_objekt) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&obdĺžnik_objekt) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Hodiny_objekt) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_otvoriť_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_odoslať_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Zavrieť_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
