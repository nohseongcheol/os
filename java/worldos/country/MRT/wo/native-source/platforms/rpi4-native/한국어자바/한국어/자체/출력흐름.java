// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 dawal_xëyma: 순서를 보존해 내보내는 바이트의 Yoon_dugal_xabaar. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void biir(int xëyma) throws 입출력예외 {
        try { 표준흐름.write(xëyma);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public void biir(byte[] mbir) throws 입출력예외 {
        try { 표준흐름.write(mbir);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public void biir(byte[] mbir, int daw, int diir_xëyma) throws 입출력예외 {
        try { 표준흐름.write(mbir, daw, diir_xëyma);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public void Tej() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
}
