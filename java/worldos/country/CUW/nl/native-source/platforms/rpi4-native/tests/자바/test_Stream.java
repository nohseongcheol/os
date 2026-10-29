// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class test_Stream {
    public static void main(String[] args) throws Exception {
        ServerSocket server_WAARDE = new ServerSocket(9250);
        Socket gast_WAARDE = new Socket("localhost", 9250);
        Socket Verbinden = server_WAARDE.accept();
        if (Verbinden.getPort() != gast_WAARDE.getLocalPort() || gast_WAARDE.getPort() != Verbinden.getLocalPort()) throw new RuntimeException("poort_WAARDE 불일치");
        byte[] datagram = "한글 Stream_WAARDE".getBytes("UTF-8");
        gast_WAARDE.getOutputStream().write(datagram);
        byte[] OPBRENGST_item = new byte[100];
        int tijdsduur_WAARDE = Verbinden.getInputStream().read(OPBRENGST_item, 0, OPBRENGST_item.length);
        System.out.println(tijdsduur_WAARDE == datagram.length);
        for (int i = 0; i < tijdsduur_WAARDE; i++) if (OPBRENGST_item[i] != datagram[i]) throw new RuntimeException("Inhoud_WAARDE 불일치");
        Verbinden.getOutputStream().write(42);
        System.out.println(gast_WAARDE.getInputStream().read());
        gast_WAARDE.close();
        System.out.println(Verbinden.getInputStream().read());
        Verbinden.close(); server_WAARDE.close();
        ServerSocket leeg_server = new ServerSocket(9250);
        leeg_server.setSoTimeout(10);
        try { leeg_server.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIJD_WAARDE 제한"); }
        leeg_server.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
