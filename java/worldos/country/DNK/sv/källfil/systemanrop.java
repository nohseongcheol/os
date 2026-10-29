// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.DNK.l_sv;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class systemanrop {
    private systemanrop() { }
    public static RandomAccessFile Öppna(String sökväg_2, String Läge) throws IOException {
        return new RandomAccessFile(sökväg_2, Läge);
    }
    public static int Läs(RandomAccessFile filnamn, byte[] data) throws IOException {
        return filnamn.read(data);
    }
    public static void Skriv(RandomAccessFile filnamn, byte[] data) throws IOException {
        filnamn.write(data);
    }
    public static void seek(RandomAccessFile filnamn, long position) throws IOException {
        filnamn.seek(position);
    }
    public static void sync(RandomAccessFile filnamn) throws IOException {
        filnamn.getFD().sync();
    }
    public static void Stäng(RandomAccessFile filnamn) throws IOException {
        filnamn.close();
    }
    public static void Ta_bort(String sökväg_2) throws IOException {
        Files.delete(Paths.get(sökväg_2));
    }
    public static long Storlek(String sökväg_2) throws IOException {
        return Files.size(Paths.get(sökväg_2));
    }
    public static Socket Anslut(String Adress, int port) throws IOException {
        return new Socket(Adress, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Åtgärd) {
        Thread thread = new Thread(Åtgärd);
        thread.start();
        return thread;
    }
    public static Process Starta(List<String> kommando) throws IOException {
        return new ProcessBuilder(kommando).start();
    }
}
