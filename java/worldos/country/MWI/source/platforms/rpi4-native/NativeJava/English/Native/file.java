// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** Keeps the familiar file concept. Current storage consists of RAM files lost on reboot. */
public final class file {
    private file() {}
    public static byte[] readByteValue(String name) throws InputOutputException {
        try {
        FileInputStream streamValue = new FileInputStream(name);
        try {
            byte[] temporaryValue = new byte[16384]; int number = 0, value;
            while ((value = streamValue.read()) != -1) { if (number == temporaryValue.length) throw new InputOutputException("File size limit"); temporaryValue[number++] = (byte)value; }
            byte[] result = new byte[number]; System.arraycopy(temporaryValue, 0, result, 0, number); return result;
        } finally { streamValue.close(); }
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public static void writeByteValue(String name, byte[] contentValue) throws InputOutputException {
        try {
        FileOutputStream streamValue = new FileOutputStream(name);
        try { for (int loopIndex = 0; loopIndex < contentValue.length; loopIndex++) streamValue.write(contentValue[loopIndex] & 255); } finally { streamValue.close(); }
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public static String read(String name) throws InputOutputException {
        try { return Characters.decryptData(readByteValue(name));
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public static void write(String name, String contentValue) throws InputOutputException {
        try { writeByteValue(name, Characters.encode(contentValue));
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
}
