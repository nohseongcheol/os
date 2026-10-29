// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static پيوستون پرانيستل(String پته, int 접속번호) throws 입출력예외 {
        try { return پيوستون.پرانيستل(پته, 접속번호);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.پرانيستل(접속번호);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public static Socket نښلېدل(String پته, int درشل_ارزښت) throws 입출력예외 {
        try { return new Socket(پته, درشل_ارزښت);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public static ServerSocket 듣기(int درشل_ارزښت) throws 입출력예외 {
        try { return new ServerSocket(درشل_ارزښت);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public static Socket 받기(ServerSocket 서버) throws 입출력예외 {
        try { return 서버.accept();
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
}
