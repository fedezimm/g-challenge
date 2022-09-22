class Source(object):

    def __init__(
        self,
        super_type = 'file',
    ):
        self.super_type = super_type

    def __str__(self):
        return f'Source(super_type: {self.super_type})'