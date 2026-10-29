// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.POL.l_pl;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class wywołanie_systemowe {
    private wywołanie_systemowe() { }
    public static RandomAccessFile Otwórz(String ścieżka_2, String Tryb) throws IOException {
        return new RandomAccessFile(ścieżka_2, Tryb);
    }
    public static int Odczyt(RandomAccessFile nazwa_pliku, byte[] data) throws IOException {
        return nazwa_pliku.read(data);
    }
    public static void Zapis(RandomAccessFile nazwa_pliku, byte[] data) throws IOException {
        nazwa_pliku.write(data);
    }
    public static void seek(RandomAccessFile nazwa_pliku, long pozycja) throws IOException {
        nazwa_pliku.seek(pozycja);
    }
    public static void sync(RandomAccessFile nazwa_pliku) throws IOException {
        nazwa_pliku.getFD().sync();
    }
    public static void Zamknięte(RandomAccessFile nazwa_pliku) throws IOException {
        nazwa_pliku.close();
    }
    public static void Usuń(String ścieżka_2) throws IOException {
        Files.delete(Paths.get(ścieżka_2));
    }
    public static long Rozmiar(String ścieżka_2) throws IOException {
        return Files.size(Paths.get(ścieżka_2));
    }
    public static Socket Połącz(String Adres, int port) throws IOException {
        return new Socket(Adres, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Akcja) {
        Thread thread = new Thread(Akcja);
        thread.start();
        return thread;
    }
    public static Process Uruchom(List<String> polecenie) throws IOException {
        return new ProcessBuilder(polecenie).start();
    }
}
