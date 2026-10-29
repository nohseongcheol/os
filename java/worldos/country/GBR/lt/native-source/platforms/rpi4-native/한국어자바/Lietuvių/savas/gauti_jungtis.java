// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;

/** gauti_VALUE_cef4d8ab(受信)·jungtis_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class gauti_jungtis {
    private final java.net.ServerSocket 표준창구;
    private gauti_jungtis(int prievado_numeris) throws Į_I_išimtis {
        try { 표준창구 = new java.net.ServerSocket(prievado_numeris);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public static gauti_jungtis Atverti(int prievado_numeris) throws Į_I_išimtis {
        try { return new gauti_jungtis(prievado_numeris);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public ryšys gauti() throws Į_I_išimtis {
        try { return new ryšys(표준창구.accept());
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public int prievado_numeris() { return 표준창구.getLocalPort(); }
    public void SKIRTASIS_LAIKAS(int 밀리초) throws Į_I_išimtis {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public boolean informacinės_technologijos_uždaryta() { return 표준창구.isClosed(); }
    public void Užverti() throws Į_I_išimtis {
        try { 표준창구.close();
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
}
