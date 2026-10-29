// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** Conserve la notion familière de fichier. Le stockage actuel repose sur des fichiers en RAM perdus au redémarrage. */
public final class Fichier {
    private Fichier() {}
    public static byte[] lireValeurOctet(String nom) throws ExceptionSortieEntrée {
        try {
        FileInputStream valeurFlux = new FileInputStream(nom);
        try {
            byte[] valeurTemporaire = new byte[16384]; int nombre = 0, valeur;
            while ((valeur = valeurFlux.read()) != -1) { if (nombre == valeurTemporaire.length) throw new ExceptionSortieEntrée("Limite de taille du fichier"); valeurTemporaire[nombre++] = (byte)valeur; }
            byte[] résultat = new byte[nombre]; System.arraycopy(valeurTemporaire, 0, résultat, 0, nombre); return résultat;
        } finally { valeurFlux.close(); }
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public static void écrireValeurOctet(String nom, byte[] valeurContenuValeur) throws ExceptionSortieEntrée {
        try {
        FileOutputStream valeurFlux = new FileOutputStream(nom);
        try { for (int indiceBoucle = 0; indiceBoucle < valeurContenuValeur.length; indiceBoucle++) valeurFlux.write(valeurContenuValeur[indiceBoucle] & 255); } finally { valeurFlux.close(); }
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public static String lire(String nom) throws ExceptionSortieEntrée {
        try { return Caractères.déchiffrerDonnées(lireValeurOctet(nom));
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public static void écrire(String nom, String valeurContenuValeur) throws ExceptionSortieEntrée {
        try { écrireValeurOctet(nom, Caractères.encoder(valeurContenuValeur));
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
}
