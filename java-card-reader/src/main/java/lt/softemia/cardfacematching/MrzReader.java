package lt.softemia.cardfacematching;

import jssc.SerialPort;
import jssc.SerialPortException;
import jssc.SerialPortTimeoutException;
import net.sf.scuba.util.Hex;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Enumeration;

public class MrzReader {
    private int timeout;
    private SerialPort serialPort;

    public void setPort(String port, int timeout) throws SerialPortException {
        this.timeout = timeout;
        serialPort = new SerialPort(port);
    }

    public String read() throws IOException {
        long t0 = System.currentTimeMillis();
        try {
            serialPort.openPort();
            serialPort.setParams(SerialPort.BAUDRATE_9600, SerialPort.DATABITS_8, SerialPort.STOPBITS_1, SerialPort.PARITY_NONE);
            byte[] cmd = new byte[]{73, 0, 0};

            System.out.println("[TIME] mrz 1: " + (System.currentTimeMillis() - t0));

            serialPort.writeBytes(cmd);

            System.out.println("[TIME] mrz 2: " + (System.currentTimeMillis() - t0));

//            System.out.println("mrz sending: " + Arrays.toString(cmd));
            byte[] data = serialPort.readBytes(3, timeout);
//            System.out.println("mrz received: " + Arrays.toString(data));
            assert data[1] == 0;
            int len = data[2];
//            int len = data[1] * 256 + data[2];

            System.out.println("[TIME] mrz 3: " + (System.currentTimeMillis() - t0));

//            System.out.println("mrz sending: " + len);
            byte[] mrz = serialPort.readBytes(len, timeout);
//            System.out.println("mrz received: " + Arrays.toString(mrz));
            String out = new String(mrz, StandardCharsets.US_ASCII);
            out = out.replace("\r", "");

            System.out.println("[TIME] mrz 4: " + (System.currentTimeMillis() - t0));

            if(out.length() < 1){
                throw new IOException("Failed to read MRZ through serial port");
            }

            return out;
        } catch (SerialPortException | SerialPortTimeoutException e) {
            throw new IOException("Failed to read MRZ through serial port", e);
        } finally {
            if (serialPort.isOpened()) {
                try {
                    serialPort.closePort();
                } catch (SerialPortException e) {
                    System.out.println("Failed to close COM port");
                }
            }
        }
    }
}
