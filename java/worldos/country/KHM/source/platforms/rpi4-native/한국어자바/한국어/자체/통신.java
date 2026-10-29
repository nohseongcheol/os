// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 숫자 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket បើក(int ច្រក_តំលៃ) throws ចូល_ចេញ_ការលើកលែង {
        try { return new DatagramSocket(ច្រក_តំលៃ);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public static void ផ្ញើ(DatagramSocket 종단, int ច្រក_តំលៃ, String មាតិកា_តំលៃ) throws ចូល_ចេញ_ការលើកលែង {
        try {
        ផ្ញើ(종단, "127.0.0.1", ច្រក_តំលៃ, មាតិកា_តំលៃ);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public static void ផ្ញើ(DatagramSocket 종단, String អ៊ីម៉ែល, int ច្រក_តំលៃ, String មាតិកា_តំលៃ) throws ចូល_ចេញ_ការលើកលែង {
        try {
        byte[] បៃ_តំលៃ = 문자.부호화(មាតិកា_តំលៃ);
        종단.send(new DatagramPacket(បៃ_តំលៃ, បៃ_តំលៃ.length, InetAddress.getByName(អ៊ីម៉ែល), ច្រក_តំលៃ));
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public static String 받기(DatagramSocket 종단) throws ចូល_ចេញ_ការលើកលែង {
        try {
        byte[] បៃ_តំលៃ = new byte[512]; DatagramPacket 전문 = new DatagramPacket(បៃ_តំលៃ, បៃ_តំលៃ.length); 종단.receive(전문);
        byte[] ការវាស់វែង = new byte[전문.getLength()]; System.arraycopy(បៃ_តំលៃ, 0, ការវាស់វែង, 0, ការវាស់វែង.length); return 문자.ដោះកូដ_ទិន្នន័យ(ការវាស់វែង);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public static void អស់ម៉ោង(DatagramSocket 종단, int 밀리초) throws ចូល_ចេញ_ការលើកលែង {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public static void បិទ(DatagramSocket 종단) { 종단.close(); }
}
