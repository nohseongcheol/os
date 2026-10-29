// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *njia_hoja(mp_obj_t thamani) {
    size_t 개수; const char *njia = mp_obj_str_get_data(thamani, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!njia[순번]) mp_raise_OSError(MP_EINVAL);
    return njia;
}
static mp_obj_t 파일읽기(mp_obj_t Jina) {
    intptr_t faili_kishiko = 결과검사(사용자호출(3, (uintptr_t)njia_hoja(Jina), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t panga_ukubwa = 결과검사(사용자호출(9, faili_kishiko, 0, 0, 0, 0, 0));
        vstr_t data; vstr_init_len(&data, panga_ukubwa);
        intptr_t 결과 = 사용자호출(2, faili_kishiko, (uintptr_t)data.buf, panga_ukubwa, 0, 0, 0);
        결과검사(결과); data.len = 결과;
        mp_obj_t thamani = mp_obj_new_bytes_from_vstr(&data);
        nlr_pop(); 사용자호출(4, faili_kishiko, 0, 0, 0, 0, 0); return thamani;
    }
    사용자호출(4, faili_kishiko, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(faili_msomaji_kipengee, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t panga_ukubwa=mp_obj_get_int(한도);
    if(panga_ukubwa<0||panga_ukubwa>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t data; vstr_init_len(&data,panga_ukubwa);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)data.buf,panga_ukubwa,0,0,0);
    if(개수<0) { vstr_clear(&data); 결과검사(개수); }
    data.len=개수; return mp_obj_new_bytes_from_vstr(&data);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t andika_faili(mp_obj_t Jina, mp_obj_t maudhui_thamani) {
    const char *njia = njia_hoja(Jina);
    mp_buffer_info_t data; mp_get_buffer_raise(maudhui_thamani, &data, MP_BUFFER_READ);
    if (data.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t faili_kishiko = 결과검사(사용자호출(3, (uintptr_t)njia, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, faili_kishiko, (uintptr_t)data.buf, data.len, 0, 0, 0);
    사용자호출(4, faili_kishiko, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(faili_Writer_kipengee, andika_faili);
static mp_obj_t ondoa_faili(mp_obj_t Jina) { 결과검사(사용자호출(11, (uintptr_t)njia_hoja(Jina), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, ondoa_faili);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *hoja_ARRAY) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(hoja_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t panga_ukubwa[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, panga_ukubwa);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t saa_thamani(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(saa_kipengee, saa_thamani);
static mp_obj_t 전문열기(mp_obj_t namba_ya_kituo) {
    int 자료위치 = mp_obj_get_int(namba_ya_kituo); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t faili_kishiko = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, faili_kishiko, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, faili_kishiko, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(faili_kishiko);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t faili_kishiko, mp_obj_t namba_ya_kituo, mp_obj_t maudhui_thamani) {
    int 자료위치 = mp_obj_get_int(namba_ya_kituo); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data; mp_get_buffer_raise(maudhui_thamani, &data, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(faili_kishiko), (uintptr_t)data.buf, data.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t thamani) {
    size_t urefu_thamani; const char *SMS=mp_obj_str_get_data(thamani,&urefu_thamani);
    unsigned 현재위치=0; uint32_t anwani=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned thamani=0,숫자수=0;
        while(현재위치<urefu_thamani&&SMS[현재위치]>='0'&&SMS[현재위치]<='9') {
            thamani=thamani*10+SMS[현재위치++]-'0'; if(++숫자수>3||thamani>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        anwani=anwani<<8|thamani;
        if(부분<3&&(현재위치>=urefu_thamani||SMS[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=urefu_thamani)mp_raise_OSError(MP_EINVAL);
    return anwani;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *hoja_ARRAY) {
    (void)항목수; uint32_t anwani=인터넷주소읽기(hoja_ARRAY[1]);
    int namba_ya_kituo=mp_obj_get_int(hoja_ARRAY[2]);if(namba_ya_kituo<1||namba_ya_kituo>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data;mp_get_buffer_raise(hoja_ARRAY[3],&data,MP_BUFFER_READ);
    struct pk_sockaddr_in lengo={0};lengo.sin_family=AF_INET;lengo.sin_port=pk_htons(namba_ya_kituo);lengo.sin_addr.s_addr=pk_htonl(anwani);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(hoja_ARRAY[0]),(uintptr_t)data.buf,data.len,0,(uintptr_t)&lengo,sizeof(lengo))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t faili_kishiko) {
    unsigned char data[512]; struct pk_sockaddr_in kompyuta_rika_thamani; pk_socklen_t urefu_data = sizeof(kompyuta_rika_thamani);
    intptr_t panga_ukubwa = 결과검사(사용자호출(35, mp_obj_get_int(faili_kishiko), (uintptr_t)data, 512, 0, (uintptr_t)&kompyuta_rika_thamani, (uintptr_t)&urefu_data));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(data, panga_ukubwa), MP_OBJ_NEW_SMALL_INT(pk_htons(kompyuta_rika_thamani.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t faili_kishiko) { 결과검사(사용자호출(4, mp_obj_get_int(faili_kishiko), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t unda_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,wingu_Familia,Stream_Mtandao,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,unda_Stream);
static mp_obj_t UNGANISHA_Stream(mp_obj_t 종단,mp_obj_t anwani_SMS,mp_obj_t kielezo) {
    int namba_ya_kituo=mp_obj_get_int(kielezo); if(namba_ya_kituo<1||namba_ya_kituo>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 anwani={0}; anwani.anwani_Familia=wingu_Familia;
    anwani.namba_ya_kituo=망차례짧은수(namba_ya_kituo); anwani.Anwani_tovuti.anwani_thamani=Mtandao_namba_kamili(인터넷주소읽기(anwani_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&anwani,sizeof(anwani),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_kiunganisho_kipengee,UNGANISHA_Stream);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int urefu_thamani=mp_obj_get_int(한도); if(urefu_thamani<1||urefu_thamani>512)mp_raise_OSError(MP_EINVAL);
    unsigned char data[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)data,urefu_thamani,0,0,0));
    return mp_obj_new_bytes(data,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_msomaji_kipengee,흐름읽기);
static mp_obj_t andika_Stream(mp_obj_t 종단,mp_obj_t maudhui_thamani) {
    mp_buffer_info_t data; mp_get_buffer_raise(maudhui_thamani,&data,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)data.buf,data.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Writer_kipengee,andika_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t saa_thamani_4692cef5) {
    결과검사(사용자호출(17,mp_obj_get_int(saa_thamani_4692cef5),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(subiri_kipengee,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Jina) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)njia_hoja(Jina),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t unda_Saraka(mp_obj_t Jina) {
    결과검사(사용자호출(18,(uintptr_t)njia_hoja(Jina),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,unda_Saraka);
static mp_obj_t ondoa_Saraka(mp_obj_t Jina) {
    결과검사(사용자호출(18,(uintptr_t)njia_hoja(Jina),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,ondoa_Saraka);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_kiunganisho_kipengee) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_msomaji_kipengee) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Writer_kipengee) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&subiri_kipengee) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&faili_msomaji_kipengee) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&faili_Writer_kipengee) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&saa_kipengee) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
