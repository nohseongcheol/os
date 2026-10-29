// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static კავშირი გახსნა(String მისამართი, int 접속번호) throws 입출력예외 {
        try { return კავშირი.გახსნა(მისამართი, 접속번호);
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.გახსნა(접속번호);
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public static Socket დაკავშირება(String მისამართი, int პორტი_მნიშვნელობა) throws 입출력예외 {
        try { return new Socket(მისამართი, პორტი_მნიშვნელობა);
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public static ServerSocket 듣기(int პორტი_მნიშვნელობა) throws 입출력예외 {
        try { return new ServerSocket(პორტი_მნიშვნელობა);
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public static Socket 받기(ServerSocket სერვერი_მნიშვნელობა) throws 입출력예외 {
        try { return სერვერი_მნიშვნელობა.accept();
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
}
