// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;

/** Konektatu(連結)·kanal_sarrera(通路): 상대와 이어진 TCP byte_balio 흐름의 amaiera_puntu. */
public final class konexio {
    private final java.net.Socket 표준연결;
    konexio(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static konexio Ireki(String helbide, int ataka_zenbaki) throws S_I_salbuespen {
        try {
            return new konexio(new java.net.Socket(helbide, ataka_zenbaki));
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public 입력흐름 입력() throws S_I_salbuespen {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public 출력흐름 Irteera() throws S_I_salbuespen {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public void DENBORA_MUGA(int 밀리초) throws S_I_salbuespen {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public int ataka_zenbaki() { return 표준연결.getPort(); }
    public int lokal_ataka_zenbaki() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Itxi() throws S_I_salbuespen {
        try { 표준연결.close();
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
}
