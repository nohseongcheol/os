// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t tomhas) { if (tomhas < 0) mp_raise_OSError(-tomhas); return tomhas; }
static const char *slighe_argamaid(mp_obj_t VALUE) {
    size_t nì_COUNT; const char *Slighe = mp_obj_str_get_data(VALUE, &nì_COUNT);
    if (!nì_COUNT || nì_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < nì_COUNT; 순번++) if (!Slighe[순번]) mp_raise_OSError(MP_EINVAL);
    return Slighe;
}
static mp_obj_t 파일읽기(mp_obj_t Ainm) {
    intptr_t faidhle_làmhrachan = 결과검사(사용자호출(3, (uintptr_t)slighe_argamaid(Ainm), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t atharraich_am_meud = 결과검사(사용자호출(9, faidhle_làmhrachan, 0, 0, 0, 0, 0));
        vstr_t dàta; vstr_init_len(&dàta, atharraich_am_meud);
        intptr_t tomhas = 사용자호출(2, faidhle_làmhrachan, (uintptr_t)dàta.buf, atharraich_am_meud, 0, 0, 0);
        결과검사(tomhas); dàta.len = tomhas;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&dàta);
        nlr_pop(); 사용자호출(4, faidhle_làmhrachan, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, faidhle_làmhrachan, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(faidhle_Leughadair_nì, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t atharraich_am_meud=mp_obj_get_int(한도);
    if(atharraich_am_meud<0||atharraich_am_meud>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t dàta; vstr_init_len(&dàta,atharraich_am_meud);
    intptr_t nì_COUNT=사용자호출(2,0,(uintptr_t)dàta.buf,atharraich_am_meud,0,0,0);
    if(nì_COUNT<0) { vstr_clear(&dàta); 결과검사(nì_COUNT); }
    dàta.len=nì_COUNT; return mp_obj_new_bytes_from_vstr(&dàta);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t sgrìobh_faidhle(mp_obj_t Ainm, mp_obj_t susbaint_VALUE) {
    const char *Slighe = slighe_argamaid(Ainm);
    mp_buffer_info_t dàta; mp_get_buffer_raise(susbaint_VALUE, &dàta, MP_BUFFER_READ);
    if (dàta.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t faidhle_làmhrachan = 결과검사(사용자호출(3, (uintptr_t)Slighe, 577, 0, 0, 0, 0));
    intptr_t cur_a_steach_COUNT = 사용자호출(1, faidhle_làmhrachan, (uintptr_t)dàta.buf, dàta.len, 0, 0, 0);
    사용자호출(4, faidhle_làmhrachan, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(cur_a_steach_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(faidhle_Sgrìobhadair_nì, sgrìobh_faidhle);
static mp_obj_t thoir_air_falbh_faidhle(mp_obj_t Ainm) { 결과검사(사용자호출(11, (uintptr_t)slighe_argamaid(Ainm), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, thoir_air_falbh_faidhle);
static mp_obj_t 사각형그리기(size_t nì_COUNT, const mp_obj_t *argamaid_ARRAY) {
    (void)nì_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argamaid_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t atharraich_am_meud[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, atharraich_am_meud);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t cleoc_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(cleoc_nì, cleoc_VALUE);
static mp_obj_t UDP_fosgail(mp_obj_t 접속번호) {
    int dàta_suidhich = mp_obj_get_int(접속번호); if (dàta_suidhich < 0 || dàta_suidhich > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t faidhle_làmhrachan = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(dàta_suidhich); 첫째값.sin_addr.s_addr = 0;
    intptr_t tomhas = 사용자호출(33, faidhle_làmhrachan, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (tomhas < 0) { 사용자호출(4, faidhle_làmhrachan, 0, 0, 0, 0, 0); 결과검사(tomhas); }
    return mp_obj_new_int(faidhle_làmhrachan);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, UDP_fosgail);
static mp_obj_t UDP_cuir(mp_obj_t faidhle_làmhrachan, mp_obj_t 접속번호, mp_obj_t susbaint_VALUE) {
    int dàta_suidhich = mp_obj_get_int(접속번호); if (dàta_suidhich < 1 || dàta_suidhich > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t dàta; mp_get_buffer_raise(susbaint_VALUE, &dàta, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(dàta_suidhich); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(faidhle_làmhrachan), (uintptr_t)dàta.buf, dàta.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, UDP_cuir);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t faid_VALUE; const char *SMS=mp_obj_str_get_data(VALUE,&faid_VALUE);
    unsigned 현재위치=0; uint32_t ADDRESS=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,figear_COUNT=0;
        while(현재위치<faid_VALUE&&SMS[현재위치]>='0'&&SMS[현재위치]<='9') {
            VALUE=VALUE*10+SMS[현재위치++]-'0'; if(++figear_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!figear_COUNT)mp_raise_OSError(MP_EINVAL);
        ADDRESS=ADDRESS<<8|VALUE;
        if(부분<3&&(현재위치>=faid_VALUE||SMS[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=faid_VALUE)mp_raise_OSError(MP_EINVAL);
    return ADDRESS;
}
static mp_obj_t 전문주소전송(size_t cur_a_steach_COUNT, const mp_obj_t *argamaid_ARRAY) {
    (void)cur_a_steach_COUNT; uint32_t ADDRESS=인터넷주소읽기(argamaid_ARRAY[1]);
    int 접속번호=mp_obj_get_int(argamaid_ARRAY[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t dàta;mp_get_buffer_raise(argamaid_ARRAY[3],&dàta,MP_BUFFER_READ);
    struct pk_sockaddr_in targaid={0};targaid.sin_family=AF_INET;targaid.sin_port=pk_htons(접속번호);targaid.sin_addr.s_addr=pk_htonl(ADDRESS);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argamaid_ARRAY[0]),(uintptr_t)dàta.buf,dàta.len,0,(uintptr_t)&targaid,sizeof(targaid))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t faidhle_làmhrachan) {
    unsigned char dàta[512]; struct pk_sockaddr_in seise_VALUE; pk_socklen_t faid_dàta = sizeof(seise_VALUE);
    intptr_t atharraich_am_meud = 결과검사(사용자호출(35, mp_obj_get_int(faidhle_làmhrachan), (uintptr_t)dàta, 512, 0, (uintptr_t)&seise_VALUE, (uintptr_t)&faid_dàta));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(dàta, atharraich_am_meud), MP_OBJ_NEW_SMALL_INT(pk_htons(seise_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_dùin(mp_obj_t faidhle_làmhrachan) { 결과검사(사용자호출(4, mp_obj_get_int(faidhle_làmhrachan), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, UDP_dùin);
static mp_obj_t fosgail_sruth(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,neul_teaghlach,sruth_lìonra,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,fosgail_sruth);
static mp_obj_t CONNECT_sruth(mp_obj_t 종단,mp_obj_t ADDRESS_SMS,mp_obj_t INDEX) {
    int 접속번호=mp_obj_get_int(INDEX); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ADDRESS={0}; ADDRESS.ADDRESS_teaghlach=neul_teaghlach;
    ADDRESS.접속번호=망차례짧은수(접속번호); ADDRESS.Seòladh_eadar_lìn.ADDRESS_VALUE=lìonra_àireamh_shlàn(인터넷주소읽기(ADDRESS_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ADDRESS,sizeof(ADDRESS),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(sruth_ceanglaiche_nì,CONNECT_sruth);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int faid_VALUE=mp_obj_get_int(한도); if(faid_VALUE<1||faid_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char dàta[512];
    intptr_t nì_COUNT=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)dàta,faid_VALUE,0,0,0));
    return mp_obj_new_bytes(dàta,nì_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(sruth_Leughadair_nì,흐름읽기);
static mp_obj_t sgrìobh_sruth(mp_obj_t 종단,mp_obj_t susbaint_VALUE) {
    mp_buffer_info_t dàta; mp_get_buffer_raise(susbaint_VALUE,&dàta,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)dàta.buf,dàta.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(sruth_Sgrìobhadair_nì,sgrìobh_sruth);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(fuirich_nì,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Ainm) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)slighe_argamaid(Ainm),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Create_eòlaire(mp_obj_t Ainm) {
    결과검사(사용자호출(18,(uintptr_t)slighe_argamaid(Ainm),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(eòlaire_cruthadair_nì,Create_eòlaire);
static mp_obj_t thoir_air_falbh_eòlaire(mp_obj_t Ainm) {
    결과검사(사용자호출(18,(uintptr_t)slighe_argamaid(Ainm),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,thoir_air_falbh_eòlaire);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&sruth_ceanglaiche_nì) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&sruth_Leughadair_nì) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&sruth_Sgrìobhadair_nì) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&fuirich_nì) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&eòlaire_cruthadair_nì) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&faidhle_Leughadair_nì) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&faidhle_Sgrìobhadair_nì) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&cleoc_nì) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
