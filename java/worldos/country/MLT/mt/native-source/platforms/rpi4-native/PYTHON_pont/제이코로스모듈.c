// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t miżura) { if (miżura < 0) mp_raise_OSError(-miżura); return miżura; }
static const char *mogħdija_argument(mp_obj_t VALUE) {
    size_t element_COUNT; const char *mogħdija = mp_obj_str_get_data(VALUE, &element_COUNT);
    if (!element_COUNT || element_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < element_COUNT; 순번++) if (!mogħdija[순번]) mp_raise_OSError(MP_EINVAL);
    return mogħdija;
}
static mp_obj_t 파일읽기(mp_obj_t isem) {
    intptr_t fajl_handle = 결과검사(사용자호출(3, (uintptr_t)mogħdija_argument(isem), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t daqqas = 결과검사(사용자호출(9, fajl_handle, 0, 0, 0, 0, 0));
        vstr_t data; vstr_init_len(&data, daqqas);
        intptr_t miżura = 사용자호출(2, fajl_handle, (uintptr_t)data.buf, daqqas, 0, 0, 0);
        결과검사(miżura); data.len = miżura;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&data);
        nlr_pop(); 사용자호출(4, fajl_handle, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, fajl_handle, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(fajl_Qarrej_oġġett, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t daqqas=mp_obj_get_int(한도);
    if(daqqas<0||daqqas>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t data; vstr_init_len(&data,daqqas);
    intptr_t element_COUNT=사용자호출(2,0,(uintptr_t)data.buf,daqqas,0,0,0);
    if(element_COUNT<0) { vstr_clear(&data); 결과검사(element_COUNT); }
    data.len=element_COUNT; return mp_obj_new_bytes_from_vstr(&data);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t kiteb_fajl(mp_obj_t isem, mp_obj_t Kontenut_VALUE) {
    const char *mogħdija = mogħdija_argument(isem);
    mp_buffer_info_t data; mp_get_buffer_raise(Kontenut_VALUE, &data, MP_BUFFER_READ);
    if (data.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t fajl_handle = 결과검사(사용자호출(3, (uintptr_t)mogħdija, 577, 0, 0, 0, 0));
    intptr_t entrata_COUNT = 사용자호출(1, fajl_handle, (uintptr_t)data.buf, data.len, 0, 0, 0);
    사용자호출(4, fajl_handle, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(entrata_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(fajl_Writer_oġġett, kiteb_fajl);
static mp_obj_t neħħa_fajl(mp_obj_t isem) { 결과검사(사용자호출(11, (uintptr_t)mogħdija_argument(isem), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, neħħa_fajl);
static mp_obj_t 사각형그리기(size_t element_COUNT, const mp_obj_t *argument_ARRAY) {
    (void)element_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argument_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t daqqas[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, daqqas);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Arloġġ_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Arloġġ_oġġett, Arloġġ_VALUE);
static mp_obj_t UDP_fetaħ(mp_obj_t 접속번호) {
    int data_pożizzjoni = mp_obj_get_int(접속번호); if (data_pożizzjoni < 0 || data_pożizzjoni > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t fajl_handle = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_pożizzjoni); 첫째값.sin_addr.s_addr = 0;
    intptr_t miżura = 사용자호출(33, fajl_handle, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (miżura < 0) { 사용자호출(4, fajl_handle, 0, 0, 0, 0, 0); 결과검사(miżura); }
    return mp_obj_new_int(fajl_handle);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, UDP_fetaħ);
static mp_obj_t UDP_bagħat(mp_obj_t fajl_handle, mp_obj_t 접속번호, mp_obj_t Kontenut_VALUE) {
    int data_pożizzjoni = mp_obj_get_int(접속번호); if (data_pożizzjoni < 1 || data_pożizzjoni > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data; mp_get_buffer_raise(Kontenut_VALUE, &data, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_pożizzjoni); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(fajl_handle), (uintptr_t)data.buf, data.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, UDP_bagħat);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t tul_VALUE; const char *SMS=mp_obj_str_get_data(VALUE,&tul_VALUE);
    unsigned 현재위치=0; uint32_t ADDRESS=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,ċifra_COUNT=0;
        while(현재위치<tul_VALUE&&SMS[현재위치]>='0'&&SMS[현재위치]<='9') {
            VALUE=VALUE*10+SMS[현재위치++]-'0'; if(++ċifra_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!ċifra_COUNT)mp_raise_OSError(MP_EINVAL);
        ADDRESS=ADDRESS<<8|VALUE;
        if(부분<3&&(현재위치>=tul_VALUE||SMS[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=tul_VALUE)mp_raise_OSError(MP_EINVAL);
    return ADDRESS;
}
static mp_obj_t 전문주소전송(size_t entrata_COUNT, const mp_obj_t *argument_ARRAY) {
    (void)entrata_COUNT; uint32_t ADDRESS=인터넷주소읽기(argument_ARRAY[1]);
    int 접속번호=mp_obj_get_int(argument_ARRAY[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data;mp_get_buffer_raise(argument_ARRAY[3],&data,MP_BUFFER_READ);
    struct pk_sockaddr_in mira={0};mira.sin_family=AF_INET;mira.sin_port=pk_htons(접속번호);mira.sin_addr.s_addr=pk_htonl(ADDRESS);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argument_ARRAY[0]),(uintptr_t)data.buf,data.len,0,(uintptr_t)&mira,sizeof(mira))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t fajl_handle) {
    unsigned char data[512]; struct pk_sockaddr_in peer_VALUE; pk_socklen_t tul_data = sizeof(peer_VALUE);
    intptr_t daqqas = 결과검사(사용자호출(35, mp_obj_get_int(fajl_handle), (uintptr_t)data, 512, 0, (uintptr_t)&peer_VALUE, (uintptr_t)&tul_data));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(data, daqqas), MP_OBJ_NEW_SMALL_INT(pk_htons(peer_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_agħlaq(mp_obj_t fajl_handle) { 결과검사(사용자호출(4, mp_obj_get_int(fajl_handle), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, UDP_agħlaq);
static mp_obj_t fetaħ_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,cloud_Familja,Stream_netwerk,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,fetaħ_Stream);
static mp_obj_t AQBAD_Stream(mp_obj_t 종단,mp_obj_t ADDRESS_SMS,mp_obj_t INDEX) {
    int 접속번호=mp_obj_get_int(INDEX); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ADDRESS={0}; ADDRESS.ADDRESS_Familja=cloud_Familja;
    ADDRESS.접속번호=망차례짧은수(접속번호); ADDRESS.indirizz_tal_Internet.ADDRESS_VALUE=netwerk_numru_sħiħ(인터넷주소읽기(ADDRESS_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ADDRESS,sizeof(ADDRESS),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_konnettur_oġġett,AQBAD_Stream);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int tul_VALUE=mp_obj_get_int(한도); if(tul_VALUE<1||tul_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char data[512];
    intptr_t element_COUNT=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)data,tul_VALUE,0,0,0));
    return mp_obj_new_bytes(data,element_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Qarrej_oġġett,흐름읽기);
static mp_obj_t kiteb_Stream(mp_obj_t 종단,mp_obj_t Kontenut_VALUE) {
    mp_buffer_info_t data; mp_get_buffer_raise(Kontenut_VALUE,&data,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)data.buf,data.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Writer_oġġett,kiteb_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t isem) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)mogħdija_argument(isem),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t ħalaq_direttorju(mp_obj_t isem) {
    결과검사(사용자호출(18,(uintptr_t)mogħdija_argument(isem),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,ħalaq_direttorju);
static mp_obj_t neħħa_direttorju(mp_obj_t isem) {
    결과검사(사용자호출(18,(uintptr_t)mogħdija_argument(isem),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,neħħa_direttorju);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_konnettur_oġġett) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_Qarrej_oġġett) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Writer_oġġett) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&fajl_Qarrej_oġġett) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&fajl_Writer_oġġett) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Arloġġ_oġġett) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
