// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;

/** 입력(入力)과 Stream_VALUE: 순서대로 들어오는 바이트를 읽는 Kanāls_ievade. */
public final class ievades_straume {
    private final java.io.InputStream 표준흐름;
    ievades_straume(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Lasīt() throws ievadizvade_izņēmums {
        try { return 표준흐름.read();
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public int Lasīt(byte[] dati) throws ievadizvade_izņēmums {
        try { return 표준흐름.read(dati);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public int Lasīt(byte[] dati, int Palaist, int 길이) throws ievadizvade_izņēmums {
        try { return 표준흐름.read(dati, Palaist, 길이);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public void Aizvērt() throws ievadizvade_izņēmums {
        try { 표준흐름.close();
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
}
