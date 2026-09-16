/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _include_système_socket
#define _include_système_socket

#include <définitions_de_base.h>
#include <système/types_de_données.h>

typedef unsigned short type_de_famille_adresse;

struct adresse_du_point_de_communication {
    type_de_famille_adresse famille_adresse_du_point;
    char données_adresse[14];
};

#define famille_adresse_non_spécifiée 0
#define code_de_famille_adresse_interréseau 2
#define famille_de_protocoles_interréseau code_de_famille_adresse_interréseau

#define point_de_flux_de_données 1
#define point_de_datagrammes 2

#define arrêter_réception 0
#define arrêter_émission 1
#define arrêter_les_deux_sens 2

#ifdef __cplusplus
extern "C" {
#endif
int créer_un_point_de_communication(int domain, int type, int protocol);
int associer_une_adresse_locale(int descripteur_de_fichier, const struct adresse_du_point_de_communication *address, type_de_longueur_adresse address_len);
int connecter_au_correspondant(int descripteur_de_fichier, const struct adresse_du_point_de_communication *address, type_de_longueur_adresse address_len);
int préparer_accueil_des_connexions(int descripteur_de_fichier, int backlog);
int accepter_une_connexion(int descripteur_de_fichier, struct adresse_du_point_de_communication *address, type_de_longueur_adresse *address_len);
int obtenir_adresse_locale(int descripteur_de_fichier, struct adresse_du_point_de_communication *address, type_de_longueur_adresse *address_len);
int obtenir_adresse_du_correspondant(int descripteur_de_fichier, struct adresse_du_point_de_communication *address, type_de_longueur_adresse *address_len);
ssize_t envoyer(int descripteur_de_fichier, const void *tampon_de_transfert_2, size_t longueur, int flags);
ssize_t recevoir(int descripteur_de_fichier, void *tampon_de_transfert_2, size_t longueur, int flags);
ssize_t envoyer_vers_une_adresse(int descripteur_de_fichier, const void *message, size_t longueur, int flags,
               const struct adresse_du_point_de_communication *dest_addr, type_de_longueur_adresse dest_len);
ssize_t recevoir_avec_adresse_source(int descripteur_de_fichier, void *tampon_de_transfert_2, size_t longueur, int flags,
                 struct adresse_du_point_de_communication *address, type_de_longueur_adresse *address_len);
int fermer_un_sens_de_communication(int descripteur_de_fichier, int how);
int régler_une_option_du_point(int descripteur_de_fichier, int level, int option_name,
               const void *option_value, type_de_longueur_adresse option_len);
#ifdef __cplusplus
}
#endif

#endif
