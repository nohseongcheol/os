// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;

/** Tengjast(連結)·rás_færsla(通路): 상대와 이어진 TCP bæti_VALUE 흐름의 endastöð. */
public final class tenging {
    private final java.net.Socket 표준연결;
    tenging(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static tenging Opna(String slóð, int tengisnúmer) throws I_Ú_undantekning {
        try {
            return new tenging(new java.net.Socket(slóð, tengisnúmer));
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public 입력흐름 입력() throws I_Ú_undantekning {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public úttak_Stream úttak() throws I_Ú_undantekning {
        try { return new úttak_Stream(표준연결.getOutputStream());
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public void TIMEOUT(int 밀리초) throws I_Ú_undantekning {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public int tengisnúmer() { return 표준연결.getPort(); }
    public int staðbundið_tengisnúmer() { return 표준연결.getLocalPort(); }
    public boolean upplýsingatækni_lokað() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Loka() throws I_Ú_undantekning {
        try { 표준연결.close();
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
}
