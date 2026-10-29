// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.NGA.l_ig;
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
    public static RandomAccessFile Mepee(String path, String mode) throws IOException {
        return new RandomAccessFile(path, mode);
    }
    public static int Wepụta_ọzi(RandomAccessFile Faịlụ, byte[] data) throws IOException {
        return Faịlụ.read(data);
    }
    public static void Chekwaa_ozi(RandomAccessFile Faịlụ, byte[] data) throws IOException {
        Faịlụ.write(data);
    }
    public static void seek(RandomAccessFile Faịlụ, long position) throws IOException {
        Faịlụ.seek(position);
    }
    public static void sync(RandomAccessFile Faịlụ) throws IOException {
        Faịlụ.getFD().sync();
    }
    public static void Mechie(RandomAccessFile Faịlụ) throws IOException {
        Faịlụ.close();
    }
    public static void Wepụ(String path) throws IOException {
        Files.delete(Paths.get(path));
    }
    public static long Ụhara(String path) throws IOException {
        return Files.size(Paths.get(path));
    }
    public static Socket Banye(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable action) {
        Thread thread = new Thread(action);
        thread.start();
        return thread;
    }
    public static Process execute(List<String> Ntiiwu) throws IOException {
        return new ProcessBuilder(Ntiiwu).start();
    }
}
