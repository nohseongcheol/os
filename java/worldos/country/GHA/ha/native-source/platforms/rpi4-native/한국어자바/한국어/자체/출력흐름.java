// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 watsuwa_Daraja: 순서를 보존해 내보내는 바이트의 tasha_Mashigar_bayanai. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Yi_Rubutu(int Daraja) throws I_O_banbanchi {
        try { 표준흐름.write(Daraja);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public void Yi_Rubutu(byte[] Tarin_bayani) throws I_O_banbanchi {
        try { 표준흐름.write(Tarin_bayani);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public void Yi_Rubutu(byte[] Tarin_bayani, int Tafiyar_da, int Tsawo_Daraja) throws I_O_banbanchi {
        try { 표준흐름.write(Tarin_bayani, Tafiyar_da, Tsawo_Daraja);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public void 내보내기() throws I_O_banbanchi {
        try { 표준흐름.flush();
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public void Rufe() throws I_O_banbanchi {
        try { 표준흐름.close();
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
}
