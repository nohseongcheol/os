// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Afvoer(出力)과 Stream_VALUE: 순서를 보존해 내보내는 바이트의 kanaal_inskrywing. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Skryf(int VALUE) throws I_O_uitsondering {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public void Skryf(byte[] data) throws I_O_uitsondering {
        try { 표준흐름.write(data);
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public void Skryf(byte[] data, int Loop, int lengte_VALUE) throws I_O_uitsondering {
        try { 표준흐름.write(data, Loop, lengte_VALUE);
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public void 내보내기() throws I_O_uitsondering {
        try { 표준흐름.flush();
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public void Sluit() throws I_O_uitsondering {
        try { 표준흐름.close();
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
}
