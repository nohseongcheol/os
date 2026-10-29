// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket server_VALUE = new ServerSocket(9250);
        Socket i_ftuar_VALUE = new Socket("localhost", 9250);
        Socket Lidhu = server_VALUE.accept();
        if (Lidhu.getPort() != i_ftuar_VALUE.getLocalPort() || i_ftuar_VALUE.getPort() != Lidhu.getLocalPort()) throw new RuntimeException("portë_VALUE 불일치");
        byte[] 전문 = "한글 Stream_VALUE".getBytes("UTF-8");
        i_ftuar_VALUE.getOutputStream().write(전문);
        byte[] RECEIVED_njësi = new byte[100];
        int gjatësi_VALUE = Lidhu.getInputStream().read(RECEIVED_njësi, 0, RECEIVED_njësi.length);
        System.out.println(gjatësi_VALUE == 전문.length);
        for (int i = 0; i < gjatësi_VALUE; i++) if (RECEIVED_njësi[i] != 전문[i]) throw new RuntimeException("Përmbajtje_VALUE 불일치");
        Lidhu.getOutputStream().write(42);
        System.out.println(i_ftuar_VALUE.getInputStream().read());
        i_ftuar_VALUE.close();
        System.out.println(Lidhu.getInputStream().read());
        Lidhu.close(); server_VALUE.close();
        ServerSocket bosh_server = new ServerSocket(9250);
        bosh_server.setSoTimeout(10);
        try { bosh_server.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("Ora_VALUE_4692cef5 제한"); }
        bosh_server.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
