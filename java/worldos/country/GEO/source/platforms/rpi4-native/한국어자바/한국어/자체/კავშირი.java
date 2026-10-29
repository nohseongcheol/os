// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** დაკავშირება(連結)·არხი_შენატანი(通路): 상대와 이어진 TCP ბაიტი_მნიშვნელობა 흐름의 종단. */
public final class კავშირი {
    private final java.net.Socket 표준연결;
    კავშირი(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static კავშირი გახსნა(String მისამართი, int 접속번호) throws 입출력예외 {
        try {
            return new კავშირი(new java.net.Socket(მისამართი, 접속번호));
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public 입력흐름 입력() throws 입출력예외 {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public 출력흐름 출력() throws 입출력예외 {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public void დრო_ამოიწურა(int 밀리초) throws 입출력예외 {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public int 접속번호() { return 표준연결.getPort(); }
    public int 지역접속번호() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void დახურვა() throws 입출력예외 {
        try { 표준연결.close();
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
}
