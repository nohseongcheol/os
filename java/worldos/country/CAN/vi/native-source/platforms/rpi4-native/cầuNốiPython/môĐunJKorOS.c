// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "gọiThựcHiện.h"
#include "ABIMạng.h"
static intptr_t đãKiểmTra(intptr_t kếtQuả) { if (kếtQuả < 0) mp_raise_OSError(-kếtQuả); return kếtQuả; }
static const char *đốiSốĐườngDẫn(mp_obj_t giáTrị) {
    size_t sốLượngPhầnMục; const char *đườngDẫn = mp_obj_str_get_data(giáTrị, &sốLượngPhầnMục);
    if (!sốLượngPhầnMục || sốLượngPhầnMục > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngPhầnMục; chỉSốThứBậc++) if (!đườngDẫn[chỉSốThứBậc]) mp_raise_OSError(MP_EINVAL);
    return đườngDẫn;
}
static mp_obj_t đọcTệp(mp_obj_t tên) {
    intptr_t thẻXửLýTệp = đãKiểmTra(gọiThựcHiệnNgườiDùng(3, (uintptr_t)đốiSốĐườngDẫn(tên), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t trảVềCụcBộPhi;
    if (nlr_push(&trảVềCụcBộPhi) == 0) {
        size_t cỡ = đãKiểmTra(gọiThựcHiệnNgườiDùng(9, thẻXửLýTệp, 0, 0, 0, 0, 0));
        vstr_t DữLiệu; vstr_init_len(&DữLiệu, cỡ);
        intptr_t kếtQuả = gọiThựcHiệnNgườiDùng(2, thẻXửLýTệp, (uintptr_t)DữLiệu.buf, cỡ, 0, 0, 0);
        đãKiểmTra(kếtQuả); DữLiệu.len = kếtQuả;
        mp_obj_t giáTrị = mp_obj_new_bytes_from_vstr(&DữLiệu);
        nlr_pop(); gọiThựcHiệnNgườiDùng(4, thẻXửLýTệp, 0, 0, 0, 0, 0); return giáTrị;
    }
    gọiThựcHiệnNgườiDùng(4, thẻXửLýTệp, 0, 0, 0, 0, 0); nlr_jump(trảVềCụcBộPhi.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(đốiTượngBộĐọcTệp, đọcTệp);
static mp_obj_t đọcĐầuVàoChuẩn(mp_obj_t giớiHạnSứcChứa) {
    mp_int_t cỡ=mp_obj_get_int(giớiHạnSứcChứa);
    if(cỡ<0||cỡ>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t DữLiệu; vstr_init_len(&DữLiệu,cỡ);
    intptr_t sốLượngPhầnMục=gọiThựcHiệnNgườiDùng(2,0,(uintptr_t)DữLiệu.buf,cỡ,0,0,0);
    if(sốLượngPhầnMục<0) { vstr_clear(&DữLiệu); đãKiểmTra(sốLượngPhầnMục); }
    DữLiệu.len=sốLượngPhầnMục; return mp_obj_new_bytes_from_vstr(&DữLiệu);
}
static MP_DEFINE_CONST_FUN_OBJ_1(đốiTượngBộĐọcĐầuVàoChuẩn, đọcĐầuVàoChuẩn);
static mp_obj_t ghiTệp(mp_obj_t tên, mp_obj_t giáTrịNộiDung) {
    const char *đườngDẫn = đốiSốĐườngDẫn(tên);
    mp_buffer_info_t DữLiệu; mp_get_buffer_raise(giáTrịNộiDung, &DữLiệu, MP_BUFFER_READ);
    if (DữLiệu.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t thẻXửLýTệp = đãKiểmTra(gọiThựcHiệnNgườiDùng(3, (uintptr_t)đườngDẫn, 577, 0, 0, 0, 0));
    intptr_t sốLượngMục = gọiThựcHiệnNgườiDùng(1, thẻXửLýTệp, (uintptr_t)DữLiệu.buf, DữLiệu.len, 0, 0, 0);
    gọiThựcHiệnNgườiDùng(4, thẻXửLýTệp, 0, 0, 0, 0, 0); return mp_obj_new_int(đãKiểmTra(sốLượngMục));
}
static MP_DEFINE_CONST_FUN_OBJ_2(đốiTượngBộGhiTệp, ghiTệp);
static mp_obj_t gỡTệp(mp_obj_t tên) { đãKiểmTra(gọiThựcHiệnNgườiDùng(11, (uintptr_t)đốiSốĐườngDẫn(tên), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(đốiTượngBộGỡTệp, gỡTệp);
static mp_obj_t hìnhChữNhậtTô(size_t sốLượngPhầnMục, const mp_obj_t *mảngĐốiSố) {
    (void)sốLượngPhầnMục; unsigned giáTrịĐầuTiên[5]; for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < 5; chỉSốThứBậc++) giáTrịĐầuTiên[chỉSốThứBậc] = mp_obj_get_int(mảngĐốiSố[chỉSốThứBậc]);
    đãKiểmTra(hìnhChữNhậtMànHình(giáTrịĐầuTiên[0], giáTrịĐầuTiên[1], giáTrịĐầuTiên[2], giáTrịĐầuTiên[3], giáTrịĐầuTiên[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(đốiTượngHìnhChữNhật, 5, 5, hìnhChữNhậtTô);
static mp_obj_t đọcCỡMànHình(void) {
    mp_obj_t cỡ[2] = {mp_obj_new_int(đãKiểmTra(đọcRộngMànHình())), mp_obj_new_int(đãKiểmTra(đọcCaoMànHình()))};
    return mp_obj_new_tuple(2, cỡ);
}
static MP_DEFINE_CONST_FUN_OBJ_0(đốiTượngCỡMànHình, đọcCỡMànHình);
static mp_obj_t chờĐầuVàoMànHìnhCho(void) { return mp_obj_new_int(đãKiểmTra(chờPhímMànHìnhCho())); }
static MP_DEFINE_CONST_FUN_OBJ_0(đốiTượngChờMànHình, chờĐầuVàoMànHìnhCho);
static mp_obj_t giáTrịĐồngHồ(void) { return mp_obj_new_int_from_uint(gọiThựcHiệnNgườiDùng(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(đốiTượngĐồngHồ, giáTrịĐồngHồ);
static mp_obj_t mởUDP(mp_obj_t sốCổng) {
    int vịTríDữLiệu = mp_obj_get_int(sốCổng); if (vịTríDữLiệu < 0 || vịTríDữLiệu > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t thẻXửLýTệp = đãKiểmTra(gọiThựcHiệnNgườiDùng(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in giáTrịĐầuTiên = {0}; giáTrịĐầuTiên.sin_family = AF_INET; giáTrịĐầuTiên.sin_port = pk_htons(vịTríDữLiệu); giáTrịĐầuTiên.sin_addr.s_addr = 0;
    intptr_t kếtQuả = gọiThựcHiệnNgườiDùng(33, thẻXửLýTệp, (uintptr_t)&giáTrịĐầuTiên, sizeof(giáTrịĐầuTiên), 0, 0, 0);
    if (kếtQuả < 0) { gọiThựcHiệnNgườiDùng(4, thẻXửLýTệp, 0, 0, 0, 0, 0); đãKiểmTra(kếtQuả); }
    return mp_obj_new_int(thẻXửLýTệp);
}
static MP_DEFINE_CONST_FUN_OBJ_1(đốiTượngGọnMởUDP, mởUDP);
static mp_obj_t gửiUDP(mp_obj_t thẻXửLýTệp, mp_obj_t sốCổng, mp_obj_t giáTrịNộiDung) {
    int vịTríDữLiệu = mp_obj_get_int(sốCổng); if (vịTríDữLiệu < 1 || vịTríDữLiệu > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t DữLiệu; mp_get_buffer_raise(giáTrịNộiDung, &DữLiệu, MP_BUFFER_READ);
    struct pk_sockaddr_in giáTrịĐầuTiên = {0}; giáTrịĐầuTiên.sin_family = AF_INET; giáTrịĐầuTiên.sin_port = pk_htons(vịTríDữLiệu); giáTrịĐầuTiên.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(đãKiểmTra(gọiThựcHiệnNgườiDùng(34, mp_obj_get_int(thẻXửLýTệp), (uintptr_t)DữLiệu.buf, DữLiệu.len, 0, (uintptr_t)&giáTrịĐầuTiên, sizeof(giáTrịĐầuTiên))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(đốiTượngGọnGửiUDP, gửiUDP);
static uint32_t đọcĐịaChỉLiênMạng(mp_obj_t giáTrị) {
    size_t độDài; const char *vănBản=mp_obj_str_get_data(giáTrị,&độDài);
    unsigned vịTríHiệnTại=0; uint32_t địaChỉ=0;
    for(unsigned giáTrịPhầnCon=0;giáTrịPhầnCon<4;giáTrịPhầnCon++) {
        unsigned giáTrị=0,sốLượngChữSố=0;
        while(vịTríHiệnTại<độDài&&vănBản[vịTríHiệnTại]>='0'&&vănBản[vịTríHiệnTại]<='9') {
            giáTrị=giáTrị*10+vănBản[vịTríHiệnTại++]-'0'; if(++sốLượngChữSố>3||giáTrị>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!sốLượngChữSố)mp_raise_OSError(MP_EINVAL);
        địaChỉ=địaChỉ<<8|giáTrị;
        if(giáTrịPhầnCon<3&&(vịTríHiệnTại>=độDài||vănBản[vịTríHiệnTại++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(vịTríHiệnTại!=độDài)mp_raise_OSError(MP_EINVAL);
    return địaChỉ;
}
static mp_obj_t gửiĐếnUDP(size_t sốLượngMục, const mp_obj_t *mảngĐốiSố) {
    (void)sốLượngMục; uint32_t địaChỉ=đọcĐịaChỉLiênMạng(mảngĐốiSố[1]);
    int sốCổng=mp_obj_get_int(mảngĐốiSố[2]);if(sốCổng<1||sốCổng>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t DữLiệu;mp_get_buffer_raise(mảngĐốiSố[3],&DữLiệu,MP_BUFFER_READ);
    struct pk_sockaddr_in giáTrịĐốiĐích={0};giáTrịĐốiĐích.sin_family=AF_INET;giáTrịĐốiĐích.sin_port=pk_htons(sốCổng);giáTrịĐốiĐích.sin_addr.s_addr=pk_htonl(địaChỉ);
    return mp_obj_new_int(đãKiểmTra(gọiThựcHiệnNgườiDùng(34,mp_obj_get_int(mảngĐốiSố[0]),(uintptr_t)DữLiệu.buf,DữLiệu.len,0,(uintptr_t)&giáTrịĐốiĐích,sizeof(giáTrịĐốiĐích))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(đốiTượngGọnGửiĐếnUDP,4,4,gửiĐếnUDP);
static mp_obj_t nhậnGọnUDP(mp_obj_t thẻXửLýTệp) {
    unsigned char DữLiệu[512]; struct pk_sockaddr_in giáTrịĐốiTác; pk_socklen_t dữLiệuĐộDài = sizeof(giáTrịĐốiTác);
    intptr_t cỡ = đãKiểmTra(gọiThựcHiệnNgườiDùng(35, mp_obj_get_int(thẻXửLýTệp), (uintptr_t)DữLiệu, 512, 0, (uintptr_t)&giáTrịĐốiTác, (uintptr_t)&dữLiệuĐộDài));
    mp_obj_t cácGiáTrị[2] = {mp_obj_new_bytes(DữLiệu, cỡ), MP_OBJ_NEW_SMALL_INT(pk_htons(giáTrịĐốiTác.sin_port))};
    return mp_obj_new_tuple(2, cácGiáTrị);
}
static MP_DEFINE_CONST_FUN_OBJ_1(đốiTượngGọnNhậnGọnUDP, nhậnGọnUDP);
static mp_obj_t đóngUDP(mp_obj_t thẻXửLýTệp) { đãKiểmTra(gọiThựcHiệnNgườiDùng(4, mp_obj_get_int(thẻXửLýTệp), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(đốiTượngGọnĐóngUDP, đóngUDP);
static mp_obj_t mởLuồng(void) {
    return mp_obj_new_int(đãKiểmTra(gọiThựcHiệnNgườiDùng(32,HọLiênMạng,MạngLuồng,giaoThứcVậnChuyểnLuồng,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(đốiTượngBộMởLuồng,mởLuồng);
static mp_obj_t kếtNốiLuồng(mp_obj_t điểmCuối,mp_obj_t vănBảnĐịaChỉ,mp_obj_t sốHiệu) {
    int sốCổng=mp_obj_get_int(sốHiệu); if(sốCổng<1||sốCổng>65535)mp_raise_OSError(MP_EINVAL);
    struct ĐịaChỉỔCắmMạngLiênMạng địaChỉ={0}; địaChỉ.họĐịaChỉ=HọLiênMạng;
    địaChỉ.sốCổng=ngắnKiểuMạng(sốCổng); địaChỉ.ĐịaChỉLiênMạng.giáTrịĐịaChỉ=sốNguyênMạng(đọcĐịaChỉLiênMạng(vănBảnĐịaChỉ));
    đãKiểmTra(gọiThựcHiệnNgườiDùng(37,mp_obj_get_int(điểmCuối),(uintptr_t)&địaChỉ,sizeof(địaChỉ),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(đốiTượngĐầuNốiLuồng,kếtNốiLuồng);
static mp_obj_t đọcLuồng(mp_obj_t điểmCuối,mp_obj_t giớiHạnSứcChứa) {
    int độDài=mp_obj_get_int(giớiHạnSứcChứa); if(độDài<1||độDài>512)mp_raise_OSError(MP_EINVAL);
    unsigned char DữLiệu[512];
    intptr_t sốLượngPhầnMục=đãKiểmTra(gọiThựcHiệnNgườiDùng(2,mp_obj_get_int(điểmCuối),(uintptr_t)DữLiệu,độDài,0,0,0));
    return mp_obj_new_bytes(DữLiệu,sốLượngPhầnMục);
}
static MP_DEFINE_CONST_FUN_OBJ_2(đốiTượngBộĐọcLuồng,đọcLuồng);
static mp_obj_t ghiLuồng(mp_obj_t điểmCuối,mp_obj_t giáTrịNộiDung) {
    mp_buffer_info_t DữLiệu; mp_get_buffer_raise(giáTrịNộiDung,&DữLiệu,MP_BUFFER_READ);
    return mp_obj_new_int(đãKiểmTra(gọiThựcHiệnNgườiDùng(1,mp_obj_get_int(điểmCuối),(uintptr_t)DữLiệu.buf,DữLiệu.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(đốiTượngBộGhiLuồng,ghiLuồng);
static mp_obj_t chờTạmThời(mp_obj_t giáTrịThờiGian) {
    đãKiểmTra(gọiThựcHiệnNgườiDùng(17,mp_obj_get_int(giáTrịThờiGian),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(chờĐốiTượng,chờTạmThời);
static mp_obj_t loạiMục(mp_obj_t tên) {
    return mp_obj_new_int(đãKiểmTra(gọiThựcHiệnNgườiDùng(18,(uintptr_t)đốiSốĐườngDẫn(tên),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(đốiTượngLoạiMục,loạiMục);
static mp_obj_t tạoThưMục(mp_obj_t tên) {
    đãKiểmTra(gọiThựcHiệnNgườiDùng(18,(uintptr_t)đốiSốĐườngDẫn(tên),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(đốiTượngBộTạoThưMục,tạoThưMục);
static mp_obj_t gỡThưMục(mp_obj_t tên) {
    đãKiểmTra(gọiThựcHiệnNgườiDùng(18,(uintptr_t)đốiSốĐườngDẫn(tên),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(đốiTượngBộGỡThưMục,gỡThưMục);
static const mp_rom_map_elem_t cácTênMôĐun[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&đốiTượngBộMởLuồng) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&đốiTượngĐầuNốiLuồng) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&đốiTượngBộĐọcLuồng) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&đốiTượngBộGhiLuồng) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&chờĐốiTượng) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&đốiTượngLoạiMục) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&đốiTượngBộTạoThưMục) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&đốiTượngBộGỡThưMục) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&đốiTượngBộĐọcĐầuVàoChuẩn) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&đốiTượngBộĐọcTệp) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&đốiTượngBộGhiTệp) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&đốiTượngBộGỡTệp) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&đốiTượngHìnhChữNhật) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&đốiTượngCỡMànHình) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&đốiTượngChờMànHình) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&đốiTượngĐồngHồ) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&đốiTượngGọnMởUDP) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&đốiTượngGọnGửiUDP) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&đốiTượngGọnGửiĐếnUDP) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&đốiTượngGọnNhậnGọnUDP) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&đốiTượngGọnĐóngUDP) },
};
static MP_DEFINE_CONST_DICT(cácBiếnToànCụcMôĐun, cácTênMôĐun);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&cácBiếnToànCụcMôĐun };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
