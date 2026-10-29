// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ZAF.l_nso;
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
    public static RandomAccessFile Bula(String Tsejana, String Mokgwa) throws IOException {
        return new RandomAccessFile(Tsejana, Mokgwa);
    }
    public static int Bala(RandomAccessFile Faele, byte[] data) throws IOException {
        return Faele.read(data);
    }
    public static void Ngwala(RandomAccessFile Faele, byte[] data) throws IOException {
        Faele.write(data);
    }
    public static void seek(RandomAccessFile Faele, long position) throws IOException {
        Faele.seek(position);
    }
    public static void sync(RandomAccessFile Faele) throws IOException {
        Faele.getFD().sync();
    }
    public static void Tswalela(RandomAccessFile Faele) throws IOException {
        Faele.close();
    }
    public static void Tloša(String Tsejana) throws IOException {
        Files.delete(Paths.get(Tsejana));
    }
    public static long Bogolo(String Tsejana) throws IOException {
        return Files.size(Paths.get(Tsejana));
    }
    public static Socket Ikgokaganye(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Mogato) {
        Thread thread = new Thread(Mogato);
        thread.start();
        return thread;
    }
    public static Process execute(List<String> Taelo) throws IOException {
        return new ProcessBuilder(Taelo).start();
    }
}
