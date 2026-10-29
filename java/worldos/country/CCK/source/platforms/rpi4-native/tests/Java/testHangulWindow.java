// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import English.Native.window;
import English.Native.Widget;
import English.Native.*;

public class testHangulWindow implements RunnableTask, ActionReceiver {
    window Screen;
    label README;
    TextField inputValue;
    public void executeTask() {
        Checks.require(EventQueue.isEventDispatching(), "English Screen performTask 큐");
        Screen = new window("English library window", 400, 280);
        README = Widget.tagValue("한글로 Java 코딩", 20, 20, 340, 30);
        inputValue = Widget.TextField("name", 20, 65, 340, 30);
        Screen.addElement(README);
        Screen.addElement(inputValue);
        Screen.addElement(Widget.button("greet", 20, 110, 180, 32, this));
        Screen.showWindow();
        Output.writeLine("KOREAN SWING READY");
    }
    public void receiveAction(ActionNotice event) {
        Checks.require(EventQueue.isEventDispatching(), "English action 되부름");
        Checks.require(event.index() == 1001 && event.eventSource() instanceof button, "English event 객체와 originValue");
        Checks.require(!((Object)event.eventSource() instanceof javax.swing.JButton), "표준 단추와 독립된 formatValue");
        Checks.require(!((Object)event instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 formatValue");
        README.writeText("안녕하세요 " + inputValue.readText());
        Output.writeLine("KOREAN SWING CLICK " + inputValue.readText());
    }
    public static void main(String[] arguments) {
        EventQueue.invokeLater(new testHangulWindow());
    }
}
