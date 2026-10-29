// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static کنکشن بنڑاؤ(String پتا, int 접속번호) throws 입출력예외 {
        try { return کنکشن.بنڑاؤ(پتا, 접속번호);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.بنڑاؤ(접속번호);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
    public static Socket جڑو(String پتا, int دہانہ_قدر) throws 입출력예외 {
        try { return new Socket(پتا, دہانہ_قدر);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
    public static ServerSocket 듣기(int دہانہ_قدر) throws 입출력예외 {
        try { return new ServerSocket(دہانہ_قدر);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
    public static Socket 받기(ServerSocket سرور_قدر) throws 입출력예외 {
        try { return سرور_قدر.accept();
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
}
