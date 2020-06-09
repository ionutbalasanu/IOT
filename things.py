from stream import Stream
from threading import Thread
from util import Util
import sys

config_file_name = './test_dir/'

if __name__ == '__main__':
    sensor_name = sys.argv[1]
    config_file_name = config_file_name + str(sensor_name) + "_config"
    print(config_file_name)
    FIFO_NAME = Stream.DEFAULT_FIFO_NAME
    reader_endpoint = None
    thing_reader_stream = Stream()
    try:
        reader_endpoint = thing_reader_stream.create_reader_pipe(FIFO_NAME)

        try:
            while thing_reader_stream.get_threads_stop_flag() is False:
                print("Starting the listening Thread !")
                listening_thread = Thread(target=thing_reader_stream.listen_to_pipe_polling, args=(reader_endpoint,))
                listening_thread.daemon = True
                listening_thread.start()
                listening_thread.join()

                if thing_reader_stream.get_received_value() == b'GET':
                    writer_endpoint = thing_reader_stream.check_endpoint_exists(Stream.TEMPORARY_RESPONSE_FIFO_NAME)
                    if writer_endpoint is False:
                        writer_endpoint = thing_reader_stream.connect_to_pipe(Stream.TEMPORARY_RESPONSE_FIFO_NAME, False)

                    message = Util.create_response_msg(Util.read_temp(config_file_name))
                    Stream.write_to_pipe(writer_endpoint, message)

                elif thing_reader_stream.get_received_value() == b'EOF':
                    thing_reader_stream.disconnect_pipe(Stream.TEMPORARY_RESPONSE_FIFO_NAME)

        except KeyboardInterrupt as kbd_ex:
            pass

        finally:
            pass
    finally:
        thing_reader_stream.destroy_reader_pipe(FIFO_NAME)
