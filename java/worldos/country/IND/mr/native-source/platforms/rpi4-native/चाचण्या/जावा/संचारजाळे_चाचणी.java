// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import मराठी.स्वकीय.वर्ण;
import मराठी.स्वकीय.संचार;
public class संचारजाळे_चाचणी {
    public static void main(String[] args) throws Exception {
        DatagramSocket पुढील_मूल्य = संचार.उघडा(9431), मागे_मूल्य = संचार.उघडा(9432);
        try {
            संचार.पाठवा(पुढील_मूल्य, 9432, "जावा UDP 한글😀"); System.out.println(संचार.स्वीकारा(मागे_मूल्य));
            byte[] स्रोत = वर्ण.संकेतन("회신"); पुढील_मूल्य.send(new DatagramPacket(स्रोत, स्रोत.length, InetAddress.getByName("localhost"), 9432));
            byte[] स्वीकारलेले_मूल्य = new byte[32]; DatagramPacket स्वतंत्रसंदेश = new DatagramPacket(स्वीकारलेले_मूल्य, स्वीकारलेले_मूल्य.length); मागे_मूल्य.receive(स्वतंत्रसंदेश);
            System.out.println(स्वतंत्रसंदेश.getLength()); System.out.println(स्वतंत्रसंदेश.getPort()); System.out.println(स्वतंत्रसंदेश.getAddress().getHostAddress());
            System.out.println(मागे_मूल्य.getLocalPort());
            मागे_मूल्य.setSoTimeout(10);
            try { मागे_मूल्य.receive(स्वतंत्रसंदेश); } catch (SocketTimeoutException e) { System.out.println("मूल्य_स्वीकारा वेळ_मूल्य 초과"); }
            मागे_मूल्य.close();
            try { मागे_मूल्य.receive(स्वतंत्रसंदेश); } catch (java.io.IOException e) { System.out.println("닫힌 संचार"); }
        } finally { पुढील_मूल्य.close(); मागे_मूल्य.close(); }
    }
}
