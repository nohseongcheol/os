// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t mēhua) { if (mēhua < 0) mp_raise_OSError(-mēhua); return mēhua; }
static const char *ara_tohenga(mp_obj_t uara) {
    size_t tuemi_COUNT; const char *ara = mp_obj_str_get_data(uara, &tuemi_COUNT);
    if (!tuemi_COUNT || tuemi_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < tuemi_COUNT; 순번++) if (!ara[순번]) mp_raise_OSError(MP_EINVAL);
    return ara;
}
static mp_obj_t 파일읽기(mp_obj_t Ingoa) {
    intptr_t kōnae_raweke = 결과검사(사용자호출(3, (uintptr_t)ara_tohenga(Ingoa), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t rahi = 결과검사(사용자호출(9, kōnae_raweke, 0, 0, 0, 0, 0));
        vstr_t raraunga; vstr_init_len(&raraunga, rahi);
        intptr_t mēhua = 사용자호출(2, kōnae_raweke, (uintptr_t)raraunga.buf, rahi, 0, 0, 0);
        결과검사(mēhua); raraunga.len = mēhua;
        mp_obj_t uara = mp_obj_new_bytes_from_vstr(&raraunga);
        nlr_pop(); 사용자호출(4, kōnae_raweke, 0, 0, 0, 0, 0); return uara;
    }
    사용자호출(4, kōnae_raweke, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(kōnae_Pūpānui_ahanoa, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t rahi=mp_obj_get_int(한도);
    if(rahi<0||rahi>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t raraunga; vstr_init_len(&raraunga,rahi);
    intptr_t tuemi_COUNT=사용자호출(2,0,(uintptr_t)raraunga.buf,rahi,0,0,0);
    if(tuemi_COUNT<0) { vstr_clear(&raraunga); 결과검사(tuemi_COUNT); }
    raraunga.len=tuemi_COUNT; return mp_obj_new_bytes_from_vstr(&raraunga);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t tuhi_kōnae(mp_obj_t Ingoa, mp_obj_t Ihirangi_uara) {
    const char *ara = ara_tohenga(Ingoa);
    mp_buffer_info_t raraunga; mp_get_buffer_raise(Ihirangi_uara, &raraunga, MP_BUFFER_READ);
    if (raraunga.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t kōnae_raweke = 결과검사(사용자호출(3, (uintptr_t)ara, 577, 0, 0, 0, 0));
    intptr_t tāurunga_COUNT = 사용자호출(1, kōnae_raweke, (uintptr_t)raraunga.buf, raraunga.len, 0, 0, 0);
    사용자호출(4, kōnae_raweke, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(tāurunga_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(kōnae_Kaituhi_ahanoa, tuhi_kōnae);
static mp_obj_t tango_kōnae(mp_obj_t Ingoa) { 결과검사(사용자호출(11, (uintptr_t)ara_tohenga(Ingoa), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, tango_kōnae);
static mp_obj_t 사각형그리기(size_t tuemi_COUNT, const mp_obj_t *tohenga_HUĀNGA) {
    (void)tuemi_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(tohenga_HUĀNGA[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t rahi[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, rahi);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Karaka_uara(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Karaka_ahanoa, Karaka_uara);
static mp_obj_t UDP_tiwhikete(mp_obj_t 접속번호) {
    int raraunga_tūranga = mp_obj_get_int(접속번호); if (raraunga_tūranga < 0 || raraunga_tūranga > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t kōnae_raweke = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(raraunga_tūranga); 첫째값.sin_addr.s_addr = 0;
    intptr_t mēhua = 사용자호출(33, kōnae_raweke, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (mēhua < 0) { 사용자호출(4, kōnae_raweke, 0, 0, 0, 0, 0); 결과검사(mēhua); }
    return mp_obj_new_int(kōnae_raweke);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, UDP_tiwhikete);
static mp_obj_t UDP_tuku(mp_obj_t kōnae_raweke, mp_obj_t 접속번호, mp_obj_t Ihirangi_uara) {
    int raraunga_tūranga = mp_obj_get_int(접속번호); if (raraunga_tūranga < 1 || raraunga_tūranga > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t raraunga; mp_get_buffer_raise(Ihirangi_uara, &raraunga, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(raraunga_tūranga); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(kōnae_raweke), (uintptr_t)raraunga.buf, raraunga.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, UDP_tuku);
static uint32_t 인터넷주소읽기(mp_obj_t uara) {
    size_t roa_uara; const char *Ngā_kupu=mp_obj_str_get_data(uara,&roa_uara);
    unsigned 현재위치=0; uint32_t ADDRESS=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned uara=0,mati_COUNT=0;
        while(현재위치<roa_uara&&Ngā_kupu[현재위치]>='0'&&Ngā_kupu[현재위치]<='9') {
            uara=uara*10+Ngā_kupu[현재위치++]-'0'; if(++mati_COUNT>3||uara>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!mati_COUNT)mp_raise_OSError(MP_EINVAL);
        ADDRESS=ADDRESS<<8|uara;
        if(부분<3&&(현재위치>=roa_uara||Ngā_kupu[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=roa_uara)mp_raise_OSError(MP_EINVAL);
    return ADDRESS;
}
static mp_obj_t 전문주소전송(size_t tāurunga_COUNT, const mp_obj_t *tohenga_HUĀNGA) {
    (void)tāurunga_COUNT; uint32_t ADDRESS=인터넷주소읽기(tohenga_HUĀNGA[1]);
    int 접속번호=mp_obj_get_int(tohenga_HUĀNGA[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t raraunga;mp_get_buffer_raise(tohenga_HUĀNGA[3],&raraunga,MP_BUFFER_READ);
    struct pk_sockaddr_in ūnga={0};ūnga.sin_family=AF_INET;ūnga.sin_port=pk_htons(접속번호);ūnga.sin_addr.s_addr=pk_htonl(ADDRESS);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(tohenga_HUĀNGA[0]),(uintptr_t)raraunga.buf,raraunga.len,0,(uintptr_t)&ūnga,sizeof(ūnga))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t kōnae_raweke) {
    unsigned char raraunga[512]; struct pk_sockaddr_in hoa_uara; pk_socklen_t roa_raraunga = sizeof(hoa_uara);
    intptr_t rahi = 결과검사(사용자호출(35, mp_obj_get_int(kōnae_raweke), (uintptr_t)raraunga, 512, 0, (uintptr_t)&hoa_uara, (uintptr_t)&roa_raraunga));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(raraunga, rahi), MP_OBJ_NEW_SMALL_INT(pk_htons(hoa_uara.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_kati(mp_obj_t kōnae_raweke) { 결과검사(사용자호출(4, mp_obj_get_int(kōnae_raweke), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, UDP_kati);
static mp_obj_t tiwhikete_roma(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,kapua_Whānau,roma_whatunga,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,tiwhikete_roma);
static mp_obj_t TŪHONO_roma(mp_obj_t 종단,mp_obj_t ADDRESS_TEXT,mp_obj_t INDEX) {
    int 접속번호=mp_obj_get_int(INDEX); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ADDRESS={0}; ADDRESS.ADDRESS_Whānau=kapua_Whānau;
    ADDRESS.접속번호=망차례짧은수(접속번호); ADDRESS.Wāhitau_ipurangi.ADDRESS_uara=whatunga_tau_tōpū(인터넷주소읽기(ADDRESS_TEXT));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ADDRESS,sizeof(ADDRESS),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(roma_pūtūhono_ahanoa,TŪHONO_roma);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int roa_uara=mp_obj_get_int(한도); if(roa_uara<1||roa_uara>512)mp_raise_OSError(MP_EINVAL);
    unsigned char raraunga[512];
    intptr_t tuemi_COUNT=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)raraunga,roa_uara,0,0,0));
    return mp_obj_new_bytes(raraunga,tuemi_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(roma_Pūpānui_ahanoa,흐름읽기);
static mp_obj_t tuhi_roma(mp_obj_t 종단,mp_obj_t Ihirangi_uara) {
    mp_buffer_info_t raraunga; mp_get_buffer_raise(Ihirangi_uara,&raraunga,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)raraunga.buf,raraunga.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(roma_Kaituhi_ahanoa,tuhi_roma);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_uara) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_uara),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Ingoa) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)ara_tohenga(Ingoa),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Waihanga_whaiaronga(mp_obj_t Ingoa) {
    결과검사(사용자호출(18,(uintptr_t)ara_tohenga(Ingoa),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,Waihanga_whaiaronga);
static mp_obj_t tango_whaiaronga(mp_obj_t Ingoa) {
    결과검사(사용자호출(18,(uintptr_t)ara_tohenga(Ingoa),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,tango_whaiaronga);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&roma_pūtūhono_ahanoa) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&roma_Pūpānui_ahanoa) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&roma_Kaituhi_ahanoa) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&kōnae_Pūpānui_ahanoa) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&kōnae_Kaituhi_ahanoa) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Karaka_ahanoa) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
