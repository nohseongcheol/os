// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;

/** 입력(入力)과 Stream_VALUE: 순서대로 들어오는 바이트를 읽는 rás_færsla. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Lestur() throws I_Ú_undantekning {
        try { return 표준흐름.read();
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public int Lestur(byte[] gögn) throws I_Ú_undantekning {
        try { return 표준흐름.read(gögn);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public int Lestur(byte[] gögn, int Keyra_2, int lengd_VALUE) throws I_Ú_undantekning {
        try { return 표준흐름.read(gögn, Keyra_2, lengd_VALUE);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public void Loka() throws I_Ú_undantekning {
        try { 표준흐름.close();
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
}
