// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import ελληνικά.ίδιο.문자;
import ελληνικά.ίδιο.통신;
public class δοκιμή_Δικτύωση {
    public static void main(String[] args) throws Exception {
        DatagramSocket μπροστινή_τιμή = 통신.Άνοιγμα(9431), Πίσω_τιμή = 통신.Άνοιγμα(9432);
        try {
            통신.στέλνω(μπροστινή_τιμή, 9432, "자바 UDP 한글😀"); System.out.println(통신.λαμβάνω(Πίσω_τιμή));
            byte[] ΠΗΓΗ = 문자.κωδικοποιώ("회신"); μπροστινή_τιμή.send(new DatagramPacket(ΠΗΓΗ, ΠΗΓΗ.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket αυτοδύναμο_πακέτο = new DatagramPacket(받은값, 받은값.length); Πίσω_τιμή.receive(αυτοδύναμο_πακέτο);
            System.out.println(αυτοδύναμο_πακέτο.getLength()); System.out.println(αυτοδύναμο_πακέτο.getPort()); System.out.println(αυτοδύναμο_πακέτο.getAddress().getHostAddress());
            System.out.println(Πίσω_τιμή.getLocalPort());
            Πίσω_τιμή.setSoTimeout(10);
            try { Πίσω_τιμή.receive(αυτοδύναμο_πακέτο); } catch (SocketTimeoutException e) { System.out.println("λαμβάνω_τιμή_cef4d8ab τιμή_ώρας 초과"); }
            Πίσω_τιμή.close();
            try { Πίσω_τιμή.receive(αυτοδύναμο_πακέτο); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { μπροστινή_τιμή.close(); Πίσω_τιμή.close(); }
    }
}
