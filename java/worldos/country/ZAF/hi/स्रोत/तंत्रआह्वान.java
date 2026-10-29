// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ZAF.l_hi;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class तंत्रआह्वान {
    private तंत्रआह्वान() { }
    public static RandomAccessFile खोलें(String पथ, String विधि) throws IOException {
        return new RandomAccessFile(पथ, विधि);
    }
    public static int पढ़ें(RandomAccessFile संचिका, byte[] आँकड़े) throws IOException {
        return संचिका.read(आँकड़े);
    }
    public static void लिखें(RandomAccessFile संचिका, byte[] आँकड़े) throws IOException {
        संचिका.write(आँकड़े);
    }
    public static void स्थानबदलें(RandomAccessFile संचिका, long स्थान) throws IOException {
        संचिका.seek(स्थान);
    }
    public static void समक्रमण(RandomAccessFile संचिका) throws IOException {
        संचिका.getFD().sync();
    }
    public static void बंदकरें(RandomAccessFile संचिका) throws IOException {
        संचिका.close();
    }
    public static void हटाएँ(String पथ) throws IOException {
        Files.delete(Paths.get(पथ));
    }
    public static long आकार(String पथ) throws IOException {
        return Files.size(Paths.get(पथ));
    }
    public static Socket जोड़ना(String पता, int द्वारक्रमांक) throws IOException {
        return new Socket(पता, द्वारक्रमांक);
    }
    public static DatagramSocket स्वतंत्रसंदेश(int द्वारक्रमांक) throws SocketException {
        return new DatagramSocket(द्वारक्रमांक);
    }
    public static Thread सूत्र(Runnable क्रिया) {
        Thread सूत्र = new Thread(क्रिया);
        सूत्र.start();
        return सूत्र;
    }
    public static Process निष्पादन(List<String> आदेश) throws IOException {
        return new ProcessBuilder(आदेश).start();
    }
}
