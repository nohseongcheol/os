// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ISL.l_is;
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
    public static RandomAccessFile Opna(String SLÓÐ, String Hamur) throws IOException {
        return new RandomAccessFile(SLÓÐ, Hamur);
    }
    public static int Lestur(RandomAccessFile Skrá, byte[] data) throws IOException {
        return Skrá.read(data);
    }
    public static void Skrift(RandomAccessFile Skrá, byte[] data) throws IOException {
        Skrá.write(data);
    }
    public static void seek(RandomAccessFile Skrá, long Staðsetning) throws IOException {
        Skrá.seek(Staðsetning);
    }
    public static void sync(RandomAccessFile Skrá) throws IOException {
        Skrá.getFD().sync();
    }
    public static void Loka(RandomAccessFile Skrá) throws IOException {
        Skrá.close();
    }
    public static void Fjarlægja(String SLÓÐ) throws IOException {
        Files.delete(Paths.get(SLÓÐ));
    }
    public static long Stærð(String SLÓÐ) throws IOException {
        return Files.size(Paths.get(SLÓÐ));
    }
    public static Socket Tengjast(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Aðgerð) {
        Thread thread = new Thread(Aðgerð);
        thread.start();
        return thread;
    }
    public static Process Keyra(List<String> Skipun) throws IOException {
        return new ProcessBuilder(Skipun).start();
    }
}
