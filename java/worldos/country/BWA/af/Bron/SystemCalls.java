// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.BWA.l_af;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class SystemCalls {
    private SystemCalls() { }
    public static RandomAccessFile open(String Pad, String Modus) throws IOException {
        return new RandomAccessFile(Pad, Modus);
    }
    public static int Lees(RandomAccessFile Lêer, byte[] data) throws IOException {
        return Lêer.read(data);
    }
    public static void Skryf(RandomAccessFile Lêer, byte[] data) throws IOException {
        Lêer.write(data);
    }
    public static void seek(RandomAccessFile Lêer, long Posisie) throws IOException {
        Lêer.seek(Posisie);
    }
    public static void sync(RandomAccessFile Lêer) throws IOException {
        Lêer.getFD().sync();
    }
    public static void Sluit(RandomAccessFile Lêer) throws IOException {
        Lêer.close();
    }
    public static void Verwyder(String Pad) throws IOException {
        Files.delete(Paths.get(Pad));
    }
    public static long Grootte(String Pad) throws IOException {
        return Files.size(Paths.get(Pad));
    }
    public static Socket Koppel(String address, int Poort) throws IOException {
        return new Socket(address, Poort);
    }
    public static DatagramSocket datagram(int Poort) throws SocketException {
        return new DatagramSocket(Poort);
    }
    public static Thread thread(Runnable Aksie) {
        Thread thread = new Thread(Aksie);
        thread.start();
        return thread;
    }
    public static Process Voer_uit(List<String> Opdrag) throws IOException {
        return new ProcessBuilder(Opdrag).start();
    }
}
