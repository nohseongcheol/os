// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;

/** Savienoties(連結)·Kanāls_ievade(通路): 상대와 이어진 TCP byte_VALUE 흐름의 dalībnieks. */
public final class paziņa {
    private final java.net.Socket 표준연결;
    paziņa(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static paziņa Atvērt(String adrese, int porta_numurs) throws ievadizvade_izņēmums {
        try {
            return new paziņa(new java.net.Socket(adrese, porta_numurs));
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public ievades_straume 입력() throws ievadizvade_izņēmums {
        try { return new ievades_straume(표준연결.getInputStream());
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public ražojums_Stream Izvade() throws ievadizvade_izņēmums {
        try { return new ražojums_Stream(표준연결.getOutputStream());
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public void NOILGUMS(int 밀리초) throws ievadizvade_izņēmums {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public int porta_numurs() { return 표준연결.getPort(); }
    public int vietējs_porta_numurs() { return 표준연결.getLocalPort(); }
    public boolean informācijas_tehnoloģija_slēgts() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Aizvērt() throws ievadizvade_izņēmums {
        try { 표준연결.close();
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
}
