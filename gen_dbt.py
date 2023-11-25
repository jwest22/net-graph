import os

dbt_models_directory = "dbt"

models = {
    "model_1": {
        "sql": "SELECT * FROM source_table_1",
        "description": "This is model 1"
    },
    "model_2": {
        "sql": "SELECT * FROM source_table_2",
        "description": "This is model 2"
    }
}

yaml_content = "version: 2\n\nmodels:"

for model_name, model_info in models.items():
    model_file_path = os.path.join(dbt_models_directory, model_name + ".sql")
    with open(model_file_path, 'w') as file:
        file.write(model_info["sql"])

    yaml_content += f"""
  - name: {model_name}
    description: "{model_info['description']}"
"""

yaml_file_path = os.path.join(dbt_models_directory, "models.yml")
with open(yaml_file_path, 'w') as file:
    file.write(yaml_content)

print("Model files and combined YAML file created.")
