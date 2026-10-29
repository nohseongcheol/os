// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.MDG.l_mg;
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
    public static RandomAccessFile Sokafy(String LALANA, String Fomba) throws IOException {
        return new RandomAccessFile(LALANA, Fomba);
    }
    public static int Mamaky(RandomAccessFile Rakitra, byte[] data) throws IOException {
        return Rakitra.read(data);
    }
    public static void Manoratra(RandomAccessFile Rakitra, byte[] data) throws IOException {
        Rakitra.write(data);
    }
    public static void seek(RandomAccessFile Rakitra, long position) throws IOException {
        Rakitra.seek(position);
    }
    public static void sync(RandomAccessFile Rakitra) throws IOException {
        Rakitra.getFD().sync();
    }
    public static void hidio(RandomAccessFile Rakitra) throws IOException {
        Rakitra.close();
    }
    public static void Esory(String LALANA) throws IOException {
        Files.delete(Paths.get(LALANA));
    }
    public static long Habe(String LALANA) throws IOException {
        return Files.size(Paths.get(LALANA));
    }
    public static Socket Atomboy(String address, int Irika) throws IOException {
        return new Socket(address, Irika);
    }
    public static DatagramSocket datagram(int Irika) throws SocketException {
        return new DatagramSocket(Irika);
    }
    public static Thread thread(Runnable Asa) {
        Thread thread = new Thread(Asa);
        thread.start();
        return thread;
    }
    public static Process execute(List<String> Baiko) throws IOException {
        return new ProcessBuilder(Baiko).start();
    }
}
