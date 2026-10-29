// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static kgokaganya Bula(String atrese, int 접속번호) throws 입출력예외 {
        try { return kgokaganya.Bula(atrese, 접속번호);
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.Bula(접속번호);
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public static Socket Ikgokaganye(String atrese, int phote_boleng) throws 입출력예외 {
        try { return new Socket(atrese, phote_boleng);
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public static ServerSocket 듣기(int phote_boleng) throws 입출력예외 {
        try { return new ServerSocket(phote_boleng);
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public static Socket 받기(ServerSocket seba_boleng) throws 입출력예외 {
        try { return seba_boleng.accept();
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
}
