// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.GRC.l_el;
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
    public static RandomAccessFile Άνοιγμα(String ΔΙΑΔΡΟΜΗ, String Κατάσταση) throws IOException {
        return new RandomAccessFile(ΔΙΑΔΡΟΜΗ, Κατάσταση);
    }
    public static int Ανάγνωση(RandomAccessFile Αρχείο, byte[] data) throws IOException {
        return Αρχείο.read(data);
    }
    public static void Εγγραφή(RandomAccessFile Αρχείο, byte[] data) throws IOException {
        Αρχείο.write(data);
    }
    public static void seek(RandomAccessFile Αρχείο, long Θέση) throws IOException {
        Αρχείο.seek(Θέση);
    }
    public static void sync(RandomAccessFile Αρχείο) throws IOException {
        Αρχείο.getFD().sync();
    }
    public static void Κλείσιμο(RandomAccessFile Αρχείο) throws IOException {
        Αρχείο.close();
    }
    public static void Αφαίρεση(String ΔΙΑΔΡΟΜΗ) throws IOException {
        Files.delete(Paths.get(ΔΙΑΔΡΟΜΗ));
    }
    public static long Μέγεθος(String ΔΙΑΔΡΟΜΗ) throws IOException {
        return Files.size(Paths.get(ΔΙΑΔΡΟΜΗ));
    }
    public static Socket Σύνδεση(String address, int Θύρα) throws IOException {
        return new Socket(address, Θύρα);
    }
    public static DatagramSocket datagram(int Θύρα) throws SocketException {
        return new DatagramSocket(Θύρα);
    }
    public static Thread thread(Runnable Ενέργεια) {
        Thread thread = new Thread(Ενέργεια);
        thread.start();
        return thread;
    }
    public static Process Εκτέλεση(List<String> Εντολή) throws IOException {
        return new ProcessBuilder(Εντολή).start();
    }
}
