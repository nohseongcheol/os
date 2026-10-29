// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Luxembourg.JLuxOS.AppelSystème;

import Luxembourg.JLuxOS.EspaceMémoire.GestionnairePage;
import Luxembourg.JLuxOS.Tâche.valeurProcessus;
import Luxembourg.JLuxOS.Tâche.Ordonnanceur;
import Luxembourg.JLuxOS.SystèmeFichier.ChargeurCodeExécutable;
import Luxembourg.JLuxOS.SystèmeFichier.SystèmeFichier;
import Luxembourg.JLuxOS.SystèmeFichier.informationFichier;
import Luxembourg.JLuxOS.Noyau.valeurMatériel;
import Luxembourg.JLuxOS.valeurEntrée.GestionnaireEntrée;
import Luxembourg.JLuxOS.valeurEntrée.évènementEntrée;

/** Couche de gestion Java des appels POSIX de première étape d’engos. */
public final class AppelSystème {
    public static final int lireDrapeauSeulement = 0;
    public static final int chercherDémarrer = 0;
    public static final int chercherActuel = 1;
    public static final int trouverFinEntréeÉlément = 2;

    private final SystèmeFichier SystèmeFichier;
    private final GestionnairePage gestionPage;
    private final Ordonnanceur Ordonnanceur;
    private final ChargeurCodeExécutable chargeur = new ChargeurCodeExécutable();
    private final valeurMatériel Périphérique;
    private final GestionnaireEntrée GestionEntrée;

    public AppelSystème(SystèmeFichier SystèmeFichier, GestionnairePage gestionPage, Ordonnanceur Ordonnanceur, valeurMatériel Périphérique, GestionnaireEntrée GestionEntrée) {
        this.SystèmeFichier = SystèmeFichier;
        this.gestionPage = gestionPage;
        this.Ordonnanceur = Ordonnanceur;
        this.Périphérique = Périphérique;
        this.GestionEntrée = GestionEntrée;
    }

    public int identificateurProcessus(valeurProcessus processusActuel) {
        return processusActuel.valeurIdentificateur();
    }

    public int identificateurProcessusParent(valeurProcessus processusActuel) {
        return processusActuel.identificateurParent();
    }

    public int ouvrir(valeurProcessus processusActuel, String nom, int valeurDrapeau) {
        if (valeurDrapeau != lireDrapeauSeulement) {
            return -30;
        }
        return processusActuel.descripteurFichier().ouvrir(nom);
    }

    public int lire(valeurProcessus processusActuel, int entréeÉlémentDescripteur, byte[] recevoirDestination, int taille) {
        if (entréeÉlémentDescripteur == 0) {
            if (taille <= 0 || recevoirDestination.length == 0) {
                return 0;
            }
            évènementEntrée évènement = GestionEntrée.évènementSuivant();
            if (évènement == null || évènement.genreÉvènement() != évènementEntrée.valeurGenre.basDirectionTouche) {
                return -11;
            }
            recevoirDestination[0] = (byte) évènement.valeurPremier();
            return 1;
        }
        return processusActuel.descripteurFichier().lire(entréeÉlémentDescripteur, recevoirDestination, taille);
    }

    public int écrire(valeurProcessus processusActuel, int entréeÉlémentDescripteur, byte[] Données, int taille) {
        if (entréeÉlémentDescripteur != 1 && entréeÉlémentDescripteur != 2) {
            return processusActuel.descripteurFichier().estOuvrir(entréeÉlémentDescripteur) ? -30 : -9;
        }
        if (taille < 0 || taille > Données.length) {
            return -22;
        }
        Périphérique.sortieSériel(new String(Données, 0, taille, java.nio.charset.StandardCharsets.UTF_8));
        return taille;
    }

    public int fermer(valeurProcessus processusActuel, int entréeÉlémentDescripteur) {
        return processusActuel.descripteurFichier().fermer(entréeÉlémentDescripteur);
    }

    public int positionDéplacer(valeurProcessus processusActuel, int entréeÉlémentDescripteur, int valeurDistance, int racineProjet) {
        return processusActuel.descripteurFichier().positionDéplacer(entréeÉlémentDescripteur, valeurDistance, racineProjet);
    }

    public int descripteurDuplicata(valeurProcessus processusActuel, int entréeÉlémentDescripteur) {
        return processusActuel.descripteurFichier().descripteurCloné(entréeÉlémentDescripteur, 0);
    }

    public int àPositionDescripteurDuplicata(valeurProcessus processusActuel, int entréeÉlémentDescripteur, int descripteurNouveau) {
        return processusActuel.descripteurFichier().àPositionDuplicata(entréeÉlémentDescripteur, descripteurNouveau);
    }

    public int estAccessible(String nom, int modeMéthode) {
        informationFichier informationSystème = SystèmeFichier.informationSystème(nom);
        if (informationSystème == null) {
            return -2;
        }
        if ((modeMéthode & 1) != 0 && (informationSystème.genreForme() & 0111) == 0) {
            return -13;
        }
        if ((modeMéthode & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int listeTâcheCommuter(String nom) {
        return "/".equals(nom) ? 0 : -20;
    }

    public String listeTâcheActuel(int recevoirTaille) {
        return recevoirTaille >= 2 ? "/" : null;
    }

    public int identificateurUtilisateur() { return 0; }
    public int identificateurUtilisateurEfficace() { return 0; }
    public int identificateurGroupe() { return 0; }
    public int identificateurGroupeEfficace() { return 0; }

    public int synchroniserFichier(valeurProcessus processusActuel, int entréeÉlémentDescripteur) {
        return processusActuel.descripteurFichier().informationSystème(entréeÉlémentDescripteur) == null ? -9 : 0;
    }

    public void synchroniserTous() {
        // Le système de fichiers actuel est en lecture seule ; aucune donnée n’est donc à vider.
    }

    public boolean estTerminal(valeurProcessus processusActuel, int entréeÉlémentDescripteur) {
        informationFichier informationSystème = processusActuel.descripteurFichier().informationSystème(entréeÉlémentDescripteur);
        return informationSystème != null && (informationSystème.genreForme() & 0170000) == 0020000;
    }

    public int contrôleFichier(valeurProcessus processusActuel, int entréeÉlémentDescripteur, int commande, int argumentParamètre) {
        if (commande == 0) {
            return processusActuel.descripteurFichier().descripteurCloné(entréeÉlémentDescripteur, argumentParamètre);
        }
        if (commande == 1) {
            return processusActuel.descripteurFichier().fermerValeurOpérationExécutionActivé(entréeÉlémentDescripteur);
        }
        if (commande == 2) {
            return processusActuel.descripteurFichier().définirOpérationExécutionActivéFermer(entréeÉlémentDescripteur, (argumentParamètre & 1) != 0);
        }
        if (commande == 3) {
            return processusActuel.descripteurFichier().informationSystème(entréeÉlémentDescripteur) == null ? -9 : lireDrapeauSeulement;
        }
        if (commande == 4) {
            return argumentParamètre == lireDrapeauSeulement ? 0 : -30;
        }
        return -22;
    }

    public int créerEntréeÉlément(String nom, int valeurPermission) {
        return -30;
    }

    public informationFichier informationDescripteur(valeurProcessus processusActuel, int entréeÉlémentDescripteur) {
        return processusActuel.descripteurFichier().informationSystème(entréeÉlémentDescripteur);
    }

    public détailsSystème détailsSystème() {
        return new détailsSystème("JLuxOS", "JLuxOS", "0.1", "Java managed kernel", "i386");
    }

    public informationFichier informationFichier(String nom) {
        return SystèmeFichier.informationSystème(nom);
    }

    public valeurProcessus processusCloner(valeurProcessus valeurParent) {
        return Ordonnanceur.valeurCloner(valeurParent);
    }

    public int attendreEnfantPour(valeurProcessus valeurParent, int identificateurEnfant, boolean bloquantNon) {
        return Ordonnanceur.attendreEnfantPour(valeurParent, identificateurEnfant, bloquantNon);
    }

    public int rompreProgramme(valeurProcessus processusActuel, int finNouveau) {
        int finPrécédentÉlément = processusActuel.rompreProgramme();
        if (finNouveau == 0) {
            return finPrécédentÉlément;
        }
        if (finNouveau < 0x06000000 || finNouveau > 0x07000000) {
            return -12;
        }
        int pagePremier = finPrécédentÉlément / GestionnairePage.taillePage;
        int pageDernier = (finNouveau + GestionnairePage.taillePage - 1) / GestionnairePage.taillePage;
        if (finNouveau > finPrécédentÉlément) {
            for (int numéro = pagePremier; numéro < pageDernier; numéro++) {
                int adresse = numéro * GestionnairePage.taillePage;
                try {
                    gestionPage.lireValeurOctet(processusActuel.EspaceAdresse(), adresse);
                } catch (IllegalStateException erreur) {
                    gestionPage.pageTableCorrespondance(processusActuel.EspaceAdresse(), adresse, true);
                }
            }
        }
        processusActuel.définirRompreProgramme(finNouveau);
        return finNouveau;
    }

    public int augmenterRompreProgramme(valeurProcessus processusActuel, int montantIncrément) {
        int finPrécédentÉlément = processusActuel.rompreProgramme();
        int résultat = rompreProgramme(processusActuel, finPrécédentÉlément + montantIncrément);
        return résultat < 0 ? résultat : finPrécédentÉlément;
    }

    public int exécuterCommande(valeurProcessus processusActuel, byte[] fichierCodeExécutable) {
        return exécuterCommande(processusActuel, fichierCodeExécutable, new String[0], new String[0]);
    }

    public int exécuterCommande(valeurProcessus processusActuel, byte[] fichierCodeExécutable, String[] argumentParamètre, String[] environnement) {
        ChargeurCodeExécutable.image valeurImage;
        try {
            valeurImage = chargeur.Contrôles(fichierCodeExécutable);
        } catch (IllegalArgumentException erreur) {
            return -8;
        }
        if (argumentParamètre == null || environnement == null || argumentParamètre.length > 16 || environnement.length > 16) {
            return -7;
        }
        for (ChargeurCodeExécutable.valeurSection valeurSection : valeurImage.listeSections()) {
            if ((valeurSection.valeurDrapeau() & 2) == 0 || valeurSection.taille() == 0) {
                continue;
            }
            int pagePremier = valeurSection.adresse() / GestionnairePage.taillePage;
            int pageDernier = (valeurSection.adresse() + valeurSection.taille() + GestionnairePage.taillePage - 1) / GestionnairePage.taillePage;
            for (int numéro = pagePremier; numéro < pageDernier; numéro++) {
                int adresse = numéro * GestionnairePage.taillePage;
                try {
                    gestionPage.lireValeurOctet(processusActuel.EspaceAdresse(), adresse);
                    gestionPage.écrirePlagePrivé(processusActuel.EspaceAdresse(), adresse, GestionnairePage.taillePage);
                } catch (IllegalStateException erreur) {
                    gestionPage.pageTableCorrespondance(processusActuel.EspaceAdresse(), adresse, true);
                }
            }
            for (int numéro = 0; numéro < valeurSection.taille(); numéro++) {
                byte valeur = valeurSection.valeurGenre() == 8 ? 0 : fichierCodeExécutable[valeurSection.positionFichier() + numéro];
                gestionPage.écrireValeurOctet(processusActuel.EspaceAdresse(), valeurSection.adresse() + numéro, valeur);
            }
        }
        processusActuel.définirContexteExécution(valeurImage.démarrerAdresse(), argumentParamètre, environnement);
        processusActuel.descripteurFichier().fermerOpérationExécutionActivé();
        return 0;
    }

    public void programmeTerminerSession(valeurProcessus processusActuel, int valeurÉtatValeur) {
        processusActuel.programmeQuitter(valeurÉtatValeur);
    }
}
