// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class test_strøm {
    public static void main(String[] args) throws Exception {
        ServerSocket server_VERDI = new ServerSocket(9250);
        Socket gjest_VERDI = new Socket("localhost", 9250);
        Socket Koble_til = server_VERDI.accept();
        if (Koble_til.getPort() != gjest_VERDI.getLocalPort() || gjest_VERDI.getPort() != Koble_til.getLocalPort()) throw new RuntimeException("port_VERDI 불일치");
        byte[] datagram = "한글 strøm_VERDI".getBytes("UTF-8");
        gjest_VERDI.getOutputStream().write(datagram);
        byte[] MOTTATT_AVKAST_vare = new byte[100];
        int lengde_VERDI = Koble_til.getInputStream().read(MOTTATT_AVKAST_vare, 0, MOTTATT_AVKAST_vare.length);
        System.out.println(lengde_VERDI == datagram.length);
        for (int i = 0; i < lengde_VERDI; i++) if (MOTTATT_AVKAST_vare[i] != datagram[i]) throw new RuntimeException("Innhold_VERDI 불일치");
        Koble_til.getOutputStream().write(42);
        System.out.println(gjest_VERDI.getInputStream().read());
        gjest_VERDI.close();
        System.out.println(Koble_til.getInputStream().read());
        Koble_til.close(); server_VERDI.close();
        ServerSocket tom_server = new ServerSocket(9250);
        tom_server.setSoTimeout(10);
        try { tom_server.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TID_VERDI 제한"); }
        tom_server.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
