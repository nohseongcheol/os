// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket 서버 = new ServerSocket(9250);
        Socket ແຂກ_ຄ່າ = new Socket("localhost", 9250);
        Socket ເຊື່ອມຕໍ່ = 서버.accept();
        if (ເຊື່ອມຕໍ່.getPort() != ແຂກ_ຄ່າ.getLocalPort() || ແຂກ_ຄ່າ.getPort() != ເຊື່ອມຕໍ່.getLocalPort()) throw new RuntimeException("ຜອດ_ຄ່າ 불일치");
        byte[] 전문 = "한글 ສະຕຣີມ_ຄ່າ".getBytes("UTF-8");
        ແຂກ_ຄ່າ.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int ຄວາມຍາວ_ຄ່າ = ເຊື່ອມຕໍ່.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(ຄວາມຍາວ_ຄ່າ == 전문.length);
        for (int i = 0; i < ຄວາມຍາວ_ຄ່າ; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("ເນື້ອໃນ_ຄ່າ_cb0f2404 불일치");
        ເຊື່ອມຕໍ່.getOutputStream().write(42);
        System.out.println(ແຂກ_ຄ່າ.getInputStream().read());
        ແຂກ_ຄ່າ.close();
        System.out.println(ເຊື່ອມຕໍ່.getInputStream().read());
        ເຊື່ອມຕໍ່.close(); 서버.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("ເວລາ_ຄ່າ 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
