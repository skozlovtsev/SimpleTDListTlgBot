import json


class MyJsonWorks:
    def __init__(self, path, load_data=True):
        self.__path = path
        self.load_data = load_data
        self.__data = {}
        self.__put(self.read())

    def __put(self, data):
        if self.load_data:
            self.__data = data

    def __call__(self):
        return self.__data

    def read(self):
        try:
            with open(self.__path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def write(self, data: dict):
        with open(self.__path, 'w') as file:
            json.dump(data, file, indent=4)
            self.__put(data)

    def add(self, item: dict):
        if self.__data == {}:
            self.__data = self.read()
        if [*item] in [*self.__data]:
            self.__data.update(item)
        else:
            self.__data[[*item][0]] = list(item.values())[0]
        self.write(self.__data)

    def delete(self, key):
        if self.__data == {}:
            self.__data = self.read()
        self.__data.pop(key)
        self.write(self.__data)


if __name__ == '__main__':
    f = MyJsonWorks('somejn.json')
    print(f())
    f.write({"name": "Jon", "age": 30})
    print(f())
    f.add({"gender": "male"})
    print(f())
    f.delete("name")
    print(f())