// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 dawal_xëyma: 순서대로 들어오는 바이트를 읽는 Yoon_dugal_xabaar. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int 읽기() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public int 읽기(byte[] mbir) throws 입출력예외 {
        try { return 표준흐름.read(mbir);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public int 읽기(byte[] mbir, int daw, int diir_xëyma) throws 입출력예외 {
        try { return 표준흐름.read(mbir, daw, diir_xëyma);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public void Tej() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
}
