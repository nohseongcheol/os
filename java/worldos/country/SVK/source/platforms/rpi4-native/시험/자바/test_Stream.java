// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class test_Stream {
    public static void main(String[] args) throws Exception {
        ServerSocket server_VALUE = new ServerSocket(9250);
        Socket hosť_VALUE = new Socket("localhost", 9250);
        Socket Pripojiť = server_VALUE.accept();
        if (Pripojiť.getPort() != hosť_VALUE.getLocalPort() || hosť_VALUE.getPort() != Pripojiť.getLocalPort()) throw new RuntimeException("port_VALUE 불일치");
        byte[] datagram = "한글 Stream_VALUE".getBytes("UTF-8");
        hosť_VALUE.getOutputStream().write(datagram);
        byte[] RECEIVED_položka = new byte[100];
        int dĺžka_VALUE = Pripojiť.getInputStream().read(RECEIVED_položka, 0, RECEIVED_položka.length);
        System.out.println(dĺžka_VALUE == datagram.length);
        for (int i = 0; i < dĺžka_VALUE; i++) if (RECEIVED_položka[i] != datagram[i]) throw new RuntimeException("obsah_VALUE 불일치");
        Pripojiť.getOutputStream().write(42);
        System.out.println(hosť_VALUE.getInputStream().read());
        hosť_VALUE.close();
        System.out.println(Pripojiť.getInputStream().read());
        Pripojiť.close(); server_VALUE.close();
        ServerSocket prázdny_server = new ServerSocket(9250);
        prázdny_server.setSoTimeout(10);
        try { prázdny_server.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("čas_VALUE 제한"); }
        prázdny_server.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
