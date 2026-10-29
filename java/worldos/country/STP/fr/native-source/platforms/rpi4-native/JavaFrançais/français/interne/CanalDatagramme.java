// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** Extrémité d’envoi et de réception des datagrammes UDP, conservant les limites des messages. */
public final class CanalDatagramme {
    private final java.net.DatagramSocket extrémitéStandard;
    private CanalDatagramme(int numéroPort) throws ExceptionSortieEntrée {
        try { extrémitéStandard = Communication.ouvrir(numéroPort);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public static CanalDatagramme ouvrir(int numéroPort) throws ExceptionSortieEntrée {
        try { return new CanalDatagramme(numéroPort);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public void envoyer(String adresse, int numéroPort, String Données) throws ExceptionSortieEntrée {
        try { Communication.envoyer(extrémitéStandard, adresse, numéroPort, Données);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public String recevoir() throws ExceptionSortieEntrée {
        try { return Communication.recevoir(extrémitéStandard);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public void délaiExpiration(int millisecondes) throws ExceptionSortieEntrée {
        try { Communication.délaiExpiration(extrémitéStandard, millisecondes);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public int numéroPort() { return extrémitéStandard.getLocalPort(); }
    public boolean estFermé() { return extrémitéStandard.isClosed(); }
    public void fermer() { Communication.fermer(extrémitéStandard); }
}
