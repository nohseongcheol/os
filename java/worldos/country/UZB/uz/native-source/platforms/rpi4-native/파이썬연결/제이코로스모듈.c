// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t o_lchov) { if (o_lchov < 0) mp_raise_OSError(-o_lchov); return o_lchov; }
static const char *yo_l_dalil(mp_obj_t VALUE) {
    size_t element_COUNT; const char *yo_l = mp_obj_str_get_data(VALUE, &element_COUNT);
    if (!element_COUNT || element_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < element_COUNT; 순번++) if (!yo_l[순번]) mp_raise_OSError(MP_EINVAL);
    return yo_l;
}
static mp_obj_t 파일읽기(mp_obj_t Nomi) {
    intptr_t fayl_deskriptor = 결과검사(사용자호출(3, (uintptr_t)yo_l_dalil(Nomi), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Hajmi = 결과검사(사용자호출(9, fayl_deskriptor, 0, 0, 0, 0, 0));
        vstr_t ma_lumotlar; vstr_init_len(&ma_lumotlar, Hajmi);
        intptr_t o_lchov = 사용자호출(2, fayl_deskriptor, (uintptr_t)ma_lumotlar.buf, Hajmi, 0, 0, 0);
        결과검사(o_lchov); ma_lumotlar.len = o_lchov;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&ma_lumotlar);
        nlr_pop(); 사용자호출(4, fayl_deskriptor, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, fayl_deskriptor, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(fayl_o_quvchi_obyekt, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Hajmi=mp_obj_get_int(한도);
    if(Hajmi<0||Hajmi>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t ma_lumotlar; vstr_init_len(&ma_lumotlar,Hajmi);
    intptr_t element_COUNT=사용자호출(2,0,(uintptr_t)ma_lumotlar.buf,Hajmi,0,0,0);
    if(element_COUNT<0) { vstr_clear(&ma_lumotlar); 결과검사(element_COUNT); }
    ma_lumotlar.len=element_COUNT; return mp_obj_new_bytes_from_vstr(&ma_lumotlar);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t yozmoq_fayl(mp_obj_t Nomi, mp_obj_t tarkib_VALUE) {
    const char *yo_l = yo_l_dalil(Nomi);
    mp_buffer_info_t ma_lumotlar; mp_get_buffer_raise(tarkib_VALUE, &ma_lumotlar, MP_BUFFER_READ);
    if (ma_lumotlar.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t fayl_deskriptor = 결과검사(사용자호출(3, (uintptr_t)yo_l, 577, 0, 0, 0, 0));
    intptr_t kiritish_COUNT = 사용자호출(1, fayl_deskriptor, (uintptr_t)ma_lumotlar.buf, ma_lumotlar.len, 0, 0, 0);
    사용자호출(4, fayl_deskriptor, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(kiritish_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(fayl_Bloglar_tahrirchisi_obyekt, yozmoq_fayl);
static mp_obj_t olib_tashlamoq_fayl(mp_obj_t Nomi) { 결과검사(사용자호출(11, (uintptr_t)yo_l_dalil(Nomi), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, olib_tashlamoq_fayl);
static mp_obj_t 사각형그리기(size_t element_COUNT, const mp_obj_t *dalil_ARRAY) {
    (void)element_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(dalil_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Hajmi[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Hajmi);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Soat_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Soat_obyekt, Soat_VALUE);
static mp_obj_t UDP_ochmoq(mp_obj_t 접속번호) {
    int ma_lumotlar_holat = mp_obj_get_int(접속번호); if (ma_lumotlar_holat < 0 || ma_lumotlar_holat > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t fayl_deskriptor = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ma_lumotlar_holat); 첫째값.sin_addr.s_addr = 0;
    intptr_t o_lchov = 사용자호출(33, fayl_deskriptor, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (o_lchov < 0) { 사용자호출(4, fayl_deskriptor, 0, 0, 0, 0, 0); 결과검사(o_lchov); }
    return mp_obj_new_int(fayl_deskriptor);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_ochmoq_OBJ, UDP_ochmoq);
static mp_obj_t UDP_yuborish(mp_obj_t fayl_deskriptor, mp_obj_t 접속번호, mp_obj_t tarkib_VALUE) {
    int ma_lumotlar_holat = mp_obj_get_int(접속번호); if (ma_lumotlar_holat < 1 || ma_lumotlar_holat > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ma_lumotlar; mp_get_buffer_raise(tarkib_VALUE, &ma_lumotlar, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ma_lumotlar_holat); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(fayl_deskriptor), (uintptr_t)ma_lumotlar.buf, ma_lumotlar.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_yuborish_OBJ, UDP_yuborish);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t uzunlik_VALUE; const char *Matn=mp_obj_str_get_data(VALUE,&uzunlik_VALUE);
    unsigned 현재위치=0; uint32_t manzil=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,raqam_COUNT=0;
        while(현재위치<uzunlik_VALUE&&Matn[현재위치]>='0'&&Matn[현재위치]<='9') {
            VALUE=VALUE*10+Matn[현재위치++]-'0'; if(++raqam_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!raqam_COUNT)mp_raise_OSError(MP_EINVAL);
        manzil=manzil<<8|VALUE;
        if(부분<3&&(현재위치>=uzunlik_VALUE||Matn[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=uzunlik_VALUE)mp_raise_OSError(MP_EINVAL);
    return manzil;
}
static mp_obj_t 전문주소전송(size_t kiritish_COUNT, const mp_obj_t *dalil_ARRAY) {
    (void)kiritish_COUNT; uint32_t manzil=인터넷주소읽기(dalil_ARRAY[1]);
    int 접속번호=mp_obj_get_int(dalil_ARRAY[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ma_lumotlar;mp_get_buffer_raise(dalil_ARRAY[3],&ma_lumotlar,MP_BUFFER_READ);
    struct pk_sockaddr_in nishon={0};nishon.sin_family=AF_INET;nishon.sin_port=pk_htons(접속번호);nishon.sin_addr.s_addr=pk_htonl(manzil);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(dalil_ARRAY[0]),(uintptr_t)ma_lumotlar.buf,ma_lumotlar.len,0,(uintptr_t)&nishon,sizeof(nishon))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t fayl_deskriptor) {
    unsigned char ma_lumotlar[512]; struct pk_sockaddr_in bir_rangli_VALUE; pk_socklen_t uzunlik_ma_lumotlar = sizeof(bir_rangli_VALUE);
    intptr_t Hajmi = 결과검사(사용자호출(35, mp_obj_get_int(fayl_deskriptor), (uintptr_t)ma_lumotlar, 512, 0, (uintptr_t)&bir_rangli_VALUE, (uintptr_t)&uzunlik_ma_lumotlar));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(ma_lumotlar, Hajmi), MP_OBJ_NEW_SMALL_INT(pk_htons(bir_rangli_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_yopmoq(mp_obj_t fayl_deskriptor) { 결과검사(사용자호출(4, mp_obj_get_int(fayl_deskriptor), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_yopmoq_OBJ, UDP_yopmoq);
static mp_obj_t ochmoq_oqim(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,bulut_Oila,oqim_Tarmoq,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,ochmoq_oqim);
static mp_obj_t ulash_oqim(mp_obj_t 종단,mp_obj_t manzil_SMS,mp_obj_t INDEX) {
    int 접속번호=mp_obj_get_int(INDEX); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 manzil={0}; manzil.manzil_Oila=bulut_Oila;
    manzil.접속번호=망차례짧은수(접속번호); manzil.Internetdagi_manzil.manzil_VALUE=Tarmoq_butun_son(인터넷주소읽기(manzil_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&manzil,sizeof(manzil),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(oqim_Ulagich_obyekt,ulash_oqim);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int uzunlik_VALUE=mp_obj_get_int(한도); if(uzunlik_VALUE<1||uzunlik_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char ma_lumotlar[512];
    intptr_t element_COUNT=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)ma_lumotlar,uzunlik_VALUE,0,0,0));
    return mp_obj_new_bytes(ma_lumotlar,element_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(oqim_o_quvchi_obyekt,흐름읽기);
static mp_obj_t yozmoq_oqim(mp_obj_t 종단,mp_obj_t tarkib_VALUE) {
    mp_buffer_info_t ma_lumotlar; mp_get_buffer_raise(tarkib_VALUE,&ma_lumotlar,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)ma_lumotlar.buf,ma_lumotlar.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(oqim_Bloglar_tahrirchisi_obyekt,yozmoq_oqim);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(bir_daqiqa_obyekt,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Nomi) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)yo_l_dalil(Nomi),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Yaratish_katalog(mp_obj_t Nomi) {
    결과검사(사용자호출(18,(uintptr_t)yo_l_dalil(Nomi),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,Yaratish_katalog);
static mp_obj_t olib_tashlamoq_katalog(mp_obj_t Nomi) {
    결과검사(사용자호출(18,(uintptr_t)yo_l_dalil(Nomi),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,olib_tashlamoq_katalog);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&oqim_Ulagich_obyekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&oqim_o_quvchi_obyekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&oqim_Bloglar_tahrirchisi_obyekt) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&bir_daqiqa_obyekt) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&fayl_o_quvchi_obyekt) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&fayl_Bloglar_tahrirchisi_obyekt) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Soat_obyekt) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_ochmoq_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_yuborish_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_yopmoq_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
