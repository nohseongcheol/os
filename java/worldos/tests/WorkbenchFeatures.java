// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.*;
import java.nio.file.*;
import java.util.*;
import java.util.List;
import java.util.jar.*;
import java.util.concurrent.atomic.*;
import javax.swing.*;

public final class WorkbenchFeatures {
    static List<Component> components(Container parent) {
        List<Component> result=new ArrayList<>();
        for(Component child:parent.getComponents()){result.add(child);if(child instanceof Container)result.addAll(components((Container)child));}
        return result;
    }
    public static void main(String[] arguments) {
        try { verify(arguments); } catch (Throwable error) { error.printStackTrace(); System.exit(1); }
    }
    static void verify(String[] arguments) throws Exception {
        Properties labels=new Properties();String main;
        try(JarFile jar=new JarFile("/opt/worldos/edition.jar")){
            main=jar.getManifest().getMainAttributes().getValue("Main-Class");
            try(Reader reader=new InputStreamReader(jar.getInputStream(jar.getJarEntry("messages.properties")),java.nio.charset.StandardCharsets.UTF_8)){labels.load(reader);}
        }
        URLClassLoader loader=new URLClassLoader(new URL[]{new File("/opt/worldos/edition.jar").toURI().toURL()});
        Class.forName(main,true,loader).getMethod("main",String[].class).invoke(null,(Object)new String[0]);
        SwingUtilities.invokeAndWait(()->{});
        AtomicReference<JFrame> window=new AtomicReference<>();
        for(Frame frame:Frame.getFrames())if(frame instanceof JFrame && frame.isVisible())window.set((JFrame)frame);
        if(window.get()==null)throw new AssertionError("No workbench window");
        List<JTextField> fields=new ArrayList<>();List<JTextArea> areas=new ArrayList<>();AtomicReference<JButton> run=new AtomicReference<>();
        for(Component component:components(window.get())){
            if(component instanceof JTextField)fields.add((JTextField)component);
            if(component instanceof JTextArea)areas.add((JTextArea)component);
            if(component instanceof JButton && ((JButton)component).getText().equals(labels.getProperty("run")))run.set((JButton)component);
        }
        if(fields.size()!=3 || areas.size()!=2 || run.get()==null)throw new AssertionError("Workbench controls missing");
        // RTL split panes expose children in a different order. Identify their roles.
        JTextArea editor=areas.stream().filter(JTextArea::isEditable).findFirst().orElseThrow();
        JTextArea console=areas.stream().filter(area->!area.isEditable()).findFirst().orElseThrow();
        if(editor.getLocationOnScreen().y>=console.getLocationOnScreen().y)
            throw new AssertionError("The source editor must remain above the output pane");
        JTextField filename=fields.stream().filter(field->field.getColumns()==26).findFirst().orElseThrow();
        JTextField classname=fields.stream().filter(field->field.getColumns()==15).findFirst().orElseThrow();
        JTextField argumentsField=fields.stream().filter(field->field.getColumns()==25).findFirst().orElseThrow();
        AtomicReference<String> initial=new AtomicReference<>();
        SwingUtilities.invokeAndWait(()->initial.set(editor.getText()));
        if(!initial.get().contains("public class"))throw new AssertionError("Starter source was not installed: "+console.getText());
        System.out.println("PASS localized-starter-source-loaded");
        String source="public class 검증 { public static void main(String[] 인수) { System.out.println(\"UI_RUN_OK:\"+인수[0]); } }";
        SwingUtilities.invokeAndWait(()->{filename.setText("검증.java");classname.setText("검증");argumentsField.setText("\"한글 argument\"");editor.setText(source);run.get().doClick();});
        AtomicReference<String> output=new AtomicReference<>("");
        for(int attempt=0;attempt<180;attempt++){
            SwingUtilities.invokeAndWait(()->output.set(console.getText()));
            if(output.get().contains("UI_RUN_OK:한글 argument"))break;
            Thread.sleep(500);
        }
        if(!output.get().contains("UI_RUN_OK:한글 argument"))throw new AssertionError(output.get());
        if(!Files.readString(Paths.get("/home/user/workspace/검증.java")).equals(source))throw new AssertionError("Source save mismatch");
        System.out.println("PASS workbench-edit-save-compile-run-unicode-arguments");
        Robot robot=new Robot();robot.waitForIdle();Thread.sleep(500);
        javax.imageio.ImageIO.write(robot.createScreenCapture(new Rectangle(Toolkit.getDefaultToolkit().getScreenSize())),"png",new File("/home/user/workspace/workbench.png"));
        System.out.println("WORLDOS_WORKBENCH_OK");System.exit(0);
    }
}
