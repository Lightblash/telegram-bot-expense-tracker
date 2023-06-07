import os


def get_env_var(variable: str) -> str:
    value = os.environ.get(variable)
    if value:
        # Remove the quotation marks if they exist
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
            return value

        return value

    print("Environment variable not set.")
