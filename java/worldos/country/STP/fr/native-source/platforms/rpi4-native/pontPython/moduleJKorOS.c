// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "invoquer.h"
#include "ABIRéseau.h"
static intptr_t contrôlé(intptr_t résultat) { if (résultat < 0) mp_raise_OSError(-résultat); return résultat; }
static const char *argumentChemin(mp_obj_t valeur) {
    size_t nombreÉlémentsÉlémentListe; const char *chemin = mp_obj_str_get_data(valeur, &nombreÉlémentsÉlémentListe);
    if (!nombreÉlémentsÉlémentListe || nombreÉlémentsÉlémentListe > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsÉlémentListe; indiceOrdinal++) if (!chemin[indiceOrdinal]) mp_raise_OSError(MP_EINVAL);
    return chemin;
}
static mp_obj_t lireFichier(mp_obj_t nom) {
    intptr_t poignéeFichier = contrôlé(invoquerUtilisateur(3, (uintptr_t)argumentChemin(nom), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t retournerLocalNon;
    if (nlr_push(&retournerLocalNon) == 0) {
        size_t taille = contrôlé(invoquerUtilisateur(9, poignéeFichier, 0, 0, 0, 0, 0));
        vstr_t Données; vstr_init_len(&Données, taille);
        intptr_t résultat = invoquerUtilisateur(2, poignéeFichier, (uintptr_t)Données.buf, taille, 0, 0, 0);
        contrôlé(résultat); Données.len = résultat;
        mp_obj_t valeur = mp_obj_new_bytes_from_vstr(&Données);
        nlr_pop(); invoquerUtilisateur(4, poignéeFichier, 0, 0, 0, 0, 0); return valeur;
    }
    invoquerUtilisateur(4, poignéeFichier, 0, 0, 0, 0, 0); nlr_jump(retournerLocalNon.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(objetLecteurFichier, lireFichier);
static mp_obj_t lireEntréeStandard(mp_obj_t limiteCapacité) {
    mp_int_t taille=mp_obj_get_int(limiteCapacité);
    if(taille<0||taille>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t Données; vstr_init_len(&Données,taille);
    intptr_t nombreÉlémentsÉlémentListe=invoquerUtilisateur(2,0,(uintptr_t)Données.buf,taille,0,0,0);
    if(nombreÉlémentsÉlémentListe<0) { vstr_clear(&Données); contrôlé(nombreÉlémentsÉlémentListe); }
    Données.len=nombreÉlémentsÉlémentListe; return mp_obj_new_bytes_from_vstr(&Données);
}
static MP_DEFINE_CONST_FUN_OBJ_1(objetLecteurEntréeStandard, lireEntréeStandard);
static mp_obj_t écrireFichier(mp_obj_t nom, mp_obj_t valeurContenuValeur) {
    const char *chemin = argumentChemin(nom);
    mp_buffer_info_t Données; mp_get_buffer_raise(valeurContenuValeur, &Données, MP_BUFFER_READ);
    if (Données.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t poignéeFichier = contrôlé(invoquerUtilisateur(3, (uintptr_t)chemin, 577, 0, 0, 0, 0));
    intptr_t nombreÉlémentsEntréeÉlément = invoquerUtilisateur(1, poignéeFichier, (uintptr_t)Données.buf, Données.len, 0, 0, 0);
    invoquerUtilisateur(4, poignéeFichier, 0, 0, 0, 0, 0); return mp_obj_new_int(contrôlé(nombreÉlémentsEntréeÉlément));
}
static MP_DEFINE_CONST_FUN_OBJ_2(objetRédacteurFichier, écrireFichier);
static mp_obj_t supprimerFichier(mp_obj_t nom) { contrôlé(invoquerUtilisateur(11, (uintptr_t)argumentChemin(nom), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(objetSuppresseurFichier, supprimerFichier);
static mp_obj_t rectanglePeindre(size_t nombreÉlémentsÉlémentListe, const mp_obj_t *tableauArgument) {
    (void)nombreÉlémentsÉlémentListe; unsigned valeurPremier[5]; for (unsigned indiceOrdinal = 0; indiceOrdinal < 5; indiceOrdinal++) valeurPremier[indiceOrdinal] = mp_obj_get_int(tableauArgument[indiceOrdinal]);
    contrôlé(rectangleÉcran(valeurPremier[0], valeurPremier[1], valeurPremier[2], valeurPremier[3], valeurPremier[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(objetRectangle, 5, 5, rectanglePeindre);
static mp_obj_t lireTailleÉcran(void) {
    mp_obj_t taille[2] = {mp_obj_new_int(contrôlé(lireLargeurÉcran())), mp_obj_new_int(contrôlé(lireHauteurÉcran()))};
    return mp_obj_new_tuple(2, taille);
}
static MP_DEFINE_CONST_FUN_OBJ_0(objetTailleÉcran, lireTailleÉcran);
static mp_obj_t attendreEntréeÉcranPour(void) { return mp_obj_new_int(contrôlé(attendreToucheÉcranPour())); }
static MP_DEFINE_CONST_FUN_OBJ_0(objetAttendreÉcran, attendreEntréeÉcranPour);
static mp_obj_t valeurHorloge(void) { return mp_obj_new_int_from_uint(invoquerUtilisateur(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(objetHorloge, valeurHorloge);
static mp_obj_t ouvrirUDP(mp_obj_t numéroPort) {
    int positionDonnées = mp_obj_get_int(numéroPort); if (positionDonnées < 0 || positionDonnées > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t poignéeFichier = contrôlé(invoquerUtilisateur(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in valeurPremier = {0}; valeurPremier.sin_family = AF_INET; valeurPremier.sin_port = pk_htons(positionDonnées); valeurPremier.sin_addr.s_addr = 0;
    intptr_t résultat = invoquerUtilisateur(33, poignéeFichier, (uintptr_t)&valeurPremier, sizeof(valeurPremier), 0, 0, 0);
    if (résultat < 0) { invoquerUtilisateur(4, poignéeFichier, 0, 0, 0, 0, 0); contrôlé(résultat); }
    return mp_obj_new_int(poignéeFichier);
}
static MP_DEFINE_CONST_FUN_OBJ_1(objetValeurOuvrirUDP, ouvrirUDP);
static mp_obj_t envoyerUDP(mp_obj_t poignéeFichier, mp_obj_t numéroPort, mp_obj_t valeurContenuValeur) {
    int positionDonnées = mp_obj_get_int(numéroPort); if (positionDonnées < 1 || positionDonnées > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t Données; mp_get_buffer_raise(valeurContenuValeur, &Données, MP_BUFFER_READ);
    struct pk_sockaddr_in valeurPremier = {0}; valeurPremier.sin_family = AF_INET; valeurPremier.sin_port = pk_htons(positionDonnées); valeurPremier.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(contrôlé(invoquerUtilisateur(34, mp_obj_get_int(poignéeFichier), (uintptr_t)Données.buf, Données.len, 0, (uintptr_t)&valeurPremier, sizeof(valeurPremier))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(objetValeurEnvoyerUDP, envoyerUDP);
static uint32_t lireAdresseInternet(mp_obj_t valeur) {
    size_t longueur; const char *texte=mp_obj_str_get_data(valeur,&longueur);
    unsigned positionActuel=0; uint32_t adresse=0;
    for(unsigned valeurSousPartie=0;valeurSousPartie<4;valeurSousPartie++) {
        unsigned valeur=0,nombreÉlémentsChiffre=0;
        while(positionActuel<longueur&&texte[positionActuel]>='0'&&texte[positionActuel]<='9') {
            valeur=valeur*10+texte[positionActuel++]-'0'; if(++nombreÉlémentsChiffre>3||valeur>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!nombreÉlémentsChiffre)mp_raise_OSError(MP_EINVAL);
        adresse=adresse<<8|valeur;
        if(valeurSousPartie<3&&(positionActuel>=longueur||texte[positionActuel++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(positionActuel!=longueur)mp_raise_OSError(MP_EINVAL);
    return adresse;
}
static mp_obj_t envoyerVersUDP(size_t nombreÉlémentsEntréeÉlément, const mp_obj_t *tableauArgument) {
    (void)nombreÉlémentsEntréeÉlément; uint32_t adresse=lireAdresseInternet(tableauArgument[1]);
    int numéroPort=mp_obj_get_int(tableauArgument[2]);if(numéroPort<1||numéroPort>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t Données;mp_get_buffer_raise(tableauArgument[3],&Données,MP_BUFFER_READ);
    struct pk_sockaddr_in valeurCible={0};valeurCible.sin_family=AF_INET;valeurCible.sin_port=pk_htons(numéroPort);valeurCible.sin_addr.s_addr=pk_htonl(adresse);
    return mp_obj_new_int(contrôlé(invoquerUtilisateur(34,mp_obj_get_int(tableauArgument[0]),(uintptr_t)Données.buf,Données.len,0,(uintptr_t)&valeurCible,sizeof(valeurCible))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(objetValeurEnvoyerVersUDP,4,4,envoyerVersUDP);
static mp_obj_t opérationRéceptionUDP(mp_obj_t poignéeFichier) {
    unsigned char Données[512]; struct pk_sockaddr_in valeurPairRéseau; pk_socklen_t donnéesLongueur = sizeof(valeurPairRéseau);
    intptr_t taille = contrôlé(invoquerUtilisateur(35, mp_obj_get_int(poignéeFichier), (uintptr_t)Données, 512, 0, (uintptr_t)&valeurPairRéseau, (uintptr_t)&donnéesLongueur));
    mp_obj_t valeurs[2] = {mp_obj_new_bytes(Données, taille), MP_OBJ_NEW_SMALL_INT(pk_htons(valeurPairRéseau.sin_port))};
    return mp_obj_new_tuple(2, valeurs);
}
static MP_DEFINE_CONST_FUN_OBJ_1(objetValeurOpérationRéceptionUDP, opérationRéceptionUDP);
static mp_obj_t fermerUDP(mp_obj_t poignéeFichier) { contrôlé(invoquerUtilisateur(4, mp_obj_get_int(poignéeFichier), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(objetValeurFermerUDP, fermerUDP);
static mp_obj_t ouvrirFlux(void) {
    return mp_obj_new_int(contrôlé(invoquerUtilisateur(32,FamilleInternet,RéseauFlux,protocoleTransportFlux,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(objetOuvreurFlux,ouvrirFlux);
static mp_obj_t connecterFlux(mp_obj_t extrémité,mp_obj_t texteAdresse,mp_obj_t numéro) {
    int numéroPort=mp_obj_get_int(numéro); if(numéroPort<1||numéroPort>65535)mp_raise_OSError(MP_EINVAL);
    struct AdressePriseRéseauInternet adresse={0}; adresse.familleAdresse=FamilleInternet;
    adresse.numéroPort=courtRéseau(numéroPort); adresse.AdresseInternet.valeurAdresse=entierRéseau(lireAdresseInternet(texteAdresse));
    contrôlé(invoquerUtilisateur(37,mp_obj_get_int(extrémité),(uintptr_t)&adresse,sizeof(adresse),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(objetConnecteurFlux,connecterFlux);
static mp_obj_t lireFlux(mp_obj_t extrémité,mp_obj_t limiteCapacité) {
    int longueur=mp_obj_get_int(limiteCapacité); if(longueur<1||longueur>512)mp_raise_OSError(MP_EINVAL);
    unsigned char Données[512];
    intptr_t nombreÉlémentsÉlémentListe=contrôlé(invoquerUtilisateur(2,mp_obj_get_int(extrémité),(uintptr_t)Données,longueur,0,0,0));
    return mp_obj_new_bytes(Données,nombreÉlémentsÉlémentListe);
}
static MP_DEFINE_CONST_FUN_OBJ_2(objetLecteurFlux,lireFlux);
static mp_obj_t écrireFlux(mp_obj_t extrémité,mp_obj_t valeurContenuValeur) {
    mp_buffer_info_t Données; mp_get_buffer_raise(valeurContenuValeur,&Données,MP_BUFFER_READ);
    return mp_obj_new_int(contrôlé(invoquerUtilisateur(1,mp_obj_get_int(extrémité),(uintptr_t)Données.buf,Données.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(objetRédacteurFlux,écrireFlux);
static mp_obj_t attendreTemporairement(mp_obj_t valeurTemps) {
    contrôlé(invoquerUtilisateur(17,mp_obj_get_int(valeurTemps),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(attendreObjet,attendreTemporairement);
static mp_obj_t genreEntréeÉlément(mp_obj_t nom) {
    return mp_obj_new_int(contrôlé(invoquerUtilisateur(18,(uintptr_t)argumentChemin(nom),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(objetGenreEntréeÉlément,genreEntréeÉlément);
static mp_obj_t créerRépertoire(mp_obj_t nom) {
    contrôlé(invoquerUtilisateur(18,(uintptr_t)argumentChemin(nom),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(objetCréateurRépertoire,créerRépertoire);
static mp_obj_t supprimerRépertoire(mp_obj_t nom) {
    contrôlé(invoquerUtilisateur(18,(uintptr_t)argumentChemin(nom),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(objetSuppresseurRépertoire,supprimerRépertoire);
static const mp_rom_map_elem_t nomsModule[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&objetOuvreurFlux) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&objetConnecteurFlux) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&objetLecteurFlux) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&objetRédacteurFlux) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&attendreObjet) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&objetGenreEntréeÉlément) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&objetCréateurRépertoire) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&objetSuppresseurRépertoire) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&objetLecteurEntréeStandard) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&objetLecteurFichier) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&objetRédacteurFichier) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&objetSuppresseurFichier) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&objetRectangle) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&objetTailleÉcran) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&objetAttendreÉcran) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&objetHorloge) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&objetValeurOuvrirUDP) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&objetValeurEnvoyerUDP) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&objetValeurEnvoyerVersUDP) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&objetValeurOpérationRéceptionUDP) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&objetValeurFermerUDP) },
};
static MP_DEFINE_CONST_DICT(variablesGlobalesModule, nomsModule);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&variablesGlobalesModule };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
