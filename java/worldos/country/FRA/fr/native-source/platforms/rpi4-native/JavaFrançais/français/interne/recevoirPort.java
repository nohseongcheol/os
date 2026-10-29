// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** Accepte les connexions TCP entrantes. */
public final class recevoirPort {
    private final java.net.ServerSocket portStandard;
    private recevoirPort(int numéroPort) throws ExceptionSortieEntrée {
        try { portStandard = new java.net.ServerSocket(numéroPort);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public static recevoirPort ouvrir(int numéroPort) throws ExceptionSortieEntrée {
        try { return new recevoirPort(numéroPort);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public Connexion recevoir() throws ExceptionSortieEntrée {
        try { return new Connexion(portStandard.accept());
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public int numéroPort() { return portStandard.getLocalPort(); }
    public void délaiExpiration(int millisecondes) throws ExceptionSortieEntrée {
        try { portStandard.setSoTimeout(millisecondes);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public boolean estFermé() { return portStandard.isClosed(); }
    public void fermer() throws ExceptionSortieEntrée {
        try { portStandard.close();
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
}
