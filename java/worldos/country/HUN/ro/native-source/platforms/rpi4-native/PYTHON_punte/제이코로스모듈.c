// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t KR) { if (KR < 0) mp_raise_OSError(-KR); return KR; }
static const char *cale_argument(mp_obj_t VALUE) {
    size_t element_COUNT; const char *Cale = mp_obj_str_get_data(VALUE, &element_COUNT);
    if (!element_COUNT || element_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < element_COUNT; 순번++) if (!Cale[순번]) mp_raise_OSError(MP_EINVAL);
    return Cale;
}
static mp_obj_t 파일읽기(mp_obj_t Nume) {
    intptr_t Fișier_handle = 결과검사(사용자호출(3, (uintptr_t)cale_argument(Nume), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Mărime = 결과검사(사용자호출(9, Fișier_handle, 0, 0, 0, 0, 0));
        vstr_t date; vstr_init_len(&date, Mărime);
        intptr_t KR = 사용자호출(2, Fișier_handle, (uintptr_t)date.buf, Mărime, 0, 0, 0);
        결과검사(KR); date.len = KR;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&date);
        nlr_pop(); 사용자호출(4, Fișier_handle, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, Fișier_handle, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Fișier_Reader_obiect, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Mărime=mp_obj_get_int(한도);
    if(Mărime<0||Mărime>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t date; vstr_init_len(&date,Mărime);
    intptr_t element_COUNT=사용자호출(2,0,(uintptr_t)date.buf,Mărime,0,0,0);
    if(element_COUNT<0) { vstr_clear(&date); 결과검사(element_COUNT); }
    date.len=element_COUNT; return mp_obj_new_bytes_from_vstr(&date);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t scriere_Fișier(mp_obj_t Nume, mp_obj_t Conținut_VALUE) {
    const char *Cale = cale_argument(Nume);
    mp_buffer_info_t date; mp_get_buffer_raise(Conținut_VALUE, &date, MP_BUFFER_READ);
    if (date.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t Fișier_handle = 결과검사(사용자호출(3, (uintptr_t)Cale, 577, 0, 0, 0, 0));
    intptr_t intrare_COUNT = 사용자호출(1, Fișier_handle, (uintptr_t)date.buf, date.len, 0, 0, 0);
    사용자호출(4, Fișier_handle, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(intrare_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Fișier_Writer_obiect, scriere_Fișier);
static mp_obj_t elimina_Fișier(mp_obj_t Nume) { 결과검사(사용자호출(11, (uintptr_t)cale_argument(Nume), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, elimina_Fișier);
static mp_obj_t Paint_dreptunghi(size_t element_COUNT, const mp_obj_t *argument_ARRAY) {
    (void)element_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argument_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(dreptunghi_obiect, 5, 5, Paint_dreptunghi);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Mărime[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Mărime);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Ceas_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Ceas_obiect, Ceas_VALUE);
static mp_obj_t UDP_crea(mp_obj_t număr_port) {
    int date_poziție = mp_obj_get_int(număr_port); if (date_poziție < 0 || date_poziție > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t Fișier_handle = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(date_poziție); 첫째값.sin_addr.s_addr = 0;
    intptr_t KR = 사용자호출(33, Fișier_handle, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (KR < 0) { 사용자호출(4, Fișier_handle, 0, 0, 0, 0, 0); 결과검사(KR); }
    return mp_obj_new_int(Fișier_handle);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_crea_OBJ, UDP_crea);
static mp_obj_t UDP_trimite(mp_obj_t Fișier_handle, mp_obj_t număr_port, mp_obj_t Conținut_VALUE) {
    int date_poziție = mp_obj_get_int(număr_port); if (date_poziție < 1 || date_poziție > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t date; mp_get_buffer_raise(Conținut_VALUE, &date, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(date_poziție); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(Fișier_handle), (uintptr_t)date.buf, date.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_trimite_OBJ, UDP_trimite);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t lungime_VALUE; const char *SMS=mp_obj_str_get_data(VALUE,&lungime_VALUE);
    unsigned curent_poziție=0; uint32_t adresa=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,cifră_COUNT=0;
        while(curent_poziție<lungime_VALUE&&SMS[curent_poziție]>='0'&&SMS[curent_poziție]<='9') {
            VALUE=VALUE*10+SMS[curent_poziție++]-'0'; if(++cifră_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!cifră_COUNT)mp_raise_OSError(MP_EINVAL);
        adresa=adresa<<8|VALUE;
        if(부분<3&&(curent_poziție>=lungime_VALUE||SMS[curent_poziție++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(curent_poziție!=lungime_VALUE)mp_raise_OSError(MP_EINVAL);
    return adresa;
}
static mp_obj_t 전문주소전송(size_t intrare_COUNT, const mp_obj_t *argument_ARRAY) {
    (void)intrare_COUNT; uint32_t adresa=인터넷주소읽기(argument_ARRAY[1]);
    int număr_port=mp_obj_get_int(argument_ARRAY[2]);if(număr_port<1||număr_port>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t date;mp_get_buffer_raise(argument_ARRAY[3],&date,MP_BUFFER_READ);
    struct pk_sockaddr_in țintă={0};țintă.sin_family=AF_INET;țintă.sin_port=pk_htons(număr_port);țintă.sin_addr.s_addr=pk_htonl(adresa);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argument_ARRAY[0]),(uintptr_t)date.buf,date.len,0,(uintptr_t)&țintă,sizeof(țintă))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t Fișier_handle) {
    unsigned char date[512]; struct pk_sockaddr_in pereche_VALUE; pk_socklen_t lungime_date = sizeof(pereche_VALUE);
    intptr_t Mărime = 결과검사(사용자호출(35, mp_obj_get_int(Fișier_handle), (uintptr_t)date, 512, 0, (uintptr_t)&pereche_VALUE, (uintptr_t)&lungime_date));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(date, Mărime), MP_OBJ_NEW_SMALL_INT(pk_htons(pereche_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_închide(mp_obj_t Fișier_handle) { 결과검사(사용자호출(4, mp_obj_get_int(Fișier_handle), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_închide_OBJ, UDP_închide);
static mp_obj_t crea_flux(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,cloud_Familie,flux_rețea,flux_protocol_de_transport,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,crea_flux);
static mp_obj_t conecta_flux(mp_obj_t participant,mp_obj_t adresa_SMS,mp_obj_t INDEX) {
    int număr_port=mp_obj_get_int(INDEX); if(număr_port<1||număr_port>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 adresa={0}; adresa.adresa_Familie=cloud_Familie;
    adresa.număr_port=망차례짧은수(număr_port); adresa.adresă_internet.adresa_VALUE=rețea_întreg(인터넷주소읽기(adresa_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(participant),(uintptr_t)&adresa,sizeof(adresa),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(flux_Conector_obiect,conecta_flux);
static mp_obj_t 흐름읽기(mp_obj_t participant,mp_obj_t 한도) {
    int lungime_VALUE=mp_obj_get_int(한도); if(lungime_VALUE<1||lungime_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char date[512];
    intptr_t element_COUNT=결과검사(사용자호출(2,mp_obj_get_int(participant),(uintptr_t)date,lungime_VALUE,0,0,0));
    return mp_obj_new_bytes(date,element_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(flux_Reader_obiect,흐름읽기);
static mp_obj_t scriere_flux(mp_obj_t participant,mp_obj_t Conținut_VALUE) {
    mp_buffer_info_t date; mp_get_buffer_raise(Conținut_VALUE,&date,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(participant),(uintptr_t)date.buf,date.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(flux_Writer_obiect,scriere_flux);
static mp_obj_t 잠시기다리기(mp_obj_t oră_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(oră_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Nume) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)cale_argument(Nume),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t crea_Director(mp_obj_t Nume) {
    결과검사(사용자호출(18,(uintptr_t)cale_argument(Nume),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Director_autor_obiect,crea_Director);
static mp_obj_t elimina_Director(mp_obj_t Nume) {
    결과검사(사용자호출(18,(uintptr_t)cale_argument(Nume),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,elimina_Director);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&flux_Conector_obiect) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&flux_Reader_obiect) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&flux_Writer_obiect) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&Director_autor_obiect) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Fișier_Reader_obiect) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Fișier_Writer_obiect) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&dreptunghi_obiect) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Ceas_obiect) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_crea_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_trimite_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_închide_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
