// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자체;

/** 입력(入力)과 roma_uara: 순서대로 들어오는 바이트를 읽는 hongere_tāurunga. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Pānuitia() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public int Pānuitia(byte[] raraunga) throws 입출력예외 {
        try { return 표준흐름.read(raraunga);
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public int Pānuitia(byte[] raraunga, int whakahaere, int roa_uara) throws 입출력예외 {
        try { return 표준흐름.read(raraunga, whakahaere, roa_uara);
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public void Kati() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
}
