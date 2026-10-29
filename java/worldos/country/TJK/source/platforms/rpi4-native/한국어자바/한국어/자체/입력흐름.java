// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 ҷараён_қимат: 순서대로 들어오는 바이트를 읽는 канал_ворида. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Хондан() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public int Хондан(byte[] иттилоот) throws 입출력예외 {
        try { return 표준흐름.read(иттилоот);
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public int Хондан(byte[] иттилоот, int порча, int дарозӣ_қимат) throws 입출력예외 {
        try { return 표준흐름.read(иттилоот, порча, дарозӣ_қимат);
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public void Пӯшидан() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
}
