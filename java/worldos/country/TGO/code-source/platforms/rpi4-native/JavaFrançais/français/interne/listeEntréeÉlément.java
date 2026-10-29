// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
import java.util.ArrayList;
/** Collection ordonnée d’éléments. Cette édition fournit des listes de chaînes. */
public final class listeEntréeÉlément {
    private final ArrayList<String> valeurEntréeÉlément = new ArrayList<String>();
    public void ajouterValeurs(String valeur) { valeurEntréeÉlément.add(valeur); }
    public String lire(int valeurOrdre) { return valeurEntréeÉlément.get(valeurOrdre); }
    public String remplacerValeur(int valeurOrdre, String valeur) { return valeurEntréeÉlément.set(valeurOrdre, valeur); }
    public String effacerEntréeÉlément(int valeurOrdre) { return valeurEntréeÉlément.remove(valeurOrdre); }
    public int taille() { return valeurEntréeÉlément.size(); }
    public boolean estValeurVide() { return valeurEntréeÉlément.isEmpty(); }
    public void effacerContenuContenu() { valeurEntréeÉlément.clear(); }
}
