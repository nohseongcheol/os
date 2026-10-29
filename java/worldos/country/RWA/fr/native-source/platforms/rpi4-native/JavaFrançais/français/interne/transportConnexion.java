// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
import java.net.*;
public final class transportConnexion {
    private transportConnexion() {}
    public static Connexion ouvrir(String adresse, int numéroPort) throws ExceptionSortieEntrée {
        try { return Connexion.ouvrir(adresse, numéroPort);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public static recevoirPort ouvrirRécepteur(int numéroPort) throws ExceptionSortieEntrée {
        try { return recevoirPort.ouvrir(numéroPort);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public static Socket connecter(String adresse, int valeurPort) throws ExceptionSortieEntrée {
        try { return new Socket(adresse, valeurPort);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public static ServerSocket écouterExtrémité(int valeurPort) throws ExceptionSortieEntrée {
        try { return new ServerSocket(valeurPort);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public static Socket recevoir(ServerSocket valeurServeur) throws ExceptionSortieEntrée {
        try { return valeurServeur.accept();
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
}
