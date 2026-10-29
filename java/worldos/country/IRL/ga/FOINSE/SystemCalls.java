// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IRL.l_ga;
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
    public static RandomAccessFile Oscail(String CONAIR, String Mód) throws IOException {
        return new RandomAccessFile(CONAIR, Mód);
    }
    public static int Léigh(RandomAccessFile Comhad, byte[] data) throws IOException {
        return Comhad.read(data);
    }
    public static void Scríobh(RandomAccessFile Comhad, byte[] data) throws IOException {
        Comhad.write(data);
    }
    public static void seek(RandomAccessFile Comhad, long position) throws IOException {
        Comhad.seek(position);
    }
    public static void sync(RandomAccessFile Comhad) throws IOException {
        Comhad.getFD().sync();
    }
    public static void Dún(RandomAccessFile Comhad) throws IOException {
        Comhad.close();
    }
    public static void Bain(String CONAIR) throws IOException {
        Files.delete(Paths.get(CONAIR));
    }
    public static long Méid(String CONAIR) throws IOException {
        return Files.size(Paths.get(CONAIR));
    }
    public static Socket Nasc(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Gníomh) {
        Thread thread = new Thread(Gníomh);
        thread.start();
        return thread;
    }
    public static Process Rith(List<String> Ordú) throws IOException {
        return new ProcessBuilder(Ordú).start();
    }
}
