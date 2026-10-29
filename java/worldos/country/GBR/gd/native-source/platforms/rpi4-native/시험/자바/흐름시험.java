// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket frithealaiche_VALUE = new ServerSocket(9250);
        Socket aoigh_VALUE = new Socket("localhost", 9250);
        Socket CONNECT = frithealaiche_VALUE.accept();
        if (CONNECT.getPort() != aoigh_VALUE.getLocalPort() || aoigh_VALUE.getPort() != CONNECT.getLocalPort()) throw new RuntimeException("port_VALUE 불일치");
        byte[] 전문 = "한글 sruth_VALUE".getBytes("UTF-8");
        aoigh_VALUE.getOutputStream().write(전문);
        byte[] RECEIVED_nì = new byte[100];
        int faid_VALUE = CONNECT.getInputStream().read(RECEIVED_nì, 0, RECEIVED_nì.length);
        System.out.println(faid_VALUE == 전문.length);
        for (int i = 0; i < faid_VALUE; i++) if (RECEIVED_nì[i] != 전문[i]) throw new RuntimeException("susbaint_VALUE 불일치");
        CONNECT.getOutputStream().write(42);
        System.out.println(aoigh_VALUE.getInputStream().read());
        aoigh_VALUE.close();
        System.out.println(CONNECT.getInputStream().read());
        CONNECT.close(); frithealaiche_VALUE.close();
        ServerSocket falamh_frithealaiche = new ServerSocket(9250);
        falamh_frithealaiche.setSoTimeout(10);
        try { falamh_frithealaiche.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_VALUE 제한"); }
        falamh_frithealaiche.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
