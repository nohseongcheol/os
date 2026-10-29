// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class preskusiti_tok {
    public static void main(String[] args) throws Exception {
        ServerSocket strežnik_VALUE = new ServerSocket(9250);
        Socket gost_VALUE = new Socket("localhost", 9250);
        Socket Poveži = strežnik_VALUE.accept();
        if (Poveži.getPort() != gost_VALUE.getLocalPort() || gost_VALUE.getPort() != Poveži.getLocalPort()) throw new RuntimeException("vrata_VALUE 불일치");
        byte[] datagram = "한글 tok_VALUE".getBytes("UTF-8");
        gost_VALUE.getOutputStream().write(datagram);
        byte[] RECEIVED_element = new byte[100];
        int 길이 = Poveži.getInputStream().read(RECEIVED_element, 0, RECEIVED_element.length);
        System.out.println(길이 == datagram.length);
        for (int i = 0; i < 길이; i++) if (RECEIVED_element[i] != datagram[i]) throw new RuntimeException("vsebina_VALUE 불일치");
        Poveži.getOutputStream().write(42);
        System.out.println(gost_VALUE.getInputStream().read());
        gost_VALUE.close();
        System.out.println(Poveži.getInputStream().read());
        Poveži.close(); strežnik_VALUE.close();
        ServerSocket prazen_strežnik = new ServerSocket(9250);
        prazen_strežnik.setSoTimeout(10);
        try { prazen_strežnik.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("čas_VALUE 제한"); }
        prazen_strežnik.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
