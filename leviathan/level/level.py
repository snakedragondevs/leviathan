class Level:

    closed = False

    def is_closed(self):
        return self.closed

    def close(self):
        if self.closed:
            raise Exception("Tried to close a level which is already closed")

        for chunk in self.chunks:
            self.unload_chunk(chunk.get_x(), chunk.get_y(), False)

        self.save()

        self.unregister_generator()

        self.provider.close()
        self.provider = None
        self.block_metadata = None
        self.block_cache = None
        self.temporal_position = None

        self.closed = True
