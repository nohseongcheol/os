// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자체;

/** 출력(出力)과 Stream_ixabiso: 순서를 보존해 내보내는 바이트의 ijelo_ufako_nkcukacha. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Bhala(int ixabiso) throws 입출력예외 {
        try { 표준흐름.write(ixabiso);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public void Bhala(byte[] iingcombolo) throws 입출력예외 {
        try { 표준흐름.write(iingcombolo);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public void Bhala(byte[] iingcombolo, int Phumeza, int ubude_ixabiso) throws 입출력예외 {
        try { 표준흐름.write(iingcombolo, Phumeza, ubude_ixabiso);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public void Vala() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
}
