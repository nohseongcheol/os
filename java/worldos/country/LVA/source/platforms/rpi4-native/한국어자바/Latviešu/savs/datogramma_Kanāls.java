// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;

/** datogramma(電文)·Kanāls_ievade(通路): 경계를 가진 UDP 자료를 주고받는 dalībnieks. */
public final class datogramma_Kanāls {
    private final java.net.DatagramSocket 표준종단;
    private datogramma_Kanāls(int porta_numurs) throws ievadizvade_izņēmums {
        try { 표준종단 = 통신.Atvērt(porta_numurs);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public static datogramma_Kanāls Atvērt(int porta_numurs) throws ievadizvade_izņēmums {
        try { return new datogramma_Kanāls(porta_numurs);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public void sūtīt(String adrese, int porta_numurs, String dati) throws ievadizvade_izņēmums {
        try { 통신.sūtīt(표준종단, adrese, porta_numurs, dati);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public String saņemt() throws ievadizvade_izņēmums {
        try { return 통신.saņemt(표준종단);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public void NOILGUMS(int 밀리초) throws ievadizvade_izņēmums {
        try { 통신.NOILGUMS(표준종단, 밀리초);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public int porta_numurs() { return 표준종단.getLocalPort(); }
    public boolean informācijas_tehnoloģija_slēgts() { return 표준종단.isClosed(); }
    public void Aizvērt() { 통신.Aizvērt(표준종단); }
}
