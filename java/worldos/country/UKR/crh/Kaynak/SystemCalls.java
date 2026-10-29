// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.UKR.l_crh;
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
    public static RandomAccessFile Aç(String Yolçıq, String Tarz) throws IOException {
        return new RandomAccessFile(Yolçıq, Tarz);
    }
    public static int Okuma(RandomAccessFile Dosya, byte[] data) throws IOException {
        return Dosya.read(data);
    }
    public static void Yazma(RandomAccessFile Dosya, byte[] data) throws IOException {
        Dosya.write(data);
    }
    public static void seek(RandomAccessFile Dosya, long position) throws IOException {
        Dosya.seek(position);
    }
    public static void sync(RandomAccessFile Dosya) throws IOException {
        Dosya.getFD().sync();
    }
    public static void Qapat(RandomAccessFile Dosya) throws IOException {
        Dosya.close();
    }
    public static void Çetlet(String Yolçıq) throws IOException {
        Files.delete(Paths.get(Yolçıq));
    }
    public static long Boyut(String Yolçıq) throws IOException {
        return Files.size(Paths.get(Yolçıq));
    }
    public static Socket Bağlan(String address, int Kapı) throws IOException {
        return new Socket(address, Kapı);
    }
    public static DatagramSocket datagram(int Kapı) throws SocketException {
        return new DatagramSocket(Kapı);
    }
    public static Thread thread(Runnable Amel) {
        Thread thread = new Thread(Amel);
        thread.start();
        return thread;
    }
    public static Process İcra_et(List<String> Komut) throws IOException {
        return new ProcessBuilder(Komut).start();
    }
}
