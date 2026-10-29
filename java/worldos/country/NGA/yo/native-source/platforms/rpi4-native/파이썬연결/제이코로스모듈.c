// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *ọ̀nà_ágúmẹ́ntì(mp_obj_t iye) {
    size_t 개수; const char *ọ̀nà = mp_obj_str_get_data(iye, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!ọ̀nà[순번]) mp_raise_OSError(MP_EINVAL);
    return ọ̀nà;
}
static mp_obj_t 파일읽기(mp_obj_t Orúkọ) {
    intptr_t fáìlì_èkù = 결과검사(사용자호출(3, (uintptr_t)ọ̀nà_ágúmẹ́ntì(Orúkọ), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Ìwọ̀n = 결과검사(사용자호출(9, fáìlì_èkù, 0, 0, 0, 0, 0));
        vstr_t détà; vstr_init_len(&détà, Ìwọ̀n);
        intptr_t 결과 = 사용자호출(2, fáìlì_èkù, (uintptr_t)détà.buf, Ìwọ̀n, 0, 0, 0);
        결과검사(결과); détà.len = 결과;
        mp_obj_t iye = mp_obj_new_bytes_from_vstr(&détà);
        nlr_pop(); 사용자호출(4, fáìlì_èkù, 0, 0, 0, 0, 0); return iye;
    }
    사용자호출(4, fáìlì_èkù, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(fáìlì_akàwé_nǹkan, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Ìwọ̀n=mp_obj_get_int(한도);
    if(Ìwọ̀n<0||Ìwọ̀n>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t détà; vstr_init_len(&détà,Ìwọ̀n);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)détà.buf,Ìwọ̀n,0,0,0);
    if(개수<0) { vstr_clear(&détà); 결과검사(개수); }
    détà.len=개수; return mp_obj_new_bytes_from_vstr(&détà);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t kọ_fáìlì(mp_obj_t Orúkọ, mp_obj_t Àkóónú_iye) {
    const char *ọ̀nà = ọ̀nà_ágúmẹ́ntì(Orúkọ);
    mp_buffer_info_t détà; mp_get_buffer_raise(Àkóónú_iye, &détà, MP_BUFFER_READ);
    if (détà.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t fáìlì_èkù = 결과검사(사용자호출(3, (uintptr_t)ọ̀nà, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, fáìlì_èkù, (uintptr_t)détà.buf, détà.len, 0, 0, 0);
    사용자호출(4, fáìlì_èkù, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(fáìlì_Òǹkọ̀wé_nǹkan, kọ_fáìlì);
static mp_obj_t ṣèmúkúro_fáìlì(mp_obj_t Orúkọ) { 결과검사(사용자호출(11, (uintptr_t)ọ̀nà_ágúmẹ́ntì(Orúkọ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, ṣèmúkúro_fáìlì);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *ágúmẹ́ntì_ÀRÉÈ) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(ágúmẹ́ntì_ÀRÉÈ[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Ìwọ̀n[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Ìwọ̀n);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t aago_iye(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(aago_nǹkan, aago_iye);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t fáìlì_èkù = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, fáìlì_èkù, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, fáìlì_èkù, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(fáìlì_èkù);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t fáìlì_èkù, mp_obj_t 접속번호, mp_obj_t Àkóónú_iye) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t détà; mp_get_buffer_raise(Àkóónú_iye, &détà, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(fáìlì_èkù), (uintptr_t)détà.buf, détà.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t iye) {
    size_t gígùn_iye; const char *SMS=mp_obj_str_get_data(iye,&gígùn_iye);
    unsigned 현재위치=0; uint32_t àdírẹ́ẹ̀sì=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned iye=0,숫자수=0;
        while(현재위치<gígùn_iye&&SMS[현재위치]>='0'&&SMS[현재위치]<='9') {
            iye=iye*10+SMS[현재위치++]-'0'; if(++숫자수>3||iye>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        àdírẹ́ẹ̀sì=àdírẹ́ẹ̀sì<<8|iye;
        if(부분<3&&(현재위치>=gígùn_iye||SMS[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=gígùn_iye)mp_raise_OSError(MP_EINVAL);
    return àdírẹ́ẹ̀sì;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *ágúmẹ́ntì_ÀRÉÈ) {
    (void)항목수; uint32_t àdírẹ́ẹ̀sì=인터넷주소읽기(ágúmẹ́ntì_ÀRÉÈ[1]);
    int 접속번호=mp_obj_get_int(ágúmẹ́ntì_ÀRÉÈ[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t détà;mp_get_buffer_raise(ágúmẹ́ntì_ÀRÉÈ[3],&détà,MP_BUFFER_READ);
    struct pk_sockaddr_in àfojúsùn={0};àfojúsùn.sin_family=AF_INET;àfojúsùn.sin_port=pk_htons(접속번호);àfojúsùn.sin_addr.s_addr=pk_htonl(àdírẹ́ẹ̀sì);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(ágúmẹ́ntì_ÀRÉÈ[0]),(uintptr_t)détà.buf,détà.len,0,(uintptr_t)&àfojúsùn,sizeof(àfojúsùn))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t fáìlì_èkù) {
    unsigned char détà[512]; struct pk_sockaddr_in ọ̀gbà_iye; pk_socklen_t gígùn_détà = sizeof(ọ̀gbà_iye);
    intptr_t Ìwọ̀n = 결과검사(사용자호출(35, mp_obj_get_int(fáìlì_èkù), (uintptr_t)détà, 512, 0, (uintptr_t)&ọ̀gbà_iye, (uintptr_t)&gígùn_détà));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(détà, Ìwọ̀n), MP_OBJ_NEW_SMALL_INT(pk_htons(ọ̀gbà_iye.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t fáìlì_èkù) { 결과검사(사용자호출(4, mp_obj_get_int(fáìlì_èkù), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t ṣí_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,Íntánẹ́ẹ̀tì_Ẹbí,Stream_Alásopọ̀,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,ṣí_Stream);
static mp_obj_t SOMỌ́_Stream(mp_obj_t 종단,mp_obj_t àdírẹ́ẹ̀sì_SMS,mp_obj_t wá_atọ̀ka_àkóónú) {
    int 접속번호=mp_obj_get_int(wá_atọ̀ka_àkóónú); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 àdírẹ́ẹ̀sì={0}; àdírẹ́ẹ̀sì.àdírẹ́ẹ̀sì_Ẹbí=Íntánẹ́ẹ̀tì_Ẹbí;
    àdírẹ́ẹ̀sì.접속번호=망차례짧은수(접속번호); àdírẹ́ẹ̀sì.àdíréẹ̀sì_íntánẹ́ẹ̀tì.àdírẹ́ẹ̀sì_iye=Alásopọ̀_nọ́ńbà_odindi(인터넷주소읽기(àdírẹ́ẹ̀sì_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&àdírẹ́ẹ̀sì,sizeof(àdírẹ́ẹ̀sì),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_olùsopọ̀_nǹkan,SOMỌ́_Stream);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int gígùn_iye=mp_obj_get_int(한도); if(gígùn_iye<1||gígùn_iye>512)mp_raise_OSError(MP_EINVAL);
    unsigned char détà[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)détà,gígùn_iye,0,0,0));
    return mp_obj_new_bytes(détà,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_akàwé_nǹkan,흐름읽기);
static mp_obj_t kọ_Stream(mp_obj_t 종단,mp_obj_t Àkóónú_iye) {
    mp_buffer_info_t détà; mp_get_buffer_raise(Àkóónú_iye,&détà,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)détà.buf,détà.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Òǹkọ̀wé_nǹkan,kọ_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Orúkọ) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)ọ̀nà_ágúmẹ́ntì(Orúkọ),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Ṣẹ̀dá_àkójọpọ̀_fáìlì(mp_obj_t Orúkọ) {
    결과검사(사용자호출(18,(uintptr_t)ọ̀nà_ágúmẹ́ntì(Orúkọ),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,Ṣẹ̀dá_àkójọpọ̀_fáìlì);
static mp_obj_t ṣèmúkúro_àkójọpọ̀_fáìlì(mp_obj_t Orúkọ) {
    결과검사(사용자호출(18,(uintptr_t)ọ̀nà_ágúmẹ́ntì(Orúkọ),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,ṣèmúkúro_àkójọpọ̀_fáìlì);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_olùsopọ̀_nǹkan) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_akàwé_nǹkan) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Òǹkọ̀wé_nǹkan) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&fáìlì_akàwé_nǹkan) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&fáìlì_Òǹkọ̀wé_nǹkan) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&aago_nǹkan) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
