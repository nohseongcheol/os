// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ISR.l_he;
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
    public static RandomAccessFile פתח(String נתיב, String מצב) throws IOException {
        return new RandomAccessFile(נתיב, מצב);
    }
    public static int קרא(RandomAccessFile קובץ, byte[] נתונים) throws IOException {
        return קובץ.read(נתונים);
    }
    public static void כתוב(RandomAccessFile קובץ, byte[] נתונים) throws IOException {
        קובץ.write(נתונים);
    }
    public static void seek(RandomAccessFile קובץ, long מיקום) throws IOException {
        קובץ.seek(מיקום);
    }
    public static void sync(RandomAccessFile קובץ) throws IOException {
        קובץ.getFD().sync();
    }
    public static void סגירה(RandomAccessFile קובץ) throws IOException {
        קובץ.close();
    }
    public static void הסר(String נתיב) throws IOException {
        Files.delete(Paths.get(נתיב));
    }
    public static long גודל(String נתיב) throws IOException {
        return Files.size(Paths.get(נתיב));
    }
    public static Socket חיבור(String address, int מספרשער) throws IOException {
        return new Socket(address, מספרשער);
    }
    public static DatagramSocket datagram(int מספרשער) throws SocketException {
        return new DatagramSocket(מספרשער);
    }
    public static Thread תהליכון(Runnable פעולה) {
        Thread תהליכון = new Thread(פעולה);
        תהליכון.start();
        return תהליכון;
    }
    public static Process בצע(List<String> פקודה) throws IOException {
        return new ProcessBuilder(פקודה).start();
    }
}
