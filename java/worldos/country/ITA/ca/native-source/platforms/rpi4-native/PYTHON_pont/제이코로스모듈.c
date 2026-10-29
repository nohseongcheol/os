// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t RESULTAT) { if (RESULTAT < 0) mp_raise_OSError(-RESULTAT); return RESULTAT; }
static const char *camí_arg(mp_obj_t VALOR) {
    size_t element_COMPT; const char *Camí = mp_obj_str_get_data(VALOR, &element_COMPT);
    if (!element_COMPT || element_COMPT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < element_COMPT; 순번++) if (!Camí[순번]) mp_raise_OSError(MP_EINVAL);
    return Camí;
}
static mp_obj_t tancar_arxiu(mp_obj_t Nom) {
    intptr_t arxiu_control_7f4cdfd5 = 결과검사(사용자호출(3, (uintptr_t)camí_arg(Nom), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Mida = 결과검사(사용자호출(9, arxiu_control_7f4cdfd5, 0, 0, 0, 0, 0));
        vstr_t dades; vstr_init_len(&dades, Mida);
        intptr_t RESULTAT = 사용자호출(2, arxiu_control_7f4cdfd5, (uintptr_t)dades.buf, Mida, 0, 0, 0);
        결과검사(RESULTAT); dades.len = RESULTAT;
        mp_obj_t VALOR = mp_obj_new_bytes_from_vstr(&dades);
        nlr_pop(); 사용자호출(4, arxiu_control_7f4cdfd5, 0, 0, 0, 0, 0); return VALOR;
    }
    사용자호출(4, arxiu_control_7f4cdfd5, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(arxiu_Lector_objecte, tancar_arxiu);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Mida=mp_obj_get_int(한도);
    if(Mida<0||Mida>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t dades; vstr_init_len(&dades,Mida);
    intptr_t element_COMPT=사용자호출(2,0,(uintptr_t)dades.buf,Mida,0,0,0);
    if(element_COMPT<0) { vstr_clear(&dades); 결과검사(element_COMPT); }
    dades.len=element_COMPT; return mp_obj_new_bytes_from_vstr(&dades);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t escriure_arxiu(mp_obj_t Nom, mp_obj_t contingut_VALOR) {
    const char *Camí = camí_arg(Nom);
    mp_buffer_info_t dades; mp_get_buffer_raise(contingut_VALOR, &dades, MP_BUFFER_READ);
    if (dades.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t arxiu_control_7f4cdfd5 = 결과검사(사용자호출(3, (uintptr_t)Camí, 577, 0, 0, 0, 0));
    intptr_t introducció_COMPT = 사용자호출(1, arxiu_control_7f4cdfd5, (uintptr_t)dades.buf, dades.len, 0, 0, 0);
    사용자호출(4, arxiu_control_7f4cdfd5, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(introducció_COMPT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(arxiu_Writer_objecte, escriure_arxiu);
static mp_obj_t suprimir_arxiu(mp_obj_t Nom) { 결과검사(사용자호출(11, (uintptr_t)camí_arg(Nom), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, suprimir_arxiu);
static mp_obj_t 사각형그리기(size_t element_COMPT, const mp_obj_t *arg_MATRIU) {
    (void)element_COMPT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(arg_MATRIU[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Mida[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Mida);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Rellotge_VALOR(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Rellotge_objecte, Rellotge_VALOR);
static mp_obj_t UDP_crear(mp_obj_t número_de_port) {
    int dades_càrrec = mp_obj_get_int(número_de_port); if (dades_càrrec < 0 || dades_càrrec > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t arxiu_control_7f4cdfd5 = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(dades_càrrec); 첫째값.sin_addr.s_addr = 0;
    intptr_t RESULTAT = 사용자호출(33, arxiu_control_7f4cdfd5, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (RESULTAT < 0) { 사용자호출(4, arxiu_control_7f4cdfd5, 0, 0, 0, 0, 0); 결과검사(RESULTAT); }
    return mp_obj_new_int(arxiu_control_7f4cdfd5);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_crear_OBJ, UDP_crear);
static mp_obj_t UDP_enviar(mp_obj_t arxiu_control_7f4cdfd5, mp_obj_t número_de_port, mp_obj_t contingut_VALOR) {
    int dades_càrrec = mp_obj_get_int(número_de_port); if (dades_càrrec < 1 || dades_càrrec > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t dades; mp_get_buffer_raise(contingut_VALOR, &dades, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(dades_càrrec); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(arxiu_control_7f4cdfd5), (uintptr_t)dades.buf, dades.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_enviar_OBJ, UDP_enviar);
static uint32_t tancar_adreça_d_Internet(mp_obj_t VALOR) {
    size_t durada_VALOR; const char *SMS=mp_obj_str_get_data(VALOR,&durada_VALOR);
    unsigned 현재위치=0; uint32_t Adreça=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALOR=0,dígit_COMPT=0;
        while(현재위치<durada_VALOR&&SMS[현재위치]>='0'&&SMS[현재위치]<='9') {
            VALOR=VALOR*10+SMS[현재위치++]-'0'; if(++dígit_COMPT>3||VALOR>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!dígit_COMPT)mp_raise_OSError(MP_EINVAL);
        Adreça=Adreça<<8|VALOR;
        if(부분<3&&(현재위치>=durada_VALOR||SMS[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=durada_VALOR)mp_raise_OSError(MP_EINVAL);
    return Adreça;
}
static mp_obj_t 전문주소전송(size_t introducció_COMPT, const mp_obj_t *arg_MATRIU) {
    (void)introducció_COMPT; uint32_t Adreça=tancar_adreça_d_Internet(arg_MATRIU[1]);
    int número_de_port=mp_obj_get_int(arg_MATRIU[2]);if(número_de_port<1||número_de_port>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t dades;mp_get_buffer_raise(arg_MATRIU[3],&dades,MP_BUFFER_READ);
    struct pk_sockaddr_in objectiu={0};objectiu.sin_family=AF_INET;objectiu.sin_port=pk_htons(número_de_port);objectiu.sin_addr.s_addr=pk_htonl(Adreça);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(arg_MATRIU[0]),(uintptr_t)dades.buf,dades.len,0,(uintptr_t)&objectiu,sizeof(objectiu))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t arxiu_control_7f4cdfd5) {
    unsigned char dades[512]; struct pk_sockaddr_in homòleg_VALOR; pk_socklen_t durada_dades = sizeof(homòleg_VALOR);
    intptr_t Mida = 결과검사(사용자호출(35, mp_obj_get_int(arxiu_control_7f4cdfd5), (uintptr_t)dades, 512, 0, (uintptr_t)&homòleg_VALOR, (uintptr_t)&durada_dades));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(dades, Mida), MP_OBJ_NEW_SMALL_INT(pk_htons(homòleg_VALOR.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Tanca(mp_obj_t arxiu_control_7f4cdfd5) { 결과검사(사용자호출(4, mp_obj_get_int(arxiu_control_7f4cdfd5), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Tanca_OBJ, UDP_Tanca);
static mp_obj_t crear_flux(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,núvol_Família,flux_xarxa,flux_protocol_de_transport,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,crear_flux);
static mp_obj_t CONNECTA_flux(mp_obj_t extrem,mp_obj_t ADREÇA_SMS,mp_obj_t INDEX) {
    int número_de_port=mp_obj_get_int(INDEX); if(número_de_port<1||número_de_port>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 Adreça={0}; Adreça.ADREÇA_Família=núvol_Família;
    Adreça.número_de_port=망차례짧은수(número_de_port); Adreça.adreça_d_Internet.ADREÇA_VALOR=망차례정수(tancar_adreça_d_Internet(ADREÇA_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(extrem),(uintptr_t)&Adreça,sizeof(Adreça),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(flux_Connector_objecte,CONNECTA_flux);
static mp_obj_t tancar_flux(mp_obj_t extrem,mp_obj_t 한도) {
    int durada_VALOR=mp_obj_get_int(한도); if(durada_VALOR<1||durada_VALOR>512)mp_raise_OSError(MP_EINVAL);
    unsigned char dades[512];
    intptr_t element_COMPT=결과검사(사용자호출(2,mp_obj_get_int(extrem),(uintptr_t)dades,durada_VALOR,0,0,0));
    return mp_obj_new_bytes(dades,element_COMPT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(flux_Lector_objecte,tancar_flux);
static mp_obj_t escriure_flux(mp_obj_t extrem,mp_obj_t contingut_VALOR) {
    mp_buffer_info_t dades; mp_get_buffer_raise(contingut_VALOR,&dades,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(extrem),(uintptr_t)dades.buf,dades.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(flux_Writer_objecte,escriure_flux);
static mp_obj_t 잠시기다리기(mp_obj_t Hora_VALOR) {
    결과검사(사용자호출(17,mp_obj_get_int(Hora_VALOR),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Espera_objecte,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Nom) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)camí_arg(Nom),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Crear_directori(mp_obj_t Nom) {
    결과검사(사용자호출(18,(uintptr_t)camí_arg(Nom),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(directori_autor_objecte,Crear_directori);
static mp_obj_t suprimir_directori(mp_obj_t Nom) {
    결과검사(사용자호출(18,(uintptr_t)camí_arg(Nom),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,suprimir_directori);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&flux_Connector_objecte) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&flux_Lector_objecte) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&flux_Writer_objecte) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&Espera_objecte) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&directori_autor_objecte) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&arxiu_Lector_objecte) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&arxiu_Writer_objecte) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Rellotge_objecte) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_crear_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_enviar_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Tanca_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
