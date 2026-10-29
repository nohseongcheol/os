// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class teszt_Stream {
    public static void main(String[] args) throws Exception {
        ServerSocket kiszolgáló_ÉRTÉK = new ServerSocket(9250);
        Socket vendég_ÉRTÉK = new Socket("localhost", 9250);
        Socket Kapcsolódás = kiszolgáló_ÉRTÉK.accept();
        if (Kapcsolódás.getPort() != vendég_ÉRTÉK.getLocalPort() || vendég_ÉRTÉK.getPort() != Kapcsolódás.getLocalPort()) throw new RuntimeException("port_ÉRTÉK 불일치");
        byte[] datagram = "한글 Stream_ÉRTÉK".getBytes("UTF-8");
        vendég_ÉRTÉK.getOutputStream().write(datagram);
        byte[] KAPOTT_cikk = new byte[100];
        int hossz_ÉRTÉK = Kapcsolódás.getInputStream().read(KAPOTT_cikk, 0, KAPOTT_cikk.length);
        System.out.println(hossz_ÉRTÉK == datagram.length);
        for (int i = 0; i < hossz_ÉRTÉK; i++) if (KAPOTT_cikk[i] != datagram[i]) throw new RuntimeException("Tartalom_ÉRTÉK 불일치");
        Kapcsolódás.getOutputStream().write(42);
        System.out.println(vendég_ÉRTÉK.getInputStream().read());
        vendég_ÉRTÉK.close();
        System.out.println(Kapcsolódás.getInputStream().read());
        Kapcsolódás.close(); kiszolgáló_ÉRTÉK.close();
        ServerSocket üres_kiszolgáló = new ServerSocket(9250);
        üres_kiszolgáló.setSoTimeout(10);
        try { üres_kiszolgáló.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("IDŐ_ÉRTÉK 제한"); }
        üres_kiszolgáló.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
