// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.Java;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** Distingue le nombre de char UTF-16 du nombre de points de code Unicode. */
public final class Caractères {
    private Caractères() {}
    public static byte[] encoder(String valeurContenuValeur) { return valeurContenuValeur.getBytes(StandardCharsets.UTF_8); }
    public static String déchiffrerDonnées(byte[] valeurContenuValeur) { return new String(valeurContenuValeur, StandardCharsets.UTF_8); }
    public static String normaliserValeur(String valeurContenuValeur) { return Normalizer.normalize(valeurContenuValeur, Normalizer.Form.NFC); }
    public static int nombreÉlémentsPointCode(String valeurContenuValeur) { return valeurContenuValeur.codePointCount(0, valeurContenuValeur.length()); }
    public static List<String> motLexical(String valeurContenuValeur, Locale Langue) {
        BreakIterator valeurDiviseur = BreakIterator.getWordInstance(Langue);
        valeurDiviseur.setText(valeurContenuValeur);
        List<String> résultat = new ArrayList<>();
        int lancer = valeurDiviseur.first();
        for (int terminaison = valeurDiviseur.next(); terminaison != BreakIterator.DONE; lancer = terminaison, terminaison = valeurDiviseur.next())
            résultat.add(valeurContenuValeur.substring(lancer, terminaison));
        return résultat;
    }
}
