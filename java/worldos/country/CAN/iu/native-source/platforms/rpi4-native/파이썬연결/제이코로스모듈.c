// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *aqqut_aturniqarnirainiq(mp_obj_t atuutilik) {
    size_t 개수; const char *aqqut = mp_obj_str_get_data(atuutilik, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!aqqut[순번]) mp_raise_OSError(MP_EINVAL);
    return aqqut;
}
static mp_obj_t 파일읽기(mp_obj_t atiq) {
    intptr_t ini_nuuttarut = 결과검사(사용자호출(3, (uintptr_t)aqqut_aturniqarnirainiq(atiq), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t anininga = 결과검사(사용자호출(9, ini_nuuttarut, 0, 0, 0, 0, 0));
        vstr_t titiqqat; vstr_init_len(&titiqqat, anininga);
        intptr_t 결과 = 사용자호출(2, ini_nuuttarut, (uintptr_t)titiqqat.buf, anininga, 0, 0, 0);
        결과검사(결과); titiqqat.len = 결과;
        mp_obj_t atuutilik = mp_obj_new_bytes_from_vstr(&titiqqat);
        nlr_pop(); 사용자호출(4, ini_nuuttarut, 0, 0, 0, 0, 0); return atuutilik;
    }
    사용자호출(4, ini_nuuttarut, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ini_Uqalimaarut_kisu, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t anininga=mp_obj_get_int(한도);
    if(anininga<0||anininga>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t titiqqat; vstr_init_len(&titiqqat,anininga);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)titiqqat.buf,anininga,0,0,0);
    if(개수<0) { vstr_clear(&titiqqat); 결과검사(개수); }
    titiqqat.len=개수; return mp_obj_new_bytes_from_vstr(&titiqqat);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t titiraq_ini(mp_obj_t atiq, mp_obj_t Ilulingit_atuutilik) {
    const char *aqqut = aqqut_aturniqarnirainiq(atiq);
    mp_buffer_info_t titiqqat; mp_get_buffer_raise(Ilulingit_atuutilik, &titiqqat, MP_BUFFER_READ);
    if (titiqqat.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ini_nuuttarut = 결과검사(사용자호출(3, (uintptr_t)aqqut, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ini_nuuttarut, (uintptr_t)titiqqat.buf, titiqqat.len, 0, 0, 0);
    사용자호출(4, ini_nuuttarut, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ini_Titiqqaliurut_kisu, titiraq_ini);
static mp_obj_t sanirvalli_ini(mp_obj_t atiq) { 결과검사(사용자호출(11, (uintptr_t)aqqut_aturniqarnirainiq(atiq), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, sanirvalli_ini);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *aturniqarnirainiq_array) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(aturniqarnirainiq_array[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t anininga[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, anininga);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t qaujisaut_atuutilik(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(qaujisaut_kisu, qaujisaut_atuutilik);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ini_nuuttarut = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, ini_nuuttarut, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, ini_nuuttarut, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(ini_nuuttarut);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t ini_nuuttarut, mp_obj_t 접속번호, mp_obj_t Ilulingit_atuutilik) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t titiqqat; mp_get_buffer_raise(Ilulingit_atuutilik, &titiqqat, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ini_nuuttarut), (uintptr_t)titiqqat.buf, titiqqat.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t atuutilik) {
    size_t takininga_atuutilik; const char *titiqqaq=mp_obj_str_get_data(atuutilik,&takininga_atuutilik);
    unsigned 현재위치=0; uint32_t turaarut=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned atuutilik=0,숫자수=0;
        while(현재위치<takininga_atuutilik&&titiqqaq[현재위치]>='0'&&titiqqaq[현재위치]<='9') {
            atuutilik=atuutilik*10+titiqqaq[현재위치++]-'0'; if(++숫자수>3||atuutilik>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        turaarut=turaarut<<8|atuutilik;
        if(부분<3&&(현재위치>=takininga_atuutilik||titiqqaq[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=takininga_atuutilik)mp_raise_OSError(MP_EINVAL);
    return turaarut;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *aturniqarnirainiq_array) {
    (void)항목수; uint32_t turaarut=인터넷주소읽기(aturniqarnirainiq_array[1]);
    int 접속번호=mp_obj_get_int(aturniqarnirainiq_array[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t titiqqat;mp_get_buffer_raise(aturniqarnirainiq_array[3],&titiqqat,MP_BUFFER_READ);
    struct pk_sockaddr_in turaagaq={0};turaagaq.sin_family=AF_INET;turaagaq.sin_port=pk_htons(접속번호);turaagaq.sin_addr.s_addr=pk_htonl(turaarut);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(aturniqarnirainiq_array[0]),(uintptr_t)titiqqat.buf,titiqqat.len,0,(uintptr_t)&turaagaq,sizeof(turaagaq))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ini_nuuttarut) {
    unsigned char titiqqat[512]; struct pk_sockaddr_in ilagijaujuq_atuutilik; pk_socklen_t takininga_titiqqat = sizeof(ilagijaujuq_atuutilik);
    intptr_t anininga = 결과검사(사용자호출(35, mp_obj_get_int(ini_nuuttarut), (uintptr_t)titiqqat, 512, 0, (uintptr_t)&ilagijaujuq_atuutilik, (uintptr_t)&takininga_titiqqat));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(titiqqat, anininga), MP_OBJ_NEW_SMALL_INT(pk_htons(ilagijaujuq_atuutilik.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t ini_nuuttarut) { 결과검사(사용자호출(4, mp_obj_get_int(ini_nuuttarut), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t matuirli_ingirrania_aulataup(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,cloud_illumiuqatigiit,ingirrania_aulataup_Kasuqatigiitsimajut,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,matuirli_ingirrania_aulataup);
static mp_obj_t kasurli_ingirrania_aulataup(mp_obj_t 종단,mp_obj_t turaarut_titiqqaq,mp_obj_t nalunaiqsimavik) {
    int 접속번호=mp_obj_get_int(nalunaiqsimavik); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 turaarut={0}; turaarut.turaarut_illumiuqatigiit=cloud_illumiuqatigiit;
    turaarut.접속번호=망차례짧은수(접속번호); turaarut.Ikiaqqivikkut_turaarut.turaarut_atuutilik=Kasuqatigiitsimajut_naasaut(인터넷주소읽기(turaarut_titiqqaq));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&turaarut,sizeof(turaarut),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ingirrania_aulataup_kasurut_kisu,kasurli_ingirrania_aulataup);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int takininga_atuutilik=mp_obj_get_int(한도); if(takininga_atuutilik<1||takininga_atuutilik>512)mp_raise_OSError(MP_EINVAL);
    unsigned char titiqqat[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)titiqqat,takininga_atuutilik,0,0,0));
    return mp_obj_new_bytes(titiqqat,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ingirrania_aulataup_Uqalimaarut_kisu,흐름읽기);
static mp_obj_t titiraq_ingirrania_aulataup(mp_obj_t 종단,mp_obj_t Ilulingit_atuutilik) {
    mp_buffer_info_t titiqqat; mp_get_buffer_raise(Ilulingit_atuutilik,&titiqqat,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)titiqqat.buf,titiqqat.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ingirrania_aulataup_Titiqqaliurut_kisu,titiraq_ingirrania_aulataup);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t atiq) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)aqqut_aturniqarnirainiq(atiq),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t 폴더만들기(mp_obj_t atiq) {
    결과검사(사용자호출(18,(uintptr_t)aqqut_aturniqarnirainiq(atiq),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,폴더만들기);
static mp_obj_t sanirvalli_tukimuagutiit(mp_obj_t atiq) {
    결과검사(사용자호출(18,(uintptr_t)aqqut_aturniqarnirainiq(atiq),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,sanirvalli_tukimuagutiit);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ingirrania_aulataup_kasurut_kisu) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ingirrania_aulataup_Uqalimaarut_kisu) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&ingirrania_aulataup_Titiqqaliurut_kisu) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ini_Uqalimaarut_kisu) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&ini_Titiqqaliurut_kisu) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&qaujisaut_kisu) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
