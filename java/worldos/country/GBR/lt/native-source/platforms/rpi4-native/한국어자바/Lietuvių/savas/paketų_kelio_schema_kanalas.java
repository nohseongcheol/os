// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;

/** paketų_kelio_schema(電文)·kanalas_įrašas(通路): 경계를 가진 UDP 자료를 주고받는 dalyvis. */
public final class paketų_kelio_schema_kanalas {
    private final java.net.DatagramSocket 표준종단;
    private paketų_kelio_schema_kanalas(int prievado_numeris) throws Į_I_išimtis {
        try { 표준종단 = 통신.Atverti(prievado_numeris);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public static paketų_kelio_schema_kanalas Atverti(int prievado_numeris) throws Į_I_išimtis {
        try { return new paketų_kelio_schema_kanalas(prievado_numeris);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public void siųsti(String ADDRESS, int prievado_numeris, String duomenys) throws Į_I_išimtis {
        try { 통신.siųsti(표준종단, ADDRESS, prievado_numeris, duomenys);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public String gauti() throws Į_I_išimtis {
        try { return 통신.gauti(표준종단);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public void SKIRTASIS_LAIKAS(int 밀리초) throws Į_I_išimtis {
        try { 통신.SKIRTASIS_LAIKAS(표준종단, 밀리초);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public int prievado_numeris() { return 표준종단.getLocalPort(); }
    public boolean informacinės_technologijos_uždaryta() { return 표준종단.isClosed(); }
    public void Užverti() { 통신.Užverti(표준종단); }
}
