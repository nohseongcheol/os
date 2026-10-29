// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.EST.l_ru;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class системный_вызов {
    private системный_вызов() { }
    public static RandomAccessFile Открыть(String путь, String Режим) throws IOException {
        return new RandomAccessFile(путь, Режим);
    }
    public static int Чтение(RandomAccessFile файл, byte[] данные) throws IOException {
        return файл.read(данные);
    }
    public static void Запись(RandomAccessFile файл, byte[] данные) throws IOException {
        файл.write(данные);
    }
    public static void seek(RandomAccessFile файл, long позиция) throws IOException {
        файл.seek(позиция);
    }
    public static void sync(RandomAccessFile файл) throws IOException {
        файл.getFD().sync();
    }
    public static void Закрыть(RandomAccessFile файл) throws IOException {
        файл.close();
    }
    public static void Удалить(String путь) throws IOException {
        Files.delete(Paths.get(путь));
    }
    public static long Размер(String путь) throws IOException {
        return Files.size(Paths.get(путь));
    }
    public static Socket Подключить(String address, int номерПорта) throws IOException {
        return new Socket(address, номерПорта);
    }
    public static DatagramSocket datagram(int номерПорта) throws SocketException {
        return new DatagramSocket(номерПорта);
    }
    public static Thread потокВыполнения(Runnable Действие) {
        Thread потокВыполнения = new Thread(Действие);
        потокВыполнения.start();
        return потокВыполнения;
    }
    public static Process Выполнить(List<String> команда) throws IOException {
        return new ProcessBuilder(команда).start();
    }
}
