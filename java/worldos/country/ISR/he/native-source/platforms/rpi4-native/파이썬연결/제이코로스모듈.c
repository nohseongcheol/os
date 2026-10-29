// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t תוצאה) { if (תוצאה < 0) mp_raise_OSError(-תוצאה); return תוצאה; }
static const char *נתיב_ארגומנט(mp_obj_t ערך) {
    size_t 개수; const char *נתיב = mp_obj_str_get_data(ערך, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!נתיב[순번]) mp_raise_OSError(MP_EINVAL);
    return נתיב;
}
static mp_obj_t 파일읽기(mp_obj_t שם) {
    intptr_t קובץ_נקודת_אחיזה = 결과검사(사용자호출(3, (uintptr_t)נתיב_ארגומנט(שם), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t גודל = 결과검사(사용자호출(9, קובץ_נקודת_אחיזה, 0, 0, 0, 0, 0));
        vstr_t נתונים; vstr_init_len(&נתונים, גודל);
        intptr_t תוצאה = 사용자호출(2, קובץ_נקודת_אחיזה, (uintptr_t)נתונים.buf, גודל, 0, 0, 0);
        결과검사(תוצאה); נתונים.len = תוצאה;
        mp_obj_t ערך = mp_obj_new_bytes_from_vstr(&נתונים);
        nlr_pop(); 사용자호출(4, קובץ_נקודת_אחיזה, 0, 0, 0, 0, 0); return ערך;
    }
    사용자호출(4, קובץ_נקודת_אחיזה, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(קובץ_קורא_אובייקט, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t גודל=mp_obj_get_int(한도);
    if(גודל<0||גודל>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t נתונים; vstr_init_len(&נתונים,גודל);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)נתונים.buf,גודל,0,0,0);
    if(개수<0) { vstr_clear(&נתונים); 결과검사(개수); }
    נתונים.len=개수; return mp_obj_new_bytes_from_vstr(&נתונים);
}
static MP_DEFINE_CONST_FUN_OBJ_1(תקן_קלט_קורא_אובייקט, 표준입력읽기);
static mp_obj_t כתיבה_קובץ(mp_obj_t שם, mp_obj_t תוכן_ערך) {
    const char *נתיב = נתיב_ארגומנט(שם);
    mp_buffer_info_t נתונים; mp_get_buffer_raise(תוכן_ערך, &נתונים, MP_BUFFER_READ);
    if (נתונים.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t קובץ_נקודת_אחיזה = 결과검사(사용자호출(3, (uintptr_t)נתיב, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, קובץ_נקודת_אחיזה, (uintptr_t)נתונים.buf, נתונים.len, 0, 0, 0);
    사용자호출(4, קובץ_נקודת_אחיזה, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(קובץ_כתבן_אובייקט, כתיבה_קובץ);
static mp_obj_t הסר_קובץ(mp_obj_t שם) { 결과검사(사용자호출(11, (uintptr_t)נתיב_ארגומנט(שם), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, הסר_קובץ);
static mp_obj_t צייר_מלבן(size_t 개수, const mp_obj_t *ארגומנט_מערך) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(ארגומנט_מערך[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(מלבן_אובייקט, 5, 5, צייר_מלבן);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t גודל[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, גודל);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t שעון_ערך(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(שעון_אובייקט, שעון_ערך);
static mp_obj_t פרוטוקול_יחידת_נתונים_של_משתמש_פתח(mp_obj_t מספר_יציאה) {
    int נתונים_עמדה = mp_obj_get_int(מספר_יציאה); if (נתונים_עמדה < 0 || נתונים_עמדה > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t קובץ_נקודת_אחיזה = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(נתונים_עמדה); 첫째값.sin_addr.s_addr = 0;
    intptr_t תוצאה = 사용자호출(33, קובץ_נקודת_אחיזה, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (תוצאה < 0) { 사용자호출(4, קובץ_נקודת_אחיזה, 0, 0, 0, 0, 0); 결과검사(תוצאה); }
    return mp_obj_new_int(קובץ_נקודת_אחיזה);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, פרוטוקול_יחידת_נתונים_של_משתמש_פתח);
static mp_obj_t פרוטוקול_יחידת_נתונים_של_משתמש_שלח(mp_obj_t קובץ_נקודת_אחיזה, mp_obj_t מספר_יציאה, mp_obj_t תוכן_ערך) {
    int נתונים_עמדה = mp_obj_get_int(מספר_יציאה); if (נתונים_עמדה < 1 || נתונים_עמדה > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t נתונים; mp_get_buffer_raise(תוכן_ערך, &נתונים, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(נתונים_עמדה); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(קובץ_נקודת_אחיזה), (uintptr_t)נתונים.buf, נתונים.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, פרוטוקול_יחידת_נתונים_של_משתמש_שלח);
static uint32_t 인터넷주소읽기(mp_obj_t ערך) {
    size_t 길이; const char *טקסט=mp_obj_str_get_data(ערך,&길이);
    unsigned נוכחי_עמדה=0; uint32_t למען=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned ערך=0,숫자수=0;
        while(נוכחי_עמדה<길이&&טקסט[נוכחי_עמדה]>='0'&&טקסט[נוכחי_עמדה]<='9') {
            ערך=ערך*10+טקסט[נוכחי_עמדה++]-'0'; if(++숫자수>3||ערך>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        למען=למען<<8|ערך;
        if(부분<3&&(נוכחי_עמדה>=길이||טקסט[נוכחי_עמדה++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(נוכחי_עמדה!=길이)mp_raise_OSError(MP_EINVAL);
    return למען;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *ארגומנט_מערך) {
    (void)항목수; uint32_t למען=인터넷주소읽기(ארגומנט_מערך[1]);
    int מספר_יציאה=mp_obj_get_int(ארגומנט_מערך[2]);if(מספר_יציאה<1||מספר_יציאה>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t נתונים;mp_get_buffer_raise(ארגומנט_מערך[3],&נתונים,MP_BUFFER_READ);
    struct pk_sockaddr_in יעד={0};יעד.sin_family=AF_INET;יעד.sin_port=pk_htons(מספר_יציאה);יעד.sin_addr.s_addr=pk_htonl(למען);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(ארגומנט_מערך[0]),(uintptr_t)נתונים.buf,נתונים.len,0,(uintptr_t)&יעד,sizeof(יעד))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t קובץ_נקודת_אחיזה) {
    unsigned char נתונים[512]; struct pk_sockaddr_in עמית_ערך; pk_socklen_t 길이값 = sizeof(עמית_ערך);
    intptr_t גודל = 결과검사(사용자호출(35, mp_obj_get_int(קובץ_נקודת_אחיזה), (uintptr_t)נתונים, 512, 0, (uintptr_t)&עמית_ערך, (uintptr_t)&길이값));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(נתונים, גודל), MP_OBJ_NEW_SMALL_INT(pk_htons(עמית_ערך.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t פרוטוקול_יחידת_נתונים_של_משתמש_סגור(mp_obj_t קובץ_נקודת_אחיזה) { 결과검사(사용자호출(4, mp_obj_get_int(קובץ_נקודת_אחיזה), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, פרוטוקול_יחידת_נתונים_של_משתמש_סגור);
static mp_obj_t פתח_זרם(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,ענן_משפחה,זרם_רשת,זרם_פרוטוקול_תעבורה,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,פתח_זרם);
static mp_obj_t לקשר_זרם(mp_obj_t משתתף,mp_obj_t למען_טקסט,mp_obj_t מדד) {
    int מספר_יציאה=mp_obj_get_int(מדד); if(מספר_יציאה<1||מספר_יציאה>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 למען={0}; למען.למען_משפחה=ענן_משפחה;
    למען.מספר_יציאה=망차례짧은수(מספר_יציאה); למען.כתובת_אינטרנט.למען_ערך=רשת_מספר_שלם(인터넷주소읽기(למען_טקסט));
    결과검사(사용자호출(37,mp_obj_get_int(משתתף),(uintptr_t)&למען,sizeof(למען),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(זרם_מחבר_אובייקט,לקשר_זרם);
static mp_obj_t 흐름읽기(mp_obj_t משתתף,mp_obj_t 한도) {
    int 길이=mp_obj_get_int(한도); if(길이<1||길이>512)mp_raise_OSError(MP_EINVAL);
    unsigned char נתונים[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(משתתף),(uintptr_t)נתונים,길이,0,0,0));
    return mp_obj_new_bytes(נתונים,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(זרם_קורא_אובייקט,흐름읽기);
static mp_obj_t כתיבה_זרם(mp_obj_t משתתף,mp_obj_t תוכן_ערך) {
    mp_buffer_info_t נתונים; mp_get_buffer_raise(תוכן_ערך,&נתונים,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(משתתף),(uintptr_t)נתונים.buf,נתונים.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(זרם_כתבן_אובייקט,כתיבה_זרם);
static mp_obj_t 잠시기다리기(mp_obj_t ערך_זמן) {
    결과검사(사용자호출(17,mp_obj_get_int(ערך_זמן),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(רק_רגע_אובייקט,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t שם) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)נתיב_ארגומנט(שם),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t ליצור_מדריך(mp_obj_t שם) {
    결과검사(사용자호출(18,(uintptr_t)נתיב_ארגומנט(שם),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(מדריך_יוצר_אובייקט,ליצור_מדריך);
static mp_obj_t הסר_מדריך(mp_obj_t שם) {
    결과검사(사용자호출(18,(uintptr_t)נתיב_ארגומנט(שם),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,הסר_מדריך);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&זרם_מחבר_אובייקט) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&זרם_קורא_אובייקט) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&זרם_כתבן_אובייקט) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&רק_רגע_אובייקט) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&מדריך_יוצר_אובייקט) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&תקן_קלט_קורא_אובייקט) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&קובץ_קורא_אובייקט) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&קובץ_כתבן_אובייקט) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&מלבן_אובייקט) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&שעון_אובייקט) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
