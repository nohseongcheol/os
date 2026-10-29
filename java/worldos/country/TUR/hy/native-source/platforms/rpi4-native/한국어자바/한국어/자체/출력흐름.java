// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Ելք(出力)과 հոսք_արժեք: 순서를 보존해 내보내는 바이트의 կապուղի_մուտքագրում. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Գրել(int արժեք) throws 입출력예외 {
        try { 표준흐름.write(արժեք);
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public void Գրել(byte[] տվյալ) throws 입출력예외 {
        try { 표준흐름.write(տվյալ);
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public void Գրել(byte[] տվյալ, int Գործարկել, int տեւողություն_արժեք) throws 입출력예외 {
        try { 표준흐름.write(տվյալ, Գործարկել, տեւողություն_արժեք);
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public void Փակ() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
}
