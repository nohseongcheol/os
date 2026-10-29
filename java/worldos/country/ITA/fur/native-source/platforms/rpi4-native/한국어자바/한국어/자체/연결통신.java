// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static 연결통로 Vierç(String 주소, int 접속번호) throws 입출력예외 {
        try { return 연결통로.Vierç(주소, 접속번호);
        } catch (java.io.IOException Erôr) { throw 예외변환.입출력(Erôr); }
        catch (RuntimeException Erôr) { throw 예외변환.실행(Erôr); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.Vierç(접속번호);
        } catch (java.io.IOException Erôr) { throw 예외변환.입출력(Erôr); }
        catch (RuntimeException Erôr) { throw 예외변환.실행(Erôr); }
    }
    public static Socket Conetiti(String 주소, int 창구) throws 입출력예외 {
        try { return new Socket(주소, 창구);
        } catch (java.io.IOException Erôr) { throw 예외변환.입출력(Erôr); }
        catch (RuntimeException Erôr) { throw 예외변환.실행(Erôr); }
    }
    public static ServerSocket 듣기(int 창구) throws 입출력예외 {
        try { return new ServerSocket(창구);
        } catch (java.io.IOException Erôr) { throw 예외변환.입출력(Erôr); }
        catch (RuntimeException Erôr) { throw 예외변환.실행(Erôr); }
    }
    public static Socket 받기(ServerSocket 서버) throws 입출력예외 {
        try { return 서버.accept();
        } catch (java.io.IOException Erôr) { throw 예외변환.입출력(Erôr); }
        catch (RuntimeException Erôr) { throw 예외변환.실행(Erôr); }
    }
}
