// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 урсгал_утга: 순서대로 들어오는 바이트를 읽는 суваг_оролт. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Унших() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public int Унших(byte[] өгөгдөл) throws 입출력예외 {
        try { return 표준흐름.read(өгөгдөл);
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public int Унших(byte[] өгөгдөл, int Ажиллуулах, int урт_утга) throws 입출력예외 {
        try { return 표준흐름.read(өгөгдөл, Ажиллуулах, урт_утга);
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public void Хаах() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
}
