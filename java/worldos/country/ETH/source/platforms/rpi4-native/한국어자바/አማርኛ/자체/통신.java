// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 숫자 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket መክፈቻ(int ወደብ_እሴት) throws ግቤት_ውጤት_ልዩነት {
        try { return new DatagramSocket(ወደብ_እሴት);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public static void ላክ(DatagramSocket 종단, int ወደብ_እሴት, String ይዘት_እሴት) throws ግቤት_ውጤት_ልዩነት {
        try {
        ላክ(종단, "127.0.0.1", ወደብ_እሴት, ይዘት_እሴት);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public static void ላክ(DatagramSocket 종단, String አድራሻ, int ወደብ_እሴት, String ይዘት_እሴት) throws ግቤት_ውጤት_ልዩነት {
        try {
        byte[] ባይት_እሴት = 문자.부호화(ይዘት_እሴት);
        종단.send(new DatagramPacket(ባይት_እሴት, ባይት_እሴት.length, InetAddress.getByName(አድራሻ), ወደብ_እሴት));
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public static String 받기(DatagramSocket 종단) throws ግቤት_ውጤት_ልዩነት {
        try {
        byte[] ባይት_እሴት = new byte[512]; DatagramPacket 전문 = new DatagramPacket(ባይት_እሴት, ባይት_እሴት.length); 종단.receive(전문);
        byte[] ልኬት = new byte[전문.getLength()]; System.arraycopy(ባይት_እሴት, 0, ልኬት, 0, ልኬት.length); return 문자.ምስጠራውን_ፍታ_ውሂብ(ልኬት);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws ግቤት_ውጤት_ልዩነት {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public static void መዝጊያ(DatagramSocket 종단) { 종단.close(); }
}
