// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "síť_ABI.h"
static intptr_t 결과검사(intptr_t VÝSLEDEK) { if (VÝSLEDEK < 0) mp_raise_OSError(-VÝSLEDEK); return VÝSLEDEK; }
static const char *cesta_argument(mp_obj_t HODNOTA) {
    size_t zboží_POČET; const char *cesta_2 = mp_obj_str_get_data(HODNOTA, &zboží_POČET);
    if (!zboží_POČET || zboží_POČET > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < zboží_POČET; 순번++) if (!cesta_2[순번]) mp_raise_OSError(MP_EINVAL);
    return cesta_2;
}
static mp_obj_t 파일읽기(mp_obj_t Název) {
    intptr_t popisovač_souboru = 결과검사(사용자호출(3, (uintptr_t)cesta_argument(Název), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Velikost = 결과검사(사용자호출(9, popisovač_souboru, 0, 0, 0, 0, 0));
        vstr_t data; vstr_init_len(&data, Velikost);
        intptr_t VÝSLEDEK = 사용자호출(2, popisovač_souboru, (uintptr_t)data.buf, Velikost, 0, 0, 0);
        결과검사(VÝSLEDEK); data.len = VÝSLEDEK;
        mp_obj_t HODNOTA = mp_obj_new_bytes_from_vstr(&data);
        nlr_pop(); 사용자호출(4, popisovač_souboru, 0, 0, 0, 0, 0); return HODNOTA;
    }
    사용자호출(4, popisovač_souboru, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Soubor_Čtenář_objekt, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Velikost=mp_obj_get_int(한도);
    if(Velikost<0||Velikost>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t data; vstr_init_len(&data,Velikost);
    intptr_t zboží_POČET=사용자호출(2,0,(uintptr_t)data.buf,Velikost,0,0,0);
    if(zboží_POČET<0) { vstr_clear(&data); 결과검사(zboží_POČET); }
    data.len=zboží_POČET; return mp_obj_new_bytes_from_vstr(&data);
}
static MP_DEFINE_CONST_FUN_OBJ_1(zařízení_STDIN_Čtenář_objekt, 표준입력읽기);
static mp_obj_t zápis_Soubor(mp_obj_t Název, mp_obj_t Obsah_HODNOTA) {
    const char *cesta_2 = cesta_argument(Název);
    mp_buffer_info_t data; mp_get_buffer_raise(Obsah_HODNOTA, &data, MP_BUFFER_READ);
    if (data.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t popisovač_souboru = 결과검사(사용자호출(3, (uintptr_t)cesta_2, 577, 0, 0, 0, 0));
    intptr_t položka_POČET = 사용자호출(1, popisovač_souboru, (uintptr_t)data.buf, data.len, 0, 0, 0);
    사용자호출(4, popisovač_souboru, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(položka_POČET));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Soubor_Writer_objekt, zápis_Soubor);
static mp_obj_t odebrat_Soubor(mp_obj_t Název) { 결과검사(사용자호출(11, (uintptr_t)cesta_argument(Název), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, odebrat_Soubor);
static mp_obj_t Malování_obdélník(size_t zboží_POČET, const mp_obj_t *argument_pole) {
    (void)zboží_POČET; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argument_pole[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(obdélník_objekt, 5, 5, Malování_obdélník);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Velikost[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Velikost);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Hodiny_HODNOTA(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Hodiny_objekt, Hodiny_HODNOTA);
static mp_obj_t protokol_UDP_otevřít(mp_obj_t číslo_portu) {
    int data_pozice = mp_obj_get_int(číslo_portu); if (data_pozice < 0 || data_pozice > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t popisovač_souboru = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_pozice); 첫째값.sin_addr.s_addr = 0;
    intptr_t VÝSLEDEK = 사용자호출(33, popisovač_souboru, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (VÝSLEDEK < 0) { 사용자호출(4, popisovač_souboru, 0, 0, 0, 0, 0); 결과검사(VÝSLEDEK); }
    return mp_obj_new_int(popisovač_souboru);
}
static MP_DEFINE_CONST_FUN_OBJ_1(protokol_UDP_otevřít_OBJ, protokol_UDP_otevřít);
static mp_obj_t protokol_UDP_poslat(mp_obj_t popisovač_souboru, mp_obj_t číslo_portu, mp_obj_t Obsah_HODNOTA) {
    int data_pozice = mp_obj_get_int(číslo_portu); if (data_pozice < 1 || data_pozice > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data; mp_get_buffer_raise(Obsah_HODNOTA, &data, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_pozice); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(popisovač_souboru), (uintptr_t)data.buf, data.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(protokol_UDP_poslat_OBJ, protokol_UDP_poslat);
static uint32_t 인터넷주소읽기(mp_obj_t HODNOTA) {
    size_t délka_HODNOTA; const char *text=mp_obj_str_get_data(HODNOTA,&délka_HODNOTA);
    unsigned dobrá_pozice=0; uint32_t Adresa=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned HODNOTA=0,číslice_POČET=0;
        while(dobrá_pozice<délka_HODNOTA&&text[dobrá_pozice]>='0'&&text[dobrá_pozice]<='9') {
            HODNOTA=HODNOTA*10+text[dobrá_pozice++]-'0'; if(++číslice_POČET>3||HODNOTA>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!číslice_POČET)mp_raise_OSError(MP_EINVAL);
        Adresa=Adresa<<8|HODNOTA;
        if(부분<3&&(dobrá_pozice>=délka_HODNOTA||text[dobrá_pozice++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(dobrá_pozice!=délka_HODNOTA)mp_raise_OSError(MP_EINVAL);
    return Adresa;
}
static mp_obj_t 전문주소전송(size_t položka_POČET, const mp_obj_t *argument_pole) {
    (void)položka_POČET; uint32_t Adresa=인터넷주소읽기(argument_pole[1]);
    int číslo_portu=mp_obj_get_int(argument_pole[2]);if(číslo_portu<1||číslo_portu>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data;mp_get_buffer_raise(argument_pole[3],&data,MP_BUFFER_READ);
    struct pk_sockaddr_in cílová_úroveň={0};cílová_úroveň.sin_family=AF_INET;cílová_úroveň.sin_port=pk_htons(číslo_portu);cílová_úroveň.sin_addr.s_addr=pk_htonl(Adresa);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argument_pole[0]),(uintptr_t)data.buf,data.len,0,(uintptr_t)&cílová_úroveň,sizeof(cílová_úroveň))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t popisovač_souboru) {
    unsigned char data[512]; struct pk_sockaddr_in partner_HODNOTA; pk_socklen_t délka_data = sizeof(partner_HODNOTA);
    intptr_t Velikost = 결과검사(사용자호출(35, mp_obj_get_int(popisovač_souboru), (uintptr_t)data, 512, 0, (uintptr_t)&partner_HODNOTA, (uintptr_t)&délka_data));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(data, Velikost), MP_OBJ_NEW_SMALL_INT(pk_htons(partner_HODNOTA.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t protokol_UDP_Zavřít(mp_obj_t popisovač_souboru) { 결과검사(사용자호출(4, mp_obj_get_int(popisovač_souboru), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(protokol_UDP_Zavřít_OBJ, protokol_UDP_Zavřít);
static mp_obj_t otevřít_tok(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,cloud_řada,tok_síť,tok_transportní_protokol,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,otevřít_tok);
static mp_obj_t spojit_tok(mp_obj_t účastník,mp_obj_t ODKAZ_SMS,mp_obj_t INDEX) {
    int číslo_portu=mp_obj_get_int(INDEX); if(číslo_portu<1||číslo_portu>65535)mp_raise_OSError(MP_EINVAL);
    struct cloud_soket_ODKAZ Adresa={0}; Adresa.ODKAZ_řada=cloud_řada;
    Adresa.číslo_portu=망차례짧은수(číslo_portu); Adresa.internetová_adresa.ODKAZ_HODNOTA=síť_integer(인터넷주소읽기(ODKAZ_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(účastník),(uintptr_t)&Adresa,sizeof(Adresa),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(tok_Spojnice_objekt,spojit_tok);
static mp_obj_t 흐름읽기(mp_obj_t účastník,mp_obj_t 한도) {
    int délka_HODNOTA=mp_obj_get_int(한도); if(délka_HODNOTA<1||délka_HODNOTA>512)mp_raise_OSError(MP_EINVAL);
    unsigned char data[512];
    intptr_t zboží_POČET=결과검사(사용자호출(2,mp_obj_get_int(účastník),(uintptr_t)data,délka_HODNOTA,0,0,0));
    return mp_obj_new_bytes(data,zboží_POČET);
}
static MP_DEFINE_CONST_FUN_OBJ_2(tok_Čtenář_objekt,흐름읽기);
static mp_obj_t zápis_tok(mp_obj_t účastník,mp_obj_t Obsah_HODNOTA) {
    mp_buffer_info_t data; mp_get_buffer_raise(Obsah_HODNOTA,&data,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(účastník),(uintptr_t)data.buf,data.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(tok_Writer_objekt,zápis_tok);
static mp_obj_t 잠시기다리기(mp_obj_t časová_hodnota) {
    결과검사(사용자호출(17,mp_obj_get_int(časová_hodnota),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(počkej_objekt,잠시기다리기);
static mp_obj_t položka_Druh(mp_obj_t Název) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)cesta_argument(Název),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(položka_Druh_objekt,položka_Druh);
static mp_obj_t Create_Adresář(mp_obj_t Název) {
    결과검사(사용자호출(18,(uintptr_t)cesta_argument(Název),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Adresář_autor_objekt,Create_Adresář);
static mp_obj_t odebrat_Adresář(mp_obj_t Název) {
    결과검사(사용자호출(18,(uintptr_t)cesta_argument(Název),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,odebrat_Adresář);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&tok_Spojnice_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&tok_Čtenář_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&tok_Writer_objekt) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&počkej_objekt) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&položka_Druh_objekt) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&Adresář_autor_objekt) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&zařízení_STDIN_Čtenář_objekt) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Soubor_Čtenář_objekt) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Soubor_Writer_objekt) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&obdélník_objekt) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Hodiny_objekt) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&protokol_UDP_otevřít_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&protokol_UDP_poslat_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&protokol_UDP_Zavřít_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
