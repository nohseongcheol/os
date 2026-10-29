// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.TUR.l_az;
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
    public static RandomAccessFile Aç(String Cığır, String Mod) throws IOException {
        return new RandomAccessFile(Cığır, Mod);
    }
    public static int Oxuma(RandomAccessFile FAYL, byte[] data) throws IOException {
        return FAYL.read(data);
    }
    public static void Yazma(RandomAccessFile FAYL, byte[] data) throws IOException {
        FAYL.write(data);
    }
    public static void seek(RandomAccessFile FAYL, long position) throws IOException {
        FAYL.seek(position);
    }
    public static void sync(RandomAccessFile FAYL) throws IOException {
        FAYL.getFD().sync();
    }
    public static void Bağla(RandomAccessFile FAYL) throws IOException {
        FAYL.close();
    }
    public static void Çıxart(String Cığır) throws IOException {
        Files.delete(Paths.get(Cığır));
    }
    public static long Böyüklük(String Cığır) throws IOException {
        return Files.size(Paths.get(Cığır));
    }
    public static Socket Bağlan(String address, int Qapı) throws IOException {
        return new Socket(address, Qapı);
    }
    public static DatagramSocket datagram(int Qapı) throws SocketException {
        return new DatagramSocket(Qapı);
    }
    public static Thread thread(Runnable Gedişat) {
        Thread thread = new Thread(Gedişat);
        thread.start();
        return thread;
    }
    public static Process execute(List<String> Əmr) throws IOException {
        return new ProcessBuilder(Əmr).start();
    }
}
