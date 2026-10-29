// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Выхад(出力)과 паток_значэнне: 순서를 보존해 내보내는 바이트의 канал_увядзенне. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Запіс(int значэнне) throws увод_вывад_выключэнне {
        try { 표준흐름.write(значэнне);
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public void Запіс(byte[] дадзеныя) throws увод_вывад_выключэнне {
        try { 표준흐름.write(дадзеныя);
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public void Запіс(byte[] дадзеныя, int Выканаць, int даўжыня_значэнне) throws увод_вывад_выключэнне {
        try { 표준흐름.write(дадзеныя, Выканаць, даўжыня_значэнне);
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public void 내보내기() throws увод_вывад_выключэнне {
        try { 표준흐름.flush();
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public void Закрыць() throws увод_вывад_выключэнне {
        try { 표준흐름.close();
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
}
