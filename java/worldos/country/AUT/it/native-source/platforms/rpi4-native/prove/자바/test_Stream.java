// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class test_Stream {
    public static void main(String[] args) throws Exception {
        ServerSocket server_VALORE = new ServerSocket(9250);
        Socket guest_VALORE = new Socket("localhost", 9250);
        Socket Connetti = server_VALORE.accept();
        if (Connetti.getPort() != guest_VALORE.getLocalPort() || guest_VALORE.getPort() != Connetti.getLocalPort()) throw new RuntimeException("porta_VALORE 불일치");
        byte[] datagramma = "한글 Stream_VALORE".getBytes("UTF-8");
        guest_VALORE.getOutputStream().write(datagramma);
        byte[] RICEV_SCAD_articolo = new byte[100];
        int durata_VALORE = Connetti.getInputStream().read(RICEV_SCAD_articolo, 0, RICEV_SCAD_articolo.length);
        System.out.println(durata_VALORE == datagramma.length);
        for (int i = 0; i < durata_VALORE; i++) if (RICEV_SCAD_articolo[i] != datagramma[i]) throw new RuntimeException("Contenuto_VALORE 불일치");
        Connetti.getOutputStream().write(42);
        System.out.println(guest_VALORE.getInputStream().read());
        guest_VALORE.close();
        System.out.println(Connetti.getInputStream().read());
        Connetti.close(); server_VALORE.close();
        ServerSocket vuota_server = new ServerSocket(9250);
        vuota_server.setSoTimeout(10);
        try { vuota_server.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("valore 제한"); }
        vuota_server.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
