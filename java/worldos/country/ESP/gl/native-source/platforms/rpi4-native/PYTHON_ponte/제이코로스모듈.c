// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t RESULTANTE) { if (RESULTANTE < 0) mp_raise_OSError(-RESULTANTE); return RESULTANTE; }
static const char *camiño_argumento(mp_obj_t VALOR) {
    size_t elemento_CONTAR; const char *CAMIÑO = mp_obj_str_get_data(VALOR, &elemento_CONTAR);
    if (!elemento_CONTAR || elemento_CONTAR > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < elemento_CONTAR; 순번++) if (!CAMIÑO[순번]) mp_raise_OSError(MP_EINVAL);
    return CAMIÑO;
}
static mp_obj_t 파일읽기(mp_obj_t Nome) {
    intptr_t Ficheiro_agarradoira = 결과검사(사용자호출(3, (uintptr_t)camiño_argumento(Nome), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Tamaño = 결과검사(사용자호출(9, Ficheiro_agarradoira, 0, 0, 0, 0, 0));
        vstr_t datos; vstr_init_len(&datos, Tamaño);
        intptr_t RESULTANTE = 사용자호출(2, Ficheiro_agarradoira, (uintptr_t)datos.buf, Tamaño, 0, 0, 0);
        결과검사(RESULTANTE); datos.len = RESULTANTE;
        mp_obj_t VALOR = mp_obj_new_bytes_from_vstr(&datos);
        nlr_pop(); 사용자호출(4, Ficheiro_agarradoira, 0, 0, 0, 0, 0); return VALOR;
    }
    사용자호출(4, Ficheiro_agarradoira, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Ficheiro_Lector_obxecto, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Tamaño=mp_obj_get_int(한도);
    if(Tamaño<0||Tamaño>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t datos; vstr_init_len(&datos,Tamaño);
    intptr_t elemento_CONTAR=사용자호출(2,0,(uintptr_t)datos.buf,Tamaño,0,0,0);
    if(elemento_CONTAR<0) { vstr_clear(&datos); 결과검사(elemento_CONTAR); }
    datos.len=elemento_CONTAR; return mp_obj_new_bytes_from_vstr(&datos);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t escribir_Ficheiro(mp_obj_t Nome, mp_obj_t Contido_VALOR) {
    const char *CAMIÑO = camiño_argumento(Nome);
    mp_buffer_info_t datos; mp_get_buffer_raise(Contido_VALOR, &datos, MP_BUFFER_READ);
    if (datos.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t Ficheiro_agarradoira = 결과검사(사용자호출(3, (uintptr_t)CAMIÑO, 577, 0, 0, 0, 0));
    intptr_t introdución_CONTAR = 사용자호출(1, Ficheiro_agarradoira, (uintptr_t)datos.buf, datos.len, 0, 0, 0);
    사용자호출(4, Ficheiro_agarradoira, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(introdución_CONTAR));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Ficheiro_Writer_obxecto, escribir_Ficheiro);
static mp_obj_t eliminar_Ficheiro(mp_obj_t Nome) { 결과검사(사용자호출(11, (uintptr_t)camiño_argumento(Nome), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, eliminar_Ficheiro);
static mp_obj_t 사각형그리기(size_t elemento_CONTAR, const mp_obj_t *argumento_MATRIZ) {
    (void)elemento_CONTAR; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argumento_MATRIZ[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Tamaño[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Tamaño);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Reloxo_VALOR(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Reloxo_obxecto, Reloxo_VALOR);
static mp_obj_t UDP_abrir(mp_obj_t número_do_porto) {
    int datos_cargo = mp_obj_get_int(número_do_porto); if (datos_cargo < 0 || datos_cargo > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t Ficheiro_agarradoira = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(datos_cargo); 첫째값.sin_addr.s_addr = 0;
    intptr_t RESULTANTE = 사용자호출(33, Ficheiro_agarradoira, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (RESULTANTE < 0) { 사용자호출(4, Ficheiro_agarradoira, 0, 0, 0, 0, 0); 결과검사(RESULTANTE); }
    return mp_obj_new_int(Ficheiro_agarradoira);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_abrir_OBJ, UDP_abrir);
static mp_obj_t UDP_enviar(mp_obj_t Ficheiro_agarradoira, mp_obj_t número_do_porto, mp_obj_t Contido_VALOR) {
    int datos_cargo = mp_obj_get_int(número_do_porto); if (datos_cargo < 1 || datos_cargo > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t datos; mp_get_buffer_raise(Contido_VALOR, &datos, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(datos_cargo); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(Ficheiro_agarradoira), (uintptr_t)datos.buf, datos.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_enviar_OBJ, UDP_enviar);
static uint32_t 인터넷주소읽기(mp_obj_t VALOR) {
    size_t duración_VALOR; const char *Texto=mp_obj_str_get_data(VALOR,&duración_VALOR);
    unsigned ao_corrente_cargo=0; uint32_t ENDEREZO=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALOR=0,díxito_CONTAR=0;
        while(ao_corrente_cargo<duración_VALOR&&Texto[ao_corrente_cargo]>='0'&&Texto[ao_corrente_cargo]<='9') {
            VALOR=VALOR*10+Texto[ao_corrente_cargo++]-'0'; if(++díxito_CONTAR>3||VALOR>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!díxito_CONTAR)mp_raise_OSError(MP_EINVAL);
        ENDEREZO=ENDEREZO<<8|VALOR;
        if(부분<3&&(ao_corrente_cargo>=duración_VALOR||Texto[ao_corrente_cargo++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(ao_corrente_cargo!=duración_VALOR)mp_raise_OSError(MP_EINVAL);
    return ENDEREZO;
}
static mp_obj_t 전문주소전송(size_t introdución_CONTAR, const mp_obj_t *argumento_MATRIZ) {
    (void)introdución_CONTAR; uint32_t ENDEREZO=인터넷주소읽기(argumento_MATRIZ[1]);
    int número_do_porto=mp_obj_get_int(argumento_MATRIZ[2]);if(número_do_porto<1||número_do_porto>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t datos;mp_get_buffer_raise(argumento_MATRIZ[3],&datos,MP_BUFFER_READ);
    struct pk_sockaddr_in obxectivo_VALOR={0};obxectivo_VALOR.sin_family=AF_INET;obxectivo_VALOR.sin_port=pk_htons(número_do_porto);obxectivo_VALOR.sin_addr.s_addr=pk_htonl(ENDEREZO);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argumento_MATRIZ[0]),(uintptr_t)datos.buf,datos.len,0,(uintptr_t)&obxectivo_VALOR,sizeof(obxectivo_VALOR))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t Ficheiro_agarradoira) {
    unsigned char datos[512]; struct pk_sockaddr_in punto_VALOR; pk_socklen_t duración_datos = sizeof(punto_VALOR);
    intptr_t Tamaño = 결과검사(사용자호출(35, mp_obj_get_int(Ficheiro_agarradoira), (uintptr_t)datos, 512, 0, (uintptr_t)&punto_VALOR, (uintptr_t)&duración_datos));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(datos, Tamaño), MP_OBJ_NEW_SMALL_INT(pk_htons(punto_VALOR.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_peche(mp_obj_t Ficheiro_agarradoira) { 결과검사(사용자호출(4, mp_obj_get_int(Ficheiro_agarradoira), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_peche_OBJ, UDP_peche);
static mp_obj_t abrir_fluxo(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,nube_Familia,fluxo_Rede,fluxo_protocolo_de_transporte,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,abrir_fluxo);
static mp_obj_t CONECTAR_fluxo(mp_obj_t extremo,mp_obj_t ENDEREZO_SMS,mp_obj_t ÍNDICE) {
    int número_do_porto=mp_obj_get_int(ÍNDICE); if(número_do_porto<1||número_do_porto>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ENDEREZO={0}; ENDEREZO.ENDEREZO_Familia=nube_Familia;
    ENDEREZO.número_do_porto=망차례짧은수(número_do_porto); ENDEREZO.enderezo_de_internet.ENDEREZO_VALOR=Rede_número_enteiro(인터넷주소읽기(ENDEREZO_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(extremo),(uintptr_t)&ENDEREZO,sizeof(ENDEREZO),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(fluxo_Conector_obxecto,CONECTAR_fluxo);
static mp_obj_t 흐름읽기(mp_obj_t extremo,mp_obj_t 한도) {
    int duración_VALOR=mp_obj_get_int(한도); if(duración_VALOR<1||duración_VALOR>512)mp_raise_OSError(MP_EINVAL);
    unsigned char datos[512];
    intptr_t elemento_CONTAR=결과검사(사용자호출(2,mp_obj_get_int(extremo),(uintptr_t)datos,duración_VALOR,0,0,0));
    return mp_obj_new_bytes(datos,elemento_CONTAR);
}
static MP_DEFINE_CONST_FUN_OBJ_2(fluxo_Lector_obxecto,흐름읽기);
static mp_obj_t escribir_fluxo(mp_obj_t extremo,mp_obj_t Contido_VALOR) {
    mp_buffer_info_t datos; mp_get_buffer_raise(Contido_VALOR,&datos,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(extremo),(uintptr_t)datos.buf,datos.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(fluxo_Writer_obxecto,escribir_fluxo);
static mp_obj_t 잠시기다리기(mp_obj_t hora_VALOR) {
    결과검사(사용자호출(17,mp_obj_get_int(hora_VALOR),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(agarda_obxecto,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Nome) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)camiño_argumento(Nome),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t crear_directorio(mp_obj_t Nome) {
    결과검사(사용자호출(18,(uintptr_t)camiño_argumento(Nome),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(directorio_creador_obxecto,crear_directorio);
static mp_obj_t eliminar_directorio(mp_obj_t Nome) {
    결과검사(사용자호출(18,(uintptr_t)camiño_argumento(Nome),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,eliminar_directorio);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&fluxo_Conector_obxecto) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&fluxo_Lector_obxecto) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&fluxo_Writer_obxecto) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&agarda_obxecto) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&directorio_creador_obxecto) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Ficheiro_Lector_obxecto) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Ficheiro_Writer_obxecto) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Reloxo_obxecto) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_abrir_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_enviar_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_peche_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
