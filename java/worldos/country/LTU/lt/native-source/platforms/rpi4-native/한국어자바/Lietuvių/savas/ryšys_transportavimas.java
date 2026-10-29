// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;
import java.net.*;
public final class ryšys_transportavimas {
    private ryšys_transportavimas() {}
    public static ryšys Atverti(String ADDRESS, int prievado_numeris) throws Į_I_išimtis {
        try { return ryšys.Atverti(ADDRESS, prievado_numeris);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public static gauti_jungtis 수신열기(int prievado_numeris) throws Į_I_išimtis {
        try { return gauti_jungtis.Atverti(prievado_numeris);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public static Socket Prisijungti(String ADDRESS, int jungtis_VALUE) throws Į_I_išimtis {
        try { return new Socket(ADDRESS, jungtis_VALUE);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public static ServerSocket laukti_dalyvis(int jungtis_VALUE) throws Į_I_išimtis {
        try { return new ServerSocket(jungtis_VALUE);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public static Socket gauti(ServerSocket serveris_VALUE) throws Į_I_išimtis {
        try { return serveris_VALUE.accept();
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
}
