// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол.자체;

/** 출력(出力)과 урсгал_утга: 순서를 보존해 내보내는 바이트의 суваг_оролт. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Бичих(int утга) throws 입출력예외 {
        try { 표준흐름.write(утга);
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public void Бичих(byte[] өгөгдөл) throws 입출력예외 {
        try { 표준흐름.write(өгөгдөл);
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public void Бичих(byte[] өгөгдөл, int Ажиллуулах, int урт_утга) throws 입출력예외 {
        try { 표준흐름.write(өгөгдөл, Ажиллуулах, урт_утга);
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public void Хаах() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
}
