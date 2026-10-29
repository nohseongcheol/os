// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.AZE.l_ku;
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
    public static RandomAccessFile Veke(String RÊ, String Mod) throws IOException {
        return new RandomAccessFile(RÊ, Mod);
    }
    public static int Bixwîne(RandomAccessFile Pel, byte[] data) throws IOException {
        return Pel.read(data);
    }
    public static void Binivîse(RandomAccessFile Pel, byte[] data) throws IOException {
        Pel.write(data);
    }
    public static void seek(RandomAccessFile Pel, long Cih) throws IOException {
        Pel.seek(Cih);
    }
    public static void sync(RandomAccessFile Pel) throws IOException {
        Pel.getFD().sync();
    }
    public static void Bigire(RandomAccessFile Pel) throws IOException {
        Pel.close();
    }
    public static void Rake(String RÊ) throws IOException {
        Files.delete(Paths.get(RÊ));
    }
    public static long Mezinahî(String RÊ) throws IOException {
        return Files.size(Paths.get(RÊ));
    }
    public static Socket Girêbide(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Çalakî) {
        Thread thread = new Thread(Çalakî);
        thread.start();
        return thread;
    }
    public static Process Bixebitîne(List<String> Ferman) throws IOException {
        return new ProcessBuilder(Ferman).start();
    }
}
