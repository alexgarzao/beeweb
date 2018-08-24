class Files:
    def __init__(self, path=""):
        self.path = path
        self.files = {}

    def add(self, id, filename):
        if self.files.get(id) != None:
            raise DuplicatedFileException("File id {} already exists".format(id))

        file = File(id, filename)
        self.files[id] = file

        return file

    def get(self, id):
        file = self.files.get(id)
        if not file:
            possible = ','.join(list(self.files))
            raise NotFoundFileException("File id {} not found. Possible values: {}".format(id, possible))

        return file

    def get_filename(self, id):
        file = self.get(id)
        return self.path + "/" + file.filename


class File:
    def __init__(self, id, filename):
        self.id = id
        self.filename = filename


class DuplicatedFileException(Exception):
    pass


class NotFoundFileException(Exception):
    pass
