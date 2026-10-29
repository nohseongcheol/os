// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;

/** úttak(出力)과 Stream_VALUE: 순서를 보존해 내보내는 바이트의 rás_færsla. */
public final class úttak_Stream {
    private final java.io.OutputStream 표준흐름;
    úttak_Stream(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Skrift(int VALUE) throws I_Ú_undantekning {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public void Skrift(byte[] gögn) throws I_Ú_undantekning {
        try { 표준흐름.write(gögn);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public void Skrift(byte[] gögn, int Keyra_2, int lengd_VALUE) throws I_Ú_undantekning {
        try { 표준흐름.write(gögn, Keyra_2, lengd_VALUE);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public void 내보내기() throws I_Ú_undantekning {
        try { 표준흐름.flush();
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public void Loka() throws I_Ú_undantekning {
        try { 표준흐름.close();
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
}
