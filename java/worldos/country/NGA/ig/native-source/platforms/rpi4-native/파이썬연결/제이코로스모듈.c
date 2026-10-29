// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *ụzọ_ozi_agụment(mp_obj_t valuu) {
    size_t 개수; const char *ụzọ_ozi = mp_obj_str_get_data(valuu, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!ụzọ_ozi[순번]) mp_raise_OSError(MP_EINVAL);
    return ụzọ_ozi;
}
static mp_obj_t 파일읽기(mp_obj_t Aha) {
    intptr_t ọbọakwụkwọ_ebenjìaka = 결과검사(사용자호출(3, (uintptr_t)ụzọ_ozi_agụment(Aha), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Ụhara = 결과검사(사용자호출(9, ọbọakwụkwọ_ebenjìaka, 0, 0, 0, 0, 0));
        vstr_t datà; vstr_init_len(&datà, Ụhara);
        intptr_t 결과 = 사용자호출(2, ọbọakwụkwọ_ebenjìaka, (uintptr_t)datà.buf, Ụhara, 0, 0, 0);
        결과검사(결과); datà.len = 결과;
        mp_obj_t valuu = mp_obj_new_bytes_from_vstr(&datà);
        nlr_pop(); 사용자호출(4, ọbọakwụkwọ_ebenjìaka, 0, 0, 0, 0, 0); return valuu;
    }
    사용자호출(4, ọbọakwụkwọ_ebenjìaka, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ọbọakwụkwọ_Ọgụụ_ihe, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Ụhara=mp_obj_get_int(한도);
    if(Ụhara<0||Ụhara>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t datà; vstr_init_len(&datà,Ụhara);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)datà.buf,Ụhara,0,0,0);
    if(개수<0) { vstr_clear(&datà); 결과검사(개수); }
    datà.len=개수; return mp_obj_new_bytes_from_vstr(&datà);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t dee_ọbọakwụkwọ(mp_obj_t Aha, mp_obj_t ndịnà_valuu) {
    const char *ụzọ_ozi = ụzọ_ozi_agụment(Aha);
    mp_buffer_info_t datà; mp_get_buffer_raise(ndịnà_valuu, &datà, MP_BUFFER_READ);
    if (datà.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ọbọakwụkwọ_ebenjìaka = 결과검사(사용자호출(3, (uintptr_t)ụzọ_ozi, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ọbọakwụkwọ_ebenjìaka, (uintptr_t)datà.buf, datà.len, 0, 0, 0);
    사용자호출(4, ọbọakwụkwọ_ebenjìaka, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ọbọakwụkwọ_Ọdee_ihe, dee_ọbọakwụkwọ);
static mp_obj_t wepụ_ọbọakwụkwọ(mp_obj_t Aha) { 결과검사(사용자호출(11, (uintptr_t)ụzọ_ozi_agụment(Aha), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, wepụ_ọbọakwụkwọ);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *agụment_MKPOKỌTA) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(agụment_MKPOKỌTA[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Ụhara[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Ụhara);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t elekere_valuu(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(elekere_ihe, elekere_valuu);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ọbọakwụkwọ_ebenjìaka = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, ọbọakwụkwọ_ebenjìaka, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, ọbọakwụkwọ_ebenjìaka, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(ọbọakwụkwọ_ebenjìaka);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t ọbọakwụkwọ_ebenjìaka, mp_obj_t 접속번호, mp_obj_t ndịnà_valuu) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t datà; mp_get_buffer_raise(ndịnà_valuu, &datà, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ọbọakwụkwọ_ebenjìaka), (uintptr_t)datà.buf, datà.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t valuu) {
    size_t ogologo_valuu; const char *SMS=mp_obj_str_get_data(valuu,&ogologo_valuu);
    unsigned 현재위치=0; uint32_t àdreèsì=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned valuu=0,숫자수=0;
        while(현재위치<ogologo_valuu&&SMS[현재위치]>='0'&&SMS[현재위치]<='9') {
            valuu=valuu*10+SMS[현재위치++]-'0'; if(++숫자수>3||valuu>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        àdreèsì=àdreèsì<<8|valuu;
        if(부분<3&&(현재위치>=ogologo_valuu||SMS[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=ogologo_valuu)mp_raise_OSError(MP_EINVAL);
    return àdreèsì;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *agụment_MKPOKỌTA) {
    (void)항목수; uint32_t àdreèsì=인터넷주소읽기(agụment_MKPOKỌTA[1]);
    int 접속번호=mp_obj_get_int(agụment_MKPOKỌTA[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t datà;mp_get_buffer_raise(agụment_MKPOKỌTA[3],&datà,MP_BUFFER_READ);
    struct pk_sockaddr_in ebenlereanya={0};ebenlereanya.sin_family=AF_INET;ebenlereanya.sin_port=pk_htons(접속번호);ebenlereanya.sin_addr.s_addr=pk_htonl(àdreèsì);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(agụment_MKPOKỌTA[0]),(uintptr_t)datà.buf,datà.len,0,(uintptr_t)&ebenlereanya,sizeof(ebenlereanya))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ọbọakwụkwọ_ebenjìaka) {
    unsigned char datà[512]; struct pk_sockaddr_in ibè_valuu; pk_socklen_t ogologo_datà = sizeof(ibè_valuu);
    intptr_t Ụhara = 결과검사(사용자호출(35, mp_obj_get_int(ọbọakwụkwọ_ebenjìaka), (uintptr_t)datà, 512, 0, (uintptr_t)&ibè_valuu, (uintptr_t)&ogologo_datà));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(datà, Ụhara), MP_OBJ_NEW_SMALL_INT(pk_htons(ibè_valuu.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t ọbọakwụkwọ_ebenjìaka) { 결과검사(사용자호출(4, mp_obj_get_int(ọbọakwụkwọ_ebenjìaka), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t mepee_agịrị(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,urukpu_Ezinụlọ,agịrị_Netwọọkụ,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,mepee_agịrị);
static mp_obj_t JIKỌ_agịrị(mp_obj_t 종단,mp_obj_t àdreèsì_SMS,mp_obj_t indèks) {
    int 접속번호=mp_obj_get_int(indèks); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 àdreèsì={0}; àdreèsì.àdreèsì_Ezinụlọ=urukpu_Ezinụlọ;
    àdreèsì.접속번호=망차례짧은수(접속번호); àdreèsì.adreesi_ịntaneèt.àdreèsì_valuu=Netwọọkụ_ọnụọgụ_nzùrùòkè(인터넷주소읽기(àdreèsì_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&àdreèsì,sizeof(àdreèsì),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(agịrị_ṅjikọta_ihe,JIKỌ_agịrị);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int ogologo_valuu=mp_obj_get_int(한도); if(ogologo_valuu<1||ogologo_valuu>512)mp_raise_OSError(MP_EINVAL);
    unsigned char datà[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)datà,ogologo_valuu,0,0,0));
    return mp_obj_new_bytes(datà,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(agịrị_Ọgụụ_ihe,흐름읽기);
static mp_obj_t dee_agịrị(mp_obj_t 종단,mp_obj_t ndịnà_valuu) {
    mp_buffer_info_t datà; mp_get_buffer_raise(ndịnà_valuu,&datà,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)datà.buf,datà.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(agịrị_Ọdee_ihe,dee_agịrị);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Aha) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)ụzọ_ozi_agụment(Aha),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t mepụta_dàịrektrị(mp_obj_t Aha) {
    결과검사(사용자호출(18,(uintptr_t)ụzọ_ozi_agụment(Aha),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,mepụta_dàịrektrị);
static mp_obj_t wepụ_dàịrektrị(mp_obj_t Aha) {
    결과검사(사용자호출(18,(uintptr_t)ụzọ_ozi_agụment(Aha),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,wepụ_dàịrektrị);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&agịrị_ṅjikọta_ihe) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&agịrị_Ọgụụ_ihe) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&agịrị_Ọdee_ihe) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ọbọakwụkwọ_Ọgụụ_ihe) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&ọbọakwụkwọ_Ọdee_ihe) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&elekere_ihe) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
