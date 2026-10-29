// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "ခေါ်လုပ်.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t ရလဒ်) { if (ရလဒ် < 0) mp_raise_OSError(-ရလဒ်); return ရလဒ်; }
static const char *လမ်းကြောင်းပေးအချက်(mp_obj_t တန်ဖိုး) {
    size_t အရေအတွက်; const char *လမ်း = mp_obj_str_get_data(တန်ဖိုး, &အရေအတွက်);
    if (!အရေအတွက် || အရေအတွက် > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t အစဉ်အမှတ် = 0; အစဉ်အမှတ် < အရေအတွက်; အစဉ်အမှတ်++) if (!လမ်း[အစဉ်အမှတ်]) mp_raise_OSError(MP_EINVAL);
    return လမ်း;
}
static mp_obj_t ဖိုင်ဖတ်(mp_obj_t အမည်) {
    intptr_t ဖိုင်ကိုင်တွယ်ရာ = 결과검사(သုံးစွဲသူခေါ်လုပ်(3, (uintptr_t)လမ်းကြောင်းပေးအချက်(အမည်), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t အရွယ် = 결과검사(သုံးစွဲသူခေါ်လုပ်(9, ဖိုင်ကိုင်တွယ်ရာ, 0, 0, 0, 0, 0));
        vstr_t ဒေတာ; vstr_init_len(&ဒေတာ, အရွယ်);
        intptr_t ရလဒ် = သုံးစွဲသူခေါ်လုပ်(2, ဖိုင်ကိုင်တွယ်ရာ, (uintptr_t)ဒေတာ.buf, အရွယ်, 0, 0, 0);
        결과검사(ရလဒ်); ဒေတာ.len = ရလဒ်;
        mp_obj_t တန်ဖိုး = mp_obj_new_bytes_from_vstr(&ဒေတာ);
        nlr_pop(); သုံးစွဲသူခေါ်လုပ်(4, ဖိုင်ကိုင်တွယ်ရာ, 0, 0, 0, 0, 0); return တန်ဖိုး;
    }
    သုံးစွဲသူခေါ်လုပ်(4, ဖိုင်ကိုင်တွယ်ရာ, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ဖိုင်ဖတ်သူအရာဝတ္ထု, ဖိုင်ဖတ်);
static mp_obj_t စံအဝင်ဖတ်(mp_obj_t ဆံ့ပမာဏအကန့်) {
    mp_int_t အရွယ်=mp_obj_get_int(ဆံ့ပမာဏအကန့်);
    if(အရွယ်<0||အရွယ်>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t ဒေတာ; vstr_init_len(&ဒေတာ,အရွယ်);
    intptr_t အရေအတွက်=သုံးစွဲသူခေါ်လုပ်(2,0,(uintptr_t)ဒေတာ.buf,အရွယ်,0,0,0);
    if(အရေအတွက်<0) { vstr_clear(&ဒေတာ); 결과검사(အရေအတွက်); }
    ဒေတာ.len=အရေအတွက်; return mp_obj_new_bytes_from_vstr(&ဒေတာ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(စံအဝင်ဖတ်သူအရာဝတ္ထု, စံအဝင်ဖတ်);
static mp_obj_t ဖိုင်ရေး(mp_obj_t အမည်, mp_obj_t အကြောင်းအရာတန်ဖိုး) {
    const char *လမ်း = လမ်းကြောင်းပေးအချက်(အမည်);
    mp_buffer_info_t ဒေတာ; mp_get_buffer_raise(အကြောင်းအရာတန်ဖိုး, &ဒေတာ, MP_BUFFER_READ);
    if (ဒေတာ.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ဖိုင်ကိုင်တွယ်ရာ = 결과검사(သုံးစွဲသူခေါ်လုပ်(3, (uintptr_t)လမ်း, 577, 0, 0, 0, 0));
    intptr_t အချက်အရေအတွက် = သုံးစွဲသူခေါ်လုပ်(1, ဖိုင်ကိုင်တွယ်ရာ, (uintptr_t)ဒေတာ.buf, ဒေတာ.len, 0, 0, 0);
    သုံးစွဲသူခေါ်လုပ်(4, ဖိုင်ကိုင်တွယ်ရာ, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(အချက်အရေအတွက်));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ဖိုင်ရေးသူအရာဝတ္ထု, ဖိုင်ရေး);
static mp_obj_t ဖိုင်ဖျက်(mp_obj_t အမည်) { 결과검사(သုံးစွဲသူခေါ်လုပ်(11, (uintptr_t)လမ်းကြောင်းပေးအချက်(အမည်), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, ဖိုင်ဖျက်);
static mp_obj_t 사각형그리기(size_t အရေအတွက်, const mp_obj_t *ပေးအချက်အခင်းအကျင်း) {
    (void)အရေအတွက်; unsigned ပထမတန်ဖိုး[5]; for (unsigned အစဉ်အမှတ် = 0; အစဉ်အမှတ် < 5; အစဉ်အမှတ်++) ပထမတန်ဖိုး[အစဉ်အမှတ်] = mp_obj_get_int(ပေးအချက်အခင်းအကျင်း[အစဉ်အမှတ်]);
    결과검사(မျက်နှာပြင်စတုဂံ(ပထမတန်ဖိုး[0], ပထမတန်ဖိုး[1], ပထမတန်ဖိုး[2], ပထမတန်ဖိုး[3], ပထမတန်ဖိုး[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(စတုဂံအရာဝတ္ထု, 5, 5, 사각형그리기);
static mp_obj_t မျက်နှာပြင်အရွယ်ဖတ်(void) {
    mp_obj_t အရွယ်[2] = {mp_obj_new_int(결과검사(မျက်နှာပြင်အနံဖတ်())), mp_obj_new_int(결과검사(မျက်နှာပြင်အမြင့်ဖတ်()))};
    return mp_obj_new_tuple(2, အရွယ်);
}
static MP_DEFINE_CONST_FUN_OBJ_0(မျက်နှာပြင်အရွယ်အရာဝတ္ထု, မျက်နှာပြင်အရွယ်ဖတ်);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(မျက်နှာပြင်စောင့်အရာဝတ္ထု, 화면입력기다리기);
static mp_obj_t နာရီတန်ဖိုး(void) { return mp_obj_new_int_from_uint(သုံးစွဲသူခေါ်လုပ်(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(နာရီအရာဝတ္ထု, နာရီတန်ဖိုး);
static mp_obj_t UDPဖွင့်(mp_obj_t ဆက်သွယ်ပေါက်ကိန်း) {
    int ဒေတာနေရာ = mp_obj_get_int(ဆက်သွယ်ပေါက်ကိန်း); if (ဒေတာနေရာ < 0 || ဒေတာနေရာ > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ဖိုင်ကိုင်တွယ်ရာ = 결과검사(သုံးစွဲသူခေါ်လုပ်(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in ပထမတန်ဖိုး = {0}; ပထမတန်ဖိုး.sin_family = AF_INET; ပထမတန်ဖိုး.sin_port = pk_htons(ဒေတာနေရာ); ပထမတန်ဖိုး.sin_addr.s_addr = 0;
    intptr_t ရလဒ် = သုံးစွဲသူခေါ်လုပ်(33, ဖိုင်ကိုင်တွယ်ရာ, (uintptr_t)&ပထမတန်ဖိုး, sizeof(ပထမတန်ဖိုး), 0, 0, 0);
    if (ရလဒ် < 0) { သုံးစွဲသူခေါ်လုပ်(4, ဖိုင်ကိုင်တွယ်ရာ, 0, 0, 0, 0, 0); 결과검사(ရလဒ်); }
    return mp_obj_new_int(ဖိုင်ကိုင်တွယ်ရာ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, UDPဖွင့်);
static mp_obj_t UDPပို့(mp_obj_t ဖိုင်ကိုင်တွယ်ရာ, mp_obj_t ဆက်သွယ်ပေါက်ကိန်း, mp_obj_t အကြောင်းအရာတန်ဖိုး) {
    int ဒေတာနေရာ = mp_obj_get_int(ဆက်သွယ်ပေါက်ကိန်း); if (ဒေတာနေရာ < 1 || ဒေတာနေရာ > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ဒေတာ; mp_get_buffer_raise(အကြောင်းအရာတန်ဖိုး, &ဒေတာ, MP_BUFFER_READ);
    struct pk_sockaddr_in ပထမတန်ဖိုး = {0}; ပထမတန်ဖိုး.sin_family = AF_INET; ပထမတန်ဖိုး.sin_port = pk_htons(ဒေတာနေရာ); ပထမတန်ဖိုး.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(သုံးစွဲသူခေါ်လုပ်(34, mp_obj_get_int(ဖိုင်ကိုင်တွယ်ရာ), (uintptr_t)ဒေတာ.buf, ဒေတာ.len, 0, (uintptr_t)&ပထမတန်ဖိုး, sizeof(ပထမတန်ဖိုး))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, UDPပို့);
static uint32_t အင်တာနက်လိပ်စာဖတ်(mp_obj_t တန်ဖိုး) {
    size_t အလျား; const char *စာသား=mp_obj_str_get_data(တန်ဖိုး,&အလျား);
    unsigned လက်ရှိနေရာ=0; uint32_t လိပ်စာ=0;
    for(unsigned အစိတ်အပိုင်းတန်ဖိုး=0;အစိတ်အပိုင်းတန်ဖိုး<4;အစိတ်အပိုင်းတန်ဖိုး++) {
        unsigned တန်ဖိုး=0,ဂဏန်းအရေအတွက်=0;
        while(လက်ရှိနေရာ<အလျား&&စာသား[လက်ရှိနေရာ]>='0'&&စာသား[လက်ရှိနေရာ]<='9') {
            တန်ဖိုး=တန်ဖိုး*10+စာသား[လက်ရှိနေရာ++]-'0'; if(++ဂဏန်းအရေအတွက်>3||တန်ဖိုး>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!ဂဏန်းအရေအတွက်)mp_raise_OSError(MP_EINVAL);
        လိပ်စာ=လိပ်စာ<<8|တန်ဖိုး;
        if(အစိတ်အပိုင်းတန်ဖိုး<3&&(လက်ရှိနေရာ>=အလျား||စာသား[လက်ရှိနေရာ++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(လက်ရှိနေရာ!=အလျား)mp_raise_OSError(MP_EINVAL);
    return လိပ်စာ;
}
static mp_obj_t 전문주소전송(size_t အချက်အရေအတွက်, const mp_obj_t *ပေးအချက်အခင်းအကျင်း) {
    (void)အချက်အရေအတွက်; uint32_t လိပ်စာ=အင်တာနက်လိပ်စာဖတ်(ပေးအချက်အခင်းအကျင်း[1]);
    int ဆက်သွယ်ပေါက်ကိန်း=mp_obj_get_int(ပေးအချက်အခင်းအကျင်း[2]);if(ဆက်သွယ်ပေါက်ကိန်း<1||ဆက်သွယ်ပေါက်ကိန်း>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ဒေတာ;mp_get_buffer_raise(ပေးအချက်အခင်းအကျင်း[3],&ဒေတာ,MP_BUFFER_READ);
    struct pk_sockaddr_in ဦးတည်ချက်တန်ဖိုး={0};ဦးတည်ချက်တန်ဖိုး.sin_family=AF_INET;ဦးတည်ချက်တန်ဖိုး.sin_port=pk_htons(ဆက်သွယ်ပေါက်ကိန်း);ဦးတည်ချက်တန်ဖိုး.sin_addr.s_addr=pk_htonl(လိပ်စာ);
    return mp_obj_new_int(결과검사(သုံးစွဲသူခေါ်လုပ်(34,mp_obj_get_int(ပေးအချက်အခင်းအကျင်း[0]),(uintptr_t)ဒေတာ.buf,ဒေတာ.len,0,(uintptr_t)&ဦးတည်ချက်တန်ဖိုး,sizeof(ဦးတည်ချက်တန်ဖိုး))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ဖိုင်ကိုင်တွယ်ရာ) {
    unsigned char ဒေတာ[512]; struct pk_sockaddr_in တစ်ဖက်တန်ဖိုး; pk_socklen_t အလျားဒေတာ = sizeof(တစ်ဖက်တန်ဖိုး);
    intptr_t အရွယ် = 결과검사(သုံးစွဲသူခေါ်လုပ်(35, mp_obj_get_int(ဖိုင်ကိုင်တွယ်ရာ), (uintptr_t)ဒေတာ, 512, 0, (uintptr_t)&တစ်ဖက်တန်ဖိုး, (uintptr_t)&အလျားဒေတာ));
    mp_obj_t တန်ဖိုးများ[2] = {mp_obj_new_bytes(ဒေတာ, အရွယ်), MP_OBJ_NEW_SMALL_INT(pk_htons(တစ်ဖက်တန်ဖိုး.sin_port))};
    return mp_obj_new_tuple(2, တန်ဖိုးများ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDPပိတ်(mp_obj_t ဖိုင်ကိုင်တွယ်ရာ) { 결과검사(သုံးစွဲသူခေါ်လုပ်(4, mp_obj_get_int(ဖိုင်ကိုင်တွယ်ရာ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, UDPပိတ်);
static mp_obj_t စီးကြောင်းဖွင့်(void) {
    return mp_obj_new_int(결과검사(သုံးစွဲသူခေါ်လုပ်(32,အင်တာနက်မျိုးစု,စီးကြောင်းဆက်သွယ်မှု,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,စီးကြောင်းဖွင့်);
static mp_obj_t စီးကြောင်းချိတ်ဆက်(mp_obj_t ဆုံးမှတ်,mp_obj_t လိပ်စာစာသား,mp_obj_t နံပါတ်) {
    int ဆက်သွယ်ပေါက်ကိန်း=mp_obj_get_int(နံပါတ်); if(ဆက်သွယ်ပေါက်ကိန်း<1||ဆက်သွယ်ပေါက်ကိန်း>65535)mp_raise_OSError(MP_EINVAL);
    struct အင်တာနက်ကွန်ရက်ပေါက်လိပ်စာ လိပ်စာ={0}; လိပ်စာ.လိပ်စာမျိုးစု=အင်တာနက်မျိုးစု;
    လိပ်စာ.ဆက်သွယ်ပေါက်ကိန်း=ကွန်ရက်တို(ဆက်သွယ်ပေါက်ကိန်း); လိပ်စာ.အင်တာနက်လိပ်စာ.လိပ်စာတန်ဖိုး=ကွန်ရက်ကိန်းပြည့်(အင်တာနက်လိပ်စာဖတ်(လိပ်စာစာသား));
    결과검사(သုံးစွဲသူခေါ်လုပ်(37,mp_obj_get_int(ဆုံးမှတ်),(uintptr_t)&လိပ်စာ,sizeof(လိပ်စာ),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(흐름연결객체,စီးကြောင်းချိတ်ဆက်);
static mp_obj_t စီးကြောင်းဖတ်(mp_obj_t ဆုံးမှတ်,mp_obj_t ဆံ့ပမာဏအကန့်) {
    int အလျား=mp_obj_get_int(ဆံ့ပမာဏအကန့်); if(အလျား<1||အလျား>512)mp_raise_OSError(MP_EINVAL);
    unsigned char ဒေတာ[512];
    intptr_t အရေအတွက်=결과검사(သုံးစွဲသူခေါ်လုပ်(2,mp_obj_get_int(ဆုံးမှတ်),(uintptr_t)ဒေတာ,အလျား,0,0,0));
    return mp_obj_new_bytes(ဒေတာ,အရေအတွက်);
}
static MP_DEFINE_CONST_FUN_OBJ_2(စီးကြောင်းဖတ်သူအရာဝတ္ထု,စီးကြောင်းဖတ်);
static mp_obj_t စီးကြောင်းရေး(mp_obj_t ဆုံးမှတ်,mp_obj_t အကြောင်းအရာတန်ဖိုး) {
    mp_buffer_info_t ဒေတာ; mp_get_buffer_raise(အကြောင်းအရာတန်ဖိုး,&ဒေတာ,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(သုံးစွဲသူခေါ်လုပ်(1,mp_obj_get_int(ဆုံးမှတ်),(uintptr_t)ဒေတာ.buf,ဒေတာ.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(စီးကြောင်းရေးသူအရာဝတ္ထု,စီးကြောင်းရေး);
static mp_obj_t 잠시기다리기(mp_obj_t အချိန်တန်ဖိုး) {
    결과검사(သုံးစွဲသူခေါ်လုပ်(17,mp_obj_get_int(အချိန်တန်ဖိုး),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(အရာဝတ္ထုစောင့်,잠시기다리기);
static mp_obj_t အချက်အမျိုးအစား(mp_obj_t အမည်) {
    return mp_obj_new_int(결과검사(သုံးစွဲသူခေါ်လုပ်(18,(uintptr_t)လမ်းကြောင်းပေးအချက်(အမည်),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(အချက်အမျိုးအစားအရာဝတ္ထု,အချက်အမျိုးအစား);
static mp_obj_t ဖိုင်တွဲဖန်တီး(mp_obj_t အမည်) {
    결과검사(သုံးစွဲသူခေါ်လုပ်(18,(uintptr_t)လမ်းကြောင်းပေးအချက်(အမည်),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,ဖိုင်တွဲဖန်တီး);
static mp_obj_t ဖိုင်တွဲဖယ်ရှား(mp_obj_t အမည်) {
    결과검사(သုံးစွဲသူခေါ်လုပ်(18,(uintptr_t)လမ်းကြောင်းပေးအချက်(အမည်),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,ဖိုင်တွဲဖယ်ရှား);
static const mp_rom_map_elem_t မော်ဂျူးအမည်များ[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&흐름연결객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&စီးကြောင်းဖတ်သူအရာဝတ္ထု) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&စီးကြောင်းရေးသူအရာဝတ္ထု) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&အရာဝတ္ထုစောင့်) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&အချက်အမျိုးအစားအရာဝတ္ထု) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&စံအဝင်ဖတ်သူအရာဝတ္ထု) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ဖိုင်ဖတ်သူအရာဝတ္ထု) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&ဖိုင်ရေးသူအရာဝတ္ထု) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&စတုဂံအရာဝတ္ထု) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&မျက်နှာပြင်အရွယ်အရာဝတ္ထု) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&မျက်နှာပြင်စောင့်အရာဝတ္ထု) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&နာရီအရာဝတ္ထု) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, မော်ဂျူးအမည်များ);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
