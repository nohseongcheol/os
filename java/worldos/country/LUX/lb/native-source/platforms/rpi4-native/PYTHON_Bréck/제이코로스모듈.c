// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t Mooss) { if (Mooss < 0) mp_raise_OSError(-Mooss); return Mooss; }
static const char *Wee_Argument(mp_obj_t VALUE) {
    size_t Element_COUNT; const char *Wee = mp_obj_str_get_data(VALUE, &Element_COUNT);
    if (!Element_COUNT || Element_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < Element_COUNT; 순번++) if (!Wee[순번]) mp_raise_OSError(MP_EINVAL);
    return Wee;
}
static mp_obj_t 파일읽기(mp_obj_t Numm) {
    intptr_t Fichier_Handle = 결과검사(사용자호출(3, (uintptr_t)Wee_Argument(Numm), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t d_Gréisst_veränneren = 결과검사(사용자호출(9, Fichier_Handle, 0, 0, 0, 0, 0));
        vstr_t Daten; vstr_init_len(&Daten, d_Gréisst_veränneren);
        intptr_t Mooss = 사용자호출(2, Fichier_Handle, (uintptr_t)Daten.buf, d_Gréisst_veränneren, 0, 0, 0);
        결과검사(Mooss); Daten.len = Mooss;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&Daten);
        nlr_pop(); 사용자호출(4, Fichier_Handle, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, Fichier_Handle, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Fichier_Lieser_Objet, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t d_Gréisst_veränneren=mp_obj_get_int(한도);
    if(d_Gréisst_veränneren<0||d_Gréisst_veränneren>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t Daten; vstr_init_len(&Daten,d_Gréisst_veränneren);
    intptr_t Element_COUNT=사용자호출(2,0,(uintptr_t)Daten.buf,d_Gréisst_veränneren,0,0,0);
    if(Element_COUNT<0) { vstr_clear(&Daten); 결과검사(Element_COUNT); }
    Daten.len=Element_COUNT; return mp_obj_new_bytes_from_vstr(&Daten);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t schreiwen_Fichier(mp_obj_t Numm, mp_obj_t Inhalt_VALUE) {
    const char *Wee = Wee_Argument(Numm);
    mp_buffer_info_t Daten; mp_get_buffer_raise(Inhalt_VALUE, &Daten, MP_BUFFER_READ);
    if (Daten.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t Fichier_Handle = 결과검사(사용자호출(3, (uintptr_t)Wee, 577, 0, 0, 0, 0));
    intptr_t Agab_COUNT = 사용자호출(1, Fichier_Handle, (uintptr_t)Daten.buf, Daten.len, 0, 0, 0);
    사용자호출(4, Fichier_Handle, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(Agab_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Fichier_Schreiwer_Objet, schreiwen_Fichier);
static mp_obj_t ewechhuelen_Fichier(mp_obj_t Numm) { 결과검사(사용자호출(11, (uintptr_t)Wee_Argument(Numm), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, ewechhuelen_Fichier);
static mp_obj_t 사각형그리기(size_t Element_COUNT, const mp_obj_t *Argument_ARRAY) {
    (void)Element_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(Argument_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t d_Gréisst_veränneren[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, d_Gréisst_veränneren);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Auer_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Auer_Objet, Auer_VALUE);
static mp_obj_t UDP_ariichten(mp_obj_t 접속번호) {
    int Daten_positionéieren = mp_obj_get_int(접속번호); if (Daten_positionéieren < 0 || Daten_positionéieren > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t Fichier_Handle = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(Daten_positionéieren); 첫째값.sin_addr.s_addr = 0;
    intptr_t Mooss = 사용자호출(33, Fichier_Handle, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (Mooss < 0) { 사용자호출(4, Fichier_Handle, 0, 0, 0, 0, 0); 결과검사(Mooss); }
    return mp_obj_new_int(Fichier_Handle);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, UDP_ariichten);
static mp_obj_t UDP_mailen(mp_obj_t Fichier_Handle, mp_obj_t 접속번호, mp_obj_t Inhalt_VALUE) {
    int Daten_positionéieren = mp_obj_get_int(접속번호); if (Daten_positionéieren < 1 || Daten_positionéieren > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t Daten; mp_get_buffer_raise(Inhalt_VALUE, &Daten, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(Daten_positionéieren); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(Fichier_Handle), (uintptr_t)Daten.buf, Daten.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, UDP_mailen);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t Längt_VALUE; const char *SMS=mp_obj_str_get_data(VALUE,&Längt_VALUE);
    unsigned 현재위치=0; uint32_t Adress=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,Ziffer_COUNT=0;
        while(현재위치<Längt_VALUE&&SMS[현재위치]>='0'&&SMS[현재위치]<='9') {
            VALUE=VALUE*10+SMS[현재위치++]-'0'; if(++Ziffer_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!Ziffer_COUNT)mp_raise_OSError(MP_EINVAL);
        Adress=Adress<<8|VALUE;
        if(부분<3&&(현재위치>=Längt_VALUE||SMS[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=Längt_VALUE)mp_raise_OSError(MP_EINVAL);
    return Adress;
}
static mp_obj_t 전문주소전송(size_t Agab_COUNT, const mp_obj_t *Argument_ARRAY) {
    (void)Agab_COUNT; uint32_t Adress=인터넷주소읽기(Argument_ARRAY[1]);
    int 접속번호=mp_obj_get_int(Argument_ARRAY[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t Daten;mp_get_buffer_raise(Argument_ARRAY[3],&Daten,MP_BUFFER_READ);
    struct pk_sockaddr_in Zil={0};Zil.sin_family=AF_INET;Zil.sin_port=pk_htons(접속번호);Zil.sin_addr.s_addr=pk_htonl(Adress);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(Argument_ARRAY[0]),(uintptr_t)Daten.buf,Daten.len,0,(uintptr_t)&Zil,sizeof(Zil))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t Fichier_Handle) {
    unsigned char Daten[512]; struct pk_sockaddr_in Peer_VALUE; pk_socklen_t Längt_Daten = sizeof(Peer_VALUE);
    intptr_t d_Gréisst_veränneren = 결과검사(사용자호출(35, mp_obj_get_int(Fichier_Handle), (uintptr_t)Daten, 512, 0, (uintptr_t)&Peer_VALUE, (uintptr_t)&Längt_Daten));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(Daten, d_Gréisst_veränneren), MP_OBJ_NEW_SMALL_INT(pk_htons(Peer_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Clôture(mp_obj_t Fichier_Handle) { 결과검사(사용자호출(4, mp_obj_get_int(Fichier_Handle), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, UDP_Clôture);
static mp_obj_t ariichten_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,Cloud_Famill,Stream_Reseau,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,ariichten_Stream);
static mp_obj_t Verbannen_Stream(mp_obj_t 종단,mp_obj_t Adress_SMS,mp_obj_t INDEX) {
    int 접속번호=mp_obj_get_int(INDEX); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 Adress={0}; Adress.Adress_Famill=Cloud_Famill;
    Adress.접속번호=망차례짧은수(접속번호); Adress.Internetsadress.Adress_VALUE=Reseau_Ganzzuel(인터넷주소읽기(Adress_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&Adress,sizeof(Adress),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_Konnektor_Objet,Verbannen_Stream);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int Längt_VALUE=mp_obj_get_int(한도); if(Längt_VALUE<1||Längt_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char Daten[512];
    intptr_t Element_COUNT=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)Daten,Längt_VALUE,0,0,0));
    return mp_obj_new_bytes(Daten,Element_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Lieser_Objet,흐름읽기);
static mp_obj_t schreiwen_Stream(mp_obj_t 종단,mp_obj_t Inhalt_VALUE) {
    mp_buffer_info_t Daten; mp_get_buffer_raise(Inhalt_VALUE,&Daten,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)Daten.buf,Daten.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Schreiwer_Objet,schreiwen_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Waart_Objet,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Numm) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)Wee_Argument(Numm),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Create_Verzeechnes(mp_obj_t Numm) {
    결과검사(사용자호출(18,(uintptr_t)Wee_Argument(Numm),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,Create_Verzeechnes);
static mp_obj_t ewechhuelen_Verzeechnes(mp_obj_t Numm) {
    결과검사(사용자호출(18,(uintptr_t)Wee_Argument(Numm),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,ewechhuelen_Verzeechnes);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_Konnektor_Objet) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_Lieser_Objet) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Schreiwer_Objet) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&Waart_Objet) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Fichier_Lieser_Objet) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Fichier_Schreiwer_Objet) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Auer_Objet) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
