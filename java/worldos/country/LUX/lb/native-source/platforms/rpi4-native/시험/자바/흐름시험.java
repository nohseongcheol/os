// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket Server_VALUE = new ServerSocket(9250);
        Socket Gaascht_VALUE = new Socket("localhost", 9250);
        Socket Verbannen = Server_VALUE.accept();
        if (Verbannen.getPort() != Gaascht_VALUE.getLocalPort() || Gaascht_VALUE.getPort() != Verbannen.getLocalPort()) throw new RuntimeException("Port_VALUE 불일치");
        byte[] 전문 = "한글 Stream_VALUE".getBytes("UTF-8");
        Gaascht_VALUE.getOutputStream().write(전문);
        byte[] RECEIVED_Element = new byte[100];
        int Längt_VALUE = Verbannen.getInputStream().read(RECEIVED_Element, 0, RECEIVED_Element.length);
        System.out.println(Längt_VALUE == 전문.length);
        for (int i = 0; i < Längt_VALUE; i++) if (RECEIVED_Element[i] != 전문[i]) throw new RuntimeException("Inhalt_VALUE 불일치");
        Verbannen.getOutputStream().write(42);
        System.out.println(Gaascht_VALUE.getInputStream().read());
        Gaascht_VALUE.close();
        System.out.println(Verbannen.getInputStream().read());
        Verbannen.close(); Server_VALUE.close();
        ServerSocket eidel_Server = new ServerSocket(9250);
        eidel_Server.setSoTimeout(10);
        try { eidel_Server.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_VALUE 제한"); }
        eidel_Server.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
