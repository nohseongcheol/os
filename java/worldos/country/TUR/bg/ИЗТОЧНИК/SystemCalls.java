// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.TUR.l_bg;
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
    public static RandomAccessFile Отваряне(String ПЪТ, String Режим) throws IOException {
        return new RandomAccessFile(ПЪТ, Режим);
    }
    public static int Четене(RandomAccessFile Файл, byte[] data) throws IOException {
        return Файл.read(data);
    }
    public static void Писане(RandomAccessFile Файл, byte[] data) throws IOException {
        Файл.write(data);
    }
    public static void seek(RandomAccessFile Файл, long Позиция) throws IOException {
        Файл.seek(Позиция);
    }
    public static void sync(RandomAccessFile Файл) throws IOException {
        Файл.getFD().sync();
    }
    public static void Затворен(RandomAccessFile Файл) throws IOException {
        Файл.close();
    }
    public static void Премахване(String ПЪТ) throws IOException {
        Files.delete(Paths.get(ПЪТ));
    }
    public static long Размер(String ПЪТ) throws IOException {
        return Files.size(Paths.get(ПЪТ));
    }
    public static Socket Свързване(String address, int Порт) throws IOException {
        return new Socket(address, Порт);
    }
    public static DatagramSocket datagram(int Порт) throws SocketException {
        return new DatagramSocket(Порт);
    }
    public static Thread thread(Runnable Операция) {
        Thread thread = new Thread(Операция);
        thread.start();
        return thread;
    }
    public static Process Изпълнение(List<String> Команда) throws IOException {
        return new ProcessBuilder(Команда).start();
    }
}
