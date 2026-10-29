// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import français.interne.fenêtre;
import français.interne.étiquette;
import français.interne.ChampTexte;
import français.interne.bouton;
import français.interne.FileAttenteÉvènement;
import français.interne.Sortie;
import français.interne.TâcheTâcheExécutable;
import français.interne.RécepteurAction;
import français.interne.NotificationAction;

/** Fenêtre Swing du noyau autonome : saisie française, action du bouton, puis mise à jour du libellé. */
public class ExempleFenêtre implements TâcheTâcheExécutable, RécepteurAction {
    private fenêtre fenêtreSalutation;
    private ChampTexte champNom;
    private étiquette salutation;
    private int nombreÉlémentsSalutation;

    public void ouvrirFenêtre() {
        fenêtreSalutation = new fenêtre("fr Swing", 460, 300);
        fenêtreSalutation.ajouterÉlément(new étiquette("Bonjour", 20, 20, 420, 28));
        champNom = new ChampTexte("fr", 20, 64, 420, 30);
        salutation = new étiquette("Bonjour", 20, 152, 420, 28);
        fenêtreSalutation.ajouterÉlément(champNom);
        fenêtreSalutation.ajouterÉlément(new bouton("saluer", 20, 108, 180, 32, this));
        fenêtreSalutation.ajouterÉlément(salutation);
        fenêtreSalutation.ajouterÉlément(new étiquette("F9 / Shift+Space | X", 20, 204, 420, 28));
        fenêtreSalutation.afficherFenêtre();
        Sortie.écrireLigne("GUI Exemples préparer: ExempleFenêtre");
    }

    public void saluer() {
        nombreÉlémentsSalutation++;
        salutation.écrireTexte("Bonjour, " + champNom.lireTexte() + "님! (" + nombreÉlémentsSalutation + ")");
        Sortie.écrireLigne("GUI Salutation: " + salutation.lireTexte());
    }

    public void exécuterTâche() { ouvrirFenêtre(); }
    public void recevoirAction(NotificationAction notification) {
        Sortie.écrireLigne("action notification: " + notification.texteCommande());
        saluer();
    }
    public static void lancer() {
        FileAttenteÉvènement.invoquerUltérieur(new ExempleFenêtre());
    }
}
