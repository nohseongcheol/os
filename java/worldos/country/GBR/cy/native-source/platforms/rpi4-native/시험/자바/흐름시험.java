// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket gweinydd_VALUE = new ServerSocket(9250);
        Socket gwestai_VALUE = new Socket("localhost", 9250);
        Socket Cysylltu = gweinydd_VALUE.accept();
        if (Cysylltu.getPort() != gwestai_VALUE.getLocalPort() || gwestai_VALUE.getPort() != Cysylltu.getLocalPort()) throw new RuntimeException("porth_VALUE 불일치");
        byte[] 전문 = "한글 ffrwd_VALUE".getBytes("UTF-8");
        gwestai_VALUE.getOutputStream().write(전문);
        byte[] RECEIVED_eitem = new byte[100];
        int hyd_VALUE = Cysylltu.getInputStream().read(RECEIVED_eitem, 0, RECEIVED_eitem.length);
        System.out.println(hyd_VALUE == 전문.length);
        for (int i = 0; i < hyd_VALUE; i++) if (RECEIVED_eitem[i] != 전문[i]) throw new RuntimeException("Cynnwys_VALUE 불일치");
        Cysylltu.getOutputStream().write(42);
        System.out.println(gwestai_VALUE.getInputStream().read());
        gwestai_VALUE.close();
        System.out.println(Cysylltu.getInputStream().read());
        Cysylltu.close(); gweinydd_VALUE.close();
        ServerSocket gwag_gweinydd = new ServerSocket(9250);
        gwag_gweinydd.setSoTimeout(10);
        try { gwag_gweinydd.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_VALUE 제한"); }
        gwag_gweinydd.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
