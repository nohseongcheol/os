// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t KR) { if (KR < 0) mp_raise_OSError(-KR); return KR; }
static const char *bane_argument(mp_obj_t VERDI) {
    size_t vare_ANTALL; const char *Sti = mp_obj_str_get_data(VERDI, &vare_ANTALL);
    if (!vare_ANTALL || vare_ANTALL > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < vare_ANTALL; 순번++) if (!Sti[순번]) mp_raise_OSError(MP_EINVAL);
    return Sti;
}
static mp_obj_t 파일읽기(mp_obj_t Navn) {
    intptr_t Fil_håndtak = 결과검사(사용자호출(3, (uintptr_t)bane_argument(Navn), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Størrelse = 결과검사(사용자호출(9, Fil_håndtak, 0, 0, 0, 0, 0));
        vstr_t data; vstr_init_len(&data, Størrelse);
        intptr_t KR = 사용자호출(2, Fil_håndtak, (uintptr_t)data.buf, Størrelse, 0, 0, 0);
        결과검사(KR); data.len = KR;
        mp_obj_t VERDI = mp_obj_new_bytes_from_vstr(&data);
        nlr_pop(); 사용자호출(4, Fil_håndtak, 0, 0, 0, 0, 0); return VERDI;
    }
    사용자호출(4, Fil_håndtak, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Fil_Leser_objekt, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Størrelse=mp_obj_get_int(한도);
    if(Størrelse<0||Størrelse>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t data; vstr_init_len(&data,Størrelse);
    intptr_t vare_ANTALL=사용자호출(2,0,(uintptr_t)data.buf,Størrelse,0,0,0);
    if(vare_ANTALL<0) { vstr_clear(&data); 결과검사(vare_ANTALL); }
    data.len=vare_ANTALL; return mp_obj_new_bytes_from_vstr(&data);
}
static MP_DEFINE_CONST_FUN_OBJ_1(STDIN_Leser_objekt, 표준입력읽기);
static mp_obj_t skrive_Fil(mp_obj_t Navn, mp_obj_t Innhold_VERDI) {
    const char *Sti = bane_argument(Navn);
    mp_buffer_info_t data; mp_get_buffer_raise(Innhold_VERDI, &data, MP_BUFFER_READ);
    if (data.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t Fil_håndtak = 결과검사(사용자호출(3, (uintptr_t)Sti, 577, 0, 0, 0, 0));
    intptr_t oppføring_ANTALL = 사용자호출(1, Fil_håndtak, (uintptr_t)data.buf, data.len, 0, 0, 0);
    사용자호출(4, Fil_håndtak, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(oppføring_ANTALL));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Fil_Writer_objekt, skrive_Fil);
static mp_obj_t fjerne_Fil(mp_obj_t Navn) { 결과검사(사용자호출(11, (uintptr_t)bane_argument(Navn), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, fjerne_Fil);
static mp_obj_t Paint_rektangel(size_t vare_ANTALL, const mp_obj_t *argument_MATRISE) {
    (void)vare_ANTALL; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argument_MATRISE[순번]);
    결과검사(skjermbilde_rektangel(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(rektangel_objekt, 5, 5, Paint_rektangel);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Størrelse[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Størrelse);
}
static MP_DEFINE_CONST_FUN_OBJ_0(skjermbilde_skalere_objekt, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(skjermbilde_vent_objekt, 화면입력기다리기);
static mp_obj_t Klokke_VERDI(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Klokke_objekt, Klokke_VERDI);
static mp_obj_t UDP_åpen(mp_obj_t portnummer) {
    int data_plassere = mp_obj_get_int(portnummer); if (data_plassere < 0 || data_plassere > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t Fil_håndtak = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_plassere); 첫째값.sin_addr.s_addr = 0;
    intptr_t KR = 사용자호출(33, Fil_håndtak, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (KR < 0) { 사용자호출(4, Fil_håndtak, 0, 0, 0, 0, 0); 결과검사(KR); }
    return mp_obj_new_int(Fil_håndtak);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_åpen_OBJ, UDP_åpen);
static mp_obj_t UDP_sende(mp_obj_t Fil_håndtak, mp_obj_t portnummer, mp_obj_t Innhold_VERDI) {
    int data_plassere = mp_obj_get_int(portnummer); if (data_plassere < 1 || data_plassere > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data; mp_get_buffer_raise(Innhold_VERDI, &data, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_plassere); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(Fil_håndtak), (uintptr_t)data.buf, data.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_sende_OBJ, UDP_sende);
static uint32_t 인터넷주소읽기(mp_obj_t VERDI) {
    size_t lengde_VERDI; const char *Tekst=mp_obj_str_get_data(VERDI,&lengde_VERDI);
    unsigned betalt_plassere=0; uint32_t e_post=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VERDI=0,siffer_ANTALL=0;
        while(betalt_plassere<lengde_VERDI&&Tekst[betalt_plassere]>='0'&&Tekst[betalt_plassere]<='9') {
            VERDI=VERDI*10+Tekst[betalt_plassere++]-'0'; if(++siffer_ANTALL>3||VERDI>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!siffer_ANTALL)mp_raise_OSError(MP_EINVAL);
        e_post=e_post<<8|VERDI;
        if(부분<3&&(betalt_plassere>=lengde_VERDI||Tekst[betalt_plassere++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(betalt_plassere!=lengde_VERDI)mp_raise_OSError(MP_EINVAL);
    return e_post;
}
static mp_obj_t 전문주소전송(size_t oppføring_ANTALL, const mp_obj_t *argument_MATRISE) {
    (void)oppføring_ANTALL; uint32_t e_post=인터넷주소읽기(argument_MATRISE[1]);
    int portnummer=mp_obj_get_int(argument_MATRISE[2]);if(portnummer<1||portnummer>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data;mp_get_buffer_raise(argument_MATRISE[3],&data,MP_BUFFER_READ);
    struct pk_sockaddr_in mål={0};mål.sin_family=AF_INET;mål.sin_port=pk_htons(portnummer);mål.sin_addr.s_addr=pk_htonl(e_post);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argument_MATRISE[0]),(uintptr_t)data.buf,data.len,0,(uintptr_t)&mål,sizeof(mål))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t Fil_håndtak) {
    unsigned char data[512]; struct pk_sockaddr_in node_VERDI_6a3b6fa7; pk_socklen_t lengde_data = sizeof(node_VERDI_6a3b6fa7);
    intptr_t Størrelse = 결과검사(사용자호출(35, mp_obj_get_int(Fil_håndtak), (uintptr_t)data, 512, 0, (uintptr_t)&node_VERDI_6a3b6fa7, (uintptr_t)&lengde_data));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(data, Størrelse), MP_OBJ_NEW_SMALL_INT(pk_htons(node_VERDI_6a3b6fa7.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Lukk(mp_obj_t Fil_håndtak) { 결과검사(사용자호출(4, mp_obj_get_int(Fil_håndtak), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Lukk_OBJ, UDP_Lukk);
static mp_obj_t åpen_strøm(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,sky_serie,strøm_nettverk,strøm_transportprotokoll,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,åpen_strøm);
static mp_obj_t KOBLE_TIL_strøm(mp_obj_t deltaker,mp_obj_t e_post_SMS,mp_obj_t INDEKS) {
    int portnummer=mp_obj_get_int(INDEKS); if(portnummer<1||portnummer>65535)mp_raise_OSError(MP_EINVAL);
    struct sky_socket_e_post e_post={0}; e_post.e_post_serie=sky_serie;
    e_post.portnummer=망차례짧은수(portnummer); e_post.Internett_adresse.e_post_VERDI=nettverk_heltall(인터넷주소읽기(e_post_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(deltaker),(uintptr_t)&e_post,sizeof(e_post),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(strøm_Kobling_objekt,KOBLE_TIL_strøm);
static mp_obj_t 흐름읽기(mp_obj_t deltaker,mp_obj_t 한도) {
    int lengde_VERDI=mp_obj_get_int(한도); if(lengde_VERDI<1||lengde_VERDI>512)mp_raise_OSError(MP_EINVAL);
    unsigned char data[512];
    intptr_t vare_ANTALL=결과검사(사용자호출(2,mp_obj_get_int(deltaker),(uintptr_t)data,lengde_VERDI,0,0,0));
    return mp_obj_new_bytes(data,vare_ANTALL);
}
static MP_DEFINE_CONST_FUN_OBJ_2(strøm_Leser_objekt,흐름읽기);
static mp_obj_t skrive_strøm(mp_obj_t deltaker,mp_obj_t Innhold_VERDI) {
    mp_buffer_info_t data; mp_get_buffer_raise(Innhold_VERDI,&data,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(deltaker),(uintptr_t)data.buf,data.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(strøm_Writer_objekt,skrive_strøm);
static mp_obj_t 잠시기다리기(mp_obj_t TID_VERDI) {
    결과검사(사용자호출(17,mp_obj_get_int(TID_VERDI),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(vent_objekt,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Navn) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)bane_argument(Navn),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t åpne_katalog(mp_obj_t Navn) {
    결과검사(사용자호출(18,(uintptr_t)bane_argument(Navn),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(katalog_forfatter_objekt,åpne_katalog);
static mp_obj_t fjerne_katalog(mp_obj_t Navn) {
    결과검사(사용자호출(18,(uintptr_t)bane_argument(Navn),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,fjerne_katalog);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&strøm_Kobling_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&strøm_Leser_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&strøm_Writer_objekt) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&vent_objekt) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&katalog_forfatter_objekt) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&STDIN_Leser_objekt) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Fil_Leser_objekt) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Fil_Writer_objekt) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&rektangel_objekt) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&skjermbilde_skalere_objekt) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&skjermbilde_vent_objekt) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Klokke_objekt) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_åpen_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_sende_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Lukk_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
