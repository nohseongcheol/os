// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket server_VALUE = new ServerSocket(9250);
        Socket invitat_VALUE = new Socket("localhost", 9250);
        Socket Conectează = server_VALUE.accept();
        if (Conectează.getPort() != invitat_VALUE.getLocalPort() || invitat_VALUE.getPort() != Conectează.getLocalPort()) throw new RuntimeException("muta_VALUE 불일치");
        byte[] diagramă_informații = "한글 flux_VALUE".getBytes("UTF-8");
        invitat_VALUE.getOutputStream().write(diagramă_informații);
        byte[] RECEIVED_element = new byte[100];
        int lungime_VALUE = Conectează.getInputStream().read(RECEIVED_element, 0, RECEIVED_element.length);
        System.out.println(lungime_VALUE == diagramă_informații.length);
        for (int i = 0; i < lungime_VALUE; i++) if (RECEIVED_element[i] != diagramă_informații[i]) throw new RuntimeException("Conținut_VALUE 불일치");
        Conectează.getOutputStream().write(42);
        System.out.println(invitat_VALUE.getInputStream().read());
        invitat_VALUE.close();
        System.out.println(Conectează.getInputStream().read());
        Conectează.close(); server_VALUE.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("oră_VALUE 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
