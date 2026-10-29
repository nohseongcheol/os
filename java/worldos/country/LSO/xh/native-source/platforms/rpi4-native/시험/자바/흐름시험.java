// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket iseva_ixabiso = new ServerSocket(9250);
        Socket undwendwe_ixabiso = new Socket("localhost", 9250);
        Socket Nxulumanisa = iseva_ixabiso.accept();
        if (Nxulumanisa.getPort() != undwendwe_ixabiso.getLocalPort() || undwendwe_ixabiso.getPort() != Nxulumanisa.getLocalPort()) throw new RuntimeException("iphothi_ixabiso 불일치");
        byte[] 전문 = "한글 Stream_ixabiso".getBytes("UTF-8");
        undwendwe_ixabiso.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int ubude_ixabiso = Nxulumanisa.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(ubude_ixabiso == 전문.length);
        for (int i = 0; i < ubude_ixabiso; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("Isiqulatho_ixabiso 불일치");
        Nxulumanisa.getOutputStream().write(42);
        System.out.println(undwendwe_ixabiso.getInputStream().read());
        undwendwe_ixabiso.close();
        System.out.println(Nxulumanisa.getInputStream().read());
        Nxulumanisa.close(); iseva_ixabiso.close();
        ServerSocket engenanto_iseva = new ServerSocket(9250);
        engenanto_iseva.setSoTimeout(10);
        try { engenanto_iseva.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        engenanto_iseva.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
