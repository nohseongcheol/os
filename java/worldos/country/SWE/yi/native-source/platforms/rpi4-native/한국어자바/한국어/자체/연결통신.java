// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static 연결통로 עפֿן(String 주소, int 접속번호) throws 입출력예외 {
        try { return 연결통로.עפֿן(주소, 접속번호);
        } catch (java.io.IOException טעות) { throw 예외변환.입출력(טעות); }
        catch (RuntimeException טעות) { throw 예외변환.실행(טעות); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.עפֿן(접속번호);
        } catch (java.io.IOException טעות) { throw 예외변환.입출력(טעות); }
        catch (RuntimeException טעות) { throw 예외변환.실행(טעות); }
    }
    public static Socket 연결(String 주소, int 창구) throws 입출력예외 {
        try { return new Socket(주소, 창구);
        } catch (java.io.IOException טעות) { throw 예외변환.입출력(טעות); }
        catch (RuntimeException טעות) { throw 예외변환.실행(טעות); }
    }
    public static ServerSocket 듣기(int 창구) throws 입출력예외 {
        try { return new ServerSocket(창구);
        } catch (java.io.IOException טעות) { throw 예외변환.입출력(טעות); }
        catch (RuntimeException טעות) { throw 예외변환.실행(טעות); }
    }
    public static Socket 받기(ServerSocket 서버) throws 입출력예외 {
        try { return 서버.accept();
        } catch (java.io.IOException טעות) { throw 예외변환.입출력(טעות); }
        catch (RuntimeException טעות) { throw 예외변환.실행(טעות); }
    }
}
