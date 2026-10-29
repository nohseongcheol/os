// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t RESULTAT) { if (RESULTAT < 0) mp_raise_OSError(-RESULTAT); return RESULTAT; }
static const char *väg_argument(mp_obj_t värde) {
    size_t objekt_ANTAL; const char *sökväg_2 = mp_obj_str_get_data(värde, &objekt_ANTAL);
    if (!objekt_ANTAL || objekt_ANTAL > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < objekt_ANTAL; 순번++) if (!sökväg_2[순번]) mp_raise_OSError(MP_EINVAL);
    return sökväg_2;
}
static mp_obj_t läsa_fil(mp_obj_t Namn) {
    intptr_t filreferens = 결과검사(사용자호출(3, (uintptr_t)väg_argument(Namn), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Storlek = 결과검사(사용자호출(9, filreferens, 0, 0, 0, 0, 0));
        vstr_t data; vstr_init_len(&data, Storlek);
        intptr_t RESULTAT = 사용자호출(2, filreferens, (uintptr_t)data.buf, Storlek, 0, 0, 0);
        결과검사(RESULTAT); data.len = RESULTAT;
        mp_obj_t värde = mp_obj_new_bytes_from_vstr(&data);
        nlr_pop(); 사용자호출(4, filreferens, 0, 0, 0, 0, 0); return värde;
    }
    사용자호출(4, filreferens, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(fil_Läsare_objekt, läsa_fil);
static mp_obj_t läsa_Standard_indata(mp_obj_t 한도) {
    mp_int_t Storlek=mp_obj_get_int(한도);
    if(Storlek<0||Storlek>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t data; vstr_init_len(&data,Storlek);
    intptr_t objekt_ANTAL=사용자호출(2,0,(uintptr_t)data.buf,Storlek,0,0,0);
    if(objekt_ANTAL<0) { vstr_clear(&data); 결과검사(objekt_ANTAL); }
    data.len=objekt_ANTAL; return mp_obj_new_bytes_from_vstr(&data);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Standard_indata_Läsare_objekt, läsa_Standard_indata);
static mp_obj_t skriva_fil(mp_obj_t Namn, mp_obj_t Innehåll_värde) {
    const char *sökväg_2 = väg_argument(Namn);
    mp_buffer_info_t data; mp_get_buffer_raise(Innehåll_värde, &data, MP_BUFFER_READ);
    if (data.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t filreferens = 결과검사(사용자호출(3, (uintptr_t)sökväg_2, 577, 0, 0, 0, 0));
    intptr_t post_ANTAL = 사용자호출(1, filreferens, (uintptr_t)data.buf, data.len, 0, 0, 0);
    사용자호출(4, filreferens, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(post_ANTAL));
}
static MP_DEFINE_CONST_FUN_OBJ_2(fil_Writer_objekt, skriva_fil);
static mp_obj_t ta_bort_fil(mp_obj_t Namn) { 결과검사(사용자호출(11, (uintptr_t)väg_argument(Namn), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, ta_bort_fil);
static mp_obj_t Paint_rektangel(size_t objekt_ANTAL, const mp_obj_t *argument_MATRIS) {
    (void)objekt_ANTAL; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argument_MATRIS[순번]);
    결과검사(skärmbild_rektangel(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(rektangel_objekt, 5, 5, Paint_rektangel);
static mp_obj_t läsa_skärmbild_storlek(void) {
    mp_obj_t Storlek[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Storlek);
}
static MP_DEFINE_CONST_FUN_OBJ_0(skärmbild_storlek_objekt, läsa_skärmbild_storlek);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(skärmbild_vänta_objekt, 화면입력기다리기);
static mp_obj_t Klocka_värde(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Klocka_objekt, Klocka_värde);
static mp_obj_t UDP_skapa(mp_obj_t portnummer) {
    int data_placera = mp_obj_get_int(portnummer); if (data_placera < 0 || data_placera > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t filreferens = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_placera); 첫째값.sin_addr.s_addr = 0;
    intptr_t RESULTAT = 사용자호출(33, filreferens, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (RESULTAT < 0) { 사용자호출(4, filreferens, 0, 0, 0, 0, 0); 결과검사(RESULTAT); }
    return mp_obj_new_int(filreferens);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_skapa_OBJ, UDP_skapa);
static mp_obj_t UDP_skicka(mp_obj_t filreferens, mp_obj_t portnummer, mp_obj_t Innehåll_värde) {
    int data_placera = mp_obj_get_int(portnummer); if (data_placera < 1 || data_placera > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data; mp_get_buffer_raise(Innehåll_värde, &data, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_placera); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(filreferens), (uintptr_t)data.buf, data.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_skicka_OBJ, UDP_skicka);
static uint32_t läsa_Internetadress(mp_obj_t värde) {
    size_t längd_värde; const char *text=mp_obj_str_get_data(värde,&längd_värde);
    unsigned aktuellt_placera=0; uint32_t Adress=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned värde=0,siffra_ANTAL=0;
        while(aktuellt_placera<längd_värde&&text[aktuellt_placera]>='0'&&text[aktuellt_placera]<='9') {
            värde=värde*10+text[aktuellt_placera++]-'0'; if(++siffra_ANTAL>3||värde>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!siffra_ANTAL)mp_raise_OSError(MP_EINVAL);
        Adress=Adress<<8|värde;
        if(부분<3&&(aktuellt_placera>=längd_värde||text[aktuellt_placera++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(aktuellt_placera!=längd_värde)mp_raise_OSError(MP_EINVAL);
    return Adress;
}
static mp_obj_t 전문주소전송(size_t post_ANTAL, const mp_obj_t *argument_MATRIS) {
    (void)post_ANTAL; uint32_t Adress=läsa_Internetadress(argument_MATRIS[1]);
    int portnummer=mp_obj_get_int(argument_MATRIS[2]);if(portnummer<1||portnummer>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data;mp_get_buffer_raise(argument_MATRIS[3],&data,MP_BUFFER_READ);
    struct pk_sockaddr_in mål={0};mål.sin_family=AF_INET;mål.sin_port=pk_htons(portnummer);mål.sin_addr.s_addr=pk_htonl(Adress);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argument_MATRIS[0]),(uintptr_t)data.buf,data.len,0,(uintptr_t)&mål,sizeof(mål))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t filreferens) {
    unsigned char data[512]; struct pk_sockaddr_in peer_värde; pk_socklen_t längd_data = sizeof(peer_värde);
    intptr_t Storlek = 결과검사(사용자호출(35, mp_obj_get_int(filreferens), (uintptr_t)data, 512, 0, (uintptr_t)&peer_värde, (uintptr_t)&längd_data));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(data, Storlek), MP_OBJ_NEW_SMALL_INT(pk_htons(peer_värde.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Stäng(mp_obj_t filreferens) { 결과검사(사용자호출(4, mp_obj_get_int(filreferens), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Stäng_OBJ, UDP_Stäng);
static mp_obj_t skapa_flöde(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,nät_serie,flöde_nätverk,flöde_transportprotokoll,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,skapa_flöde);
static mp_obj_t ANSLUT_flöde(mp_obj_t deltagare,mp_obj_t ADRESS_SMS,mp_obj_t INDEX) {
    int portnummer=mp_obj_get_int(INDEX); if(portnummer<1||portnummer>65535)mp_raise_OSError(MP_EINVAL);
    struct nät_socket_ADRESS Adress={0}; Adress.ADRESS_serie=nät_serie;
    Adress.portnummer=망차례짧은수(portnummer); Adress.Internetadress.ADRESS_värde=nätverk_heltal(läsa_Internetadress(ADRESS_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(deltagare),(uintptr_t)&Adress,sizeof(Adress),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(flöde_Koppling_objekt,ANSLUT_flöde);
static mp_obj_t läsa_flöde(mp_obj_t deltagare,mp_obj_t 한도) {
    int längd_värde=mp_obj_get_int(한도); if(längd_värde<1||längd_värde>512)mp_raise_OSError(MP_EINVAL);
    unsigned char data[512];
    intptr_t objekt_ANTAL=결과검사(사용자호출(2,mp_obj_get_int(deltagare),(uintptr_t)data,längd_värde,0,0,0));
    return mp_obj_new_bytes(data,objekt_ANTAL);
}
static MP_DEFINE_CONST_FUN_OBJ_2(flöde_Läsare_objekt,läsa_flöde);
static mp_obj_t skriva_flöde(mp_obj_t deltagare,mp_obj_t Innehåll_värde) {
    mp_buffer_info_t data; mp_get_buffer_raise(Innehåll_värde,&data,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(deltagare),(uintptr_t)data.buf,data.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(flöde_Writer_objekt,skriva_flöde);
static mp_obj_t 잠시기다리기(mp_obj_t tid_värde) {
    결과검사(사용자호출(17,mp_obj_get_int(tid_värde),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(vänta_objekt,잠시기다리기);
static mp_obj_t post_variant(mp_obj_t Namn) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)väg_argument(Namn),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(post_variant_objekt,post_variant);
static mp_obj_t Skapa_Katalog(mp_obj_t Namn) {
    결과검사(사용자호출(18,(uintptr_t)väg_argument(Namn),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Katalog_Skapare_objekt,Skapa_Katalog);
static mp_obj_t ta_bort_Katalog(mp_obj_t Namn) {
    결과검사(사용자호출(18,(uintptr_t)väg_argument(Namn),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,ta_bort_Katalog);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&flöde_Koppling_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&flöde_Läsare_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&flöde_Writer_objekt) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&vänta_objekt) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&post_variant_objekt) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&Katalog_Skapare_objekt) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&Standard_indata_Läsare_objekt) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&fil_Läsare_objekt) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&fil_Writer_objekt) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&rektangel_objekt) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&skärmbild_storlek_objekt) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&skärmbild_vänta_objekt) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Klocka_objekt) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_skapa_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_skicka_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Stäng_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
