// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
import java.net.*;
public final class connectionTransport {
    private connectionTransport() {}
    public static Connection open(String address, int portNumber) throws InputOutputException {
        try { return Connection.open(address, portNumber);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public static receivePort openReceiver(int portNumber) throws InputOutputException {
        try { return receivePort.open(portNumber);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public static Socket connect(String address, int portValue) throws InputOutputException {
        try { return new Socket(address, portValue);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public static ServerSocket listenEndpoint(int portValue) throws InputOutputException {
        try { return new ServerSocket(portValue);
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
    public static Socket receive(ServerSocket serverValue) throws InputOutputException {
        try { return serverValue.accept();
        } catch (java.io.IOException error) { throw convertException.inputOutput(error); }
        catch (RuntimeException error) { throw convertException.executeCommand(error); }
    }
}
