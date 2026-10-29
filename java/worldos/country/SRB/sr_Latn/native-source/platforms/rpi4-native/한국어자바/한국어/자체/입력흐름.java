// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 tok_VALUE: 순서대로 들어오는 바이트를 읽는 Kanal_stavka. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int 읽기() throws U_I_izuzetak {
        try { return 표준흐름.read();
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public int 읽기(byte[] podaci) throws U_I_izuzetak {
        try { return 표준흐름.read(podaci);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public int 읽기(byte[] podaci, int koristiti, int 길이) throws U_I_izuzetak {
        try { return 표준흐름.read(podaci, koristiti, 길이);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public void Zatvori() throws U_I_izuzetak {
        try { 표준흐름.close();
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
}
