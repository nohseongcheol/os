// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t hasil) { if (hasil < 0) mp_raise_OSError(-hasil); return hasil; }
static const char *jalur_argumen(mp_obj_t VALUE) {
    size_t item_COUNT; const char *jalur = mp_obj_str_get_data(VALUE, &item_COUNT);
    if (!item_COUNT || item_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < item_COUNT; 순번++) if (!jalur[순번]) mp_raise_OSError(MP_EINVAL);
    return jalur;
}
static mp_obj_t 파일읽기(mp_obj_t Nama_2) {
    intptr_t file_handel = 결과검사(사용자호출(3, (uintptr_t)jalur_argumen(Nama_2), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Ukuran = 결과검사(사용자호출(9, file_handel, 0, 0, 0, 0, 0));
        vstr_t data; vstr_init_len(&data, Ukuran);
        intptr_t hasil = 사용자호출(2, file_handel, (uintptr_t)data.buf, Ukuran, 0, 0, 0);
        결과검사(hasil); data.len = hasil;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&data);
        nlr_pop(); 사용자호출(4, file_handel, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, file_handel, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(file_Pembaca_objek, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Ukuran=mp_obj_get_int(한도);
    if(Ukuran<0||Ukuran>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t data; vstr_init_len(&data,Ukuran);
    intptr_t item_COUNT=사용자호출(2,0,(uintptr_t)data.buf,Ukuran,0,0,0);
    if(item_COUNT<0) { vstr_clear(&data); 결과검사(item_COUNT); }
    data.len=item_COUNT; return mp_obj_new_bytes_from_vstr(&data);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t tulis_file(mp_obj_t Nama_2, mp_obj_t Isi_VALUE) {
    const char *jalur = jalur_argumen(Nama_2);
    mp_buffer_info_t data; mp_get_buffer_raise(Isi_VALUE, &data, MP_BUFFER_READ);
    if (data.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t file_handel = 결과검사(사용자호출(3, (uintptr_t)jalur, 577, 0, 0, 0, 0));
    intptr_t entri_COUNT = 사용자호출(1, file_handel, (uintptr_t)data.buf, data.len, 0, 0, 0);
    사용자호출(4, file_handel, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(entri_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(file_Writer_objek, tulis_file);
static mp_obj_t hapus_file(mp_obj_t Nama_2) { 결과검사(사용자호출(11, (uintptr_t)jalur_argumen(Nama_2), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, hapus_file);
static mp_obj_t Paint_persegi(size_t item_COUNT, const mp_obj_t *argumen_ARRAY) {
    (void)item_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argumen_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(persegi_objek, 5, 5, Paint_persegi);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Ukuran[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Ukuran);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Jam_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Jam_objek, Jam_VALUE);
static mp_obj_t UDP_buat(mp_obj_t nomor_port) {
    int data_posisi = mp_obj_get_int(nomor_port); if (data_posisi < 0 || data_posisi > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t file_handel = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_posisi); 첫째값.sin_addr.s_addr = 0;
    intptr_t hasil = 사용자호출(33, file_handel, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (hasil < 0) { 사용자호출(4, file_handel, 0, 0, 0, 0, 0); 결과검사(hasil); }
    return mp_obj_new_int(file_handel);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_buat_OBJ, UDP_buat);
static mp_obj_t UDP_kirim(mp_obj_t file_handel, mp_obj_t nomor_port, mp_obj_t Isi_VALUE) {
    int data_posisi = mp_obj_get_int(nomor_port); if (data_posisi < 1 || data_posisi > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data; mp_get_buffer_raise(Isi_VALUE, &data, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_posisi); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(file_handel), (uintptr_t)data.buf, data.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_kirim_OBJ, UDP_kirim);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t panjang_VALUE; const char *teks=mp_obj_str_get_data(VALUE,&panjang_VALUE);
    unsigned saat_ini_posisi=0; uint32_t surel=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,angka_COUNT=0;
        while(saat_ini_posisi<panjang_VALUE&&teks[saat_ini_posisi]>='0'&&teks[saat_ini_posisi]<='9') {
            VALUE=VALUE*10+teks[saat_ini_posisi++]-'0'; if(++angka_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!angka_COUNT)mp_raise_OSError(MP_EINVAL);
        surel=surel<<8|VALUE;
        if(부분<3&&(saat_ini_posisi>=panjang_VALUE||teks[saat_ini_posisi++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(saat_ini_posisi!=panjang_VALUE)mp_raise_OSError(MP_EINVAL);
    return surel;
}
static mp_obj_t 전문주소전송(size_t entri_COUNT, const mp_obj_t *argumen_ARRAY) {
    (void)entri_COUNT; uint32_t surel=인터넷주소읽기(argumen_ARRAY[1]);
    int nomor_port=mp_obj_get_int(argumen_ARRAY[2]);if(nomor_port<1||nomor_port>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data;mp_get_buffer_raise(argumen_ARRAY[3],&data,MP_BUFFER_READ);
    struct pk_sockaddr_in target={0};target.sin_family=AF_INET;target.sin_port=pk_htons(nomor_port);target.sin_addr.s_addr=pk_htonl(surel);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argumen_ARRAY[0]),(uintptr_t)data.buf,data.len,0,(uintptr_t)&target,sizeof(target))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t file_handel) {
    unsigned char data[512]; struct pk_sockaddr_in serekan_VALUE; pk_socklen_t panjang_data = sizeof(serekan_VALUE);
    intptr_t Ukuran = 결과검사(사용자호출(35, mp_obj_get_int(file_handel), (uintptr_t)data, 512, 0, (uintptr_t)&serekan_VALUE, (uintptr_t)&panjang_data));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(data, Ukuran), MP_OBJ_NEW_SMALL_INT(pk_htons(serekan_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Tutup(mp_obj_t file_handel) { 결과검사(사용자호출(4, mp_obj_get_int(file_handel), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Tutup_OBJ, UDP_Tutup);
static mp_obj_t buat_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,cloud_famili,Stream_jaringan,Stream_protokol_transportasi,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,buat_Stream);
static mp_obj_t CONNECT_Stream(mp_obj_t peserta,mp_obj_t surel_SMS,mp_obj_t INDEX) {
    int nomor_port=mp_obj_get_int(INDEX); if(nomor_port<1||nomor_port>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 surel={0}; surel.surel_famili=cloud_famili;
    surel.nomor_port=망차례짧은수(nomor_port); surel.Alamat_internet.surel_VALUE=jaringan_bilangan_bulat(인터넷주소읽기(surel_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(peserta),(uintptr_t)&surel,sizeof(surel),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_Konektor_objek,CONNECT_Stream);
static mp_obj_t 흐름읽기(mp_obj_t peserta,mp_obj_t 한도) {
    int panjang_VALUE=mp_obj_get_int(한도); if(panjang_VALUE<1||panjang_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char data[512];
    intptr_t item_COUNT=결과검사(사용자호출(2,mp_obj_get_int(peserta),(uintptr_t)data,panjang_VALUE,0,0,0));
    return mp_obj_new_bytes(data,item_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Pembaca_objek,흐름읽기);
static mp_obj_t tulis_Stream(mp_obj_t peserta,mp_obj_t Isi_VALUE) {
    mp_buffer_info_t data; mp_get_buffer_raise(Isi_VALUE,&data,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(peserta),(uintptr_t)data.buf,data.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Writer_objek,tulis_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(tunggu_objek,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Nama_2) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)jalur_argumen(Nama_2),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Buat_Direktori(mp_obj_t Nama_2) {
    결과검사(사용자호출(18,(uintptr_t)jalur_argumen(Nama_2),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Direktori_kreator_objek,Buat_Direktori);
static mp_obj_t hapus_Direktori(mp_obj_t Nama_2) {
    결과검사(사용자호출(18,(uintptr_t)jalur_argumen(Nama_2),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,hapus_Direktori);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_Konektor_objek) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_Pembaca_objek) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Writer_objek) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&tunggu_objek) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&Direktori_kreator_objek) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&file_Pembaca_objek) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&file_Writer_objek) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&persegi_objek) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Jam_objek) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_buat_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_kirim_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Tutup_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
