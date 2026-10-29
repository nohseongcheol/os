// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** UNGANISHA(連結)·mkondo_ingizo(通路): 상대와 이어진 TCP baiti_thamani 흐름의 종단. */
public final class muunganisho {
    private final java.net.Socket 표준연결;
    muunganisho(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static muunganisho unda(String anwani, int namba_ya_kituo) throws I_T_vighairi {
        try {
            return new muunganisho(new java.net.Socket(anwani, namba_ya_kituo));
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public 입력흐름 입력() throws I_T_vighairi {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public 출력흐름 출력() throws I_T_vighairi {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public void 대기시간(int 밀리초) throws I_T_vighairi {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public int namba_ya_kituo() { return 표준연결.getPort(); }
    public int jirani_namba_ya_kituo() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void funga() throws I_T_vighairi {
        try { 표준연결.close();
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
}
