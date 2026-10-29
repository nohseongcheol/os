// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *tsela_Thulaganyo(mp_obj_t Boleng) {
    size_t 개수; const char *tsela = mp_obj_str_get_data(Boleng, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!tsela[순번]) mp_raise_OSError(MP_EINVAL);
    return tsela;
}
static mp_obj_t 파일읽기(mp_obj_t leina) {
    intptr_t faele_mokgwakamogelo = 결과검사(사용자호출(3, (uintptr_t)tsela_Thulaganyo(leina), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t lekanya = 결과검사(사용자호출(9, faele_mokgwakamogelo, 0, 0, 0, 0, 0));
        vstr_t tshedimosetso; vstr_init_len(&tshedimosetso, lekanya);
        intptr_t 결과 = 사용자호출(2, faele_mokgwakamogelo, (uintptr_t)tshedimosetso.buf, lekanya, 0, 0, 0);
        결과검사(결과); tshedimosetso.len = 결과;
        mp_obj_t Boleng = mp_obj_new_bytes_from_vstr(&tshedimosetso);
        nlr_pop(); 사용자호출(4, faele_mokgwakamogelo, 0, 0, 0, 0, 0); return Boleng;
    }
    사용자호출(4, faele_mokgwakamogelo, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(faele_mmuisi_selwana, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t lekanya=mp_obj_get_int(한도);
    if(lekanya<0||lekanya>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t tshedimosetso; vstr_init_len(&tshedimosetso,lekanya);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)tshedimosetso.buf,lekanya,0,0,0);
    if(개수<0) { vstr_clear(&tshedimosetso); 결과검사(개수); }
    tshedimosetso.len=개수; return mp_obj_new_bytes_from_vstr(&tshedimosetso);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t kwala_faele(mp_obj_t leina, mp_obj_t Diteng_Boleng) {
    const char *tsela = tsela_Thulaganyo(leina);
    mp_buffer_info_t tshedimosetso; mp_get_buffer_raise(Diteng_Boleng, &tshedimosetso, MP_BUFFER_READ);
    if (tshedimosetso.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t faele_mokgwakamogelo = 결과검사(사용자호출(3, (uintptr_t)tsela, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, faele_mokgwakamogelo, (uintptr_t)tshedimosetso.buf, tshedimosetso.len, 0, 0, 0);
    사용자호출(4, faele_mokgwakamogelo, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(faele_Sekwadi_selwana, kwala_faele);
static mp_obj_t tlosa_faele(mp_obj_t leina) { 결과검사(사용자호출(11, (uintptr_t)tsela_Thulaganyo(leina), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, tlosa_faele);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *Thulaganyo_setlhopha) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(Thulaganyo_setlhopha[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t lekanya[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, lekanya);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t tshupanako_Boleng(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(tshupanako_selwana, tshupanako_Boleng);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t faele_mokgwakamogelo = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, faele_mokgwakamogelo, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, faele_mokgwakamogelo, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(faele_mokgwakamogelo);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t faele_mokgwakamogelo, mp_obj_t 접속번호, mp_obj_t Diteng_Boleng) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t tshedimosetso; mp_get_buffer_raise(Diteng_Boleng, &tshedimosetso, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(faele_mokgwakamogelo), (uintptr_t)tshedimosetso.buf, tshedimosetso.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t Boleng) {
    size_t boleele_Boleng; const char *SMS=mp_obj_str_get_data(Boleng,&boleele_Boleng);
    unsigned 현재위치=0; uint32_t aterese=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned Boleng=0,숫자수=0;
        while(현재위치<boleele_Boleng&&SMS[현재위치]>='0'&&SMS[현재위치]<='9') {
            Boleng=Boleng*10+SMS[현재위치++]-'0'; if(++숫자수>3||Boleng>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        aterese=aterese<<8|Boleng;
        if(부분<3&&(현재위치>=boleele_Boleng||SMS[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=boleele_Boleng)mp_raise_OSError(MP_EINVAL);
    return aterese;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *Thulaganyo_setlhopha) {
    (void)항목수; uint32_t aterese=인터넷주소읽기(Thulaganyo_setlhopha[1]);
    int 접속번호=mp_obj_get_int(Thulaganyo_setlhopha[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t tshedimosetso;mp_get_buffer_raise(Thulaganyo_setlhopha[3],&tshedimosetso,MP_BUFFER_READ);
    struct pk_sockaddr_in setotwa={0};setotwa.sin_family=AF_INET;setotwa.sin_port=pk_htons(접속번호);setotwa.sin_addr.s_addr=pk_htonl(aterese);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(Thulaganyo_setlhopha[0]),(uintptr_t)tshedimosetso.buf,tshedimosetso.len,0,(uintptr_t)&setotwa,sizeof(setotwa))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t faele_mokgwakamogelo) {
    unsigned char tshedimosetso[512]; struct pk_sockaddr_in semphato_Boleng; pk_socklen_t boleele_tshedimosetso = sizeof(semphato_Boleng);
    intptr_t lekanya = 결과검사(사용자호출(35, mp_obj_get_int(faele_mokgwakamogelo), (uintptr_t)tshedimosetso, 512, 0, (uintptr_t)&semphato_Boleng, (uintptr_t)&boleele_tshedimosetso));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(tshedimosetso, lekanya), MP_OBJ_NEW_SMALL_INT(pk_htons(semphato_Boleng.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t faele_mokgwakamogelo) { 결과검사(사용자호출(4, mp_obj_get_int(faele_mokgwakamogelo), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t bula_moela(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,tlelaote_Lelapa,moela_Neteweke,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,bula_moela);
static mp_obj_t Golaganya_moela(mp_obj_t 종단,mp_obj_t aterese_SMS,mp_obj_t tshupane) {
    int 접속번호=mp_obj_get_int(tshupane); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 aterese={0}; aterese.aterese_Lelapa=tlelaote_Lelapa;
    aterese.접속번호=망차례짧은수(접속번호); aterese.aterese_ya_Inthanete.aterese_Boleng=Neteweke_Palotlalo(인터넷주소읽기(aterese_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&aterese,sizeof(aterese),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(moela_segolaganyi_selwana,Golaganya_moela);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int boleele_Boleng=mp_obj_get_int(한도); if(boleele_Boleng<1||boleele_Boleng>512)mp_raise_OSError(MP_EINVAL);
    unsigned char tshedimosetso[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)tshedimosetso,boleele_Boleng,0,0,0));
    return mp_obj_new_bytes(tshedimosetso,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(moela_mmuisi_selwana,흐름읽기);
static mp_obj_t kwala_moela(mp_obj_t 종단,mp_obj_t Diteng_Boleng) {
    mp_buffer_info_t tshedimosetso; mp_get_buffer_raise(Diteng_Boleng,&tshedimosetso,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)tshedimosetso.buf,tshedimosetso.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(moela_Sekwadi_selwana,kwala_moela);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t leina) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)tsela_Thulaganyo(leina),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t tlhama_Lenaneofaele(mp_obj_t leina) {
    결과검사(사용자호출(18,(uintptr_t)tsela_Thulaganyo(leina),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,tlhama_Lenaneofaele);
static mp_obj_t tlosa_Lenaneofaele(mp_obj_t leina) {
    결과검사(사용자호출(18,(uintptr_t)tsela_Thulaganyo(leina),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,tlosa_Lenaneofaele);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&moela_segolaganyi_selwana) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&moela_mmuisi_selwana) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&moela_Sekwadi_selwana) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&faele_mmuisi_selwana) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&faele_Sekwadi_selwana) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&tshupanako_selwana) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
