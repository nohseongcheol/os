// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *Hanyar_shiga_Tubalin_aiki(mp_obj_t Daraja) {
    size_t 개수; const char *Hanyar_shiga = mp_obj_str_get_data(Daraja, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!Hanyar_shiga[순번]) mp_raise_OSError(MP_EINVAL);
    return Hanyar_shiga;
}
static mp_obj_t 파일읽기(mp_obj_t Suna) {
    intptr_t Fayil_Mariki = 결과검사(사용자호출(3, (uintptr_t)Hanyar_shiga_Tubalin_aiki(Suna), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Girma = 결과검사(사용자호출(9, Fayil_Mariki, 0, 0, 0, 0, 0));
        vstr_t Tarin_bayani; vstr_init_len(&Tarin_bayani, Girma);
        intptr_t 결과 = 사용자호출(2, Fayil_Mariki, (uintptr_t)Tarin_bayani.buf, Girma, 0, 0, 0);
        결과검사(결과); Tarin_bayani.len = 결과;
        mp_obj_t Daraja = mp_obj_new_bytes_from_vstr(&Tarin_bayani);
        nlr_pop(); 사용자호출(4, Fayil_Mariki, 0, 0, 0, 0, 0); return Daraja;
    }
    사용자호출(4, Fayil_Mariki, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Fayil_Manazarci_abu, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Girma=mp_obj_get_int(한도);
    if(Girma<0||Girma>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t Tarin_bayani; vstr_init_len(&Tarin_bayani,Girma);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)Tarin_bayani.buf,Girma,0,0,0);
    if(개수<0) { vstr_clear(&Tarin_bayani); 결과검사(개수); }
    Tarin_bayani.len=개수; return mp_obj_new_bytes_from_vstr(&Tarin_bayani);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t Rubuta_Fayil(mp_obj_t Suna, mp_obj_t kunshiya_Daraja) {
    const char *Hanyar_shiga = Hanyar_shiga_Tubalin_aiki(Suna);
    mp_buffer_info_t Tarin_bayani; mp_get_buffer_raise(kunshiya_Daraja, &Tarin_bayani, MP_BUFFER_READ);
    if (Tarin_bayani.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t Fayil_Mariki = 결과검사(사용자호출(3, (uintptr_t)Hanyar_shiga, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, Fayil_Mariki, (uintptr_t)Tarin_bayani.buf, Tarin_bayani.len, 0, 0, 0);
    사용자호출(4, Fayil_Mariki, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Fayil_Marubuci_abu, Rubuta_Fayil);
static mp_obj_t Cire_Fayil(mp_obj_t Suna) { 결과검사(사용자호출(11, (uintptr_t)Hanyar_shiga_Tubalin_aiki(Suna), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, Cire_Fayil);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *Tubalin_aiki_TSARI) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(Tubalin_aiki_TSARI[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Girma[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Girma);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t agogo_Daraja(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(agogo_abu, agogo_Daraja);
static mp_obj_t 전문열기(mp_obj_t lambar_kafa) {
    int 자료위치 = mp_obj_get_int(lambar_kafa); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t Fayil_Mariki = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, Fayil_Mariki, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, Fayil_Mariki, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(Fayil_Mariki);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t Fayil_Mariki, mp_obj_t lambar_kafa, mp_obj_t kunshiya_Daraja) {
    int 자료위치 = mp_obj_get_int(lambar_kafa); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t Tarin_bayani; mp_get_buffer_raise(kunshiya_Daraja, &Tarin_bayani, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(Fayil_Mariki), (uintptr_t)Tarin_bayani.buf, Tarin_bayani.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t Daraja) {
    size_t Tsawo_Daraja; const char *SMS=mp_obj_str_get_data(Daraja,&Tsawo_Daraja);
    unsigned 현재위치=0; uint32_t imel=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned Daraja=0,숫자수=0;
        while(현재위치<Tsawo_Daraja&&SMS[현재위치]>='0'&&SMS[현재위치]<='9') {
            Daraja=Daraja*10+SMS[현재위치++]-'0'; if(++숫자수>3||Daraja>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        imel=imel<<8|Daraja;
        if(부분<3&&(현재위치>=Tsawo_Daraja||SMS[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=Tsawo_Daraja)mp_raise_OSError(MP_EINVAL);
    return imel;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *Tubalin_aiki_TSARI) {
    (void)항목수; uint32_t imel=인터넷주소읽기(Tubalin_aiki_TSARI[1]);
    int lambar_kafa=mp_obj_get_int(Tubalin_aiki_TSARI[2]);if(lambar_kafa<1||lambar_kafa>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t Tarin_bayani;mp_get_buffer_raise(Tubalin_aiki_TSARI[3],&Tarin_bayani,MP_BUFFER_READ);
    struct pk_sockaddr_in tageti={0};tageti.sin_family=AF_INET;tageti.sin_port=pk_htons(lambar_kafa);tageti.sin_addr.s_addr=pk_htonl(imel);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(Tubalin_aiki_TSARI[0]),(uintptr_t)Tarin_bayani.buf,Tarin_bayani.len,0,(uintptr_t)&tageti,sizeof(tageti))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t Fayil_Mariki) {
    unsigned char Tarin_bayani[512]; struct pk_sockaddr_in Fiya_Daraja; pk_socklen_t Tsawo_Tarin_bayani = sizeof(Fiya_Daraja);
    intptr_t Girma = 결과검사(사용자호출(35, mp_obj_get_int(Fayil_Mariki), (uintptr_t)Tarin_bayani, 512, 0, (uintptr_t)&Fiya_Daraja, (uintptr_t)&Tsawo_Tarin_bayani));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(Tarin_bayani, Girma), MP_OBJ_NEW_SMALL_INT(pk_htons(Fiya_Daraja.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t Fayil_Mariki) { 결과검사(사용자호출(4, mp_obj_get_int(Fayil_Mariki), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t buɗe_watsuwa(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,Intanet_Iyali,watsuwa_Hanyar_sadarwa,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,buɗe_watsuwa);
static mp_obj_t HAƊI_watsuwa(mp_obj_t 종단,mp_obj_t imel_SMS,mp_obj_t Indes) {
    int lambar_kafa=mp_obj_get_int(Indes); if(lambar_kafa<1||lambar_kafa>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 imel={0}; imel.imel_Iyali=Intanet_Iyali;
    imel.lambar_kafa=망차례짧은수(lambar_kafa); imel.Adireshin_yanar_gizo.imel_Daraja=Hanyar_sadarwa_Lamba_mara(인터넷주소읽기(imel_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&imel,sizeof(imel),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(watsuwa_na_urar_haɗawa_abu,HAƊI_watsuwa);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int Tsawo_Daraja=mp_obj_get_int(한도); if(Tsawo_Daraja<1||Tsawo_Daraja>512)mp_raise_OSError(MP_EINVAL);
    unsigned char Tarin_bayani[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)Tarin_bayani,Tsawo_Daraja,0,0,0));
    return mp_obj_new_bytes(Tarin_bayani,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(watsuwa_Manazarci_abu,흐름읽기);
static mp_obj_t Rubuta_watsuwa(mp_obj_t 종단,mp_obj_t kunshiya_Daraja) {
    mp_buffer_info_t Tarin_bayani; mp_get_buffer_raise(kunshiya_Daraja,&Tarin_bayani,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)Tarin_bayani.buf,Tarin_bayani.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(watsuwa_Marubuci_abu,Rubuta_watsuwa);
static mp_obj_t 잠시기다리기(mp_obj_t lokaci_Daraja) {
    결과검사(사용자호출(17,mp_obj_get_int(lokaci_Daraja),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(jira_abu,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Suna) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)Hanyar_shiga_Tubalin_aiki(Suna),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t ƙirƙíra_ma_ajiya(mp_obj_t Suna) {
    결과검사(사용자호출(18,(uintptr_t)Hanyar_shiga_Tubalin_aiki(Suna),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,ƙirƙíra_ma_ajiya);
static mp_obj_t Cire_ma_ajiya(mp_obj_t Suna) {
    결과검사(사용자호출(18,(uintptr_t)Hanyar_shiga_Tubalin_aiki(Suna),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,Cire_ma_ajiya);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&watsuwa_na_urar_haɗawa_abu) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&watsuwa_Manazarci_abu) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&watsuwa_Marubuci_abu) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&jira_abu) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Fayil_Manazarci_abu) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Fayil_Marubuci_abu) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&agogo_abu) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
