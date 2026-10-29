// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 ಅಂಕೆ_ಮೌಲ್ಯ 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket ತೆರೆ(int ಪೋರ್ಟ್_ಮೌಲ್ಯ) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { return new DatagramSocket(ಪೋರ್ಟ್_ಮೌಲ್ಯ);
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public static void ಕಳುಹಿಸಿ(DatagramSocket 종단, int ಪೋರ್ಟ್_ಮೌಲ್ಯ, String ವಿಷಯ_ಮೌಲ್ಯ) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try {
        ಕಳುಹಿಸಿ(종단, "127.0.0.1", ಪೋರ್ಟ್_ಮೌಲ್ಯ, ವಿಷಯ_ಮೌಲ್ಯ);
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public static void ಕಳುಹಿಸಿ(DatagramSocket 종단, String ಇಮೇಲ್, int ಪೋರ್ಟ್_ಮೌಲ್ಯ, String ವಿಷಯ_ಮೌಲ್ಯ) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try {
        byte[] ಬೈಟ್_ಮೌಲ್ಯ = 문자.부호화(ವಿಷಯ_ಮೌಲ್ಯ);
        종단.send(new DatagramPacket(ಬೈಟ್_ಮೌಲ್ಯ, ಬೈಟ್_ಮೌಲ್ಯ.length, InetAddress.getByName(ಇಮೇಲ್), ಪೋರ್ಟ್_ಮೌಲ್ಯ));
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public static String 받기(DatagramSocket 종단) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try {
        byte[] ಬೈಟ್_ಮೌಲ್ಯ = new byte[512]; DatagramPacket 전문 = new DatagramPacket(ಬೈಟ್_ಮೌಲ್ಯ, ಬೈಟ್_ಮೌಲ್ಯ.length); 종단.receive(전문);
        byte[] ಮಾಪನ = new byte[전문.getLength()]; System.arraycopy(ಬೈಟ್_ಮೌಲ್ಯ, 0, ಮಾಪನ, 0, ಮಾಪನ.length); return 문자.ಡೀಕ್ರಿಪ್ಟ್_ಮಾಡಿ_ಡೇಟಾ(ಮಾಪನ);
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public static void ಮುಚ್ಚು(DatagramSocket 종단) { 종단.close(); }
}
