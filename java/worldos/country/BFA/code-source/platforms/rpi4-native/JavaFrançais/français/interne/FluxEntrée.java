// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** Canal lisant les octets entrants dans leur ordre. */
public final class FluxEntrée {
    private final java.io.InputStream fluxStandard;
    FluxEntrée(java.io.InputStream fluxStandard) { this.fluxStandard = fluxStandard; }
    public int lire() throws ExceptionSortieEntrée {
        try { return fluxStandard.read();
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public int lire(byte[] Données) throws ExceptionSortieEntrée {
        try { return fluxStandard.read(Données);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public int lire(byte[] Données, int lancer, int longueur) throws ExceptionSortieEntrée {
        try { return fluxStandard.read(Données, lancer, longueur);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public void fermer() throws ExceptionSortieEntrée {
        try { fluxStandard.close();
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
}
