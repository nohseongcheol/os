#include <conversion_des_adresses/ordre_des_octets.h>
#include <errno.h>
#include <système/socket.h>
#include <unistd.h>

static unsigned int length_of(const char *s)
{
    unsigned int n = 0;
    while (s[n] != 0) n++;
    return n;
}

static void say(const char *s) { (void)écrire(STDOUT_FILENO, s, length_of(s)); }

static void report(const char *identité_du_système, int pass)
{
    say(pass ? "NTEST:PASS:" : "NTEST:FAIL:");
    say(identité_du_système);
    say("\n");
}

int main(void)
{
    struct adresse_du_point_de_communication_interréseau server_address = {0};
    struct adresse_du_point_de_communication_interréseau source = {0};
    type_de_longueur_adresse source_length = sizeof(source);
    char tampon_de_transfert_2[8] = {0};
    int server = créer_un_point_de_communication(code_de_famille_adresse_interréseau, point_de_datagrammes, protocole_de_datagrammes_utilisateur);
    int client = créer_un_point_de_communication(code_de_famille_adresse_interréseau, point_de_datagrammes, 0);

    report("socket-server", server >= 3);
    report("socket-client", client >= 3 && client != server);
    server_address.famille_adresse_interréseau = code_de_famille_adresse_interréseau;
    server_address.numéro_de_port_de_communication = convertir_16_bits_vers_ordre_réseau(32345);
    server_address.contenu_adresse_interréseau.valeur_adresse = convertir_32_bits_vers_ordre_réseau(adresse_de_bouclage);
    report("bind", associer_une_adresse_locale(server, (const struct adresse_du_point_de_communication *)&server_address,
                        sizeof(server_address)) == 0);
    report("connect", connecter_au_correspondant(client, (const struct adresse_du_point_de_communication *)&server_address,
                              sizeof(server_address)) == 0);
    report("send", envoyer(client, "ping", 4, 0) == 4);
    report("recvfrom", recevoir_avec_adresse_source(server, tampon_de_transfert_2, sizeof(tampon_de_transfert_2), 0,
                                (struct adresse_du_point_de_communication *)&source, &source_length) == 4 &&
                       tampon_de_transfert_2[0] == 'p' && tampon_de_transfert_2[3] == 'g' && source_length == 16);
    errno = 0;
    report("empty-eagain", recevoir(server, tampon_de_transfert_2, sizeof(tampon_de_transfert_2), 0) == -1 && errno == EAGAIN);
    report("getsockname", obtenir_adresse_locale(server, (struct adresse_du_point_de_communication *)&source,
                                      &source_length) == 0 && source.numéro_de_port_de_communication == convertir_16_bits_vers_ordre_réseau(32345));
    errno = 0;
    report("udp-listen-not-supported", préparer_accueil_des_connexions(server, 1) == -1 && errno == EOPNOTSUPP);
    report("close-client", fermer(client) == 0);
    report("close-server", fermer(server) == 0);
    say("NTEST:DONE\n");
    return 0;
}
