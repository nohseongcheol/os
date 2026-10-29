// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t չափ) { if (չափ < 0) mp_raise_OSError(-չափ); return չափ; }
static const char *ուղի_արգումենտ(mp_obj_t արժեք) {
    size_t 개수; const char *Ճանապարհ = mp_obj_str_get_data(արժեք, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!Ճանապարհ[순번]) mp_raise_OSError(MP_EINVAL);
    return Ճանապարհ;
}
static mp_obj_t 파일읽기(mp_obj_t Անուն) {
    intptr_t նիշք_բռնակ = 결과검사(사용자호출(3, (uintptr_t)ուղի_արգումենտ(Անուն), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Չափս = 결과검사(사용자호출(9, նիշք_բռնակ, 0, 0, 0, 0, 0));
        vstr_t տվյալ; vstr_init_len(&տվյալ, Չափս);
        intptr_t չափ = 사용자호출(2, նիշք_բռնակ, (uintptr_t)տվյալ.buf, Չափս, 0, 0, 0);
        결과검사(չափ); տվյալ.len = չափ;
        mp_obj_t արժեք = mp_obj_new_bytes_from_vstr(&տվյալ);
        nlr_pop(); 사용자호출(4, նիշք_բռնակ, 0, 0, 0, 0, 0); return արժեք;
    }
    사용자호출(4, նիշք_բռնակ, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(նիշք_Ընթերցիչ_առարկա, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Չափս=mp_obj_get_int(한도);
    if(Չափս<0||Չափս>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t տվյալ; vstr_init_len(&տվյալ,Չափս);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)տվյալ.buf,Չափս,0,0,0);
    if(개수<0) { vstr_clear(&տվյալ); 결과검사(개수); }
    տվյալ.len=개수; return mp_obj_new_bytes_from_vstr(&տվյալ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t գրել_նիշք(mp_obj_t Անուն, mp_obj_t Բովանդակություն_արժեք) {
    const char *Ճանապարհ = ուղի_արգումենտ(Անուն);
    mp_buffer_info_t տվյալ; mp_get_buffer_raise(Բովանդակություն_արժեք, &տվյալ, MP_BUFFER_READ);
    if (տվյալ.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t նիշք_բռնակ = 결과검사(사용자호출(3, (uintptr_t)Ճանապարհ, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, նիշք_բռնակ, (uintptr_t)տվյալ.buf, տվյալ.len, 0, 0, 0);
    사용자호출(4, նիշք_բռնակ, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(նիշք_Գրող_առարկա, գրել_նիշք);
static mp_obj_t հեռացնել_նիշք(mp_obj_t Անուն) { 결과검사(사용자호출(11, (uintptr_t)ուղի_արգումենտ(Անուն), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, հեռացնել_նիշք);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *արգումենտ_ԶԱՆԳՎԱԾ) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(արգումենտ_ԶԱՆԳՎԱԾ[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Չափս[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Չափս);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Ժամացույց_արժեք(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Ժամացույց_առարկա, Ժամացույց_արժեք);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int տվյալ_դիրք = mp_obj_get_int(접속번호); if (տվյալ_դիրք < 0 || տվյալ_դիրք > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t նիշք_բռնակ = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(տվյալ_դիրք); 첫째값.sin_addr.s_addr = 0;
    intptr_t չափ = 사용자호출(33, նիշք_բռնակ, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (չափ < 0) { 사용자호출(4, նիշք_բռնակ, 0, 0, 0, 0, 0); 결과검사(չափ); }
    return mp_obj_new_int(նիշք_բռնակ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t նիշք_բռնակ, mp_obj_t 접속번호, mp_obj_t Բովանդակություն_արժեք) {
    int տվյալ_դիրք = mp_obj_get_int(접속번호); if (տվյալ_դիրք < 1 || տվյալ_դիրք > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t տվյալ; mp_get_buffer_raise(Բովանդակություն_արժեք, &տվյալ, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(տվյալ_դիրք); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(նիշք_բռնակ), (uintptr_t)տվյալ.buf, տվյալ.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t արժեք) {
    size_t տեւողություն_արժեք; const char *Տեքստ=mp_obj_str_get_data(արժեք,&տեւողություն_արժեք);
    unsigned 현재위치=0; uint32_t հասցե=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned արժեք=0,숫자수=0;
        while(현재위치<տեւողություն_արժեք&&Տեքստ[현재위치]>='0'&&Տեքստ[현재위치]<='9') {
            արժեք=արժեք*10+Տեքստ[현재위치++]-'0'; if(++숫자수>3||արժեք>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        հասցե=հասցե<<8|արժեք;
        if(부분<3&&(현재위치>=տեւողություն_արժեք||Տեքստ[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=տեւողություն_արժեք)mp_raise_OSError(MP_EINVAL);
    return հասցե;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *արգումենտ_ԶԱՆԳՎԱԾ) {
    (void)항목수; uint32_t հասցե=인터넷주소읽기(արգումենտ_ԶԱՆԳՎԱԾ[1]);
    int 접속번호=mp_obj_get_int(արգումենտ_ԶԱՆԳՎԱԾ[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t տվյալ;mp_get_buffer_raise(արգումենտ_ԶԱՆԳՎԱԾ[3],&տվյալ,MP_BUFFER_READ);
    struct pk_sockaddr_in թիրախ={0};թիրախ.sin_family=AF_INET;թիրախ.sin_port=pk_htons(접속번호);թիրախ.sin_addr.s_addr=pk_htonl(հասցե);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(արգումենտ_ԶԱՆԳՎԱԾ[0]),(uintptr_t)տվյալ.buf,տվյալ.len,0,(uintptr_t)&թիրախ,sizeof(թիրախ))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t նիշք_բռնակ) {
    unsigned char տվյալ[512]; struct pk_sockaddr_in հավասարազոր_սարք_արժեք; pk_socklen_t տեւողություն_տվյալ = sizeof(հավասարազոր_սարք_արժեք);
    intptr_t Չափս = 결과검사(사용자호출(35, mp_obj_get_int(նիշք_բռնակ), (uintptr_t)տվյալ, 512, 0, (uintptr_t)&հավասարազոր_սարք_արժեք, (uintptr_t)&տեւողություն_տվյալ));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(տվյալ, Չափս), MP_OBJ_NEW_SMALL_INT(pk_htons(հավասարազոր_սարք_արժեք.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t նիշք_բռնակ) { 결과검사(사용자호출(4, mp_obj_get_int(նիշք_բռնակ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t բացել_հոսք(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,ամպ_Ընտանիք,հոսք_Ցանց,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,բացել_հոսք);
static mp_obj_t Կապակցել_հոսք(mp_obj_t 종단,mp_obj_t հասցե_Գրվածք,mp_obj_t դասիչ) {
    int 접속번호=mp_obj_get_int(դասիչ); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 հասցե={0}; հասցե.հասցե_Ընտանիք=ամպ_Ընտանիք;
    հասցե.접속번호=망차례짧은수(접속번호); հասցե.համացանցի_հասցե.հասցե_արժեք=Ցանց_ամբողջ_թիվ(인터넷주소읽기(հասցե_Գրվածք));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&հասցե,sizeof(հասցե),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(հոսք_Կապակցիչ_առարկա,Կապակցել_հոսք);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int տեւողություն_արժեք=mp_obj_get_int(한도); if(տեւողություն_արժեք<1||տեւողություն_արժեք>512)mp_raise_OSError(MP_EINVAL);
    unsigned char տվյալ[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)տվյալ,տեւողություն_արժեք,0,0,0));
    return mp_obj_new_bytes(տվյալ,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(հոսք_Ընթերցիչ_առարկա,흐름읽기);
static mp_obj_t գրել_հոսք(mp_obj_t 종단,mp_obj_t Բովանդակություն_արժեք) {
    mp_buffer_info_t տվյալ; mp_get_buffer_raise(Բովանդակություն_արժեք,&տվյալ,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)տվյալ.buf,տվյալ.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(հոսք_Գրող_առարկա,գրել_հոսք);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Անուն) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)ուղի_արգումենտ(Անուն),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Կերտի_ր_գրացուցակ(mp_obj_t Անուն) {
    결과검사(사용자호출(18,(uintptr_t)ուղի_արգումենտ(Անուն),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,Կերտի_ր_գրացուցակ);
static mp_obj_t հեռացնել_գրացուցակ(mp_obj_t Անուն) {
    결과검사(사용자호출(18,(uintptr_t)ուղի_արգումենտ(Անուն),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,հեռացնել_գրացուցակ);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&հոսք_Կապակցիչ_առարկա) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&հոսք_Ընթերցիչ_առարկա) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&հոսք_Գրող_առարկա) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&նիշք_Ընթերցիչ_առարկա) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&նիշք_Գրող_առարկա) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Ժամացույց_առարկա) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
