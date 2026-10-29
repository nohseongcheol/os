#include <conversion_des_adresses/ordre_des_octets.h>
#include <errno.h>
#include <fcntl.h>
#include <interréseau/adresse.h>
#include <définitions_de_base.h>
#include <système/socket.h>
#include <système/stat.h>
#include <système/identité_du_système.h>
#include <système/attente_des_enfants.h>
#include <unistd.h>
#include "shell_locale.h"

/* Adapted from koros4's request interpreter. Private names are localized
 * in each WorldOS edition; main and POSIX ABI names remain unchanged. */

enum { capacité_de_la_ligne_d_entrée = 512, nombre_maximal_d_arguments = 16, imbrication_maximale_des_scripts = 4 };
static int profondeur_d_imbrication_des_scripts;
struct flux_d_entrée {
    int descripteur_d_entrée;
    char tampon_de_transfert_2[256];
    size_t position;
    size_t longueur;
};

static size_t longueur_du_texte_en_octets(const char *texte)
{
    size_t longueur = 0;
    while (texte[longueur] != '\0')
        longueur++;
    return longueur;
}

static int textes_identiques(const char *gauche, const char *droite)
{
    size_t position = 0;
    while (gauche[position] == droite[position]) {
        if (gauche[position] == '\0')
            return 1;
        position++;
    }
    return 0;
}

static void écrire_le_texte(const char *texte)
{
    size_t longueur = longueur_du_texte_en_octets(texte);
    while (longueur > 0U) {
        ssize_t nombre_d_octets_écrits = écrire(STDOUT_FILENO, texte, longueur);
        if (nombre_d_octets_écrits <= 0)
            return;
        texte += nombre_d_octets_écrits;
        longueur -= (size_t)nombre_d_octets_écrits;
    }
}

static void écrire_un_entier(int valeur)
{
    char caractères_des_chiffres[16];
    unsigned int nombre_de_chiffres;
    unsigned int grandeur_sans_signe;

    if (valeur < 0) {
        écrire_le_texte("-");
        grandeur_sans_signe = (unsigned int)(-(valeur + 1)) + 1U;
    } else {
        grandeur_sans_signe = (unsigned int)valeur;
    }
    nombre_de_chiffres = 0;
    do {
        caractères_des_chiffres[nombre_de_chiffres++] = (char)('0' + grandeur_sans_signe % 10U);
        grandeur_sans_signe /= 10U;
    } while (grandeur_sans_signe != 0U);
    while (nombre_de_chiffres > 0U) {
        nombre_de_chiffres--;
        (void)écrire(STDOUT_FILENO, &caractères_des_chiffres[nombre_de_chiffres], 1);
    }
}

static void signaler_une_erreur(const char *opération)
{
    écrire_le_texte("error: ");
    écrire_le_texte(opération);
    écrire_le_texte(" errno=");
    écrire_un_entier(errno);
    écrire_le_texte("\n");
}

static int lire_une_ligne(struct flux_d_entrée *entrée, char *ligne_d_entrée, size_t capacité)
{
    size_t position = 0;
    int ligne_d_entrée_invalide = 0;
    char caractère;
    ssize_t octets_lus;
    if (capacité < 2U)
        return -2;
    for (;;) {
        if (entrée->position == entrée->longueur) {
            octets_lus = lire(entrée->descripteur_d_entrée, entrée->tampon_de_transfert_2, sizeof(entrée->tampon_de_transfert_2));
            if (octets_lus < 0) {
                if (errno == EINTR)
                    continue;
                return -1;
            }
            if (octets_lus == 0) {
                if (position == 0 && !ligne_d_entrée_invalide)
                    return -1;
                break;
            }
            entrée->longueur = (size_t)octets_lus;
            entrée->position = 0;
        }
        caractère = entrée->tampon_de_transfert_2[entrée->position++];
        if (caractère == '\n')
            break;
        if (entrée->descripteur_d_entrée == STDIN_FILENO && caractère == 4) {
            if (position == 0 && !ligne_d_entrée_invalide)
                return -1;
            break;
        }
        if (entrée->descripteur_d_entrée == STDIN_FILENO && (caractère == 8 || caractère == 127)) {
            if (position > 0) {
                do {
                    position--;
                } while (position > 0 && ((unsigned char)ligne_d_entrée[position] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (caractère == '\r')
            continue;
        if (caractère == '\0') {
            ligne_d_entrée_invalide = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (position + 1U < capacité)
            ligne_d_entrée[position++] = caractère;
        else
            ligne_d_entrée_invalide = 1;
    }
    ligne_d_entrée[position] = '\0';
    return ligne_d_entrée_invalide ? -2 : (int)position;
}

static int séparer_les_arguments(char *ligne_d_entrée, char **arguments)
{
    int nombre_d_arguments = 0;
    char *position_courante = ligne_d_entrée;
    char *position_de_sortie = ligne_d_entrée;

    while (*position_courante != '\0') {
        char guillemet = '\0';
        while (*position_courante == ' ' || *position_courante == '\t')
            position_courante++;
        if (*position_courante == '\0' || *position_courante == '#')
            break;
        if (nombre_d_arguments == nombre_maximal_d_arguments - 1)
            return -1;
        arguments[nombre_d_arguments++] = position_de_sortie;
        while (*position_courante != '\0') {
            char caractère = *position_courante++;
            if (guillemet == '\0' && (caractère == ' ' || caractère == '\t'))
                break;
            if (caractère == '\\' && guillemet != '\'') {
                if (*position_courante == '\0')
                    return -1;
                *position_de_sortie++ = *position_courante++;
            } else if (caractère == '\'' || caractère == '"') {
                if (guillemet == '\0')
                    guillemet = caractère;
                else if (guillemet == caractère)
                    guillemet = '\0';
                else
                    *position_de_sortie++ = caractère;
            } else {
                *position_de_sortie++ = caractère;
            }
        }
        if (guillemet != '\0')
            return -1;
        *position_de_sortie++ = '\0';
    }
    arguments[nombre_d_arguments] = (char *)0;
    return nombre_d_arguments;
}

static void afficher_l_aide(void)
{
    size_t position;
    écrire_le_texte(
        "WorldOS command interpreter commands:\n"
        "  help                 show this help\n"
        "  echo TEXT            print text\n"
        "  pwd                  show current directory\n"
        "  cd PATH              change directory\n"
        "  cat FILE             print a FAT file\n"
        "  stat FILE            show file size\n"
        "  pid                  show process identifiers\n"
        "  uname                show operating-system identity\n"
        "  run FILE [ARGS...]   execute a user ELF program\n"
        "  udp [TEXT]           call POSIX UDP and loop back TEXT\n"
        "  source FILE          interpret a UTF-8 command file\n"
        "  exit                 leave the shell\n");
    écrire_le_texte("Native command proposals (ASCII aliases remain available):\n");
    for (position = 0; position < sizeof(commandes_de_référence) / sizeof(commandes_de_référence[0]); position++) {
        écrire_le_texte(alias_locaux_des_commandes[position]);
        écrire_le_texte(" = ");
        écrire_le_texte(commandes_de_référence[position]);
        écrire_le_texte("\n");
    }
}

static int commande_correspondante(const char *texte, const char *commande)
{
    size_t position;
    if (textes_identiques(texte, commande))
        return 1;
    for (position = 0; position < sizeof(commandes_de_référence) / sizeof(commandes_de_référence[0]); position++)
        if (textes_identiques(commande, commandes_de_référence[position]))
            return textes_identiques(texte, alias_locaux_des_commandes[position]);
    return 0;
}

static int interpréter_l_entrée(int descripteur_d_entrée);

static int interpréter_un_fichier_de_commandes(const char *nom_du_fichier)
{
    int descripteur_de_fichier_2;
    int état;
    if (profondeur_d_imbrication_des_scripts >= imbrication_maximale_des_scripts) {
        écrire_le_texte("source: nesting limit\n");
        return 0;
    }
    descripteur_de_fichier_2 = ouvrir(nom_du_fichier, O_RDONLY);
    if (descripteur_de_fichier_2 < 0) {
        signaler_une_erreur(nom_du_fichier);
        return 0;
    }
    profondeur_d_imbrication_des_scripts++;
    état = interpréter_l_entrée(descripteur_de_fichier_2);
    profondeur_d_imbrication_des_scripts--;
    (void)fermer(descripteur_de_fichier_2);
    return état;
}

static void afficher_les_arguments(int nombre_d_arguments, char **arguments)
{
    int position;
    for (position = 1; position < nombre_d_arguments; position++) {
        if (position != 1)
            écrire_le_texte(" ");
        écrire_le_texte(arguments[position]);
    }
    écrire_le_texte("\n");
}

static void afficher_le_répertoire_courant(void)
{
    char chemin[128];
    if (obtenir_le_chemin_du_répertoire_courant(chemin, sizeof(chemin)) == (char *)0) {
        signaler_une_erreur("pwd");
        return;
    }
    écrire_le_texte(chemin);
    écrire_le_texte("\n");
}

static void afficher_le_contenu_du_fichier(const char *nom_du_fichier)
{
    char tampon_de_transfert_2[128];
    int descripteur_de_fichier_2 = ouvrir(nom_du_fichier, O_RDONLY);
    ssize_t octets_lus;

    if (descripteur_de_fichier_2 < 0) {
        signaler_une_erreur("cat");
        return;
    }
    while ((octets_lus = lire(descripteur_de_fichier_2, tampon_de_transfert_2, sizeof(tampon_de_transfert_2))) > 0)
        (void)écrire(STDOUT_FILENO, tampon_de_transfert_2, (size_t)octets_lus);
    if (octets_lus < 0)
        signaler_une_erreur("cat/read");
    (void)fermer(descripteur_de_fichier_2);
    écrire_le_texte("\n");
}

static void afficher_les_informations_du_fichier(const char *nom_du_fichier)
{
    struct état_du_fichier état;
    if (état_du_fichier(nom_du_fichier, &état) < 0) {
        signaler_une_erreur("stat");
        return;
    }
    écrire_le_texte("size=");
    écrire_un_entier((int)état.st_size);
    écrire_le_texte(S_ISDIR(état.st_mode) ? " type=directory\n" : " type=file\n");
}

static void afficher_les_identifiants_des_processus(void)
{
    écrire_le_texte("pid=");
    écrire_un_entier((int)obtenir_identifiant_du_processus());
    écrire_le_texte(" ppid=");
    écrire_un_entier((int)obtenir_identifiant_du_parent());
    écrire_le_texte("\n");
}

static void afficher_l_identité_du_système(void)
{
    struct utsname identité_du_système;
    if (obtenir_informations_du_système(&identité_du_système) < 0) {
        signaler_une_erreur("uname");
        return;
    }
    écrire_le_texte(identité_du_système.sysname);
    écrire_le_texte(" ");
    écrire_le_texte(identité_du_système.release);
    écrire_le_texte(" ");
    écrire_le_texte(identité_du_système.machine);
    écrire_le_texte("\n");
}

static void exécuter_un_programme(int nombre_d_arguments, char **arguments)
{
    pid_t identifiant_du_processus_enfant;
    int état_de_terminaison_de_l_enfant = 0;

    if (nombre_d_arguments < 2) {
        écrire_le_texte("usage: run FILE [ARGS...]\n");
        return;
    }
    identifiant_du_processus_enfant = dédoubler_le_processus();
    if (identifiant_du_processus_enfant < 0) {
        signaler_une_erreur("fork");
        return;
    }
    if (identifiant_du_processus_enfant == 0) {
        remplacer_le_programme_exécuté(arguments[1], &arguments[1], (char *const *)0);
        signaler_une_erreur("execve");
        terminer_immédiatement(127);
    }
    if (attendre_un_enfant_désigné(identifiant_du_processus_enfant, &état_de_terminaison_de_l_enfant, 0) < 0) {
        signaler_une_erreur("waitpid");
        return;
    }
    écrire_le_texte("exit-status=");
    écrire_un_entier(WEXITSTATUS(état_de_terminaison_de_l_enfant));
    écrire_le_texte("\n");
}

static void tester_le_retour_du_datagramme(const char *message)
{
    struct adresse_du_point_de_communication_interréseau adresse_de_réception = {0};
    struct adresse_du_point_de_communication_interréseau adresse_de_l_expéditeur = {0};
    type_de_longueur_adresse longueur_de_l_adresse_de_l_expéditeur = sizeof(adresse_de_l_expéditeur);
    char données_reçues[96];
    size_t longueur_du_message_en_octets = longueur_du_texte_en_octets(message);
    int point_de_réception = -1;
    int point_d_envoi = -1;
    ssize_t nombre_d_octets_reçus;

    if (longueur_du_message_en_octets >= sizeof(données_reçues)) {
        écrire_le_texte("udp: message exceeds 95 bytes\n");
        return;
    }
    point_de_réception = créer_un_point_de_communication(code_de_famille_adresse_interréseau, point_de_datagrammes, protocole_de_datagrammes_utilisateur);
    point_d_envoi = créer_un_point_de_communication(code_de_famille_adresse_interréseau, point_de_datagrammes, protocole_de_datagrammes_utilisateur);
    if (point_de_réception < 0 || point_d_envoi < 0) {
        signaler_une_erreur("socket");
        goto fermer_les_points_de_communication;
    }
    adresse_de_réception.famille_adresse_interréseau = code_de_famille_adresse_interréseau;
    adresse_de_réception.numéro_de_port_de_communication = convertir_16_bits_vers_ordre_réseau(40404);
    adresse_de_réception.contenu_adresse_interréseau.valeur_adresse = convertir_32_bits_vers_ordre_réseau(adresse_de_bouclage);
    if (associer_une_adresse_locale(point_de_réception, (const struct adresse_du_point_de_communication *)&adresse_de_réception, sizeof(adresse_de_réception)) < 0) {
        signaler_une_erreur("bind");
        goto fermer_les_points_de_communication;
    }
    if (connecter_au_correspondant(point_d_envoi, (const struct adresse_du_point_de_communication *)&adresse_de_réception, sizeof(adresse_de_réception)) < 0) {
        signaler_une_erreur("connect");
        goto fermer_les_points_de_communication;
    }
    if (envoyer(point_d_envoi, message, longueur_du_message_en_octets, 0) != (ssize_t)longueur_du_message_en_octets) {
        signaler_une_erreur("send");
        goto fermer_les_points_de_communication;
    }
    nombre_d_octets_reçus = recevoir_avec_adresse_source(point_de_réception, données_reçues, sizeof(données_reçues) - 1U, 0,
                         (struct adresse_du_point_de_communication *)&adresse_de_l_expéditeur, &longueur_de_l_adresse_de_l_expéditeur);
    if (nombre_d_octets_reçus < 0) {
        signaler_une_erreur("recvfrom");
        goto fermer_les_points_de_communication;
    }
    données_reçues[nombre_d_octets_reçus] = '\0';
    écrire_le_texte("udp-received: ");
    écrire_le_texte(données_reçues);
    écrire_le_texte("\n");

fermer_les_points_de_communication:
    if (point_d_envoi >= 0)
        (void)fermer(point_d_envoi);
    if (point_de_réception >= 0)
        (void)fermer(point_de_réception);
}

static int interpréter_l_entrée(int descripteur_d_entrée)
{
    char ligne_d_entrée[capacité_de_la_ligne_d_entrée];
    char *arguments[nombre_maximal_d_arguments];
    struct flux_d_entrée entrée = {0};
    entrée.descripteur_d_entrée = descripteur_d_entrée;

    for (;;) {
        int nombre_d_arguments;
        int état;
        if (descripteur_d_entrée == STDIN_FILENO)
            écrire_le_texte("worldos$ ");
        état = lire_une_ligne(&entrée, ligne_d_entrée, sizeof(ligne_d_entrée));
        if (état == -1)
            return 0;
        if (état == -2) {
            écrire_le_texte("input rejected: overlong or binary line\n");
            continue;
        }
        nombre_d_arguments = séparer_les_arguments(ligne_d_entrée, arguments);
        if (nombre_d_arguments < 0) {
            écrire_le_texte("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (nombre_d_arguments == 0)
            continue;
        if (commande_correspondante(arguments[0], "help"))
            afficher_l_aide();
        else if (commande_correspondante(arguments[0], "echo"))
            afficher_les_arguments(nombre_d_arguments, arguments);
        else if (commande_correspondante(arguments[0], "pwd"))
            afficher_le_répertoire_courant();
        else if (commande_correspondante(arguments[0], "cd")) {
            if (nombre_d_arguments < 2)
                écrire_le_texte("usage: cd PATH\n");
            else if (changer_le_répertoire_courant(arguments[1]) < 0)
                signaler_une_erreur("cd");
        } else if (commande_correspondante(arguments[0], "cat")) {
            if (nombre_d_arguments < 2)
                écrire_le_texte("usage: cat FILE\n");
            else
                afficher_le_contenu_du_fichier(arguments[1]);
        } else if (commande_correspondante(arguments[0], "stat")) {
            if (nombre_d_arguments < 2)
                écrire_le_texte("usage: stat FILE\n");
            else
                afficher_les_informations_du_fichier(arguments[1]);
        } else if (commande_correspondante(arguments[0], "pid"))
            afficher_les_identifiants_des_processus();
        else if (commande_correspondante(arguments[0], "uname"))
            afficher_l_identité_du_système();
        else if (commande_correspondante(arguments[0], "run"))
            exécuter_un_programme(nombre_d_arguments, arguments);
        else if (commande_correspondante(arguments[0], "udp"))
            tester_le_retour_du_datagramme(nombre_d_arguments >= 2 ? arguments[1] : "ping");
        else if (commande_correspondante(arguments[0], "source")) {
            if (nombre_d_arguments < 2)
                écrire_le_texte("usage: source FILE\n");
            else if (interpréter_un_fichier_de_commandes(arguments[1]))
                return 1;
        } else if (commande_correspondante(arguments[0], "exit"))
            return 1;
        else
            écrire_le_texte("unknown command; type help\n");
    }
}

int main(void)
{
    écrire_le_texte("WORLDOS-SHELL:READY\n");
    (void)interpréter_l_entrée(STDIN_FILENO);
    écrire_le_texte("WORLDOS-SHELL:EXIT\n");
    return 0;
}
