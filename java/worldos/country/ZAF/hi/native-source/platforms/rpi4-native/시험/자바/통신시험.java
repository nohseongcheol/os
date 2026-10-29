// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import हिंदी.निज.문자;
import हिंदी.निज.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket सामने_मान = 통신.खोलें(9431), वापस_मान = 통신.खोलें(9432);
        try {
            통신.भेजें(सामने_मान, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(वापस_मान));
            byte[] स्रोत = 문자.부호화("회신"); सामने_मान.send(new DatagramPacket(स्रोत, स्रोत.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket स्वतंत्रसंदेश = new DatagramPacket(받은값, 받은값.length); वापस_मान.receive(स्वतंत्रसंदेश);
            System.out.println(स्वतंत्रसंदेश.getLength()); System.out.println(स्वतंत्रसंदेश.getPort()); System.out.println(स्वतंत्रसंदेश.getAddress().getHostAddress());
            System.out.println(वापस_मान.getLocalPort());
            वापस_मान.setSoTimeout(10);
            try { वापस_मान.receive(स्वतंत्रसंदेश); } catch (SocketTimeoutException e) { System.out.println("수신 समय_उपयोगिता 초과"); }
            वापस_मान.close();
            try { वापस_मान.receive(स्वतंत्रसंदेश); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { सामने_मान.close(); वापस_मान.close(); }
    }
}
