// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class ᎠᏓᎪᎵᏰᏍᎩ_ᎤᏪᎬ {
    public static void main(String[] args) throws Exception {
        ServerSocket ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ = new ServerSocket(9250);
        Socket ᎠᏓᏩᏛᎯᏙᎯ_ᏧᎬᏩᎶᏗᏯ = new Socket("localhost", 9250);
        Socket ᎫᏓᎳ = ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.accept();
        if (ᎫᏓᎳ.getPort() != ᎠᏓᏩᏛᎯᏙᎯ_ᏧᎬᏩᎶᏗᏯ.getLocalPort() || ᎠᏓᏩᏛᎯᏙᎯ_ᏧᎬᏩᎶᏗᏯ.getPort() != ᎫᏓᎳ.getLocalPort()) throw new RuntimeException("ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ 불일치");
        byte[] 전문 = "한글 ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ".getBytes("UTF-8");
        ᎠᏓᏩᏛᎯᏙᎯ_ᏧᎬᏩᎶᏗᏯ.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ = ᎫᏓᎳ.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ == 전문.length);
        for (int i = 0; i < ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ 불일치");
        ᎫᏓᎳ.getOutputStream().write(42);
        System.out.println(ᎠᏓᏩᏛᎯᏙᎯ_ᏧᎬᏩᎶᏗᏯ.getInputStream().read());
        ᎠᏓᏩᏛᎯᏙᎯ_ᏧᎬᏩᎶᏗᏯ.close();
        System.out.println(ᎫᏓᎳ.getInputStream().read());
        ᎫᏓᎳ.close(); ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
