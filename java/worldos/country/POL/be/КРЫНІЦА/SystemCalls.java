// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.POL.l_be;
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
    public static RandomAccessFile Адкрыць(String ШЛЯХ, String Рэжым) throws IOException {
        return new RandomAccessFile(ШЛЯХ, Рэжым);
    }
    public static int Чытанне(RandomAccessFile Файл, byte[] data) throws IOException {
        return Файл.read(data);
    }
    public static void Запіс(RandomAccessFile Файл, byte[] data) throws IOException {
        Файл.write(data);
    }
    public static void seek(RandomAccessFile Файл, long Пазіцыя) throws IOException {
        Файл.seek(Пазіцыя);
    }
    public static void sync(RandomAccessFile Файл) throws IOException {
        Файл.getFD().sync();
    }
    public static void Закрыць(RandomAccessFile Файл) throws IOException {
        Файл.close();
    }
    public static void Выдаліць(String ШЛЯХ) throws IOException {
        Files.delete(Paths.get(ШЛЯХ));
    }
    public static long Памер(String ШЛЯХ) throws IOException {
        return Files.size(Paths.get(ШЛЯХ));
    }
    public static Socket Злучыцца(String address, int Порт) throws IOException {
        return new Socket(address, Порт);
    }
    public static DatagramSocket datagram(int Порт) throws SocketException {
        return new DatagramSocket(Порт);
    }
    public static Thread thread(Runnable Дзеянне) {
        Thread thread = new Thread(Дзеянне);
        thread.start();
        return thread;
    }
    public static Process Выкананне(List<String> Загад) throws IOException {
        return new ProcessBuilder(Загад).start();
    }
}
