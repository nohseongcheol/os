// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.BEL.l_wa;
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
    public static RandomAccessFile Drovi(String Tchimin, String Môde) throws IOException {
        return new RandomAccessFile(Tchimin, Môde);
    }
    public static int Lére(RandomAccessFile Fitchî, byte[] data) throws IOException {
        return Fitchî.read(data);
    }
    public static void Sicrire(RandomAccessFile Fitchî, byte[] data) throws IOException {
        Fitchî.write(data);
    }
    public static void seek(RandomAccessFile Fitchî, long position) throws IOException {
        Fitchî.seek(position);
    }
    public static void sync(RandomAccessFile Fitchî) throws IOException {
        Fitchî.getFD().sync();
    }
    public static void Clôre(RandomAccessFile Fitchî) throws IOException {
        Fitchî.close();
    }
    public static void Oister(String Tchimin) throws IOException {
        Files.delete(Paths.get(Tchimin));
    }
    public static long Grandeu(String Tchimin) throws IOException {
        return Files.size(Paths.get(Tchimin));
    }
    public static Socket Raloyî(String address, int Pôrt) throws IOException {
        return new Socket(address, Pôrt);
    }
    public static DatagramSocket datagram(int Pôrt) throws SocketException {
        return new DatagramSocket(Pôrt);
    }
    public static Thread thread(Runnable Accion) {
        Thread thread = new Thread(Accion);
        thread.start();
        return thread;
    }
    public static Process Enonder(List<String> Comande) throws IOException {
        return new ProcessBuilder(Comande).start();
    }
}
