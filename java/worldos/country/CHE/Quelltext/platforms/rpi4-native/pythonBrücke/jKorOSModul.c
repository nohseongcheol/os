// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "aufrufen.h"
#include "NetzwerkABI.h"
static intptr_t geprüft(intptr_t ergebnis) { if (ergebnis < 0) mp_raise_OSError(-ergebnis); return ergebnis; }
static const char *pfadArgument(mp_obj_t Wert) {
    size_t elementeintragAnzahl; const char *pfad = mp_obj_str_get_data(Wert, &elementeintragAnzahl);
    if (!elementeintragAnzahl || elementeintragAnzahl > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t ordnungszahlIndex = 0; ordnungszahlIndex < elementeintragAnzahl; ordnungszahlIndex++) if (!pfad[ordnungszahlIndex]) mp_raise_OSError(MP_EINVAL);
    return pfad;
}
static mp_obj_t dateiLesen(mp_obj_t Name) {
    intptr_t dateiKennwert = geprüft(benutzerAufrufen(3, (uintptr_t)pfadArgument(Name), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t nichtLokalZurückkehren;
    if (nlr_push(&nichtLokalZurückkehren) == 0) {
        size_t größe = geprüft(benutzerAufrufen(9, dateiKennwert, 0, 0, 0, 0, 0));
        vstr_t Daten; vstr_init_len(&Daten, größe);
        intptr_t ergebnis = benutzerAufrufen(2, dateiKennwert, (uintptr_t)Daten.buf, größe, 0, 0, 0);
        geprüft(ergebnis); Daten.len = ergebnis;
        mp_obj_t Wert = mp_obj_new_bytes_from_vstr(&Daten);
        nlr_pop(); benutzerAufrufen(4, dateiKennwert, 0, 0, 0, 0, 0); return Wert;
    }
    benutzerAufrufen(4, dateiKennwert, 0, 0, 0, 0, 0); nlr_jump(nichtLokalZurückkehren.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(dateiLeserObjekt, dateiLesen);
static mp_obj_t standardEingabeLesen(mp_obj_t kapazitätGrenzwert) {
    mp_int_t größe=mp_obj_get_int(kapazitätGrenzwert);
    if(größe<0||größe>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t Daten; vstr_init_len(&Daten,größe);
    intptr_t elementeintragAnzahl=benutzerAufrufen(2,0,(uintptr_t)Daten.buf,größe,0,0,0);
    if(elementeintragAnzahl<0) { vstr_clear(&Daten); geprüft(elementeintragAnzahl); }
    Daten.len=elementeintragAnzahl; return mp_obj_new_bytes_from_vstr(&Daten);
}
static MP_DEFINE_CONST_FUN_OBJ_1(standardEingabeLeserObjekt, standardEingabeLesen);
static mp_obj_t dateiSchreiben(mp_obj_t Name, mp_obj_t inhaltswertWert) {
    const char *pfad = pfadArgument(Name);
    mp_buffer_info_t Daten; mp_get_buffer_raise(inhaltswertWert, &Daten, MP_BUFFER_READ);
    if (Daten.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t dateiKennwert = geprüft(benutzerAufrufen(3, (uintptr_t)pfad, 577, 0, 0, 0, 0));
    intptr_t eintragAnzahl = benutzerAufrufen(1, dateiKennwert, (uintptr_t)Daten.buf, Daten.len, 0, 0, 0);
    benutzerAufrufen(4, dateiKennwert, 0, 0, 0, 0, 0); return mp_obj_new_int(geprüft(eintragAnzahl));
}
static MP_DEFINE_CONST_FUN_OBJ_2(dateiSchreiberObjekt, dateiSchreiben);
static mp_obj_t dateiEntfernen(mp_obj_t Name) { geprüft(benutzerAufrufen(11, (uintptr_t)pfadArgument(Name), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(dateiEntfernerObjekt, dateiEntfernen);
static mp_obj_t malenRechteck(size_t elementeintragAnzahl, const mp_obj_t *argumentDatenfeld) {
    (void)elementeintragAnzahl; unsigned ersterWert[5]; for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < 5; ordnungszahlIndex++) ersterWert[ordnungszahlIndex] = mp_obj_get_int(argumentDatenfeld[ordnungszahlIndex]);
    geprüft(bildschirmRechteck(ersterWert[0], ersterWert[1], ersterWert[2], ersterWert[3], ersterWert[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(rechteckObjekt, 5, 5, malenRechteck);
static mp_obj_t bildschirmGrößeLesen(void) {
    mp_obj_t größe[2] = {mp_obj_new_int(geprüft(bildschirmBreiteLesen())), mp_obj_new_int(geprüft(bildschirmHöheLesen()))};
    return mp_obj_new_tuple(2, größe);
}
static MP_DEFINE_CONST_FUN_OBJ_0(bildschirmGrößeObjekt, bildschirmGrößeLesen);
static mp_obj_t fürBildschirmEingabeWarten(void) { return mp_obj_new_int(geprüft(fürBildschirmTasteWarten())); }
static MP_DEFINE_CONST_FUN_OBJ_0(bildschirmWartenObjekt, fürBildschirmEingabeWarten);
static mp_obj_t uhrWert(void) { return mp_obj_new_int_from_uint(benutzerAufrufen(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(uhrObjekt, uhrWert);
static mp_obj_t uDPÖffnen(mp_obj_t portNummer) {
    int datenPosition = mp_obj_get_int(portNummer); if (datenPosition < 0 || datenPosition > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t dateiKennwert = geprüft(benutzerAufrufen(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in ersterWert = {0}; ersterWert.sin_family = AF_INET; ersterWert.sin_port = pk_htons(datenPosition); ersterWert.sin_addr.s_addr = 0;
    intptr_t ergebnis = benutzerAufrufen(33, dateiKennwert, (uintptr_t)&ersterWert, sizeof(ersterWert), 0, 0, 0);
    if (ergebnis < 0) { benutzerAufrufen(4, dateiKennwert, 0, 0, 0, 0, 0); geprüft(ergebnis); }
    return mp_obj_new_int(dateiKennwert);
}
static MP_DEFINE_CONST_FUN_OBJ_1(uDPÖffnenObjektwert, uDPÖffnen);
static mp_obj_t uDPSenden(mp_obj_t dateiKennwert, mp_obj_t portNummer, mp_obj_t inhaltswertWert) {
    int datenPosition = mp_obj_get_int(portNummer); if (datenPosition < 1 || datenPosition > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t Daten; mp_get_buffer_raise(inhaltswertWert, &Daten, MP_BUFFER_READ);
    struct pk_sockaddr_in ersterWert = {0}; ersterWert.sin_family = AF_INET; ersterWert.sin_port = pk_htons(datenPosition); ersterWert.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(geprüft(benutzerAufrufen(34, mp_obj_get_int(dateiKennwert), (uintptr_t)Daten.buf, Daten.len, 0, (uintptr_t)&ersterWert, sizeof(ersterWert))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(uDPSendenObjektwert, uDPSenden);
static uint32_t internetAdresseLesen(mp_obj_t Wert) {
    size_t Länge; const char *Text=mp_obj_str_get_data(Wert,&Länge);
    unsigned aktuellPosition=0; uint32_t adresse=0;
    for(unsigned unterteilWert=0;unterteilWert<4;unterteilWert++) {
        unsigned Wert=0,zifferAnzahl=0;
        while(aktuellPosition<Länge&&Text[aktuellPosition]>='0'&&Text[aktuellPosition]<='9') {
            Wert=Wert*10+Text[aktuellPosition++]-'0'; if(++zifferAnzahl>3||Wert>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!zifferAnzahl)mp_raise_OSError(MP_EINVAL);
        adresse=adresse<<8|Wert;
        if(unterteilWert<3&&(aktuellPosition>=Länge||Text[aktuellPosition++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(aktuellPosition!=Länge)mp_raise_OSError(MP_EINVAL);
    return adresse;
}
static mp_obj_t uDPZielSenden(size_t eintragAnzahl, const mp_obj_t *argumentDatenfeld) {
    (void)eintragAnzahl; uint32_t adresse=internetAdresseLesen(argumentDatenfeld[1]);
    int portNummer=mp_obj_get_int(argumentDatenfeld[2]);if(portNummer<1||portNummer>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t Daten;mp_get_buffer_raise(argumentDatenfeld[3],&Daten,MP_BUFFER_READ);
    struct pk_sockaddr_in zielobjektWert={0};zielobjektWert.sin_family=AF_INET;zielobjektWert.sin_port=pk_htons(portNummer);zielobjektWert.sin_addr.s_addr=pk_htonl(adresse);
    return mp_obj_new_int(geprüft(benutzerAufrufen(34,mp_obj_get_int(argumentDatenfeld[0]),(uintptr_t)Daten.buf,Daten.len,0,(uintptr_t)&zielobjektWert,sizeof(zielobjektWert))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(uDPZielSendenObjektwert,4,4,uDPZielSenden);
static mp_obj_t uDPEmpfangsvorgang(mp_obj_t dateiKennwert) {
    unsigned char Daten[512]; struct pk_sockaddr_in gegenstelleWert; pk_socklen_t längeDaten = sizeof(gegenstelleWert);
    intptr_t größe = geprüft(benutzerAufrufen(35, mp_obj_get_int(dateiKennwert), (uintptr_t)Daten, 512, 0, (uintptr_t)&gegenstelleWert, (uintptr_t)&längeDaten));
    mp_obj_t werte[2] = {mp_obj_new_bytes(Daten, größe), MP_OBJ_NEW_SMALL_INT(pk_htons(gegenstelleWert.sin_port))};
    return mp_obj_new_tuple(2, werte);
}
static MP_DEFINE_CONST_FUN_OBJ_1(uDPEmpfangsvorgangObjektwert, uDPEmpfangsvorgang);
static mp_obj_t uDPSchließen(mp_obj_t dateiKennwert) { geprüft(benutzerAufrufen(4, mp_obj_get_int(dateiKennwert), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(uDPSchließenObjektwert, uDPSchließen);
static mp_obj_t datenstromÖffnen(void) {
    return mp_obj_new_int(geprüft(benutzerAufrufen(32,InternetFamilie,DatenstromNetzwerk,datenstromBeförderungProtokoll,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(datenstromÖffnerObjekt,datenstromÖffnen);
static mp_obj_t datenstromVerbinden(mp_obj_t endpunkt,mp_obj_t adresseText,mp_obj_t Nummer) {
    int portNummer=mp_obj_get_int(Nummer); if(portNummer<1||portNummer>65535)mp_raise_OSError(MP_EINVAL);
    struct InternetNetzbuchseAdresse adresse={0}; adresse.adresseFamilie=InternetFamilie;
    adresse.portNummer=netzwerkKurz(portNummer); adresse.InternetAdresse.adresseWert=netzwerkGanzzahl(internetAdresseLesen(adresseText));
    geprüft(benutzerAufrufen(37,mp_obj_get_int(endpunkt),(uintptr_t)&adresse,sizeof(adresse),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(datenstromVerbinderObjekt,datenstromVerbinden);
static mp_obj_t datenstromLesen(mp_obj_t endpunkt,mp_obj_t kapazitätGrenzwert) {
    int Länge=mp_obj_get_int(kapazitätGrenzwert); if(Länge<1||Länge>512)mp_raise_OSError(MP_EINVAL);
    unsigned char Daten[512];
    intptr_t elementeintragAnzahl=geprüft(benutzerAufrufen(2,mp_obj_get_int(endpunkt),(uintptr_t)Daten,Länge,0,0,0));
    return mp_obj_new_bytes(Daten,elementeintragAnzahl);
}
static MP_DEFINE_CONST_FUN_OBJ_2(datenstromLeserObjekt,datenstromLesen);
static mp_obj_t datenstromSchreiben(mp_obj_t endpunkt,mp_obj_t inhaltswertWert) {
    mp_buffer_info_t Daten; mp_get_buffer_raise(inhaltswertWert,&Daten,MP_BUFFER_READ);
    return mp_obj_new_int(geprüft(benutzerAufrufen(1,mp_obj_get_int(endpunkt),(uintptr_t)Daten.buf,Daten.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(datenstromSchreiberObjekt,datenstromSchreiben);
static mp_obj_t zeitweiligWarten(mp_obj_t zeitWert) {
    geprüft(benutzerAufrufen(17,mp_obj_get_int(zeitWert),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(objektWarten,zeitweiligWarten);
static mp_obj_t eintragArt(mp_obj_t Name) {
    return mp_obj_new_int(geprüft(benutzerAufrufen(18,(uintptr_t)pfadArgument(Name),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(eintragArtObjekt,eintragArt);
static mp_obj_t verzeichnisErstellen(mp_obj_t Name) {
    geprüft(benutzerAufrufen(18,(uintptr_t)pfadArgument(Name),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(verzeichnisErstellerObjekt,verzeichnisErstellen);
static mp_obj_t verzeichnisEntfernen(mp_obj_t Name) {
    geprüft(benutzerAufrufen(18,(uintptr_t)pfadArgument(Name),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(verzeichnisEntfernerObjekt,verzeichnisEntfernen);
static const mp_rom_map_elem_t modulNamen[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&datenstromÖffnerObjekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&datenstromVerbinderObjekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&datenstromLeserObjekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&datenstromSchreiberObjekt) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&objektWarten) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&eintragArtObjekt) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&verzeichnisErstellerObjekt) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&verzeichnisEntfernerObjekt) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&standardEingabeLeserObjekt) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&dateiLeserObjekt) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&dateiSchreiberObjekt) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&dateiEntfernerObjekt) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&rechteckObjekt) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&bildschirmGrößeObjekt) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&bildschirmWartenObjekt) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&uhrObjekt) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&uDPÖffnenObjektwert) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&uDPSendenObjektwert) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&uDPZielSendenObjektwert) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&uDPEmpfangsvorgangObjektwert) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&uDPSchließenObjektwert) },
};
static MP_DEFINE_CONST_DICT(modulGlobalvariablen, modulNamen);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&modulGlobalvariablen };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
