// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.LVA.l_lv;
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
    public static RandomAccessFile Atvērt(String CEĻŠ, String Režīms) throws IOException {
        return new RandomAccessFile(CEĻŠ, Režīms);
    }
    public static int Lasīt(RandomAccessFile Fails, byte[] data) throws IOException {
        return Fails.read(data);
    }
    public static void Rakstīt(RandomAccessFile Fails, byte[] data) throws IOException {
        Fails.write(data);
    }
    public static void seek(RandomAccessFile Fails, long Novietojums) throws IOException {
        Fails.seek(Novietojums);
    }
    public static void sync(RandomAccessFile Fails) throws IOException {
        Fails.getFD().sync();
    }
    public static void Aizvērt(RandomAccessFile Fails) throws IOException {
        Fails.close();
    }
    public static void Aizvākt(String CEĻŠ) throws IOException {
        Files.delete(Paths.get(CEĻŠ));
    }
    public static long Izmērs(String CEĻŠ) throws IOException {
        return Files.size(Paths.get(CEĻŠ));
    }
    public static Socket Savienoties(String address, int Ports) throws IOException {
        return new Socket(address, Ports);
    }
    public static DatagramSocket datagram(int Ports) throws SocketException {
        return new DatagramSocket(Ports);
    }
    public static Thread thread(Runnable Darbība) {
        Thread thread = new Thread(Darbība);
        thread.start();
        return thread;
    }
    public static Process Izpildīt(List<String> Komanda) throws IOException {
        return new ProcessBuilder(Komanda).start();
    }
}
