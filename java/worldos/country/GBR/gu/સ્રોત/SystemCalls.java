// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.GBR.l_gu;
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
    public static RandomAccessFile ખોલો(String પથ, String સ્થિતિ) throws IOException {
        return new RandomAccessFile(પથ, સ્થિતિ);
    }
    public static int વાંચો(RandomAccessFile ફાઈલ, byte[] data) throws IOException {
        return ફાઈલ.read(data);
    }
    public static void લખો(RandomAccessFile ફાઈલ, byte[] data) throws IOException {
        ફાઈલ.write(data);
    }
    public static void seek(RandomAccessFile ફાઈલ, long સ્થાન) throws IOException {
        ફાઈલ.seek(સ્થાન);
    }
    public static void sync(RandomAccessFile ફાઈલ) throws IOException {
        ફાઈલ.getFD().sync();
    }
    public static void બંધ_કરો(RandomAccessFile ફાઈલ) throws IOException {
        ફાઈલ.close();
    }
    public static void દૂર_કરો(String પથ) throws IOException {
        Files.delete(Paths.get(પથ));
    }
    public static long માપ(String પથ) throws IOException {
        return Files.size(Paths.get(પથ));
    }
    public static Socket સંપર્ક_કરો(String address, int પોર્ટ) throws IOException {
        return new Socket(address, પોર્ટ);
    }
    public static DatagramSocket datagram(int પોર્ટ) throws SocketException {
        return new DatagramSocket(પોર્ટ);
    }
    public static Thread thread(Runnable ક્રિયા) {
        Thread thread = new Thread(ક્રિયા);
        thread.start();
        return thread;
    }
    public static Process ચલાવો(List<String> આદેશ) throws IOException {
        return new ProcessBuilder(આદેશ).start();
    }
}
