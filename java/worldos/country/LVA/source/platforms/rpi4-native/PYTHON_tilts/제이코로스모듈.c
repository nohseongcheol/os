// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t mērs) { if (mērs < 0) mp_raise_OSError(-mērs); return mērs; }
static const char *ceļš_arg(mp_obj_t VALUE) {
    size_t krājums_COUNT; const char *CEĻŠ = mp_obj_str_get_data(VALUE, &krājums_COUNT);
    if (!krājums_COUNT || krājums_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < krājums_COUNT; 순번++) if (!CEĻŠ[순번]) mp_raise_OSError(MP_EINVAL);
    return CEĻŠ;
}
static mp_obj_t 파일읽기(mp_obj_t Nosaukums) {
    intptr_t Fails_turis = 결과검사(사용자호출(3, (uintptr_t)ceļš_arg(Nosaukums), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Izmērs = 결과검사(사용자호출(9, Fails_turis, 0, 0, 0, 0, 0));
        vstr_t dati; vstr_init_len(&dati, Izmērs);
        intptr_t mērs = 사용자호출(2, Fails_turis, (uintptr_t)dati.buf, Izmērs, 0, 0, 0);
        결과검사(mērs); dati.len = mērs;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&dati);
        nlr_pop(); 사용자호출(4, Fails_turis, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, Fails_turis, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Fails_Lasītājs_objekts, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Izmērs=mp_obj_get_int(한도);
    if(Izmērs<0||Izmērs>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t dati; vstr_init_len(&dati,Izmērs);
    intptr_t krājums_COUNT=사용자호출(2,0,(uintptr_t)dati.buf,Izmērs,0,0,0);
    if(krājums_COUNT<0) { vstr_clear(&dati); 결과검사(krājums_COUNT); }
    dati.len=krājums_COUNT; return mp_obj_new_bytes_from_vstr(&dati);
}
static MP_DEFINE_CONST_FUN_OBJ_1(STDIN_Lasītājs_objekts, 표준입력읽기);
static mp_obj_t rakstīšana_Fails(mp_obj_t Nosaukums, mp_obj_t Saturs_VALUE) {
    const char *CEĻŠ = ceļš_arg(Nosaukums);
    mp_buffer_info_t dati; mp_get_buffer_raise(Saturs_VALUE, &dati, MP_BUFFER_READ);
    if (dati.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t Fails_turis = 결과검사(사용자호출(3, (uintptr_t)CEĻŠ, 577, 0, 0, 0, 0));
    intptr_t ievade_COUNT = 사용자호출(1, Fails_turis, (uintptr_t)dati.buf, dati.len, 0, 0, 0);
    사용자호출(4, Fails_turis, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(ievade_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Fails_Rakstītājs_objekts, rakstīšana_Fails);
static mp_obj_t noņemt_Fails(mp_obj_t Nosaukums) { 결과검사(사용자호출(11, (uintptr_t)ceļš_arg(Nosaukums), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, noņemt_Fails);
static mp_obj_t Molberts_taisnstūris(size_t krājums_COUNT, const mp_obj_t *arg_ARRAY) {
    (void)krājums_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(arg_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(taisnstūris_objekts, 5, 5, Molberts_taisnstūris);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Izmērs[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Izmērs);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Pulkstenis_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Pulkstenis_objekts, Pulkstenis_VALUE);
static mp_obj_t UDP_atvērt(mp_obj_t porta_numurs) {
    int dati_amats = mp_obj_get_int(porta_numurs); if (dati_amats < 0 || dati_amats > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t Fails_turis = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(dati_amats); 첫째값.sin_addr.s_addr = 0;
    intptr_t mērs = 사용자호출(33, Fails_turis, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (mērs < 0) { 사용자호출(4, Fails_turis, 0, 0, 0, 0, 0); 결과검사(mērs); }
    return mp_obj_new_int(Fails_turis);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_atvērt_OBJ, UDP_atvērt);
static mp_obj_t UDP_sūtīt(mp_obj_t Fails_turis, mp_obj_t porta_numurs, mp_obj_t Saturs_VALUE) {
    int dati_amats = mp_obj_get_int(porta_numurs); if (dati_amats < 1 || dati_amats > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t dati; mp_get_buffer_raise(Saturs_VALUE, &dati, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(dati_amats); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(Fails_turis), (uintptr_t)dati.buf, dati.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_sūtīt_OBJ, UDP_sūtīt);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t 길이; const char *Teksts=mp_obj_str_get_data(VALUE,&길이);
    unsigned pašreizējais_amats=0; uint32_t adrese=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,cipars_COUNT=0;
        while(pašreizējais_amats<길이&&Teksts[pašreizējais_amats]>='0'&&Teksts[pašreizējais_amats]<='9') {
            VALUE=VALUE*10+Teksts[pašreizējais_amats++]-'0'; if(++cipars_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!cipars_COUNT)mp_raise_OSError(MP_EINVAL);
        adrese=adrese<<8|VALUE;
        if(부분<3&&(pašreizējais_amats>=길이||Teksts[pašreizējais_amats++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(pašreizējais_amats!=길이)mp_raise_OSError(MP_EINVAL);
    return adrese;
}
static mp_obj_t 전문주소전송(size_t ievade_COUNT, const mp_obj_t *arg_ARRAY) {
    (void)ievade_COUNT; uint32_t adrese=인터넷주소읽기(arg_ARRAY[1]);
    int porta_numurs=mp_obj_get_int(arg_ARRAY[2]);if(porta_numurs<1||porta_numurs>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t dati;mp_get_buffer_raise(arg_ARRAY[3],&dati,MP_BUFFER_READ);
    struct pk_sockaddr_in mērķis={0};mērķis.sin_family=AF_INET;mērķis.sin_port=pk_htons(porta_numurs);mērķis.sin_addr.s_addr=pk_htonl(adrese);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(arg_ARRAY[0]),(uintptr_t)dati.buf,dati.len,0,(uintptr_t)&mērķis,sizeof(mērķis))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t Fails_turis) {
    unsigned char dati[512]; struct pk_sockaddr_in vienranga_VALUE; pk_socklen_t 길이값 = sizeof(vienranga_VALUE);
    intptr_t Izmērs = 결과검사(사용자호출(35, mp_obj_get_int(Fails_turis), (uintptr_t)dati, 512, 0, (uintptr_t)&vienranga_VALUE, (uintptr_t)&길이값));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(dati, Izmērs), MP_OBJ_NEW_SMALL_INT(pk_htons(vienranga_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Aizvērt(mp_obj_t Fails_turis) { 결과검사(사용자호출(4, mp_obj_get_int(Fails_turis), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Aizvērt_OBJ, UDP_Aizvērt);
static mp_obj_t atvērt_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,mākonis_saime,Stream_tīkls,Stream_transporta_protokols,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,atvērt_Stream);
static mp_obj_t saziņa_Stream(mp_obj_t dalībnieks,mp_obj_t adrese_SMS,mp_obj_t INDEX) {
    int porta_numurs=mp_obj_get_int(INDEX); if(porta_numurs<1||porta_numurs>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 adrese={0}; adrese.adrese_saime=mākonis_saime;
    adrese.porta_numurs=망차례짧은수(porta_numurs); adrese.interneta_adrese.adrese_VALUE=tīkls_vesels_skaitlis(인터넷주소읽기(adrese_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(dalībnieks),(uintptr_t)&adrese,sizeof(adrese),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_Savienotājs_objekts,saziņa_Stream);
static mp_obj_t 흐름읽기(mp_obj_t dalībnieks,mp_obj_t 한도) {
    int 길이=mp_obj_get_int(한도); if(길이<1||길이>512)mp_raise_OSError(MP_EINVAL);
    unsigned char dati[512];
    intptr_t krājums_COUNT=결과검사(사용자호출(2,mp_obj_get_int(dalībnieks),(uintptr_t)dati,길이,0,0,0));
    return mp_obj_new_bytes(dati,krājums_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Lasītājs_objekts,흐름읽기);
static mp_obj_t rakstīšana_Stream(mp_obj_t dalībnieks,mp_obj_t Saturs_VALUE) {
    mp_buffer_info_t dati; mp_get_buffer_raise(Saturs_VALUE,&dati,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(dalībnieks),(uintptr_t)dati.buf,dati.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Rakstītājs_objekts,rakstīšana_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(pagaidi_objekts,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Nosaukums) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)ceļš_arg(Nosaukums),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t atvērt_Direktorijs(mp_obj_t Nosaukums) {
    결과검사(사용자호출(18,(uintptr_t)ceļš_arg(Nosaukums),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Direktorijs_autors_objekts,atvērt_Direktorijs);
static mp_obj_t noņemt_Direktorijs(mp_obj_t Nosaukums) {
    결과검사(사용자호출(18,(uintptr_t)ceļš_arg(Nosaukums),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,noņemt_Direktorijs);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_Savienotājs_objekts) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_Lasītājs_objekts) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Rakstītājs_objekts) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&pagaidi_objekts) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&Direktorijs_autors_objekts) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&STDIN_Lasītājs_objekts) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Fails_Lasītājs_objekts) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Fails_Rakstītājs_objekts) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&taisnstūris_objekts) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Pulkstenis_objekts) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_atvērt_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_sūtīt_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Aizvērt_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
