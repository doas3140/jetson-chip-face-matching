package lt.softemia.cardfacematching;

import jssc.SerialPortException;
import net.sf.scuba.smartcards.CardServiceException;
import py4j.GatewayServer;

import javax.smartcardio.*;
import java.io.*;

public class ServerEntryPoint {
    private final MrzReader mrz_reader = new MrzReader();
    private final CardReader card_reader = new CardReader(0);
    private final MrzAndImageReader mrz_and_image_reader;

    public ServerEntryPoint() throws IOException, CardException {
        mrz_and_image_reader = new MrzAndImageReader(card_reader, mrz_reader);
    }

    public MrzReader getMrzReader(){
        return mrz_reader;
    }
    public CardReader getCardReader(){
        return card_reader;
    }
    public MrzAndImageReader getMrzAndImageReader(){
        return mrz_and_image_reader;
    }

    public static void main(String[] args) throws CardException, IOException {
        GatewayServer gatewayServer = new GatewayServer(new ServerEntryPoint());
        gatewayServer.start();
        System.out.println("Gateway Server Started");
    }

    public static void test() throws CardException, IOException, CardServiceException, SerialPortException{
        System.out.println("started test");
        MrzReader mrz_reader = new MrzReader();
        mrz_reader.setPort("COM3", 10000); // "/dev/ttyACM0"
        long t0 = System.currentTimeMillis();
        String mrz = mrz_reader.read();
        System.out.println("[TIME] mrz: " + (System.currentTimeMillis() - t0));
        CardReader cr = new CardReader(0);
        var img = cr.readImage(mrz);
        System.out.println("[TIME] card: " + (System.currentTimeMillis() - t0));
    }
}
