// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** Canal écrivant les octets sortants dans leur ordre. */
public final class FluxSortie {
    private final java.io.OutputStream fluxStandard;
    FluxSortie(java.io.OutputStream fluxStandard) { this.fluxStandard = fluxStandard; }
    public void écrire(int valeur) throws ExceptionSortieEntrée {
        try { fluxStandard.write(valeur);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public void écrire(byte[] Données) throws ExceptionSortieEntrée {
        try { fluxStandard.write(Données);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public void écrire(byte[] Données, int lancer, int longueur) throws ExceptionSortieEntrée {
        try { fluxStandard.write(Données, lancer, longueur);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public void émettreValeur() throws ExceptionSortieEntrée {
        try { fluxStandard.flush();
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public void fermer() throws ExceptionSortieEntrée {
        try { fluxStandard.close();
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
}
