// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Verbannen(連結)·Kanal_Agab(通路): 상대와 이어진 TCP Byte_VALUE 흐름의 종단. */
public final class Verbindung {
    private final java.net.Socket 표준연결;
    Verbindung(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static Verbindung ariichten(String Adress, int 접속번호) throws 입출력예외 {
        try {
            return new Verbindung(new java.net.Socket(Adress, 접속번호));
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public 입력흐름 입력() throws 입출력예외 {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public 출력흐름 출력() throws 입출력예외 {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public void TIMEOUT(int 밀리초) throws 입출력예외 {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public int 접속번호() { return 표준연결.getPort(); }
    public int 지역접속번호() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Clôture() throws 입출력예외 {
        try { 표준연결.close();
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
}
