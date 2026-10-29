// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *tsela_akumente(mp_obj_t boleng) {
    size_t 개수; const char *Tsejana = mp_obj_str_get_data(boleng, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!Tsejana[순번]) mp_raise_OSError(MP_EINVAL);
    return Tsejana;
}
static mp_obj_t 파일읽기(mp_obj_t Leina) {
    intptr_t faele_tshwaro = 결과검사(사용자호출(3, (uintptr_t)tsela_akumente(Leina), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Bogolo = 결과검사(사용자호출(9, faele_tshwaro, 0, 0, 0, 0, 0));
        vstr_t data; vstr_init_len(&data, Bogolo);
        intptr_t 결과 = 사용자호출(2, faele_tshwaro, (uintptr_t)data.buf, Bogolo, 0, 0, 0);
        결과검사(결과); data.len = 결과;
        mp_obj_t boleng = mp_obj_new_bytes_from_vstr(&data);
        nlr_pop(); 사용자호출(4, faele_tshwaro, 0, 0, 0, 0, 0); return boleng;
    }
    사용자호출(4, faele_tshwaro, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(faele_mmadi_selo, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Bogolo=mp_obj_get_int(한도);
    if(Bogolo<0||Bogolo>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t data; vstr_init_len(&data,Bogolo);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)data.buf,Bogolo,0,0,0);
    if(개수<0) { vstr_clear(&data); 결과검사(개수); }
    data.len=개수; return mp_obj_new_bytes_from_vstr(&data);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t ngwala_faele(mp_obj_t Leina, mp_obj_t Diteng_boleng) {
    const char *Tsejana = tsela_akumente(Leina);
    mp_buffer_info_t data; mp_get_buffer_raise(Diteng_boleng, &data, MP_BUFFER_READ);
    if (data.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t faele_tshwaro = 결과검사(사용자호출(3, (uintptr_t)Tsejana, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, faele_tshwaro, (uintptr_t)data.buf, data.len, 0, 0, 0);
    사용자호출(4, faele_tshwaro, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(faele_Sengwadi_selo, ngwala_faele);
static mp_obj_t tloša_faele(mp_obj_t Leina) { 결과검사(사용자호출(11, (uintptr_t)tsela_akumente(Leina), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, tloša_faele);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *akumente_arei) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(akumente_arei[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Bogolo[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Bogolo);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t sešupanako_boleng(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(sešupanako_selo, sešupanako_boleng);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t faele_tshwaro = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, faele_tshwaro, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, faele_tshwaro, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(faele_tshwaro);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t faele_tshwaro, mp_obj_t 접속번호, mp_obj_t Diteng_boleng) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data; mp_get_buffer_raise(Diteng_boleng, &data, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(faele_tshwaro), (uintptr_t)data.buf, data.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t boleng) {
    size_t botelele_boleng; const char *Sengwalwa=mp_obj_str_get_data(boleng,&botelele_boleng);
    unsigned 현재위치=0; uint32_t atrese=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned boleng=0,숫자수=0;
        while(현재위치<botelele_boleng&&Sengwalwa[현재위치]>='0'&&Sengwalwa[현재위치]<='9') {
            boleng=boleng*10+Sengwalwa[현재위치++]-'0'; if(++숫자수>3||boleng>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        atrese=atrese<<8|boleng;
        if(부분<3&&(현재위치>=botelele_boleng||Sengwalwa[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=botelele_boleng)mp_raise_OSError(MP_EINVAL);
    return atrese;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *akumente_arei) {
    (void)항목수; uint32_t atrese=인터넷주소읽기(akumente_arei[1]);
    int 접속번호=mp_obj_get_int(akumente_arei[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data;mp_get_buffer_raise(akumente_arei[3],&data,MP_BUFFER_READ);
    struct pk_sockaddr_in nepo={0};nepo.sin_family=AF_INET;nepo.sin_port=pk_htons(접속번호);nepo.sin_addr.s_addr=pk_htonl(atrese);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(akumente_arei[0]),(uintptr_t)data.buf,data.len,0,(uintptr_t)&nepo,sizeof(nepo))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t faele_tshwaro) {
    unsigned char data[512]; struct pk_sockaddr_in sedirišwa_sa_legoro_le_tee_boleng; pk_socklen_t botelele_data = sizeof(sedirišwa_sa_legoro_le_tee_boleng);
    intptr_t Bogolo = 결과검사(사용자호출(35, mp_obj_get_int(faele_tshwaro), (uintptr_t)data, 512, 0, (uintptr_t)&sedirišwa_sa_legoro_le_tee_boleng, (uintptr_t)&botelele_data));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(data, Bogolo), MP_OBJ_NEW_SMALL_INT(pk_htons(sedirišwa_sa_legoro_le_tee_boleng.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t faele_tshwaro) { 결과검사(사용자호출(4, mp_obj_get_int(faele_tshwaro), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t bula_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,Inthanete_Lapa,Stream_Netweke,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,bula_Stream);
static mp_obj_t KGOKAGANYA_Stream(mp_obj_t 종단,mp_obj_t atrese_SMS,mp_obj_t lokela) {
    int 접속번호=mp_obj_get_int(lokela); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 atrese={0}; atrese.atrese_Lapa=Inthanete_Lapa;
    atrese.접속번호=망차례짧은수(접속번호); atrese.atrese_ya_Inthanete.atrese_boleng=Netweke_palotlalo(인터넷주소읽기(atrese_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&atrese,sizeof(atrese),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_sekgokaganyi_selo,KGOKAGANYA_Stream);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int botelele_boleng=mp_obj_get_int(한도); if(botelele_boleng<1||botelele_boleng>512)mp_raise_OSError(MP_EINVAL);
    unsigned char data[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)data,botelele_boleng,0,0,0));
    return mp_obj_new_bytes(data,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_mmadi_selo,흐름읽기);
static mp_obj_t ngwala_Stream(mp_obj_t 종단,mp_obj_t Diteng_boleng) {
    mp_buffer_info_t data; mp_get_buffer_raise(Diteng_boleng,&data,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)data.buf,data.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Sengwadi_selo,ngwala_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Leina) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)tsela_akumente(Leina),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t 폴더만들기(mp_obj_t Leina) {
    결과검사(사용자호출(18,(uintptr_t)tsela_akumente(Leina),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,폴더만들기);
static mp_obj_t tloša_lelokelelo(mp_obj_t Leina) {
    결과검사(사용자호출(18,(uintptr_t)tsela_akumente(Leina),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,tloša_lelokelelo);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_sekgokaganyi_selo) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_mmadi_selo) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Sengwadi_selo) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&faele_mmadi_selo) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&faele_Sengwadi_selo) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&sešupanako_selo) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
