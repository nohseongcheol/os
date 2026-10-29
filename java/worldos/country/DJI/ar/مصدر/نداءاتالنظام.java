// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.DJI.l_ar;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class نداءاتالنظام {
    private نداءاتالنظام() { }
    public static RandomAccessFile فتح(String مسار, String نمط) throws IOException {
        return new RandomAccessFile(مسار, نمط);
    }
    public static int قراءة(RandomAccessFile ملف, byte[] بيانات) throws IOException {
        return ملف.read(بيانات);
    }
    public static void كتابة(RandomAccessFile ملف, byte[] بيانات) throws IOException {
        ملف.write(بيانات);
    }
    public static void نقلالموضع(RandomAccessFile ملف, long موضع) throws IOException {
        ملف.seek(موضع);
    }
    public static void مزامنة(RandomAccessFile ملف) throws IOException {
        ملف.getFD().sync();
    }
    public static void إغلاق(RandomAccessFile ملف) throws IOException {
        ملف.close();
    }
    public static void إزالة(String مسار) throws IOException {
        Files.delete(Paths.get(مسار));
    }
    public static long حجم(String مسار) throws IOException {
        return Files.size(Paths.get(مسار));
    }
    public static Socket اتصال(String عنوان, int رقمالمنفذ) throws IOException {
        return new Socket(عنوان, رقمالمنفذ);
    }
    public static DatagramSocket رزمةمستقلة(int رقمالمنفذ) throws SocketException {
        return new DatagramSocket(رقمالمنفذ);
    }
    public static Thread خيط(Runnable إجراء) {
        Thread خيط = new Thread(إجراء);
        خيط.start();
        return خيط;
    }
    public static Process تنفيذ(List<String> أمر) throws IOException {
        return new ProcessBuilder(أمر).start();
    }
}
