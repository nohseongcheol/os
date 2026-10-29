// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
import java.util.HashMap;
/** Associe des clés de recherche à des valeurs. */
public final class Dictionnaire {
    private final HashMap<String, String> valeurEntréeÉlément = new HashMap<String, String>();
    public String placerValeur(String matériauTouche, String valeur) { return valeurEntréeÉlément.put(matériauTouche, valeur); }
    public String trouverEntréeÉlément(String matériauTouche) { return valeurEntréeÉlément.get(matériauTouche); }
    public boolean effectueExistence(String matériauTouche) { return valeurEntréeÉlément.containsKey(matériauTouche); }
    public String effacerEntréeÉlément(String matériauTouche) { return valeurEntréeÉlément.remove(matériauTouche); }
    public int taille() { return valeurEntréeÉlément.size(); }
    public void effacerContenuContenu() { valeurEntréeÉlément.clear(); }
}
