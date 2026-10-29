// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.EST.l_fi;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class järjestelmäkutsu {
    private järjestelmäkutsu() { }
    public static RandomAccessFile Avaa(String polku_2, String Tila) throws IOException {
        return new RandomAccessFile(polku_2, Tila);
    }
    public static int Luku(RandomAccessFile tiedoston_nimi, byte[] data) throws IOException {
        return tiedoston_nimi.read(data);
    }
    public static void Kirjoitus(RandomAccessFile tiedoston_nimi, byte[] data) throws IOException {
        tiedoston_nimi.write(data);
    }
    public static void seek(RandomAccessFile tiedoston_nimi, long paikka) throws IOException {
        tiedoston_nimi.seek(paikka);
    }
    public static void sync(RandomAccessFile tiedoston_nimi) throws IOException {
        tiedoston_nimi.getFD().sync();
    }
    public static void Sulje(RandomAccessFile tiedoston_nimi) throws IOException {
        tiedoston_nimi.close();
    }
    public static void Poista(String polku_2) throws IOException {
        Files.delete(Paths.get(polku_2));
    }
    public static long Koko(String polku_2) throws IOException {
        return Files.size(Paths.get(polku_2));
    }
    public static Socket Yhdistä(String address, int Portti) throws IOException {
        return new Socket(address, Portti);
    }
    public static DatagramSocket datagram(int Portti) throws SocketException {
        return new DatagramSocket(Portti);
    }
    public static Thread thread(Runnable Toiminto) {
        Thread thread = new Thread(Toiminto);
        thread.start();
        return thread;
    }
    public static Process Suorita(List<String> komento) throws IOException {
        return new ProcessBuilder(komento).start();
    }
}
