// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t TULEMUS) { if (TULEMUS < 0) mp_raise_OSError(-TULEMUS); return TULEMUS; }
static const char *tee_argument(mp_obj_t VALUE) {
    size_t kaup_COUNT; const char *RADA = mp_obj_str_get_data(VALUE, &kaup_COUNT);
    if (!kaup_COUNT || kaup_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < kaup_COUNT; 순번++) if (!RADA[순번]) mp_raise_OSError(MP_EINVAL);
    return RADA;
}
static mp_obj_t 파일읽기(mp_obj_t Nimi_2) {
    intptr_t Fail_pide = 결과검사(사용자호출(3, (uintptr_t)tee_argument(Nimi_2), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Suurus = 결과검사(사용자호출(9, Fail_pide, 0, 0, 0, 0, 0));
        vstr_t andmed; vstr_init_len(&andmed, Suurus);
        intptr_t TULEMUS = 사용자호출(2, Fail_pide, (uintptr_t)andmed.buf, Suurus, 0, 0, 0);
        결과검사(TULEMUS); andmed.len = TULEMUS;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&andmed);
        nlr_pop(); 사용자호출(4, Fail_pide, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, Fail_pide, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Fail_Reader_objekt, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Suurus=mp_obj_get_int(한도);
    if(Suurus<0||Suurus>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t andmed; vstr_init_len(&andmed,Suurus);
    intptr_t kaup_COUNT=사용자호출(2,0,(uintptr_t)andmed.buf,Suurus,0,0,0);
    if(kaup_COUNT<0) { vstr_clear(&andmed); 결과검사(kaup_COUNT); }
    andmed.len=kaup_COUNT; return mp_obj_new_bytes_from_vstr(&andmed);
}
static MP_DEFINE_CONST_FUN_OBJ_1(STDIN_Reader_objekt, 표준입력읽기);
static mp_obj_t kirjutamine_Fail(mp_obj_t Nimi_2, mp_obj_t Sisu_VALUE) {
    const char *RADA = tee_argument(Nimi_2);
    mp_buffer_info_t andmed; mp_get_buffer_raise(Sisu_VALUE, &andmed, MP_BUFFER_READ);
    if (andmed.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t Fail_pide = 결과검사(사용자호출(3, (uintptr_t)RADA, 577, 0, 0, 0, 0));
    intptr_t kirje_COUNT = 사용자호출(1, Fail_pide, (uintptr_t)andmed.buf, andmed.len, 0, 0, 0);
    사용자호출(4, Fail_pide, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(kirje_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Fail_Writer_objekt, kirjutamine_Fail);
static mp_obj_t eemaldama_Fail(mp_obj_t Nimi_2) { 결과검사(사용자호출(11, (uintptr_t)tee_argument(Nimi_2), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, eemaldama_Fail);
static mp_obj_t Paint_ristkülik(size_t kaup_COUNT, const mp_obj_t *argument_ARRAY) {
    (void)kaup_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argument_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(ristkülik_objekt, 5, 5, Paint_ristkülik);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Suurus[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Suurus);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Kell_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Kell_objekt, Kell_VALUE);
static mp_obj_t UDP_avama(mp_obj_t pordinumber) {
    int andmed_ametikoht = mp_obj_get_int(pordinumber); if (andmed_ametikoht < 0 || andmed_ametikoht > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t Fail_pide = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(andmed_ametikoht); 첫째값.sin_addr.s_addr = 0;
    intptr_t TULEMUS = 사용자호출(33, Fail_pide, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (TULEMUS < 0) { 사용자호출(4, Fail_pide, 0, 0, 0, 0, 0); 결과검사(TULEMUS); }
    return mp_obj_new_int(Fail_pide);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_avama_OBJ, UDP_avama);
static mp_obj_t UDP_saatma(mp_obj_t Fail_pide, mp_obj_t pordinumber, mp_obj_t Sisu_VALUE) {
    int andmed_ametikoht = mp_obj_get_int(pordinumber); if (andmed_ametikoht < 1 || andmed_ametikoht > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t andmed; mp_get_buffer_raise(Sisu_VALUE, &andmed, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(andmed_ametikoht); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(Fail_pide), (uintptr_t)andmed.buf, andmed.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_saatma_OBJ, UDP_saatma);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t 길이; const char *Tekst=mp_obj_str_get_data(VALUE,&길이);
    unsigned tähtaja_piires_ametikoht=0; uint32_t ADDRESS=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,number_COUNT=0;
        while(tähtaja_piires_ametikoht<길이&&Tekst[tähtaja_piires_ametikoht]>='0'&&Tekst[tähtaja_piires_ametikoht]<='9') {
            VALUE=VALUE*10+Tekst[tähtaja_piires_ametikoht++]-'0'; if(++number_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!number_COUNT)mp_raise_OSError(MP_EINVAL);
        ADDRESS=ADDRESS<<8|VALUE;
        if(부분<3&&(tähtaja_piires_ametikoht>=길이||Tekst[tähtaja_piires_ametikoht++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(tähtaja_piires_ametikoht!=길이)mp_raise_OSError(MP_EINVAL);
    return ADDRESS;
}
static mp_obj_t 전문주소전송(size_t kirje_COUNT, const mp_obj_t *argument_ARRAY) {
    (void)kirje_COUNT; uint32_t ADDRESS=인터넷주소읽기(argument_ARRAY[1]);
    int pordinumber=mp_obj_get_int(argument_ARRAY[2]);if(pordinumber<1||pordinumber>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t andmed;mp_get_buffer_raise(argument_ARRAY[3],&andmed,MP_BUFFER_READ);
    struct pk_sockaddr_in siht={0};siht.sin_family=AF_INET;siht.sin_port=pk_htons(pordinumber);siht.sin_addr.s_addr=pk_htonl(ADDRESS);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argument_ARRAY[0]),(uintptr_t)andmed.buf,andmed.len,0,(uintptr_t)&siht,sizeof(siht))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t Fail_pide) {
    unsigned char andmed[512]; struct pk_sockaddr_in partner_VALUE; pk_socklen_t 길이값 = sizeof(partner_VALUE);
    intptr_t Suurus = 결과검사(사용자호출(35, mp_obj_get_int(Fail_pide), (uintptr_t)andmed, 512, 0, (uintptr_t)&partner_VALUE, (uintptr_t)&길이값));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(andmed, Suurus), MP_OBJ_NEW_SMALL_INT(pk_htons(partner_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Sule(mp_obj_t Fail_pide) { 결과검사(사용자호출(4, mp_obj_get_int(Fail_pide), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Sule_OBJ, UDP_Sule);
static mp_obj_t avama_voog(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,pilv_Pere,voog_võrk,voog_transpordiprotokoll,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,avama_voog);
static mp_obj_t Ühenda_voog(mp_obj_t osaleja,mp_obj_t ADDRESS_SMS,mp_obj_t INDEX) {
    int pordinumber=mp_obj_get_int(INDEX); if(pordinumber<1||pordinumber>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ADDRESS={0}; ADDRESS.ADDRESS_Pere=pilv_Pere;
    ADDRESS.pordinumber=망차례짧은수(pordinumber); ADDRESS.Interneti_aadress.ADDRESS_VALUE=võrk_täisarv(인터넷주소읽기(ADDRESS_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(osaleja),(uintptr_t)&ADDRESS,sizeof(ADDRESS),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(voog_liitmik_objekt,Ühenda_voog);
static mp_obj_t 흐름읽기(mp_obj_t osaleja,mp_obj_t 한도) {
    int 길이=mp_obj_get_int(한도); if(길이<1||길이>512)mp_raise_OSError(MP_EINVAL);
    unsigned char andmed[512];
    intptr_t kaup_COUNT=결과검사(사용자호출(2,mp_obj_get_int(osaleja),(uintptr_t)andmed,길이,0,0,0));
    return mp_obj_new_bytes(andmed,kaup_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(voog_Reader_objekt,흐름읽기);
static mp_obj_t kirjutamine_voog(mp_obj_t osaleja,mp_obj_t Sisu_VALUE) {
    mp_buffer_info_t andmed; mp_get_buffer_raise(Sisu_VALUE,&andmed,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(osaleja),(uintptr_t)andmed.buf,andmed.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(voog_Writer_objekt,kirjutamine_voog);
static mp_obj_t 잠시기다리기(mp_obj_t Aeg_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(Aeg_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Oota_objekt,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Nimi_2) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)tee_argument(Nimi_2),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t avama_kaust(mp_obj_t Nimi_2) {
    결과검사(사용자호출(18,(uintptr_t)tee_argument(Nimi_2),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(kaust_autor_objekt,avama_kaust);
static mp_obj_t eemaldama_kaust(mp_obj_t Nimi_2) {
    결과검사(사용자호출(18,(uintptr_t)tee_argument(Nimi_2),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,eemaldama_kaust);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&voog_liitmik_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&voog_Reader_objekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&voog_Writer_objekt) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&Oota_objekt) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&kaust_autor_objekt) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&STDIN_Reader_objekt) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Fail_Reader_objekt) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Fail_Writer_objekt) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&ristkülik_objekt) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Kell_objekt) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_avama_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_saatma_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Sule_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
