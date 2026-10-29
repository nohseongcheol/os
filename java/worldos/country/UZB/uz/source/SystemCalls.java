// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.UZB.l_uz;
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
    public static RandomAccessFile Ochish(String path, String Rejim) throws IOException {
        return new RandomAccessFile(path, Rejim);
    }
    public static int Oʻqish(RandomAccessFile Fayl, byte[] data) throws IOException {
        return Fayl.read(data);
    }
    public static void Yozish(RandomAccessFile Fayl, byte[] data) throws IOException {
        Fayl.write(data);
    }
    public static void seek(RandomAccessFile Fayl, long Holati) throws IOException {
        Fayl.seek(Holati);
    }
    public static void sync(RandomAccessFile Fayl) throws IOException {
        Fayl.getFD().sync();
    }
    public static void Yopish(RandomAccessFile Fayl) throws IOException {
        Fayl.close();
    }
    public static void Olib_tashlash(String path) throws IOException {
        Files.delete(Paths.get(path));
    }
    public static long Hajmi(String path) throws IOException {
        return Files.size(Paths.get(path));
    }
    public static Socket Ulanish(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Amal) {
        Thread thread = new Thread(Amal);
        thread.start();
        return thread;
    }
    public static Process Ishga_tushirish(List<String> Buyruq) throws IOException {
        return new ProcessBuilder(Buyruq).start();
    }
}
