// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** ПАЙВАСТ(連結)·канал_ворида(通路): 상대와 이어진 TCP байт_қимат 흐름의 종단. */
public final class пайваст {
    private final java.net.Socket 표준연결;
    пайваст(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static пайваст кушодан(String суроға, int 접속번호) throws 입출력예외 {
        try {
            return new пайваст(new java.net.Socket(суроға, 접속번호));
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public 입력흐름 입력() throws 입출력예외 {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public 출력흐름 출력() throws 입출력예외 {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public void 대기시간(int 밀리초) throws 입출력예외 {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public int 접속번호() { return 표준연결.getPort(); }
    public int 지역접속번호() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Пӯшидан() throws 입출력예외 {
        try { 표준연결.close();
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
}
