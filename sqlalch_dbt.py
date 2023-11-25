from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import os

Base = declarative_base()

def create_orm_class(class_name, base=Base, **fields):
    """
    Dynamically create an SQLAlchemy ORM class.

    :param class_name: Name of the class to be created.
    :param base: Base class to inherit from, default is SQLAlchemy's Base.
    :param fields: Dictionary of field names and their SQLAlchemy types.
    :return: New ORM class.
    """
    attributes = {'__tablename__': class_name.lower()}
    attributes.update(fields)
    
    return type(class_name, (base,), attributes)

models = {
    create_orm_class('User', id=Column(Integer, primary_key=True), name=Column(String), email=Column(String)),
    create_orm_class('Test', id=Column(Integer, primary_key=True), test_1=Column(String), test_2=Column(String))
}

yaml_content = "version: 2\n\nmodels:"
table_names = []

for model in models:

    # Extract table name
    table_name = model.__tablename__
    table_names.append(table_name)

    # Extract column details
    columns = model.__table__.columns
    column_details = [(column.name, str(column.type)) for column in columns]

    # Define your dbt project's model directory
    dbt_models_directory = "dbt"

    # Create SQL file for the dbt model
    yaml_content += f"""
    - name: {table_name}
      description: "Generated automatically via ORM model."
      columns:
    """
    model_sql = f"SELECT\n"
    for name, type in column_details:
        model_sql += f"    {name}, -- {type}\n"
    yaml_content += f"      - name: {name}\n            description: \"{type}\"\n"
    model_sql = model_sql.strip(",\n") + f"\nFROM {table_name}\n"
    
    model_file_path = os.path.join(dbt_models_directory, table_name + ".sql")
    with open(model_file_path, 'w') as file:
        file.write(model_sql)

yaml_file_path = os.path.join(dbt_models_directory, "_models.yml")
with open(yaml_file_path, 'w') as file:
    file.write(yaml_content)
    
built_model_names = ', '.join(table_names)

print(built_model_names  + " model files created.")
