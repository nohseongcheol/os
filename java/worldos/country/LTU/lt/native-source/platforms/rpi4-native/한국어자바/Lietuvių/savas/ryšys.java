// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;

/** Prisijungti(連結)·kanalas_įrašas(通路): 상대와 이어진 TCP baitas_VALUE 흐름의 dalyvis. */
public final class ryšys {
    private final java.net.Socket 표준연결;
    ryšys(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static ryšys Atverti(String ADDRESS, int prievado_numeris) throws Į_I_išimtis {
        try {
            return new ryšys(new java.net.Socket(ADDRESS, prievado_numeris));
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public įvesties_srautas 입력() throws Į_I_išimtis {
        try { return new įvesties_srautas(표준연결.getInputStream());
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public išvesties_srautas Išvestis() throws Į_I_išimtis {
        try { return new išvesties_srautas(표준연결.getOutputStream());
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public void SKIRTASIS_LAIKAS(int 밀리초) throws Į_I_išimtis {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public int prievado_numeris() { return 표준연결.getPort(); }
    public int vietinis_prievado_numeris() { return 표준연결.getLocalPort(); }
    public boolean informacinės_technologijos_uždaryta() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Užverti() throws Į_I_išimtis {
        try { 표준연결.close();
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
}
