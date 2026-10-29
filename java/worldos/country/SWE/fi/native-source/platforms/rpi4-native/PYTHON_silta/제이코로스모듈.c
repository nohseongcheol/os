// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t TULOS) { if (TULOS < 0) mp_raise_OSError(-TULOS); return TULOS; }
static const char *polku_argumentti(mp_obj_t ARVO) {
    size_t kohde_LASKE; const char *polku_2 = mp_obj_str_get_data(ARVO, &kohde_LASKE);
    if (!kohde_LASKE || kohde_LASKE > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < kohde_LASKE; 순번++) if (!polku_2[순번]) mp_raise_OSError(MP_EINVAL);
    return polku_2;
}
static mp_obj_t lukea_Tiedosto(mp_obj_t Nimi) {
    intptr_t Tiedosto_kahva = 결과검사(사용자호출(3, (uintptr_t)polku_argumentti(Nimi), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Koko = 결과검사(사용자호출(9, Tiedosto_kahva, 0, 0, 0, 0, 0));
        vstr_t data; vstr_init_len(&data, Koko);
        intptr_t TULOS = 사용자호출(2, Tiedosto_kahva, (uintptr_t)data.buf, Koko, 0, 0, 0);
        결과검사(TULOS); data.len = TULOS;
        mp_obj_t ARVO = mp_obj_new_bytes_from_vstr(&data);
        nlr_pop(); 사용자호출(4, Tiedosto_kahva, 0, 0, 0, 0, 0); return ARVO;
    }
    사용자호출(4, Tiedosto_kahva, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Tiedosto_Lukija_objekti, lukea_Tiedosto);
static mp_obj_t lukea_STDIN(mp_obj_t 한도) {
    mp_int_t Koko=mp_obj_get_int(한도);
    if(Koko<0||Koko>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t data; vstr_init_len(&data,Koko);
    intptr_t kohde_LASKE=사용자호출(2,0,(uintptr_t)data.buf,Koko,0,0,0);
    if(kohde_LASKE<0) { vstr_clear(&data); 결과검사(kohde_LASKE); }
    data.len=kohde_LASKE; return mp_obj_new_bytes_from_vstr(&data);
}
static MP_DEFINE_CONST_FUN_OBJ_1(STDIN_Lukija_objekti, lukea_STDIN);
static mp_obj_t kirjoitus_Tiedosto(mp_obj_t Nimi, mp_obj_t Sisältö_ARVO) {
    const char *polku_2 = polku_argumentti(Nimi);
    mp_buffer_info_t data; mp_get_buffer_raise(Sisältö_ARVO, &data, MP_BUFFER_READ);
    if (data.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t Tiedosto_kahva = 결과검사(사용자호출(3, (uintptr_t)polku_2, 577, 0, 0, 0, 0));
    intptr_t merkintä_LASKE = 사용자호출(1, Tiedosto_kahva, (uintptr_t)data.buf, data.len, 0, 0, 0);
    사용자호출(4, Tiedosto_kahva, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(merkintä_LASKE));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Tiedosto_Writer_objekti, kirjoitus_Tiedosto);
static mp_obj_t poistaa_Tiedosto(mp_obj_t Nimi) { 결과검사(사용자호출(11, (uintptr_t)polku_argumentti(Nimi), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, poistaa_Tiedosto);
static mp_obj_t Paint_suorakulmio(size_t kohde_LASKE, const mp_obj_t *argumentti_MATRIISI) {
    (void)kohde_LASKE; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argumentti_MATRIISI[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(suorakulmio_objekti, 5, 5, Paint_suorakulmio);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Koko[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Koko);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Kello_ARVO(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Kello_objekti, Kello_ARVO);
static mp_obj_t UDP_avata(mp_obj_t portin_numero) {
    int data_toimi = mp_obj_get_int(portin_numero); if (data_toimi < 0 || data_toimi > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t Tiedosto_kahva = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_toimi); 첫째값.sin_addr.s_addr = 0;
    intptr_t TULOS = 사용자호출(33, Tiedosto_kahva, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (TULOS < 0) { 사용자호출(4, Tiedosto_kahva, 0, 0, 0, 0, 0); 결과검사(TULOS); }
    return mp_obj_new_int(Tiedosto_kahva);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_avata_OBJ, UDP_avata);
static mp_obj_t UDP_lähettää(mp_obj_t Tiedosto_kahva, mp_obj_t portin_numero, mp_obj_t Sisältö_ARVO) {
    int data_toimi = mp_obj_get_int(portin_numero); if (data_toimi < 1 || data_toimi > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data; mp_get_buffer_raise(Sisältö_ARVO, &data, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_toimi); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(Tiedosto_kahva), (uintptr_t)data.buf, data.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_lähettää_OBJ, UDP_lähettää);
static uint32_t lukea_Internet_osoite(mp_obj_t ARVO) {
    size_t kesto_ARVO; const char *teksti=mp_obj_str_get_data(ARVO,&kesto_ARVO);
    unsigned nykyinen_toimi=0; uint32_t OSOITE=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned ARVO=0,numero_LASKE=0;
        while(nykyinen_toimi<kesto_ARVO&&teksti[nykyinen_toimi]>='0'&&teksti[nykyinen_toimi]<='9') {
            ARVO=ARVO*10+teksti[nykyinen_toimi++]-'0'; if(++numero_LASKE>3||ARVO>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!numero_LASKE)mp_raise_OSError(MP_EINVAL);
        OSOITE=OSOITE<<8|ARVO;
        if(부분<3&&(nykyinen_toimi>=kesto_ARVO||teksti[nykyinen_toimi++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(nykyinen_toimi!=kesto_ARVO)mp_raise_OSError(MP_EINVAL);
    return OSOITE;
}
static mp_obj_t 전문주소전송(size_t merkintä_LASKE, const mp_obj_t *argumentti_MATRIISI) {
    (void)merkintä_LASKE; uint32_t OSOITE=lukea_Internet_osoite(argumentti_MATRIISI[1]);
    int portin_numero=mp_obj_get_int(argumentti_MATRIISI[2]);if(portin_numero<1||portin_numero>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data;mp_get_buffer_raise(argumentti_MATRIISI[3],&data,MP_BUFFER_READ);
    struct pk_sockaddr_in tavoite={0};tavoite.sin_family=AF_INET;tavoite.sin_port=pk_htons(portin_numero);tavoite.sin_addr.s_addr=pk_htonl(OSOITE);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argumentti_MATRIISI[0]),(uintptr_t)data.buf,data.len,0,(uintptr_t)&tavoite,sizeof(tavoite))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t Tiedosto_kahva) {
    unsigned char data[512]; struct pk_sockaddr_in vertaissolmu_ARVO; pk_socklen_t kesto_data = sizeof(vertaissolmu_ARVO);
    intptr_t Koko = 결과검사(사용자호출(35, mp_obj_get_int(Tiedosto_kahva), (uintptr_t)data, 512, 0, (uintptr_t)&vertaissolmu_ARVO, (uintptr_t)&kesto_data));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(data, Koko), MP_OBJ_NEW_SMALL_INT(pk_htons(vertaissolmu_ARVO.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Sulje(mp_obj_t Tiedosto_kahva) { 결과검사(사용자호출(4, mp_obj_get_int(Tiedosto_kahva), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Sulje_OBJ, UDP_Sulje);
static mp_obj_t avata_virta(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,pilvi_Perhe,virta_verkko,virta_kuljetusprotokolla,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,avata_virta);
static mp_obj_t YHDISTÄ_virta(mp_obj_t päätepiste,mp_obj_t OSOITE_SMS,mp_obj_t INDEKSI) {
    int portin_numero=mp_obj_get_int(INDEKSI); if(portin_numero<1||portin_numero>65535)mp_raise_OSError(MP_EINVAL);
    struct pilvi_vastake_OSOITE OSOITE={0}; OSOITE.OSOITE_Perhe=pilvi_Perhe;
    OSOITE.portin_numero=망차례짧은수(portin_numero); OSOITE.Internet_osoite.OSOITE_ARVO=verkko_kokonaisluku(lukea_Internet_osoite(OSOITE_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(päätepiste),(uintptr_t)&OSOITE,sizeof(OSOITE),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(virta_liitin_objekti,YHDISTÄ_virta);
static mp_obj_t lukea_virta(mp_obj_t päätepiste,mp_obj_t 한도) {
    int kesto_ARVO=mp_obj_get_int(한도); if(kesto_ARVO<1||kesto_ARVO>512)mp_raise_OSError(MP_EINVAL);
    unsigned char data[512];
    intptr_t kohde_LASKE=결과검사(사용자호출(2,mp_obj_get_int(päätepiste),(uintptr_t)data,kesto_ARVO,0,0,0));
    return mp_obj_new_bytes(data,kohde_LASKE);
}
static MP_DEFINE_CONST_FUN_OBJ_2(virta_Lukija_objekti,lukea_virta);
static mp_obj_t kirjoitus_virta(mp_obj_t päätepiste,mp_obj_t Sisältö_ARVO) {
    mp_buffer_info_t data; mp_get_buffer_raise(Sisältö_ARVO,&data,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(päätepiste),(uintptr_t)data.buf,data.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(virta_Writer_objekti,kirjoitus_virta);
static mp_obj_t 잠시기다리기(mp_obj_t AIKA_ARVO) {
    결과검사(사용자호출(17,mp_obj_get_int(AIKA_ARVO),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(odottaa_objekti,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Nimi) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)polku_argumentti(Nimi),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Luo_Directory(mp_obj_t Nimi) {
    결과검사(사용자호출(18,(uintptr_t)polku_argumentti(Nimi),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Directory_tekijä_objekti,Luo_Directory);
static mp_obj_t poistaa_Directory(mp_obj_t Nimi) {
    결과검사(사용자호출(18,(uintptr_t)polku_argumentti(Nimi),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,poistaa_Directory);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&virta_liitin_objekti) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&virta_Lukija_objekti) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&virta_Writer_objekti) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&odottaa_objekti) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&Directory_tekijä_objekti) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&STDIN_Lukija_objekti) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Tiedosto_Lukija_objekti) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Tiedosto_Writer_objekti) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&suorakulmio_objekti) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Kello_objekti) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_avata_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_lähettää_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Sulje_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
