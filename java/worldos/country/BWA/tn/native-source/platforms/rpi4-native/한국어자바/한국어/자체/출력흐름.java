// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 moela_Boleng: 순서를 보존해 내보내는 바이트의 mosele_tsenyo. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void kwala(int Boleng) throws 입출력예외 {
        try { 표준흐름.write(Boleng);
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public void kwala(byte[] tshedimosetso) throws 입출력예외 {
        try { 표준흐름.write(tshedimosetso);
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public void kwala(byte[] tshedimosetso, int dirisa, int boleele_Boleng) throws 입출력예외 {
        try { 표준흐름.write(tshedimosetso, dirisa, boleele_Boleng);
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public void tswala() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
}
