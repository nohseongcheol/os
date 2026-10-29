// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Pays_Bas.JNldOS.Écran;

import java.util.Arrays;

/** Modèle d’affichage 80x25 caractères, comme le mode texte VGA. */
public final class présenterCaractère {
    public static final int valeurLargeur = 80;
    public static final int valeurHauteur = 25;
    private final char[] valeursCaractère = new char[valeurLargeur * valeurHauteur];
    private int positionHorizontal;
    private int positionVertical;

    public présenterCaractère() {
        effacerEntréeÉlément();
    }

    public void Sortie(String valeurContenuValeur) {
        for (int numéro = 0; numéro < valeurContenuValeur.length(); numéro++) {
            char Caractères = valeurContenuValeur.charAt(numéro);
            if (Caractères == '\n') {
                positionHorizontal = 0;
                positionVertical++;
            } else {
                imprimerCaractère(positionHorizontal++, positionVertical, Caractères);
            }
            if (positionHorizontal >= valeurLargeur) {
                positionHorizontal = 0;
                positionVertical++;
            }
            if (positionVertical >= valeurHauteur) {
                hautDirectionDéfiler();
            }
        }
    }

    public char Caractères(int positionHorizontal, int positionVertical) {
        vérifierPosition(positionHorizontal, positionVertical);
        return valeursCaractère[positionVertical * valeurLargeur + positionHorizontal];
    }

    public void effacerEntréeÉlément() {
        Arrays.fill(valeursCaractère, ' ');
        positionHorizontal = 0;
        positionVertical = 0;
    }

    private void imprimerCaractère(int positionHorizontal, int positionVertical, char Caractères) {
        vérifierPosition(positionHorizontal, positionVertical);
        valeursCaractère[positionVertical * valeurLargeur + positionHorizontal] = Caractères;
    }

    private void hautDirectionDéfiler() {
        System.arraycopy(valeursCaractère, valeurLargeur, valeursCaractère, 0, valeurLargeur * (valeurHauteur - 1));
        Arrays.fill(valeursCaractère, valeurLargeur * (valeurHauteur - 1), valeursCaractère.length, ' ');
        positionVertical = valeurHauteur - 1;
    }

    private void vérifierPosition(int positionHorizontal, int positionVertical) {
        if (positionHorizontal < 0 || positionHorizontal >= valeurLargeur || positionVertical < 0 || positionVertical >= valeurHauteur) {
            throw new IllegalArgumentException("Écran 위치가 올바르지 않습니다.");
        }
    }
}

