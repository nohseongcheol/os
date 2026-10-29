// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t KR) { if (KR < 0) mp_raise_OSError(-KR); return KR; }
static const char *sti_argument(mp_obj_t VÆRDI) {
    size_t vare_TÆL; const char *Sti = mp_obj_str_get_data(VÆRDI, &vare_TÆL);
    if (!vare_TÆL || vare_TÆL > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < vare_TÆL; 순번++) if (!Sti[순번]) mp_raise_OSError(MP_EINVAL);
    return Sti;
}
static mp_obj_t 파일읽기(mp_obj_t Navn) {
    intptr_t fil_handle = 결과검사(사용자호출(3, (uintptr_t)sti_argument(Navn), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Størrelse = 결과검사(사용자호출(9, fil_handle, 0, 0, 0, 0, 0));
        vstr_t data; vstr_init_len(&data, Størrelse);
        intptr_t KR = 사용자호출(2, fil_handle, (uintptr_t)data.buf, Størrelse, 0, 0, 0);
        결과검사(KR); data.len = KR;
        mp_obj_t VÆRDI = mp_obj_new_bytes_from_vstr(&data);
        nlr_pop(); 사용자호출(4, fil_handle, 0, 0, 0, 0, 0); return VÆRDI;
    }
    사용자호출(4, fil_handle, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(fil_Læser_objekt, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Størrelse=mp_obj_get_int(한도);
    if(Størrelse<0||Størrelse>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t data; vstr_init_len(&data,Størrelse);
    intptr_t vare_TÆL=사용자호출(2,0,(uintptr_t)data.buf,Størrelse,0,0,0);
    if(vare_TÆL<0) { vstr_clear(&data); 결과검사(vare_TÆL); }
    data.len=vare_TÆL; return mp_obj_new_bytes_from_vstr(&data);
}
static MP_DEFINE_CONST_FUN_OBJ_1(STDIN_Læser_objekt, 표준입력읽기);
static mp_obj_t skrive_fil(mp_obj_t Navn, mp_obj_t Indhold_VÆRDI) {
    const char *Sti = sti_argument(Navn);
    mp_buffer_info_t data; mp_get_buffer_raise(Indhold_VÆRDI, &data, MP_BUFFER_READ);
    if (data.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t fil_handle = 결과검사(사용자호출(3, (uintptr_t)Sti, 577, 0, 0, 0, 0));
    intptr_t post_TÆL_8f7753a1 = 사용자호출(1, fil_handle, (uintptr_t)data.buf, data.len, 0, 0, 0);
    사용자호출(4, fil_handle, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(post_TÆL_8f7753a1));
}
static MP_DEFINE_CONST_FUN_OBJ_2(fil_Writer_objekt, skrive_fil);
static mp_obj_t fjerne_fil(mp_obj_t Navn) { 결과검사(사용자호출(11, (uintptr_t)sti_argument(Navn), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, fjerne_fil);
static mp_obj_t Paint_rektangel(size_t vare_TÆL, const mp_obj_t *argument_MATRIX) {
    (void)vare_TÆL; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argument_MATRIX[순번]);
    결과검사(skærmbillede_rektangel(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(rektangel_objekt, 5, 5, Paint_rektangel);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Størrelse[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Størrelse);
}
static MP_DEFINE_CONST_FUN_OBJ_0(skærmbillede_tilpasse_størrelse_objekt, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(skærmbillede_vent_objekt, 화면입력기다리기);
static mp_obj_t Ur_VÆRDI(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Ur_objekt, Ur_VÆRDI);
static mp_obj_t UDP_åben(mp_obj_t portnummer) {
    int data_placere = mp_obj_get_int(portnummer); if (data_placere < 0 || data_placere > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t fil_handle = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_placere); 첫째값.sin_addr.s_addr = 0;
    intptr_t KR = 사용자호출(33, fil_handle, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (KR < 0) { 사용자호출(4, fil_handle, 0, 0, 0, 0, 0); 결과검사(KR); }
    return mp_obj_new_int(fil_handle);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_åben_OBJ, UDP_åben);
static mp_obj_t UDP_maile(mp_obj_t fil_handle, mp_obj_t portnummer, mp_obj_t Indhold_VÆRDI) {
    int data_placere = mp_obj_get_int(portnummer); if (data_placere < 1 || data_placere > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data; mp_get_buffer_raise(Indhold_VÆRDI, &data, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_placere); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(fil_handle), (uintptr_t)data.buf, data.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_maile_OBJ, UDP_maile);
static uint32_t 인터넷주소읽기(mp_obj_t VÆRDI) {
    size_t varighed_VÆRDI; const char *Tekst=mp_obj_str_get_data(VÆRDI,&varighed_VÆRDI);
    unsigned aktuel_placere=0; uint32_t mail=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VÆRDI=0,ciffer_TÆL=0;
        while(aktuel_placere<varighed_VÆRDI&&Tekst[aktuel_placere]>='0'&&Tekst[aktuel_placere]<='9') {
            VÆRDI=VÆRDI*10+Tekst[aktuel_placere++]-'0'; if(++ciffer_TÆL>3||VÆRDI>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!ciffer_TÆL)mp_raise_OSError(MP_EINVAL);
        mail=mail<<8|VÆRDI;
        if(부분<3&&(aktuel_placere>=varighed_VÆRDI||Tekst[aktuel_placere++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(aktuel_placere!=varighed_VÆRDI)mp_raise_OSError(MP_EINVAL);
    return mail;
}
static mp_obj_t 전문주소전송(size_t post_TÆL_8f7753a1, const mp_obj_t *argument_MATRIX) {
    (void)post_TÆL_8f7753a1; uint32_t mail=인터넷주소읽기(argument_MATRIX[1]);
    int portnummer=mp_obj_get_int(argument_MATRIX[2]);if(portnummer<1||portnummer>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data;mp_get_buffer_raise(argument_MATRIX[3],&data,MP_BUFFER_READ);
    struct pk_sockaddr_in mål={0};mål.sin_family=AF_INET;mål.sin_port=pk_htons(portnummer);mål.sin_addr.s_addr=pk_htonl(mail);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argument_MATRIX[0]),(uintptr_t)data.buf,data.len,0,(uintptr_t)&mål,sizeof(mål))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t fil_handle) {
    unsigned char data[512]; struct pk_sockaddr_in peer_VÆRDI; pk_socklen_t varighed_data = sizeof(peer_VÆRDI);
    intptr_t Størrelse = 결과검사(사용자호출(35, mp_obj_get_int(fil_handle), (uintptr_t)data, 512, 0, (uintptr_t)&peer_VÆRDI, (uintptr_t)&varighed_data));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(data, Størrelse), MP_OBJ_NEW_SMALL_INT(pk_htons(peer_VÆRDI.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Luk(mp_obj_t fil_handle) { 결과검사(사용자호출(4, mp_obj_get_int(fil_handle), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Luk_OBJ, UDP_Luk);
static mp_obj_t åben_strøm(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,net_serie,strøm_netværk,strøm_transportprotokol,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,åben_strøm);
static mp_obj_t Forbind_strøm(mp_obj_t slutpunkt,mp_obj_t mail_sms,mp_obj_t INDEKS) {
    int portnummer=mp_obj_get_int(INDEKS); if(portnummer<1||portnummer>65535)mp_raise_OSError(MP_EINVAL);
    struct net_socket_mail mail={0}; mail.mail_serie=net_serie;
    mail.portnummer=망차례짧은수(portnummer); mail.internetadresse.mail_VÆRDI=netværk_heltal(인터넷주소읽기(mail_sms));
    결과검사(사용자호출(37,mp_obj_get_int(slutpunkt),(uintptr_t)&mail,sizeof(mail),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(strøm_connector_objekt,Forbind_strøm);
static mp_obj_t 흐름읽기(mp_obj_t slutpunkt,mp_obj_t 한도) {
    int varighed_VÆRDI=mp_obj_get_int(한도); if(varighed_VÆRDI<1||varighed_VÆRDI>512)mp_raise_OSError(MP_EINVAL);
    unsigned char data[512];
    intptr_t vare_TÆL=결과검사(사용자호출(2,mp_obj_get_int(slutpunkt),(uintptr_t)data,varighed_VÆRDI,0,0,0));
    return mp_obj_new_bytes(data,vare_TÆL);
}
static MP_DEFINE_CONST_FUN_OBJ_2(strøm_Læser_objekt,흐름읽기);
static mp_obj_t skrive_strøm(mp_obj_t slutpunkt,mp_obj_t Indhold_VÆRDI) {
    mp_buffer_info_t data; mp_get_buffer_raise(Indhold_VÆRDI,&data,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(slutpunkt),(uintptr_t)data.buf,data.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(strøm_Writer_objekt,skrive_strøm);
static mp_obj_t 잠시기다리기(mp_obj_t TID_VÆRDI) {
    결과검사(사용자호출(17,mp_obj_get_int(TID_VÆRDI),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(vent_objekt,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Navn) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)sti_argument(Navn),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t åbne_mappe(mp_obj_t Navn) {
    결과검사(사용자호출(18,(uintptr_t)sti_argument(Navn),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(mappe_skaber_objekt,åbne_mappe);
static mp_obj_t fjerne_mappe(mp_obj_t Navn) {
    결과검사(사용자호출(18,(uintptr_t)sti_argument(Navn),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,fjerne_mappe);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&strøm_connector_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&strøm_Læser_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&strøm_Writer_objekt) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&vent_objekt) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&mappe_skaber_objekt) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&STDIN_Læser_objekt) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&fil_Læser_objekt) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&fil_Writer_objekt) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&rektangel_objekt) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&skærmbillede_tilpasse_størrelse_objekt) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&skærmbillede_vent_objekt) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Ur_objekt) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_åben_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_maile_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Luk_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
