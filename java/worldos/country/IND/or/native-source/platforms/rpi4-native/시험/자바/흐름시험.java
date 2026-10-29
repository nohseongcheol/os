// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket ସର୍ଭର୍_ମୂଲ୍ୟ = new ServerSocket(9250);
        Socket ଅତିଥି_ମୂଲ୍ୟ = new Socket("localhost", 9250);
        Socket ସଂଯୋଗ_କରନ୍ତୁ = ସର୍ଭର୍_ମୂଲ୍ୟ.accept();
        if (ସଂଯୋଗ_କରନ୍ତୁ.getPort() != ଅତିଥି_ମୂଲ୍ୟ.getLocalPort() || ଅତିଥି_ମୂଲ୍ୟ.getPort() != ସଂଯୋଗ_କରନ୍ତୁ.getLocalPort()) throw new RuntimeException("ପୋର୍ଟ_ମୂଲ୍ୟ 불일치");
        byte[] 전문 = "한글 ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ".getBytes("UTF-8");
        ଅତିଥି_ମୂଲ୍ୟ.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ = ସଂଯୋଗ_କରନ୍ତୁ.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ == 전문.length);
        for (int i = 0; i < ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("ବିଷୟ_ମୂଲ୍ୟ 불일치");
        ସଂଯୋଗ_କରନ୍ତୁ.getOutputStream().write(42);
        System.out.println(ଅତିଥି_ମୂଲ୍ୟ.getInputStream().read());
        ଅତିଥି_ମୂଲ୍ୟ.close();
        System.out.println(ସଂଯୋଗ_କରନ୍ତୁ.getInputStream().read());
        ସଂଯୋଗ_କରନ୍ତୁ.close(); ସର୍ଭର୍_ମୂଲ୍ୟ.close();
        ServerSocket ଖାଲି_ସର୍ଭର୍ = new ServerSocket(9250);
        ଖାଲି_ସର୍ଭର୍.setSoTimeout(10);
        try { ଖାଲି_ସର୍ଭର୍.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("ସମୟ_ମୂଲ୍ୟ 제한"); }
        ଖାଲି_ସର୍ଭର୍.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
