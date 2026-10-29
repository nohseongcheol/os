// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket മുൻവശം_മൂല്യം = 통신.തുറക്കുക(9431), പിന്നിലേക്ക്_മൂല്യം = 통신.തുറക്കുക(9432);
        try {
            통신.അയയ്ക്കുക(മുൻവശം_മൂല്യം, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(പിന്നിലേക്ക്_മൂല്യം));
            byte[] ഉറവിടം = 문자.부호화("회신"); മുൻവശം_മൂല്യം.send(new DatagramPacket(ഉറവിടം, ഉറവിടം.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); പിന്നിലേക്ക്_മൂല്യം.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(പിന്നിലേക്ക്_മൂല്യം.getLocalPort());
            പിന്നിലേക്ക്_മൂല്യം.setSoTimeout(10);
            try { പിന്നിലേക്ക്_മൂല്യം.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 സമയ_മൂല്യം 초과"); }
            പിന്നിലേക്ക്_മൂല്യം.close();
            try { പിന്നിലേക്ക്_മൂല്യം.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { മുൻവശം_മൂല്യം.close(); പിന്നിലേക്ക്_മൂല്യം.close(); }
    }
}
