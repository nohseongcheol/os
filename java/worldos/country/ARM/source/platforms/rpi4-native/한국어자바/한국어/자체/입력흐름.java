// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 հոսք_արժեք: 순서대로 들어오는 바이트를 읽는 կապուղի_մուտքագրում. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Ընթերցում() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public int Ընթերցում(byte[] տվյալ) throws 입출력예외 {
        try { return 표준흐름.read(տվյալ);
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public int Ընթերցում(byte[] տվյալ, int Գործարկել, int տեւողություն_արժեք) throws 입출력예외 {
        try { return 표준흐름.read(տվյալ, Գործարկել, տեւողություն_արժեք);
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public void Փակ() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
}
