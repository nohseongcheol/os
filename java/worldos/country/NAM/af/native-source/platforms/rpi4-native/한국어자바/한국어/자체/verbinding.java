// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Koppel(連結)·kanaal_inskrywing(通路): 상대와 이어진 TCP greep_VALUE 흐름의 종단. */
public final class verbinding {
    private final java.net.Socket 표준연결;
    verbinding(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static verbinding skep(String adres, int 접속번호) throws I_O_uitsondering {
        try {
            return new verbinding(new java.net.Socket(adres, 접속번호));
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public 입력흐름 입력() throws I_O_uitsondering {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public 출력흐름 Afvoer() throws I_O_uitsondering {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public void UITTELLING(int 밀리초) throws I_O_uitsondering {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public int 접속번호() { return 표준연결.getPort(); }
    public int 지역접속번호() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Sluit() throws I_O_uitsondering {
        try { 표준연결.close();
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
}
