// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** Extrémité d’un flux d’octets TCP connecté à un correspondant. */
public final class Connexion {
    private final java.net.Socket pontBibliothèqueStandard;
    Connexion(java.net.Socket pontBibliothèqueStandard) { this.pontBibliothèqueStandard = pontBibliothèqueStandard; }
    public static Connexion ouvrir(String adresse, int numéroPort) throws ExceptionSortieEntrée {
        try {
            return new Connexion(new java.net.Socket(adresse, numéroPort));
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public FluxEntrée valeurEntrée() throws ExceptionSortieEntrée {
        try { return new FluxEntrée(pontBibliothèqueStandard.getInputStream());
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public FluxSortie Sortie() throws ExceptionSortieEntrée {
        try { return new FluxSortie(pontBibliothèqueStandard.getOutputStream());
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public void délaiExpiration(int millisecondes) throws ExceptionSortieEntrée {
        try { pontBibliothèqueStandard.setSoTimeout(millisecondes);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public int numéroPort() { return pontBibliothèqueStandard.getPort(); }
    public int numéroPortLocal() { return pontBibliothèqueStandard.getLocalPort(); }
    public boolean estFermé() { return pontBibliothèqueStandard.isClosed(); }
    public boolean connecté() { return pontBibliothèqueStandard.isConnected(); }
    public void fermer() throws ExceptionSortieEntrée {
        try { pontBibliothèqueStandard.close();
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
}
