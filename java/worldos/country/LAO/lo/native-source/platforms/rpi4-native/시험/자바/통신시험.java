// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket ດ້ານຫນ້າ_ຄ່າ = 통신.ສ້າງ(9431), ກັບ_ຄືນ_ຄ່າ = 통신.ສ້າງ(9432);
        try {
            통신.ສົ່ງ(ດ້ານຫນ້າ_ຄ່າ, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(ກັບ_ຄືນ_ຄ່າ));
            byte[] ແຫຼ່ງທີ່ມາ = 문자.부호화("회신"); ດ້ານຫນ້າ_ຄ່າ.send(new DatagramPacket(ແຫຼ່ງທີ່ມາ, ແຫຼ່ງທີ່ມາ.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); ກັບ_ຄືນ_ຄ່າ.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(ກັບ_ຄືນ_ຄ່າ.getLocalPort());
            ກັບ_ຄືນ_ຄ່າ.setSoTimeout(10);
            try { ກັບ_ຄືນ_ຄ່າ.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 ເວລາ_ຄ່າ 초과"); }
            ກັບ_ຄືນ_ຄ່າ.close();
            try { ກັບ_ຄືນ_ຄ່າ.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { ດ້ານຫນ້າ_ຄ່າ.close(); ກັບ_ຄືນ_ຄ່າ.close(); }
    }
}
