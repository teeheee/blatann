import logging
import datetime

from blatann import BleDevice
from blatann.gap import advertising
from blatann.utils import setup_logger
from blatann.services import glucose
from blatann.waitables import GenericWaitable


logger = setup_logger(level="DEBUG")


def on_connect(peer, event_args):
    """
    :type peer: blatann.peer.Peer
    :type event_args: None
    """
    if peer:
        logger.info("Connected to peer")
    else:
        logger.warning("Connection timed out")


def on_disconnect(peer, event_args):
    logger.info("Disconnected from peer, reason: {}".format(event_args.reason))


def main(serial_port):
    ble_device = BleDevice(serial_port)
    ble_device.open()

    glucose_database = glucose.BasicGlucoseDatabase()
    glucose.add_glucose_server(ble_device.database, glucose_database)

    # Fake some measurement stuff, basic for now

    now = datetime.datetime.now()

    for i in range(1, 15):
        t = now + datetime.timedelta(minutes=i*5)
        v = 12.345 * i
        m = glucose.GlucoseMeasurement(i, t, value=v)
        # Add some records with context
        if i % 4 == 0:
            context = glucose.GlucoseContext(i, carb_type=glucose.CarbohydrateType.breakfast, carbs_grams=50*i,
                                             medication_type=glucose.MedicationType.long_acting_insulin,
                                             medication_units=glucose.MedicationUnits.milligrams,
                                             medication_value=100*i, hba1c_percent=i*6)
            m.context = context

        glucose_database.add_record(m)

    logger.info("Advertising")
    adv_data = advertising.AdvertisingData(local_name="Glucose Test", flags=0x06,
                                           service_uuid16s=glucose.GLUCOSE_SERVICE_UUID)
    ble_device.advertiser.set_advertise_data(adv_data)
    ble_device.client.on_connect.register(on_connect)
    ble_device.client.on_disconnect.register(on_disconnect)
    ble_device.client.set_connection_parameters(15, 30, 4000)
    ble_device.advertiser.start(timeout_sec=0, auto_restart=True)
    w = GenericWaitable()
    w.wait(60*30, exception_on_timeout=False)
    logger.info("Done")
    ble_device.close()


if __name__ == '__main__':
    main("COM49")
