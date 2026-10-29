// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static веза отворити(String адреса, int 접속번호) throws 입출력예외 {
        try { return веза.отворити(адреса, 접속번호);
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.отворити(접속번호);
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
    public static Socket повезати(String адреса, int порт_вриједност) throws 입출력예외 {
        try { return new Socket(адреса, порт_вриједност);
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
    public static ServerSocket слушати_крајња_тачка(int порт_вриједност) throws 입출력예외 {
        try { return new ServerSocket(порт_вриједност);
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
    public static Socket 받기(ServerSocket сервер_вриједност) throws 입출력예외 {
        try { return сервер_вриједност.accept();
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
}
