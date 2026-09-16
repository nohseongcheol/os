/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <conversion_des_adresses/ordre_des_octets.h>
#include <système/syscall.h>
#include <système/socket.h>

enum { SYS_socketcall = 102 };
enum {
    SC_créer_un_point_de_communication = 1, SC_associer_une_adresse_locale = 2, SC_connecter_au_correspondant = 3, SC_préparer_accueil_des_connexions = 4,
    SC_accepter_une_connexion = 5, SC_obtenir_adresse_locale = 6, SC_obtenir_adresse_du_correspondant = 7,
    SC_envoyer = 9, SC_recevoir = 10, SC_envoyer_vers_une_adresse = 11, SC_recevoir_avec_adresse_source = 12,
    SC_fermer_un_sens_de_communication = 13, SC_régler_une_option_du_point = 14
};

static long socket_call(long call, unsigned long *arguments)
{
    return __syscall_result(
        __syscall6(SYS_socketcall, call, (long)arguments, 0, 0, 0, 0));
}

uint16_t convertir_16_bits_vers_ordre_réseau(uint16_t valeur) { return (uint16_t)((valeur << 8) | (valeur >> 8)); }
uint16_t convertir_16_bits_vers_ordre_machine(uint16_t valeur) { return convertir_16_bits_vers_ordre_réseau(valeur); }
uint32_t convertir_32_bits_vers_ordre_réseau(uint32_t valeur)
{
    return ((valeur & 0x000000ffU) << 24) | ((valeur & 0x0000ff00U) << 8) |
           ((valeur & 0x00ff0000U) >> 8) | ((valeur & 0xff000000U) >> 24);
}
uint32_t convertir_32_bits_vers_ordre_machine(uint32_t valeur) { return convertir_32_bits_vers_ordre_réseau(valeur); }

int créer_un_point_de_communication(int domain, int type, int protocol)
{
    unsigned long a[3] = {(unsigned long)domain, (unsigned long)type, (unsigned long)protocol};
    return (int)socket_call(SC_créer_un_point_de_communication, a);
}

int associer_une_adresse_locale(int descripteur_de_fichier, const struct adresse_du_point_de_communication *address, type_de_longueur_adresse longueur)
{
    unsigned long a[3] = {(unsigned long)descripteur_de_fichier, (unsigned long)address, longueur};
    return (int)socket_call(SC_associer_une_adresse_locale, a);
}

int connecter_au_correspondant(int descripteur_de_fichier, const struct adresse_du_point_de_communication *address, type_de_longueur_adresse longueur)
{
    unsigned long a[3] = {(unsigned long)descripteur_de_fichier, (unsigned long)address, longueur};
    return (int)socket_call(SC_connecter_au_correspondant, a);
}

int préparer_accueil_des_connexions(int descripteur_de_fichier, int backlog)
{
    unsigned long a[2] = {(unsigned long)descripteur_de_fichier, (unsigned long)backlog};
    return (int)socket_call(SC_préparer_accueil_des_connexions, a);
}

int accepter_une_connexion(int descripteur_de_fichier, struct adresse_du_point_de_communication *address, type_de_longueur_adresse *longueur)
{
    unsigned long a[3] = {(unsigned long)descripteur_de_fichier, (unsigned long)address, (unsigned long)longueur};
    return (int)socket_call(SC_accepter_une_connexion, a);
}

int obtenir_adresse_locale(int descripteur_de_fichier, struct adresse_du_point_de_communication *address, type_de_longueur_adresse *longueur)
{
    unsigned long a[3] = {(unsigned long)descripteur_de_fichier, (unsigned long)address, (unsigned long)longueur};
    return (int)socket_call(SC_obtenir_adresse_locale, a);
}

int obtenir_adresse_du_correspondant(int descripteur_de_fichier, struct adresse_du_point_de_communication *address, type_de_longueur_adresse *longueur)
{
    unsigned long a[3] = {(unsigned long)descripteur_de_fichier, (unsigned long)address, (unsigned long)longueur};
    return (int)socket_call(SC_obtenir_adresse_du_correspondant, a);
}

ssize_t envoyer(int descripteur_de_fichier, const void *tampon_de_transfert_2, size_t longueur, int flags)
{
    unsigned long a[4] = {(unsigned long)descripteur_de_fichier, (unsigned long)tampon_de_transfert_2, longueur, (unsigned long)flags};
    return (ssize_t)socket_call(SC_envoyer, a);
}

ssize_t recevoir(int descripteur_de_fichier, void *tampon_de_transfert_2, size_t longueur, int flags)
{
    unsigned long a[4] = {(unsigned long)descripteur_de_fichier, (unsigned long)tampon_de_transfert_2, longueur, (unsigned long)flags};
    return (ssize_t)socket_call(SC_recevoir, a);
}

ssize_t envoyer_vers_une_adresse(int descripteur_de_fichier, const void *tampon_de_transfert_2, size_t longueur, int flags,
               const struct adresse_du_point_de_communication *address, type_de_longueur_adresse address_length)
{
    unsigned long a[6] = {(unsigned long)descripteur_de_fichier, (unsigned long)tampon_de_transfert_2, longueur,
                          (unsigned long)flags, (unsigned long)address, address_length};
    return (ssize_t)socket_call(SC_envoyer_vers_une_adresse, a);
}

ssize_t recevoir_avec_adresse_source(int descripteur_de_fichier, void *tampon_de_transfert_2, size_t longueur, int flags,
                 struct adresse_du_point_de_communication *address, type_de_longueur_adresse *address_length)
{
    unsigned long a[6] = {(unsigned long)descripteur_de_fichier, (unsigned long)tampon_de_transfert_2, longueur,
                          (unsigned long)flags, (unsigned long)address,
                          (unsigned long)address_length};
    return (ssize_t)socket_call(SC_recevoir_avec_adresse_source, a);
}

int fermer_un_sens_de_communication(int descripteur_de_fichier, int how)
{
    unsigned long a[2] = {(unsigned long)descripteur_de_fichier, (unsigned long)how};
    return (int)socket_call(SC_fermer_un_sens_de_communication, a);
}

int régler_une_option_du_point(int descripteur_de_fichier, int level, int option_name,
               const void *option_value, type_de_longueur_adresse option_len)
{
    unsigned long a[5] = {(unsigned long)descripteur_de_fichier, (unsigned long)level,
                          (unsigned long)option_name, (unsigned long)option_value,
                          option_len};
    return (int)socket_call(SC_régler_une_option_du_point, a);
}
