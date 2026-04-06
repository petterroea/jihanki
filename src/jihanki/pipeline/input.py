from .env import EnvironmentVariable
from pathlib import Path
import hashlib


class FileFromVar:
    def __init__(self, schema):
        self.fieldname = schema.fieldname
        self.destination = schema.destination

    def validate(self, variables):
        if self.fieldname in variables:
            return None
        return f"File {self.destination} requires field {self.fieldname}"

    def write(self, input_dir, variables):
        # semi-random but predictable file names in the host filesystem
        host_filename = (
            hashlib.sha256(self.destination.encode("ascii")).hexdigest()[:12]
            + "_"
            + Path(self.destination).name
        )

        host_location = input_dir / host_filename

        with host_location.open("w") as f:
            f.write(variables[self.fieldname])

        return "%s:%s" % (host_location.absolute(), self.destination)


class Input:
    def __init__(self, schema):
        self.environment_variables = {}
        for key, env_schema in schema.environment.items():
            self.environment_variables[key] = EnvironmentVariable(key, env_schema)

        self.files = [FileFromVar(f) for f in schema.files]

    def validate(self, request):
        variables = request.json

        for key, value in self.environment_variables.items():
            result = self.environment_variables[key].validate(variables)
            if result is not None:
                return result

        for file in self.files:
            result = file.validate(variables)
            if result is not None:
                return result
        return None

    def get_env_variables(self, variables):
        env = {}
        for key, value in self.environment_variables.items():
            env[key] = self.environment_variables[key].get_value(variables)
        return env

    def create_variable_files(self, input_dir, variables):
        return [file.write(input_dir, variables) for file in self.files]

    def dictify(self):
        d = {}
        if self.environment_variables:
            env = {}
            for key, var in self.environment_variables.items():
                if var.source == "static":
                    env[key] = f"{var.value} (static)"
                else:
                    env[key] = f"from request field '{var.fieldname}'"
            d["Environment variables"] = env
        if self.files:
            d["Files written to container"] = {
                f.destination: f"contents from request field '{f.fieldname}'"
                for f in self.files
            }
        return d
