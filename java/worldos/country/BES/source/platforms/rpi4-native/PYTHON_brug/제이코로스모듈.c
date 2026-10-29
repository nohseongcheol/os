// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t resultaat) { if (resultaat < 0) mp_raise_OSError(-resultaat); return resultaat; }
static const char *pad_argument(mp_obj_t WAARDE) {
    size_t item_AANTAL; const char *pad = mp_obj_str_get_data(WAARDE, &item_AANTAL);
    if (!item_AANTAL || item_AANTAL > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < item_AANTAL; 순번++) if (!pad[순번]) mp_raise_OSError(MP_EINVAL);
    return pad;
}
static mp_obj_t 파일읽기(mp_obj_t Naam) {
    intptr_t bestandsingang = 결과검사(사용자호출(3, (uintptr_t)pad_argument(Naam), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Grootte = 결과검사(사용자호출(9, bestandsingang, 0, 0, 0, 0, 0));
        vstr_t gegevens; vstr_init_len(&gegevens, Grootte);
        intptr_t resultaat = 사용자호출(2, bestandsingang, (uintptr_t)gegevens.buf, Grootte, 0, 0, 0);
        결과검사(resultaat); gegevens.len = resultaat;
        mp_obj_t WAARDE = mp_obj_new_bytes_from_vstr(&gegevens);
        nlr_pop(); 사용자호출(4, bestandsingang, 0, 0, 0, 0, 0); return WAARDE;
    }
    사용자호출(4, bestandsingang, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Bestand_Lezer_object, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Grootte=mp_obj_get_int(한도);
    if(Grootte<0||Grootte>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t gegevens; vstr_init_len(&gegevens,Grootte);
    intptr_t item_AANTAL=사용자호출(2,0,(uintptr_t)gegevens.buf,Grootte,0,0,0);
    if(item_AANTAL<0) { vstr_clear(&gegevens); 결과검사(item_AANTAL); }
    gegevens.len=item_AANTAL; return mp_obj_new_bytes_from_vstr(&gegevens);
}
static MP_DEFINE_CONST_FUN_OBJ_1(STDIN_Lezer_object, 표준입력읽기);
static mp_obj_t schrijven_Bestand(mp_obj_t Naam, mp_obj_t Inhoud_WAARDE) {
    const char *pad = pad_argument(Naam);
    mp_buffer_info_t gegevens; mp_get_buffer_raise(Inhoud_WAARDE, &gegevens, MP_BUFFER_READ);
    if (gegevens.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t bestandsingang = 결과검사(사용자호출(3, (uintptr_t)pad, 577, 0, 0, 0, 0));
    intptr_t invoer_AANTAL_8f7753a1 = 사용자호출(1, bestandsingang, (uintptr_t)gegevens.buf, gegevens.len, 0, 0, 0);
    사용자호출(4, bestandsingang, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(invoer_AANTAL_8f7753a1));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Bestand_Schrijver_object, schrijven_Bestand);
static mp_obj_t verwijderen_Bestand(mp_obj_t Naam) { 결과검사(사용자호출(11, (uintptr_t)pad_argument(Naam), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, verwijderen_Bestand);
static mp_obj_t Paint_rechthoek(size_t item_AANTAL, const mp_obj_t *argument_MATRIX) {
    (void)item_AANTAL; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argument_MATRIX[순번]);
    결과검사(scherm_rechthoek(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(rechthoek_object, 5, 5, Paint_rechthoek);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Grootte[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Grootte);
}
static MP_DEFINE_CONST_FUN_OBJ_0(scherm_formaat_wijzigen_object, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(scherm_wachten_object, 화면입력기다리기);
static mp_obj_t Klok_WAARDE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Klok_object, Klok_WAARDE);
static mp_obj_t UDP_open(mp_obj_t poortnummer) {
    int gegevens_functie = mp_obj_get_int(poortnummer); if (gegevens_functie < 0 || gegevens_functie > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t bestandsingang = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(gegevens_functie); 첫째값.sin_addr.s_addr = 0;
    intptr_t resultaat = 사용자호출(33, bestandsingang, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (resultaat < 0) { 사용자호출(4, bestandsingang, 0, 0, 0, 0, 0); 결과검사(resultaat); }
    return mp_obj_new_int(bestandsingang);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_open_OBJ, UDP_open);
static mp_obj_t UDP_e_mailen(mp_obj_t bestandsingang, mp_obj_t poortnummer, mp_obj_t Inhoud_WAARDE) {
    int gegevens_functie = mp_obj_get_int(poortnummer); if (gegevens_functie < 1 || gegevens_functie > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t gegevens; mp_get_buffer_raise(Inhoud_WAARDE, &gegevens, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(gegevens_functie); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(bestandsingang), (uintptr_t)gegevens.buf, gegevens.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_e_mailen_OBJ, UDP_e_mailen);
static uint32_t 인터넷주소읽기(mp_obj_t WAARDE) {
    size_t tijdsduur_WAARDE; const char *tekst=mp_obj_str_get_data(WAARDE,&tijdsduur_WAARDE);
    unsigned actueel_functie=0; uint32_t ADRES=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned WAARDE=0,cijfer_AANTAL=0;
        while(actueel_functie<tijdsduur_WAARDE&&tekst[actueel_functie]>='0'&&tekst[actueel_functie]<='9') {
            WAARDE=WAARDE*10+tekst[actueel_functie++]-'0'; if(++cijfer_AANTAL>3||WAARDE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!cijfer_AANTAL)mp_raise_OSError(MP_EINVAL);
        ADRES=ADRES<<8|WAARDE;
        if(부분<3&&(actueel_functie>=tijdsduur_WAARDE||tekst[actueel_functie++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(actueel_functie!=tijdsduur_WAARDE)mp_raise_OSError(MP_EINVAL);
    return ADRES;
}
static mp_obj_t 전문주소전송(size_t invoer_AANTAL_8f7753a1, const mp_obj_t *argument_MATRIX) {
    (void)invoer_AANTAL_8f7753a1; uint32_t ADRES=인터넷주소읽기(argument_MATRIX[1]);
    int poortnummer=mp_obj_get_int(argument_MATRIX[2]);if(poortnummer<1||poortnummer>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t gegevens;mp_get_buffer_raise(argument_MATRIX[3],&gegevens,MP_BUFFER_READ);
    struct pk_sockaddr_in doel={0};doel.sin_family=AF_INET;doel.sin_port=pk_htons(poortnummer);doel.sin_addr.s_addr=pk_htonl(ADRES);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argument_MATRIX[0]),(uintptr_t)gegevens.buf,gegevens.len,0,(uintptr_t)&doel,sizeof(doel))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t bestandsingang) {
    unsigned char gegevens[512]; struct pk_sockaddr_in peer_WAARDE; pk_socklen_t tijdsduur_gegevens = sizeof(peer_WAARDE);
    intptr_t Grootte = 결과검사(사용자호출(35, mp_obj_get_int(bestandsingang), (uintptr_t)gegevens, 512, 0, (uintptr_t)&peer_WAARDE, (uintptr_t)&tijdsduur_gegevens));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(gegevens, Grootte), MP_OBJ_NEW_SMALL_INT(pk_htons(peer_WAARDE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Sluiten(mp_obj_t bestandsingang) { 결과검사(사용자호출(4, mp_obj_get_int(bestandsingang), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Sluiten_OBJ, UDP_Sluiten);
static mp_obj_t open_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,mesh_Gezin,Stream_net,Stream_transportprotocol,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,open_Stream);
static mp_obj_t VERBINDEN_Stream(mp_obj_t eindpunt,mp_obj_t ADRES_sms,mp_obj_t INDEX) {
    int poortnummer=mp_obj_get_int(INDEX); if(poortnummer<1||poortnummer>65535)mp_raise_OSError(MP_EINVAL);
    struct mesh_socket_ADRES ADRES={0}; ADRES.ADRES_Gezin=mesh_Gezin;
    ADRES.poortnummer=망차례짧은수(poortnummer); ADRES.internetadres.ADRES_WAARDE=net_geheel_getal(인터넷주소읽기(ADRES_sms));
    결과검사(사용자호출(37,mp_obj_get_int(eindpunt),(uintptr_t)&ADRES,sizeof(ADRES),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_connector_object,VERBINDEN_Stream);
static mp_obj_t 흐름읽기(mp_obj_t eindpunt,mp_obj_t 한도) {
    int tijdsduur_WAARDE=mp_obj_get_int(한도); if(tijdsduur_WAARDE<1||tijdsduur_WAARDE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char gegevens[512];
    intptr_t item_AANTAL=결과검사(사용자호출(2,mp_obj_get_int(eindpunt),(uintptr_t)gegevens,tijdsduur_WAARDE,0,0,0));
    return mp_obj_new_bytes(gegevens,item_AANTAL);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Lezer_object,흐름읽기);
static mp_obj_t schrijven_Stream(mp_obj_t eindpunt,mp_obj_t Inhoud_WAARDE) {
    mp_buffer_info_t gegevens; mp_get_buffer_raise(Inhoud_WAARDE,&gegevens,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(eindpunt),(uintptr_t)gegevens.buf,gegevens.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Schrijver_object,schrijven_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t TIJD_WAARDE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIJD_WAARDE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(wachten_object,잠시기다리기);
static mp_obj_t invoer_soort(mp_obj_t Naam) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)pad_argument(Naam),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(invoer_soort_object,invoer_soort);
static mp_obj_t maken_map(mp_obj_t Naam) {
    결과검사(사용자호출(18,(uintptr_t)pad_argument(Naam),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(map_maker_object,maken_map);
static mp_obj_t verwijderen_map(mp_obj_t Naam) {
    결과검사(사용자호출(18,(uintptr_t)pad_argument(Naam),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,verwijderen_map);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_connector_object) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_Lezer_object) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Schrijver_object) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&wachten_object) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&invoer_soort_object) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&map_maker_object) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&STDIN_Lezer_object) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Bestand_Lezer_object) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Bestand_Schrijver_object) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&rechthoek_object) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&scherm_formaat_wijzigen_object) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&scherm_wachten_object) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Klok_object) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_open_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_e_mailen_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Sluiten_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
