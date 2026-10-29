// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.SMR.l_eo;
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
    public static RandomAccessFile Malfermu(String Vojo, String Reĝimo) throws IOException {
        return new RandomAccessFile(Vojo, Reĝimo);
    }
    public static int Lego(RandomAccessFile Dosiero, byte[] data) throws IOException {
        return Dosiero.read(data);
    }
    public static void Skribo(RandomAccessFile Dosiero, byte[] data) throws IOException {
        Dosiero.write(data);
    }
    public static void seek(RandomAccessFile Dosiero, long position) throws IOException {
        Dosiero.seek(position);
    }
    public static void sync(RandomAccessFile Dosiero) throws IOException {
        Dosiero.getFD().sync();
    }
    public static void Fermu(RandomAccessFile Dosiero) throws IOException {
        Dosiero.close();
    }
    public static void Forigi(String Vojo) throws IOException {
        Files.delete(Paths.get(Vojo));
    }
    public static long Amplekso(String Vojo) throws IOException {
        return Files.size(Paths.get(Vojo));
    }
    public static Socket Konekti(String address, int Pordo) throws IOException {
        return new Socket(address, Pordo);
    }
    public static DatagramSocket datagram(int Pordo) throws SocketException {
        return new DatagramSocket(Pordo);
    }
    public static Thread thread(Runnable Ago) {
        Thread thread = new Thread(Ago);
        thread.start();
        return thread;
    }
    public static Process Lanĉu(List<String> Komando) throws IOException {
        return new ProcessBuilder(Komando).start();
    }
}
