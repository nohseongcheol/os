// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *indlela_isiniki_myalelo(mp_obj_t ixabiso) {
    size_t 개수; const char *INDLELA = mp_obj_str_get_data(ixabiso, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!INDLELA[순번]) mp_raise_OSError(MP_EINVAL);
    return INDLELA;
}
static mp_obj_t 파일읽기(mp_obj_t Igama) {
    intptr_t ifayile_isibambi = 결과검사(사용자호출(3, (uintptr_t)indlela_isiniki_myalelo(Igama), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Ubukhulu = 결과검사(사용자호출(9, ifayile_isibambi, 0, 0, 0, 0, 0));
        vstr_t iingcombolo; vstr_init_len(&iingcombolo, Ubukhulu);
        intptr_t 결과 = 사용자호출(2, ifayile_isibambi, (uintptr_t)iingcombolo.buf, Ubukhulu, 0, 0, 0);
        결과검사(결과); iingcombolo.len = 결과;
        mp_obj_t ixabiso = mp_obj_new_bytes_from_vstr(&iingcombolo);
        nlr_pop(); 사용자호출(4, ifayile_isibambi, 0, 0, 0, 0, 0); return ixabiso;
    }
    사용자호출(4, ifayile_isibambi, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ifayile_Umfundi_into, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Ubukhulu=mp_obj_get_int(한도);
    if(Ubukhulu<0||Ubukhulu>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t iingcombolo; vstr_init_len(&iingcombolo,Ubukhulu);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)iingcombolo.buf,Ubukhulu,0,0,0);
    if(개수<0) { vstr_clear(&iingcombolo); 결과검사(개수); }
    iingcombolo.len=개수; return mp_obj_new_bytes_from_vstr(&iingcombolo);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t bhala_ifayile(mp_obj_t Igama, mp_obj_t Isiqulatho_ixabiso) {
    const char *INDLELA = indlela_isiniki_myalelo(Igama);
    mp_buffer_info_t iingcombolo; mp_get_buffer_raise(Isiqulatho_ixabiso, &iingcombolo, MP_BUFFER_READ);
    if (iingcombolo.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ifayile_isibambi = 결과검사(사용자호출(3, (uintptr_t)INDLELA, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ifayile_isibambi, (uintptr_t)iingcombolo.buf, iingcombolo.len, 0, 0, 0);
    사용자호출(4, ifayile_isibambi, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ifayile_Isibhali_into, bhala_ifayile);
static mp_obj_t shenxisa_ifayile(mp_obj_t Igama) { 결과검사(사용자호출(11, (uintptr_t)indlela_isiniki_myalelo(Igama), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, shenxisa_ifayile);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *isiniki_myalelo_ULUHLU) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(isiniki_myalelo_ULUHLU[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Ubukhulu[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Ubukhulu);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t iwotshi_ixabiso(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(iwotshi_into, iwotshi_ixabiso);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ifayile_isibambi = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, ifayile_isibambi, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, ifayile_isibambi, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(ifayile_isibambi);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t ifayile_isibambi, mp_obj_t 접속번호, mp_obj_t Isiqulatho_ixabiso) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t iingcombolo; mp_get_buffer_raise(Isiqulatho_ixabiso, &iingcombolo, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ifayile_isibambi), (uintptr_t)iingcombolo.buf, iingcombolo.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t ixabiso) {
    size_t ubude_ixabiso; const char *Umbhalo=mp_obj_str_get_data(ixabiso,&ubude_ixabiso);
    unsigned 현재위치=0; uint32_t idilesi=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned ixabiso=0,숫자수=0;
        while(현재위치<ubude_ixabiso&&Umbhalo[현재위치]>='0'&&Umbhalo[현재위치]<='9') {
            ixabiso=ixabiso*10+Umbhalo[현재위치++]-'0'; if(++숫자수>3||ixabiso>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        idilesi=idilesi<<8|ixabiso;
        if(부분<3&&(현재위치>=ubude_ixabiso||Umbhalo[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=ubude_ixabiso)mp_raise_OSError(MP_EINVAL);
    return idilesi;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *isiniki_myalelo_ULUHLU) {
    (void)항목수; uint32_t idilesi=인터넷주소읽기(isiniki_myalelo_ULUHLU[1]);
    int 접속번호=mp_obj_get_int(isiniki_myalelo_ULUHLU[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t iingcombolo;mp_get_buffer_raise(isiniki_myalelo_ULUHLU[3],&iingcombolo,MP_BUFFER_READ);
    struct pk_sockaddr_in ithagethi={0};ithagethi.sin_family=AF_INET;ithagethi.sin_port=pk_htons(접속번호);ithagethi.sin_addr.s_addr=pk_htonl(idilesi);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(isiniki_myalelo_ULUHLU[0]),(uintptr_t)iingcombolo.buf,iingcombolo.len,0,(uintptr_t)&ithagethi,sizeof(ithagethi))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ifayile_isibambi) {
    unsigned char iingcombolo[512]; struct pk_sockaddr_in untanga_ixabiso; pk_socklen_t ubude_iingcombolo = sizeof(untanga_ixabiso);
    intptr_t Ubukhulu = 결과검사(사용자호출(35, mp_obj_get_int(ifayile_isibambi), (uintptr_t)iingcombolo, 512, 0, (uintptr_t)&untanga_ixabiso, (uintptr_t)&ubude_iingcombolo));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(iingcombolo, Ubukhulu), MP_OBJ_NEW_SMALL_INT(pk_htons(untanga_ixabiso.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t ifayile_isibambi) { 결과검사(사용자호출(4, mp_obj_get_int(ifayile_isibambi), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t vula_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,ilifu_Usapho,Stream_Inethiwekhi,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,vula_Stream);
static mp_obj_t I_Connect_Stream(mp_obj_t 종단,mp_obj_t idilesi_I_SMS,mp_obj_t indeksa) {
    int 접속번호=mp_obj_get_int(indeksa); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 idilesi={0}; idilesi.idilesi_Usapho=ilifu_Usapho;
    idilesi.접속번호=망차례짧은수(접속번호); idilesi.idilesi_yeintanethi.idilesi_ixabiso=Inethiwekhi_inani_elipheleleyo(인터넷주소읽기(idilesi_I_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&idilesi,sizeof(idilesi),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_isidibanisi_into,I_Connect_Stream);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int ubude_ixabiso=mp_obj_get_int(한도); if(ubude_ixabiso<1||ubude_ixabiso>512)mp_raise_OSError(MP_EINVAL);
    unsigned char iingcombolo[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)iingcombolo,ubude_ixabiso,0,0,0));
    return mp_obj_new_bytes(iingcombolo,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Umfundi_into,흐름읽기);
static mp_obj_t bhala_Stream(mp_obj_t 종단,mp_obj_t Isiqulatho_ixabiso) {
    mp_buffer_info_t iingcombolo; mp_get_buffer_raise(Isiqulatho_ixabiso,&iingcombolo,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)iingcombolo.buf,iingcombolo.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Isibhali_into,bhala_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Igama) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)indlela_isiniki_myalelo(Igama),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t yila_isalathisi(mp_obj_t Igama) {
    결과검사(사용자호출(18,(uintptr_t)indlela_isiniki_myalelo(Igama),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,yila_isalathisi);
static mp_obj_t shenxisa_isalathisi(mp_obj_t Igama) {
    결과검사(사용자호출(18,(uintptr_t)indlela_isiniki_myalelo(Igama),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,shenxisa_isalathisi);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_isidibanisi_into) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_Umfundi_into) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Isibhali_into) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ifayile_Umfundi_into) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&ifayile_Isibhali_into) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&iwotshi_into) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
