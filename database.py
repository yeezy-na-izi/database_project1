class DataBase:
    def __init__(self, name: str, structure: dict[str, (type, bool)]):
        if not name.endswith(".csv"):
            name += ".csv"

        structure['id'] = (int, True)

        self.name = name
        self.structure = structure
        self.index = 0

        self.all_fields = set()
        self.generate_all_field()

        self.required_fields = set()
        self.generate_required_fields()

        self.sorted_all_fields = list(sorted(self.all_fields))
        self.fields_id = {self.sorted_all_fields[i]: i + 1 for i in range(len(self.sorted_all_fields))}
        self.fields_id['id'] = 0

        # TODO: если файл пустой - записать филды, если нет, проверить на соответствие, если его нет -> удалить все к
        #  чертям)

        with open(self.name, 'w') as file:
            string = 'id'
            for field_name in self.sorted_all_fields:
                string += f',{field_name}'
            string += '\n'

            file.write(string)

    def generate_required_fields(self):
        for key in self.all_fields:
            if self.structure[key][1]:
                self.required_fields.add(key)

    def generate_all_field(self):
        self.all_fields = set(self.structure.keys()) - {"id"}

    def validate(self, obj: dict):
        for field in self.required_fields:
            if field not in obj:
                raise KeyError(f"Field - {field} is required")

        for field in obj:
            if field not in self.all_fields and field != 'id':
                raise KeyError(f"Unknown field - {field}")

        for field in self.all_fields:
            if field in obj and type(obj[field]) != self.structure[field][0]:
                raise TypeError(f"Field - {field} must be {self.structure[field][0]} but {type(obj[field])} received")

    def from_str_to_record(self, string) -> dict:
        returned_obj = dict()
        field_of_record = string.split(',')

        for field_name in self.fields_id:
            raw_field = field_of_record[self.fields_id[field_name]].strip()

            if raw_field == "":
                returned_obj[field_name] = None
            else:
                returned_obj[field_name] = self.structure[field_name][0](raw_field)

        return returned_obj

    def get(self, field_name, value) -> list[dict]:
        """
        Alternative:
            SELECT * FROM <self.name> WHERE <field> = <result>;

        :return:
        """
        if field_name not in self.fields_id:
            raise KeyError(f"Unknown field - {field_name}")

        if not value:
            value = ""
        else:
            value = str(value)
        index = self.fields_id[field_name]
        returned_records = []

        with open(self.name) as file:
            file.readline()  # read header

            for record in file:
                split_record = record.split(',')

                if len(split_record) > index and split_record[index].strip() == value:
                    returned_records.append(self.from_str_to_record(record))

        return returned_records

    def create(self, obj: dict, index=None):
        self.validate(obj)
        if index is not None:
            flag = False
        else:
            flag = True
            index = self.index

        string_to_file = str(index)

        for key in self.sorted_all_fields:
            string_to_file += f",{obj.get(key, '')}"
        string_to_file += '\n'

        with open(self.name, 'a') as file:
            file.write(string_to_file)

        if flag:
            self.index += 1

    def delete(self, field_name, value):
        """
        Alternative:
            DELETE * FROM <self.name> WHERE <field> = <result>;

        :return:
        """
        if field_name not in self.fields_id:
            raise KeyError(f"Unknown field - {field_name}")

        if not value:
            value = ""
        else:
            value = str(value)
        index = self.fields_id[field_name]
        for_save = []

        with open(self.name) as file:
            for_save.append(file.readline())  # read header

            for record in file:
                split_record = record.split(',')

                if len(split_record) > index and not split_record[index].strip() == value:
                    for_save.append(record)

        with open(self.name, 'w') as file:
            for record in for_save:
                file.write(record)

    def update(self, field_for_search, result_for_search, field_for_update, result_for_update):
        """
        Alternative:
            UPDATE <self.name> WHERE <field_for_search> = 2003;

        :return:
        """
        if field_for_update not in self.fields_id:
            raise KeyError(f"Unknown field - {field_for_update}")
        if type(result_for_update) != self.structure[field_for_update][0]:
            raise TypeError(
                f"Field - {field_for_update} must be {self.structure[field_for_update][0]} but {type(result_for_search)} received")

        objects_for_update = self.get(field_for_search, result_for_search)
        self.delete(field_for_search, result_for_search)

        for obj in objects_for_update:
            obj[field_for_update] = result_for_update
            self.create(obj, obj['id'])
