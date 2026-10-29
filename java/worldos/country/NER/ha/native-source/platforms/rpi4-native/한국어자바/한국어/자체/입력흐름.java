// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 watsuwa_Daraja: 순서대로 들어오는 바이트를 읽는 tasha_Mashigar_bayanai. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Yi_Karatu() throws I_O_banbanchi {
        try { return 표준흐름.read();
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public int Yi_Karatu(byte[] Tarin_bayani) throws I_O_banbanchi {
        try { return 표준흐름.read(Tarin_bayani);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public int Yi_Karatu(byte[] Tarin_bayani, int Tafiyar_da, int Tsawo_Daraja) throws I_O_banbanchi {
        try { return 표준흐름.read(Tarin_bayani, Tafiyar_da, Tsawo_Daraja);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public void Rufe() throws I_O_banbanchi {
        try { 표준흐름.close();
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
}
