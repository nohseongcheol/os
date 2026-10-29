// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t ukuran) { if (ukuran < 0) mp_raise_OSError(-ukuran); return ukuran; }
static const char *laluan_argumen(mp_obj_t VALUE) {
    size_t item_COUNT; const char *LALUAN = mp_obj_str_get_data(VALUE, &item_COUNT);
    if (!item_COUNT || item_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < item_COUNT; 순번++) if (!LALUAN[순번]) mp_raise_OSError(MP_EINVAL);
    return LALUAN;
}
static mp_obj_t 파일읽기(mp_obj_t Nama) {
    intptr_t fail_pemegang = 결과검사(사용자호출(3, (uintptr_t)laluan_argumen(Nama), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Saiz = 결과검사(사용자호출(9, fail_pemegang, 0, 0, 0, 0, 0));
        vstr_t data; vstr_init_len(&data, Saiz);
        intptr_t ukuran = 사용자호출(2, fail_pemegang, (uintptr_t)data.buf, Saiz, 0, 0, 0);
        결과검사(ukuran); data.len = ukuran;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&data);
        nlr_pop(); 사용자호출(4, fail_pemegang, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, fail_pemegang, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(fail_Pembaca_objek, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Saiz=mp_obj_get_int(한도);
    if(Saiz<0||Saiz>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t data; vstr_init_len(&data,Saiz);
    intptr_t item_COUNT=사용자호출(2,0,(uintptr_t)data.buf,Saiz,0,0,0);
    if(item_COUNT<0) { vstr_clear(&data); 결과검사(item_COUNT); }
    data.len=item_COUNT; return mp_obj_new_bytes_from_vstr(&data);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t tulis_fail(mp_obj_t Nama, mp_obj_t Kandungan_VALUE) {
    const char *LALUAN = laluan_argumen(Nama);
    mp_buffer_info_t data; mp_get_buffer_raise(Kandungan_VALUE, &data, MP_BUFFER_READ);
    if (data.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t fail_pemegang = 결과검사(사용자호출(3, (uintptr_t)LALUAN, 577, 0, 0, 0, 0));
    intptr_t pemasukan_COUNT = 사용자호출(1, fail_pemegang, (uintptr_t)data.buf, data.len, 0, 0, 0);
    사용자호출(4, fail_pemegang, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(pemasukan_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(fail_Penulis_objek, tulis_fail);
static mp_obj_t alih_keluar_fail(mp_obj_t Nama) { 결과검사(사용자호출(11, (uintptr_t)laluan_argumen(Nama), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, alih_keluar_fail);
static mp_obj_t Paint_segi_empat_tepat(size_t item_COUNT, const mp_obj_t *argumen_ARRAY) {
    (void)item_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argumen_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(segi_empat_tepat_objek, 5, 5, Paint_segi_empat_tepat);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Saiz[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Saiz);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Jam_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Jam_objek, Jam_VALUE);
static mp_obj_t UDP_buka(mp_obj_t nombor_port) {
    int data_jawatan = mp_obj_get_int(nombor_port); if (data_jawatan < 0 || data_jawatan > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t fail_pemegang = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_jawatan); 첫째값.sin_addr.s_addr = 0;
    intptr_t ukuran = 사용자호출(33, fail_pemegang, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (ukuran < 0) { 사용자호출(4, fail_pemegang, 0, 0, 0, 0, 0); 결과검사(ukuran); }
    return mp_obj_new_int(fail_pemegang);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_buka_OBJ, UDP_buka);
static mp_obj_t UDP_e_mel_c88d0659(mp_obj_t fail_pemegang, mp_obj_t nombor_port, mp_obj_t Kandungan_VALUE) {
    int data_jawatan = mp_obj_get_int(nombor_port); if (data_jawatan < 1 || data_jawatan > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data; mp_get_buffer_raise(Kandungan_VALUE, &data, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_jawatan); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(fail_pemegang), (uintptr_t)data.buf, data.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_e_mel_OBJ, UDP_e_mel_c88d0659);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t kepanjangan_VALUE; const char *Teks=mp_obj_str_get_data(VALUE,&kepanjangan_VALUE);
    unsigned 현재위치=0; uint32_t e_mel=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,digit_COUNT=0;
        while(현재위치<kepanjangan_VALUE&&Teks[현재위치]>='0'&&Teks[현재위치]<='9') {
            VALUE=VALUE*10+Teks[현재위치++]-'0'; if(++digit_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!digit_COUNT)mp_raise_OSError(MP_EINVAL);
        e_mel=e_mel<<8|VALUE;
        if(부분<3&&(현재위치>=kepanjangan_VALUE||Teks[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=kepanjangan_VALUE)mp_raise_OSError(MP_EINVAL);
    return e_mel;
}
static mp_obj_t 전문주소전송(size_t pemasukan_COUNT, const mp_obj_t *argumen_ARRAY) {
    (void)pemasukan_COUNT; uint32_t e_mel=인터넷주소읽기(argumen_ARRAY[1]);
    int nombor_port=mp_obj_get_int(argumen_ARRAY[2]);if(nombor_port<1||nombor_port>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data;mp_get_buffer_raise(argumen_ARRAY[3],&data,MP_BUFFER_READ);
    struct pk_sockaddr_in sasaran={0};sasaran.sin_family=AF_INET;sasaran.sin_port=pk_htons(nombor_port);sasaran.sin_addr.s_addr=pk_htonl(e_mel);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argumen_ARRAY[0]),(uintptr_t)data.buf,data.len,0,(uintptr_t)&sasaran,sizeof(sasaran))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t fail_pemegang) {
    unsigned char data[512]; struct pk_sockaddr_in rakan_VALUE; pk_socklen_t kepanjangan_data = sizeof(rakan_VALUE);
    intptr_t Saiz = 결과검사(사용자호출(35, mp_obj_get_int(fail_pemegang), (uintptr_t)data, 512, 0, (uintptr_t)&rakan_VALUE, (uintptr_t)&kepanjangan_data));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(data, Saiz), MP_OBJ_NEW_SMALL_INT(pk_htons(rakan_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Tutup(mp_obj_t fail_pemegang) { 결과검사(사용자호출(4, mp_obj_get_int(fail_pemegang), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Tutup_OBJ, UDP_Tutup);
static mp_obj_t buka_strim(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,awan_Keluarga,strim_rangkaian,strim_protokol_pengangkutan,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,buka_strim);
static mp_obj_t CONNECT_strim(mp_obj_t peserta,mp_obj_t e_mel_SMS,mp_obj_t INDEX) {
    int nombor_port=mp_obj_get_int(INDEX); if(nombor_port<1||nombor_port>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 e_mel={0}; e_mel.e_mel_Keluarga=awan_Keluarga;
    e_mel.nombor_port=망차례짧은수(nombor_port); e_mel.alamat_Internet.e_mel_VALUE=rangkaian_integer(인터넷주소읽기(e_mel_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(peserta),(uintptr_t)&e_mel,sizeof(e_mel),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(strim_Penyambung_objek,CONNECT_strim);
static mp_obj_t 흐름읽기(mp_obj_t peserta,mp_obj_t 한도) {
    int kepanjangan_VALUE=mp_obj_get_int(한도); if(kepanjangan_VALUE<1||kepanjangan_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char data[512];
    intptr_t item_COUNT=결과검사(사용자호출(2,mp_obj_get_int(peserta),(uintptr_t)data,kepanjangan_VALUE,0,0,0));
    return mp_obj_new_bytes(data,item_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(strim_Pembaca_objek,흐름읽기);
static mp_obj_t tulis_strim(mp_obj_t peserta,mp_obj_t Kandungan_VALUE) {
    mp_buffer_info_t data; mp_get_buffer_raise(Kandungan_VALUE,&data,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(peserta),(uintptr_t)data.buf,data.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(strim_Penulis_objek,tulis_strim);
static mp_obj_t 잠시기다리기(mp_obj_t nilai_masa) {
    결과검사(사용자호출(17,mp_obj_get_int(nilai_masa),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(tunggu_objek,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Nama) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)laluan_argumen(Nama),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t cipta_direktori(mp_obj_t Nama) {
    결과검사(사용자호출(18,(uintptr_t)laluan_argumen(Nama),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(direktori_pencipta_objek,cipta_direktori);
static mp_obj_t alih_keluar_direktori(mp_obj_t Nama) {
    결과검사(사용자호출(18,(uintptr_t)laluan_argumen(Nama),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,alih_keluar_direktori);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&strim_Penyambung_objek) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&strim_Pembaca_objek) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&strim_Penulis_objek) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&tunggu_objek) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&direktori_pencipta_objek) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&fail_Pembaca_objek) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&fail_Penulis_objek) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&segi_empat_tepat_objek) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Jam_objek) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_buka_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_e_mel_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Tutup_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
