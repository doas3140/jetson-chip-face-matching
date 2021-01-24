package lt.softemia.cardfacematching;

import jssc.SerialPortException;
import org.jmrtd.PassportService;

import javax.smartcardio.CardException;
import javax.smartcardio.CardTerminal;
import java.io.IOException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class MrzAndImageReader {
    public ExecutorService executor = Executors.newSingleThreadExecutor();
    CardReader card_reader;
    MrzReader mrz_reader;

    public MrzAndImageReader(CardReader card_reader, MrzReader mrz_reader) {
        this.card_reader = card_reader;
        this.mrz_reader = mrz_reader;
    }

    public Future<byte[]> readImageBytesAsync(){
        return executor.submit(() -> {
            try {
                String mrz = mrz_reader.read();
                return card_reader.readImage(mrz);
            } catch (Exception e) {
                e.printStackTrace();
                return new byte[]{};
            }
        });
    }


}
