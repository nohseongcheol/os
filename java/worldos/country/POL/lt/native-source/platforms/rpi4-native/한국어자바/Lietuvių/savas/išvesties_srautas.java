// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;

/** Išvestis(出力)과 Stream_VALUE: 순서를 보존해 내보내는 바이트의 kanalas_įrašas. */
public final class išvesties_srautas {
    private final java.io.OutputStream 표준흐름;
    išvesties_srautas(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Rašymas(int VALUE) throws Į_I_išimtis {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public void Rašymas(byte[] duomenys) throws Į_I_išimtis {
        try { 표준흐름.write(duomenys);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public void Rašymas(byte[] duomenys, int Paleisti, int 길이) throws Į_I_išimtis {
        try { 표준흐름.write(duomenys, Paleisti, 길이);
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public void 내보내기() throws Į_I_išimtis {
        try { 표준흐름.flush();
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public void Užverti() throws Į_I_išimtis {
        try { 표준흐름.close();
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
}
