// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ikinyarwanda.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static kwihuza Gufungura(String aderesi, int 접속번호) throws 입출력예외 {
        try { return kwihuza.Gufungura(aderesi, 접속번호);
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.Gufungura(접속번호);
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public static Socket Guhuza(String aderesi, int poti_agaciro) throws 입출력예외 {
        try { return new Socket(aderesi, poti_agaciro);
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public static ServerSocket 듣기(int poti_agaciro) throws 입출력예외 {
        try { return new ServerSocket(poti_agaciro);
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public static Socket 받기(ServerSocket seriveri_agaciro) throws 입출력예외 {
        try { return seriveri_agaciro.accept();
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
}
