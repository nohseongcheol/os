// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ISR.l_ml;
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
    public static RandomAccessFile തുറക്കുക(String വഴി, String രീതി) throws IOException {
        return new RandomAccessFile(വഴി, രീതി);
    }
    public static int വായന(RandomAccessFile ഫയല്, byte[] data) throws IOException {
        return ഫയല്.read(data);
    }
    public static void എഴുത്തു്(RandomAccessFile ഫയല്, byte[] data) throws IOException {
        ഫയല്.write(data);
    }
    public static void seek(RandomAccessFile ഫയല്, long സ്ഥാനം) throws IOException {
        ഫയല്.seek(സ്ഥാനം);
    }
    public static void sync(RandomAccessFile ഫയല്) throws IOException {
        ഫയല്.getFD().sync();
    }
    public static void അടയ്ക്കു(RandomAccessFile ഫയല്) throws IOException {
        ഫയല്.close();
    }
    public static void നീക്കം_ചെയ്യുക(String വഴി) throws IOException {
        Files.delete(Paths.get(വഴി));
    }
    public static long വലിപ്പം(String വഴി) throws IOException {
        return Files.size(Paths.get(വഴി));
    }
    public static Socket കണക്ടു്_ചെയ്യുക(String address, int പോര്_ട്ട്) throws IOException {
        return new Socket(address, പോര്_ട്ട്);
    }
    public static DatagramSocket datagram(int പോര്_ട്ട്) throws SocketException {
        return new DatagramSocket(പോര്_ട്ട്);
    }
    public static Thread thread(Runnable നടപടി) {
        Thread thread = new Thread(നടപടി);
        thread.start();
        return thread;
    }
    public static Process പ്രവര്_ത്തിപ്പിയ്ക്കുക(List<String> ആജ്ഞ) throws IOException {
        return new ProcessBuilder(ആജ്ഞ).start();
    }
}
