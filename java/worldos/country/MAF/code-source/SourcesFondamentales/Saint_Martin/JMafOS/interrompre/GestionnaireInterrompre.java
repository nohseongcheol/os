// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Saint_Martin.JMafOS.interrompre;

import java.util.Arrays;

/** Enregistre et répartit les gestionnaires IDT du côté géré par Java. */
public final class GestionnaireInterrompre {
    private final GestionnaireÉvènementInterrompre[] listeGestionnaireÉvènement = new GestionnaireÉvènementInterrompre[256];
    private boolean actif;

    public void registreEntréeÉlément(int numéro, GestionnaireÉvènementInterrompre GestionnaireÉvènement) {
        vérifierNuméro(numéro);
        listeGestionnaireÉvènement[numéro] = GestionnaireÉvènement;
    }

    public void libérerStockage(int numéro) {
        vérifierNuméro(numéro);
        listeGestionnaireÉvènement[numéro] = null;
    }

    public int distribuerValeur(int numéro, int adressePileEnregistré) {
        vérifierNuméro(numéro);
        if (!actif) {
            return adressePileEnregistré;
        }
        GestionnaireÉvènementInterrompre GestionnaireÉvènement = listeGestionnaireÉvènement[numéro];
        return GestionnaireÉvènement == null ? adressePileEnregistré : GestionnaireÉvènement.entréeÉlémentValeurProcessus(adressePileEnregistré);
    }

    public void activer() {
        actif = true;
    }

    public void désactiver() {
        actif = false;
    }

    public boolean estActif() {
        return actif;
    }

    public void libérerTous() {
        Arrays.fill(listeGestionnaireÉvènement, null);
    }

    private void vérifierNuméro(int numéro) {
        if (numéro < 0 || numéro >= listeGestionnaireÉvènement.length) {
            throw new IllegalArgumentException("interrompre 번호가 올바르지 않습니다.");
        }
    }
}

