// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "sieć_ABI.h"
static intptr_t 결과검사(intptr_t WYNIK) { if (WYNIK < 0) mp_raise_OSError(-WYNIK); return WYNIK; }
static const char *ścieżka_argument(mp_obj_t WARTOŚĆ) {
    size_t towar_ILE_LICZB; const char *ścieżka_2 = mp_obj_str_get_data(WARTOŚĆ, &towar_ILE_LICZB);
    if (!towar_ILE_LICZB || towar_ILE_LICZB > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < towar_ILE_LICZB; 순번++) if (!ścieżka_2[순번]) mp_raise_OSError(MP_EINVAL);
    return ścieżka_2;
}
static mp_obj_t 파일읽기(mp_obj_t Nazwa) {
    intptr_t dojście_do_pliku = 결과검사(사용자호출(3, (uintptr_t)ścieżka_argument(Nazwa), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Rozmiar = 결과검사(사용자호출(9, dojście_do_pliku, 0, 0, 0, 0, 0));
        vstr_t dane; vstr_init_len(&dane, Rozmiar);
        intptr_t WYNIK = 사용자호출(2, dojście_do_pliku, (uintptr_t)dane.buf, Rozmiar, 0, 0, 0);
        결과검사(WYNIK); dane.len = WYNIK;
        mp_obj_t WARTOŚĆ = mp_obj_new_bytes_from_vstr(&dane);
        nlr_pop(); 사용자호출(4, dojście_do_pliku, 0, 0, 0, 0, 0); return WARTOŚĆ;
    }
    사용자호출(4, dojście_do_pliku, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Plik_Czytnik_obiekt, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Rozmiar=mp_obj_get_int(한도);
    if(Rozmiar<0||Rozmiar>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t dane; vstr_init_len(&dane,Rozmiar);
    intptr_t towar_ILE_LICZB=사용자호출(2,0,(uintptr_t)dane.buf,Rozmiar,0,0,0);
    if(towar_ILE_LICZB<0) { vstr_clear(&dane); 결과검사(towar_ILE_LICZB); }
    dane.len=towar_ILE_LICZB; return mp_obj_new_bytes_from_vstr(&dane);
}
static MP_DEFINE_CONST_FUN_OBJ_1(STDIN_Czytnik_obiekt, 표준입력읽기);
static mp_obj_t zapis_Plik(mp_obj_t Nazwa, mp_obj_t treść_WARTOŚĆ_cb0f2404) {
    const char *ścieżka_2 = ścieżka_argument(Nazwa);
    mp_buffer_info_t dane; mp_get_buffer_raise(treść_WARTOŚĆ_cb0f2404, &dane, MP_BUFFER_READ);
    if (dane.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t dojście_do_pliku = 결과검사(사용자호출(3, (uintptr_t)ścieżka_2, 577, 0, 0, 0, 0));
    intptr_t wpis_ILE_LICZB = 사용자호출(1, dojście_do_pliku, (uintptr_t)dane.buf, dane.len, 0, 0, 0);
    사용자호출(4, dojście_do_pliku, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(wpis_ILE_LICZB));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Plik_Edytor_obiekt, zapis_Plik);
static mp_obj_t usuń_Plik(mp_obj_t Nazwa) { 결과검사(사용자호출(11, (uintptr_t)ścieżka_argument(Nazwa), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, usuń_Plik);
static mp_obj_t Paint_prostokąt(size_t towar_ILE_LICZB, const mp_obj_t *argument_TABLICA) {
    (void)towar_ILE_LICZB; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argument_TABLICA[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(prostokąt_obiekt, 5, 5, Paint_prostokąt);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Rozmiar[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Rozmiar);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Zegar_WARTOŚĆ(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Zegar_obiekt, Zegar_WARTOŚĆ);
static mp_obj_t UDP_otwarty(mp_obj_t numer_portu) {
    int dane_stanowisko = mp_obj_get_int(numer_portu); if (dane_stanowisko < 0 || dane_stanowisko > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t dojście_do_pliku = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(dane_stanowisko); 첫째값.sin_addr.s_addr = 0;
    intptr_t WYNIK = 사용자호출(33, dojście_do_pliku, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (WYNIK < 0) { 사용자호출(4, dojście_do_pliku, 0, 0, 0, 0, 0); 결과검사(WYNIK); }
    return mp_obj_new_int(dojście_do_pliku);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_otwarty_OBJ, UDP_otwarty);
static mp_obj_t UDP_wysłać(mp_obj_t dojście_do_pliku, mp_obj_t numer_portu, mp_obj_t treść_WARTOŚĆ_cb0f2404) {
    int dane_stanowisko = mp_obj_get_int(numer_portu); if (dane_stanowisko < 1 || dane_stanowisko > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t dane; mp_get_buffer_raise(treść_WARTOŚĆ_cb0f2404, &dane, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(dane_stanowisko); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(dojście_do_pliku), (uintptr_t)dane.buf, dane.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_wysłać_OBJ, UDP_wysłać);
static uint32_t 인터넷주소읽기(mp_obj_t WARTOŚĆ) {
    size_t długość_WARTOŚĆ; const char *tekst=mp_obj_str_get_data(WARTOŚĆ,&długość_WARTOŚĆ);
    unsigned bieżący_stanowisko=0; uint32_t Adres=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned WARTOŚĆ=0,cyfra_ILE_LICZB=0;
        while(bieżący_stanowisko<długość_WARTOŚĆ&&tekst[bieżący_stanowisko]>='0'&&tekst[bieżący_stanowisko]<='9') {
            WARTOŚĆ=WARTOŚĆ*10+tekst[bieżący_stanowisko++]-'0'; if(++cyfra_ILE_LICZB>3||WARTOŚĆ>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!cyfra_ILE_LICZB)mp_raise_OSError(MP_EINVAL);
        Adres=Adres<<8|WARTOŚĆ;
        if(부분<3&&(bieżący_stanowisko>=długość_WARTOŚĆ||tekst[bieżący_stanowisko++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(bieżący_stanowisko!=długość_WARTOŚĆ)mp_raise_OSError(MP_EINVAL);
    return Adres;
}
static mp_obj_t 전문주소전송(size_t wpis_ILE_LICZB, const mp_obj_t *argument_TABLICA) {
    (void)wpis_ILE_LICZB; uint32_t Adres=인터넷주소읽기(argument_TABLICA[1]);
    int numer_portu=mp_obj_get_int(argument_TABLICA[2]);if(numer_portu<1||numer_portu>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t dane;mp_get_buffer_raise(argument_TABLICA[3],&dane,MP_BUFFER_READ);
    struct pk_sockaddr_in wartość_docelowa={0};wartość_docelowa.sin_family=AF_INET;wartość_docelowa.sin_port=pk_htons(numer_portu);wartość_docelowa.sin_addr.s_addr=pk_htonl(Adres);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argument_TABLICA[0]),(uintptr_t)dane.buf,dane.len,0,(uintptr_t)&wartość_docelowa,sizeof(wartość_docelowa))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t dojście_do_pliku) {
    unsigned char dane[512]; struct pk_sockaddr_in węzeł_równorzędny_WARTOŚĆ; pk_socklen_t długość_dane = sizeof(węzeł_równorzędny_WARTOŚĆ);
    intptr_t Rozmiar = 결과검사(사용자호출(35, mp_obj_get_int(dojście_do_pliku), (uintptr_t)dane, 512, 0, (uintptr_t)&węzeł_równorzędny_WARTOŚĆ, (uintptr_t)&długość_dane));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(dane, Rozmiar), MP_OBJ_NEW_SMALL_INT(pk_htons(węzeł_równorzędny_WARTOŚĆ.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Zamknij(mp_obj_t dojście_do_pliku) { 결과검사(사용자호출(4, mp_obj_get_int(dojście_do_pliku), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Zamknij_OBJ, UDP_Zamknij);
static mp_obj_t otwarty_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,chmura_Rodzina,Stream_sieć,Stream_protokół_transportu,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,otwarty_Stream);
static mp_obj_t POŁĄCZ_Stream(mp_obj_t uczestnik,mp_obj_t ADRES_SMS,mp_obj_t INDEKS) {
    int numer_portu=mp_obj_get_int(INDEKS); if(numer_portu<1||numer_portu>65535)mp_raise_OSError(MP_EINVAL);
    struct chmura_gniazdo_ADRES Adres={0}; Adres.ADRES_Rodzina=chmura_Rodzina;
    Adres.numer_portu=망차례짧은수(numer_portu); Adres.adres_internetowy.ADRES_WARTOŚĆ=sieć_liczba_całkowita(인터넷주소읽기(ADRES_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(uczestnik),(uintptr_t)&Adres,sizeof(Adres),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_Łącznik_obiekt,POŁĄCZ_Stream);
static mp_obj_t 흐름읽기(mp_obj_t uczestnik,mp_obj_t 한도) {
    int długość_WARTOŚĆ=mp_obj_get_int(한도); if(długość_WARTOŚĆ<1||długość_WARTOŚĆ>512)mp_raise_OSError(MP_EINVAL);
    unsigned char dane[512];
    intptr_t towar_ILE_LICZB=결과검사(사용자호출(2,mp_obj_get_int(uczestnik),(uintptr_t)dane,długość_WARTOŚĆ,0,0,0));
    return mp_obj_new_bytes(dane,towar_ILE_LICZB);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Czytnik_obiekt,흐름읽기);
static mp_obj_t zapis_Stream(mp_obj_t uczestnik,mp_obj_t treść_WARTOŚĆ_cb0f2404) {
    mp_buffer_info_t dane; mp_get_buffer_raise(treść_WARTOŚĆ_cb0f2404,&dane,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(uczestnik),(uintptr_t)dane.buf,dane.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Edytor_obiekt,zapis_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t wartość_czasu) {
    결과검사(사용자호출(17,mp_obj_get_int(wartość_czasu),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(chwileczkę_obiekt,잠시기다리기);
static mp_obj_t wpis_Rodzaj(mp_obj_t Nazwa) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)ścieżka_argument(Nazwa),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(wpis_Rodzaj_obiekt,wpis_Rodzaj);
static mp_obj_t Twórca_Katalog(mp_obj_t Nazwa) {
    결과검사(사용자호출(18,(uintptr_t)ścieżka_argument(Nazwa),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Katalog_autor_obiekt,Twórca_Katalog);
static mp_obj_t usuń_Katalog(mp_obj_t Nazwa) {
    결과검사(사용자호출(18,(uintptr_t)ścieżka_argument(Nazwa),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,usuń_Katalog);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_Łącznik_obiekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_Czytnik_obiekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Edytor_obiekt) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&chwileczkę_obiekt) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&wpis_Rodzaj_obiekt) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&Katalog_autor_obiekt) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&STDIN_Czytnik_obiekt) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Plik_Czytnik_obiekt) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Plik_Edytor_obiekt) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&prostokąt_obiekt) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Zegar_obiekt) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_otwarty_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_wysłać_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Zamknij_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
