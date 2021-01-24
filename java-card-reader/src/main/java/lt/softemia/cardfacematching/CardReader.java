package lt.softemia.cardfacematching;

import jssc.SerialPortException;
import net.sf.scuba.smartcards.CardServiceException;
import org.jmrtd.BACKey;
import org.jmrtd.PassportService;
import org.jmrtd.lds.icao.DG2File;
import org.jmrtd.lds.icao.MRZInfo;
import org.jmrtd.protocol.BACResult;

import javax.smartcardio.CardException;
import javax.smartcardio.CardTerminal;
import javax.smartcardio.TerminalFactory;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class CardReader {
    public ExecutorService executor = Executors.newSingleThreadExecutor();
    PassportService passport_service;
    int dg2_bs = 1300; // block size

    public CardReader(int terminal_index) throws IOException, CardException {
        CardTerminal terminal = getTerminal(terminal_index);
        System.out.println("using terminal: |" + terminal.getName() + "|");
        MyCardService service = new MyCardService(terminal);
        passport_service = new PassportService(service, 256, 256, true, false); // SFI - Short File Identifier
    }

    public byte[] readImage(String mrz) throws CardServiceException, IOException {
        System.out.println("reading image w/ mrz: " + mrz);
        MRZInfo info = new MRZInfo(mrz);
        InputStream dg2 = readDg2(info);
        return dg2.readAllBytes();
    }

    public Future<byte[]> readImageAsync(String mrz) {
        return executor.submit(() -> readImage(mrz));
    }

    private CardTerminal getTerminal(int index) throws CardException {
        TerminalFactory factory = TerminalFactory.getDefault();
        List<CardTerminal> terminals = factory.terminals().list();
        System.out.println("Terminals: " + terminals);
        // get the first terminal
        CardTerminal terminal = terminals.get(index);
        for (CardTerminal t: terminals) {
            if (t.getName().contains("ELYCTIS")) {
                terminal = t;
            }
        }
        return terminal;
    }

    private InputStream readDg2(MRZInfo mrz) throws CardServiceException, IOException {
        long t0 = System.currentTimeMillis();

        passport_service.open();
        passport_service.sendSelectApplet(false);

        System.out.println("[TIME] dg2 1: " + (System.currentTimeMillis() - t0));

        BACKey key = new BACKey(mrz.getDocumentNumber(), mrz.getDateOfBirth(), mrz.getDateOfExpiry());
        BACResult res = passport_service.doBAC(key);

        System.out.println("[TIME] dg2 2: " + (System.currentTimeMillis() - t0));

        DG2File dg2 = new DG2File(passport_service.getInputStream(PassportService.EF_DG2, this.dg2_bs));
        InputStream is = dg2.getFaceInfos().get(0).getFaceImageInfos().get(0).getImageInputStream();

        System.out.println("[TIME] dg2 3: " + (System.currentTimeMillis() - t0));

        return is;
    }

    public void setDg2BatchSize(int bs){ dg2_bs = bs; }
}
