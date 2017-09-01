class correction():
    def __getitem__(self, name):
        return getattr(self, name)
    def __setitem__(self, name, value):
        return setattr(self, name, value)
    def __delitem__(self, name):
        return delattr(self, name)
    def __contains__(self, name):
        return hasattr(self, name)

bounds = {
    "x": [0,1000],
    "y": [0,700]
}
FRAME_RATE = 70
INTERVAL = 1000 / FRAME_RATE

DRAG = 1
gravity = 50 * 9.8 / FRAME_RATE