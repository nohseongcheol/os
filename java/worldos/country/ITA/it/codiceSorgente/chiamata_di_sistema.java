// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ITA.l_it;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class chiamata_di_sistema {
    private chiamata_di_sistema() { }
    public static RandomAccessFile Apri(String percorso, String Modo) throws IOException {
        return new RandomAccessFile(percorso, Modo);
    }
    public static int Lettura(RandomAccessFile file, byte[] dati) throws IOException {
        return file.read(dati);
    }
    public static void Scrittura(RandomAccessFile file, byte[] dati) throws IOException {
        file.write(dati);
    }
    public static void seek(RandomAccessFile file, long posizione) throws IOException {
        file.seek(posizione);
    }
    public static void sync(RandomAccessFile file) throws IOException {
        file.getFD().sync();
    }
    public static void Chiudi(RandomAccessFile file) throws IOException {
        file.close();
    }
    public static void Rimuovi(String percorso) throws IOException {
        Files.delete(Paths.get(percorso));
    }
    public static long Dimensione(String percorso) throws IOException {
        return Files.size(Paths.get(percorso));
    }
    public static Socket Connetti(String address, int numeroPorta) throws IOException {
        return new Socket(address, numeroPorta);
    }
    public static DatagramSocket datagram(int numeroPorta) throws SocketException {
        return new DatagramSocket(numeroPorta);
    }
    public static Thread filoEsecuzione(Runnable Azione) {
        Thread filoEsecuzione = new Thread(Azione);
        filoEsecuzione.start();
        return filoEsecuzione;
    }
    public static Process Esegui(List<String> comando) throws IOException {
        return new ProcessBuilder(comando).start();
    }
}
