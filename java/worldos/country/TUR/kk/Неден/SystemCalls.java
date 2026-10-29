// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.TUR.l_kk;
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
    public static RandomAccessFile Ашу(String Жол_2, String Режимі) throws IOException {
        return new RandomAccessFile(Жол_2, Режимі);
    }
    public static int Оқу(RandomAccessFile Файл, byte[] data) throws IOException {
        return Файл.read(data);
    }
    public static void Жазу(RandomAccessFile Файл, byte[] data) throws IOException {
        Файл.write(data);
    }
    public static void seek(RandomAccessFile Файл, long Орны) throws IOException {
        Файл.seek(Орны);
    }
    public static void sync(RandomAccessFile Файл) throws IOException {
        Файл.getFD().sync();
    }
    public static void Жабу(RandomAccessFile Файл) throws IOException {
        Файл.close();
    }
    public static void Өшіру(String Жол_2) throws IOException {
        Files.delete(Paths.get(Жол_2));
    }
    public static long Өлшемі(String Жол_2) throws IOException {
        return Files.size(Paths.get(Жол_2));
    }
    public static Socket Байланысу(String address, int Порт) throws IOException {
        return new Socket(address, Порт);
    }
    public static DatagramSocket datagram(int Порт) throws SocketException {
        return new DatagramSocket(Порт);
    }
    public static Thread thread(Runnable Әрекет) {
        Thread thread = new Thread(Әрекет);
        thread.start();
        return thread;
    }
    public static Process Орындау(List<String> Команда) throws IOException {
        return new ProcessBuilder(Команда).start();
    }
}
