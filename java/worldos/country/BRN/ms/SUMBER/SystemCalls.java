// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.BRN.l_ms;
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
    public static RandomAccessFile Buka(String LALUAN, String Mod) throws IOException {
        return new RandomAccessFile(LALUAN, Mod);
    }
    public static int Baca(RandomAccessFile Fail, byte[] data) throws IOException {
        return Fail.read(data);
    }
    public static void Tulis(RandomAccessFile Fail, byte[] data) throws IOException {
        Fail.write(data);
    }
    public static void seek(RandomAccessFile Fail, long Kedudukan) throws IOException {
        Fail.seek(Kedudukan);
    }
    public static void sync(RandomAccessFile Fail) throws IOException {
        Fail.getFD().sync();
    }
    public static void Tutup(RandomAccessFile Fail) throws IOException {
        Fail.close();
    }
    public static void Buang(String LALUAN) throws IOException {
        Files.delete(Paths.get(LALUAN));
    }
    public static long Saiz(String LALUAN) throws IOException {
        return Files.size(Paths.get(LALUAN));
    }
    public static Socket Sambung(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Aksi) {
        Thread thread = new Thread(Aksi);
        thread.start();
        return thread;
    }
    public static Process Lakukan(List<String> Perintah) throws IOException {
        return new ProcessBuilder(Perintah).start();
    }
}
