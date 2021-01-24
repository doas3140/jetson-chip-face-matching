package lt.softemia.cardfacematching;

import net.sf.scuba.smartcards.CardService;
import net.sf.scuba.smartcards.CardServiceException;
import net.sf.scuba.smartcards.CommandAPDU;
import net.sf.scuba.smartcards.ResponseAPDU;

import javax.smartcardio.*;
import java.util.Arrays;
import java.util.List;

public class MyCardService extends CardService {

    private Card card;
    private CardChannel channel;
    private CardTerminal terminal;

    public MyCardService(CardTerminal terminal) {
        this.terminal = terminal;
    }

    @Override
    public void open() throws CardServiceException {
        try {
            card = terminal.connect("*");
            channel = card.getBasicChannel();
        } catch (CardException e){
            throw new CardServiceException("Failed to connect to the card", e);
        }
    }

    @Override
    public boolean isOpen() {
        return card != null && channel != null;
    }

    @Override
    public ResponseAPDU transmit(CommandAPDU commandAPDU) throws CardServiceException {
        javax.smartcardio.CommandAPDU cmd = new javax.smartcardio.CommandAPDU(commandAPDU.getBytes());
        try {
            System.out.println(channel);
            javax.smartcardio.ResponseAPDU res = channel.transmit(cmd);
            return new ResponseAPDU(res.getBytes());
        } catch (CardException e) {
            throw new CardServiceException("Transmit failed", e);
        }
    }

    @Override
    public byte[] getATR() throws CardServiceException {
        return card.getATR().getBytes();
    }

    @Override
    public void close() {
        try {
            card.disconnect(false);
        } catch (CardException e) {
            e.printStackTrace();
        }
    }

    @Override
    public boolean isConnectionLost(Exception e) {
        return false;
    }
}
