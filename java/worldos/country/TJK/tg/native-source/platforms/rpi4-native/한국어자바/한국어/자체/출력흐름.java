// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 ҷараён_қимат: 순서를 보존해 내보내는 바이트의 канал_ворида. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Навиштан(int қимат) throws 입출력예외 {
        try { 표준흐름.write(қимат);
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public void Навиштан(byte[] иттилоот) throws 입출력예외 {
        try { 표준흐름.write(иттилоот);
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public void Навиштан(byte[] иттилоот, int порча, int дарозӣ_қимат) throws 입출력예외 {
        try { 표준흐름.write(иттилоот, порча, дарозӣ_қимат);
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public void Пӯшидан() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
}
