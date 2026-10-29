// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket సర్వర్_మూల్యం = new ServerSocket(9250);
        Socket అతిథి_మూల్యం = new Socket("localhost", 9250);
        Socket కనెక్టుచేయి = సర్వర్_మూల్యం.accept();
        if (కనెక్టుచేయి.getPort() != అతిథి_మూల్యం.getLocalPort() || అతిథి_మూల్యం.getPort() != కనెక్టుచేయి.getLocalPort()) throw new RuntimeException("పోర్టు_మూల్యం 불일치");
        byte[] 전문 = "한글 ధార_మూల్యం".getBytes("UTF-8");
        అతిథి_మూల్యం.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int పొడవు_మూల్యం = కనెక్టుచేయి.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(పొడవు_మూల్యం == 전문.length);
        for (int i = 0; i < పొడవు_మూల్యం; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("విషయం_మూల్యం 불일치");
        కనెక్టుచేయి.getOutputStream().write(42);
        System.out.println(అతిథి_మూల్యం.getInputStream().read());
        అతిథి_మూల్యం.close();
        System.out.println(కనెక్టుచేయి.getInputStream().read());
        కనెక్టుచేయి.close(); సర్వర్_మూల్యం.close();
        ServerSocket ఖాళీ_సర్వర్ = new ServerSocket(9250);
        ఖాళీ_సర్వర్.setSoTimeout(10);
        try { ఖాళీ_సర్వర్.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("సమయం_మూల్యం 제한"); }
        ఖాళీ_సర్వర్.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
