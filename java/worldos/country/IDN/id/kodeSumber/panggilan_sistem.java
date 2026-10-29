// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IDN.l_id;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class panggilan_sistem {
    private panggilan_sistem() { }
    public static RandomAccessFile Buka(String jalur, String mode) throws IOException {
        return new RandomAccessFile(jalur, mode);
    }
    public static int Baca(RandomAccessFile berkas, byte[] data) throws IOException {
        return berkas.read(data);
    }
    public static void Tulis(RandomAccessFile berkas, byte[] data) throws IOException {
        berkas.write(data);
    }
    public static void seek(RandomAccessFile berkas, long posisi) throws IOException {
        berkas.seek(posisi);
    }
    public static void sync(RandomAccessFile berkas) throws IOException {
        berkas.getFD().sync();
    }
    public static void Tutup(RandomAccessFile berkas) throws IOException {
        berkas.close();
    }
    public static void Hapus(String jalur) throws IOException {
        Files.delete(Paths.get(jalur));
    }
    public static long Ukuran(String jalur) throws IOException {
        return Files.size(Paths.get(jalur));
    }
    public static Socket Sambung(String address, int nomorPort) throws IOException {
        return new Socket(address, nomorPort);
    }
    public static DatagramSocket datagram(int nomorPort) throws SocketException {
        return new DatagramSocket(nomorPort);
    }
    public static Thread utasEksekusi(Runnable Aksi) {
        Thread utasEksekusi = new Thread(Aksi);
        utasEksekusi.start();
        return utasEksekusi;
    }
    public static Process Eksekusi(List<String> perintah) throws IOException {
        return new ProcessBuilder(perintah).start();
    }
}
