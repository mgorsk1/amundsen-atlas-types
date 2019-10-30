import json
import os

# noinspection PyPackageRequirements
from atlasclient.client import Atlas
# noinspection PyPackageRequirements
from atlasclient.exceptions import Conflict

from .types import *


class AtlasClient:
    host = os.environ.get('ATLAS_HOST', 'localhost')
    port = os.environ.get('ATLAS_PORT', 21000)
    user = os.environ.get('ATLAS_USERNAME', 'admin')
    password = os.environ.get('ATLAS_PASSWORD', 'admin')

    def driver(self):
        return Atlas(host=self.host,
                     port=self.port,
                     username=self.user,
                     password=self.password)


# noinspection PyMethodMayBeStatic
class Initializer:
    def assign_subtypes(self, ends_with="_table", super_type="Table"):
        print(f'\nAssigning {super_type} entity to all the subtypes entity definitions')
        entities_to_update = []
        for t in self.driver.typedefs:
            for e in t.entityDefs:
                if e.name.endswith(ends_with):  # Assign new entity to all the tables in atlas
                    print(f'Assigning {e.name} as a subtype of {super_type}')
                    super_types = e.superTypes  # Get a property first to inflate the relational objects
                    ent_dict = e._data
                    ent_dict["superTypes"] = super_types
                    ent_dict["superTypes"].append(super_type)
                    entities_to_update.append(ent_dict)

        typedef_dict = {
            "entityDefs": entities_to_update
        }
        self.driver.typedefs.update(data=typedef_dict)
        print(f'Assignment of "{super_type}" Entity to existing "{ends_with}" entities Completed.\n')

    def create_or_update(self, typedef_dict, info):
        try:
            print(f"Trying to create {info} Entity")
            self.driver.typedefs.create(data=typedef_dict)
        except Conflict as ex:
            print("Exception: {0}".format(str(ex)))
            print(f"Already Exists, updating {info} Entity")
            self.driver.typedefs.update(data=typedef_dict)
        finally:
            print(f"Applied {info} Entity Definition")
            print(f"\n----------")

    @property
    def driver(self):
        return AtlasClient().driver()

    def get_schema_dict(self, schema):
        return json.loads(schema)

    def create_table_schema(self):
        self.create_or_update(self.get_schema_dict(table_schema), "Table")

    def create_column_schema(self):
        self.create_or_update(self.get_schema_dict(column_schema), "Column")

    def create_user_schema(self):
        self.create_or_update(self.get_schema_dict(user_schema), "User")

    def create_reader_schema(self):
        self.create_or_update(self.get_schema_dict(reader_schema), "Reader")

    def create_user_reader_relation(self):
        self.create_or_update(self.get_schema_dict(user_reader_relation), "User <-> Reader")

    def create_metadata_schema(self):
        self.create_or_update(self.get_schema_dict(metadata_schema), "Metadata")

    def create_table_metadata_schema(self):
        self.create_or_update(self.get_schema_dict(table_metadata_schema), "Table Metadata")

    def create_column_metadata_schema(self):
        self.create_or_update(self.get_schema_dict(column_metadata_schema), "Column Metadata")

    def create_required_entities(self):
        """
        IMPORTANT: The order of the entity definition matters.
        Please keep this order.
        :return: Creates or Updates the entity definition in Apache Atlas
        """
        self.create_table_schema()
        self.assign_subtypes(ends_with="_table", super_type="Table")
        self.create_column_schema()
        self.assign_subtypes(ends_with="_column", super_type="Column")
        self.create_user_schema()
        self.create_reader_schema()
        self.create_user_reader_relation()
        self.create_metadata_schema()
        self.create_table_metadata_schema()
        self.create_column_metadata_schema()
