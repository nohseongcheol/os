// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.UKR.l_uk;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class системний_виклик {
    private системний_виклик() { }
    public static RandomAccessFile Відкрити(String шлях, String Режим) throws IOException {
        return new RandomAccessFile(шлях, Режим);
    }
    public static int Читання(RandomAccessFile файл, byte[] дані) throws IOException {
        return файл.read(дані);
    }
    public static void Запис(RandomAccessFile файл, byte[] дані) throws IOException {
        файл.write(дані);
    }
    public static void seek(RandomAccessFile файл, long позиція) throws IOException {
        файл.seek(позиція);
    }
    public static void sync(RandomAccessFile файл) throws IOException {
        файл.getFD().sync();
    }
    public static void Закрити(RandomAccessFile файл) throws IOException {
        файл.close();
    }
    public static void Вилучити(String шлях) throws IOException {
        Files.delete(Paths.get(шлях));
    }
    public static long Розмір(String шлях) throws IOException {
        return Files.size(Paths.get(шлях));
    }
    public static Socket З_єднання(String Адреса, int номерПорту) throws IOException {
        return new Socket(Адреса, номерПорту);
    }
    public static DatagramSocket datagram(int номерПорту) throws SocketException {
        return new DatagramSocket(номерПорту);
    }
    public static Thread потікВиконання(Runnable Дія) {
        Thread потікВиконання = new Thread(Дія);
        потікВиконання.start();
        return потікВиконання;
    }
    public static Process Виконати(List<String> команда) throws IOException {
        return new ProcessBuilder(команда).start();
    }
}
