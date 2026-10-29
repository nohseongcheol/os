// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.SVK.l_cs;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class systémové_volání {
    private systémové_volání() { }
    public static RandomAccessFile Otevřít(String cesta_2, String Režim) throws IOException {
        return new RandomAccessFile(cesta_2, Režim);
    }
    public static int Čtení(RandomAccessFile název_souboru, byte[] data) throws IOException {
        return název_souboru.read(data);
    }
    public static void Zápis(RandomAccessFile název_souboru, byte[] data) throws IOException {
        název_souboru.write(data);
    }
    public static void seek(RandomAccessFile název_souboru, long pozice) throws IOException {
        název_souboru.seek(pozice);
    }
    public static void sync(RandomAccessFile název_souboru) throws IOException {
        název_souboru.getFD().sync();
    }
    public static void Zavřené(RandomAccessFile název_souboru) throws IOException {
        název_souboru.close();
    }
    public static void Odstranit(String cesta_2) throws IOException {
        Files.delete(Paths.get(cesta_2));
    }
    public static long Velikost(String cesta_2) throws IOException {
        return Files.size(Paths.get(cesta_2));
    }
    public static Socket Připojit(String Adresa, int port) throws IOException {
        return new Socket(Adresa, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Akce) {
        Thread thread = new Thread(Akce);
        thread.start();
        return thread;
    }
    public static Process Spustit(List<String> příkaz) throws IOException {
        return new ProcessBuilder(příkaz).start();
    }
}
