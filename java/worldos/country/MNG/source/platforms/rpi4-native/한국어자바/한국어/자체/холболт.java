// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Холбох(連結)·суваг_оролт(通路): 상대와 이어진 TCP байт_утга 흐름의 종단. */
public final class холболт {
    private final java.net.Socket 표준연결;
    холболт(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static холболт Нээх(String хаяг, int 접속번호) throws 입출력예외 {
        try {
            return new холболт(new java.net.Socket(хаяг, 접속번호));
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public 입력흐름 입력() throws 입출력예외 {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public 출력흐름 출력() throws 입출력예외 {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public void 대기시간(int 밀리초) throws 입출력예외 {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public int 접속번호() { return 표준연결.getPort(); }
    public int 지역접속번호() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Хаах() throws 입출력예외 {
        try { 표준연결.close();
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
}
