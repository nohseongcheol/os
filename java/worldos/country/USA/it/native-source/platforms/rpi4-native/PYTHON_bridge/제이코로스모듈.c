// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "rete_ABI.h"
static intptr_t 결과검사(intptr_t risultato) { if (risultato < 0) mp_raise_OSError(-risultato); return risultato; }
static const char *percorso_argomento(mp_obj_t VALORE) {
    size_t articolo_CONTA_NUMERI; const char *percorso = mp_obj_str_get_data(VALORE, &articolo_CONTA_NUMERI);
    if (!articolo_CONTA_NUMERI || articolo_CONTA_NUMERI > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < articolo_CONTA_NUMERI; 순번++) if (!percorso[순번]) mp_raise_OSError(MP_EINVAL);
    return percorso;
}
static mp_obj_t 파일읽기(mp_obj_t Nome) {
    intptr_t handle_di_file = 결과검사(사용자호출(3, (uintptr_t)percorso_argomento(Nome), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Dimensione = 결과검사(사용자호출(9, handle_di_file, 0, 0, 0, 0, 0));
        vstr_t dati; vstr_init_len(&dati, Dimensione);
        intptr_t risultato = 사용자호출(2, handle_di_file, (uintptr_t)dati.buf, Dimensione, 0, 0, 0);
        결과검사(risultato); dati.len = risultato;
        mp_obj_t VALORE = mp_obj_new_bytes_from_vstr(&dati);
        nlr_pop(); 사용자호출(4, handle_di_file, 0, 0, 0, 0, 0); return VALORE;
    }
    사용자호출(4, handle_di_file, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(File_Lettore_oggetto, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Dimensione=mp_obj_get_int(한도);
    if(Dimensione<0||Dimensione>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t dati; vstr_init_len(&dati,Dimensione);
    intptr_t articolo_CONTA_NUMERI=사용자호출(2,0,(uintptr_t)dati.buf,Dimensione,0,0,0);
    if(articolo_CONTA_NUMERI<0) { vstr_clear(&dati); 결과검사(articolo_CONTA_NUMERI); }
    dati.len=articolo_CONTA_NUMERI; return mp_obj_new_bytes_from_vstr(&dati);
}
static MP_DEFINE_CONST_FUN_OBJ_1(STDIN_Lettore_oggetto, 표준입력읽기);
static mp_obj_t scrivere_File(mp_obj_t Nome, mp_obj_t Contenuto_VALORE) {
    const char *percorso = percorso_argomento(Nome);
    mp_buffer_info_t dati; mp_get_buffer_raise(Contenuto_VALORE, &dati, MP_BUFFER_READ);
    if (dati.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t handle_di_file = 결과검사(사용자호출(3, (uintptr_t)percorso, 577, 0, 0, 0, 0));
    intptr_t voce_CONTA_NUMERI = 사용자호출(1, handle_di_file, (uintptr_t)dati.buf, dati.len, 0, 0, 0);
    사용자호출(4, handle_di_file, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(voce_CONTA_NUMERI));
}
static MP_DEFINE_CONST_FUN_OBJ_2(File_Writer_oggetto, scrivere_File);
static mp_obj_t rimuovere_File(mp_obj_t Nome) { 결과검사(사용자호출(11, (uintptr_t)percorso_argomento(Nome), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, rimuovere_File);
static mp_obj_t Paint_rettangolo(size_t articolo_CONTA_NUMERI, const mp_obj_t *argomento_array) {
    (void)articolo_CONTA_NUMERI; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argomento_array[순번]);
    결과검사(schermata_rettangolo(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(rettangolo_oggetto, 5, 5, Paint_rettangolo);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Dimensione[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Dimensione);
}
static MP_DEFINE_CONST_FUN_OBJ_0(schermata_ridimensionare_oggetto, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(schermata_aspetta_oggetto, 화면입력기다리기);
static mp_obj_t clock_VALORE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(clock_oggetto, clock_VALORE);
static mp_obj_t UDP_aperto(mp_obj_t numero_di_porta) {
    int dati_funzione = mp_obj_get_int(numero_di_porta); if (dati_funzione < 0 || dati_funzione > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t handle_di_file = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(dati_funzione); 첫째값.sin_addr.s_addr = 0;
    intptr_t risultato = 사용자호출(33, handle_di_file, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (risultato < 0) { 사용자호출(4, handle_di_file, 0, 0, 0, 0, 0); 결과검사(risultato); }
    return mp_obj_new_int(handle_di_file);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_aperto_OBJ, UDP_aperto);
static mp_obj_t UDP_inviare(mp_obj_t handle_di_file, mp_obj_t numero_di_porta, mp_obj_t Contenuto_VALORE) {
    int dati_funzione = mp_obj_get_int(numero_di_porta); if (dati_funzione < 1 || dati_funzione > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t dati; mp_get_buffer_raise(Contenuto_VALORE, &dati, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(dati_funzione); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(handle_di_file), (uintptr_t)dati.buf, dati.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_inviare_OBJ, UDP_inviare);
static uint32_t 인터넷주소읽기(mp_obj_t VALORE) {
    size_t durata_VALORE; const char *testo=mp_obj_str_get_data(VALORE,&durata_VALORE);
    unsigned Regolari_funzione=0; uint32_t e_mail=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALORE=0,cifra_CONTA_NUMERI=0;
        while(Regolari_funzione<durata_VALORE&&testo[Regolari_funzione]>='0'&&testo[Regolari_funzione]<='9') {
            VALORE=VALORE*10+testo[Regolari_funzione++]-'0'; if(++cifra_CONTA_NUMERI>3||VALORE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!cifra_CONTA_NUMERI)mp_raise_OSError(MP_EINVAL);
        e_mail=e_mail<<8|VALORE;
        if(부분<3&&(Regolari_funzione>=durata_VALORE||testo[Regolari_funzione++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(Regolari_funzione!=durata_VALORE)mp_raise_OSError(MP_EINVAL);
    return e_mail;
}
static mp_obj_t 전문주소전송(size_t voce_CONTA_NUMERI, const mp_obj_t *argomento_array) {
    (void)voce_CONTA_NUMERI; uint32_t e_mail=인터넷주소읽기(argomento_array[1]);
    int numero_di_porta=mp_obj_get_int(argomento_array[2]);if(numero_di_porta<1||numero_di_porta>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t dati;mp_get_buffer_raise(argomento_array[3],&dati,MP_BUFFER_READ);
    struct pk_sockaddr_in target={0};target.sin_family=AF_INET;target.sin_port=pk_htons(numero_di_porta);target.sin_addr.s_addr=pk_htonl(e_mail);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argomento_array[0]),(uintptr_t)dati.buf,dati.len,0,(uintptr_t)&target,sizeof(target))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t handle_di_file) {
    unsigned char dati[512]; struct pk_sockaddr_in peer_VALORE; pk_socklen_t durata_dati = sizeof(peer_VALORE);
    intptr_t Dimensione = 결과검사(사용자호출(35, mp_obj_get_int(handle_di_file), (uintptr_t)dati, 512, 0, (uintptr_t)&peer_VALORE, (uintptr_t)&durata_dati));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(dati, Dimensione), MP_OBJ_NEW_SMALL_INT(pk_htons(peer_VALORE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Chiudi(mp_obj_t handle_di_file) { 결과검사(사용자호출(4, mp_obj_get_int(handle_di_file), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Chiudi_OBJ, UDP_Chiudi);
static mp_obj_t aperto_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,cloud_serie,Stream_rete,Stream_protocollo_di_trasporto,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,aperto_Stream);
static mp_obj_t CONNETTI_Stream(mp_obj_t endpoint,mp_obj_t e_mail_SMS,mp_obj_t INDICE) {
    int numero_di_porta=mp_obj_get_int(INDICE); if(numero_di_porta<1||numero_di_porta>65535)mp_raise_OSError(MP_EINVAL);
    struct cloud_socket_e_mail e_mail={0}; e_mail.e_mail_serie=cloud_serie;
    e_mail.numero_di_porta=망차례짧은수(numero_di_porta); e_mail.indirizzo_Internet.e_mail_VALORE=rete_intero(인터넷주소읽기(e_mail_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(endpoint),(uintptr_t)&e_mail,sizeof(e_mail),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_Connettore_oggetto,CONNETTI_Stream);
static mp_obj_t 흐름읽기(mp_obj_t endpoint,mp_obj_t 한도) {
    int durata_VALORE=mp_obj_get_int(한도); if(durata_VALORE<1||durata_VALORE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char dati[512];
    intptr_t articolo_CONTA_NUMERI=결과검사(사용자호출(2,mp_obj_get_int(endpoint),(uintptr_t)dati,durata_VALORE,0,0,0));
    return mp_obj_new_bytes(dati,articolo_CONTA_NUMERI);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Lettore_oggetto,흐름읽기);
static mp_obj_t scrivere_Stream(mp_obj_t endpoint,mp_obj_t Contenuto_VALORE) {
    mp_buffer_info_t dati; mp_get_buffer_raise(Contenuto_VALORE,&dati,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(endpoint),(uintptr_t)dati.buf,dati.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_Writer_oggetto,scrivere_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t valore) {
    결과검사(사용자호출(17,mp_obj_get_int(valore),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(aspetta_oggetto,잠시기다리기);
static mp_obj_t voce_Kind(mp_obj_t Nome) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)percorso_argomento(Nome),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(voce_Kind_oggetto,voce_Kind);
static mp_obj_t Crea_elenco(mp_obj_t Nome) {
    결과검사(사용자호출(18,(uintptr_t)percorso_argomento(Nome),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(elenco_autore_oggetto,Crea_elenco);
static mp_obj_t rimuovere_elenco(mp_obj_t Nome) {
    결과검사(사용자호출(18,(uintptr_t)percorso_argomento(Nome),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,rimuovere_elenco);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_Connettore_oggetto) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_Lettore_oggetto) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_Writer_oggetto) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&aspetta_oggetto) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&voce_Kind_oggetto) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&elenco_autore_oggetto) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&STDIN_Lettore_oggetto) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&File_Lettore_oggetto) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&File_Writer_oggetto) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&rettangolo_oggetto) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&schermata_ridimensionare_oggetto) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&schermata_aspetta_oggetto) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&clock_oggetto) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_aperto_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_inviare_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Chiudi_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
