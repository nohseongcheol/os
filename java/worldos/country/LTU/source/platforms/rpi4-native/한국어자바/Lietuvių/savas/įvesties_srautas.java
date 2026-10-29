// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;

/** 입력(入力)과 Stream_VALUE: 순서대로 들어오는 바이트를 읽는 kanalas_įrašas. */
public final class įvesties_srautas {
    private final java.io.InputStream 표준흐름;
    įvesties_srautas(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Skaitymas() throws Į_I_išimtis {
        try { return 표준흐름.read();
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public int Skaitymas(byte[] duomenys) throws Į_I_išimtis {
        try { return 표준흐름.read(duomenys);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public int Skaitymas(byte[] duomenys, int Paleisti, int 길이) throws Į_I_išimtis {
        try { return 표준흐름.read(duomenys, Paleisti, 길이);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public void Užverti() throws Į_I_išimtis {
        try { 표준흐름.close();
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
}
