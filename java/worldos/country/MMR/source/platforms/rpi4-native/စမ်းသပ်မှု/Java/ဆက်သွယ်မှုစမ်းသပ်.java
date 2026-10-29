// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import မြန်မာ.ကိုယ်ပိုင်.အက္ခရာ;
import မြန်မာ.ကိုယ်ပိုင်.ဆက်သွယ်မှု;
public class ဆက်သွယ်မှုစမ်းသပ် {
    public static void main(String[] args) throws Exception {
        DatagramSocket ရှေ့တန်ဖိုး = ဆက်သွယ်မှု.ဖွင့်(9431), နောက်တန်ဖိုး = ဆက်သွယ်မှု.ဖွင့်(9432);
        try {
            ဆက်သွယ်မှု.ပို့(ရှေ့တန်ဖိုး, 9432, "Java UDP 한글😀"); System.out.println(ဆက်သွယ်မှု.လက်ခံ(နောက်တန်ဖိုး));
            byte[] မူရင်းကုဒ် = အက္ခရာ.ကုဒ်သွင်း("회신"); ရှေ့တန်ဖိုး.send(new DatagramPacket(မူရင်းကုဒ်, မူရင်းကုဒ်.length, InetAddress.getByName("localhost"), 9432));
            byte[] ရရှိတန်ဖိုး = new byte[32]; DatagramPacket ဒေတာစာ = new DatagramPacket(ရရှိတန်ဖိုး, ရရှိတန်ဖိုး.length); နောက်တန်ဖိုး.receive(ဒေတာစာ);
            System.out.println(ဒေတာစာ.getLength()); System.out.println(ဒေတာစာ.getPort()); System.out.println(ဒေတာစာ.getAddress().getHostAddress());
            System.out.println(နောက်တန်ဖိုး.getLocalPort());
            နောက်တန်ဖိုး.setSoTimeout(10);
            try { နောက်တန်ဖိုး.receive(ဒေတာစာ); } catch (SocketTimeoutException e) { System.out.println("တန်ဖိုးလက်ခံရယူ အချိန်တန်ဖိုး 초과"); }
            နောက်တန်ဖိုး.close();
            try { နောက်တန်ဖိုး.receive(ဒေတာစာ); } catch (java.io.IOException e) { System.out.println("닫힌 ဆက်သွယ်မှု"); }
        } finally { ရှေ့တန်ဖိုး.close(); နောက်တန်ဖိုး.close(); }
    }
}
