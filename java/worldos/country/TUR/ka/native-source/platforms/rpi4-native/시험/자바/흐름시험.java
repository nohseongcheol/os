// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket სერვერი_მნიშვნელობა = new ServerSocket(9250);
        Socket სტუმარი_მნიშვნელობა = new Socket("localhost", 9250);
        Socket დაკავშირება = სერვერი_მნიშვნელობა.accept();
        if (დაკავშირება.getPort() != სტუმარი_მნიშვნელობა.getLocalPort() || სტუმარი_მნიშვნელობა.getPort() != დაკავშირება.getLocalPort()) throw new RuntimeException("პორტი_მნიშვნელობა 불일치");
        byte[] 전문 = "한글 ნაკადი_მნიშვნელობა".getBytes("UTF-8");
        სტუმარი_მნიშვნელობა.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int სიგრძე_მნიშვნელობა = დაკავშირება.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(სიგრძე_მნიშვნელობა == 전문.length);
        for (int i = 0; i < სიგრძე_მნიშვნელობა; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("შიგთავსი_მნიშვნელობა 불일치");
        დაკავშირება.getOutputStream().write(42);
        System.out.println(სტუმარი_მნიშვნელობა.getInputStream().read());
        სტუმარი_მნიშვნელობა.close();
        System.out.println(დაკავშირება.getInputStream().read());
        დაკავშირება.close(); სერვერი_მნიშვნელობა.close();
        ServerSocket ცარიელი_სერვერი = new ServerSocket(9250);
        ცარიელი_სერვერი.setSoTimeout(10);
        try { ცარიელი_სერვერი.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("დრო_მნიშვნელობა 제한"); }
        ცარიელი_სერვერი.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
