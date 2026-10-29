// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t EMAITZA) { if (EMAITZA < 0) mp_raise_OSError(-EMAITZA); return EMAITZA; }
static const char *bide_izen_arg(mp_obj_t balio) {
    size_t elementu_ZENBATU; const char *Bide_izena = mp_obj_str_get_data(balio, &elementu_ZENBATU);
    if (!elementu_ZENBATU || elementu_ZENBATU > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < elementu_ZENBATU; 순번++) if (!Bide_izena[순번]) mp_raise_OSError(MP_EINVAL);
    return Bide_izena;
}
static mp_obj_t 파일읽기(mp_obj_t Izena) {
    intptr_t fitxategi_helduleku = 결과검사(사용자호출(3, (uintptr_t)bide_izen_arg(Izena), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Tamaina = 결과검사(사용자호출(9, fitxategi_helduleku, 0, 0, 0, 0, 0));
        vstr_t datuak; vstr_init_len(&datuak, Tamaina);
        intptr_t EMAITZA = 사용자호출(2, fitxategi_helduleku, (uintptr_t)datuak.buf, Tamaina, 0, 0, 0);
        결과검사(EMAITZA); datuak.len = EMAITZA;
        mp_obj_t balio = mp_obj_new_bytes_from_vstr(&datuak);
        nlr_pop(); 사용자호출(4, fitxategi_helduleku, 0, 0, 0, 0, 0); return balio;
    }
    사용자호출(4, fitxategi_helduleku, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(fitxategi_irakurle_objektu, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Tamaina=mp_obj_get_int(한도);
    if(Tamaina<0||Tamaina>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t datuak; vstr_init_len(&datuak,Tamaina);
    intptr_t elementu_ZENBATU=사용자호출(2,0,(uintptr_t)datuak.buf,Tamaina,0,0,0);
    if(elementu_ZENBATU<0) { vstr_clear(&datuak); 결과검사(elementu_ZENBATU); }
    datuak.len=elementu_ZENBATU; return mp_obj_new_bytes_from_vstr(&datuak);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t idatzi_fitxategi(mp_obj_t Izena, mp_obj_t eduki_balio) {
    const char *Bide_izena = bide_izen_arg(Izena);
    mp_buffer_info_t datuak; mp_get_buffer_raise(eduki_balio, &datuak, MP_BUFFER_READ);
    if (datuak.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t fitxategi_helduleku = 결과검사(사용자호출(3, (uintptr_t)Bide_izena, 577, 0, 0, 0, 0));
    intptr_t sarrera_ZENBATU = 사용자호출(1, fitxategi_helduleku, (uintptr_t)datuak.buf, datuak.len, 0, 0, 0);
    사용자호출(4, fitxategi_helduleku, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(sarrera_ZENBATU));
}
static MP_DEFINE_CONST_FUN_OBJ_2(fitxategi_Writer_objektu, idatzi_fitxategi);
static mp_obj_t kendu_fitxategi(mp_obj_t Izena) { 결과검사(사용자호출(11, (uintptr_t)bide_izen_arg(Izena), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, kendu_fitxategi);
static mp_obj_t 사각형그리기(size_t elementu_ZENBATU, const mp_obj_t *arg_matrize) {
    (void)elementu_ZENBATU; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(arg_matrize[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Tamaina[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Tamaina);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t erloju_balio(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(erloju_objektu, erloju_balio);
static mp_obj_t UDP_ireki(mp_obj_t ataka_zenbaki) {
    int datuak_kargu = mp_obj_get_int(ataka_zenbaki); if (datuak_kargu < 0 || datuak_kargu > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t fitxategi_helduleku = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(datuak_kargu); 첫째값.sin_addr.s_addr = 0;
    intptr_t EMAITZA = 사용자호출(33, fitxategi_helduleku, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (EMAITZA < 0) { 사용자호출(4, fitxategi_helduleku, 0, 0, 0, 0, 0); 결과검사(EMAITZA); }
    return mp_obj_new_int(fitxategi_helduleku);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_ireki_OBJ, UDP_ireki);
static mp_obj_t UDP_bidali(mp_obj_t fitxategi_helduleku, mp_obj_t ataka_zenbaki, mp_obj_t eduki_balio) {
    int datuak_kargu = mp_obj_get_int(ataka_zenbaki); if (datuak_kargu < 1 || datuak_kargu > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t datuak; mp_get_buffer_raise(eduki_balio, &datuak, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(datuak_kargu); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(fitxategi_helduleku), (uintptr_t)datuak.buf, datuak.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_bidali_OBJ, UDP_bidali);
static uint32_t 인터넷주소읽기(mp_obj_t balio) {
    size_t luzera_balio; const char *Testua=mp_obj_str_get_data(balio,&luzera_balio);
    unsigned 현재위치=0; uint32_t helbide=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned balio=0,digitu_ZENBATU=0;
        while(현재위치<luzera_balio&&Testua[현재위치]>='0'&&Testua[현재위치]<='9') {
            balio=balio*10+Testua[현재위치++]-'0'; if(++digitu_ZENBATU>3||balio>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!digitu_ZENBATU)mp_raise_OSError(MP_EINVAL);
        helbide=helbide<<8|balio;
        if(부분<3&&(현재위치>=luzera_balio||Testua[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=luzera_balio)mp_raise_OSError(MP_EINVAL);
    return helbide;
}
static mp_obj_t 전문주소전송(size_t sarrera_ZENBATU, const mp_obj_t *arg_matrize) {
    (void)sarrera_ZENBATU; uint32_t helbide=인터넷주소읽기(arg_matrize[1]);
    int ataka_zenbaki=mp_obj_get_int(arg_matrize[2]);if(ataka_zenbaki<1||ataka_zenbaki>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t datuak;mp_get_buffer_raise(arg_matrize[3],&datuak,MP_BUFFER_READ);
    struct pk_sockaddr_in helburu_balio={0};helburu_balio.sin_family=AF_INET;helburu_balio.sin_port=pk_htons(ataka_zenbaki);helburu_balio.sin_addr.s_addr=pk_htonl(helbide);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(arg_matrize[0]),(uintptr_t)datuak.buf,datuak.len,0,(uintptr_t)&helburu_balio,sizeof(helburu_balio))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t fitxategi_helduleku) {
    unsigned char datuak[512]; struct pk_sockaddr_in pareko_balio; pk_socklen_t luzera_datuak = sizeof(pareko_balio);
    intptr_t Tamaina = 결과검사(사용자호출(35, mp_obj_get_int(fitxategi_helduleku), (uintptr_t)datuak, 512, 0, (uintptr_t)&pareko_balio, (uintptr_t)&luzera_datuak));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(datuak, Tamaina), MP_OBJ_NEW_SMALL_INT(pk_htons(pareko_balio.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_itxi(mp_obj_t fitxategi_helduleku) { 결과검사(사용자호출(4, mp_obj_get_int(fitxategi_helduleku), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_itxi_OBJ, UDP_itxi);
static mp_obj_t ireki_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,hodei_sorta,Stream_sare,Stream_garraio_protokolo,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,ireki_Stream);
static mp_obj_t KONEKTATU_Stream(mp_obj_t amaiera_puntu,mp_obj_t helbide_SMS,mp_obj_t INDIZE) {
    int ataka_zenbaki=mp_obj_get_int(INDIZE); if(ataka_zenbaki<1||ataka_zenbaki>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 helbide={0}; helbide.helbide_sorta=hodei_sorta;
    helbide.ataka_zenbaki=망차례짧은수(ataka_zenbaki); helbide.Internet_helbide.helbide_balio=sare_osoko_zenbaki(인터넷주소읽기(helbide_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(amaiera_puntu),(uintptr_t)&helbide,sizeof(helbide),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_konektore_objektu,KONEKTATU_Stream);
static mp_obj_t 흐름읽기(mp_obj_t amaiera_puntu,mp_obj_t 한도) {
    int luzera_balio=mp_obj_get_int(한도); if(luzera_balio<1||luzera_balio>512)mp_raise_OSError(MP_EINVAL);
    unsigned char datuak[512];
    intptr_t elementu_ZENBATU=결과검사(사용자호출(2,mp_obj_get_int(amaiera_puntu),(uintptr_t)datuak,luzera_balio,0,0,0));
    return mp_obj_new_bytes(datuak,elementu_ZENBATU);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_irakurle_objektu,흐름읽기);
static mp_obj_t idatzi_Stream(mp_obj_t amaiera_puntu,mp_obj_t eduki_balio) {
    mp_buffer_info_t datuak; mp_get_buffer_raise(eduki_balio,&datuak,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(amaiera_puntu),(uintptr_t)datuak.buf,datuak.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Writer_objektu,idatzi_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t ordua_balio) {
    결과검사(사용자호출(17,mp_obj_get_int(ordua_balio),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(itxaron_objektu,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Izena) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)bide_izen_arg(Izena),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t sortu_direktorio(mp_obj_t Izena) {
    결과검사(사용자호출(18,(uintptr_t)bide_izen_arg(Izena),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(direktorio_sortzaile_objektu,sortu_direktorio);
static mp_obj_t kendu_direktorio(mp_obj_t Izena) {
    결과검사(사용자호출(18,(uintptr_t)bide_izen_arg(Izena),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,kendu_direktorio);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_konektore_objektu) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_irakurle_objektu) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Writer_objektu) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&itxaron_objektu) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&direktorio_sortzaile_objektu) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&fitxategi_irakurle_objektu) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&fitxategi_Writer_objektu) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&erloju_objektu) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_ireki_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_bidali_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_itxi_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
