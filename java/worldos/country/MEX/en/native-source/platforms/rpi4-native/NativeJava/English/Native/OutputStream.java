// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** Channel for writing outgoing bytes in order. */
public final class OutputStream {
    private final java.io.OutputStream standardStream;
    OutputStream(java.io.OutputStream standardStream) { this.standardStream = standardStream; }
    public void write(int value) throws InputOutputException {
        try { standardStream.write(value);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public void write(byte[] data) throws InputOutputException {
        try { standardStream.write(data);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public void write(byte[] data, int run, int lengthValue) throws InputOutputException {
        try { standardStream.write(data, run, lengthValue);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public void emitValue() throws InputOutputException {
        try { standardStream.flush();
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public void close() throws InputOutputException {
        try { standardStream.close();
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
}
