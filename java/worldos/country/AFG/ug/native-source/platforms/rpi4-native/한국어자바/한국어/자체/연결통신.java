// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static ئۇلىنىش ئاچ(String ئادرېس, int 접속번호) throws 입출력예외 {
        try { return ئۇلىنىش.ئاچ(ئادرېس, 접속번호);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.ئاچ(접속번호);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public static Socket ئۇلا(String ئادرېس, int ئېغىز_قىممىتى) throws 입출력예외 {
        try { return new Socket(ئادرېس, ئېغىز_قىممىتى);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public static ServerSocket 듣기(int ئېغىز_قىممىتى) throws 입출력예외 {
        try { return new ServerSocket(ئېغىز_قىممىتى);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public static Socket 받기(ServerSocket مۇلازىمىتېر_قىممىتى) throws 입출력예외 {
        try { return مۇلازىمىتېر_قىممىتى.accept();
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
}
