// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static epe_ipajia 열기(String ejepüsee, int 접속번호) throws 입출력예외 {
        try { return epe_ipajia.열기(ejepüsee, 접속번호);
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.열기(접속번호);
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public static Socket a_ataa(String ejepüsee, int outtülee_ajutuu) throws 입출력예외 {
        try { return new Socket(ejepüsee, outtülee_ajutuu);
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public static ServerSocket 듣기(int outtülee_ajutuu) throws 입출력예외 {
        try { return new ServerSocket(outtülee_ajutuu);
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public static Socket 받기(ServerSocket 서버) throws 입출력예외 {
        try { return 서버.accept();
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
}
