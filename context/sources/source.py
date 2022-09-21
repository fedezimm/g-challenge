class Source(object):

    def __init__(
        self,
        name,
        super_type = 'file',
    ):
        self.name = name
        self.super_type = super_type

    def __str__(self):
        return f'Source(name: {self.name}, super_type: {self.super_type})'