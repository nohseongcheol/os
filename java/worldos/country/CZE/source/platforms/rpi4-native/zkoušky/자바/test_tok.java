// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class test_tok {
    public static void main(String[] args) throws Exception {
        ServerSocket server_HODNOTA = new ServerSocket(9250);
        Socket host_HODNOTA = new Socket("localhost", 9250);
        Socket Připojit = server_HODNOTA.accept();
        if (Připojit.getPort() != host_HODNOTA.getLocalPort() || host_HODNOTA.getPort() != Připojit.getLocalPort()) throw new RuntimeException("port_HODNOTA 불일치");
        byte[] datagram = "한글 tok_HODNOTA".getBytes("UTF-8");
        host_HODNOTA.getOutputStream().write(datagram);
        byte[] RECEIVED_zboží = new byte[100];
        int délka_HODNOTA = Připojit.getInputStream().read(RECEIVED_zboží, 0, RECEIVED_zboží.length);
        System.out.println(délka_HODNOTA == datagram.length);
        for (int i = 0; i < délka_HODNOTA; i++) if (RECEIVED_zboží[i] != datagram[i]) throw new RuntimeException("Obsah_HODNOTA 불일치");
        Připojit.getOutputStream().write(42);
        System.out.println(host_HODNOTA.getInputStream().read());
        host_HODNOTA.close();
        System.out.println(Připojit.getInputStream().read());
        Připojit.close(); server_HODNOTA.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("časová_hodnota 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
