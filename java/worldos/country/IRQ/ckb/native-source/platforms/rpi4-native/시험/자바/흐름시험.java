// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket ڕاژەکار_نرخ = new ServerSocket(9250);
        Socket 손님 = new Socket("localhost", 9250);
        Socket لكاندن = ڕاژەکار_نرخ.accept();
        if (لكاندن.getPort() != 손님.getLocalPort() || 손님.getPort() != لكاندن.getLocalPort()) throw new RuntimeException("دەرگا_نرخ 불일치");
        byte[] 전문 = "한글 Stream_نرخ".getBytes("UTF-8");
        손님.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int درێژی_نرخ = لكاندن.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(درێژی_نرخ == 전문.length);
        for (int i = 0; i < درێژی_نرخ; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("ناوەرۆک_نرخ 불일치");
        لكاندن.getOutputStream().write(42);
        System.out.println(손님.getInputStream().read());
        손님.close();
        System.out.println(لكاندن.getInputStream().read());
        لكاندن.close(); ڕاژەکار_نرخ.close();
        ServerSocket بەتاڵ_ڕاژەکار = new ServerSocket(9250);
        بەتاڵ_ڕاژەکار.setSoTimeout(10);
        try { بەتاڵ_ڕاژەکار.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("کات_نرخ 제한"); }
        بەتاڵ_ڕاژەکار.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
