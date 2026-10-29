// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import English.Native.window;
import English.Native.label;
import English.Native.TextField;
import English.Native.button;
import English.Native.EventQueue;
import English.Native.Output;
import English.Native.RunnableTask;
import English.Native.ActionReceiver;
import English.Native.ActionNotice;

/** Swing window on the standalone kernel: local text input, button action, then label update. */
public class WindowExample implements RunnableTask, ActionReceiver {
    private window greetingWindow;
    private TextField nameField;
    private label greeting;
    private int greetingCount;

    public void openWindow() {
        greetingWindow = new window("en Swing", 460, 300);
        greetingWindow.addElement(new label("Hello", 20, 20, 420, 28));
        nameField = new TextField("en", 20, 64, 420, 30);
        greeting = new label("Hello", 20, 152, 420, 28);
        greetingWindow.addElement(nameField);
        greetingWindow.addElement(new button("greet", 20, 108, 180, 32, this));
        greetingWindow.addElement(greeting);
        greetingWindow.addElement(new label("F9 / Shift+Space | X", 20, 204, 420, 28));
        greetingWindow.showWindow();
        Output.writeLine("GUI examples prepare: WindowExample");
    }

    public void greet() {
        greetingCount++;
        greeting.writeText("Hello, " + nameField.readText() + "님! (" + greetingCount + ")");
        Output.writeLine("GUI Greeting: " + greeting.readText());
    }

    public void executeTask() { openWindow(); }
    public void receiveAction(ActionNotice notice) {
        Output.writeLine("action notice: " + notice.commandText());
        greet();
    }
    public static void run() {
        EventQueue.invokeLater(new WindowExample());
    }
}
