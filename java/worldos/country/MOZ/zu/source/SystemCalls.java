// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.MOZ.l_zu;
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
    public static RandomAccessFile Vula(String Indlela_2, String Indlela) throws IOException {
        return new RandomAccessFile(Indlela_2, Indlela);
    }
    public static int Funda(RandomAccessFile Ihele, byte[] data) throws IOException {
        return Ihele.read(data);
    }
    public static void Bhala(RandomAccessFile Ihele, byte[] data) throws IOException {
        Ihele.write(data);
    }
    public static void seek(RandomAccessFile Ihele, long position) throws IOException {
        Ihele.seek(position);
    }
    public static void sync(RandomAccessFile Ihele) throws IOException {
        Ihele.getFD().sync();
    }
    public static void Vala(RandomAccessFile Ihele) throws IOException {
        Ihele.close();
    }
    public static void Susa(String Indlela_2) throws IOException {
        Files.delete(Paths.get(Indlela_2));
    }
    public static long Ubungako(String Indlela_2) throws IOException {
        return Files.size(Paths.get(Indlela_2));
    }
    public static Socket Xhumanisa(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Isenzo) {
        Thread thread = new Thread(Isenzo);
        thread.start();
        return thread;
    }
    public static Process execute(List<String> Umlayelo) throws IOException {
        return new ProcessBuilder(Umlayelo).start();
    }
}
