// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.MAR.l_fr;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class AppelsSystème {
    private AppelsSystème() { }
    public static RandomAccessFile ouvrir(String chemin, String mode) throws IOException {
        return new RandomAccessFile(chemin, mode);
    }
    public static int lire(RandomAccessFile fichier, byte[] données) throws IOException {
        return fichier.read(données);
    }
    public static void écrire(RandomAccessFile fichier, byte[] données) throws IOException {
        fichier.write(données);
    }
    public static void positionner(RandomAccessFile fichier, long position) throws IOException {
        fichier.seek(position);
    }
    public static void synchroniser(RandomAccessFile fichier) throws IOException {
        fichier.getFD().sync();
    }
    public static void fermer(RandomAccessFile fichier) throws IOException {
        fichier.close();
    }
    public static void supprimer(String chemin) throws IOException {
        Files.delete(Paths.get(chemin));
    }
    public static long taille(String chemin) throws IOException {
        return Files.size(Paths.get(chemin));
    }
    public static Socket connecter(String adresse, int numéroPort) throws IOException {
        return new Socket(adresse, numéroPort);
    }
    public static DatagramSocket datagramme(int numéroPort) throws SocketException {
        return new DatagramSocket(numéroPort);
    }
    public static Thread fil(Runnable action) {
        Thread fil = new Thread(action);
        fil.start();
        return fil;
    }
    public static Process exécuter(List<String> commande) throws IOException {
        return new ProcessBuilder(commande).start();
    }
}
