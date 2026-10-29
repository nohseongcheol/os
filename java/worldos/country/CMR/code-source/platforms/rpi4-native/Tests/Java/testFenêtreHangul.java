// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import français.interne.fenêtre;
import français.interne.ComposantVisuel;
import français.interne.*;

public class testFenêtreHangul implements TâcheTâcheExécutable, RécepteurAction {
    fenêtre Écran;
    étiquette Guide;
    ChampTexte valeurEntrée;
    public void exécuterTâche() {
        Contrôles.exiger(FileAttenteÉvènement.estDistributionEnCoursÉvènement(), "français Écran Tâche 큐");
        Écran = new fenêtre("français bibliothèque fenêtre", 400, 280);
        Guide = ComposantVisuel.valeurBalise("한글로 Java 코딩", 20, 20, 340, 30);
        valeurEntrée = ComposantVisuel.ChampTexte("nom", 20, 65, 340, 30);
        Écran.ajouterÉlément(Guide);
        Écran.ajouterÉlément(valeurEntrée);
        Écran.ajouterÉlément(ComposantVisuel.bouton("saluer", 20, 110, 180, 32, this));
        Écran.afficherFenêtre();
        Sortie.écrireLigne("KOREAN SWING READY");
    }
    public void recevoirAction(NotificationAction évènement) {
        Contrôles.exiger(FileAttenteÉvènement.estDistributionEnCoursÉvènement(), "français action 되부름");
        Contrôles.exiger(évènement.numéro() == 1001 && évènement.sourceÉvènement() instanceof bouton, "français évènement 객체와 valeurOrigine");
        Contrôles.exiger(!((Object)évènement.sourceÉvènement() instanceof javax.swing.JButton), "표준 단추와 독립된 valeurFormat");
        Contrôles.exiger(!((Object)évènement instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 valeurFormat");
        Guide.écrireTexte("안녕하세요 " + valeurEntrée.lireTexte());
        Sortie.écrireLigne("KOREAN SWING CLICK " + valeurEntrée.lireTexte());
    }
    public static void main(String[] arguments) {
        FileAttenteÉvènement.invoquerUltérieur(new testFenêtreHangul());
    }
}
