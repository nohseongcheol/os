// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class test_strøm {
    public static void main(String[] args) throws Exception {
        ServerSocket server_VÆRDI = new ServerSocket(9250);
        Socket gæst_VÆRDI = new Socket("localhost", 9250);
        Socket Tilslut = server_VÆRDI.accept();
        if (Tilslut.getPort() != gæst_VÆRDI.getLocalPort() || gæst_VÆRDI.getPort() != Tilslut.getLocalPort()) throw new RuntimeException("port_VÆRDI 불일치");
        byte[] datagram = "한글 strøm_VÆRDI".getBytes("UTF-8");
        gæst_VÆRDI.getOutputStream().write(datagram);
        byte[] MODTAGET_VED_UDLØB_vare = new byte[100];
        int varighed_VÆRDI = Tilslut.getInputStream().read(MODTAGET_VED_UDLØB_vare, 0, MODTAGET_VED_UDLØB_vare.length);
        System.out.println(varighed_VÆRDI == datagram.length);
        for (int i = 0; i < varighed_VÆRDI; i++) if (MODTAGET_VED_UDLØB_vare[i] != datagram[i]) throw new RuntimeException("Indhold_VÆRDI 불일치");
        Tilslut.getOutputStream().write(42);
        System.out.println(gæst_VÆRDI.getInputStream().read());
        gæst_VÆRDI.close();
        System.out.println(Tilslut.getInputStream().read());
        Tilslut.close(); server_VÆRDI.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TID_VÆRDI 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
