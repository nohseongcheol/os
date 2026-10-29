// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t KR) { if (KR < 0) mp_raise_OSError(-KR); return KR; }
static const char *útvonal_argumentum(mp_obj_t ÉRTÉK) {
    size_t cikk_DARAB; const char *ÚTVONAL = mp_obj_str_get_data(ÉRTÉK, &cikk_DARAB);
    if (!cikk_DARAB || cikk_DARAB > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < cikk_DARAB; 순번++) if (!ÚTVONAL[순번]) mp_raise_OSError(MP_EINVAL);
    return ÚTVONAL;
}
static mp_obj_t 파일읽기(mp_obj_t Név) {
    intptr_t fájlleíró = 결과검사(사용자호출(3, (uintptr_t)útvonal_argumentum(Név), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Méret = 결과검사(사용자호출(9, fájlleíró, 0, 0, 0, 0, 0));
        vstr_t adat; vstr_init_len(&adat, Méret);
        intptr_t KR = 사용자호출(2, fájlleíró, (uintptr_t)adat.buf, Méret, 0, 0, 0);
        결과검사(KR); adat.len = KR;
        mp_obj_t ÉRTÉK = mp_obj_new_bytes_from_vstr(&adat);
        nlr_pop(); 사용자호출(4, fájlleíró, 0, 0, 0, 0, 0); return ÉRTÉK;
    }
    사용자호출(4, fájlleíró, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Fájl_Olvasó_objektum, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Méret=mp_obj_get_int(한도);
    if(Méret<0||Méret>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t adat; vstr_init_len(&adat,Méret);
    intptr_t cikk_DARAB=사용자호출(2,0,(uintptr_t)adat.buf,Méret,0,0,0);
    if(cikk_DARAB<0) { vstr_clear(&adat); 결과검사(cikk_DARAB); }
    adat.len=cikk_DARAB; return mp_obj_new_bytes_from_vstr(&adat);
}
static MP_DEFINE_CONST_FUN_OBJ_1(STDIN_Olvasó_objektum, 표준입력읽기);
static mp_obj_t ír_Fájl(mp_obj_t Név, mp_obj_t Tartalom_ÉRTÉK) {
    const char *ÚTVONAL = útvonal_argumentum(Név);
    mp_buffer_info_t adat; mp_get_buffer_raise(Tartalom_ÉRTÉK, &adat, MP_BUFFER_READ);
    if (adat.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t fájlleíró = 결과검사(사용자호출(3, (uintptr_t)ÚTVONAL, 577, 0, 0, 0, 0));
    intptr_t bejegyzés_DARAB = 사용자호출(1, fájlleíró, (uintptr_t)adat.buf, adat.len, 0, 0, 0);
    사용자호출(4, fájlleíró, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(bejegyzés_DARAB));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Fájl_Szerkesztő_objektum, ír_Fájl);
static mp_obj_t eltávolít_Fájl(mp_obj_t Név) { 결과검사(사용자호출(11, (uintptr_t)útvonal_argumentum(Név), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, eltávolít_Fájl);
static mp_obj_t Paint_téglalap(size_t cikk_DARAB, const mp_obj_t *argumentum_TÖMB) {
    (void)cikk_DARAB; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argumentum_TÖMB[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(téglalap_objektum, 5, 5, Paint_téglalap);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Méret[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Méret);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Óra_ÉRTÉK(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Óra_objektum, Óra_ÉRTÉK);
static mp_obj_t UDP_készít(mp_obj_t portszám) {
    int adat_pozíció = mp_obj_get_int(portszám); if (adat_pozíció < 0 || adat_pozíció > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t fájlleíró = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(adat_pozíció); 첫째값.sin_addr.s_addr = 0;
    intptr_t KR = 사용자호출(33, fájlleíró, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (KR < 0) { 사용자호출(4, fájlleíró, 0, 0, 0, 0, 0); 결과검사(KR); }
    return mp_obj_new_int(fájlleíró);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_készít_OBJ, UDP_készít);
static mp_obj_t UDP_küld(mp_obj_t fájlleíró, mp_obj_t portszám, mp_obj_t Tartalom_ÉRTÉK) {
    int adat_pozíció = mp_obj_get_int(portszám); if (adat_pozíció < 1 || adat_pozíció > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t adat; mp_get_buffer_raise(Tartalom_ÉRTÉK, &adat, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(adat_pozíció); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(fájlleíró), (uintptr_t)adat.buf, adat.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_küld_OBJ, UDP_küld);
static uint32_t 인터넷주소읽기(mp_obj_t ÉRTÉK) {
    size_t hossz_ÉRTÉK; const char *Szöveg=mp_obj_str_get_data(ÉRTÉK,&hossz_ÉRTÉK);
    unsigned aktuális_pozíció=0; uint32_t CÍM=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned ÉRTÉK=0,számjegy_DARAB=0;
        while(aktuális_pozíció<hossz_ÉRTÉK&&Szöveg[aktuális_pozíció]>='0'&&Szöveg[aktuális_pozíció]<='9') {
            ÉRTÉK=ÉRTÉK*10+Szöveg[aktuális_pozíció++]-'0'; if(++számjegy_DARAB>3||ÉRTÉK>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!számjegy_DARAB)mp_raise_OSError(MP_EINVAL);
        CÍM=CÍM<<8|ÉRTÉK;
        if(부분<3&&(aktuális_pozíció>=hossz_ÉRTÉK||Szöveg[aktuális_pozíció++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(aktuális_pozíció!=hossz_ÉRTÉK)mp_raise_OSError(MP_EINVAL);
    return CÍM;
}
static mp_obj_t 전문주소전송(size_t bejegyzés_DARAB, const mp_obj_t *argumentum_TÖMB) {
    (void)bejegyzés_DARAB; uint32_t CÍM=인터넷주소읽기(argumentum_TÖMB[1]);
    int portszám=mp_obj_get_int(argumentum_TÖMB[2]);if(portszám<1||portszám>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t adat;mp_get_buffer_raise(argumentum_TÖMB[3],&adat,MP_BUFFER_READ);
    struct pk_sockaddr_in cél={0};cél.sin_family=AF_INET;cél.sin_port=pk_htons(portszám);cél.sin_addr.s_addr=pk_htonl(CÍM);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argumentum_TÖMB[0]),(uintptr_t)adat.buf,adat.len,0,(uintptr_t)&cél,sizeof(cél))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t fájlleíró) {
    unsigned char adat[512]; struct pk_sockaddr_in társ_ÉRTÉK; pk_socklen_t hossz_adat = sizeof(társ_ÉRTÉK);
    intptr_t Méret = 결과검사(사용자호출(35, mp_obj_get_int(fájlleíró), (uintptr_t)adat, 512, 0, (uintptr_t)&társ_ÉRTÉK, (uintptr_t)&hossz_adat));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(adat, Méret), MP_OBJ_NEW_SMALL_INT(pk_htons(társ_ÉRTÉK.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_bezár(mp_obj_t fájlleíró) { 결과검사(사용자호출(4, mp_obj_get_int(fájlleíró), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_bezár_OBJ, UDP_bezár);
static mp_obj_t készít_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,háló_Család,Stream_hálózat,Stream_átviteli_protokoll,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,készít_Stream);
static mp_obj_t KAPCSOLAT_Stream(mp_obj_t végpont,mp_obj_t CÍM_SMS,mp_obj_t INDEX) {
    int portszám=mp_obj_get_int(INDEX); if(portszám<1||portszám>65535)mp_raise_OSError(MP_EINVAL);
    struct háló_szoftvercsatorna_CÍM CÍM={0}; CÍM.CÍM_Család=háló_Család;
    CÍM.portszám=망차례짧은수(portszám); CÍM.internetcím.CÍM_ÉRTÉK=hálózat_egész_szám(인터넷주소읽기(CÍM_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(végpont),(uintptr_t)&CÍM,sizeof(CÍM),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_Összekötő_objektum,KAPCSOLAT_Stream);
static mp_obj_t 흐름읽기(mp_obj_t végpont,mp_obj_t 한도) {
    int hossz_ÉRTÉK=mp_obj_get_int(한도); if(hossz_ÉRTÉK<1||hossz_ÉRTÉK>512)mp_raise_OSError(MP_EINVAL);
    unsigned char adat[512];
    intptr_t cikk_DARAB=결과검사(사용자호출(2,mp_obj_get_int(végpont),(uintptr_t)adat,hossz_ÉRTÉK,0,0,0));
    return mp_obj_new_bytes(adat,cikk_DARAB);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Olvasó_objektum,흐름읽기);
static mp_obj_t ír_Stream(mp_obj_t végpont,mp_obj_t Tartalom_ÉRTÉK) {
    mp_buffer_info_t adat; mp_get_buffer_raise(Tartalom_ÉRTÉK,&adat,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(végpont),(uintptr_t)adat.buf,adat.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Szerkesztő_objektum,ír_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t IDŐ_ÉRTÉK) {
    결과검사(사용자호출(17,mp_obj_get_int(IDŐ_ÉRTÉK),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(várj_objektum,잠시기다리기);
static mp_obj_t bejegyzés_Altípus(mp_obj_t Név) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)útvonal_argumentum(Név),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(bejegyzés_Altípus_objektum,bejegyzés_Altípus);
static mp_obj_t készít_címtár(mp_obj_t Név) {
    결과검사(사용자호출(18,(uintptr_t)útvonal_argumentum(Név),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(címtár_szerző_objektum,készít_címtár);
static mp_obj_t eltávolít_címtár(mp_obj_t Név) {
    결과검사(사용자호출(18,(uintptr_t)útvonal_argumentum(Név),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,eltávolít_címtár);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_Összekötő_objektum) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_Olvasó_objektum) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Szerkesztő_objektum) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&várj_objektum) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&bejegyzés_Altípus_objektum) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&címtár_szerző_objektum) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&STDIN_Olvasó_objektum) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Fájl_Olvasó_objektum) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Fájl_Szerkesztő_objektum) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&téglalap_objektum) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Óra_objektum) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_készít_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_küld_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_bezár_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
