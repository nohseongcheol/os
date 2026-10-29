// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;

/** Izvade(出力)과 Stream_VALUE: 순서를 보존해 내보내는 바이트의 Kanāls_ievade. */
public final class ražojums_Stream {
    private final java.io.OutputStream 표준흐름;
    ražojums_Stream(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Rakstīt(int VALUE) throws ievadizvade_izņēmums {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public void Rakstīt(byte[] dati) throws ievadizvade_izņēmums {
        try { 표준흐름.write(dati);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public void Rakstīt(byte[] dati, int Palaist, int 길이) throws ievadizvade_izņēmums {
        try { 표준흐름.write(dati, Palaist, 길이);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public void 내보내기() throws ievadizvade_izņēmums {
        try { 표준흐름.flush();
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public void Aizvērt() throws ievadizvade_izņēmums {
        try { 표준흐름.close();
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
}
