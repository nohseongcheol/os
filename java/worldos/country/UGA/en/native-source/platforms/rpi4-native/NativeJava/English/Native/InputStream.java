// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** Channel for reading incoming bytes in order. */
public final class InputStream {
    private final java.io.InputStream standardStream;
    InputStream(java.io.InputStream standardStream) { this.standardStream = standardStream; }
    public int read() throws InputOutputException {
        try { return standardStream.read();
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public int read(byte[] data) throws InputOutputException {
        try { return standardStream.read(data);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public int read(byte[] data, int run, int lengthValue) throws InputOutputException {
        try { return standardStream.read(data, run, lengthValue);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public void close() throws InputOutputException {
        try { standardStream.close();
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
}
