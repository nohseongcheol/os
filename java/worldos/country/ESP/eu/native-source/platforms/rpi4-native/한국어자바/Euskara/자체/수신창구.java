// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;

/** 수신(受信)·ataka_balio(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int ataka_zenbaki) throws S_I_salbuespen {
        try { 표준창구 = new java.net.ServerSocket(ataka_zenbaki);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public static 수신창구 Ireki(int ataka_zenbaki) throws S_I_salbuespen {
        try { return new 수신창구(ataka_zenbaki);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public konexio 받기() throws S_I_salbuespen {
        try { return new konexio(표준창구.accept());
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public int ataka_zenbaki() { return 표준창구.getLocalPort(); }
    public void DENBORA_MUGA(int 밀리초) throws S_I_salbuespen {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Itxi() throws S_I_salbuespen {
        try { 표준창구.close();
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
}
