#ifndef _include_interréseau_adresse
#define _include_interréseau_adresse

#include <types_entiers.h>
#include <système/socket.h>

typedef uint32_t type_de_valeur_adresse_interréseau;
typedef uint16_t type_de_numéro_de_port_de_communication;

struct adresse_interréseau {
    type_de_valeur_adresse_interréseau valeur_adresse;
};

struct adresse_du_point_de_communication_interréseau {
    type_de_famille_adresse famille_adresse_interréseau;
    type_de_numéro_de_port_de_communication numéro_de_port_de_communication;
    struct adresse_interréseau contenu_adresse_interréseau;
    unsigned char remplissage_adresse[8];
};

#define protocole_interréseau_de_base 0
#define protocole_de_datagrammes_utilisateur 17
#define toute_adresse_locale ((type_de_valeur_adresse_interréseau)0x00000000U)
#define adresse_de_bouclage ((type_de_valeur_adresse_interréseau)0x7f000001U)

#endif
