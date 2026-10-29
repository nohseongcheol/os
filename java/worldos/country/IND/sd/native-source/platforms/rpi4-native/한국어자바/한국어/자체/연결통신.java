// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static ڪنيڪشن ٺاھيو(String پتو, int 접속번호) throws 입출력예외 {
        try { return ڪنيڪشن.ٺاھيو(پتو, 접속번호);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.تعميل_ڪرڻ_حڪم(نقص); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.ٺاھيو(접속번호);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.تعميل_ڪرڻ_حڪم(نقص); }
    }
    public static Socket ڪنيڪٽ(String پتو, int پورٽ_قدر) throws 입출력예외 {
        try { return new Socket(پتو, پورٽ_قدر);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.تعميل_ڪرڻ_حڪم(نقص); }
    }
    public static ServerSocket 듣기(int پورٽ_قدر) throws 입출력예외 {
        try { return new ServerSocket(پورٽ_قدر);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.تعميل_ڪرڻ_حڪم(نقص); }
    }
    public static Socket 받기(ServerSocket سرور_قدر) throws 입출력예외 {
        try { return سرور_قدر.accept();
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.تعميل_ڪرڻ_حڪم(نقص); }
    }
}
