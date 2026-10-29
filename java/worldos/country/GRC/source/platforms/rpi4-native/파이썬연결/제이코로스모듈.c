// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t μέτρηση) { if (μέτρηση < 0) mp_raise_OSError(-μέτρηση); return μέτρηση; }
static const char *διαδρομή_όρισμα(mp_obj_t τιμή) {
    size_t 개수; const char *ΔΙΑΔΡΟΜΗ = mp_obj_str_get_data(τιμή, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!ΔΙΑΔΡΟΜΗ[순번]) mp_raise_OSError(MP_EINVAL);
    return ΔΙΑΔΡΟΜΗ;
}
static mp_obj_t 파일읽기(mp_obj_t Όνομα) {
    intptr_t Αρχείο_δείκτης_χειρισμού = 결과검사(사용자호출(3, (uintptr_t)διαδρομή_όρισμα(Όνομα), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Μέγεθος = 결과검사(사용자호출(9, Αρχείο_δείκτης_χειρισμού, 0, 0, 0, 0, 0));
        vstr_t δεδομένα; vstr_init_len(&δεδομένα, Μέγεθος);
        intptr_t μέτρηση = 사용자호출(2, Αρχείο_δείκτης_χειρισμού, (uintptr_t)δεδομένα.buf, Μέγεθος, 0, 0, 0);
        결과검사(μέτρηση); δεδομένα.len = μέτρηση;
        mp_obj_t τιμή = mp_obj_new_bytes_from_vstr(&δεδομένα);
        nlr_pop(); 사용자호출(4, Αρχείο_δείκτης_χειρισμού, 0, 0, 0, 0, 0); return τιμή;
    }
    사용자호출(4, Αρχείο_δείκτης_χειρισμού, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Αρχείο_Αναγνώστης_αντικείμενο, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Μέγεθος=mp_obj_get_int(한도);
    if(Μέγεθος<0||Μέγεθος>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t δεδομένα; vstr_init_len(&δεδομένα,Μέγεθος);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)δεδομένα.buf,Μέγεθος,0,0,0);
    if(개수<0) { vstr_clear(&δεδομένα); 결과검사(개수); }
    δεδομένα.len=개수; return mp_obj_new_bytes_from_vstr(&δεδομένα);
}
static MP_DEFINE_CONST_FUN_OBJ_1(τυπική_είσοδος_Αναγνώστης_αντικείμενο, 표준입력읽기);
static mp_obj_t εγγράφω_Αρχείο(mp_obj_t Όνομα, mp_obj_t Περιεχόμενο_τιμή) {
    const char *ΔΙΑΔΡΟΜΗ = διαδρομή_όρισμα(Όνομα);
    mp_buffer_info_t δεδομένα; mp_get_buffer_raise(Περιεχόμενο_τιμή, &δεδομένα, MP_BUFFER_READ);
    if (δεδομένα.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t Αρχείο_δείκτης_χειρισμού = 결과검사(사용자호출(3, (uintptr_t)ΔΙΑΔΡΟΜΗ, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, Αρχείο_δείκτης_χειρισμού, (uintptr_t)δεδομένα.buf, δεδομένα.len, 0, 0, 0);
    사용자호출(4, Αρχείο_δείκτης_χειρισμού, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(파일쓰기객체, εγγράφω_Αρχείο);
static mp_obj_t καταργώ_Αρχείο(mp_obj_t Όνομα) { 결과검사(사용자호출(11, (uintptr_t)διαδρομή_όρισμα(Όνομα), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, καταργώ_Αρχείο);
static mp_obj_t Ζωγραφική_ορθογώνιο(size_t 개수, const mp_obj_t *όρισμα_πίνακας) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(όρισμα_πίνακας[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(ορθογώνιο_αντικείμενο, 5, 5, Ζωγραφική_ορθογώνιο);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Μέγεθος[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Μέγεθος);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Ρολόι_τιμή(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Ρολόι_αντικείμενο, Ρολόι_τιμή);
static mp_obj_t 전문열기(mp_obj_t αριθμός_θύρας) {
    int δεδομένα_θέση = mp_obj_get_int(αριθμός_θύρας); if (δεδομένα_θέση < 0 || δεδομένα_θέση > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t Αρχείο_δείκτης_χειρισμού = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(δεδομένα_θέση); 첫째값.sin_addr.s_addr = 0;
    intptr_t μέτρηση = 사용자호출(33, Αρχείο_δείκτης_χειρισμού, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (μέτρηση < 0) { 사용자호출(4, Αρχείο_δείκτης_χειρισμού, 0, 0, 0, 0, 0); 결과검사(μέτρηση); }
    return mp_obj_new_int(Αρχείο_δείκτης_χειρισμού);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t Αρχείο_δείκτης_χειρισμού, mp_obj_t αριθμός_θύρας, mp_obj_t Περιεχόμενο_τιμή) {
    int δεδομένα_θέση = mp_obj_get_int(αριθμός_θύρας); if (δεδομένα_θέση < 1 || δεδομένα_θέση > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t δεδομένα; mp_get_buffer_raise(Περιεχόμενο_τιμή, &δεδομένα, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(δεδομένα_θέση); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(Αρχείο_δείκτης_χειρισμού), (uintptr_t)δεδομένα.buf, δεδομένα.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t τιμή) {
    size_t διάρκεια_τιμή; const char *Κείμενο=mp_obj_str_get_data(τιμή,&διάρκεια_τιμή);
    unsigned τρέχων_θέση=0; uint32_t διεύθυνση=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned τιμή=0,숫자수=0;
        while(τρέχων_θέση<διάρκεια_τιμή&&Κείμενο[τρέχων_θέση]>='0'&&Κείμενο[τρέχων_θέση]<='9') {
            τιμή=τιμή*10+Κείμενο[τρέχων_θέση++]-'0'; if(++숫자수>3||τιμή>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        διεύθυνση=διεύθυνση<<8|τιμή;
        if(부분<3&&(τρέχων_θέση>=διάρκεια_τιμή||Κείμενο[τρέχων_θέση++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(τρέχων_θέση!=διάρκεια_τιμή)mp_raise_OSError(MP_EINVAL);
    return διεύθυνση;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *όρισμα_πίνακας) {
    (void)항목수; uint32_t διεύθυνση=인터넷주소읽기(όρισμα_πίνακας[1]);
    int αριθμός_θύρας=mp_obj_get_int(όρισμα_πίνακας[2]);if(αριθμός_θύρας<1||αριθμός_θύρας>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t δεδομένα;mp_get_buffer_raise(όρισμα_πίνακας[3],&δεδομένα,MP_BUFFER_READ);
    struct pk_sockaddr_in τιμή_στόχος={0};τιμή_στόχος.sin_family=AF_INET;τιμή_στόχος.sin_port=pk_htons(αριθμός_θύρας);τιμή_στόχος.sin_addr.s_addr=pk_htonl(διεύθυνση);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(όρισμα_πίνακας[0]),(uintptr_t)δεδομένα.buf,δεδομένα.len,0,(uintptr_t)&τιμή_στόχος,sizeof(τιμή_στόχος))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t Αρχείο_δείκτης_χειρισμού) {
    unsigned char δεδομένα[512]; struct pk_sockaddr_in ομότιμος_τιμή; pk_socklen_t διάρκεια_δεδομένα = sizeof(ομότιμος_τιμή);
    intptr_t Μέγεθος = 결과검사(사용자호출(35, mp_obj_get_int(Αρχείο_δείκτης_χειρισμού), (uintptr_t)δεδομένα, 512, 0, (uintptr_t)&ομότιμος_τιμή, (uintptr_t)&διάρκεια_δεδομένα));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(δεδομένα, Μέγεθος), MP_OBJ_NEW_SMALL_INT(pk_htons(ομότιμος_τιμή.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t Αρχείο_δείκτης_χειρισμού) { 결과검사(사용자호출(4, mp_obj_get_int(Αρχείο_δείκτης_χειρισμού), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t ανοίγω_ροή(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,πλέγμα_παιδικά,ροή_δίκτυο,ροή_πρωτόκολλο_μεταφοράς,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,ανοίγω_ροή);
static mp_obj_t συνδέω_ροή(mp_obj_t τελικό_σημείο,mp_obj_t διεύθυνση_μήνυμα,mp_obj_t Ευρετήριο) {
    int αριθμός_θύρας=mp_obj_get_int(Ευρετήριο); if(αριθμός_θύρας<1||αριθμός_θύρας>65535)mp_raise_OSError(MP_EINVAL);
    struct πλέγμα_υποδοχή_διεύθυνση διεύθυνση={0}; διεύθυνση.διεύθυνση_παιδικά=πλέγμα_παιδικά;
    διεύθυνση.αριθμός_θύρας=망차례짧은수(αριθμός_θύρας); διεύθυνση.διεύθυνση_Internet.διεύθυνση_τιμή=δίκτυο_ακέραιος(인터넷주소읽기(διεύθυνση_μήνυμα));
    결과검사(사용자호출(37,mp_obj_get_int(τελικό_σημείο),(uintptr_t)&διεύθυνση,sizeof(διεύθυνση),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ροή_Σύνδεση_αντικείμενο,συνδέω_ροή);
static mp_obj_t 흐름읽기(mp_obj_t τελικό_σημείο,mp_obj_t 한도) {
    int διάρκεια_τιμή=mp_obj_get_int(한도); if(διάρκεια_τιμή<1||διάρκεια_τιμή>512)mp_raise_OSError(MP_EINVAL);
    unsigned char δεδομένα[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(τελικό_σημείο),(uintptr_t)δεδομένα,διάρκεια_τιμή,0,0,0));
    return mp_obj_new_bytes(δεδομένα,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ροή_Αναγνώστης_αντικείμενο,흐름읽기);
static mp_obj_t εγγράφω_ροή(mp_obj_t τελικό_σημείο,mp_obj_t Περιεχόμενο_τιμή) {
    mp_buffer_info_t δεδομένα; mp_get_buffer_raise(Περιεχόμενο_τιμή,&δεδομένα,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(τελικό_σημείο),(uintptr_t)δεδομένα.buf,δεδομένα.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(흐름쓰기객체,εγγράφω_ροή);
static mp_obj_t 잠시기다리기(mp_obj_t τιμή_ώρας) {
    결과검사(사용자호출(17,mp_obj_get_int(τιμή_ώρας),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(περίμενε_αντικείμενο,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Όνομα) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)διαδρομή_όρισμα(Όνομα),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t ανοίγω_Κατάλογος(mp_obj_t Όνομα) {
    결과검사(사용자호출(18,(uintptr_t)διαδρομή_όρισμα(Όνομα),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Κατάλογος_συντάκτης_αντικείμενο,ανοίγω_Κατάλογος);
static mp_obj_t καταργώ_Κατάλογος(mp_obj_t Όνομα) {
    결과검사(사용자호출(18,(uintptr_t)διαδρομή_όρισμα(Όνομα),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,καταργώ_Κατάλογος);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ροή_Σύνδεση_αντικείμενο) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ροή_Αναγνώστης_αντικείμενο) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&흐름쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&περίμενε_αντικείμενο) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&Κατάλογος_συντάκτης_αντικείμενο) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&τυπική_είσοδος_Αναγνώστης_αντικείμενο) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Αρχείο_Αναγνώστης_αντικείμενο) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&파일쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&ορθογώνιο_αντικείμενο) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Ρολόι_αντικείμενο) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
