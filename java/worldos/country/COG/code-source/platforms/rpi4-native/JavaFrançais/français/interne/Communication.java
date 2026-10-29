// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** Communication par datagrammes IPv4 UDP. Les correspondants externes utilisent des adresses numériques. */
public final class Communication {
    private Communication() {}
    public static DatagramSocket ouvrir(int valeurPort) throws ExceptionSortieEntrée {
        try { return new DatagramSocket(valeurPort);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public static void envoyer(DatagramSocket extrémité, int valeurPort, String valeurContenuValeur) throws ExceptionSortieEntrée {
        try {
        envoyer(extrémité, "127.0.0.1", valeurPort, valeurContenuValeur);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public static void envoyer(DatagramSocket extrémité, String adresse, int valeurPort, String valeurContenuValeur) throws ExceptionSortieEntrée {
        try {
        byte[] valeurOctet = Caractères.encoder(valeurContenuValeur);
        extrémité.send(new DatagramPacket(valeurOctet, valeurOctet.length, InetAddress.getByName(adresse), valeurPort));
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public static String recevoir(DatagramSocket extrémité) throws ExceptionSortieEntrée {
        try {
        byte[] valeurOctet = new byte[512]; DatagramPacket datagramme = new DatagramPacket(valeurOctet, valeurOctet.length); extrémité.receive(datagramme);
        byte[] résultat = new byte[datagramme.getLength()]; System.arraycopy(valeurOctet, 0, résultat, 0, résultat.length); return Caractères.déchiffrerDonnées(résultat);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public static void délaiExpiration(DatagramSocket extrémité, int millisecondes) throws ExceptionSortieEntrée {
        try { extrémité.setSoTimeout(millisecondes);
        } catch (java.io.IOException erreur) { throw convertirException.sortieEntrée(erreur); }
        catch (RuntimeException erreur) { throw convertirException.exécuterCommande(erreur); }
    }
    public static void fermer(DatagramSocket extrémité) { extrémité.close(); }
}
