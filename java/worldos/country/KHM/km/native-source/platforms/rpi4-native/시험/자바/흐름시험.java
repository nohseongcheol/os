// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket ម៉ាស៊ីនមេ_តំលៃ = new ServerSocket(9250);
        Socket ភ្ញៀវ_តំលៃ = new Socket("localhost", 9250);
        Socket ភ្ជាប់ = ម៉ាស៊ីនមេ_តំលៃ.accept();
        if (ភ្ជាប់.getPort() != ភ្ញៀវ_តំលៃ.getLocalPort() || ភ្ញៀវ_តំលៃ.getPort() != ភ្ជាប់.getLocalPort()) throw new RuntimeException("ច្រក_តំលៃ 불일치");
        byte[] 전문 = "한글 ស្ទ្រីម_តំលៃ".getBytes("UTF-8");
        ភ្ញៀវ_តំលៃ.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int ប្រវែង_តំលៃ = ភ្ជាប់.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(ប្រវែង_តំលៃ == 전문.length);
        for (int i = 0; i < ប្រវែង_តំលៃ; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("មាតិកា_តំលៃ 불일치");
        ភ្ជាប់.getOutputStream().write(42);
        System.out.println(ភ្ញៀវ_តំលៃ.getInputStream().read());
        ភ្ញៀវ_តំលៃ.close();
        System.out.println(ភ្ជាប់.getInputStream().read());
        ភ្ជាប់.close(); ម៉ាស៊ីនមេ_តំលៃ.close();
        ServerSocket ទទេរ_ម៉ាស៊ីនមេ = new ServerSocket(9250);
        ទទេរ_ម៉ាស៊ីនមេ.setSoTimeout(10);
        try { ទទេរ_ម៉ាស៊ីនមេ.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("ពេល_វេលា_តំលៃ 제한"); }
        ទទេរ_ម៉ាស៊ីនមេ.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
