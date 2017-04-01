class Sensor:
    def __init__(self, read_stream):
        """
        Create a new sensor. 
        
        :param read_stream: A stream object (serial, file, etc.)
        """

        self.read_stream = read_stream

    def read_data(self) -> str:
        """
        Reads data from the stream until a newline character is encountered. 
        """

        result = self.read_stream.readline()
        return result

    def close(self):
        """
        Closes the underlying stream object. This sensor will no longer be able to be read from.
        """

        stream.close()
