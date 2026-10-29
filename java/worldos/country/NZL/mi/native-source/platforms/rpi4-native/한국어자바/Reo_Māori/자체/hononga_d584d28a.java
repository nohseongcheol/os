// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자체;

/** TŪHONO(連結)·hongere_tāurunga(通路): 상대와 이어진 TCP paita_uara 흐름의 종단. */
public final class hononga_d584d28a {
    private final java.net.Socket 표준연결;
    hononga_d584d28a(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static hononga_d584d28a Huaki(String ADDRESS, int 접속번호) throws 입출력예외 {
        try {
            return new hononga_d584d28a(new java.net.Socket(ADDRESS, 접속번호));
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public 입력흐름 입력() throws 입출력예외 {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public 출력흐름 출력() throws 입출력예외 {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public void KUA_PAU_TE_WĀ(int 밀리초) throws 입출력예외 {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public int 접속번호() { return 표준연결.getPort(); }
    public int 지역접속번호() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Kati() throws 입출력예외 {
        try { 표준연결.close();
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
}
