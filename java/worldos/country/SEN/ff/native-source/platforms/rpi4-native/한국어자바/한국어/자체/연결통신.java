// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static ceŋondiral udditde(String ñiiɓirde, int 접속번호) throws 입출력예외 {
        try { return ceŋondiral.udditde(ñiiɓirde, 접속번호);
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.udditde(접속번호);
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
    public static Socket seŋaade(String ñiiɓirde, int poor_njaru) throws 입출력예외 {
        try { return new Socket(ñiiɓirde, poor_njaru);
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
    public static ServerSocket 듣기(int poor_njaru) throws 입출력예외 {
        try { return new ServerSocket(poor_njaru);
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
    public static Socket 받기(ServerSocket sarworde_njaru) throws 입출력예외 {
        try { return sarworde_njaru.accept();
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
}
