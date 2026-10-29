// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Lietuvių.savas.문자;
import Lietuvių.savas.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket priekinis_VALUE = 통신.Atverti(9431), ATGAL_VALUE = 통신.Atverti(9432);
        try {
            통신.siųsti(priekinis_VALUE, 9432, "자바 UDP 한글😀"); System.out.println(통신.gauti(ATGAL_VALUE));
            byte[] ŠALTINIS = 문자.koduoti("회신"); priekinis_VALUE.send(new DatagramPacket(ŠALTINIS, ŠALTINIS.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_VALUE = new byte[32]; DatagramPacket paketų_kelio_schema = new DatagramPacket(RECEIVED_VALUE, RECEIVED_VALUE.length); ATGAL_VALUE.receive(paketų_kelio_schema);
            System.out.println(paketų_kelio_schema.getLength()); System.out.println(paketų_kelio_schema.getPort()); System.out.println(paketų_kelio_schema.getAddress().getHostAddress());
            System.out.println(ATGAL_VALUE.getLocalPort());
            ATGAL_VALUE.setSoTimeout(10);
            try { ATGAL_VALUE.receive(paketų_kelio_schema); } catch (SocketTimeoutException e) { System.out.println("gauti_VALUE_cef4d8ab TIME_VALUE 초과"); }
            ATGAL_VALUE.close();
            try { ATGAL_VALUE.receive(paketų_kelio_schema); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { priekinis_VALUE.close(); ATGAL_VALUE.close(); }
    }
}
