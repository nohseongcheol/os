// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ITA.l_sl;
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
    public static RandomAccessFile Odpri(String POT, String Način) throws IOException {
        return new RandomAccessFile(POT, Način);
    }
    public static int Branje(RandomAccessFile Datoteka, byte[] data) throws IOException {
        return Datoteka.read(data);
    }
    public static void Pisanje(RandomAccessFile Datoteka, byte[] data) throws IOException {
        Datoteka.write(data);
    }
    public static void seek(RandomAccessFile Datoteka, long Položaj) throws IOException {
        Datoteka.seek(Položaj);
    }
    public static void sync(RandomAccessFile Datoteka) throws IOException {
        Datoteka.getFD().sync();
    }
    public static void Zapri(RandomAccessFile Datoteka) throws IOException {
        Datoteka.close();
    }
    public static void Odstrani(String POT) throws IOException {
        Files.delete(Paths.get(POT));
    }
    public static long Velikost(String POT) throws IOException {
        return Files.size(Paths.get(POT));
    }
    public static Socket Poveži(String address, int Vrata) throws IOException {
        return new Socket(address, Vrata);
    }
    public static DatagramSocket datagram(int Vrata) throws SocketException {
        return new DatagramSocket(Vrata);
    }
    public static Thread thread(Runnable Dejanje) {
        Thread thread = new Thread(Dejanje);
        thread.start();
        return thread;
    }
    public static Process Izvedi(List<String> Ukaz) throws IOException {
        return new ProcessBuilder(Ukaz).start();
    }
}
