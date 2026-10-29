// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.EST.l_et;
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
    public static RandomAccessFile Ava(String RADA, String Režiim) throws IOException {
        return new RandomAccessFile(RADA, Režiim);
    }
    public static int Lugemine(RandomAccessFile Fail, byte[] data) throws IOException {
        return Fail.read(data);
    }
    public static void Kirjutamine(RandomAccessFile Fail, byte[] data) throws IOException {
        Fail.write(data);
    }
    public static void seek(RandomAccessFile Fail, long Asukoht) throws IOException {
        Fail.seek(Asukoht);
    }
    public static void sync(RandomAccessFile Fail) throws IOException {
        Fail.getFD().sync();
    }
    public static void Suletud(RandomAccessFile Fail) throws IOException {
        Fail.close();
    }
    public static void Eemalda(String RADA) throws IOException {
        Files.delete(Paths.get(RADA));
    }
    public static long Suurus(String RADA) throws IOException {
        return Files.size(Paths.get(RADA));
    }
    public static Socket Ühendu(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Nimi) {
        Thread thread = new Thread(Nimi);
        thread.start();
        return thread;
    }
    public static Process Käivita(List<String> Käsk) throws IOException {
        return new ProcessBuilder(Käsk).start();
    }
}
