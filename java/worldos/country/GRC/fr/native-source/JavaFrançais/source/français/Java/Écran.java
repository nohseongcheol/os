// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.Java;

import javax.swing.*;

public final class Écran {
    private Écran() {}
    public static void valeurUltérieur(Runnable action) { SwingUtilities.invokeLater(action); }
    /** Appeler sur le fil de répartition des événements Swing. */
    public static JFrame fenêtre(String titreFenêtre, JComponent valeurContenuValeur, int valeurLargeur, int valeurHauteur) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("Écran.valeurUltérieur 안에서 창을 만드세요");
        JFrame fenêtre = new JFrame(titreFenêtre);
        fenêtre.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        fenêtre.setContentPane(valeurContenuValeur);
        fenêtre.setSize(valeurLargeur, valeurHauteur);
        fenêtre.setLocationByPlatform(true);
        fenêtre.setVisible(true);
        return fenêtre;
    }
}
