// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.KGZ.l_ky;
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
    public static RandomAccessFile Ачуу(String ЖОЛ, String Режим) throws IOException {
        return new RandomAccessFile(ЖОЛ, Режим);
    }
    public static int Окуу(RandomAccessFile Файл, byte[] data) throws IOException {
        return Файл.read(data);
    }
    public static void Жазуу(RandomAccessFile Файл, byte[] data) throws IOException {
        Файл.write(data);
    }
    public static void seek(RandomAccessFile Файл, long Турган_жери) throws IOException {
        Файл.seek(Турган_жери);
    }
    public static void sync(RandomAccessFile Файл) throws IOException {
        Файл.getFD().sync();
    }
    public static void Жабуу(RandomAccessFile Файл) throws IOException {
        Файл.close();
    }
    public static void Өчүрүү(String ЖОЛ) throws IOException {
        Files.delete(Paths.get(ЖОЛ));
    }
    public static long Өлчөмү(String ЖОЛ) throws IOException {
        return Files.size(Paths.get(ЖОЛ));
    }
    public static Socket Туташуу(String address, int Порт) throws IOException {
        return new Socket(address, Порт);
    }
    public static DatagramSocket datagram(int Порт) throws SocketException {
        return new DatagramSocket(Порт);
    }
    public static Thread thread(Runnable Аракети) {
        Thread thread = new Thread(Аракети);
        thread.start();
        return thread;
    }
    public static Process execute(List<String> Команда) throws IOException {
        return new ProcessBuilder(Команда).start();
    }
}
