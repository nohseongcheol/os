// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 паток_значэнне: 순서대로 들어오는 바이트를 읽는 канал_увядзенне. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Чытанне() throws увод_вывад_выключэнне {
        try { return 표준흐름.read();
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public int Чытанне(byte[] дадзеныя) throws увод_вывад_выключэнне {
        try { return 표준흐름.read(дадзеныя);
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public int Чытанне(byte[] дадзеныя, int Выканаць, int даўжыня_значэнне) throws увод_вывад_выключэнне {
        try { return 표준흐름.read(дадзеныя, Выканаць, даўжыня_значэнне);
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public void Закрыць() throws увод_вывад_выключэнне {
        try { 표준흐름.close();
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
}
