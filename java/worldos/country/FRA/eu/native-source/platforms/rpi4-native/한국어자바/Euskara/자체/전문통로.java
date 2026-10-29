// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;

/** 전문(電文)·kanal_sarrera(通路): 경계를 가진 UDP 자료를 주고받는 amaiera_puntu. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int ataka_zenbaki) throws S_I_salbuespen {
        try { 표준종단 = 통신.Ireki(ataka_zenbaki);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public static 전문통로 Ireki(int ataka_zenbaki) throws S_I_salbuespen {
        try { return new 전문통로(ataka_zenbaki);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public void bidali(String helbide, int ataka_zenbaki, String datuak) throws S_I_salbuespen {
        try { 통신.bidali(표준종단, helbide, ataka_zenbaki, datuak);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public String 받기() throws S_I_salbuespen {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public void DENBORA_MUGA(int 밀리초) throws S_I_salbuespen {
        try { 통신.DENBORA_MUGA(표준종단, 밀리초);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public int ataka_zenbaki() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Itxi() { 통신.Itxi(표준종단); }
}
