class Sensor:
    def __init__(self, read_stream):
        """
        Create a new sensor. 
        
        :param read_stream: A stream object (serial, file, etc.)
        """

        self.read_stream = read_stream

    def read_data(self):
        """
        Reads data from the stream until a newline character is encountered. 
        """

        with self.read_stream as stream:
            result = stream.readline()
        return result
